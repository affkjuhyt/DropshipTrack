from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Supplier(BaseModel):
    __tablename__ = 'suppliers'
    name = Column(String(255))
    code = Column(String(64), unique=True)
    tax_number = Column(String(64))
    payment_terms = Column(Integer)  # days
    credit_limit = Column(Numeric(precision=18, scale=6))
    
    purchase_orders = relationship('PurchaseOrder', back_populates='supplier')

class PurchaseRequest(BaseModel):
    __tablename__ = 'purchase_requests'
    requester_id = Column(Integer, ForeignKey('users.id'))
    department = Column(String(64))
    required_date = Column(DateTime)
    status = Column(String(32))  # draft, approved, rejected
    
    requester = relationship('User', foreign_keys=[requester_id])

class PurchaseOrder(BaseModel):
    __tablename__ = 'purchase_orders'
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    expected_delivery = Column(DateTime)
    payment_terms = Column(Integer)
    status = Column(String(32))  # draft, sent, received, cancelled
    
    supplier = relationship('Supplier', back_populates='purchase_orders')
