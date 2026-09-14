from sqlalchemy.orm import Session
from app.models.syllabus import CurriculumNode
from app.models.mastery import StudentTopicMastery
from typing import Optional, Dict, List, Any

class PrerequisiteGraphService:
    @staticmethod
    def get_prerequisites_for_topic(topic_id: int, db: Session) -> List[CurriculumNode]:
        node = db.query(CurriculumNode).filter(CurriculumNode.id == topic_id).first()
        if not node or not node.prerequisites:
            return []
        
        prereqs = []
        for prereq_ref in node.prerequisites:
            if isinstance(prereq_ref, int) or (isinstance(prereq_ref, str) and str(prereq_ref).isdigit()):
                p_node = db.query(CurriculumNode).filter(CurriculumNode.id == int(prereq_ref)).first()
            else:
                p_node = db.query(CurriculumNode).filter(CurriculumNode.code == str(prereq_ref)).first()
            if p_node:
                prereqs.append(p_node)
        return prereqs

    @staticmethod
    def diagnose_root_cause(student_id: int, topic_id: int, db: Session) -> Optional[Dict[str, Any]]:
        current_topic = db.query(CurriculumNode).filter(CurriculumNode.id == topic_id).first()
        if not current_topic:
            return None

        prereqs = PrerequisiteGraphService.get_prerequisites_for_topic(topic_id, db)
        if not prereqs:
            return None

        weak_prereqs = []
        for p in prereqs:
            mastery = db.query(StudentTopicMastery).filter(
                StudentTopicMastery.student_id == student_id,
                StudentTopicMastery.topic_id == p.id
            ).first()

            score = mastery.mastery_score if mastery else 35.0
            if score < 65.0:
                weak_prereqs.append({
                    "topic_id": p.id,
                    "title": p.title,
                    "score": round(score, 1),
                    "code": p.code
                })

        if weak_prereqs:
            weak_prereqs.sort(key=lambda x: x["score"])
            primary = weak_prereqs[0]
            warning = f"Struggle in '{current_topic.title}' is strongly rooted in incomplete mastery of prerequisite '{primary['title']}' ({primary['score']}%)."
            remedy = f"Review prerequisite '{primary['title']}' first before re-attempting {current_topic.title}."
            return {
                "root_cause_topic": primary,
                "warning": warning,
                "remedy": remedy,
                "all_weak_prerequisites": weak_prereqs
            }
        return None
