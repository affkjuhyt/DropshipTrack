from sqlalchemy import Column, ForeignKey, Index, Integer, String, Boolean
from sqlalchemy.orm import relationship

from models.base import BaseModel


class Attribute(BaseModel):
    __tablename__ = 'attributes'
    
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    input_type = Column(String(50), nullable=False)
    is_variant_only = Column(Boolean, default=False)
    
    # Relationships
    values = relationship("AttributeValue", back_populates="attribute")
    attributeproduct = relationship("AttributeProduct", back_populates="attribute")


class AttributeValue(BaseModel):
    __tablename__ = 'attribute_values'
    
    name = Column(String(255), nullable=False)
    attribute_id = Column(Integer, ForeignKey('attributes.id'), nullable=False)
    
    # Relationships
    attribute = relationship("Attribute", back_populates="values")
    productvalueassignment = relationship("AssignedProductAttributeValue", back_populates="value")


class AssignedProductAttributeValue(BaseModel):
    __tablename__ = 'assigned_product_attribute_values'
    
    sort_order = Column(Integer)
    value_id = Column(Integer, ForeignKey('attribute_values.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    
    value = relationship("AttributeValue", back_populates="productvalueassignment")
    product = relationship("Product", back_populates="attributevalues")
    
    __table_args__ = (
        Index('assignedprodattrval_product_idx', 'product_id'),
    )


class AttributeProduct(BaseModel):
    __tablename__ = 'attribute_products'
    
    sort_order = Column(Integer)
    attribute_id = Column(Integer, ForeignKey('attributes.id'), nullable=False)
    product_type_id = Column(Integer, ForeignKey('product_types.id'), nullable=False)
    
    attribute = relationship("Attribute", back_populates="attributeproduct")
    product_type = relationship("ProductType", back_populates="attributeproduct")
