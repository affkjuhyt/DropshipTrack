from collections.abc import Callable
from functools import total_ordering
from typing import Dict

from sqlalchemy import TypeDecorator, types
from core.money import Money, TaxedMoney


class SanitizedJSON(TypeDecorator):
    """SQLAlchemy type for storing sanitized JSON data."""
    impl = types.JSON
    
    def __init__(self, sanitizer: Callable[[Dict], Dict], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sanitizer = sanitizer
    
    def process_bind_param(self, value: Dict, dialect) -> str:
        """Sanitize the value before saving to database."""
        if value is None:
            return None
        return self._sanitizer(value)


@total_ordering
class NonDatabaseFieldBase:
    """Base class for all fields that are not stored in the database."""
    
    def __init__(self):
        self.name = None
        self.creation_counter = 0
    
    def __eq__(self, other):
        if isinstance(other, NonDatabaseFieldBase):
            return self.creation_counter == other.creation_counter
        return NotImplemented
    
    def __lt__(self, other):
        if isinstance(other, NonDatabaseFieldBase):
            return self.creation_counter < other.creation_counter
        return NotImplemented
    
    def __hash__(self):
        return hash(self.creation_counter)
    
    def contribute_to_class(self, cls, name):
        self.name = name
        setattr(cls, name, self)


class MoneyField(NonDatabaseFieldBase):
    """Field that combines amount and currency fields into Money object."""
    
    def __init__(self, amount_field: str, currency_field: str):
        super().__init__()
        self.amount_field = amount_field
        self.currency_field = currency_field
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        amount = getattr(instance, self.amount_field)
        currency = getattr(instance, self.currency_field)
        if amount is not None and currency is not None:
            return Money(amount, currency)
        return None
    
    def __set__(self, instance, value):
        if value is None:
            amount = currency = None
        else:
            amount = value.amount
            currency = value.currency
        setattr(instance, self.amount_field, amount)
        setattr(instance, self.currency_field, currency)


class TaxedMoneyField(NonDatabaseFieldBase):
    """Field that combines net, gross and currency fields into TaxedMoney object."""
    
    def __init__(self, net_field: str, gross_field: str, currency_field: str):
        super().__init__()
        self.net_field = net_field
        self.gross_field = gross_field
        self.currency_field = currency_field
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        net = getattr(instance, self.net_field)
        gross = getattr(instance, self.gross_field)
        currency = getattr(instance, self.currency_field)
        if net is None or gross is None:
            return None
        return TaxedMoney(Money(net, currency), Money(gross, currency))
    
    def __set__(self, instance, value):
        if value is None:
            net = gross = currency = None
        else:
            net = value.net.amount
            gross = value.gross.amount
            currency = value.currency
        setattr(instance, self.net_field, net)
        setattr(instance, self.gross_field, gross)
        setattr(instance, self.currency_field, currency)