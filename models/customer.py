from sqlalchemy import Column, String, Enum, Text, Numeric, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel
from schemas.customers import CustomerStatus, CustomerType

class Customer(BaseModel):
    __tablename__ = "customers"

    customer_name = Column(String(255), nullable=False)
    customer_type = Column(Enum(CustomerType), nullable=False)
    tax_id = Column(String(50), unique=True, nullable=True)
    phone_number = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    industry = Column(String(100), nullable=True)
    source = Column(String(100), nullable=True)
    credit_limit = Column(Numeric(precision=15, scale=2), nullable=True)
    payment_terms = Column(String(100), nullable=True)
    status = Column(Enum(CustomerStatus), nullable=False, default=CustomerStatus.LEAD)
    assigned_user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    # Address Foreign Keys
    billing_address_id = Column(Integer, ForeignKey('addresses.id'), nullable=True)
    shipping_address_id = Column(Integer, ForeignKey('addresses.id'), nullable=True)

    # Relationships
    contacts = relationship("Contact", back_populates="customer", lazy="dynamic")
    assigned_user = relationship("User", foreign_keys=[assigned_user_id])
    billing_address = relationship("Address", foreign_keys=[billing_address_id])
    shipping_address = relationship("Address", foreign_keys=[shipping_address_id])

    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.customer_name}')"
