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


def test_health_and_catalog():
    assert client.get("/api/health").json()["status"] == "ok"
    products = client.get("/api/products").json()
    assert len(products) == 10
    assert any(product["name"] == "Red Velvet" for product in products)


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
    })
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
    })
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
