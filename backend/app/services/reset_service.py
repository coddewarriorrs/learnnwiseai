from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.models.assessment import AnswerRecord, AssessmentAttempt
from app.models.mastery import StudentTopicMastery, LearningActivity
from app.models.risk import RiskPrediction
from app.models.intervention import Intervention, TeacherStudentNote
from app.models.assignment import AssignmentSubmission
from app.models.ai_chat import AIConversation, AIMessage
from app.models.learning_twin import StudentLearningTwin

class LearningProfileResetService:
    @staticmethod
    def reset_all_student_profiles(db: Session) -> dict:
        """
        Cleanses all student learning data, attempts, scores, and mock activities
        while preserving all user accounts, classes, curriculum nodes, and questions.
        """
        students = db.query(User).filter(User.role == UserRole.STUDENT).all()
        student_ids = [s.id for s in students]

        if not student_ids:
            return {"status": "ok", "message": "No students found to reset"}

        # 1. Delete answer records & attempts
        db.query(AnswerRecord).filter(AnswerRecord.student_id.in_(student_ids)).delete(synchronize_session=False)
        db.query(AssessmentAttempt).filter(AssessmentAttempt.student_id.in_(student_ids)).delete(synchronize_session=False)

        # 2. Delete topic masteries & learning activities
        db.query(StudentTopicMastery).filter(StudentTopicMastery.student_id.in_(student_ids)).delete(synchronize_session=False)
        db.query(LearningActivity).filter(LearningActivity.student_id.in_(student_ids)).delete(synchronize_session=False)

        # 3. Delete risk predictions
        db.query(RiskPrediction).filter(RiskPrediction.student_id.in_(student_ids)).delete(synchronize_session=False)

        # 4. Delete interventions & notes
        db.query(Intervention).filter(Intervention.student_id.in_(student_ids)).delete(synchronize_session=False)
        db.query(TeacherStudentNote).filter(TeacherStudentNote.student_id.in_(student_ids)).delete(synchronize_session=False)

        # 5. Reset assignment submissions
        db.query(AssignmentSubmission).filter(AssignmentSubmission.student_id.in_(student_ids)).delete(synchronize_session=False)

        # 6. Reset AI conversations
        convs = db.query(AIConversation).filter(AIConversation.student_id.in_(student_ids)).all()
        conv_ids = [c.id for c in convs]
        if conv_ids:
            db.query(AIMessage).filter(AIMessage.conversation_id.in_(conv_ids)).delete(synchronize_session=False)
            db.query(AIConversation).filter(AIConversation.id.in_(conv_ids)).delete(synchronize_session=False)

        # 7. Initialize fresh StudentLearningTwin for every student
        db.query(StudentLearningTwin).filter(StudentLearningTwin.student_id.in_(student_ids)).delete(synchronize_session=False)
        for sid in student_ids:
            twin = StudentLearningTwin(
                student_id=sid,
                misconception_fingerprint=[],
                recovery_mode_active=False,
                recovery_mode_step=0,
                struggle_signal_detected=False,
                timeline_events=[],
                decayed_topics=[],
                consecutive_topic_successes=0,
                consecutive_topic_failures=0
            )
            db.add(twin)

        db.commit()
        return {
            "status": "success",
            "students_reset_count": len(student_ids),
            "message": "Student learning profiles successfully reset to fresh, authentic state."
        }

    @staticmethod
    def reset_single_student(student_id: int, db: Session) -> dict:
        db.query(AnswerRecord).filter(AnswerRecord.student_id == student_id).delete(synchronize_session=False)
        db.query(AssessmentAttempt).filter(AssessmentAttempt.student_id == student_id).delete(synchronize_session=False)
        db.query(StudentTopicMastery).filter(StudentTopicMastery.student_id == student_id).delete(synchronize_session=False)
        db.query(LearningActivity).filter(LearningActivity.student_id == student_id).delete(synchronize_session=False)
        db.query(RiskPrediction).filter(RiskPrediction.student_id == student_id).delete(synchronize_session=False)
        db.query(Intervention).filter(Intervention.student_id == student_id).delete(synchronize_session=False)
        db.query(TeacherStudentNote).filter(TeacherStudentNote.student_id == student_id).delete(synchronize_session=False)
        db.query(AssignmentSubmission).filter(AssignmentSubmission.student_id == student_id).delete(synchronize_session=False)
        
        convs = db.query(AIConversation).filter(AIConversation.student_id == student_id).all()
        conv_ids = [c.id for c in convs]
        if conv_ids:
            db.query(AIMessage).filter(AIMessage.conversation_id.in_(conv_ids)).delete(synchronize_session=False)
            db.query(AIConversation).filter(AIConversation.id.in_(conv_ids)).delete(synchronize_session=False)

        twin = db.query(StudentLearningTwin).filter(StudentLearningTwin.student_id == student_id).first()
        if twin:
            twin.misconception_fingerprint = []
            twin.recovery_mode_active = False
            twin.recovery_mode_step = 0
            twin.recovery_mode_topic_id = None
            twin.struggle_signal_detected = False
            twin.struggle_signal_reason = None
            twin.timeline_events = []
            twin.decayed_topics = []
            twin.consecutive_topic_successes = 0
            twin.consecutive_topic_failures = 0
            twin.last_active_topic_id = None
        else:
            db.add(StudentLearningTwin(
                student_id=student_id,
                misconception_fingerprint=[],
                recovery_mode_active=False,
                recovery_mode_step=0,
                struggle_signal_detected=False,
                timeline_events=[],
                decayed_topics=[],
                consecutive_topic_successes=0,
                consecutive_topic_failures=0
            ))
        db.commit()
        return {"status": "success", "message": f"Student {student_id} learning profile reset successfully."}
