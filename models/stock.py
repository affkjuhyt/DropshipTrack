from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Warehouse(BaseModel):
    __tablename__ = 'warehouses'
    name = Column(String(255))
    code = Column(String(64), unique=True)
    address_id = Column(Integer, ForeignKey('addresses.id'))
    
    address = relationship('Address', back_populates='warehouses')
    stock_movements = relationship('StockMovement', back_populates='warehouse')
    orders = relationship('Order', back_populates='collection_point')

class StockMovement(BaseModel):
    __tablename__ = 'stock_movements'
    product_id = Column(Integer, ForeignKey('products.id'))
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'))
    quantity = Column(Numeric(precision=10, scale=2))
    type = Column(String(32))  # in, out, transfer
    reference = Column(String(64))
    unit_cost = Column(Numeric(precision=18, scale=6))
    
    product = relationship('Product', back_populates='stock_movements')
    warehouse = relationship('Warehouse', back_populates='stock_movements')

class InventoryAdjustment(BaseModel):
    __tablename__ = 'inventory_adjustments'
    date = Column(DateTime)
    reason = Column(String(255))
    status = Column(String(32))  # draft, confirmed
    
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'))
    adjusted_by = Column(Integer, ForeignKey('users.id'))
