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
    from app.models.syllabus_hierarchy import (
        Board, AcademicYear, AcademicClass, Subject, Unit, 
        Chapter, Topic, SubTopic, LearningOutcome
    )
    from sqlalchemy import or_

    all_nodes = {n.id: n for n in db.query(CurriculumNode).all()}

    # 1. Resolve target entity in CBSE 2026-27 hierarchy
    selected_class = None
    selected_subject = None
    selected_chapter = None
    selected_topic = None

    # Check Class
    class_id_candidate = req.academic_class_id or req.class_id or req.class_number
    if class_id_candidate is not None:
        selected_class = db.query(AcademicClass).filter(
            or_(
                AcademicClass.id == class_id_candidate,
                AcademicClass.class_number == class_id_candidate
            )
        ).first()

    # Check Subject
    if req.subject_id:
        selected_subject = db.query(Subject).filter(Subject.id == req.subject_id).first()
    elif req.subject:
        subj_q = db.query(Subject)
        if selected_class:
            subj_q = subj_q.filter(Subject.class_id == selected_class.id)
        selected_subject = subj_q.filter(Subject.name.ilike(f"%{req.subject.strip()}%")).first()

    # Check Chapter
    if req.chapter_id:
        selected_chapter = db.query(Chapter).filter(Chapter.id == req.chapter_id).first()
    elif req.chapter:
        chap_q = db.query(Chapter)
        if selected_subject:
            chap_q = chap_q.join(Unit, Unit.id == Chapter.unit_id).filter(Unit.subject_id == selected_subject.id)
        selected_chapter = chap_q.filter(Chapter.title.ilike(f"%{req.chapter.strip()}%")).first()

    # Check Topic
    topic_id_candidate = req.hierarchy_topic_id or req.topic_id
    if topic_id_candidate:
        selected_topic = db.query(Topic).filter(Topic.id == topic_id_candidate).first()

    # 2. Build Query strictly isolating the scope
    query = db.query(Question)
    is_hierarchy_scoped = False

    if selected_topic:
        query = query.filter(or_(Question.hierarchy_topic_id == selected_topic.id, Question.topic_id == selected_topic.id))
        is_hierarchy_scoped = True
    elif selected_chapter:
        query = query.filter(Question.chapter_id == selected_chapter.id)
        is_hierarchy_scoped = True
    elif selected_subject:
        query = query.filter(Question.subject_id == selected_subject.id)
        is_hierarchy_scoped = True
    elif selected_class:
        query = query.filter(Question.class_id == selected_class.id)
        is_hierarchy_scoped = True
    else:
        # Fallback to legacy CurriculumNode resolution
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
                subj_node_ids = set()
                for n in all_nodes.values():
                    if n.type == NodeType.SUBJECT:
                        if cls.subject and cls.subject.lower() in n.title.lower():
                            subj_node_ids.add(n.id)
                        elif cls.class_code and cls.class_code.upper() in n.code.upper():
                            subj_node_ids.add(n.id)
                chap_node_ids = {n.id for n in all_nodes.values() if n.type == NodeType.CHAPTER and n.parent_id in subj_node_ids}
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
        if target_topic_ids:
            query = query.filter(Question.topic_id.in_(list(target_topic_ids)))

    if req.difficulty:
        query = query.filter(Question.difficulty == req.difficulty)
    if req.exclude_ids:
        query = query.filter(~Question.id.in_(req.exclude_ids))

    candidates = query.all()

    # Step A: If strict difficulty had 0 candidates, relax difficulty within the SAME isolated scope
    if not candidates and req.difficulty:
        relax_query = db.query(Question)
        if selected_topic:
            relax_query = relax_query.filter(or_(Question.hierarchy_topic_id == selected_topic.id, Question.topic_id == selected_topic.id))
        elif selected_chapter:
            relax_query = relax_query.filter(Question.chapter_id == selected_chapter.id)
        elif selected_subject:
            relax_query = relax_query.filter(Question.subject_id == selected_subject.id)
        elif selected_class:
            relax_query = relax_query.filter(Question.class_id == selected_class.id)
        if req.exclude_ids:
            relax_query = relax_query.filter(~Question.id.in_(req.exclude_ids))
        candidates = relax_query.all()

    # Step B: If all existing questions in scope were completed / excluded, dynamically generate fresh questions!
    if not candidates and (selected_chapter or selected_topic or selected_subject or selected_class):
        try:
            from app.services.question_generator_service import QuestionGeneratorService
            candidates = QuestionGeneratorService.generate_questions_for_scope(
                db=db,
                class_id=selected_class.id if selected_class else None,
                subject_id=selected_subject.id if selected_subject else None,
                chapter_id=selected_chapter.id if selected_chapter else None,
                topic_id=selected_topic.id if selected_topic else None,
                difficulty=req.difficulty,
                count=req.num_questions
            )
        except Exception:
            candidates = []

    # Step C: Only if dynamic generation yielded nothing, fall back to spaced repetition reuse
    # NEVER jump to another class, subject, or chapter!
    if not candidates:
        reuse_query = db.query(Question)
        if selected_topic:
            reuse_query = reuse_query.filter(or_(Question.hierarchy_topic_id == selected_topic.id, Question.topic_id == selected_topic.id))
        elif selected_chapter:
            reuse_query = reuse_query.filter(Question.chapter_id == selected_chapter.id)
        elif selected_subject:
            reuse_query = reuse_query.filter(Question.subject_id == selected_subject.id)
        elif selected_class:
            reuse_query = reuse_query.filter(Question.class_id == selected_class.id)
        candidates = reuse_query.all()

    # Step C: Only if NO scope was provided at all, fallback to general pool
    if not candidates and not is_hierarchy_scoped:
        candidates = db.query(Question).limit(30).all()

    if not candidates:
        raise HTTPException(status_code=404, detail="No questions found for the selected syllabus scope.")

    # If student didn't specify difficulty, adjust based on student risk
    if not req.difficulty:
        risk_record = db.query(RiskPrediction).filter(RiskPrediction.student_id == current_user.id).first()
        if risk_record and risk_record.risk_level == RiskLevel.HIGH:
            candidates.sort(key=lambda q: (0 if q.difficulty == DifficultyLevel.EASY else (1 if q.difficulty == DifficultyLevel.MEDIUM else 2)))
        elif risk_record and risk_record.risk_level == RiskLevel.LOW:
            candidates.sort(key=lambda q: (0 if q.difficulty == DifficultyLevel.HARD else (1 if q.difficulty == DifficultyLevel.MEDIUM else 2)))

    # 3. Anti-repetition & spaced learning prioritization
    # 3. Anti-repetition & dynamic generation mechanism
    student_records = (
        db.query(AnswerRecord)
        .filter(AnswerRecord.student_id == current_user.id)
        .order_by(AnswerRecord.created_at.desc())
        .all()
    )
    latest_record_map = {}
    for r in student_records:
        if r.question_id not in latest_record_map:
            latest_record_map[r.question_id] = r

    exclude_set = set(req.exclude_ids or [])
    unattempted = [q for q in candidates if q.id not in latest_record_map and q.id not in exclude_set]

    # If unattempted questions in scope are fewer than needed, dynamically generate fresh questions!
    needed = req.num_questions - len(unattempted)
    if needed > 0 and (selected_chapter or selected_topic or selected_subject or selected_class):
        try:
            from app.services.question_generator_service import QuestionGeneratorService
            fresh_qs = QuestionGeneratorService.generate_questions_for_scope(
                db=db,
                class_id=selected_class.id if selected_class else None,
                subject_id=selected_subject.id if selected_subject else None,
                chapter_id=selected_chapter.id if selected_chapter else None,
                topic_id=selected_topic.id if selected_topic else None,
                difficulty=req.difficulty,
                count=max(needed, 5)
            )
            for fq in fresh_qs:
                if fq.id not in exclude_set and fq.id not in latest_record_map:
                    unattempted.append(fq)
        except Exception:
            pass  # Fallback to existing candidate pool if generation fails

    incorrect = [q for q in candidates if q.id in latest_record_map and not latest_record_map[q.id].is_correct and q.id not in exclude_set]
    correct = [q for q in candidates if q.id in latest_record_map and latest_record_map[q.id].is_correct and q.id not in exclude_set]

    random.shuffle(unattempted)
    random.shuffle(incorrect)
    random.shuffle(correct)

    selected = []
    seen_ids = set()

    for q in unattempted:
        if q.id not in seen_ids and len(selected) < req.num_questions:
            selected.append(q)
            seen_ids.add(q.id)

    if len(selected) < req.num_questions:
        for q in incorrect:
            if q.id not in seen_ids and len(selected) < req.num_questions:
                selected.append(q)
                seen_ids.add(q.id)

    if len(selected) < req.num_questions:
        for q in correct:
            if q.id not in seen_ids and len(selected) < req.num_questions:
                selected.append(q)
                seen_ids.add(q.id)

    if len(selected) < req.num_questions:
        remaining = [q for q in candidates if q.id not in seen_ids]
        random.shuffle(remaining)
        for q in remaining:
            if len(selected) < req.num_questions:
                selected.append(q)
                seen_ids.add(q.id)

    random.shuffle(selected)

    # 4. Assemble response with complete syllabus breadcrumbs
    results = []
    for q in selected:
        c_id = q.class_id
        c_name = None
        s_id = q.subject_id
        s_name = None
        u_id = q.unit_id
        u_name = None
        ch_id = q.chapter_id
        ch_name = None
        domain = None
        t_id = q.hierarchy_topic_id or q.topic_id
        t_name = None
        lo_stmt = q.learning_outcome

        if q.class_id:
            ac = db.query(AcademicClass).filter(AcademicClass.id == q.class_id).first()
            if ac:
                c_name = ac.title
        if q.subject_id:
            s = db.query(Subject).filter(Subject.id == q.subject_id).first()
            if s:
                s_name = s.name
        if q.unit_id:
            u = db.query(Unit).filter(Unit.id == q.unit_id).first()
            if u:
                u_name = u.title
        if q.chapter_id:
            ch = db.query(Chapter).filter(Chapter.id == q.chapter_id).first()
            if ch:
                ch_name = ch.title
                domain = ch.domain
        if q.hierarchy_topic_id:
            top = db.query(Topic).filter(Topic.id == q.hierarchy_topic_id).first()
            if top:
                t_name = top.title
        elif q.topic_id:
            legacy_node = all_nodes.get(q.topic_id)
            if legacy_node:
                t_name = legacy_node.title
                if not ch_name and legacy_node.parent_id:
                    ch_node = all_nodes.get(legacy_node.parent_id)
                    if ch_node:
                        ch_name = ch_node.title
                        if not s_name and ch_node.parent_id:
                            s_node = all_nodes.get(ch_node.parent_id)
                            if s_node:
                                s_name = s_node.title

        results.append(QuestionResponse(
            id=q.id,
            class_id=c_id,
            class_name=c_name or "CBSE",
            subject_id=s_id,
            subject_name=s_name or "General",
            unit_id=u_id,
            unit_name=u_name,
            chapter_id=ch_id,
            chapter_name=ch_name,
            domain=domain,
            topic_id=t_id,
            hierarchy_topic_id=q.hierarchy_topic_id,
            topic_name=t_name or "Topic Practice",
            learning_outcome=lo_stmt,
            learning_outcome_id=q.learning_outcome_id,
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

