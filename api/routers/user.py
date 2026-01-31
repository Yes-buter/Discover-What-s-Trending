from fastapi import APIRouter, HTTPException, Depends
from typing import List
from api.core.database import supabase
from api.models.schemas import Favorite, FavoriteCreate
from api.routers.auth import get_current_user

router = APIRouter(prefix="/api/user", tags=["user"])

@router.get("/favorites", response_model=List[Favorite])
async def get_favorites(current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.id
        response = supabase.table("favorites").select("*").eq("user_id", user_id).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/favorites/enriched")
async def get_enriched_favorites(current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.id
        # Get all favorites
        favs = supabase.table("favorites").select("*").eq("user_id", user_id).execute().data
        
        project_ids = [int(f['item_id']) for f in favs if f['item_type'] == 'project' and f['item_id'].isdigit()]
        paper_ids = [f['item_id'] for f in favs if f['item_type'] == 'paper']
        
        projects = []
        if project_ids:
            # Fetch projects
            # Note: Supabase-py doesn't support 'in_' very well in some versions, but 'in' operator is standard.
            # .in_("id", project_ids)
            p_res = supabase.table("github_projects").select("*").in_("id", project_ids).execute()
            projects = p_res.data
            
        papers = []
        if paper_ids:
            # Fetch papers
            p_res = supabase.table("papers").select("*").in_("id", paper_ids).execute()
            papers = p_res.data
            
        return {
            "projects": projects,
            "papers": papers
        }
    except Exception as e:
        print(f"Error fetching enriched favorites: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/favorites", response_model=Favorite)
async def add_favorite(favorite: FavoriteCreate, current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.id
        data = favorite.dict()
        data["user_id"] = user_id
        
        response = supabase.table("favorites").insert(data).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/favorites/{item_type}/{item_id}")
async def remove_favorite(item_type: str, item_id: str, current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.id
        response = supabase.table("favorites").delete().eq("user_id", user_id).eq("item_type", item_type).eq("item_id", item_id).execute()
        return {"message": "Favorite removed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
