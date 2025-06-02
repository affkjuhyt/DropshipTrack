from sqlalchemy import Column, ForeignKey, Integer, String, Text
from models.base import BaseModel


class Ticket(BaseModel):
    __tablename__ = 'tickets'
    title = Column(String(255))
    description = Column(Text)
    customer_id = Column(Integer, ForeignKey('users.id'))
    assigned_to = Column(Integer, ForeignKey('users.id'))
    status = Column(String(32))  # open, in_progress, resolved, closed
    priority = Column(String(32))  # low, medium, high, urgent
    category = Column(String(64))

class TicketComment(BaseModel):
    __tablename__ = 'ticket_comments'
    ticket_id = Column(Integer, ForeignKey('tickets.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(Text)
