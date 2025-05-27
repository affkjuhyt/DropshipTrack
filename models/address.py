from sqlalchemy import ARRAY, Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB


class Address:
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
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
    
    # Metadata fields
    private_metadata = Column(JSONB, default=dict)
    metadata = Column(JSONB, default=dict)
    
    # Relationships
    users = relationship("User", secondary="user_addresses", back_populates="addresses")
