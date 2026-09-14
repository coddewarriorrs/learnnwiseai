from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum as SQLEnum, String, JSON, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base
import enum

class MasteryStatus(str, enum.Enum):
    CRITICAL = "CRITICAL"
    NEEDS_PRACTICE = "NEEDS_PRACTICE"
    STRONG = "STRONG"

class StudentTopicMastery(Base):
    __tablename__ = "student_topic_mastery"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("curriculum_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    mastery_score = Column(Float, default=0.0, nullable=False)
    status = Column(SQLEnum(MasteryStatus), default=MasteryStatus.NEEDS_PRACTICE, nullable=False)
    total_attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)
    last_attempt_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("student_id", "topic_id", name="uq_student_topic_mastery"),
    )

class LearningActivity(Base):
    __tablename__ = "learning_activity"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    activity_type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    details = Column(JSON, default=dict)
    score = Column(Float, nullable=True)
    duration_seconds = Column(Integer, default=0)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
