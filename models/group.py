from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

from models.base import BaseModel
from models.permission import Permission  # Add this import

# Define the group_permissions association table
group_permissions = Table('group_permissions', BaseModel.metadata,
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

# Define the group_channels association table
group_channels = Table('group_channels', BaseModel.metadata,
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True),
    Column('channel_id', Integer, ForeignKey('channel.id'), primary_key=True)
)

class Group(BaseModel):
    __tablename__ = 'groups'

    name = Column(String(150), unique=True, nullable=False)
    restricted_access_to_channels = Column(Boolean, default=False)
    
    # Relationships
    permissions = relationship('Permission', secondary=group_permissions, back_populates='groups')
    channels = relationship('Channel', secondary=group_channels, back_populates='groups')
    users = relationship('User', secondary='user_groups', back_populates='groups')

    def __repr__(self):
        return f"<Group {self.name}>"
