from sqlalchemy import Column, ForeignKey, Index, Integer
from sqlalchemy.orm import relationship

from models.base import BaseModel

from .products import Product, ProductType


class AssignedProductAttributeValue(BaseModel):
    __tablename__ = 'assigned_product_attribute_values'
    
    sort_order = Column(Integer)
    value_id = Column(Integer, ForeignKey('attribute_values.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    
    value = relationship("AttributeValue", back_populates="productvalueassignment")
    product = relationship("Product", back_populates="attributevalues")
    
    __table_args__ = (
        Index('assignedprodattrval_product_idx', 'product_id'),
        {'sqlite_autoincrement': True}
    )
    
    def get_ordering_queryset(self):
        return self.product.attributevalues


class AttributeProduct(BaseModel):
    __tablename__ = 'attribute_products'
    
    sort_order = Column(Integer)
    attribute_id = Column(Integer, ForeignKey('attributes.id'), nullable=False)
    product_type_id = Column(Integer, ForeignKey('product_types.id'), nullable=False)
    
    attribute = relationship("Attribute", back_populates="attributeproduct")
    product_type = relationship("ProductType", back_populates="attributeproduct")
    
    __table_args__ = (
        {'sqlite_autoincrement': True}
    )
    
    def get_ordering_queryset(self):
        return self.product_type.attributeproduct