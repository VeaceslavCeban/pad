import os
import sys

# Добавляем корень сервиса (users_service) в sys.path, чтобы увидеть пакет app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_send_and_list_notifications():
    payload = {"recipient": "user@example.com", "message": "Hello"}
    resp = client.post("/notifications", json=payload)
    assert resp.status_code == 200

    resp2 = client.get("/notifications")
    assert resp2.status_code == 200
    data = resp2.json()
    assert any(n["recipient"] == "user@example.com" for n in data)
