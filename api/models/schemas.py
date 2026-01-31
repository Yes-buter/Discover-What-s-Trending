from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from uuid import UUID

# GitHub Project Models
class GithubProjectBase(BaseModel):
    repo_id: str
    name: str
    full_name: str
    description: Optional[str] = None
    language: Optional[str] = None
    stars: int
    forks: int
    url: str
    trending_date: date

class GithubProject(GithubProjectBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Paper Models
class PaperBase(BaseModel):
    title: str
    abstract: str
    authors: List[str]
    pdf_url: Optional[str] = None
    code_url: Optional[str] = None
    published_date: date
    source: str
    category_id: Optional[UUID] = None

class Paper(PaperBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Category Models
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    slug: str

class Category(CategoryBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# User Models
class UserBase(BaseModel):
    # email: str # Removed email
    username: str
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Favorite Models
class FavoriteBase(BaseModel):
    item_type: str
    item_id: str

class FavoriteCreate(FavoriteBase):
    pass

class Favorite(FavoriteBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Subscription Models
class SubscriptionBase(BaseModel):
    keyword: Optional[str] = None
    category: Optional[str] = None
    is_active: bool = True

class SubscriptionCreate(SubscriptionBase):
    pass

class Subscription(SubscriptionBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Response Models
class PaginatedResponse(BaseModel):
    data: List[dict]
    total: int
    page: int
    limit: int
