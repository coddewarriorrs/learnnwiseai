from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.api.router import api_router

# Auto-create tables if not existing
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description='LearnWise AI: Adaptive Smart Education Platform'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

from fastapi.responses import RedirectResponse
import urllib.parse

@app.get('/health', tags=['health'])
def health_check():
    return {
        'status': 'healthy',
        'project': settings.PROJECT_NAME,
        'version': settings.VERSION
    }

@app.get('/whatsapp', tags=['integrations'])
@app.get('/api/whatsapp', tags=['integrations'])
def redirect_to_whatsapp(phone: str = "", text: str = "Hello from LearnWise AI - Education that adapts to every learner!"):
    clean_phone = "".join([c for c in phone if c.isdigit()])
    encoded_text = urllib.parse.quote(text)
    if clean_phone:
        target_url = f"https://wa.me/{clean_phone}?text={encoded_text}"
    else:
        target_url = f"https://web.whatsapp.com/send?text={encoded_text}"
    return RedirectResponse(url=target_url, status_code=307)

@app.get('/', tags=['root'])
def root():
    return {
        'message': 'Welcome to LearnWise AI API',
        'docs': '/docs',
        'health': '/health',
        'whatsapp': '/whatsapp'
    }

