from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class MisconceptionItem(BaseModel):
    mistake_type: str
    count: int
    frequency_pct: float
    topics: List[str]
    last_detected: Optional[str] = None
    remedy_advice: str

class PrerequisiteGapItem(BaseModel):
    topic_id: int
    topic_name: str
    subject: str
    root_prerequisite_id: int
    root_prerequisite_name: str
    gap_severity: str # 'CRITICAL', 'MODERATE', 'MINOR'
    suggested_action: str

class RecoveryModeStatus(BaseModel):
    active: bool
    step: int
    step_name: str
    topic_id: Optional[int] = None
    topic_name: Optional[str] = None
    subject: Optional[str] = None
    guidance: str

class StruggleSignalStatus(BaseModel):
    detected: bool
    reason: Optional[str] = None
    intervention_recommended: Optional[str] = None

class DecayedTopicItem(BaseModel):
    topic_id: int
    topic_name: str
    subject: str
    highest_mastery: float
    current_estimated_mastery: float
    days_since_last_practice: int
    memory_decay_pct: float
    needs_review: bool

class TimelineMilestone(BaseModel):
    week_or_date: str
    summary: str
    status: str # 'STRUGGLING', 'IMPROVING', 'STRONG', 'MASTERED'
    mastery_avg: float
    questions_attempted: int
    mistakes_made: int
    key_achievement: Optional[str] = None

class NextBestAction(BaseModel):
    action_type: str # 'PRACTICE_SAME_TOPIC', 'REVIEW_PREREQUISITE', 'RECOVERY_STEP', 'REASSESSMENT', 'ADVANCE_TOPIC'
    title: str
    description: str
    topic_id: Optional[int] = None
    topic_name: Optional[str] = None
    subject: Optional[str] = None
    difficulty: Optional[str] = None
    cta_label: str
    cta_url: str

class WhatIfSimulationItem(BaseModel):
    scenario: str
    projected_mastery_gain: float
    projected_new_mastery: float
    projected_risk_reduction: str
    recommended_time_minutes: int

class StudentLearningTwinResponse(BaseModel):
    student_id: int
    student_name: str
    overall_mastery: float
    risk_level: str
    risk_score: float
    learning_velocity: float
    active_streak_days: int
    total_questions_answered: int
    accuracy_rate: float
    
    current_focus_topic: Optional[Dict[str, Any]] = None
    misconception_fingerprint: List[MisconceptionItem] = []
    prerequisite_gaps: List[PrerequisiteGapItem] = []
    recovery_mode: RecoveryModeStatus
    struggle_signal: StruggleSignalStatus
    decayed_topics: List[DecayedTopicItem] = []
    timeline: List[TimelineMilestone] = []
    next_best_action: NextBestAction
    what_if_simulations: List[WhatIfSimulationItem] = []

class ResetProfileResponse(BaseModel):
    success: bool
    message: str
    student_id: int
