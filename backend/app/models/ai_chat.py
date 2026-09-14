from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.sql import func
from app.database import Base
import enum

class MessageSender(str, enum.Enum):
    STUDENT = "STUDENT"
    AI = "AI"

class AIConversation(Base):
    __tablename__ = "ai_conversations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("curriculum_nodes.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), default="Socratic Learning Session")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AIMessage(Base):
    __tablename__ = "ai_messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("ai_conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    sender = Column(SQLEnum(MessageSender), nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(Text, nullable=True)
    audio_url = Column(Text, nullable=True)
    image_analysis = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
