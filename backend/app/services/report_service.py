from sqlalchemy.orm import Session
from app.models.user import User
from app.models.class_model import Class, ClassMember
from app.models.mastery import StudentTopicMastery, LearningActivity
from app.models.risk import RiskPrediction
from app.models.intervention import Intervention
from app.models.assessment import AssessmentAttempt
from typing import Dict, Any
import io
import csv

class ReportService:
    @staticmethod
    def get_student_report_data(student_id: int, db: Session) -> Dict[str, Any]:
        student = db.query(User).filter(User.id == student_id).first()
        if not student:
            return {}

        masteries = (
            db.query(StudentTopicMastery)
            .filter(StudentTopicMastery.student_id == student_id)
            .all()
        )
        avg_mastery = sum(m.mastery_score for m in masteries) / len(masteries) if masteries else 0.0

        risk = db.query(RiskPrediction).filter(RiskPrediction.student_id == student_id).first()
        interventions = db.query(Intervention).filter(Intervention.student_id == student_id).all()
        attempts = db.query(AssessmentAttempt).filter(AssessmentAttempt.student_id == student_id).all()
        activities = db.query(LearningActivity).filter(LearningActivity.student_id == student_id).count()

        return {
            "student_name": student.full_name,
            "email": student.email,
            "grade_level": student.grade_level or "Grade 11",
            "overall_mastery": round(avg_mastery, 1),
            "topics_assessed": len(masteries),
            "risk_score": risk.composite_risk_score if risk else 20.0,
            "risk_level": risk.risk_level.value if risk else "LOW",
            "risk_reasons": risk.reasons if risk else [],
            "recommended_action": risk.recommended_action if risk else "Maintain regular practice pace.",
            "total_assessments": len(attempts),
            "average_assessment_score": round(sum(a.percentage for a in attempts) / len(attempts), 1) if attempts else 0.0,
            "total_activities": activities,
            "interventions_count": len(interventions)
        }

    @staticmethod
    def generate_student_csv(student_id: int, db: Session) -> str:
        data = ReportService.get_student_report_data(student_id, db)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Field", "Value"])
        for k, v in data.items():
            if isinstance(v, list):
                writer.writerow([k, "; ".join(str(item) for item in v)])
            else:
                writer.writerow([k, str(v)])
        return output.getvalue()

    @staticmethod
    def get_class_report_data(class_id: int, teacher_id: int, db: Session) -> Dict[str, Any]:
        cls = db.query(Class).filter(Class.id == class_id, Class.teacher_id == teacher_id).first()
        if not cls:
            return {}

        members = db.query(ClassMember).filter(ClassMember.class_id == class_id).all()
        student_ids = [m.student_id for m in members]

        if not student_ids:
            return {
                "class_name": cls.name,
                "grade": cls.grade,
                "subject": cls.subject,
                "student_count": 0,
                "average_mastery": 0.0,
                "risk_breakdown": {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
            }

        risks = db.query(RiskPrediction).filter(RiskPrediction.student_id.in_(student_ids)).all()
        high_risk = sum(1 for r in risks if r.risk_level.value == "HIGH")
        med_risk = sum(1 for r in risks if r.risk_level.value == "MEDIUM")
        low_risk = sum(1 for r in risks if r.risk_level.value == "LOW")

        masteries = db.query(StudentTopicMastery).filter(StudentTopicMastery.student_id.in_(student_ids)).all()
        avg_mastery = sum(m.mastery_score for m in masteries) / len(masteries) if masteries else 0.0

        return {
            "class_name": cls.name,
            "grade": cls.grade,
            "subject": cls.subject,
            "student_count": len(student_ids),
            "average_mastery": round(avg_mastery, 1),
            "risk_breakdown": {
                "HIGH": high_risk,
                "MEDIUM": med_risk,
                "LOW": low_risk
            }
        }

    @staticmethod
    def generate_class_csv(class_id: int, teacher_id: int, db: Session) -> str:
        cls = db.query(Class).filter(Class.id == class_id, Class.teacher_id == teacher_id).first()
        if not cls:
            return ""

        members = db.query(ClassMember).filter(ClassMember.class_id == class_id).all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Student ID", "Student Name", "Email", "Risk Score", "Risk Level", "Overall Mastery %"])

        for m in members:
            student = db.query(User).filter(User.id == m.student_id).first()
            if not student:
                continue
            risk = db.query(RiskPrediction).filter(RiskPrediction.student_id == student.id).first()
            masteries = db.query(StudentTopicMastery).filter(StudentTopicMastery.student_id == student.id).all()
            avg_m = round(sum(item.mastery_score for item in masteries) / len(masteries), 1) if masteries else 0.0
            
            writer.writerow([
                student.id,
                student.full_name,
                student.email,
                risk.composite_risk_score if risk else "N/A",
                risk.risk_level.value if risk else "LOW",
                avg_m
            ])
        return output.getvalue()
