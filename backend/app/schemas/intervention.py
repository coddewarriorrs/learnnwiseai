from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.intervention import InterventionType, InterventionStatus

class InterventionCreate(BaseModel):
    student_id: int
    topic_id: Optional[int] = None
    type: InterventionType = InterventionType.PREREQUISITE_REVIEW
    reason: str
    action: str

class InterventionUpdate(BaseModel):
    status: InterventionStatus

class InterventionResponse(BaseModel):
    id: int
    student_id: int
    student_name: Optional[str] = None
    teacher_id: int
    teacher_name: Optional[str] = None
    topic_id: Optional[int] = None
    topic_title: Optional[str] = None
    type: InterventionType
    reason: str
    action: str
    status: InterventionStatus
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TeacherNoteCreate(BaseModel):
    student_id: int
    note: str

class TeacherNoteResponse(BaseModel):
    id: int
    teacher_id: int
    student_id: int
    note: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
