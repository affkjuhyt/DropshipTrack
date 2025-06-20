from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from db.session import get_db
from models.products import Product, ProductVariant
from models.stock import StockMovement
from schemas.products import ProductCreate, ProductResponse, ProductPagination, ProductStatus


router = APIRouter(prefix="/api/products", tags=["products"])

@router.post("/", response_model=ProductResponse)
async def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product along with its default variant and initial stock"""

    # Check if product with same name exists
    existing_product = db.query(Product).filter(Product.name == product_data.name).first()
    if existing_product:
        raise HTTPException(
            status_code=400,
            detail=f"Product with name '{product_data.name}' already exists"
        )

    # Check if product variant with same SKU exists
    existing_variant = db.query(ProductVariant).filter(ProductVariant.sku == product_data.sku).first()
    if existing_variant:
        raise HTTPException(
            status_code=400,
            detail=f"Product variant with SKU '{product_data.sku}' already exists"
        )

    product = Product(
        name=product_data.name,
        status=product_data.status,
        category_id=product_data.category_id,
    )
    db.add(product)
    db.flush()

    product_variant = ProductVariant(
        sku=product_data.sku,
        name=product_data.name,
        product_id=product.id,
    )
    db.add(product_variant)
    db.flush()

    stock_movement = StockMovement(
        product_variant_id=product_variant.id,
        type="none",
        reference="manual",
    )
    db.add(stock_movement)

    db.commit()
    db.refresh(product)

    return product


@router.get("/", response_model=ProductPagination)
async def list_products(
    page: int = Query(1, gt=0),
    size: int = Query(10, gt=0, le=100),
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", description="Sort order (asc or desc)"),
    status: Optional[ProductStatus] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List products with filtering, pagination, sorting and search.
    
    Args:
        page: Page number (starts from 1)
        size: Number of items per page (max 100)
        sort_by: Field to sort by
        sort_order: Sort order (asc or desc)
        status: Filter by product status
        search: Search in product name or SKU
        db: Database session
        
    Returns:
        Paginated list of products matching the criteria
    """
    query = db.query(Product)
    
    # Apply filters
    if status:
        query = query.filter(Product.status == status)
    if search:
        search_filter = or_(
            Product.name.ilike(f"%{search}%"),
            # Product.sku.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Get total count
    total = query.count()
    
    # Apply sorting
    if hasattr(Product, sort_by):
        sort_field = getattr(Product, sort_by)
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
