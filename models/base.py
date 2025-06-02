from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(String, ForeignKey('users.id'), nullable=True)
    updated_by = Column(String, ForeignKey('users.id'), nullable=True)
    
    # Metadata fields
    private_metadata = Column(JSONB, default=dict)
    metadata = Column(JSONB, default=dict)
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"

class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class UserTrackMixin:
    created_by = Column(String, ForeignKey('users.id'), nullable=True)
    updated_by = Column(String, ForeignKey('users.id'), nullable=True)