from sqlalchemy.orm import Session
from app.models.risk import RiskPrediction, RiskLevel
from app.models.mastery import StudentTopicMastery, MasteryStatus, LearningActivity
from app.models.assessment import AssessmentAttempt
from app.models.assignment import AssignmentSubmission, SubmissionStatus
from app.models.class_model import ClassMember, Class
from datetime import datetime, timezone
from typing import List

class RiskEngine:
    @staticmethod
    def calculate_student_risk(student_id: int, db: Session) -> RiskPrediction:
        # 1. Performance calculation: Average across assessment attempts and topic masteries
        attempts = db.query(AssessmentAttempt).filter(AssessmentAttempt.student_id == student_id).all()
        if attempts:
            perf_pct = sum(a.percentage for a in attempts) / len(attempts)
        else:
            masteries = db.query(StudentTopicMastery).filter(StudentTopicMastery.student_id == student_id).all()
            if masteries:
                perf_pct = sum(m.mastery_score for m in masteries) / len(masteries)
            else:
                perf_pct = 75.0

        performance_risk = max(0.0, min(100.0, 100.0 - perf_pct))

        # 2. Attendance calculation
        activity_count = db.query(LearningActivity).filter(LearningActivity.student_id == student_id).count()
        attendance_pct = min(100.0, max(40.0, activity_count * 10.0 + 45.0))
        attendance_risk = max(0.0, min(100.0, 100.0 - attendance_pct))

        # 3. Assignment completion
        submissions = db.query(AssignmentSubmission).filter(AssignmentSubmission.student_id == student_id).all()
        if submissions:
            completed = sum(1 for s in submissions if s.status == SubmissionStatus.COMPLETED)
            assignment_pct = (completed / len(submissions)) * 100.0
        else:
            assignment_pct = 80.0
        assignment_risk = max(0.0, min(100.0, 100.0 - assignment_pct))

        # 4. Engagement calculation
        recent_activities = db.query(LearningActivity).filter(
            LearningActivity.student_id == student_id
        ).order_by(LearningActivity.timestamp.desc()).limit(10).all()
        
        engagement_pct = min(100.0, len(recent_activities) * 10.0 + 35.0)
        engagement_risk = max(0.0, min(100.0, 100.0 - engagement_pct))

        # Formula: 0.35 * Performance + 0.25 * Attendance + 0.20 * Assignment + 0.20 * Engagement
        composite_score = (
            0.35 * performance_risk +
            0.25 * attendance_risk +
            0.20 * assignment_risk +
            0.20 * engagement_risk
        )
        composite_score = round(max(0.0, min(100.0, composite_score)), 1)

        # Classification: 0–39 LOW, 40–69 MEDIUM, 70–100 HIGH
        if composite_score < 40.0:
            level = RiskLevel.LOW
        elif composite_score <= 69.0:
            level = RiskLevel.MEDIUM
        else:
            level = RiskLevel.HIGH

        reasons: List[str] = []
        if performance_risk > 35.0:
            critical_topics = db.query(StudentTopicMastery).filter(
                StudentTopicMastery.student_id == student_id,
                StudentTopicMastery.status == MasteryStatus.CRITICAL
            ).all()
            if critical_topics:
                reasons.append(f"{len(critical_topics)} foundational topic(s) currently at CRITICAL mastery (<40%).")
            else:
                reasons.append("Recent assessment accuracy is trending below target thresholds.")

        if assignment_risk > 35.0:
            reasons.append("Assignment completion rate is irregular or pending submissions.")

        if engagement_risk > 45.0:
            reasons.append("Low practice session frequency over the past 14 days.")

        if attendance_risk > 35.0:
            reasons.append("Learning platform activity shows gaps between scheduled class sessions.")

        if not reasons:
            reasons.append("Consistent pace and steady performance across current syllabus topics.")

        if level == RiskLevel.HIGH:
            recommended_action = "Assign targeted prerequisite review and schedule a one-to-one diagnostic check-in."
        elif level == RiskLevel.MEDIUM:
            recommended_action = "Provide guided adaptive practice questions on weakest topics."
        else:
            recommended_action = "Maintain regular practice cadence and challenge with advanced problems."

        prediction = db.query(RiskPrediction).filter(RiskPrediction.student_id == student_id).first()
        if not prediction:
            prediction = RiskPrediction(student_id=student_id)
            db.add(prediction)

        prediction.performance_risk = round(performance_risk, 1)
        prediction.attendance_risk = round(attendance_risk, 1)
        prediction.assignment_risk = round(assignment_risk, 1)
        prediction.engagement_risk = round(engagement_risk, 1)
        prediction.composite_risk_score = composite_score
        prediction.risk_level = level
        prediction.reasons = reasons
        prediction.recommended_action = recommended_action
        prediction.calculated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(prediction)
        return prediction

    @staticmethod
    def get_teacher_student_ids(teacher_id: int, db: Session) -> List[int]:
        members = (
            db.query(ClassMember.student_id)
            .join(Class, Class.id == ClassMember.class_id)
            .filter(Class.teacher_id == teacher_id)
            .distinct()
            .all()
        )
        return [m[0] for m in members]
