import os
import sys

# Добавляем корень сервиса (users_service) в sys.path, чтобы увидеть пакет app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_inventory():
    resp = client.get("/inventory")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1
