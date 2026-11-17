from fastapi.testclient import TestClient

from app.database.connection import Base, engine
from app.main import app
from seed import seed


def setup_module():
    Base.metadata.drop_all(bind=engine)
    seed()


client = TestClient(app)


def test_health_and_catalog():
    assert client.get("/api/health").json()["status"] == "ok"
    products = client.get("/api/products").json()
    assert len(products) == 10
    assert any(product["name"] == "Red Velvet" for product in products)


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
    paid = client.post(f"/api/orders/{order['id']}/pay")
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
    transition = client.patch("/api/orders/1/status?status=ENTREGUE")
    assert transition.status_code == 409
