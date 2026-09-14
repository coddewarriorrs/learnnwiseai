from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.models.ai_chat import AIConversation, AIMessage
from app.models.syllabus import CurriculumNode
from app.schemas.ai import TutorChatRequest, TutorChatResponse, ImageAnalysisRequest, ImageAnalysisResult
from app.services.ai_tutor_service import AITutorService
from app.core.permissions import get_current_user, require_role
from typing import List

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/tutor", response_model=TutorChatResponse)
async def tutor_chat(
    req: TutorChatRequest,
    current_user: User = Depends(require_role([UserRole.STUDENT])),
    db: Session = Depends(get_db)
):
    result = await AITutorService.chat(
        student_id=current_user.id,
        message=req.message,
        topic_id=req.topic_id,
        conversation_id=req.conversation_id,
        image_base64=req.image_base64,
        voice_input=req.voice_input,
        question_context=req.question_context,
        client_message_id=req.client_message_id,
        db=db
    )
    return TutorChatResponse(**result)

@router.get("/active-session")
def get_active_session(
    current_user: User = Depends(require_role([UserRole.STUDENT])),
    db: Session = Depends(get_db)
):
    """
    Returns the most recent conversation session and its messages for the student,
    ensuring continuity across page refreshes.
    """
    conv = (
        db.query(AIConversation)
        .filter(AIConversation.student_id == current_user.id)
        .order_by(AIConversation.created_at.desc())
        .first()
    )
    if not conv:
        return {"conversation_id": None, "messages": []}

    msgs = (
        db.query(AIMessage)
        .filter(AIMessage.conversation_id == conv.id)
        .order_by(AIMessage.created_at.asc())
        .all()
    )
    return {
        "conversation_id": conv.id,
        "title": conv.title,
        "messages": [
            {
                "id": str(m.id),
                "sender": m.sender.value,
                "content": m.content,
                "image_url": m.image_url,
                "image_analysis": m.image_analysis,
                "timestamp": m.created_at.strftime("%H:%M") if m.created_at else None,
                "created_at": m.created_at
            }
            for m in msgs
        ]
    }

@router.post("/analyze-image", response_model=ImageAnalysisResult)
def analyze_solution_image(
    req: ImageAnalysisRequest,
    current_user: User = Depends(require_role([UserRole.STUDENT])),
    db: Session = Depends(get_db)
):
    """
    Dedicated endpoint for analyzing notebook / handwritten math or science solutions:
    - Identifies mathematical steps
    - Detects first incorrect step
    - Explains WHERE, WHY, and HOW to correct
    """
    topic_title = "Mathematics & Science"
    if req.topic_id:
        topic_node = db.query(CurriculumNode).filter(CurriculumNode.id == req.topic_id).first()
        if topic_node:
            topic_title = topic_node.title

    analysis = AITutorService.analyze_handwritten_solution(
        image_base64=req.image_base64,
        topic_title=topic_title,
        message=req.problem_context
    )
    return ImageAnalysisResult(**analysis)

@router.get("/conversations")
def list_conversations(
    current_user: User = Depends(require_role([UserRole.STUDENT])),
    db: Session = Depends(get_db)
):
    conversations = (
        db.query(AIConversation)
        .filter(AIConversation.student_id == current_user.id)
        .order_by(AIConversation.created_at.desc())
        .all()
    )
    return [
        {
            "id": c.id,
            "title": c.title,
            "topic_id": c.topic_id,
            "created_at": c.created_at
        }
        for c in conversations
    ]

@router.get("/conversations/{conversation_id}/messages")
def get_conversation_messages(
    conversation_id: int,
    current_user: User = Depends(require_role([UserRole.STUDENT])),
    db: Session = Depends(get_db)
):
    conv = db.query(AIConversation).filter(
        AIConversation.id == conversation_id,
        AIConversation.student_id == current_user.id
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found or access denied")

    messages = (
        db.query(AIMessage)
        .filter(AIMessage.conversation_id == conversation_id)
        .order_by(AIMessage.created_at.asc())
        .all()
    )
    return [
        {
            "id": m.id,
            "sender": m.sender.value,
            "content": m.content,
            "image_url": m.image_url,
            "image_analysis": m.image_analysis,
            "created_at": m.created_at
        }
        for m in messages
    ]
