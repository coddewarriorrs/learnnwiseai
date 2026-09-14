from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.schemas.practice import QuestionResponse

class AssessmentCreate(BaseModel):
    class_id: int
    title: str
    description: Optional[str] = None
    duration_minutes: int = 30
    due_date: Optional[datetime] = None
    question_ids: List[int] = []

class AssessmentResponse(BaseModel):
    id: int
    class_id: int
    title: str
    description: Optional[str] = None
    duration_minutes: int
    due_date: Optional[datetime] = None
    is_published: bool
    total_points: int
    created_at: Optional[datetime] = None
    question_count: Optional[int] = 0

    class Config:
        from_attributes = True

class AssessmentDetailResponse(AssessmentResponse):
    questions: List[QuestionResponse] = []

class AssessmentSubmitRequest(BaseModel):
    answers: List[Dict[str, Any]] # [{"question_id": 1, "selected_answer": "A", "time_taken_seconds": 20}]
    time_taken_seconds: int = 0

class AssessmentResultResponse(BaseModel):
    attempt_id: int
    score: float
    max_score: float
    percentage: float
    status: str
    feedback: str
    topic_mastery_impact: List[Dict[str, Any]] = []
    risk_updated: bool = True
