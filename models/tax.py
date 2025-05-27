from decimal import Decimal
from typing import Optional

from sqlalchemy import Column, String, Boolean, ForeignKey, Numeric, Integer, UniqueConstraint
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import expression

from .base import Base
from .channel import Channel


class TaxClass(Base):
    __tablename__ = 'tax_classes'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    
    # Relationships
    country_rates = relationship('TaxClassCountryRate', back_populates='tax_class')

    def __repr__(self):
        return f"<TaxClass {self.name}>"


class TaxClassCountryRate(Base):
    __tablename__ = 'tax_class_country_rates'

    id = Column(Integer, primary_key=True)
    tax_class_id = Column(Integer, ForeignKey('tax_classes.id'), nullable=True)
    country = Column(String(2), nullable=False)  # ISO country code
    rate = Column(Numeric(12, 4), nullable=False)
    
    # Relationships
    tax_class = relationship('TaxClass', back_populates='country_rates')

    __table_args__ = (
        UniqueConstraint('country', 'tax_class_id', name='unique_country_tax_class'),
        UniqueConstraint(
            'country', 
            name='unique_country_without_tax_class',
            sqlite_where=(tax_class_id == None),
            postgresql_where=(tax_class_id == None),
            mssql_where=(tax_class_id == None)
        ),
    )

    def __repr__(self):
        return f"<TaxClassCountryRate {self.country}: {self.rate}>"


class TaxConfiguration(Base):
    __tablename__ = 'tax_configurations'

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=False, unique=True)
    charge_taxes = Column(Boolean, default=True)
    tax_calculation_strategy = Column(String(20), nullable=True)
    display_gross_prices = Column(Boolean, default=True)
    prices_entered_with_tax = Column(Boolean, default=True)
    tax_app_id = Column(String(256), nullable=True)
    
    # Relationships
    channel = relationship('Channel', back_populates='tax_configuration')
    country_exceptions = relationship('TaxConfigurationPerCountry', back_populates='tax_configuration')


class TaxConfigurationPerCountry(Base):
    __tablename__ = 'tax_configuration_per_countries'

    id = Column(Integer, primary_key=True)
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