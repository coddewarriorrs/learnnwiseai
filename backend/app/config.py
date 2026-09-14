from pydantic_settings import BaseSettings
from typing import Optional, List
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "LearnWise AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./learnwise.db")
    
    JWT_SECRET: str = os.getenv("JWT_SECRET", "learnwise-super-secret-key-change-in-prod-2026-hackathon")
    JWT_REFRESH_SECRET: str = os.getenv("JWT_REFRESH_SECRET", "learnwise-refresh-super-secret-key-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "*"
    ]
    
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "gemini")
    AI_API_KEY: Optional[str] = os.getenv("AI_API_KEY", None)
    AI_MODEL: str = os.getenv("AI_MODEL", "gemini-1.5-flash")
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
