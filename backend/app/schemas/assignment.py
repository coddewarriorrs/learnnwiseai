from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.assignment import SubmissionStatus

class AssignmentCreate(BaseModel):
    class_id: int
    title: str
    instructions: str
    topic_id: Optional[int] = None
    total_points: int = 50
    due_date: Optional[datetime] = None

class AssignmentResponse(BaseModel):
    id: int
    class_id: int
    class_name: Optional[str] = None
    title: str
    instructions: str
    topic_id: Optional[int] = None
    total_points: int
    due_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    submission_status: Optional[SubmissionStatus] = None
    submission_grade: Optional[float] = None

    class Config:
        from_attributes = True

class SubmissionSubmitRequest(BaseModel):
    content: str

class GradeSubmissionRequest(BaseModel):
    grade: float
    feedback: str
