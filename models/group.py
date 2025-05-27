from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from .base import Base
from .permission import Permission
from .channel import Channel


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    restricted_access_to_channels = Column(Boolean, default=False)
    
    # Relationships
    permissions = relationship('Permission', secondary='group_permissions', back_populates='groups')
    channels = relationship('Channel', secondary='group_channels', back_populates='groups')
    users = relationship('User', secondary='user_groups', back_populates='groups')

    def __repr__(self):
        return f"<Group {self.name}>"


# Association tables
group_permissions = Base.metadata.tables[
    'group_permissions'
] = Table(
    'group_permissions',
    Base.metadata,
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

group_channels = Base.metadata.tables[
    'group_channels'
] = Table(
    'group_channels',
    Base.metadata,
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True),
    Column('channel_id', Integer, ForeignKey('channels.id'), primary_key=True)
)