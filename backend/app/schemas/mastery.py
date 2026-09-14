from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.mastery import MasteryStatus

class TopicMasteryItem(BaseModel):
    topic_id: int
    topic_title: str
    subject: Optional[str] = None
    chapter: Optional[str] = None
    mastery_score: float
    status: MasteryStatus
    total_attempts: int
    correct_attempts: int
    accuracy_percentage: float
    last_attempt_at: Optional[datetime] = None

class StudentMasteryOverview(BaseModel):
    overall_mastery: float
    topics_mastered: int
    topics_needing_attention: int
    critical_topics: int
    topics: List[TopicMasteryItem] = []
