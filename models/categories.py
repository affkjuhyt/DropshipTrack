from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from models.base import BaseModel

class Category(BaseModel):
    __tablename__ = 'categories'

    name = Column(String(250), unique=True)
    slug = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    tax_class_id = Column(Integer, ForeignKey('tax_classes.id'), nullable=True)
    
    parent = relationship('Category',
                         primaryjoin='Category.parent_id == Category.id',
                         remote_side='Category.id',
                         back_populates='children')
    products = relationship('Product', back_populates='category')
    tax_class = relationship('TaxClass', back_populates='categories')
    children = relationship('Category', back_populates='parent')