from fastapi import APIRouter
from app.api import auth, classes, students, teachers, practice, assessments, assignments, interventions, risk, ai, syllabus, admin, reports, websocket, learning_twin

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(classes.router)
api_router.include_router(students.router)
api_router.include_router(teachers.router)
api_router.include_router(practice.router)
api_router.include_router(assessments.router)
api_router.include_router(assignments.router)
api_router.include_router(interventions.router)
api_router.include_router(risk.router)
api_router.include_router(ai.router)
api_router.include_router(learning_twin.router)
api_router.include_router(syllabus.router)
api_router.include_router(admin.router)
api_router.include_router(reports.router)
api_router.include_router(websocket.router)

