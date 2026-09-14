from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum as SQLEnum, JSON, Text
from sqlalchemy.sql import func
from app.database import Base
import enum

class RiskLevel(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class RiskPrediction(Base):
    __tablename__ = "risk_predictions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    performance_risk = Column(Float, default=0.0)
    attendance_risk = Column(Float, default=0.0)
    assignment_risk = Column(Float, default=0.0)
    engagement_risk = Column(Float, default=0.0)
    composite_risk_score = Column(Float, default=0.0)
    risk_level = Column(SQLEnum(RiskLevel), default=RiskLevel.LOW, nullable=False, index=True)
    reasons = Column(JSON, default=list)
    recommended_action = Column(Text, nullable=True)
    calculated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
