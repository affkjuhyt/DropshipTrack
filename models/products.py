from sqlalchemy import Column, Index, String, Text, DateTime, ForeignKey, Integer, Boolean, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from models.base import BaseModel
from models.associations import variant_media
from models.categories import Category
from models.tax import TaxClass  # Add this import

class ProductVariant(BaseModel):
    __tablename__ = 'product_variants'

    sku = Column(String(255), unique=True, nullable=True)
    name = Column(String(255), nullable=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    track_inventory = Column(Boolean, default=True)
    is_preorder = Column(Boolean, default=False)
    preorder_end_date = Column(DateTime, nullable=True)
    preorder_global_threshold = Column(Integer, nullable=True)
    quantity_limit_per_customer = Column(Integer, nullable=True)
    
    # Update the relationship with explicit foreign keys
    product = relationship('Product', 
                          foreign_keys=[product_id],
                          back_populates='variants')
    media = relationship('ProductMedia', secondary='variant_media', back_populates='variants')


class Product(BaseModel):
    __tablename__ = 'products'

    name = Column(String(250), nullable=False)
    slug = Column(String(255), unique=True)
    description = Column(JSONB)
    description_plaintext = Column(Text)
    search_document = Column(Text, default="")
    search_index_dirty = Column(Boolean, default=False, index=True)
    rating = Column(Float)
    
    # Relationships
    product_type_id = Column(Integer, ForeignKey('product_types.id'))
    product_type = relationship("ProductType", back_populates="products")
    
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    category = relationship('Category', back_populates='products')
    
    # Add the variants relationship
    variants = relationship('ProductVariant',
                           foreign_keys='[ProductVariant.product_id]',
                           back_populates='product')
    
    default_variant_id = Column(Integer, ForeignKey('product_variants.id', use_alter=True, name='fk_product_default_variant'))
    default_variant = relationship('ProductVariant', foreign_keys=[default_variant_id])
    
    tax_class_id = Column(Integer, ForeignKey('tax_classes.id'), nullable=True)
    tax_class = relationship('TaxClass', back_populates='products')
    
    # Add the stock_movements relationship
    stock_movements = relationship('StockMovement', back_populates='product')
    
    __table_args__ = (
        Index('idx_product_slug', slug),
        Index('idx_product_name', name),
    )



class ProductType(BaseModel):
    __tablename__ = 'product_types'

    name = Column(String(250), nullable=False)
    slug = Column(String(255), unique=True)
    kind = Column(String(32))
    has_variants = Column(Boolean, default=True)
    is_shipping_required = Column(Boolean, default=True)
    is_digital = Column(Boolean, default=False)
    
    # Relationships
    tax_class_id = Column(Integer, ForeignKey('tax_classes.id'))
    tax_class = relationship("TaxClass", back_populates="product_types")
    # Add the products relationship
    products = relationship("Product", back_populates="product_type")


class ProductMedia(BaseModel):
    __tablename__ = 'product_media'

    alt = Column(String(255), nullable=True)
    type = Column(String(50), nullable=False)  # image, video, etc.
    external_url = Column(String(2048), nullable=True)
    oembed_data = Column(JSONB, nullable=True)
    
    # Relationships
    variants = relationship('ProductVariant', secondary='variant_media', back_populates='media')
