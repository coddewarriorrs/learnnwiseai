from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.sql import func
from app.database import Base
import enum

class NodeType(str, enum.Enum):
    BOARD = "BOARD"
    ACADEMIC_YEAR = "ACADEMIC_YEAR"
    CLASS = "CLASS"
    SUBJECT = "SUBJECT"
    CHAPTER = "CHAPTER"
    TOPIC = "TOPIC"
    SUBTOPIC = "SUBTOPIC"
    LEARNING_OUTCOME = "LEARNING_OUTCOME"

class NodeStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"

class CurriculumNode(Base):
    __tablename__ = "curriculum_nodes"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(SQLEnum(NodeType), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    code = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey("curriculum_nodes.id", ondelete="CASCADE"), nullable=True, index=True)
    prerequisites = Column(JSON, default=list)
    status = Column(SQLEnum(NodeStatus), default=NodeStatus.PUBLISHED)
    version = Column(String(50), default="1.0.0")
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
