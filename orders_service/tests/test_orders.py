import os
import sys

# Добавляем корень сервиса (users_service) в sys.path, чтобы увидеть пакет app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_list_orders():
    payload = {"user_id": 1, "product_ids": [1, 2], "total": 30.0}
    resp = client.post("/orders", json=payload)
    assert resp.status_code == 200
    order = resp.json()
    assert order["total"] == 30.0

    resp2 = client.get("/orders")
    assert resp2.status_code == 200
    data = resp2.json()
    assert any(o["id"] == order["id"] for o in data)
