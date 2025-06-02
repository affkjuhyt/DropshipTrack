from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Account(BaseModel):
    __tablename__ = 'accounts'
    name = Column(String(255), nullable=False)
    code = Column(String(64), unique=True)
    type = Column(String(32))  # asset, liability, equity, income, expense
    parent_id = Column(Integer, ForeignKey('accounts.id'))
    is_group = Column(Boolean, default=False)
    currency = Column(String(3))
    balance = Column(Numeric(precision=18, scale=6))
    
    children = relationship('Account', back_populates='parent')
    parent = relationship('Account', remote_side=[id], back_populates='children')
    journal_items = relationship('JournalItem', back_populates='account')

class JournalEntry(BaseModel):
    __tablename__ = 'journal_entries'
    date = Column(DateTime, nullable=False)
    reference = Column(String(64))
    status = Column(String(32))  # draft, posted
    total_debit = Column(Numeric(precision=18, scale=6))
    total_credit = Column(Numeric(precision=18, scale=6))
    
    items = relationship('JournalItem', back_populates='entry')

class JournalItem(BaseModel):
    __tablename__ = 'journal_items'
    entry_id = Column(Integer, ForeignKey('journal_entries.id'))
    account_id = Column(Integer, ForeignKey('accounts.id'))
    debit = Column(Numeric(precision=18, scale=6))
    credit = Column(Numeric(precision=18, scale=6))
    description = Column(Text)
    
    entry = relationship('JournalEntry', back_populates='items')
    account = relationship('Account', back_populates='journal_items')
