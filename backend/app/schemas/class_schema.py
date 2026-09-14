from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.auth import UserResponse

class ClassCreate(BaseModel):
    name: str = Field(..., min_length=2)
    grade: str
    subject: str
    board: str = "CBSE"
    academic_year: str = "2026-2027"

class ClassResponse(BaseModel):
    id: int
    name: str
    grade: str
    subject: str
    board: str
    academic_year: str
    teacher_id: int
    class_code: str
    invite_token: str
    invite_active: bool
    invite_expires_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    student_count: Optional[int] = 0

    class Config:
        from_attributes = True

class ClassDetailResponse(ClassResponse):
    students: List[UserResponse] = []

class JoinClassRequest(BaseModel):
    class_code: Optional[str] = None
    invite_token: Optional[str] = None
