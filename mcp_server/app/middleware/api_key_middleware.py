"""
Middleware for API key usage tracking and rate limiting.
"""

import time
from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.core.config import settings
from app.db.session import get_db
from app.models.api_key import APIKey, APIKeyUsage

async def track_api_key_usage(
    request: Request,
    api_key: APIKey,
    db: Session,
    response_status: int,
    response_time: float,
    error_message: Optional[str] = None
):
    """
    Track API key usage in the database.
    """
    usage = APIKeyUsage(
        api_key_id=api_key.id,
        timestamp=datetime.utcnow(),
        endpoint=str(request.url),
        response_status=response_status,
        response_time=response_time,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        error_message=error_message
    )
    
    # Update API key usage statistics
    api_key.last_used_at = datetime.utcnow()
    api_key.usage_count += 1
    
    db.add(usage)
    db.commit()

async def check_rate_limit(api_key: APIKey, db: Session) -> bool:
    """
    Check if the API key has exceeded its rate limit.
    Returns True if the key can be used, False if rate limit exceeded.
    """
    # Get recent usage count
    one_minute_ago = datetime.utcnow() - settings.RATE_LIMIT_WINDOW
    recent_usage = db.query(APIKeyUsage).filter(
        APIKeyUsage.api_key_id == api_key.id,
        APIKeyUsage.timestamp >= one_minute_ago
    ).count()
    
    return recent_usage < (api_key.rate_limit or settings.RATE_LIMIT_PER_MINUTE)

class APIKeyMiddleware:
    """
    Middleware for handling API key authentication, rate limiting, and usage tracking.
    """
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, request: Request, call_next):
        # Skip middleware for non-API routes
        if not request.url.path.startswith("/api"):
            return await call_next(request)
        
        # Skip middleware for API key management routes
        if request.url.path.startswith("/api/keys"):
            return await call_next(request)
        
        start_time = time.time()
        error_message = None
        response_status = 200
        
        try:
            # Get API key from header
            api_key_header = request.headers.get("X-API-Key")
            if not api_key_header:
                raise HTTPException(
                    status_code=401,
                    detail="API key is required"
                )
            
            # Get database session
            db = next(get_db())
            
            # Get API key from database
            api_key = db.query(APIKey).filter(
                APIKey.encrypted_key == api_key_header,
                APIKey.is_active == True
            ).first()
            
            if not api_key:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid API key"
                )
            
            # Check if API key has expired
            if api_key.expires_at and api_key.expires_at <= datetime.utcnow():
                raise HTTPException(
                    status_code=401,
                    detail="API key has expired"
                )
            
            # Check rate limit
            if not await check_rate_limit(api_key, db):
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded"
                )
            
            # Add API key to request state
            request.state.api_key = api_key
            
            # Process request
            response = await call_next(request)
            response_status = response.status_code
            
            return response
            
        except HTTPException as e:
            response_status = e.status_code
            error_message = str(e.detail)
            raise
            
        except Exception as e:
            response_status = 500
            error_message = str(e)
            raise
            
        finally:
            # Track API key usage if we have a valid key
            if hasattr(request.state, "api_key"):
                end_time = time.time()
                response_time = end_time - start_time
                
                await track_api_key_usage(
                    request=request,
                    api_key=request.state.api_key,
                    db=db,
                    response_status=response_status,
                    response_time=response_time,
                    error_message=error_message
                ) 