from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.models.intervention import Intervention, InterventionStatus
from app.models.syllabus import CurriculumNode
from app.schemas.intervention import InterventionCreate, InterventionUpdate, InterventionResponse
from app.services.risk_engine import RiskEngine
from app.realtime.manager import ws_manager
from app.core.permissions import get_current_user, require_role, verify_teacher_student_access
from datetime import datetime, timezone

router = APIRouter(prefix="/interventions", tags=["interventions"])

@router.get("", response_model=list[InterventionResponse])
def list_interventions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == UserRole.TEACHER:
        items = db.query(Intervention).filter(Intervention.teacher_id == current_user.id).order_by(Intervention.created_at.desc()).all()
    elif current_user.role == UserRole.STUDENT:
        items = db.query(Intervention).filter(Intervention.student_id == current_user.id).order_by(Intervention.created_at.desc()).all()
    else:
        items = db.query(Intervention).order_by(Intervention.created_at.desc()).all()

    results = []
    for item in items:
        student = db.query(User).filter(User.id == item.student_id).first()
        teacher = db.query(User).filter(User.id == item.teacher_id).first()
        topic = db.query(CurriculumNode).filter(CurriculumNode.id == item.topic_id).first() if item.topic_id else None
        
        ir = InterventionResponse.model_validate(item)
        ir.student_name = student.full_name if student else None
        ir.teacher_name = teacher.full_name if teacher else None
        ir.topic_title = topic.title if topic else None
        results.append(ir)
    return results

@router.post("", response_model=InterventionResponse)
async def create_intervention(
    req: InterventionCreate,
    current_user: User = Depends(require_role([UserRole.TEACHER, UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    student = verify_teacher_student_access(req.student_id, current_user, db)

    intervention = Intervention(
        student_id=req.student_id,
        teacher_id=current_user.id,
        topic_id=req.topic_id,
        type=req.type,
        reason=req.reason,
        action=req.action,
        status=InterventionStatus.ASSIGNED
    )
    db.add(intervention)
    db.commit()
    db.refresh(intervention)

    topic = db.query(CurriculumNode).filter(CurriculumNode.id == req.topic_id).first() if req.topic_id else None

    # Broadcast event
    await ws_manager.broadcast_event(
        event_type="INTERVENTION_CREATED",
        data={
            "intervention_id": intervention.id,
            "student_id": student.id,
            "student_name": student.full_name,
            "action": intervention.action,
            "type": intervention.type.value
        },
        target_teacher_ids=[current_user.id]
    )

    resp = InterventionResponse.model_validate(intervention)
    resp.student_name = student.full_name
    resp.teacher_name = current_user.full_name
    resp.topic_title = topic.title if topic else None
    return resp

@router.patch("/{intervention_id}/status", response_model=InterventionResponse)
async def update_intervention_status(
    intervention_id: int,
    req: InterventionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    intervention = db.query(Intervention).filter(Intervention.id == intervention_id).first()
    if not intervention:
        raise HTTPException(status_code=404, detail="Intervention not found")

    if current_user.role == UserRole.STUDENT and intervention.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this intervention")

    intervention.status = req.status
    if req.status == InterventionStatus.COMPLETED:
        intervention.completed_at = datetime.now(timezone.utc)
        # Reassess and recalculate risk score on completion!
        RiskEngine.calculate_student_risk(intervention.student_id, db)

    db.commit()
    db.refresh(intervention)

    student = db.query(User).filter(User.id == intervention.student_id).first()
    teacher = db.query(User).filter(User.id == intervention.teacher_id).first()
    topic = db.query(CurriculumNode).filter(CurriculumNode.id == intervention.topic_id).first() if intervention.topic_id else None

    # Broadcast update
    await ws_manager.broadcast_event(
        event_type="INTERVENTION_STATUS_CHANGED",
        data={
            "intervention_id": intervention.id,
            "status": intervention.status.value,
            "student_name": student.full_name if student else "Student"
        },
        target_teacher_ids=[intervention.teacher_id]
    )

    resp = InterventionResponse.model_validate(intervention)
    resp.student_name = student.full_name if student else None
    resp.teacher_name = teacher.full_name if teacher else None
    resp.topic_title = topic.title if topic else None
    return resp
