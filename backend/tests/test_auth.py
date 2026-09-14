import pytest
from app.models.user import User, UserRole
from app.core.security import verify_password

def test_login_teacher(client):
    res = client.post("/api/auth/login", json={
        "email": "teacher@learnwise.ai",
        "password": "LearnWise@2026"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["user"]["role"] == "TEACHER"
    assert data["user"]["email"] == "teacher@learnwise.ai"

def test_login_student(client):
    res = client.post("/api/auth/login", json={
        "email": "arjun@learnwise.ai",
        "password": "LearnWise@2026"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["user"]["role"] == "STUDENT"

def test_login_invalid_password(client):
    res = client.post("/api/auth/login", json={
        "email": "teacher@learnwise.ai",
        "password": "WrongPassword123"
    })
    assert res.status_code == 401

def test_register_duplicate_email(client):
    res = client.post("/api/auth/register", json={
        "email": "arjun@learnwise.ai",
        "password": "NewPassword123",
        "full_name": "Arjun Duplicate",
        "role": "STUDENT"
    })
    assert res.status_code == 400
    assert "already exists" in res.json()["detail"].lower()
