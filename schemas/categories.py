from typing import Optional
from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str
    slug: str
    description: Optional[dict] = None
    parent_id: Optional[int] = None
    tax_class_id: Optional[int] = None

    class Config:
        from_attributes = True
