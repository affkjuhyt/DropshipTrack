from sqlalchemy import ARRAY, Boolean, Column, String
from sqlalchemy.orm import relationship

from models.base import BaseModel

class Address(BaseModel):
    __tablename__ = 'addresses'

    first_name = Column(String(256))
    last_name = Column(String(256))
    company_name = Column(String(256))
    street_address_1 = Column(String(256))
    street_address_2 = Column(String(256))
    city = Column(String(256))
    city_area = Column(String(128))
    postal_code = Column(String(20))
    country = Column(String)
    country_area = Column(String(128))
    phone = Column(ARRAY(String))
    validation_skipped = Column(Boolean, default=False)
    
    # Relationships
    users = relationship("User", secondary="user_addresses", back_populates="addresses")
    warehouses = relationship('Warehouse', back_populates='address')
    billing_customers = relationship('Customer', foreign_keys='Customer.billing_address_id', back_populates='billing_address')
    shipping_customers = relationship('Customer', foreign_keys='Customer.shipping_address_id', back_populates='shipping_address')
