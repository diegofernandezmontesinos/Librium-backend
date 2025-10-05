# tests/test_auth.py
import json
from app import models
from app.database import Base


def test_register_and_login(client):
    # Register
    payload = {"username": "testuser", "password": "Test1234!"}
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["username"] == "testuser"
    assert "id" in data

    # Login (captcha skipped/optional)
    r2 = client.post("/auth/login", json={**payload, "captchaToken": "token"})
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["status"] == 200
    assert data2["username"] == "testuser"

    # Check cookie set
    cookies = r2.cookies
    assert "autorizado" in cookies
