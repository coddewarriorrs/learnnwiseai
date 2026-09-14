from sqlalchemy.orm import Session
from app.models.mastery import StudentTopicMastery
from app.models.syllabus import CurriculumNode, NodeType
from app.services.prerequisite_graph import PrerequisiteGraphService
from typing import Dict, Any

class LearningPathEngine:
    @staticmethod
    def generate_path(student_id: int, db: Session) -> Dict[str, Any]:
        weakest_mastery = (
            db.query(StudentTopicMastery, CurriculumNode)
            .join(CurriculumNode, CurriculumNode.id == StudentTopicMastery.topic_id)
            .filter(StudentTopicMastery.student_id == student_id)
            .order_by(StudentTopicMastery.mastery_score.asc())
            .first()
        )

        steps = []
        current_focus = "General Mathematics"
        current_score = 75.0
        recovery_mode = False

        if weakest_mastery:
            m_record, node = weakest_mastery
            current_focus = node.title
            current_score = m_record.mastery_score

            if current_score < 60.0:
                recovery_mode = True
                prereqs = PrerequisiteGraphService.get_prerequisites_for_topic(node.id, db)
                step_num = 1

                for p in prereqs:
                    steps.append({
                        "step_number": step_num,
                        "title": f"Review Foundation: {p.title}",
                        "concept": p.title,
                        "type": "PREREQUISITE_REVIEW",
                        "is_completed": False,
                        "topic_id": p.id,
                        "recommendation_reason": f"Required prerequisite for mastering {node.title}."
                    })
                    step_num += 1

                steps.append({
                    "step_number": step_num,
                    "title": f"Worked Examples: {node.title}",
                    "concept": node.title,
                    "type": "CONCEPT_EXPLANATION",
                    "is_completed": False,
                    "topic_id": node.id,
                    "recommendation_reason": "Deconstruct step-by-step problem solutions."
                })
                step_num += 1

                steps.append({
                    "step_number": step_num,
                    "title": f"Adaptive Practice: {node.title}",
                    "concept": node.title,
                    "type": "PRACTICE",
                    "is_completed": False,
                    "topic_id": node.id,
                    "recommendation_reason": "Reinforce problem solving starting with foundational difficulty."
                })
                step_num += 1

                steps.append({
                    "step_number": step_num,
                    "title": f"Reassessment Check: {node.title}",
                    "concept": node.title,
                    "type": "ASSESSMENT",
                    "is_completed": False,
                    "topic_id": node.id,
                    "recommendation_reason": "Verify learning gap closure."
                })
            else:
                steps = [
                    {
                        "step_number": 1,
                        "title": f"Concept Deep Dive: {node.title}",
                        "concept": node.title,
                        "type": "CONCEPT_EXPLANATION",
                        "is_completed": True,
                        "topic_id": node.id,
                        "recommendation_reason": "Foundation established."
                    },
                    {
                        "step_number": 2,
                        "title": f"Challenging Practice: {node.title}",
                        "concept": node.title,
                        "type": "PRACTICE",
                        "is_completed": False,
                        "topic_id": node.id,
                        "recommendation_reason": "Advance to high-difficulty problems."
                    },
                    {
                        "step_number": 3,
                        "title": "Topic Mastery Assessment",
                        "concept": node.title,
                        "type": "ASSESSMENT",
                        "is_completed": False,
                        "topic_id": node.id,
                        "recommendation_reason": "Confirm strong mastery status."
                    }
                ]
        else:
            first_topic = db.query(CurriculumNode).filter(CurriculumNode.type == NodeType.TOPIC).first()
            t_name = first_topic.title if first_topic else "Algebraic Foundations"
            t_id = first_topic.id if first_topic else 1
            steps = [
                {
                    "step_number": 1,
                    "title": f"Diagnostic Benchmark: {t_name}",
                    "concept": t_name,
                    "type": "PRACTICE",
                    "is_completed": False,
                    "topic_id": t_id,
                    "recommendation_reason": "Initial baseline evaluation."
                }
            ]

        return {
            "student_id": student_id,
            "subject": "Mathematics",
            "current_focus_topic": current_focus,
            "current_mastery": current_score,
            "recovery_mode_active": recovery_mode,
            "path": steps
        }
