from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ImageAnalysisStep(BaseModel):
    step_number: int
    step_content: str
    is_correct: bool
    comment: Optional[str] = None

class ImageAnalysisResult(BaseModel):
    is_readable: bool = True
    unreadable_reason: Optional[str] = None
    problem_statement_detected: Optional[str] = None
    steps: List[ImageAnalysisStep] = []
    first_incorrect_step: Optional[int] = None
    mistake_type: Optional[str] = None
    where_error_occurred: Optional[str] = None
    why_error_occurred: Optional[str] = None
    how_to_correct: Optional[str] = None
    correct_final_result: Optional[str] = None

class TutorChatRequest(BaseModel):
    message: str
    topic_id: Optional[int] = None
    conversation_id: Optional[int] = None
    image_base64: Optional[str] = None
    audio_base64: Optional[str] = None
    voice_input: Optional[bool] = False
    question_context: Optional[Dict[str, Any]] = None
    client_timestamp: Optional[str] = None
    client_message_id: Optional[str] = None

class TutorChatResponse(BaseModel):
    conversation_id: int
    message_id: Optional[int] = None
    client_message_id: Optional[str] = None
    reply: str
    suggested_questions: List[str] = []
    prerequisite_remedy: Optional[Dict[str, Any]] = None
    image_analysis: Optional[ImageAnalysisResult] = None
    audio_narration_url: Optional[str] = None
    twin_context_applied: Optional[Dict[str, Any]] = None

class ImageAnalysisRequest(BaseModel):
    image_base64: str
    problem_context: Optional[str] = None
    topic_id: Optional[int] = None


class LearningPathStep(BaseModel):
    step_number: int
    title: str
    concept: str
    type: str # 'PREREQUISITE_REVIEW', 'CONCEPT_EXPLANATION', 'PRACTICE', 'ASSESSMENT'
    is_completed: bool = False
    topic_id: Optional[int] = None
    recommendation_reason: str

class LearningPathResponse(BaseModel):
    student_id: int
    subject: str
    current_focus_topic: str
    current_mastery: float
    recovery_mode_active: bool
    path: List[LearningPathStep] = []
