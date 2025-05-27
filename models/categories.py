from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from models.base import BaseModel

class Category(BaseModel):
    __tablename__ = 'categories'

    name = Column(String(250))
    slug = Column(String(255), unique=True)
    description = Column(JSONB)
    description_plaintext = Column(Text)
    parent_id = Column(Integer, ForeignKey('categories.id'))
    background_image = Column(String)
    background_image_alt = Column(String(128))
    seo_title = Column(String)
    seo_description = Column(String)
    
    parent = relationship('Category', remote_side=[id], back_populates='children')
    children = relationship('Category', back_populates='parent')