from sqlalchemy import Column, Integer, String, Boolean, Interval
from sqlalchemy.orm import validates, relationship

from core.config import settings
from models.base import BaseModel
from models.associations import group_channels, shipping_zone_channels

class Channel(BaseModel):
    __tablename__ = 'channel'

    name = Column(String(250), nullable=False)
    is_active = Column(Boolean, default=False)
    slug = Column(String(255), unique=True)
    currency_code = Column(String(settings.DEFAULT_CURRENCY_CODE_LENGTH))
    default_country = Column(String(2))  # ISO country code
    allocation_strategy = Column(String(255), default='PRIORITIZE_SORTING_ORDER')
    order_mark_as_paid_strategy = Column(String(255), default='PAYMENT_FLOW')
    default_transaction_flow_strategy = Column(String(255), default='CHARGE')
    automatically_confirm_all_new_orders = Column(Boolean, default=True, nullable=True)
    allow_unpaid_orders = Column(Boolean, default=False)
    automatically_fulfill_non_shippable_gift_card = Column(Boolean, default=True, nullable=True)
    expire_orders_after = Column(Integer, nullable=True)
    delete_expired_orders_after = Column(Interval, default='60 days')
    include_draft_order_in_voucher_usage = Column(Boolean, default=False)
    use_legacy_error_flow_for_checkout = Column(Boolean, default=True)
    automatically_complete_fully_paid_checkouts = Column(Boolean, default=False)
    draft_order_line_price_freeze_period = Column(Integer, nullable=True)
    use_legacy_line_discount_propagation_for_order = Column(Boolean, default=True)
    
    # Add relationship with Group
    groups = relationship('Group', secondary=group_channels, back_populates='channels')
    # Add relationship with ShippingZone
    shipping_zones = relationship('ShippingZone', secondary=shipping_zone_channels, back_populates='channels')
    # Add relationship with TaxConfiguration
    tax_configuration = relationship('TaxConfiguration', back_populates='channel', uselist=False)
    # Add relationship with Order
    orders = relationship('Order', back_populates='channel')
    
    @validates('currency_code')
    def validate_currency(self, key, value):
        if not value or len(value) != 3:
            raise ValueError('Currency code must be 3 characters')
        return value.upper()

    @validates('default_country')
    def validate_country(self, key, value):
        if not value or len(value) != 2:
            raise ValueError('Country code must be 2 characters')
        return value.upper()
