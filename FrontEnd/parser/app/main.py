from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import datetime

from app.core.config import settings
from app.api.endpoints import companies, admin
from app.services.scheduler import start_scheduler, shutdown_scheduler
from app.database import get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_scheduler()
    yield
    await shutdown_scheduler()

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    companies.router,
    prefix=settings.API_V1_STR,
    tags=["companies"]
)

app.include_router(
    admin.router,
    prefix=settings.API_V1_STR + "/admin",
    tags=["admin"]
)

@app.get("/")
async def root():
    return {
        "message": "Company Parser API Service",
        "docs": "/api/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "timestamp": datetime.datetime.now().isoformat()
    }