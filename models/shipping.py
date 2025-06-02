from sqlalchemy import Column, String, Boolean, Text, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from models.base import BaseModel


class ShippingZone(BaseModel):
    __tablename__ = 'shipping_zones'

    name = Column(String(100), nullable=False)
    default = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    
    # Relationships
    channels = relationship('Channel', secondary='shipping_zone_channels', back_populates='shipping_zones')
    shipping_methods = relationship('ShippingMethod', back_populates='shipping_zone')

    def __repr__(self):
        return f"<ShippingZone {self.name}>"


class ShippingMethod(BaseModel):
    __tablename__ = 'shipping_methods'

    name = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)  # 'price_based' or 'weight_based'
    shipping_zone_id = Column(Integer, ForeignKey('shipping_zones.id'), nullable=False)
    minimum_order_weight = Column(Numeric(12, 3), nullable=True)
    maximum_order_weight = Column(Numeric(12, 3), nullable=True)
    minimum_order_price_amount = Column(Numeric(12, 2), nullable=True)
    maximum_order_price_amount = Column(Numeric(12, 2), nullable=True)
    
    # Relationships
    shipping_zone = relationship('ShippingZone', back_populates='shipping_methods')
    channel_listings = relationship('ShippingMethodChannelListing', back_populates='shipping_method')
    excluded_products = relationship('Product', secondary='shipping_method_excluded_products')

    @hybrid_property
    def is_price_based(self):
        return self.type == 'price_based'

    @hybrid_property
    def is_weight_based(self):
        return self.type == 'weight_based'


class ShippingMethodChannelListing(BaseModel):
    __tablename__ = 'shipping_method_channel_listings'

    shipping_method_id = Column(Integer, ForeignKey('shipping_methods.id'), nullable=False)
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=False)
    price_amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    minimum_order_price_amount = Column(Numeric(12, 2), nullable=True)
    maximum_order_price_amount = Column(Numeric(12, 2), nullable=True)
    
    # Relationships
    shipping_method = relationship('ShippingMethod', back_populates='channel_listings')
    channel = relationship('Channel')
