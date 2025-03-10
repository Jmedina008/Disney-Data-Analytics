"""
Pydantic schemas for user management.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr = Field(..., description="User's email address")
    full_name: Optional[str] = Field(None, description="User's full name")
    is_active: Optional[bool] = Field(True, description="Whether the user account is active")

class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(
        ...,
        description="User's password",
        min_length=8,
        max_length=100
    )

class UserUpdate(BaseModel):
    """Schema for updating a user."""
    email: Optional[EmailStr] = Field(None, description="Updated email address")
    full_name: Optional[str] = Field(None, description="Updated full name")
    password: Optional[str] = Field(
        None,
        description="Updated password",
        min_length=8,
        max_length=100
    )
    is_active: Optional[bool] = Field(None, description="Updated active status")

class UserInDBBase(UserBase):
    """Base schema for user in database."""
    id: int
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True

class User(UserInDBBase):
    """Schema for user responses."""
    pass

class UserInDB(UserInDBBase):
    """Schema for user in database (includes hashed password)."""
    hashed_password: str 