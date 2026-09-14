from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.models.class_model import Class, ClassMember
from app.models.mastery import StudentTopicMastery, MasteryStatus, LearningActivity
from app.models.syllabus import CurriculumNode
from app.models.risk import RiskPrediction, RiskLevel
from app.models.intervention import Intervention, TeacherStudentNote
from app.models.assessment import AssessmentAttempt
from app.models.assignment import AssignmentSubmission, Assignment
from app.schemas.intervention import TeacherNoteCreate, TeacherNoteResponse
from app.services.risk_engine import RiskEngine
from app.core.permissions import get_current_user, require_role, verify_teacher_student_access
from typing import List, Dict, Any

router = APIRouter(prefix="/teacher", tags=["teacher"])

@router.get("/dashboard")
def get_teacher_dashboard(
    current_user: User = Depends(require_role([UserRole.TEACHER, UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    teacher_id = current_user.id
    classes = db.query(Class).filter(Class.teacher_id == teacher_id).all()
    class_ids = [c.id for c in classes]

    members = db.query(ClassMember).filter(ClassMember.class_id.in_(class_ids)).all() if class_ids else []
    student_ids = list(set(m.student_id for m in members))

    total_students = len(student_ids)

    # Masteries for all students
    masteries = db.query(StudentTopicMastery).filter(StudentTopicMastery.student_id.in_(student_ids)).all() if student_ids else []
    avg_mastery = round(sum(m.mastery_score for m in masteries) / len(masteries), 1) if masteries else 0.0

    # Risk counts
    risks = db.query(RiskPrediction).filter(RiskPrediction.student_id.in_(student_ids)).all() if student_ids else []
    high_risk_count = sum(1 for r in risks if r.risk_level == RiskLevel.HIGH)
    med_risk_count = sum(1 for r in risks if r.risk_level == RiskLevel.MEDIUM)
    low_risk_count = sum(1 for r in risks if r.risk_level == RiskLevel.LOW)

    # Topic weaknesses across classes
    weakness_stats: Dict[int, Dict[str, Any]] = {}
    for m in masteries:
        if m.topic_id not in weakness_stats:
            node = db.query(CurriculumNode).filter(CurriculumNode.id == m.topic_id).first()
            weakness_stats[m.topic_id] = {
                "topic": node.title if node else f"Topic #{m.topic_id}",
                "total_score": 0.0,
                "count": 0,
                "critical_count": 0
            }
        weakness_stats[m.topic_id]["total_score"] += m.mastery_score
        weakness_stats[m.topic_id]["count"] += 1
        if m.status == MasteryStatus.CRITICAL:
            weakness_stats[m.topic_id]["critical_count"] += 1

    topic_weakness_chart = []
    for tid, data in weakness_stats.items():
        avg_score = round(data["total_score"] / data["count"], 1) if data["count"] > 0 else 0.0
        topic_weakness_chart.append({
            "topic": data["topic"],
            "average_mastery": avg_score,
            "students_critical": data["critical_count"]
        })
    topic_weakness_chart.sort(key=lambda x: x["average_mastery"])

    # Recent activity feed
    activities = (
        db.query(LearningActivity, User)
        .join(User, User.id == LearningActivity.student_id)
        .filter(LearningActivity.student_id.in_(student_ids))
        .order_by(LearningActivity.timestamp.desc())
        .limit(10)
        .all()
    ) if student_ids else []

    return {
        "metrics": {
            "total_students": total_students,
            "total_classes": len(classes),
            "average_mastery": avg_mastery,
            "high_risk_count": high_risk_count,
            "medium_risk_count": med_risk_count,
            "low_risk_count": low_risk_count,
            "pending_interventions": db.query(Intervention).filter(Intervention.teacher_id == teacher_id, Intervention.status != "COMPLETED").count()
        },
        "risk_distribution": [
            {"name": "High Risk", "value": high_risk_count, "color": "#EF4444"},
            {"name": "Medium Risk", "value": med_risk_count, "color": "#F59E0B"},
            {"name": "Low Risk", "value": low_risk_count, "color": "#10B981"}
        ],
        "topic_weaknesses": topic_weakness_chart[:5],
        "classes": [{"id": c.id, "name": c.name, "subject": c.subject, "code": c.class_code} for c in classes],
        "activity_feed": [
            {
                "id": act.id,
                "student_name": user.full_name,
                "student_id": user.id,
                "title": act.title,
                "type": act.activity_type,
                "score": act.score,
                "timestamp": act.timestamp
            }
            for act, user in activities
        ]
    }

@router.get("/students")
def get_teacher_students(
    current_user: User = Depends(require_role([UserRole.TEACHER, UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    teacher_id = current_user.id
    classes = db.query(Class).filter(Class.teacher_id == teacher_id).all()
    class_ids = [c.id for c in classes]

    members = db.query(ClassMember).filter(ClassMember.class_id.in_(class_ids)).all() if class_ids else []
    student_ids = list(set(m.student_id for m in members))

    students = db.query(User).filter(User.id.in_(student_ids)).all() if student_ids else []
    results = []

    for s in students:
        risk = db.query(RiskPrediction).filter(RiskPrediction.student_id == s.id).first()
        if not risk:
            risk = RiskEngine.calculate_student_risk(s.id, db)
        
        masteries = db.query(StudentTopicMastery).filter(StudentTopicMastery.student_id == s.id).all()
        avg_m = round(sum(m.mastery_score for m in masteries) / len(masteries), 1) if masteries else 0.0

        # Enrolled classes for this student under this teacher
        student_classes = (
            db.query(Class)
            .join(ClassMember, ClassMember.class_id == Class.id)
            .filter(Class.teacher_id == teacher_id, ClassMember.student_id == s.id)
            .all()
        )

        results.append({
            "id": s.id,
            "name": s.full_name,
            "email": s.email,
            "grade": s.grade_level,
            "classes": [c.name for c in student_classes],
            "average_mastery": avg_m,
            "risk_score": risk.composite_risk_score,
            "risk_level": risk.risk_level.value,
            "risk_reasons": risk.reasons,
            "recommended_action": risk.recommended_action
        })

    # Sort by highest risk score first
    results.sort(key=lambda x: x["risk_score"], reverse=True)
    return results

@router.get("/students/{student_id}")
def get_teacher_student_profile(
    student_id: int,
    current_user: User = Depends(require_role([UserRole.TEACHER, UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    # Verify strict data isolation: teacher can only see their own students
    student = verify_teacher_student_access(student_id, current_user, db)

    risk = db.query(RiskPrediction).filter(RiskPrediction.student_id == student.id).first()
    if not risk:
        risk = RiskEngine.calculate_student_risk(student.id, db)

    masteries = (
        db.query(StudentTopicMastery, CurriculumNode)
        .join(CurriculumNode, CurriculumNode.id == StudentTopicMastery.topic_id)
        .filter(StudentTopicMastery.student_id == student.id)
        .all()
    )

    interventions = (
        db.query(Intervention)
        .filter(Intervention.student_id == student.id)
        .order_by(Intervention.created_at.desc())
        .all()
    )

    notes = (
        db.query(TeacherStudentNote)
        .filter(TeacherStudentNote.teacher_id == current_user.id, TeacherStudentNote.student_id == student.id)
        .order_by(TeacherStudentNote.created_at.desc())
        .all()
    )

    activities = (
        db.query(LearningActivity)
        .filter(LearningActivity.student_id == student.id)
        .order_by(LearningActivity.timestamp.desc())
        .limit(10)
        .all()
    )

    attempts = (
        db.query(AssessmentAttempt)
        .filter(AssessmentAttempt.student_id == student.id)
        .order_by(AssessmentAttempt.submitted_at.desc())
        .all()
    )

    return {
        "student": {
            "id": student.id,
            "name": student.full_name,
            "email": student.email,
            "grade": student.grade_level
        },
        "risk": {
            "score": risk.composite_risk_score,
            "level": risk.risk_level.value,
            "performance_risk": risk.performance_risk,
            "attendance_risk": risk.attendance_risk,
            "assignment_risk": risk.assignment_risk,
            "engagement_risk": risk.engagement_risk,
            "reasons": risk.reasons,
            "recommended_action": risk.recommended_action
        },
        "masteries": [
            {
                "topic_id": node.id,
                "topic": node.title,
                "score": m.mastery_score,
                "status": m.status.value,
                "total_attempts": m.total_attempts,
                "correct_attempts": m.correct_attempts
            }
            for m, node in masteries
        ],
        "interventions": [
            {
                "id": i.id,
                "type": i.type.value,
                "reason": i.reason,
                "action": i.action,
                "status": i.status.value,
                "created_at": i.created_at
            }
            for i in interventions
        ],
        "notes": [
            {
                "id": n.id,
                "note": n.note,
                "created_at": n.created_at
            }
            for n in notes
        ],
        "recent_activity": [
            {
                "title": act.title,
                "type": act.activity_type,
                "score": act.score,
                "timestamp": act.timestamp
            }
            for act in activities
        ],
        "assessment_history": [
            {
                "id": a.id,
                "percentage": a.percentage,
                "time_taken": a.time_taken_seconds,
                "submitted_at": a.submitted_at
            }
            for a in attempts
        ]
    }

@router.post("/notes", response_model=TeacherNoteResponse)
def create_teacher_note(
    req: TeacherNoteCreate,
    current_user: User = Depends(require_role([UserRole.TEACHER, UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    verify_teacher_student_access(req.student_id, current_user, db)
    note = TeacherStudentNote(
        teacher_id=current_user.id,
        student_id=req.student_id,
        note=req.note
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return TeacherNoteResponse.model_validate(note)
