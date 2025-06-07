from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from db.session import get_db
from models.customer import Customer
from models.users import User
from models.address import Address
from schemas.customers import (
    CustomerCreate,
    CustomerUpdate,
    CustomerInDB,
    CustomerPagination,
    CustomerType,
    CustomerStatus
)
from core.security import get_current_active_user

router = APIRouter(prefix="/api/customers", tags=["customers"])

@router.post("/", response_model=CustomerInDB)
async def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new customer."""
    # Create customer
    db_customer = Customer(
        customer_name=customer.customer_name,
        customer_type=customer.customer_type,
        phone_number=customer.phone,
        email=customer.email,
        status=customer.status,
        created_by=current_user.id,
        updated_by=current_user.id,
        assigned_user_id=current_user.id
    )
    
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.get("/{customer_id}", response_model=CustomerInDB)
async def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific customer by ID."""
    customer = db.query(Customer).get(customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return customer

@router.put("/{customer_id}", response_model=CustomerInDB)
async def update_customer(
    customer_id: int,
    customer_update: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a specific customer."""
    db_customer = db.query(Customer).get(customer_id)
    if not db_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Validate billing address if provided
    if customer_update.billing_address_id:
        billing_address = db.query(Address).get(customer_update.billing_address_id)
        if not billing_address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Billing address not found"
            )
    
    # Validate shipping address if provided
    if customer_update.shipping_address_id:
        shipping_address = db.query(Address).get(customer_update.shipping_address_id)
        if not shipping_address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shipping address not found"
            )
    
    # Update customer fields
    update_data = customer_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_customer, field, value)
    
    db_customer.updated_by = current_user.id
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a specific customer."""
    db_customer = db.query(Customer).get(customer_id)
    if not db_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    db.delete(db_customer)
    db.commit()

@router.get("/", response_model=CustomerPagination)
async def list_customers(
    page: int = Query(1, gt=0),
    size: int = Query(10, gt=0, le=100),
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", description="Sort order (asc or desc)"),
    customer_type: Optional[CustomerType] = None,
    status: Optional[CustomerStatus] = None,
    industry: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List customers with filtering, pagination, sorting and search."""
    query = db.query(Customer)

    # Apply filters
    if customer_type:
        query = query.filter(Customer.customer_type == customer_type)
    if status:
        query = query.filter(Customer.status == status)
    if industry:
        query = query.filter(Customer.industry == industry)
    if search:
        search_filter = or_(
            Customer.customer_name.ilike(f"%{search}%"),
            Customer.email.ilike(f"%{search}%"),
            Customer.phone_number.ilike(f"%{search}%"),
            Customer.tax_id.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    # Get total count
    total = query.count()

    # Apply sorting
    if hasattr(Customer, sort_by):
        sort_field = getattr(Customer, sort_by)
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