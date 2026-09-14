from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.models.class_model import Class, ClassMember
from app.models.risk import RiskPrediction, RiskLevel
from app.models.mastery import StudentTopicMastery, LearningActivity
from app.models.syllabus import CurriculumNode
from app.schemas.risk import RiskResponse, EarlyWarningStudent
from app.services.risk_engine import RiskEngine
from app.core.permissions import get_current_user, require_role, verify_teacher_student_access
from typing import List

router = APIRouter(prefix="/risk", tags=["risk"])

@router.post("/calculate/{student_id}", response_model=RiskResponse)
def calculate_risk(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == UserRole.STUDENT and current_user.id != student_id:
        raise HTTPException(status_code=403, detail="Cannot calculate risk for another student")
    if current_user.role == UserRole.TEACHER:
        verify_teacher_student_access(student_id, current_user, db)

    prediction = RiskEngine.calculate_student_risk(student_id, db)
    student = db.query(User).filter(User.id == student_id).first()

    resp = RiskResponse.model_validate(prediction)
    resp.student_name = student.full_name if student else None
    return resp

@router.get("/early-warning", response_model=List[EarlyWarningStudent])
def get_early_warning_dashboard(
    current_user: User = Depends(require_role([UserRole.TEACHER, UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    teacher_id = current_user.id
    classes = db.query(Class).filter(Class.teacher_id == teacher_id).all() if current_user.role == UserRole.TEACHER else db.query(Class).all()
    class_ids = [c.id for c in classes]

    members = db.query(ClassMember).filter(ClassMember.class_id.in_(class_ids)).all() if class_ids else []
    student_ids = list(set(m.student_id for m in members))

    results = []
    for sid in student_ids:
        student = db.query(User).filter(User.id == sid).first()
        if not student:
            continue

        risk = db.query(RiskPrediction).filter(RiskPrediction.student_id == sid).first()
        if not risk:
            risk = RiskEngine.calculate_student_risk(sid, db)

        # Find top weak topic
        weak_mastery = (
            db.query(StudentTopicMastery, CurriculumNode)
            .join(CurriculumNode, CurriculumNode.id == StudentTopicMastery.topic_id)
            .filter(StudentTopicMastery.student_id == sid)
            .order_by(StudentTopicMastery.mastery_score.asc())
            .first()
        )
        weak_title = weak_mastery[1].title if weak_mastery else "Algebra Fundamentals"

        # Find student's class name
        c_member = db.query(ClassMember, Class).join(Class, Class.id == ClassMember.class_id).filter(ClassMember.student_id == sid).first()
        c_name = c_member[1].name if c_member else "General Class"

        # Last activity
        last_act = (
            db.query(LearningActivity)
            .filter(LearningActivity.student_id == sid)
            .order_by(LearningActivity.timestamp.desc())
            .first()
        )

        results.append(EarlyWarningStudent(
            student_id=student.id,
            student_name=student.full_name,
            student_email=student.email,
            class_name=c_name,
            risk_score=risk.composite_risk_score,
            risk_level=risk.risk_level,
            top_weak_topic=weak_title,
            reasons=risk.reasons,
            recommended_action=risk.recommended_action or "Review prerequisite concepts.",
            last_activity=last_act.timestamp if last_act else None
        ))

    # Sort so HIGH risk appears first, ordered by score descending
    results.sort(key=lambda x: x.risk_score, reverse=True)
    return results
