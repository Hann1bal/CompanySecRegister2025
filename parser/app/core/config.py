from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://company_user:company_password@localhost:5432/company_db")
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Company Parser API"
    
    # Scheduler
    SCHEDULER_HOUR: int = 2  # 2 AM
    SCHEDULER_MINUTE: int = 0
    
    # Parser
    PARSER_BATCH_SIZE: int = 1000
    PARSER_MAX_CONCURRENT: int = 10
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()