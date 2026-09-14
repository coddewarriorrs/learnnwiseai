from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.services.report_service import ReportService
from app.core.permissions import get_current_user, require_role, verify_teacher_class_access

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/student")
def get_student_report(
    student_id: int = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    target_id = current_user.id
    if current_user.role in [UserRole.TEACHER, UserRole.ADMIN] and student_id:
        target_id = student_id

    data = ReportService.get_student_report_data(target_id, db)
    return data

@router.get("/student/download")
def download_student_csv(
    student_id: int = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    target_id = current_user.id
    if current_user.role in [UserRole.TEACHER, UserRole.ADMIN] and student_id:
        target_id = student_id

    csv_content = ReportService.generate_student_csv(target_id, db)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=student_report_{target_id}.csv"}
    )

@router.get("/class/{class_id}")
def get_class_report(
    class_id: int,
    current_user: User = Depends(require_role([UserRole.TEACHER, UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    verify_teacher_class_access(class_id, current_user, db)
    data = ReportService.get_class_report_data(class_id, current_user.id, db)
    return data

@router.get("/class/{class_id}/download")
def download_class_csv(
    class_id: int,
    current_user: User = Depends(require_role([UserRole.TEACHER, UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    verify_teacher_class_access(class_id, current_user, db)
    csv_content = ReportService.generate_class_csv(class_id, current_user.id, db)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=class_report_{class_id}.csv"}
    )
