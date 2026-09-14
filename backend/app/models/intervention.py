from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from app.database import Base
import enum

class InterventionType(str, enum.Enum):
    PREREQUISITE_REVIEW = "PREREQUISITE_REVIEW"
    EXTRA_PRACTICE = "EXTRA_PRACTICE"
    ONE_TO_ONE = "ONE_TO_ONE"
    TARGETED_QUIZ = "TARGETED_QUIZ"
    CONCEPT_EXPLANATION = "CONCEPT_EXPLANATION"
    REASSESSMENT = "REASSESSMENT"

class InterventionStatus(str, enum.Enum):
    RECOMMENDED = "RECOMMENDED"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class Intervention(Base):
    __tablename__ = "interventions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("curriculum_nodes.id", ondelete="SET NULL"), nullable=True)
    type = Column(SQLEnum(InterventionType), default=InterventionType.PREREQUISITE_REVIEW)
    reason = Column(Text, nullable=False)
    action = Column(Text, nullable=False)
    status = Column(SQLEnum(InterventionStatus), default=InterventionStatus.RECOMMENDED, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

class TeacherStudentNote(Base):
    __tablename__ = "teacher_student_notes"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    note = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
