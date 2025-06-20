from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db.session import get_db
from models.categories import Category
from schemas.categories import CategoryCreate, CategoryPagination, CategoryResponse

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.post("/", response_model=CategoryResponse)
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category"""
    # Check if parent exists if parent_id is provided
    if category.parent_id:
        parent = db.query(Category).filter(Category.id == category.parent_id).first()
        if not parent:
            raise HTTPException(
                status_code=404,
                detail="Parent category not found"
            )
    
    # Check if tax_class exists if tax_class_id is provided
    if category.tax_class_id:
        from models.tax import TaxClass
        tax_class = db.query(TaxClass).filter(TaxClass.id == category.tax_class_id).first()
        if not tax_class:
            raise HTTPException(
                status_code=404,
                detail="Tax class not found"
            )
    
    # Create new category
    db_category = Category(
        name=category.name,
        slug=category.slug,
        description=category.description,
        parent_id=category.parent_id,
        tax_class_id=category.tax_class_id
    )
    
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category


@router.get("/", response_model=CategoryPagination)
async def list_categories(
    page: int = Query(1, gt=0),
    size: int = Query(10, gt=0, le=100),
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", description="Sort order (asc or desc)"),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List categories with filtering, pagination, sorting and search."""
    query = db.query(Category)

    # Apply filters
    if search:
        query = query.filter(Category.name.ilike(f"%{search}%"))
    
    # Get total count
    total = query.count()
    
    # Apply sorting
    if hasattr(Category, sort_by):
        sort_field = getattr(Category, sort_by)
        if sort_order == "desc":
            sort_field = sort_field.desc()
        query = query.order_by(sort_field)
        
    # Apply pagination
    query = query.offset((page - 1) * size).limit(size)

    return {
        "items": query.all(),
        "total": total,
        "page": page,
        "size": size
    }
