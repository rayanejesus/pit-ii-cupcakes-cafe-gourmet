import os

# The API tests use the local database and must never drop a shared database.
os.environ.pop("DATABASE_URL", None)
os.environ["ORDER_MANAGEMENT_TOKEN"] = "test-management-token"

from fastapi.testclient import TestClient

from app.database.connection import Base, engine
from app.main import app
from seed import seed


def setup_module():
    Base.metadata.drop_all(bind=engine)
    seed()


client = TestClient(app)
management_headers = {"X-Order-Management-Token": "test-management-token"}
order_headers = {"Idempotency-Key": "test-order-key-0001"}


def test_health_and_catalog():
    assert client.get("/api/health").json()["status"] == "ok"
    products = client.get("/api/products").json()
    assert len(products) == 10
    assert any(product["name"] == "Red Velvet" for product in products)
    assert len({product["image_url"] for product in products}) == 10


def test_seed_is_idempotent():
    seed()
    seed()
    assert len(client.get("/api/products").json()) == 10


def test_order_recalculates_total_and_payment():
    response = client.post("/api/orders", json={
        "customer_name": "Ana Souza",
        "customer_email": "ana@example.com",
        "address": "Rua das Flores, 10",
        "payment_method": "PIX",
        "items": [{"product_id": 1, "quantity": 2}],
    }, headers=order_headers)
    assert response.status_code == 201
    order = response.json()
    assert order["subtotal"] == "37.80"
    assert order["total"] == "46.30"
    paid = client.post(f"/api/orders/{order['id']}/pay", headers=management_headers)
    assert paid.status_code == 200
    assert paid.json()["status"] == "PAGO"


def test_invalid_stock_and_transition():
    response = client.post("/api/orders", json={
        "customer_name": "João Lima",
        "customer_email": "joao@example.com",
        "address": "Avenida Central, 100",
        "payment_method": "CARTAO",
        "items": [{"product_id": 1, "quantity": 50}],
    }, headers={"Idempotency-Key": "invalid-stock-key-0001"})
    assert response.status_code == 409
    transition = client.patch("/api/orders/1/status?status=ENTREGUE", headers=management_headers)
    assert transition.status_code == 409


def test_order_read_requires_management_token():
    response = client.get("/api/orders")
    assert response.status_code == 401


def test_cors_preflight_for_catalog_route():
    response = client.options(
        "/api/products?search=",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
    assert "GET" in response.headers["access-control-allow-methods"]


def test_cors_preflight_for_order_creation_with_idempotency_header():
    response = client.options(
        "/api/orders",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type,idempotency-key",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
    assert "idempotency-key" in response.headers["access-control-allow-headers"].lower()


def test_invalid_order_returns_json_without_persisting():
    response = client.post(
        "/api/orders",
        headers={"Idempotency-Key": "invalid-json-key-0001"},
        content='{"customer_name": "Incompleto"}',
    )
    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/json")
    assert response.json()["detail"]


def test_cors_rejects_unconfigured_origin():
    response = client.options(
        "/api/products",
        headers={
            "Origin": "https://not-configured.example",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers


def test_order_requires_idempotency_key():
    response = client.post("/api/orders", json={
        "customer_name": "Sem Chave",
        "customer_email": "sem-chave@example.com",
        "address": "Avenida Central, 100",
        "payment_method": "PIX",
        "items": [{"product_id": 1, "quantity": 1}],
    })
    assert response.status_code == 422


def test_multiple_products_total_and_duplicate_request():
    payload = {
        "customer_name": "Maria Souza",
        "customer_email": "maria@example.com",
        "address": "Rua das Flores, 10",
        "payment_method": "PIX",
        "items": [{"product_id": 2, "quantity": 1}, {"product_id": 3, "quantity": 2}],
    }
    headers = {"Idempotency-Key": "multiple-products-key-0001"}
    first = client.post("/api/orders", json=payload, headers=headers)
    duplicate = client.post("/api/orders", json=payload, headers=headers)
    assert first.status_code == 201
    assert duplicate.status_code == 201
    assert duplicate.json()["id"] == first.json()["id"]
    assert first.json()["subtotal"] == "55.70"
    assert first.json()["shipping"] == "8.50"
    assert first.json()["total"] == "64.20"
    assert len(first.json()["items"]) == 2


def test_same_idempotency_key_with_different_payload_returns_conflict():
    headers = {"Idempotency-Key": "different-payload-key-0001"}
    first = client.post("/api/orders", json={
        "customer_name": "Paula Souza",
        "customer_email": "paula@example.com",
        "address": "Rua Um, 10",
        "payment_method": "PIX",
        "items": [{"product_id": 4, "quantity": 1}],
    }, headers=headers)
    different = client.post("/api/orders", json={
        "customer_name": "Paula Souza",
        "customer_email": "paula@example.com",
        "address": "Rua Dois, 20",
        "payment_method": "PIX",
        "items": [{"product_id": 4, "quantity": 2}],
    }, headers=headers)
    assert first.status_code == 201
    assert different.status_code == 409
    assert "chave de idempotência" in different.json()["detail"]
