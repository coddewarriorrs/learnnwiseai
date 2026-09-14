from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.sql import func
from app.database import Base

class StudentLearningTwin(Base):
    __tablename__ = "student_learning_twins"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    
    # Misconception tracking
    misconception_fingerprint = Column(JSON, default=list)
    
    # Learning Recovery Mode
    recovery_mode_active = Column(Boolean, default=False)
    recovery_mode_step = Column(Integer, default=0) # 1: Identify, 2: Explain differently, 3: Simple Example, 4: Guided, 5: Easy, 6: Medium, 7: Reassess
    recovery_mode_topic_id = Column(Integer, ForeignKey("curriculum_nodes.id", ondelete="SET NULL"), nullable=True)
    
    # Possible Struggle / Disengagement Signal
    struggle_signal_detected = Column(Boolean, default=False)
    struggle_signal_reason = Column(String(255), nullable=True)
    
    # Performance Progression
    learning_velocity = Column(Float, default=1.0)
    timeline_events = Column(JSON, default=list) # Weekly / Milestone history
    decayed_topics = Column(JSON, default=list) # Topics with detected memory decay
    
    # Same-Topic Persistence Counters
    last_active_topic_id = Column(Integer, ForeignKey("curriculum_nodes.id", ondelete="SET NULL"), nullable=True)
    consecutive_topic_successes = Column(Integer, default=0)
    consecutive_topic_failures = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
