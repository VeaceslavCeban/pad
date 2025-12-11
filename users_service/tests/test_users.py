
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_users_returns_demo():
    resp = client.get("/users")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_create_user():
    payload = {"name": "Test User", "email": "test@example.com"}
    resp = client.post("/users", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert "id" in data
