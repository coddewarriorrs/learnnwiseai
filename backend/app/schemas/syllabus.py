from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime
from app.models.syllabus import NodeType, NodeStatus

class CurriculumNodeCreate(BaseModel):
    type: NodeType
    title: str
    code: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    prerequisites: List[str] = []
    status: NodeStatus = NodeStatus.PUBLISHED
    version: str = "1.0.0"
    order_index: int = 0

class CurriculumNodeResponse(BaseModel):
    id: int
    type: NodeType
    title: str
    code: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    prerequisites: List[Any] = []
    status: NodeStatus
    version: str
    order_index: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SyllabusTreeItem(CurriculumNodeResponse):
    children: List["SyllabusTreeItem"] = []
