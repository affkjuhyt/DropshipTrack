from sqlalchemy import Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from .base import Base


class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    codename = Column(String(100), nullable=False)
    content_type_id = Column(Integer, ForeignKey('content_types.id'), nullable=False)
    
    # Relationships
    content_type = relationship('ContentType', back_populates='permissions')

    def __repr__(self):
        return f"<Permission {self.content_type} | {self.name}>"


class PermissionsMixin:
    """
    Add the fields and methods necessary to support permissions.
    To be used as a mixin in User model.
    """
    
    @declared_attr
    def is_superuser(cls):
        return Column(Boolean, default=False)
    
    @declared_attr
    def groups(cls):
        return relationship('Group', secondary='user_groups', back_populates='users')
    
    @declared_attr
    def user_permissions(cls):
        return relationship('Permission', secondary='user_user_permissions', back_populates='users')
    
    def get_user_permissions(self, obj=None):
        """Return a list of permission strings that this user has directly."""
        # Implementation would depend on your auth backend
        pass
    
    def get_group_permissions(self, obj=None):
        """Return a list of permission strings that this user has through their groups."""
        # Implementation would depend on your auth backend
        pass
    
    def get_all_permissions(self, obj=None):
        """Return all permissions available to this user."""
        permissions = set()
        permissions.update(self.get_user_permissions(obj))
        permissions.update(self.get_group_permissions(obj))
        return permissions
    
    def has_perm(self, perm, obj=None):
        """Return True if the user has the specified permission."""
        if self.is_active and self.is_superuser:
            return True
        # Implementation would depend on your auth backend
        return perm in self.get_all_permissions(obj)
    
    def has_perms(self, perm_list, obj=None):
        """Return True if the user has all of the specified permissions."""
        return all(self.has_perm(perm, obj) for perm in perm_list)


# Association tables
user_groups = Base.metadata.tables[
    'user_groups'
] = Table(
    'user_groups',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True)
)

user_user_permissions = Base.metadata.tables[
    'user_user_permissions'
] = Table(
    'user_user_permissions',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)