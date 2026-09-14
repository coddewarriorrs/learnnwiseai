from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base

class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    country = Column(String(50), default="India")
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AcademicYear(Base):
    __tablename__ = "academic_years"

    id = Column(Integer, primary_key=True, index=True)
    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False, index=True)
    year_code = Column(String(20), index=True, nullable=False)
    title = Column(String(100), nullable=False)
    is_current = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AcademicClass(Base):
    __tablename__ = "academic_classes"

    id = Column(Integer, primary_key=True, index=True)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id", ondelete="CASCADE"), nullable=False, index=True)
    class_number = Column(Integer, nullable=False, index=True)
    title = Column(String(50), nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("academic_classes.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    is_integrated_science = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    unit_number = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    weightage_marks = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("units.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_number = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    domain = Column(String(50), nullable=True, index=True)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    code = Column(String(100), unique=True, index=True, nullable=False)
    prerequisites = Column(JSON, default=list)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SubTopic(Base):
    __tablename__ = "subtopics"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    code = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LearningOutcome(Base):
    __tablename__ = "learning_outcomes"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    code = Column(String(100), unique=True, index=True, nullable=False)
    statement = Column(Text, nullable=False)
    bloom_level = Column(String(50), default="APPLY")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
