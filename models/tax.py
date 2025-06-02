from sqlalchemy import Column, String, Boolean, ForeignKey, Numeric, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from models.base import BaseModel


class TaxClass(BaseModel):
    __tablename__ = 'tax_classes'

    name = Column(String(255), nullable=False)
    products = relationship('Product', back_populates='tax_class')
    
    # Relationships
    country_rates = relationship('TaxClassCountryRate', back_populates='tax_class')

    def __repr__(self):
        return f"<TaxClass {self.name}>"


class TaxClassCountryRate(BaseModel):
    __tablename__ = 'tax_class_country_rates'

    tax_class_id = Column(Integer, ForeignKey('tax_classes.id'), nullable=True)
    country = Column(String(2), nullable=False)  # ISO country code
    rate = Column(Numeric(12, 4), nullable=False)
    
    # Relationships
    tax_class = relationship('TaxClass', back_populates='country_rates')

    __table_args__ = (
        UniqueConstraint('country', 'tax_class_id', name='unique_country_tax_class'),
    )

    def __repr__(self):
        return f"<TaxClassCountryRate {self.country}: {self.rate}>"


class TaxConfiguration(BaseModel):
    __tablename__ = 'tax_configurations'

    channel_id = Column(Integer, ForeignKey('channel.id'), nullable=False, unique=True)
    charge_taxes = Column(Boolean, default=True)
    tax_calculation_strategy = Column(String(20), nullable=True)
    display_gross_prices = Column(Boolean, default=True)
    prices_entered_with_tax = Column(Boolean, default=True)
    tax_app_id = Column(String(256), nullable=True)
    
    # Relationships
    channel = relationship('Channel', back_populates='tax_configuration')
    country_exceptions = relationship('TaxConfigurationPerCountry', back_populates='tax_configuration')


class TaxConfigurationPerCountry(BaseModel):
    __tablename__ = 'tax_configuration_per_countries'

    tax_configuration_id = Column(Integer, ForeignKey('tax_configurations.id'), nullable=False)
    country = Column(String(2), nullable=False)  # ISO country code
    charge_taxes = Column(Boolean, default=True)
    tax_calculation_strategy = Column(String(20), nullable=True)
    display_gross_prices = Column(Boolean, default=True)
    tax_app_id = Column(String(256), nullable=True)
    
    # Relationships
    tax_configuration = relationship('TaxConfiguration', back_populates='country_exceptions')

    __table_args__ = (
        UniqueConstraint('tax_configuration_id', 'country', name='unique_tax_config_country'),
    )

    def __repr__(self):
        return f"<TaxConfigurationPerCountry {self.country}>"