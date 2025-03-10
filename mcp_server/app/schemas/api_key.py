"""
Pydantic schemas for API key management.
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, Optional
from datetime import datetime

class APIKeyBase(BaseModel):
    """Base API key schema."""
    service_name: str = Field(..., description="Name of the service (e.g., 'tmdb', 'weather')")
    key_metadata: Dict = Field(
        ...,
        description="Metadata for the API key, including the key itself and any additional fields"
    )
    rate_limit: Optional[int] = Field(
        None,
        description="Rate limit per minute for this API key"
    )

class APIKeyCreate(APIKeyBase):
    """Schema for creating a new API key."""
    pass

class APIKeyUpdate(BaseModel):
    """Schema for updating an API key."""
    key_metadata: Optional[Dict] = Field(
        None,
        description="Updated metadata for the API key"
    )
    is_active: Optional[bool] = Field(
        None,
        description="Whether the API key is active"
    )
    rate_limit: Optional[int] = Field(
        None,
        description="Updated rate limit per minute"
    )

class APIKeyResponse(APIKeyBase):
    """Schema for API key responses."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime]
    last_used_at: Optional[datetime]
    usage_count: int
    owner_id: int

    class Config:
        from_attributes = True

class APIKeyUsageResponse(BaseModel):
    """Schema for API key usage logs."""
    id: int
    api_key_id: int
    timestamp: datetime
    endpoint: str
    response_status: int
    response_time: float
    ip_address: str
    user_agent: Optional[str]
    error_message: Optional[str]

    class Config:
        from_attributes = True 