from fastapi import APIRouter, HTTPException, BackgroundTasks
from api.services.crawlers import crawler_service

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.post("/crawl")
async def trigger_crawl(background_tasks: BackgroundTasks):
    """
    Trigger a background crawl task for all sources.
    """
    background_tasks.add_task(crawler_service.crawl_all)
    return {"message": "Crawl task started in background"}
