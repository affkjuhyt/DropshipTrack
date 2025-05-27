from uuid import uuid4
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.base import Base
from db.fields import MoneyField, TaxedMoneyField, SanitizedJSON
from core.config import settings

class Order(Base):
    __tablename__ = 'order'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    number = Column(Integer, unique=True)
    use_old_id = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=func.now(), index=True)
    expired_at = Column(DateTime, nullable=True)

    status = Column(String(32), default='UNFULFILLED')
    authorize_status = Column(String(32), default='NONE', index=True)
    charge_status = Column(String(32), default='NONE', index=True)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=True)
    user = relationship('User', back_populates='orders')
    
    language_code = Column(String(35), default=settings.LANGUAGE_CODE)
    tracking_client_id = Column(String(36))
    
    billing_address_id = Column(UUID(as_uuid=True), ForeignKey('address.id'), nullable=True)
    billing_address = relationship('Address', foreign_keys=[billing_address_id])
    
    shipping_address_id = Column(UUID(as_uuid=True), ForeignKey('address.id'), nullable=True)
    shipping_address = relationship('Address', foreign_keys=[shipping_address_id])
    
    draft_save_billing_address = Column(Boolean, nullable=True)
    draft_save_shipping_address = Column(Boolean, nullable=True)
    user_email = Column(String(255), default='')
    
    original_id = Column(UUID(as_uuid=True), ForeignKey('order.id'), nullable=True)
    original = relationship('Order', remote_side=[id])
    
    origin = Column(String(32))
    currency = Column(String(settings.DEFAULT_CURRENCY_CODE_LENGTH))
    
    shipping_method_id = Column(UUID(as_uuid=True), ForeignKey('shipping_method.id'), nullable=True)
    shipping_method = relationship('ShippingMethod', back_populates='orders')
    
    collection_point_id = Column(UUID(as_uuid=True), ForeignKey('warehouse.id'), nullable=True)
    collection_point = relationship('Warehouse', back_populates='orders')
    
    shipping_method_name = Column(String(255), nullable=True)
    collection_point_name = Column(String(255), nullable=True)
    
    channel_id = Column(UUID(as_uuid=True), ForeignKey('channel.id'))
    channel = relationship('Channel', back_populates='orders')
    
    shipping_price_net_amount = Column(Numeric(settings.DEFAULT_MAX_DIGITS, settings.DEFAULT_DECIMAL_PLACES), default=Decimal('0.0'))
    shipping_price_net = MoneyField(amount_field='shipping_price_net_amount', currency_field='currency')
    
    shipping_price_gross_amount = Column(Numeric(settings.DEFAULT_MAX_DIGITS, settings.DEFAULT_DECIMAL_PLACES), default=Decimal('0.0'))
    shipping_price_gross = MoneyField(amount_field='shipping_price_gross_amount', currency_field='currency')
    
    shipping_price = TaxedMoneyField(
        net_amount_field='shipping_price_net_amount',
        gross_amount_field='shipping_price_gross_amount',
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
    shipping_tax_class_id = Column(UUID(as_uuid=True), ForeignKey('tax_class.id'), nullable=True)
    shipping_tax_class = relationship('TaxClass')
    shipping_tax_class_name = Column(String(255), nullable=True)
    shipping_tax_class_private_metadata = Column(JSONB, default={})
    shipping_tax_class_metadata = Column(JSONB, default={})
    
    checkout_token = Column(String(36))
    
    total_net_amount = Column(Numeric(settings.DEFAULT_MAX_DIGITS, settings.DEFAULT_DECIMAL_PLACES), default=Decimal('0.0'))
    
    metadata_ = Column('metadata', SanitizedJSON)
    private_metadata = Column(SanitizedJSON)