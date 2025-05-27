from decimal import Decimal
from typing import TYPE_CHECKING, Optional, List

from sqlalchemy import Column, String, Boolean, Text, ForeignKey, Integer, Numeric, or_, and_
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.hybrid import hybrid_property

from .base import Base
from .channel import Channel
from .products import Product
from db.fields import MoneyField, SanitizedJSONField

if TYPE_CHECKING:
    from .address import Address
    from .order import Order


class ShippingZone(Base):
    __tablename__ = 'shipping_zones'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    countries = Column(SanitizedJSONField, default=list)
    default = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    
    # Relationships
    channels = relationship('Channel', secondary='shipping_zone_channels', back_populates='shipping_zones')
    shipping_methods = relationship('ShippingMethod', back_populates='shipping_zone')

    def __repr__(self):
        return f"<ShippingZone {self.name}>"


class ShippingMethod(Base):
    __tablename__ = 'shipping_methods'

    id = Column(Integer, primary_key=True)
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


class ShippingMethodChannelListing(Base):
    __tablename__ = 'shipping_method_channel_listings'

    id = Column(Integer, primary_key=True)
    shipping_method_id = Column(Integer, ForeignKey('shipping_methods.id'), nullable=False)
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=False)
    price_amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    minimum_order_price_amount = Column(Numeric(12, 2), nullable=True)
    maximum_order_price_amount = Column(Numeric(12, 2), nullable=True)
    
    # Relationships
    shipping_method = relationship('ShippingMethod', back_populates='channel_listings')
    channel = relationship('Channel')


# Association tables
shipping_zone_channels = Base.metadata.tables[
    'shipping_zone_channels'
] = Table(
    'shipping_zone_channels',
    Base.metadata,
    Column('shipping_zone_id', Integer, ForeignKey('shipping_zones.id'), primary_key=True),
    Column('channel_id', Integer, ForeignKey('channels.id'), primary_key=True)
)

shipping_method_excluded_products = Base.metadata.tables[
    'shipping_method_excluded_products'
] = Table(
    'shipping_method_excluded_products',
    Base.metadata,
    Column('shipping_method_id', Integer, ForeignKey('shipping_methods.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)