from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .base import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    slug = Column(String(255), unique=True)
    description = Column(JSONB)
    description_plaintext = Column(Text)
    updated_at = Column(DateTime)
    parent_id = Column(Integer, ForeignKey('categories.id'))
    background_image = Column(String)
    background_image_alt = Column(String(128))
    private_metadata = Column(JSONB)
    metadata = Column(JSONB)
    seo_title = Column(String)
    seo_description = Column(String)
    
    parent = relationship('Category', remote_side=[id], back_populates='children')
    children = relationship('Category', back_populates='parent')