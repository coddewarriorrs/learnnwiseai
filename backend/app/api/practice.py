from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.models.question import Question, DifficultyLevel
from app.models.syllabus import CurriculumNode, NodeType
from app.schemas.practice import StartPracticeRequest, QuestionResponse, SubmitAnswerRequest, SubmitAnswerResponse
from app.services.mastery_engine import MasteryEngine
from app.services.risk_engine import RiskEngine
from app.realtime.manager import ws_manager
from app.core.permissions import get_current_user, require_role
from app.services.smart_practice_engine import SmartPracticeEngine
import random

router = APIRouter(prefix="/practice", tags=["practice"])

from app.models.class_model import Class
from app.models.assessment import AnswerRecord
from app.models.risk import RiskPrediction, RiskLevel

@router.post("/start", response_model=list[QuestionResponse])
def start_practice(
    req: StartPracticeRequest,
    current_user: User = Depends(require_role([UserRole.STUDENT])),
    db: Session = Depends(get_db)
):
    all_nodes = {n.id: n for n in db.query(CurriculumNode).all()}

    # 1. Resolve target topic IDs based on hierarchical scope
    target_topic_ids = set()

    if req.topic_id:
        target_topic_ids.add(req.topic_id)
    elif req.chapter_id:
        for n in all_nodes.values():
            if n.type == NodeType.TOPIC and n.parent_id == req.chapter_id:
                target_topic_ids.add(n.id)
    elif req.class_id:
        cls = db.query(Class).filter(Class.id == req.class_id).first()
        if cls:
            # Find subject node matching class subject name or class code
            subj_node_ids = set()
            for n in all_nodes.values():
                if n.type == NodeType.SUBJECT:
                    if cls.subject and cls.subject.lower() in n.title.lower():
                        subj_node_ids.add(n.id)
                    elif cls.class_code and cls.class_code.upper() in n.code.upper():
                        subj_node_ids.add(n.id)
            
            # Find all chapters under these subjects
            chap_node_ids = {n.id for n in all_nodes.values() if n.type == NodeType.CHAPTER and n.parent_id in subj_node_ids}
            # Find all topics under these chapters
            for n in all_nodes.values():
                if n.type == NodeType.TOPIC and n.parent_id in chap_node_ids:
                    target_topic_ids.add(n.id)
    elif req.subject or req.subject_id:
        subj_node_ids = set()
        if req.subject_id:
            subj_node_ids.add(req.subject_id)
        if req.subject:
            for n in all_nodes.values():
                if n.type == NodeType.SUBJECT and req.subject.lower() in n.title.lower():
                    subj_node_ids.add(n.id)
        
        chap_node_ids = {n.id for n in all_nodes.values() if n.type == NodeType.CHAPTER and n.parent_id in subj_node_ids}
        for n in all_nodes.values():
            if n.type == NodeType.TOPIC and n.parent_id in chap_node_ids:
                target_topic_ids.add(n.id)

    # 2. Query candidate questions strictly within target scope
    query = db.query(Question)
    if target_topic_ids:
        query = query.filter(Question.topic_id.in_(list(target_topic_ids)))
    if req.difficulty:
        query = query.filter(Question.difficulty == req.difficulty)
    if req.exclude_ids:
        query = query.filter(~Question.id.in_(req.exclude_ids))

    candidates = query.all()

    # Step A: If difficulty was too strict, relax difficulty within target topics
    if not candidates and req.difficulty and target_topic_ids:
        candidates = db.query(Question).filter(
            Question.topic_id.in_(list(target_topic_ids)),
            ~Question.id.in_(req.exclude_ids or [])
        ).all()

    # Step B: If student completed all questions in target topics, reuse questions from target topics (spaced repetition)
    # NEVER jump to another chapter or subject!
    if not candidates and target_topic_ids:
        candidates = db.query(Question).filter(Question.topic_id.in_(list(target_topic_ids))).all()

    # Step C: Only if NO target topics were specified at all, allow fallback to general pool
    if not candidates and not target_topic_ids:
        candidates = db.query(Question).all()

    if not candidates:
        raise HTTPException(status_code=404, detail="No questions found for the selected topic.")

    # If student didn't specify difficulty, adjust based on student risk
    if not req.difficulty:
        risk_record = db.query(RiskPrediction).filter(RiskPrediction.student_id == current_user.id).first()
        if risk_record and risk_record.risk_level == RiskLevel.HIGH:
            # Prioritize EASY questions for high risk students
            candidates.sort(key=lambda q: (0 if q.difficulty == DifficultyLevel.EASY else (1 if q.difficulty == DifficultyLevel.MEDIUM else 2)))
        elif risk_record and risk_record.risk_level == RiskLevel.LOW:
            # Prioritize HARD questions for low risk students
            candidates.sort(key=lambda q: (0 if q.difficulty == DifficultyLevel.HARD else (1 if q.difficulty == DifficultyLevel.MEDIUM else 2)))

    # 3. Anti-repetition & spaced learning prioritization
    student_records = (
        db.query(AnswerRecord)
        .filter(AnswerRecord.student_id == current_user.id)
        .order_by(AnswerRecord.created_at.desc())
        .all()
    )
    # Map each question to student's latest record
    latest_record_map = {}
    for r in student_records:
        if r.question_id not in latest_record_map:
            latest_record_map[r.question_id] = r

    # Pool 1: Unattempted by student (guaranteed fresh questions)
    unattempted = [q for q in candidates if q.id not in latest_record_map]
    # Pool 2: Previously answered incorrectly (remedial reinforcement)
    incorrect = [q for q in candidates if q.id in latest_record_map and not latest_record_map[q.id].is_correct]
    # Pool 3: Previously answered correctly (spaced repetition, oldest first)
    correct = [q for q in candidates if q.id in latest_record_map and latest_record_map[q.id].is_correct]
    random.shuffle(unattempted)
    random.shuffle(incorrect)
    random.shuffle(correct)

    selected = []
    seen_ids = set()

    # Pass 1: Pick unattempted first (fresh questions)
    for q in unattempted:
        if q.id not in seen_ids and len(selected) < req.num_questions:
            selected.append(q)
            seen_ids.add(q.id)

    # Pass 2: Pick previously incorrect (remedial reinforcement)
    if len(selected) < req.num_questions:
        for q in incorrect:
            if q.id not in seen_ids and len(selected) < req.num_questions:
                selected.append(q)
                seen_ids.add(q.id)

    # Pass 3: Pick from previous correct (spaced repetition)
    if len(selected) < req.num_questions:
        for q in correct:
            if q.id not in seen_ids and len(selected) < req.num_questions:
                selected.append(q)
                seen_ids.add(q.id)

    # Pass 4: If still under requested count, draw uniquely from any remaining candidates
    if len(selected) < req.num_questions:
        remaining = [q for q in candidates if q.id not in seen_ids]
        random.shuffle(remaining)
        for q in remaining:
            if len(selected) < req.num_questions:
                selected.append(q)
                seen_ids.add(q.id)

    # Shuffle selected set so each practice round feels dynamic and diverse
    random.shuffle(selected)

    # 4. Assemble response with complete syllabus breadcrumbs
    results = []
    for q in selected:
        topic = all_nodes.get(q.topic_id)
        chapter = all_nodes.get(topic.parent_id) if topic else None
        subject = all_nodes.get(chapter.parent_id) if chapter else None

        results.append(QuestionResponse(
            id=q.id,
            topic_id=q.topic_id,
            topic_name=topic.title if topic else "General",
            chapter_name=chapter.title if chapter else None,
            subject_name=subject.title if subject else "General",
            title=q.title,
            prompt=q.prompt,
            options=q.options,
            difficulty=q.difficulty,
            points=q.points
        ))
    return results

@router.post("/submit-answer", response_model=SubmitAnswerResponse)
async def submit_practice_answer(
    req: SubmitAnswerRequest,
    current_user: User = Depends(require_role([UserRole.STUDENT])),
    db: Session = Depends(get_db)
):
    student_id = current_user.id
    result = SmartPracticeEngine.process_answer_submission(
        student_id=student_id,
        question_id=req.question_id,
        selected_answer=req.selected_answer,
        time_taken_seconds=req.time_taken_seconds,
        db=db
    )

    # Broadcast event to teacher real-time feed
    question = db.query(Question).filter(Question.id == req.question_id).first()
    await ws_manager.broadcast_event(
        event_type="PRACTICE_COMPLETED",
        data={
            "student_id": student_id,
            "student_name": current_user.full_name,
            "question_title": question.title if question else "Practice Question",
            "is_correct": result["is_correct"],
            "new_mastery": result["updated_mastery_score"],
            "stay_on_topic": result["stay_on_topic"],
            "mistake_type": result.get("mistake_type")
        }
    )

    return SubmitAnswerResponse(
        question_id=req.question_id,
        is_correct=result["is_correct"],
        correct_answer=result["correct_answer"],
        explanation=result["explanation"],
        explanation_brief=result["explanation_brief"],
        explanation_full=result["explanation_full"],
        mistake_type=result["mistake_type"],
        concept_involved=result["concept_involved"],
        how_to_avoid=result["how_to_avoid"],
        prerequisite_hint=result["prerequisite_hint"],
        updated_mastery_score=result["updated_mastery_score"],
        updated_mastery_status=result["updated_mastery_status"],
        root_cause_warning=result["root_cause_warning"],
        recommended_remedy=result["recommended_remedy"],
        stay_on_topic=result["stay_on_topic"],
        stay_on_topic_reason=result["stay_on_topic_reason"],
        consecutive_successes=result["consecutive_successes"],
        next_recommended_topic_id=result["next_recommended_topic_id"],
        recovery_mode_triggered=result["recovery_mode_triggered"],
        misconception_alert=result["misconception_alert"]
    )

