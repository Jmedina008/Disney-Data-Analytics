"""
Database models for API key management.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class APIKey(Base):
    """API Key model."""
    
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, index=True, nullable=False)
    encrypted_key = Column(String, nullable=False)
    key_metadata = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    last_used_at = Column(DateTime, nullable=True)
    usage_count = Column(Integer, default=0)
    rate_limit = Column(Integer, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    owner = relationship("User", back_populates="api_keys")
    usage_logs = relationship("APIKeyUsage", back_populates="api_key")

class APIKeyUsage(Base):
    """API Key usage log model."""
    
    __tablename__ = "api_key_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    api_key_id = Column(Integer, ForeignKey("api_keys.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    endpoint = Column(String, nullable=False)
    response_status = Column(Integer, nullable=True)
    response_time = Column(Integer, nullable=True)  # in milliseconds
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    error_message = Column(String, nullable=True)
    
    # Relationships
    api_key = relationship("APIKey", back_populates="usage_logs") 