import pytest
from app.models.user import User
from app.models.syllabus import CurriculumNode
from app.models.question import Question
from app.services.mastery_engine import MasteryEngine
from app.services.risk_engine import RiskEngine
from app.services.prerequisite_graph import PrerequisiteGraphService

def test_risk_formula_calculation(client, db):
    arjun = db.query(User).filter(User.email == "arjun@learnwise.ai").first()
    prediction = RiskEngine.calculate_student_risk(arjun.id, db)
    
    # Verify exact formula: 0.35P + 0.25A + 0.20M + 0.20E
    expected = (
        0.35 * prediction.performance_risk +
        0.25 * prediction.attendance_risk +
        0.20 * prediction.assignment_risk +
        0.20 * prediction.engagement_risk
    )
    expected = round(expected, 1)
    assert abs(prediction.composite_risk_score - expected) < 0.2
    assert prediction.risk_level.value in ["HIGH", "MEDIUM", "LOW"]
    assert len(prediction.reasons) > 0

def test_prerequisite_graph_root_cause_diagnosis(db):
    arjun = db.query(User).filter(User.email == "arjun@learnwise.ai").first()
    topic = db.query(CurriculumNode).filter(CurriculumNode.code == "TOP-CALC-03").first() # Integration by Parts
    
    diagnosis = PrerequisiteGraphService.diagnose_root_cause(arjun.id, topic.id, db)
    assert diagnosis is not None
    assert "root_cause_topic" in diagnosis
    assert "warning" in diagnosis
    assert "remedy" in diagnosis
