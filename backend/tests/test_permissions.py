import pytest
from app.models.user import User, UserRole
from app.models.class_model import Class, ClassMember
from app.core.security import get_password_hash

def test_student_cannot_access_teacher_dashboard(client):
    login_res = client.post("/api/auth/login", json={
        "email": "arjun@learnwise.ai",
        "password": "LearnWise@2026"
    })
    token = login_res.json()["access_token"]
    res = client.get("/api/teacher/dashboard", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 403

def test_teacher_cannot_access_other_teacher_student(client, db):
    # Create Teacher B
    pw_hash = get_password_hash("TeacherB@2026")
    teacher_b = db.query(User).filter(User.email == "teacher_b@learnwise.ai").first()
    if not teacher_b:
        teacher_b = User(
            email="teacher_b@learnwise.ai",
            hashed_password=pw_hash,
            full_name="Dr. Second Teacher",
            role=UserRole.TEACHER
        )
        db.add(teacher_b)
        db.commit()
        db.refresh(teacher_b)

    # Login as Teacher B
    login_b = client.post("/api/auth/login", json={
        "email": "teacher_b@learnwise.ai",
        "password": "TeacherB@2026"
    })
    token_b = login_b.json()["access_token"]

    # Arjun belongs only to Dr. Vance's class, NOT Teacher B
    arjun = db.query(User).filter(User.email == "arjun@learnwise.ai").first()
    res = client.get(f"/api/teacher/students/{arjun.id}", headers={"Authorization": f"Bearer {token_b}"})
    assert res.status_code == 403
    assert "does not belong to any of your classes" in res.json()["detail"].lower()
