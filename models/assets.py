from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from models.base import BaseModel


class Asset(BaseModel):
    __tablename__ = 'assets'
    name = Column(String(255))
    asset_number = Column(String(64), unique=True)
    category = Column(String(64))
    purchase_date = Column(DateTime)
    purchase_value = Column(Numeric(precision=18, scale=6))
    current_value = Column(Numeric(precision=18, scale=6))
    location = Column(String(255))
    status = Column(String(32))  # active, disposed, maintenance
    
    maintenances = relationship('AssetMaintenance', back_populates='asset')

class AssetMaintenance(BaseModel):
    __tablename__ = 'asset_maintenances'
    asset_id = Column(Integer, ForeignKey('assets.id'))
    maintenance_date = Column(DateTime)
    cost = Column(Numeric(precision=18, scale=6))
    description = Column(Text)
    performed_by = Column(Integer, ForeignKey('users.id'))
    performed_by_user = relationship('User', foreign_keys=[performed_by])
    
    asset = relationship('Asset', back_populates='maintenances')
