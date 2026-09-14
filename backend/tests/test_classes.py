import pytest
from app.models.user import User
from app.models.class_model import Class, ClassMember

def test_prevent_duplicate_class_membership(client):
    login_res = client.post("/api/auth/login", json={
        "email": "arjun@learnwise.ai",
        "password": "LearnWise@2026"
    })
    token = login_res.json()["access_token"]

    # Arjun is already enrolled in MATH11
    res = client.post("/api/classes/join", json={"class_code": "MATH11"}, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 400
    assert "already enrolled" in res.json()["detail"].lower()

def test_verify_invite_token(client):
    res = client.get("/api/classes/join/verify/math11-invite-token-abc")
    assert res.status_code == 200
    data = res.json()
    assert data["valid"] is True
    assert "Mathematics" in data["class_name"]

def test_verify_invalid_invite_token(client):
    res = client.get("/api/classes/join/verify/non-existent-token-999")
    assert res.status_code == 404
