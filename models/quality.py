from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from models.base import BaseModel


class QualityCheck(BaseModel):
    __tablename__ = 'quality_checks'
    product_id = Column(Integer, ForeignKey('products.id'))
    inspection_date = Column(DateTime)
    inspector_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String(32))  # passed, failed, pending
    notes = Column(Text)
    
    product = relationship('Product', back_populates='quality_checks')
    inspector = relationship('User', foreign_keys=[inspector_id])

class QualityParameter(BaseModel):
    __tablename__ = 'quality_parameters'
    name = Column(String(255))
    product_type_id = Column(Integer, ForeignKey('product_types.id'))
    min_value = Column(Numeric)
    max_value = Column(Numeric)
    unit = Column(String(32))
    
    product_type = relationship('ProductType', back_populates='quality_parameters')
