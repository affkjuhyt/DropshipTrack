from token import OP
from typing import Optional
from pydantic import BaseModel
from enum import Enum


class ProductStatus(str, Enum):
    AVAILABLE = 'available'
    OUT_OF_STOCK = 'out_of_stock'
    DISCONTINUED = 'discontinued'


class ProductCreate(BaseModel):
    name: str
    sku: str
    price: float
    quantity: int
    category_id: int
    status: ProductStatus
    
    
class ProductResponse(BaseModel):
    id: int
    name: str
    sku: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    category_id: Optional[int] = None
    status: ProductStatus
    

class ProductPagination(BaseModel):
    items: list[ProductResponse]
    total: int
    page: int
    size: int
    