from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

from models.base import BaseModel
from models.permission import Permission
from models.channel import Channel
from models.associations import group_channels, group_permissions

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
