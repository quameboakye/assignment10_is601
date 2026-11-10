import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration settings with SQLite fallback for local testing"""
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-for-testing")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()