from sqlalchemy import Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from models.base import BaseModel


class ContentType(BaseModel):
    __tablename__ = 'content_types'
    
    app_label = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    
    # Relationships
    permissions = relationship('Permission', back_populates='content_type')
    
    def __repr__(self):
        return f"<ContentType {self.app_label}.{self.model}>"


class Permission(BaseModel):
    __tablename__ = 'permissions'

    name = Column(String(255), nullable=False)
    codename = Column(String(100), nullable=False)
    content_type_id = Column(Integer, ForeignKey('content_types.id'), nullable=False)
    
    # Relationships
    content_type = relationship('ContentType', back_populates='permissions')
    groups = relationship('Group', secondary='group_permissions', back_populates='permissions')  # Add this line
    users = relationship('User', secondary='user_user_permissions', back_populates='user_permissions')  # Add this line

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
        if self.is_superuser:
            return True
        # Implementation would depend on your auth backend
        return perm in self.get_all_permissions(obj)
    
    def has_perms(self, perm_list, obj=None):
        """Return True if the user has all of the specified permissions."""
        return all(self.has_perm(perm, obj) for perm in perm_list)
