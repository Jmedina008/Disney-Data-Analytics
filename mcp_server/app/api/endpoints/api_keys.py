"""
API endpoints for managing API keys.
"""

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.config import settings, API_SERVICES
from app.core.security import (
    encrypt_api_key,
    decrypt_api_key,
    verify_token
)
from app.db.session import get_db
from app.models.api_key import APIKey, APIKeyUsage
from app.schemas.api_key import (
    APIKeyCreate,
    APIKeyUpdate,
    APIKeyResponse,
    APIKeyUsageResponse
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/keys", response_model=APIKeyResponse)
async def create_api_key(
    *,
    db: Session = Depends(get_db),
    api_key_in: APIKeyCreate,
    token: str = Depends(oauth2_scheme)
):
    """
    Create a new API key.
    """
    # Verify token and get user
    token_data = verify_token(token)
    user_id = token_data["sub"]
    
    # Validate service
    if api_key_in.service_name not in API_SERVICES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid service. Available services: {list(API_SERVICES.keys())}"
        )
    
    # Check required fields
    service_config = API_SERVICES[api_key_in.service_name]
    for field in service_config["required_fields"]:
        if field not in api_key_in.key_metadata:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required field: {field}"
            )
    
    # Create API key
    encrypted_key = encrypt_api_key(api_key_in.key_metadata["api_key"])
    db_api_key = APIKey(
        service_name=api_key_in.service_name,
        encrypted_key=encrypted_key,
        key_metadata=api_key_in.key_metadata,
        owner_id=user_id,
        rate_limit=api_key_in.rate_limit or settings.RATE_LIMIT_PER_MINUTE
    )
    
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    
    return db_api_key

@router.get("/keys", response_model=List[APIKeyResponse])
async def get_api_keys(
    *,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    service_name: Optional[str] = None
):
    """
    Get all API keys for the authenticated user.
    """
    # Verify token and get user
    token_data = verify_token(token)
    user_id = token_data["sub"]
    
    # Query API keys
    query = db.query(APIKey).filter(APIKey.owner_id == user_id)
    if service_name:
        query = query.filter(APIKey.service_name == service_name)
    
    return query.all()

@router.get("/keys/{key_id}", response_model=APIKeyResponse)
async def get_api_key(
    *,
    db: Session = Depends(get_db),
    key_id: int,
    token: str = Depends(oauth2_scheme)
):
    """
    Get a specific API key by ID.
    """
    # Verify token and get user
    token_data = verify_token(token)
    user_id = token_data["sub"]
    
    # Get API key
    api_key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.owner_id == user_id
    ).first()
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    
    return api_key

@router.put("/keys/{key_id}", response_model=APIKeyResponse)
async def update_api_key(
    *,
    db: Session = Depends(get_db),
    key_id: int,
    api_key_in: APIKeyUpdate,
    token: str = Depends(oauth2_scheme)
):
    """
    Update an API key.
    """
    # Verify token and get user
    token_data = verify_token(token)
    user_id = token_data["sub"]
    
    # Get API key
    api_key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.owner_id == user_id
    ).first()
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    
    # Update fields
    if api_key_in.key_metadata:
        # Validate required fields
        service_config = API_SERVICES[api_key.service_name]
        for field in service_config["required_fields"]:
            if field not in api_key_in.key_metadata:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required field: {field}"
                )
        
        # Update key and metadata
        api_key.encrypted_key = encrypt_api_key(api_key_in.key_metadata["api_key"])
        api_key.key_metadata = api_key_in.key_metadata
    
    if api_key_in.is_active is not None:
        api_key.is_active = api_key_in.is_active
    
    if api_key_in.rate_limit:
        api_key.rate_limit = api_key_in.rate_limit
    
    api_key.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(api_key)
    
    return api_key

@router.delete("/keys/{key_id}")
async def delete_api_key(
    *,
    db: Session = Depends(get_db),
    key_id: int,
    token: str = Depends(oauth2_scheme)
):
    """
    Delete an API key.
    """
    # Verify token and get user
    token_data = verify_token(token)
    user_id = token_data["sub"]
    
    # Get API key
    api_key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.owner_id == user_id
    ).first()
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    
    # Delete API key
    db.delete(api_key)
    db.commit()
    
    return {"message": "API key deleted successfully"}

@router.get("/keys/{key_id}/usage", response_model=List[APIKeyUsageResponse])
async def get_api_key_usage(
    *,
    db: Session = Depends(get_db),
    key_id: int,
    token: str = Depends(oauth2_scheme)
):
    """
    Get usage logs for an API key.
    """
    # Verify token and get user
    token_data = verify_token(token)
    user_id = token_data["sub"]
    
    # Get API key
    api_key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.owner_id == user_id
    ).first()
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    
    # Get usage logs
    usage_logs = db.query(APIKeyUsage).filter(
        APIKeyUsage.api_key_id == key_id
    ).order_by(APIKeyUsage.timestamp.desc()).all()
    
    return usage_logs 