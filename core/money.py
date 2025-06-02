from decimal import Decimal
from typing import Union

class Money:
    """Represents a monetary amount with a specific currency."""
    
    def __init__(self, amount: Union[Decimal, float, str, int], currency: str):
        if isinstance(amount, float):
            # Convert float to Decimal for precise calculations
            amount = Decimal(str(amount))
        elif isinstance(amount, (str, int)):
            amount = Decimal(str(amount))
        
        self.amount = amount
        self.currency = currency.upper()
    
    def __add__(self, other):
        if not isinstance(other, Money):
            raise TypeError("Cannot add Money and non-Money")
        if self.currency != other.currency:
            raise ValueError("Cannot add Money with different currencies")
        return Money(self.amount + other.amount, self.currency)
    
    def __sub__(self, other):
        if not isinstance(other, Money):
            raise TypeError("Cannot subtract Money and non-Money")
        if self.currency != other.currency:
            raise ValueError("Cannot subtract Money with different currencies")
        return Money(self.amount - other.amount, self.currency)
    
    def __mul__(self, other):
        if isinstance(other, (int, Decimal, float)):
            return Money(self.amount * Decimal(str(other)), self.currency)
        raise TypeError("Cannot multiply Money with non-numeric type")
    
    def __truediv__(self, other):
        if isinstance(other, (int, Decimal, float)):
            return Money(self.amount / Decimal(str(other)), self.currency)
        raise TypeError("Cannot divide Money with non-numeric type")
    
    def __eq__(self, other):
        if not isinstance(other, Money):
            return False
        return self.amount == other.amount and self.currency == other.currency
    
    def __str__(self):
        return f"{self.amount} {self.currency}"
    
    def __repr__(self):
        return f"Money({repr(str(self.amount))}, {repr(self.currency)})"


class TaxedMoney:
    """Represents a monetary amount that includes both net and gross values."""
    
    def __init__(self, net: Money, gross: Money):
        if not isinstance(net, Money) or not isinstance(gross, Money):
            raise TypeError("Both net and gross must be Money instances")
        if net.currency != gross.currency:
            raise ValueError("Net and gross must have the same currency")
        
        self.net = net
        self.gross = gross
        self.currency = net.currency
    
    @property
    def tax(self) -> Money:
        """Calculate the tax amount (difference between gross and net)."""
        return Money(self.gross.amount - self.net.amount, self.currency)
    
    def __add__(self, other):
        if not isinstance(other, TaxedMoney):
            raise TypeError("Cannot add TaxedMoney and non-TaxedMoney")
        if self.currency != other.currency:
            raise ValueError("Cannot add TaxedMoney with different currencies")
        return TaxedMoney(
            net=self.net + other.net,
            gross=self.gross + other.gross
        )
    
    def __sub__(self, other):
        if not isinstance(other, TaxedMoney):
            raise TypeError("Cannot subtract TaxedMoney and non-TaxedMoney")
        if self.currency != other.currency:
            raise ValueError("Cannot subtract TaxedMoney with different currencies")
        return TaxedMoney(
            net=self.net - other.net,
            gross=self.gross - other.gross
        )
    
    def __eq__(self, other):
        if not isinstance(other, TaxedMoney):
            return False
        return self.net == other.net and self.gross == other.gross
    
    def __str__(self):
        return f"TaxedMoney(net={self.net}, gross={self.gross})"
    
    def __repr__(self):
        return f"TaxedMoney(net={repr(self.net)}, gross={repr(self.gross)})"