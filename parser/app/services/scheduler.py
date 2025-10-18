from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from datetime import datetime

from ..core.config import settings

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()

async def start_scheduler():
    """
    Запуск планировщика для ежедневного обновления
    """
    try:
        # Ежедневный запуск в 2:00
        scheduler.add_job(
            scheduled_data_refresh,
            trigger=CronTrigger(
                hour=settings.SCHEDULER_HOUR,
                minute=settings.SCHEDULER_MINUTE
            ),
            id="daily_data_refresh"
        )
        
        if not scheduler.running:
            scheduler.start()
            
        logger.info(f"Scheduler started. Next run at {scheduler.get_jobs()[0].next_run_time}")
        
    except Exception as e:
        logger.error(f"Error starting scheduler: {str(e)}")

async def shutdown_scheduler():
    """
    Остановка планировщика
    """
    if scheduler.running:
        scheduler.shutdown()
    logger.info("Scheduler stopped")

async def scheduled_data_refresh():
    """
    Задача для ежедневного обновления данных
    """
    logger.info("Starting scheduled data refresh")
    
    try:
        logger.info("Scheduled data refresh completed")
        
    except Exception as e:
        logger.error(f"Scheduled data refresh failed: {str(e)}")