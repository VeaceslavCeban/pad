import os
import sys

# Добавляем корень сервиса (users_service) в sys.path, чтобы увидеть пакет app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_products_returns_demo():
    resp = client.get("/products")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_create_product():
    payload = {"name": "Test Product", "price": 99.99}
    resp = client.post("/products", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]
    assert "id" in data
