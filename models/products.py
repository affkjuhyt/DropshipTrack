from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Boolean, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .base import Base
import uuid
from datetime import datetime

class ProductVariant(Base):
    __tablename__ = 'product_variants'

    id = Column(Integer, primary_key=True)
    sku = Column(String(255), unique=True, nullable=True)
    name = Column(String(255), nullable=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    track_inventory = Column(Boolean, default=True)
    is_preorder = Column(Boolean, default=False)
    preorder_end_date = Column(DateTime, nullable=True)
    preorder_global_threshold = Column(Integer, nullable=True)
    quantity_limit_per_customer = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default='now()')
    updated_at = Column(DateTime, server_default='now()', onupdate='now()')
    private_metadata = Column(JSONB)
    metadata = Column(JSONB)
    
    product = relationship('Product', back_populates='variants')
    media = relationship('ProductMedia', secondary='variant_media', back_populates='variants')


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    slug = Column(String(255), unique=True)
    description = Column(JSONB)
    description_plaintext = Column(Text)
    search_document = Column(Text, default="")
    search_index_dirty = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    rating = Column(Float)
    
    # Relationships
    product_type_id = Column(Integer, ForeignKey('product_types.id'))
    product_type = relationship("ProductType", back_populates="products")
    
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="products")
    
    default_variant_id = Column(Integer, ForeignKey('product_variants.id'))
    default_variant = relationship("ProductVariant", foreign_keys=[default_variant_id])
    
    tax_class_id = Column(Integer, ForeignKey('tax_classes.id'))
    tax_class = relationship("TaxClass", back_populates="products")
    
    # Metadata fields
    private_metadata = Column(JSONB, default=dict)
    metadata = Column(JSONB, default=dict)


class ProductType:
    __tablename__ = 'product_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    slug = Column(String(255), unique=True)
    kind = Column(String(32))
    has_variants = Column(Boolean, default=True)
    is_shipping_required = Column(Boolean, default=True)
    is_digital = Column(Boolean, default=False)
    
    # Relationships
    tax_class_id = Column(Integer, ForeignKey('tax_classes.id'))
    tax_class = relationship("TaxClass", back_populates="product_types")
    
    # Metadata fields
    private_metadata = Column(JSONB, default=dict)
    metadata = Column(JSONB, default=dict)
    