from typing import Optional
from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None
    tax_class_id: Optional[int] = None

    class Config:
        from_attributes = True
        

class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None
    tax_class_id: Optional[int] = None
    
    
class CategoryPagination(BaseModel):
    items: list[CategoryResponse]
    total: int
    page: int
    size: int

