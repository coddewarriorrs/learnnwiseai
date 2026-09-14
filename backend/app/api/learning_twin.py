from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.core.permissions import get_current_user, require_role
from app.schemas.learning_twin import StudentLearningTwinResponse, ResetProfileResponse
from app.services.smart_practice_engine import SmartPracticeEngine
from app.services.reset_service import LearningProfileResetService
from typing import Dict, Any

router = APIRouter(prefix="/twin", tags=["learning-twin"])

@router.get("/me", response_model=StudentLearningTwinResponse)
def get_my_learning_twin(
    current_user: User = Depends(require_role([UserRole.STUDENT])),
    db: Session = Depends(get_db)
):
    """
    Returns the current student's full Personal Learning Twin profile:
    - Real-time overall mastery & risk
    - Misconception fingerprint (recurring mistake types)
    - Prerequisite knowledge gaps
    - Learning Recovery Mode status (if struggling)
    - Possible struggle / disengagement signal
    - Knowledge decay alerts
    - Timeline progression milestones
    - Single highest-leverage Next Best Action
    - Predictive What-If simulations
    """
    profile = SmartPracticeEngine.get_full_twin_profile(student_id=current_user.id, db=db)
    return profile

@router.get("/student/{student_id}", response_model=StudentLearningTwinResponse)
def get_student_learning_twin(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Allows teachers and admins to inspect any student's Learning Twin.
    Students can only view their own Learning Twin.
    """
    if current_user.role == UserRole.STUDENT and current_user.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own Personal Learning Twin."
        )

    profile = SmartPracticeEngine.get_full_twin_profile(student_id=student_id, db=db)
    return profile

@router.post("/reset-profile", response_model=ResetProfileResponse)
def reset_student_profile(
    target_student_id: int = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Completely resets student learning data (attempts, mastery, activity, twin state)
    to establish a fresh diagnostic profile, while strictly preserving user accounts,
    classes, curriculum, and questions.
    """
    # If student, can only reset self
    if current_user.role == UserRole.STUDENT:
        student_id = current_user.id
    else:
        student_id = target_student_id or current_user.id

    LearningProfileResetService.reset_single_student(student_id=student_id, db=db)
    return ResetProfileResponse(
        success=True,
        message="Learning profile and Personal Learning Twin successfully reset to fresh initial state.",
        student_id=student_id
    )
