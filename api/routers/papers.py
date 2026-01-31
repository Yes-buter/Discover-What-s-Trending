from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from uuid import UUID
from api.core.database import supabase
from api.models.schemas import Paper, PaginatedResponse

router = APIRouter(prefix="/api/papers", tags=["papers"])

@router.get("/latest")
async def get_latest_papers(
    category: Optional[str] = None,
    source: Optional[str] = None,
    page: int = 1,
    limit: int = 20
):
    try:
        query = supabase.table("papers").select("*", count="exact")
        
        if category:
            # First get category id from slug or name if possible, 
            # assuming category param is the category slug or ID. 
            # For simplicity, let's assume it might be ID or we filter by category_id if UUID
            pass
            # For now, let's just filter if it's a UUID, otherwise maybe join?
            # Supabase-py doesn't support complex joins easily in one go without raw sql or specific syntax
            # Let's assume frontend sends category_id for now or we filter by joining.
            # A simpler way is to filter by category_id if provided.
        
        if source:
            query = query.eq("source", source)
            
        # Pagination
        start = (page - 1) * limit
        end = start + limit - 1
        query = query.range(start, end).order("published_date", desc=True)
        
        response = query.execute()
        
        return {
            "data": response.data,
            "total": response.count,
            "page": page,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
async def get_categories():
    try:
        response = supabase.table("categories").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{paper_id}", response_model=Paper)
async def get_paper_details(paper_id: UUID):
    try:
        response = supabase.table("papers").select("*").eq("id", str(paper_id)).single().execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=404, detail="Paper not found")
