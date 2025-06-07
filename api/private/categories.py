from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from models.categories import Category
from schemas.categories import CategoryCreate

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.post("/", response_model=CategoryCreate)
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category"""
    
    # Check if slug already exists
    existing_category = db.query(Category).filter(Category.slug == category.slug).first()
    if existing_category:
        raise HTTPException(
            status_code=400,
            detail="Slug already exists"
        )
    
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