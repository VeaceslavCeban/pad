
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_process_payment():
    payload = {"order_id": 1, "amount": 30.0, "method": "card"}
    resp = client.post("/payments", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert "Оплата" in data["message"]
