from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, JSON, Boolean
from sqlalchemy.sql import func
from app.database import Base
import enum

class DifficultyLevel(str, enum.Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("curriculum_nodes.id", ondelete="CASCADE"), nullable=True, index=True)
    
    # CBSE 2026-27 Structured Hierarchy Links
    class_id = Column(Integer, ForeignKey("academic_classes.id", ondelete="SET NULL"), nullable=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True, index=True)
    unit_id = Column(Integer, ForeignKey("units.id", ondelete="SET NULL"), nullable=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id", ondelete="SET NULL"), nullable=True, index=True)
    hierarchy_topic_id = Column(Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True, index=True)
    subtopic_id = Column(Integer, ForeignKey("subtopics.id", ondelete="SET NULL"), nullable=True, index=True)
    learning_outcome_id = Column(Integer, ForeignKey("learning_outcomes.id", ondelete="SET NULL"), nullable=True, index=True)
    learning_outcome = Column(Text, nullable=True)
    is_ai_generated = Column(Boolean, default=False)

    title = Column(String(255), nullable=False)
    prompt = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)
    correct_answer = Column(String(50), nullable=False)
    explanation = Column(Text, nullable=False)
    prerequisite_hint = Column(Text, nullable=True)
    difficulty = Column(SQLEnum(DifficultyLevel), default=DifficultyLevel.MEDIUM, index=True)
    points = Column(Integer, default=10)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

