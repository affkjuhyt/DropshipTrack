from sqlalchemy import Column, Integer, ForeignKey, Table
from models.base import BaseModel

group_channels = Table('group_channels', BaseModel.metadata,
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True),
    Column('channel_id', Integer, ForeignKey('channel.id'), primary_key=True)
)

group_permissions = Table('group_permissions', BaseModel.metadata,
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

shipping_zone_channels = Table('shipping_zone_channels', BaseModel.metadata,
    Column('shipping_zone_id', Integer, ForeignKey('shipping_zones.id'), primary_key=True),
    Column('channel_id', Integer, ForeignKey('channel.id'), primary_key=True)
)

shipping_method_excluded_products = Table('shipping_method_excluded_products', BaseModel.metadata,
    Column('shipping_method_id', Integer, ForeignKey('shipping_methods.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)

variant_media = Table('variant_media', BaseModel.metadata,
    Column('variant_id', Integer, ForeignKey('product_variants.id'), primary_key=True),
    Column('media_id', Integer, ForeignKey('product_media.id'), primary_key=True)
)
