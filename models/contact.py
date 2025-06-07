from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.base import BaseModel

class Contact(BaseModel):
    __tablename__ = "contacts"

    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    salutation = Column(String(20), nullable=True)
    title = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    work_phone_number = Column(String(20), nullable=True)
    preferred_communication_method = Column(String(50), nullable=True)
    linkedin_profile = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)

    # Relationships
    customer = relationship("Customer", back_populates="contacts")

    def __repr__(self):
        return f"<Contact(id={self.id}, name='{self.first_name} {self.last_name}')>"
    