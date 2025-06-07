from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
import enum

class CustomerType(enum.Enum):
    INDIVIDUAL = "individual"
    BUSINESS = "business"

class CustomerStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    LEAD = "lead"

class CustomerBase(BaseModel):
    customer_name: str = Field(alias="customerName")
    customer_type: CustomerType = Field(alias="customerType")
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address_line1: Optional[str] = Field(None, alias="addressLine1")
    address_line2: Optional[str] = Field(None, alias="addressLine2")
    city: Optional[str] = None
    state: Optional[str] = None
    zipCode: Optional[str] = None
    country: Optional[str] = None
    status: CustomerStatus = CustomerStatus.LEAD
    
    class Config:
        from_attributes = True
        populate_by_name = True

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class CustomerInDB(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int]
    updated_by: Optional[int]
    assigned_user_id: Optional[int]

    class Config:
        from_attributes = True

class CustomerFilter(BaseModel):
    customer_type: Optional[CustomerType] = None
    status: Optional[CustomerStatus] = None
    industry: Optional[str] = None
    search: Optional[str] = None

class CustomerPagination(BaseModel):
    items: List[CustomerInDB]
    total: int
    page: int
    size: int
