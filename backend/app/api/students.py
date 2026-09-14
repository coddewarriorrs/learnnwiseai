from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.models.class_model import Class, ClassMember
from app.models.mastery import StudentTopicMastery, MasteryStatus, LearningActivity
from app.models.syllabus import CurriculumNode
from app.models.risk import RiskPrediction, RiskLevel
from app.models.assignment import Assignment, AssignmentSubmission, SubmissionStatus
from app.models.assessment import AssessmentAttempt
from app.models.intervention import Intervention
from app.schemas.mastery import StudentMasteryOverview, TopicMasteryItem
from app.schemas.risk import RiskResponse
from app.schemas.ai import LearningPathResponse
from app.services.risk_engine import RiskEngine
from app.services.learning_path_engine import LearningPathEngine
from app.core.permissions import get_current_user, require_role
from typing import List, Dict, Any

router = APIRouter(prefix="/students", tags=["students"])

@router.get("/me/dashboard")
def get_student_dashboard(
    current_user: User = Depends(require_role([UserRole.STUDENT])),
    db: Session = Depends(get_db)
):
    student_id = current_user.id

    # Topic Masteries
    masteries = (
        db.query(StudentTopicMastery, CurriculumNode)
        .join(CurriculumNode, CurriculumNode.id == StudentTopicMastery.topic_id)
        .filter(StudentTopicMastery.student_id == student_id)
        .all()
    )

    total_topics = len(masteries)
    mastered_count = sum(1 for m, _ in masteries if m.status == MasteryStatus.STRONG)
    attention_count = sum(1 for m, _ in masteries if m.status == MasteryStatus.NEEDS_PRACTICE)
    critical_count = sum(1 for m, _ in masteries if m.status == MasteryStatus.CRITICAL)
    avg_mastery = round(sum(m.mastery_score for m, _ in masteries) / total_topics, 1) if total_topics > 0 else 0.0

    # Risk Prediction
    risk = db.query(RiskPrediction).filter(RiskPrediction.student_id == student_id).first()
    if not risk:
        risk = RiskEngine.calculate_student_risk(student_id, db)

    # Classes
    classes = (
        db.query(Class)
        .join(ClassMember, ClassMember.class_id == Class.id)
        .filter(ClassMember.student_id == student_id)
        .all()
    )

    # Pending Assignments
    assignments = (
        db.query(Assignment, AssignmentSubmission)
        .outerjoin(
            AssignmentSubmission,
            (AssignmentSubmission.assignment_id == Assignment.id) & (AssignmentSubmission.student_id == student_id)
        )
        .filter(Assignment.class_id.in_([c.id for c in classes]))
        .limit(5)
        .all()
    ) if classes else []

    assignment_list = []
    for a, sub in assignments:
        assignment_list.append({
            "id": a.id,
            "title": a.title,
            "due_date": a.due_date,
            "status": sub.status.value if sub else "ASSIGNED",
            "grade": sub.grade if sub else None
        })

    # Recent Activity
    activities = (
        db.query(LearningActivity)
        .filter(LearningActivity.student_id == student_id)
        .order_by(LearningActivity.timestamp.desc())
        .limit(6)
        .all()
    )

    # Next Best Action
    learning_path = LearningPathEngine.generate_path(student_id, db)
    next_action = {
        "title": "Continue Practice",
        "description": "Start an adaptive quiz session to reinforce your concepts.",
        "type": "PRACTICE"
    }
    if learning_path["path"]:
        first_step = learning_path["path"][0]
        next_action = {
            "title": first_step["title"],
            "description": first_step["recommendation_reason"],
            "type": first_step["type"],
            "topic_id": first_step.get("topic_id")
        }

    # Format topic mastery chart data
    topic_items = []
    for m, node in masteries:
        topic_items.append({
            "topic_id": node.id,
            "topic": node.title,
            "mastery": m.mastery_score,
            "status": m.status.value,
            "total_attempts": m.total_attempts,
            "correct_attempts": m.correct_attempts
        })

    return {
        "student": {
            "id": current_user.id,
            "name": current_user.full_name,
            "email": current_user.email,
            "grade": current_user.grade_level,
            "parent_token": current_user.parent_access_token
        },
        "metrics": {
            "overall_mastery": avg_mastery,
            "topics_mastered": mastered_count,
            "topics_needing_attention": attention_count,
            "critical_topics": critical_count,
            "total_topics_tracked": total_topics,
            "learning_streak_days": min(14, max(1, len(activities) // 2)),
            "risk_score": risk.composite_risk_score,
            "risk_level": risk.risk_level.value,
            "risk_reasons": risk.reasons
        },
        "next_best_action": next_action,
        "topic_mastery": topic_items,
        "enrolled_classes": [{"id": c.id, "name": c.name, "subject": c.subject} for c in classes],
        "assignments": assignment_list,
        "interventions": [
            {
                "id": item.id,
                "teacher_id": item.teacher_id,
                "teacher_name": (db.query(User.full_name).filter(User.id == item.teacher_id).scalar()) or "Teacher",
                "topic_id": item.topic_id,
                "topic_title": (db.query(CurriculumNode.title).filter(CurriculumNode.id == item.topic_id).scalar()) if item.topic_id else None,
                "type": item.type.value,
                "reason": item.reason,
                "action": item.action,
                "status": item.status.value,
                "created_at": item.created_at.isoformat() if item.created_at else None,
                "completed_at": item.completed_at.isoformat() if item.completed_at else None,
            }
            for item in db.query(Intervention).filter(Intervention.student_id == student_id).order_by(Intervention.created_at.desc()).all()
        ],
        "recent_activity": [
            {
                "id": act.id,
                "title": act.title,
                "type": act.activity_type,
                "score": act.score,
                "timestamp": act.timestamp
            }
            for act in activities
        ]
    }

@router.get("/me/mastery", response_model=StudentMasteryOverview)
def get_student_mastery(
    current_user: User = Depends(require_role([UserRole.STUDENT])),
    db: Session = Depends(get_db)
):
    masteries = (
        db.query(StudentTopicMastery, CurriculumNode)
        .join(CurriculumNode, CurriculumNode.id == StudentTopicMastery.topic_id)
        .filter(StudentTopicMastery.student_id == current_user.id)
        .all()
    )

    items = []
    total = len(masteries)
    mastered = 0
    attention = 0
    critical = 0

    for m, node in masteries:
        if m.status == MasteryStatus.STRONG:
            mastered += 1
        elif m.status == MasteryStatus.NEEDS_PRACTICE:
            attention += 1
        else:
            critical += 1

        acc = (m.correct_attempts / m.total_attempts * 100.0) if m.total_attempts > 0 else 0.0
        items.append(TopicMasteryItem(
            topic_id=node.id,
            topic_title=node.title,
            mastery_score=m.mastery_score,
            status=m.status,
            total_attempts=m.total_attempts,
            correct_attempts=m.correct_attempts,
            accuracy_percentage=round(acc, 1),
            last_attempt_at=m.last_attempt_at
        ))

    avg = round(sum(i.mastery_score for i in items) / total, 1) if total > 0 else 0.0

    return StudentMasteryOverview(
        overall_mastery=avg,
        topics_mastered=mastered,
        topics_needing_attention=attention,
        critical_topics=critical,
        topics=items
    )

@router.get("/me/learning-path", response_model=LearningPathResponse)
def get_student_learning_path(
    current_user: User = Depends(require_role([UserRole.STUDENT])),
    db: Session = Depends(get_db)
):
    return LearningPathEngine.generate_path(current_user.id, db)

@router.get("/parent/progress/{token}")
def get_parent_progress_view(token: str, db: Session = Depends(get_db)):
    student = db.query(User).filter(User.parent_access_token == token).first()
    if not student:
        raise HTTPException(status_code=404, detail="Parent access record not found")

    masteries = (
        db.query(StudentTopicMastery, CurriculumNode)
        .join(CurriculumNode, CurriculumNode.id == StudentTopicMastery.topic_id)
        .filter(StudentTopicMastery.student_id == student.id)
        .all()
    )

    risk = db.query(RiskPrediction).filter(RiskPrediction.student_id == student.id).first()
    interventions = db.query(Intervention).filter(Intervention.student_id == student.id).all()
    avg_mastery = sum(m.mastery_score for m, _ in masteries) / len(masteries) if masteries else 0.0

    strengths = [node.title for m, node in masteries if m.status == MasteryStatus.STRONG]
    needs_support = [node.title for m, node in masteries if m.status == MasteryStatus.CRITICAL]

    return {
        "student_name": student.full_name,
        "grade": student.grade_level or "Grade 11",
        "overall_progress_score": round(avg_mastery, 1),
        "risk_level": risk.risk_level.value if risk else "LOW",
        "risk_summary": risk.reasons if risk else ["Demonstrating steady academic engagement."],
        "strengths": strengths if strengths else ["Consistent participation"],
        "areas_needing_support": needs_support if needs_support else ["None currently critical"],
        "active_interventions": [
            {
                "action": i.action,
                "reason": i.reason,
                "status": i.status.value,
                "created_at": i.created_at
            }
            for i in interventions
        ]
    }
