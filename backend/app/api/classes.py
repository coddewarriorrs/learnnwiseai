from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.models.class_model import Class, ClassMember
from app.schemas.class_schema import ClassCreate, ClassResponse, ClassDetailResponse, JoinClassRequest
from app.schemas.auth import UserResponse
from app.core.permissions import get_current_user, require_role, verify_teacher_class_access
import secrets
import string

router = APIRouter(prefix="/classes", tags=["classes"])

def generate_class_code(length=6) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))

@router.post("", response_model=ClassResponse)
def create_class(
    req: ClassCreate,
    current_user: User = Depends(require_role([UserRole.TEACHER, UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    code = generate_class_code()
    while db.query(Class).filter(Class.class_code == code).first():
        code = generate_class_code()

    new_class = Class(
        name=req.name,
        grade=req.grade,
        subject=req.subject,
        board=req.board,
        academic_year=req.academic_year,
        teacher_id=current_user.id,
        class_code=code,
        invite_token=secrets.token_urlsafe(16),
        invite_active=True
    )
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    
    resp = ClassResponse.model_validate(new_class)
    resp.student_count = 0
    return resp

@router.get("", response_model=list[ClassResponse])
def get_classes(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role == UserRole.TEACHER:
        classes = db.query(Class).filter(Class.teacher_id == current_user.id).all()
    elif current_user.role == UserRole.STUDENT:
        classes = (
            db.query(Class)
            .join(ClassMember, ClassMember.class_id == Class.id)
            .filter(ClassMember.student_id == current_user.id)
            .all()
        )
    else: # ADMIN
        classes = db.query(Class).all()

    results = []
    for c in classes:
        count = db.query(ClassMember).filter(ClassMember.class_id == c.id).count()
        cr = ClassResponse.model_validate(c)
        cr.student_count = count
        results.append(cr)
    return results

@router.get("/{class_id}", response_model=ClassDetailResponse)
def get_class_detail(
    class_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    target_class = db.query(Class).filter(Class.id == class_id).first()
    if not target_class:
        raise HTTPException(status_code=404, detail="Class not found")

    if current_user.role == UserRole.TEACHER and target_class.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this class")

    members = (
        db.query(User)
        .join(ClassMember, ClassMember.student_id == User.id)
        .filter(ClassMember.class_id == class_id)
        .all()
    )

    resp = ClassDetailResponse.model_validate(target_class)
    resp.student_count = len(members)
    resp.students = [UserResponse.model_validate(m) for m in members]
    return resp

@router.post("/{class_id}/regenerate-invite", response_model=ClassResponse)
def regenerate_invite(
    class_id: int,
    current_user: User = Depends(require_role([UserRole.TEACHER, UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    target_class = verify_teacher_class_access(class_id, current_user, db)
    target_class.invite_token = secrets.token_urlsafe(16)
    target_class.invite_active = True
    db.commit()
    db.refresh(target_class)
    count = db.query(ClassMember).filter(ClassMember.class_id == target_class.id).count()
    resp = ClassResponse.model_validate(target_class)
    resp.student_count = count
    return resp

@router.patch("/{class_id}/toggle-invite", response_model=ClassResponse)
def toggle_invite(
    class_id: int,
    current_user: User = Depends(require_role([UserRole.TEACHER, UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    target_class = verify_teacher_class_access(class_id, current_user, db)
    target_class.invite_active = not target_class.invite_active
    db.commit()
    db.refresh(target_class)
    count = db.query(ClassMember).filter(ClassMember.class_id == target_class.id).count()
    resp = ClassResponse.model_validate(target_class)
    resp.student_count = count
    return resp

@router.get("/join/verify/{token}")
def verify_invite(token: str, db: Session = Depends(get_db)):
    target_class = db.query(Class).filter(Class.invite_token == token).first()
    if not target_class:
        raise HTTPException(status_code=404, detail="Invalid invite link")
    if not target_class.invite_active:
        raise HTTPException(status_code=400, detail="This invite link has been deactivated by the teacher")
    return {
        "valid": True,
        "class_id": target_class.id,
        "class_name": target_class.name,
        "subject": target_class.subject,
        "grade": target_class.grade
    }

@router.post("/join")
def join_class(
    req: JoinClassRequest,
    current_user: User = Depends(require_role([UserRole.STUDENT])),
    db: Session = Depends(get_db)
):
    target_class = None
    if req.invite_token:
        target_class = db.query(Class).filter(Class.invite_token == req.invite_token).first()
    elif req.class_code:
        target_class = db.query(Class).filter(Class.class_code == req.class_code.strip().upper()).first()

    if not target_class:
        raise HTTPException(status_code=404, detail="Class not found with the provided code or token")

    if not target_class.invite_active:
        raise HTTPException(status_code=400, detail="Class invites are currently disabled for this class")

    # Check duplicate membership
    existing = db.query(ClassMember).filter(
        ClassMember.class_id == target_class.id,
        ClassMember.student_id == current_user.id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="You are already enrolled in this class.")

    member = ClassMember(
        class_id=target_class.id,
        student_id=current_user.id
    )
    db.add(member)
    db.commit()

    return {
        "message": f"Successfully joined {target_class.name}!",
        "class_id": target_class.id,
        "class_name": target_class.name,
        "subject": target_class.subject
    }
