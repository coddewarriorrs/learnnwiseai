from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.models.syllabus import CurriculumNode, NodeType, NodeStatus
from app.schemas.syllabus import CurriculumNodeCreate, CurriculumNodeResponse, SyllabusTreeItem
from app.core.permissions import get_current_user, require_role
from typing import List, Dict, Any

router = APIRouter(prefix="/syllabus", tags=["syllabus"])

@router.get("", response_model=List[CurriculumNodeResponse])
def get_syllabus_nodes(
    type: NodeType = None,
    parent_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(CurriculumNode).filter(CurriculumNode.status == NodeStatus.PUBLISHED)
    if type:
        query = query.filter(CurriculumNode.type == type)
    if parent_id is not None:
        query = query.filter(CurriculumNode.parent_id == parent_id)
    nodes = query.order_by(CurriculumNode.order_index).all()
    return [CurriculumNodeResponse.model_validate(n) for n in nodes]

@router.get("/tree")
def get_syllabus_tree(db: Session = Depends(get_db)):
    all_nodes = db.query(CurriculumNode).order_by(CurriculumNode.order_index).all()
    
    # Build tree from nodes
    node_map = {}
    for n in all_nodes:
        node_map[n.id] = {
            "id": n.id,
            "type": n.type.value,
            "title": n.title,
            "code": n.code,
            "description": n.description,
            "parent_id": n.parent_id,
            "prerequisites": n.prerequisites or [],
            "status": n.status.value,
            "order_index": n.order_index,
            "children": []
        }

    tree = []
    for n in all_nodes:
        if n.parent_id is None or n.parent_id not in node_map:
            tree.append(node_map[n.id])
        else:
            node_map[n.parent_id]["children"].append(node_map[n.id])

    return tree

@router.get("/topics")
def get_topics(db: Session = Depends(get_db)):
    all_nodes = {n.id: n for n in db.query(CurriculumNode).all()}
    topics = [n for n in all_nodes.values() if n.type == NodeType.TOPIC]
    
    results = []
    for t in topics:
        chapter = all_nodes.get(t.parent_id)
        subject = all_nodes.get(chapter.parent_id) if chapter else None
        grade = all_nodes.get(subject.parent_id) if subject else None
        
        results.append({
            "id": t.id,
            "title": t.title,
            "code": t.code,
            "prerequisites": t.prerequisites or [],
            "chapter_id": chapter.id if chapter else None,
            "chapter_title": chapter.title if chapter else None,
            "subject_id": subject.id if subject else None,
            "subject_title": subject.title if subject else "General",
            "grade": grade.title if grade else None
        })
    return sorted(results, key=lambda x: (x["subject_title"] or "", x["chapter_title"] or "", x["title"]))

@router.post("", response_model=CurriculumNodeResponse)
def create_syllabus_node(
    req: CurriculumNodeCreate,
    current_user: User = Depends(require_role([UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    existing = db.query(CurriculumNode).filter(CurriculumNode.code == req.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Node with this code already exists")

    node = CurriculumNode(
        type=req.type,
        title=req.title,
        code=req.code,
        description=req.description,
        parent_id=req.parent_id,
        prerequisites=req.prerequisites,
        status=req.status,
        version=req.version,
        order_index=req.order_index
    )
    db.add(node)
    db.commit()
    db.refresh(node)
    return CurriculumNodeResponse.model_validate(node)

@router.post("/import")
def import_syllabus_nodes(
    nodes: List[CurriculumNodeCreate],
    current_user: User = Depends(require_role([UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    imported = 0
    for item in nodes:
        existing = db.query(CurriculumNode).filter(CurriculumNode.code == item.code).first()
        if existing:
            existing.title = item.title
            existing.description = item.description
            existing.prerequisites = item.prerequisites
            existing.status = item.status
            existing.order_index = item.order_index
        else:
            node = CurriculumNode(
                type=item.type,
                title=item.title,
                code=item.code,
                description=item.description,
                parent_id=item.parent_id,
                prerequisites=item.prerequisites,
                status=item.status,
                order_index=item.order_index
            )
            db.add(node)
        imported += 1
    db.commit()
    return {"message": f"Successfully processed {imported} syllabus nodes"}
