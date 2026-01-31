from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from api.core.database import supabase
from api.models.schemas import GithubProject, PaginatedResponse

router = APIRouter(prefix="/api/github", tags=["github"])

@router.get("/trending")
async def get_trending_projects(
    language: Optional[str] = None,
    since: Optional[str] = None, # daily, weekly, monthly
    page: int = 1,
    limit: int = 20
):
    try:
        query = supabase.table("github_projects").select("*", count="exact")
        
        if language:
            query = query.eq("language", language)
            
        # Pagination
        start = (page - 1) * limit
        end = start + limit - 1
        query = query.range(start, end).order("stars", desc=True)
        
        response = query.execute()
        
        return {
            "data": response.data,
            "total": response.count,
            "page": page,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{project_id}", response_model=GithubProject)
async def get_project_details(project_id: int):
    try:
        response = supabase.table("github_projects").select("*").eq("id", project_id).single().execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=404, detail="Project not found")
