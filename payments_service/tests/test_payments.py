import os
import sys

# Добавляем корень сервиса (users_service) в sys.path, чтобы увидеть пакет app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
