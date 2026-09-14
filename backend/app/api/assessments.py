from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.models.assessment import Assessment, AssessmentQuestion, AssessmentAttempt, AnswerRecord, AttemptStatus
from app.models.question import Question
from app.models.class_model import Class, ClassMember
from app.schemas.assessment import (
    AssessmentCreate, AssessmentResponse, AssessmentDetailResponse,
    AssessmentSubmitRequest, AssessmentResultResponse
)
from app.schemas.practice import QuestionResponse
from app.services.mastery_engine import MasteryEngine
from app.services.risk_engine import RiskEngine
from app.realtime.manager import ws_manager
from app.core.permissions import get_current_user, require_role, verify_teacher_class_access
from datetime import datetime, timezone

router = APIRouter(prefix="/assessments", tags=["assessments"])

@router.get("", response_model=list[AssessmentResponse])
def list_assessments(
    class_id: int = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Assessment)
    if class_id:
        query = query.filter(Assessment.class_id == class_id)
    assessments = query.all()

    results = []
    for a in assessments:
        q_count = db.query(AssessmentQuestion).filter(AssessmentQuestion.assessment_id == a.id).count()
        ar = AssessmentResponse.model_validate(a)
        ar.question_count = q_count
        results.append(ar)
    return results

@router.post("", response_model=AssessmentResponse)
def create_assessment(
    req: AssessmentCreate,
    current_user: User = Depends(require_role([UserRole.TEACHER, UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    verify_teacher_class_access(req.class_id, current_user, db)

    assessment = Assessment(
        class_id=req.class_id,
        title=req.title,
        description=req.description,
        duration_minutes=req.duration_minutes,
        due_date=req.due_date,
        total_points=len(req.question_ids) * 10
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    for idx, qid in enumerate(req.question_ids):
        aq = AssessmentQuestion(
            assessment_id=assessment.id,
            question_id=qid,
            order_index=idx,
            points=10
        )
        db.add(aq)
    db.commit()

    ar = AssessmentResponse.model_validate(assessment)
    ar.question_count = len(req.question_ids)
    return ar

@router.get("/{assessment_id}", response_model=AssessmentDetailResponse)
def get_assessment(
    assessment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    aq_list = (
        db.query(AssessmentQuestion, Question)
        .join(Question, Question.id == AssessmentQuestion.question_id)
        .filter(AssessmentQuestion.assessment_id == assessment_id)
        .order_by(AssessmentQuestion.order_index)
        .all()
    )

    questions = []
    for _, q in aq_list:
        questions.append(QuestionResponse(
            id=q.id,
            topic_id=q.topic_id,
            title=q.title,
            prompt=q.prompt,
            options=q.options,
            difficulty=q.difficulty,
            points=q.points
        ))

    resp = AssessmentDetailResponse.model_validate(assessment)
    resp.question_count = len(questions)
    resp.questions = questions
    return resp

@router.post("/{assessment_id}/submit", response_model=AssessmentResultResponse)
async def submit_assessment(
    assessment_id: int,
    req: AssessmentSubmitRequest,
    current_user: User = Depends(require_role([UserRole.STUDENT])),
    db: Session = Depends(get_db)
):
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    student_id = current_user.id
    total_earned = 0.0
    max_score = 0.0
    topics_touched = set()

    attempt = AssessmentAttempt(
        assessment_id=assessment_id,
        student_id=student_id,
        score=0.0,
        max_score=0.0,
        percentage=0.0,
        time_taken_seconds=req.time_taken_seconds,
        status=AttemptStatus.COMPLETED
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    for item in req.answers:
        qid = item.get("question_id")
        sel_ans = item.get("selected_answer", "")
        time_taken = item.get("time_taken_seconds", 10)
        
        q = db.query(Question).filter(Question.id == qid).first()
        if not q:
            continue

        is_correct = (sel_ans.strip().upper() == q.correct_answer.strip().upper())
        max_score += q.points
        if is_correct:
            total_earned += q.points
        
        topics_touched.add(q.topic_id)

        record = AnswerRecord(
            attempt_id=attempt.id,
            question_id=q.id,
            student_id=student_id,
            selected_answer=sel_ans,
            is_correct=is_correct,
            time_taken_seconds=time_taken
        )
        db.add(record)

    db.commit()

    percentage = round((total_earned / max_score * 100.0) if max_score > 0 else 0.0, 1)
    attempt.score = total_earned
    attempt.max_score = max_score
    attempt.percentage = percentage
    attempt.submitted_at = datetime.now(timezone.utc)
    db.commit()

    # Recalculate mastery for every topic tested in this assessment
    impact_list = []
    for tid in topics_touched:
        updated = MasteryEngine.calculate_topic_mastery(student_id, tid, db)
        impact_list.append({
            "topic_id": tid,
            "mastery_score": updated.mastery_score,
            "status": updated.status.value
        })

    # Recalculate risk
    risk = RiskEngine.calculate_student_risk(student_id, db)

    # Real-time WebSocket broadcast
    await ws_manager.broadcast_event(
        event_type="ASSESSMENT_COMPLETED",
        data={
            "student_id": student_id,
            "student_name": current_user.full_name,
            "assessment_title": assessment.title,
            "score": total_earned,
            "percentage": percentage,
            "risk_level": risk.risk_level.value
        }
    )

    feedback = (
        "Outstanding performance! Concept mastery verified." if percentage >= 80.0
        else "Satisfactory performance. Recommended to review flagged questions." if percentage >= 50.0
        else "Review required. Focus on foundational prerequisite concepts."
    )

    return AssessmentResultResponse(
        attempt_id=attempt.id,
        score=total_earned,
        max_score=max_score,
        percentage=percentage,
        status="COMPLETED",
        feedback=feedback,
        topic_mastery_impact=impact_list,
        risk_updated=True
    )
