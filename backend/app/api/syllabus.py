from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.models.syllabus import CurriculumNode, NodeType, NodeStatus
from app.models.syllabus_hierarchy import (
    Board, AcademicYear, AcademicClass, Subject, Unit, 
    Chapter, Topic, SubTopic, LearningOutcome
)
from app.models.question import Question
from app.schemas.syllabus import CurriculumNodeCreate, CurriculumNodeResponse, SyllabusTreeItem
from app.core.permissions import get_current_user, require_role
from typing import List, Dict, Any, Optional

router = APIRouter(prefix="/syllabus", tags=["syllabus"])

# =========================================================================
# 1. CANONICAL HIERARCHY ENDPOINTS (CBSE / NCERT Classes 8–12, 2026-27)
# =========================================================================

@router.get("")
def get_canonical_syllabus_overview(
    year: Optional[str] = "2026-27",
    db: Session = Depends(get_db)
):
    """Returns the canonical CBSE syllabus metadata and hierarchy overview."""
    acad_year = db.query(AcademicYear).filter(AcademicYear.year_code == year).first()
    if not acad_year:
        acad_year = db.query(AcademicYear).filter(AcademicYear.is_current == True).first()

    board = db.query(Board).filter(Board.id == acad_year.board_id).first() if acad_year else None
    classes = db.query(AcademicClass).filter(
        AcademicClass.academic_year_id == acad_year.id
    ).order_by(AcademicClass.class_number.asc()).all() if acad_year else []

    class_list = []
    for c in classes:
        subjs = db.query(Subject).filter(Subject.class_id == c.id).order_by(Subject.order_index.asc()).all()
        class_list.append({
            "id": c.id,
            "class_number": c.class_number,
            "title": c.title,
            "code": c.code,
            "subjects": [
                {
                    "id": s.id,
                    "name": s.name,
                    "code": s.code,
                    "is_integrated_science": s.is_integrated_science
                }
                for s in subjs
            ]
        })

    return {
        "board": {
            "id": board.id if board else 1,
            "name": board.name if board else "Central Board of Secondary Education",
            "code": board.code if board else "CBSE",
            "country": board.country if board else "India"
        },
        "academic_year": {
            "id": acad_year.id if acad_year else 1,
            "year_code": acad_year.year_code if acad_year else "2026-27",
            "title": acad_year.title if acad_year else "CBSE Academic Session 2026-2027",
            "is_current": acad_year.is_current if acad_year else True
        },
        "classes": class_list
    }

@router.get("/classes")
def list_syllabus_classes(
    year: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all canonical classes (Class 8 to 12) for the active academic year."""
    query = db.query(AcademicClass).join(AcademicYear, AcademicYear.id == AcademicClass.academic_year_id)
    if year:
        query = query.filter(AcademicYear.year_code == year)
    else:
        query = query.filter(AcademicYear.is_current == True)
    
    classes = query.order_by(AcademicClass.class_number.asc()).all()
    
    results = []
    for c in classes:
        subjects_count = db.query(Subject).filter(Subject.class_id == c.id).count()
        results.append({
            "id": c.id,
            "class_number": c.class_number,
            "title": c.title,
            "code": c.code,
            "description": c.description,
            "subjects_count": subjects_count
        })
    return results

@router.get("/classes/{class_id}")
def get_syllabus_class_details(
    class_id: int,
    db: Session = Depends(get_db)
):
    """Get specific class details, its subjects, and curriculum summary."""
    c = db.query(AcademicClass).filter(AcademicClass.id == class_id).first()
    if not c:
        # Fallback by class_number if class_id is 8, 9, 10, 11, 12
        c = db.query(AcademicClass).filter(AcademicClass.class_number == class_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Syllabus Class not found")

    subjects = db.query(Subject).filter(Subject.class_id == c.id).order_by(Subject.order_index.asc()).all()
    
    return {
        "id": c.id,
        "class_number": c.class_number,
        "title": c.title,
        "code": c.code,
        "description": c.description,
        "subjects": [
            {
                "id": s.id,
                "name": s.name,
                "code": s.code,
                "is_integrated_science": s.is_integrated_science,
                "description": s.description
            }
            for s in subjects
        ]
    }

@router.get("/classes/{class_id}/subjects")
def get_syllabus_class_subjects(
    class_id: int,
    db: Session = Depends(get_db)
):
    """
    List subjects for a given class:
    - Classes 8, 9, 10: Returns Mathematics and integrated Science.
      (Physics, Chemistry, Biology are NOT shown as separate board subjects).
    - Classes 11, 12: Returns separate Mathematics, Physics, Chemistry, Biology.
    """
    c = db.query(AcademicClass).filter(AcademicClass.id == class_id).first()
    if not c:
        c = db.query(AcademicClass).filter(AcademicClass.class_number == class_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Syllabus Class not found")

    subjects = db.query(Subject).filter(Subject.class_id == c.id).order_by(Subject.order_index.asc()).all()
    
    results = []
    for s in subjects:
        units_count = db.query(Unit).filter(Unit.subject_id == s.id).count()
        # Count chapters across all units of this subject
        chapters_count = (
            db.query(Chapter)
            .join(Unit, Unit.id == Chapter.unit_id)
            .filter(Unit.subject_id == s.id)
            .count()
        )
        results.append({
            "id": s.id,
            "class_id": c.id,
            "class_number": c.class_number,
            "class_title": c.title,
            "name": s.name,
            "code": s.code,
            "is_integrated_science": s.is_integrated_science,
            "description": s.description,
            "units_count": units_count,
            "chapters_count": chapters_count
        })
    return results

@router.get("/classes/{class_id}/subjects/{subject_id}")
def get_syllabus_subject_structure(
    class_id: int,
    subject_id: int,
    db: Session = Depends(get_db)
):
    """Returns the structured Units and Chapters hierarchy for a subject in a class."""
    s = db.query(Subject).filter(Subject.id == subject_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Subject not found")

    units = db.query(Unit).filter(Unit.subject_id == s.id).order_by(Unit.unit_number.asc()).all()
    
    unit_list = []
    for u in units:
        chapters = db.query(Chapter).filter(Chapter.unit_id == u.id).order_by(Chapter.chapter_number.asc()).all()
        chapter_list = []
        for ch in chapters:
            topics_count = db.query(Topic).filter(Topic.chapter_id == ch.id).count()
            chapter_list.append({
                "id": ch.id,
                "chapter_number": ch.chapter_number,
                "title": ch.title,
                "name": ch.title,
                "code": ch.code,
                "domain": ch.domain, # e.g. "Physics", "Chemistry", "Biology" for Science
                "description": ch.description,
                "topics_count": topics_count
            })
        unit_list.append({
            "id": u.id,
            "unit_number": u.unit_number,
            "title": u.title,
            "name": u.title,
            "code": u.code,
            "weightage_marks": u.weightage_marks,
            "chapters": chapter_list
        })

    return {
        "subject": {
            "id": s.id,
            "name": s.name,
            "code": s.code,
            "is_integrated_science": s.is_integrated_science
        },
        "units": unit_list
    }

@router.get("/chapters/{chapter_id}/topics")
def get_syllabus_chapter_topics(
    chapter_id: int,
    db: Session = Depends(get_db)
):
    """Returns all Topics, Sub-topics, Learning Outcomes, and Questions for a chapter."""
    ch = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not ch:
        raise HTTPException(status_code=404, detail="Chapter not found")

    topics = db.query(Topic).filter(Topic.chapter_id == ch.id).order_by(Topic.order_index.asc()).all()
    
    topic_list = []
    for t in topics:
        subtopics = db.query(SubTopic).filter(SubTopic.topic_id == t.id).order_by(SubTopic.order_index.asc()).all()
        los = db.query(LearningOutcome).filter(LearningOutcome.topic_id == t.id).all()
        q_count = db.query(Question).filter(Question.hierarchy_topic_id == t.id).count()
        
        topic_list.append({
            "id": t.id,
            "title": t.title,
            "code": t.code,
            "prerequisites": t.prerequisites or [],
            "subtopics": [{"id": st.id, "title": st.title, "code": st.code} for st in subtopics],
            "learning_outcomes": [
                {
                    "id": lo.id,
                    "code": lo.code,
                    "statement": lo.statement,
                    "bloom_level": lo.bloom_level
                }
                for lo in los
            ],
            "questions_count": q_count
        })

    return {
        "chapter": {
            "id": ch.id,
            "chapter_number": ch.chapter_number,
            "title": ch.title,
            "code": ch.code,
            "domain": ch.domain
        },
        "topics": topic_list
    }

# =========================================================================
# 2. ADMIN IMPORT MECHANISM (For future academic sessions e.g. 2027-28)
# =========================================================================

@router.post("/admin/import")
def import_future_syllabus(
    payload: Dict[str, Any],
    current_user: User = Depends(require_role([UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    """
    Admin import endpoint allowing syllabus updates for future academic years (e.g. 2027-28)
    without rewriting code or restarting the application.
    """
    board_data = payload.get("board", {"code": "CBSE", "name": "Central Board of Secondary Education"})
    year_data = payload.get("academic_year", {"year_code": "2027-28", "title": "CBSE Academic Session 2027-2028"})
    classes_data = payload.get("classes", [])

    # Board
    board = db.query(Board).filter(Board.code == board_data["code"]).first()
    if not board:
        board = Board(name=board_data["name"], code=board_data["code"])
        db.add(board)
        db.commit()
        db.refresh(board)

    # Academic Year
    acad_year = db.query(AcademicYear).filter(
        AcademicYear.board_id == board.id,
        AcademicYear.year_code == year_data["year_code"]
    ).first()
    if not acad_year:
        acad_year = AcademicYear(
            board_id=board.id,
            year_code=year_data["year_code"],
            title=year_data.get("title", f"Academic Session {year_data['year_code']}"),
            is_current=year_data.get("is_current", False)
        )
        db.add(acad_year)
        db.commit()
        db.refresh(acad_year)

    created_classes = 0
    created_topics = 0

    for c_item in classes_data:
        ac = db.query(AcademicClass).filter(
            AcademicClass.academic_year_id == acad_year.id,
            AcademicClass.class_number == c_item["class_number"]
        ).first()
        if not ac:
            ac = AcademicClass(
                academic_year_id=acad_year.id,
                class_number=c_item["class_number"],
                title=c_item["title"],
                code=c_item.get("code", f"{board.code}-{year_data['year_code']}-{c_item['class_number']}"),
                description=c_item.get("description", "")
            )
            db.add(ac)
            db.commit()
            db.refresh(ac)
            created_classes += 1

        for s_item in c_item.get("subjects", []):
            subj = db.query(Subject).filter(
                Subject.class_id == ac.id,
                Subject.name == s_item["name"]
            ).first()
            if not subj:
                subj = Subject(
                    class_id=ac.id,
                    name=s_item["name"],
                    code=s_item.get("code", f"{ac.code}-{s_item['name'][:4].upper()}"),
                    is_integrated_science=s_item.get("is_integrated_science", False)
                )
                db.add(subj)
                db.commit()
                db.refresh(subj)

            for u_item in s_item.get("units", []):
                unit = db.query(Unit).filter(
                    Unit.subject_id == subj.id,
                    Unit.title == u_item["title"]
                ).first()
                if not unit:
                    unit = Unit(
                        subject_id=subj.id,
                        unit_number=u_item.get("unit_number", 1),
                        title=u_item["title"],
                        code=u_item.get("code", f"{subj.code}-U{u_item.get('unit_number', 1)}")
                    )
                    db.add(unit)
                    db.commit()
                    db.refresh(unit)

                for ch_item in u_item.get("chapters", []):
                    ch = db.query(Chapter).filter(
                        Chapter.unit_id == unit.id,
                        Chapter.title == ch_item["title"]
                    ).first()
                    if not ch:
                        ch = Chapter(
                            unit_id=unit.id,
                            chapter_number=ch_item.get("chapter_number", 1),
                            title=ch_item["title"],
                            code=ch_item.get("code", f"{unit.code}-CH{ch_item.get('chapter_number', 1)}"),
                            domain=ch_item.get("domain")
                        )
                        db.add(ch)
                        db.commit()
                        db.refresh(ch)

                    for t_item in ch_item.get("topics", []):
                        top = db.query(Topic).filter(
                            Topic.chapter_id == ch.id,
                            Topic.title == t_item["title"]
                        ).first()
                        if not top:
                            top = Topic(
                                chapter_id=ch.id,
                                title=t_item["title"],
                                code=t_item.get("code", f"{ch.code}-T{created_topics + 1}"),
                                prerequisites=t_item.get("prerequisites", [])
                            )
                            db.add(top)
                            created_topics += 1

    db.commit()
    return {
        "message": "Successfully imported future academic session syllabus",
        "academic_year": acad_year.year_code,
        "classes_imported": created_classes,
        "topics_imported": created_topics
    }

# =========================================================================
# 3. BACKWARD COMPATIBILITY ENDPOINTS (Tree, Legacy Topics)
# =========================================================================

@router.get("/tree")
def get_syllabus_tree(db: Session = Depends(get_db)):
    all_nodes = db.query(CurriculumNode).order_by(CurriculumNode.order_index).all()
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
    # Query canonical topics table first
    topics = db.query(Topic).all()
    if topics:
        results = []
        for t in topics:
            chapter = db.query(Chapter).filter(Chapter.id == t.chapter_id).first()
            unit = db.query(Unit).filter(Unit.id == chapter.unit_id).first() if chapter else None
            subject = db.query(Subject).filter(Subject.id == unit.subject_id).first() if unit else None
            acad_class = db.query(AcademicClass).filter(AcademicClass.id == subject.class_id).first() if subject else None
            
            results.append({
                "id": t.id,
                "title": t.title,
                "code": t.code,
                "prerequisites": t.prerequisites or [],
                "chapter_id": chapter.id if chapter else None,
                "chapter_title": chapter.title if chapter else None,
                "domain": chapter.domain if chapter else None,
                "subject_id": subject.id if subject else None,
                "subject_title": subject.name if subject else "General",
                "class_id": acad_class.id if acad_class else None,
                "grade": acad_class.title if acad_class else "Class 11"
            })
        return sorted(results, key=lambda x: (x.get("grade") or "", x.get("subject_title") or "", x.get("chapter_title") or "", x["title"]))

    # Fallback to CurriculumNode if topics table empty
    all_nodes = {n.id: n for n in db.query(CurriculumNode).all()}
    c_topics = [n for n in all_nodes.values() if n.type == NodeType.TOPIC]
    results = []
    for t in c_topics:
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
