from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.models.question import DifficultyLevel

class QuestionOption(BaseModel):
    id: str
    text: str

class QuestionResponse(BaseModel):
    id: int
    topic_id: int
    topic_name: Optional[str] = None
    subject_name: Optional[str] = None
    chapter_name: Optional[str] = None
    title: str
    prompt: str
    options: List[Dict[str, Any]]
    difficulty: DifficultyLevel
    points: int

    class Config:
        from_attributes = True

class StartPracticeRequest(BaseModel):
    class_id: Optional[int] = None
    subject: Optional[str] = None
    subject_id: Optional[int] = None
    chapter: Optional[str] = None
    chapter_id: Optional[int] = None
    topic_id: Optional[int] = None
    difficulty: Optional[DifficultyLevel] = None
    num_questions: int = Field(default=5, ge=1, le=50)
    exclude_ids: Optional[List[int]] = None

class SubmitAnswerRequest(BaseModel):
    question_id: int
    selected_answer: str
    time_taken_seconds: int = 15

class SubmitAnswerResponse(BaseModel):
    question_id: int
    is_correct: bool
    correct_answer: str
    explanation: str
    explanation_brief: Optional[str] = None
    explanation_full: Optional[str] = None
    mistake_type: Optional[str] = None
    concept_involved: Optional[str] = None
    how_to_avoid: Optional[str] = None
    prerequisite_hint: Optional[str] = None
    updated_mastery_score: float
    updated_mastery_status: str
    root_cause_warning: Optional[str] = None
    recommended_remedy: Optional[str] = None
    stay_on_topic: bool = False
    stay_on_topic_reason: Optional[str] = None
    consecutive_successes: int = 0
    next_recommended_topic_id: Optional[int] = None
    recovery_mode_triggered: bool = False
    misconception_alert: Optional[str] = None

