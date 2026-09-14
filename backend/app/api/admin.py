from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.models.class_model import Class
from app.models.syllabus import CurriculumNode
from app.models.question import Question, DifficultyLevel
from app.models.mastery import StudentTopicMastery
from app.schemas.auth import UserResponse
from app.core.permissions import get_current_user, require_role
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

router = APIRouter(prefix="/admin", tags=["admin"])

class UpdateRoleRequest(BaseModel):
    role: UserRole

class CreateQuestionRequest(BaseModel):
    topic_id: int
    title: str
    prompt: str
    options: List[Dict[str, Any]]
    correct_answer: str
    explanation: str
    prerequisite_hint: Optional[str] = None
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    points: int = 10

@router.get("/dashboard")
def get_admin_dashboard(
    current_user: User = Depends(require_role([UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    total_users = db.query(User).count()
    total_students = db.query(User).filter(User.role == UserRole.STUDENT).count()
    total_teachers = db.query(User).filter(User.role == UserRole.TEACHER).count()
    total_classes = db.query(Class).count()
    total_curriculum = db.query(CurriculumNode).count()
    total_questions = db.query(Question).count()

    masteries = db.query(StudentTopicMastery).all()
    avg_mastery = round(sum(m.mastery_score for m in masteries) / len(masteries), 1) if masteries else 0.0

    return {
        "metrics": {
            "total_users": total_users,
            "total_students": total_students,
            "total_teachers": total_teachers,
            "total_classes": total_classes,
            "total_curriculum_nodes": total_curriculum,
            "total_questions": total_questions,
            "platform_average_mastery": avg_mastery
        }
    }

@router.get("/users", response_model=List[UserResponse])
def list_users(
    role: UserRole = None,
    current_user: User = Depends(require_role([UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    users = query.all()
    return [UserResponse.model_validate(u) for u in users]

@router.patch("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    req: UpdateRoleRequest,
    current_user: User = Depends(require_role([UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = req.role
    db.commit()
    return {"message": f"Updated {user.full_name}'s role to {req.role.value}"}

@router.post("/questions")
def create_question(
    req: CreateQuestionRequest,
    current_user: User = Depends(require_role([UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    topic = db.query(CurriculumNode).filter(CurriculumNode.id == req.topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    q = Question(
        topic_id=req.topic_id,
        title=req.title,
        prompt=req.prompt,
        options=req.options,
        correct_answer=req.correct_answer,
        explanation=req.explanation,
        prerequisite_hint=req.prerequisite_hint,
        difficulty=req.difficulty,
        points=req.points
    )
    db.add(q)
    db.commit()
    db.refresh(q)
    return {"message": "Question created successfully", "id": q.id}
