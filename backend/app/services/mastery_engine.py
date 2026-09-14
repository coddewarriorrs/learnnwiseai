from sqlalchemy.orm import Session
from app.models.mastery import StudentTopicMastery, MasteryStatus, LearningActivity
from app.models.question import Question, DifficultyLevel
from app.models.assessment import AnswerRecord
from app.services.prerequisite_graph import PrerequisiteGraphService
from datetime import datetime, timezone
from typing import Dict, Any

class MasteryEngine:
    DIFFICULTY_WEIGHTS = {
        DifficultyLevel.EASY: 1.0,
        DifficultyLevel.MEDIUM: 1.5,
        DifficultyLevel.HARD: 2.0
    }

    @staticmethod
    def calculate_topic_mastery(student_id: int, topic_id: int, db: Session) -> StudentTopicMastery:
        records = (
            db.query(AnswerRecord, Question)
            .join(Question, Question.id == AnswerRecord.question_id)
            .filter(AnswerRecord.student_id == student_id, Question.topic_id == topic_id)
            .order_by(AnswerRecord.created_at.desc())
            .all()
        )

        mastery_record = db.query(StudentTopicMastery).filter(
            StudentTopicMastery.student_id == student_id,
            StudentTopicMastery.topic_id == topic_id
        ).first()

        if not mastery_record:
            mastery_record = StudentTopicMastery(
                student_id=student_id,
                topic_id=topic_id,
                mastery_score=0.0,
                status=MasteryStatus.CRITICAL,
                total_attempts=0,
                correct_attempts=0
            )
            db.add(mastery_record)

        if not records:
            db.commit()
            db.refresh(mastery_record)
            return mastery_record

        # Recency decay calculation: exponential weighting for last 10 attempts
        total_weighted_points = 0.0
        earned_weighted_points = 0.0
        decay_factor = 1.0

        for record, question in records[:10]:
            weight = MasteryEngine.DIFFICULTY_WEIGHTS.get(question.difficulty, 1.0)
            adjusted_weight = weight * decay_factor
            total_weighted_points += adjusted_weight * 100.0
            if record.is_correct:
                earned_weighted_points += adjusted_weight * 100.0
            decay_factor *= 0.88  # Recency decay

        calculated_score = (earned_weighted_points / total_weighted_points) if total_weighted_points > 0 else 0.0
        calculated_score = max(0.0, min(100.0, round(calculated_score, 1)))

        # Categorize status according to specification:
        # <40% CRITICAL, 40-70% NEEDS PRACTICE, >70% STRONG
        if calculated_score < 40.0:
            status = MasteryStatus.CRITICAL
        elif calculated_score <= 70.0:
            status = MasteryStatus.NEEDS_PRACTICE
        else:
            status = MasteryStatus.STRONG

        mastery_record.mastery_score = calculated_score
        mastery_record.status = status
        mastery_record.total_attempts = len(records)
        mastery_record.correct_attempts = len([r for r, _ in records if r.is_correct])
        mastery_record.last_attempt_at = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(mastery_record)
        return mastery_record

    @staticmethod
    def record_practice_answer(student_id: int, question_id: int, selected_answer: str, time_taken_seconds: int, db: Session) -> Dict[str, Any]:
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise ValueError("Question not found")

        is_correct = (selected_answer.strip().upper() == question.correct_answer.strip().upper())
        
        # Store answer record
        record = AnswerRecord(
            student_id=student_id,
            question_id=question_id,
            selected_answer=selected_answer,
            is_correct=is_correct,
            time_taken_seconds=time_taken_seconds
        )
        db.add(record)

        # Log learning activity
        activity = LearningActivity(
            student_id=student_id,
            activity_type="PRACTICE",
            title=f"Practice: {question.title}",
            details={"topic_id": question.topic_id, "correct": is_correct, "points": question.points if is_correct else 0},
            score=100.0 if is_correct else 0.0,
            duration_seconds=time_taken_seconds
        )
        db.add(activity)
        db.commit()

        # Update mastery
        updated_mastery = MasteryEngine.calculate_topic_mastery(student_id, question.topic_id, db)

        # Diagnose prerequisite gap if answer was wrong
        root_cause_info = None
        if not is_correct:
            root_cause_info = PrerequisiteGraphService.diagnose_root_cause(student_id, question.topic_id, db)

        return {
            "is_correct": is_correct,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation,
            "prerequisite_hint": question.prerequisite_hint,
            "mastery_score": updated_mastery.mastery_score,
            "mastery_status": updated_mastery.status.value,
            "root_cause": root_cause_info
        }
