from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Personal Finance Management System"
    API_V1_STR: str = "/api/v1"
    SQLALCHEMY_DATABASE_URL: str = "postgresql://postgres:2001d@localhost:5432/finance"
    
    # Auth Settings
    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY_KEEP_IT_SAFE" # Change this in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    
    GOOGLE_CLIENT_ID: str = "" # Provide this from Google Cloud Console

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
