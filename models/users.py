from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, UUID, Table
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from models.base import BaseModel
from models.group import Group  # Add this import

# Define the user_addresses association table
user_addresses = Table('user_addresses', BaseModel.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('address_id', Integer, ForeignKey('addresses.id'), primary_key=True)
)

# Define the user_groups association table
user_groups = Table('user_groups', BaseModel.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True)
)

# Define the user_user_permissions association table
user_user_permissions = Table('user_user_permissions', BaseModel.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

class User(BaseModel):
    __tablename__ = 'users'

    email = Column(String, unique=True, nullable=False)
    first_name = Column(String(256))
    last_name = Column(String(256))
    hashed_password = Column(String, nullable=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_confirmed = Column(Boolean, default=True)
    last_confirm_email_request = Column(DateTime)
    note = Column(Text)
    date_joined = Column(DateTime, default=datetime.utcnow)
    last_password_reset_request = Column(DateTime)
    jwt_token_key = Column(String(12), default=lambda: str(uuid.uuid4())[:12])
    language_code = Column(String(35))
    search_document = Column(Text, default="")
    
    # Foreign keys to addresses table (using Integer to match the addresses table)
    default_shipping_address_id = Column(Integer, ForeignKey('addresses.id', use_alter=True, name='fk_user_shipping_address'))
    default_billing_address_id = Column(Integer, ForeignKey('addresses.id', use_alter=True, name='fk_user_billing_address'))
    
    # This UUID field is fine as it's not a foreign key
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    
    # Relationships
    addresses = relationship("Address", secondary=user_addresses, back_populates="users")
    default_shipping_address = relationship("Address", foreign_keys=[default_shipping_address_id])
    default_billing_address = relationship("Address", foreign_keys=[default_billing_address_id])
    
    # Permission related fields
    is_superuser = Column(Boolean, default=False)
    groups = relationship("Group", secondary=user_groups, back_populates="users")
    user_permissions = relationship("Permission", secondary=user_user_permissions, back_populates="users")
    
    # Orders relationship - specify the foreign key explicitly
    orders = relationship('Order', back_populates='user', foreign_keys='Order.user_id')
