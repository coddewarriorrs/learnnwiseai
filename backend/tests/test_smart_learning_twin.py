import pytest
from app.models.user import User, UserRole
from app.models.question import Question, DifficultyLevel
from app.models.syllabus import CurriculumNode
from app.models.mastery import StudentTopicMastery
from app.models.assessment import AnswerRecord
from app.models.learning_twin import StudentLearningTwin
from app.services.smart_practice_engine import SmartPracticeEngine
from app.services.ai_tutor_service import AITutorService
from app.services.reset_service import LearningProfileResetService

def test_fresh_learning_profile_reset(db):
    """Test Requirement 1: Fresh Learning Profile reset wipes attempts and initializes clean slate."""
    student = db.query(User).filter(User.email == "arjun@learnwise.ai").first()
    assert student is not None

    # Reset arjun's profile
    LearningProfileResetService.reset_single_student(student.id, db)
    
    attempts = db.query(AnswerRecord).filter(AnswerRecord.student_id == student.id).count()
    assert attempts == 0
    
    twin = SmartPracticeEngine.get_or_create_twin(student.id, db)
    assert twin.recovery_mode_active is False
    assert twin.consecutive_topic_successes == 0
    assert len(twin.misconception_fingerprint or []) == 0

def test_mistake_classification_and_dual_explanations(db):
    """Test Requirements 4 & 5: Mistake detection into 8 types and dual brief/full explanations."""
    student = db.query(User).filter(User.email == "arjun@learnwise.ai").first()
    question = db.query(Question).first()
    assert question is not None

    # Find a wrong answer
    wrong_opt = "B" if question.correct_answer != "B" else "A"

    result = SmartPracticeEngine.process_answer_submission(
        student_id=student.id,
        question_id=question.id,
        selected_answer=wrong_opt,
        time_taken_seconds=2, # Fast -> CARELESS_MISTAKE
        db=db
    )

    assert result["is_correct"] is False
    assert result["mistake_type"] == "CARELESS_MISTAKE"
    assert result["explanation_brief"] is not None
    assert "Incorrect" in result["explanation_brief"]
    assert result["explanation_full"] is not None
    assert "Detailed Step-by-Step Solution" in result["explanation_full"]
    assert result["how_to_avoid"] is not None

    # Test correct answer dual explanation
    result_correct = SmartPracticeEngine.process_answer_submission(
        student_id=student.id,
        question_id=question.id,
        selected_answer=question.correct_answer,
        time_taken_seconds=20,
        db=db
    )
    assert result_correct["is_correct"] is True
    assert "Correct!" in result_correct["explanation_brief"]
    assert "Verification & Conceptual Walkthrough" in result_correct["explanation_full"]

def test_same_topic_practice_retention_and_advancement(db):
    """Test Requirement 2: Stay on same topic if weak (<70%), advance only when strong (>=70% & 2 streak)."""
    student = db.query(User).filter(User.email == "priya@learnwise.ai").first()
    question = db.query(Question).first()
    
    # First submission wrong -> score is low -> must stay on topic
    wrong_opt = "C" if question.correct_answer != "C" else "D"
    res1 = SmartPracticeEngine.process_answer_submission(
        student_id=student.id,
        question_id=question.id,
        selected_answer=wrong_opt,
        time_taken_seconds=15,
        db=db
    )
    assert res1["stay_on_topic"] is True
    assert "Reinforcing this topic" in res1["stay_on_topic_reason"]

    # First correct answer -> streak is 1 -> still stay on topic to verify stability
    res2 = SmartPracticeEngine.process_answer_submission(
        student_id=student.id,
        question_id=question.id,
        selected_answer=question.correct_answer,
        time_taken_seconds=25,
        db=db
    )
    assert res2["consecutive_successes"] == 1
    assert res2["stay_on_topic"] is True

    # Second correct answer -> streak is 2 -> if score >= 70, ready to advance
    res3 = SmartPracticeEngine.process_answer_submission(
        student_id=student.id,
        question_id=question.id,
        selected_answer=question.correct_answer,
        time_taken_seconds=18,
        db=db
    )
    assert res3["consecutive_successes"] >= 2
    if res3["updated_mastery_score"] >= 70.0:
        assert res3["stay_on_topic"] is False
        assert "Ready to advance" in res3["stay_on_topic_reason"]

def test_misconception_fingerprint_and_recovery_mode(db):
    """Test Requirements 11 & 13: Misconception pattern detection & Learning Recovery Mode."""
    student = db.query(User).filter(User.email == "rohit@learnwise.ai").first()
    question = db.query(Question).first()
    wrong_opt = "B" if question.correct_answer != "B" else "A"

    # Make 3 consecutive mistakes to trigger recovery mode
    for _ in range(3):
        res = SmartPracticeEngine.process_answer_submission(
            student_id=student.id,
            question_id=question.id,
            selected_answer=wrong_opt,
            time_taken_seconds=3,
            db=db
        )

    twin = SmartPracticeEngine.get_or_create_twin(student.id, db)
    assert twin.recovery_mode_active is True
    assert twin.recovery_mode_step >= 1
    assert twin.struggle_signal_detected is True
    assert len(twin.misconception_fingerprint) > 0

def test_handwritten_image_solution_analysis():
    """Test Requirement 6: Handwritten notebook calculation analysis."""
    dummy_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==" * 10
    
    analysis = AITutorService.analyze_handwritten_solution(
        image_base64=dummy_image,
        topic_title="Calculus - Integration by Parts",
        message="Please check my integration step"
    )

    assert analysis["is_readable"] is True
    assert len(analysis["steps"]) > 0
    assert analysis["first_incorrect_step"] == 3
    assert "Step 3" in analysis["where_error_occurred"]
    assert "mandated by the identity" in analysis["why_error_occurred"]
    assert "Replace the '+' with a '-'" in analysis["how_to_correct"]

def test_socratic_tutor_guardrails(db):
    """Test Requirement 22: Socratic tutor never simply gives answers when asked."""
    student = db.query(User).filter(User.email == "arjun@learnwise.ai").first()
    question = db.query(Question).first()

    reply = AITutorService._generate_socratic_reply(
        message="Give me the answer right now",
        topic="Integration by Parts",
        mastery=45.0,
        prereq_diagnosis=None,
        image_analysis=None,
        twin_context={"recent_mistake_types": ["SIGN_MISTAKE"]}
    )

    assert "not just give you this single answer" in reply
    assert "Identify the Core Principle" in reply
