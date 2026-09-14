from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import decode_token
from app.models.user import User, UserRole
from app.models.class_model import Class, ClassMember
from typing import List

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        raise credentials_exception
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None or not user.is_active:
        raise credentials_exception
    return user

def require_role(allowed_roles: List[UserRole]):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Requires one of roles: {[r.value for r in allowed_roles]}"
            )
        return current_user
    return role_checker

def verify_teacher_class_access(class_id: int, teacher: User, db: Session) -> Class:
    target_class = db.query(Class).filter(Class.id == class_id).first()
    if not target_class:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")
    if target_class.teacher_id != teacher.id and teacher.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to this class")
    return target_class

def verify_teacher_student_access(student_id: int, teacher: User, db: Session) -> User:
    if teacher.role == UserRole.ADMIN:
        student = db.query(User).filter(User.id == student_id, User.role == UserRole.STUDENT).first()
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        return student
    
    # Check if student is in any class taught by this teacher
    shared_class = (
        db.query(ClassMember)
        .join(Class, Class.id == ClassMember.class_id)
        .filter(Class.teacher_id == teacher.id, ClassMember.student_id == student_id)
        .first()
    )
    if not shared_class:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Student does not belong to any of your classes."
        )
    student = db.query(User).filter(User.id == student_id).first()
    return student
