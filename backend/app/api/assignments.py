from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.models.assignment import Assignment, AssignmentSubmission, SubmissionStatus
from app.models.class_model import Class, ClassMember
from app.schemas.assignment import (
    AssignmentCreate, AssignmentResponse, SubmissionSubmitRequest, GradeSubmissionRequest
)
from app.services.risk_engine import RiskEngine
from app.realtime.manager import ws_manager
from app.core.permissions import get_current_user, require_role, verify_teacher_class_access
from datetime import datetime, timezone

router = APIRouter(prefix="/assignments", tags=["assignments"])

@router.get("", response_model=list[AssignmentResponse])
def list_assignments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    results = []
    if current_user.role == UserRole.TEACHER:
        assignments = db.query(Assignment).filter(Assignment.teacher_id == current_user.id).all()
        for a in assignments:
            cls = db.query(Class).filter(Class.id == a.class_id).first()
            ar = AssignmentResponse.model_validate(a)
            ar.class_name = cls.name if cls else None
            results.append(ar)
    elif current_user.role == UserRole.STUDENT:
        classes = (
            db.query(ClassMember.class_id)
            .filter(ClassMember.student_id == current_user.id)
            .all()
        )
        c_ids = [c[0] for c in classes]
        assignments = db.query(Assignment).filter(Assignment.class_id.in_(c_ids)).all() if c_ids else []

        for a in assignments:
            cls = db.query(Class).filter(Class.id == a.class_id).first()
            sub = db.query(AssignmentSubmission).filter(
                AssignmentSubmission.assignment_id == a.id,
                AssignmentSubmission.student_id == current_user.id
            ).first()

            ar = AssignmentResponse.model_validate(a)
            ar.class_name = cls.name if cls else None
            ar.submission_status = sub.status if sub else SubmissionStatus.ASSIGNED
            ar.submission_grade = sub.grade if sub else None
            results.append(ar)
    else: # ADMIN
        assignments = db.query(Assignment).all()
        for a in assignments:
            cls = db.query(Class).filter(Class.id == a.class_id).first()
            ar = AssignmentResponse.model_validate(a)
            ar.class_name = cls.name if cls else None
            results.append(ar)
    return results

@router.post("", response_model=AssignmentResponse)
def create_assignment(
    req: AssignmentCreate,
    current_user: User = Depends(require_role([UserRole.TEACHER, UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    verify_teacher_class_access(req.class_id, current_user, db)

    assignment = Assignment(
        class_id=req.class_id,
        teacher_id=current_user.id,
        title=req.title,
        instructions=req.instructions,
        topic_id=req.topic_id,
        total_points=req.total_points,
        due_date=req.due_date
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    # Initialize assignment submissions for all enrolled students in the class
    members = db.query(ClassMember).filter(ClassMember.class_id == req.class_id).all()
    for m in members:
        sub = AssignmentSubmission(
            assignment_id=assignment.id,
            student_id=m.student_id,
            status=SubmissionStatus.ASSIGNED
        )
        db.add(sub)
    db.commit()

    cls = db.query(Class).filter(Class.id == req.class_id).first()
    ar = AssignmentResponse.model_validate(assignment)
    ar.class_name = cls.name if cls else None
    return ar

@router.post("/{assignment_id}/submit")
async def submit_assignment(
    assignment_id: int,
    req: SubmissionSubmitRequest,
    current_user: User = Depends(require_role([UserRole.STUDENT])),
    db: Session = Depends(get_db)
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    submission = db.query(AssignmentSubmission).filter(
        AssignmentSubmission.assignment_id == assignment_id,
        AssignmentSubmission.student_id == current_user.id
    ).first()

    if not submission:
        submission = AssignmentSubmission(
            assignment_id=assignment_id,
            student_id=current_user.id
        )
        db.add(submission)

    submission.content = req.content
    submission.status = SubmissionStatus.COMPLETED
    submission.submitted_at = datetime.now(timezone.utc)
    db.commit()

    # Recalculate risk on assignment submission
    RiskEngine.calculate_student_risk(current_user.id, db)

    # Broadcast event
    await ws_manager.broadcast_event(
        event_type="ASSIGNMENT_SUBMITTED",
        data={
            "student_id": current_user.id,
            "student_name": current_user.full_name,
            "assignment_title": assignment.title
        },
        target_teacher_ids=[assignment.teacher_id]
    )

    return {"message": "Assignment submitted successfully!", "status": "COMPLETED"}

@router.post("/{assignment_id}/grade/{student_id}")
def grade_submission(
    assignment_id: int,
    student_id: int,
    req: GradeSubmissionRequest,
    current_user: User = Depends(require_role([UserRole.TEACHER, UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment or assignment.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to grade this assignment")

    submission = db.query(AssignmentSubmission).filter(
        AssignmentSubmission.assignment_id == assignment_id,
        AssignmentSubmission.student_id == student_id
    ).first()

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    submission.grade = req.grade
    submission.feedback = req.feedback
    db.commit()

    # Update risk score
    RiskEngine.calculate_student_risk(student_id, db)

    return {"message": "Submission graded successfully", "grade": req.grade}
