from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base
import secrets

class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    grade = Column(String(50), nullable=False)
    subject = Column(String(100), nullable=False)
    board = Column(String(100), nullable=False, default="CBSE")
    academic_year = Column(String(50), nullable=False, default="2026-2027")
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    class_code = Column(String(20), unique=True, index=True, nullable=False)
    invite_token = Column(String(64), unique=True, index=True, nullable=False, default=lambda: secrets.token_urlsafe(16))
    invite_active = Column(Boolean, default=True)
    invite_expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class ClassMember(Base):
    __tablename__ = "class_members"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("class_id", "student_id", name="uq_class_student"),
    )
