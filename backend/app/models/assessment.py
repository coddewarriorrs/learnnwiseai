from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.sql import func
from app.database import Base
import enum

class AttemptStatus(str, enum.Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    duration_minutes = Column(Integer, default=30)
    due_date = Column(DateTime(timezone=True), nullable=True)
    is_published = Column(Boolean, default=True)
    total_points = Column(Integer, default=100)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    order_index = Column(Integer, default=0)
    points = Column(Integer, default=10)

class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Float, default=0.0)
    max_score = Column(Float, default=100.0)
    percentage = Column(Float, default=0.0)
    time_taken_seconds = Column(Integer, default=0)
    status = Column(SQLEnum(AttemptStatus), default=AttemptStatus.COMPLETED)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

class AnswerRecord(Base):
    __tablename__ = "answer_records"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("assessment_attempts.id", ondelete="CASCADE"), nullable=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    selected_answer = Column(String(50), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    time_taken_seconds = Column(Integer, default=0)
    mistake_type = Column(String(100), nullable=True)
    explanation_brief = Column(Text, nullable=True)
    explanation_full = Column(Text, nullable=True)
    concept_involved = Column(String(255), nullable=True)
    how_to_avoid = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
