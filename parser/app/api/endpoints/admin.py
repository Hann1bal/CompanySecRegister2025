from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.database import get_db
from app.services.parser import DataParser

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/refresh-data")
async def refresh_data(
    background_tasks: BackgroundTasks,
    full_refresh: bool = False,
    limit: int = Query(100, ge=1, le=1000, description="Number of companies to parse"),
    db: AsyncSession = Depends(get_db)
):
    try:
        parser = DataParser(db)
        
        background_tasks.add_task(
            parser.run_parsing,
            full_refresh=full_refresh,
            limit=limit
        )
        
        return {
            "message": "Data refresh started in background",
            "full_refresh": full_refresh,
            "limit": limit,
            "status": "processing"
        }
        
    except Exception as e:
        logger.error(f"Error starting data refresh: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error starting data refresh: {str(e)}"
        )

@router.get("/parser-status")
async def get_parser_status():
    return {
        "status": "unknown",
        "last_run": None,
        "next_run": "02:00"
    }