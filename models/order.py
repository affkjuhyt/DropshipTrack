from decimal import Decimal

from sqlalchemy import Column, Index, Integer, String, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from db.fields import MoneyField, TaxedMoneyField
from core.config import settings
from models.base import BaseModel

class Order(BaseModel):
    __tablename__ = 'order'

    number = Column(Integer, unique=True)
    use_old_id = Column(Boolean, default=False)
    expired_at = Column(DateTime, nullable=True)

    status = Column(String(32), default='UNFULFILLED')
    authorize_status = Column(String(32), default='NONE', index=True)
    charge_status = Column(String(32), default='NONE', index=True)
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    original_id = Column(Integer, ForeignKey('order.id'), nullable=True)
    user = relationship('User', back_populates='orders')
    original = relationship('Order', remote_side=[id])
    
    language_code = Column(String(35), default=settings.LANGUAGE_CODE)
    tracking_client_id = Column(String(36))
    
    billing_address_id = Column(Integer, ForeignKey('addresses.id'), nullable=True)
    shipping_address_id = Column(Integer, ForeignKey('addresses.id'), nullable=True)
    billing_address = relationship('Address', foreign_keys=[billing_address_id])
    shipping_address = relationship('Address', foreign_keys=[shipping_address_id])
    
    draft_save_billing_address = Column(Boolean, nullable=True)
    draft_save_shipping_address = Column(Boolean, nullable=True)
    user_email = Column(String(255), default='')
    
    origin = Column(String(32))
    currency = Column(String(settings.DEFAULT_CURRENCY_CODE_LENGTH))
    
    shipping_method_id = Column(Integer, ForeignKey('shipping_methods.id'), nullable=True)
    shipping_method = relationship('ShippingMethod', back_populates='orders')
    
    collection_point_id = Column(Integer, ForeignKey('warehouses.id'), nullable=True)
    collection_point = relationship('Warehouse', back_populates='orders')
    
    shipping_method_name = Column(String(255), nullable=True)
    collection_point_name = Column(String(255), nullable=True)
    
    channel_id = Column(Integer, ForeignKey('channel.id'))
    channel = relationship('Channel', back_populates='orders')
    
    shipping_price_net_amount = Column(Numeric(settings.DEFAULT_MAX_DIGITS, settings.DEFAULT_DECIMAL_PLACES), default=Decimal('0.0'))
    shipping_price_net = MoneyField(amount_field='shipping_price_net_amount', currency_field='currency')
    
    shipping_price_gross_amount = Column(Numeric(settings.DEFAULT_MAX_DIGITS, settings.DEFAULT_DECIMAL_PLACES), default=Decimal('0.0'))
    shipping_price_gross = MoneyField(amount_field='shipping_price_gross_amount', currency_field='currency')
    
    shipping_price = TaxedMoneyField(
        net_field='shipping_price_net_amount',
        gross_field='shipping_price_gross_amount',
        currency_field='currency'
    )
    
    base_shipping_price_amount = Column(Numeric(settings.DEFAULT_MAX_DIGITS, settings.DEFAULT_DECIMAL_PLACES), default=Decimal('0.0'))
    base_shipping_price = MoneyField(amount_field='base_shipping_price_amount', currency_field='currency')
    
    undiscounted_base_shipping_price_amount = Column(Numeric(settings.DEFAULT_MAX_DIGITS, settings.DEFAULT_DECIMAL_PLACES), default=Decimal('0.0'))
    undiscounted_base_shipping_price = MoneyField(
        amount_field='undiscounted_base_shipping_price_amount',
        currency_field='currency'
    )
    
    shipping_tax_rate = Column(Numeric(5, 4), nullable=True)
    shipping_tax_class_id = Column(Integer, ForeignKey('tax_classes.id'), nullable=True)
    shipping_tax_class = relationship('TaxClass')
    shipping_tax_class_name = Column(String(255), nullable=True)
    shipping_tax_class_private_metadata = Column(JSONB, default={})
    shipping_tax_class_metadata = Column(JSONB, default={})
    
    checkout_token = Column(String(36))
    
    total_net_amount = Column(Numeric(settings.DEFAULT_MAX_DIGITS, settings.DEFAULT_DECIMAL_PLACES), default=Decimal('0.0'))

    __table_args__ = (
        Index('idx_order_user_id', user_id),
        Index('idx_order_status', status),
    )
