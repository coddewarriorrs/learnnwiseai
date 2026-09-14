from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.risk import RiskLevel

class RiskResponse(BaseModel):
    student_id: int
    student_name: Optional[str] = None
    performance_risk: float
    attendance_risk: float
    assignment_risk: float
    engagement_risk: float
    composite_risk_score: float
    risk_level: RiskLevel
    reasons: List[str] = []
    recommended_action: Optional[str] = None
    calculated_at: Optional[datetime] = None

class EarlyWarningStudent(BaseModel):
    student_id: int
    student_name: str
    student_email: str
    class_name: str
    risk_score: float
    risk_level: RiskLevel
    top_weak_topic: Optional[str] = None
    reasons: List[str] = []
    recommended_action: str
    last_activity: Optional[datetime] = None
