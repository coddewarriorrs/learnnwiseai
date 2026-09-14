from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, JSON
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
    topic_id = Column(Integer, ForeignKey("curriculum_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    prompt = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)
    correct_answer = Column(String(50), nullable=False)
    explanation = Column(Text, nullable=False)
    prerequisite_hint = Column(Text, nullable=True)
    difficulty = Column(SQLEnum(DifficultyLevel), default=DifficultyLevel.MEDIUM, index=True)
    points = Column(Integer, default=10)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
