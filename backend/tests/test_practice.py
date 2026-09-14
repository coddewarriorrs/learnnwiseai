import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_student_token():
    res = client.post("/api/auth/login", json={
        "email": "arjun@learnwise.ai",
        "password": "LearnWise@2026"
    })
    assert res.status_code == 200
    return res.json()["access_token"]

def test_multi_subject_practice_filtering():
    token = get_student_token()
    headers = {"Authorization": f"Bearer {token}"}

    for subject in ["Physics", "Chemistry", "Biology", "Mathematics"]:
        res = client.post("/api/practice/start", json={
            "subject": subject,
            "num_questions": 2
        }, headers=headers)
        assert res.status_code == 200
        questions = res.json()
        assert len(questions) > 0
        for q in questions:
            assert q["subject_name"].lower() == subject.lower()

def test_anti_repetition_distinct_questions():
    token = get_student_token()
    headers = {"Authorization": f"Bearer {token}"}

    # First session for Physics
    res1 = client.post("/api/practice/start", json={
        "subject": "Physics",
        "num_questions": 3
    }, headers=headers)
    assert res1.status_code == 200
    batch1 = res1.json()
    ids1 = [q["id"] for q in batch1]

    # Submit answers for batch 1
    for q in batch1:
        sub_res = client.post("/api/practice/submit-answer", json={
            "question_id": q["id"],
            "selected_answer": "A",
            "time_taken_seconds": 15
        }, headers=headers)
        assert sub_res.status_code == 200

    # Second session for Physics (should prioritize unattempted questions)
    res2 = client.post("/api/practice/start", json={
        "subject": "Physics",
        "num_questions": 3
    }, headers=headers)
    assert res2.status_code == 200
    batch2 = res2.json()
    ids2 = [q["id"] for q in batch2]

    # Verify zero overlap between consecutive rounds
    overlap = set(ids1).intersection(set(ids2))
    assert len(overlap) == 0, f"Expected distinct questions, got overlap: {overlap}"
