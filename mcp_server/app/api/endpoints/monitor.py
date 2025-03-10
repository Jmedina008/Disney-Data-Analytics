"""
API endpoints for monitoring and metrics.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from datetime import datetime

from app.core.monitoring import MonitoringService
from app.db.session import get_db
from app.api.endpoints.users import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.get("/health")
async def health_check(
    db: Session = Depends(get_db)
) -> Dict:
    """
    Get system health status.
    """
    return await MonitoringService.get_system_health(db)

@router.get("/monitor/usage")
async def get_usage_statistics(
    service_name: Optional[str] = None,
    days: int = Query(default=7, ge=1, le=30),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Dict:
    """
    Get API usage statistics.
    Args:
        service_name: Optional service to filter by
        days: Number of days to look back (1-30)
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return await MonitoringService.get_usage_statistics(
        db=db,
        service_name=service_name,
        days=days
    )

@router.get("/monitor/rate-limits/{api_key_id}")
async def get_rate_limit_status(
    api_key_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Dict:
    """
    Get current rate limit status for an API key.
    """
    return await MonitoringService.get_rate_limit_status(
        db=db,
        api_key_id=api_key_id
    )

@router.get("/monitor/errors")
async def get_error_report(
    service_name: Optional[str] = None,
    days: int = Query(default=7, ge=1, le=30),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> List[Dict]:
    """
    Get error report for API usage.
    Args:
        service_name: Optional service to filter by
        days: Number of days to look back (1-30)
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return await MonitoringService.get_error_report(
        db=db,
        service_name=service_name,
        days=days
    )

@router.get("/metrics")
async def get_metrics():
    """
    Get Prometheus metrics.
    This endpoint is typically scraped by Prometheus.
    """
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    from fastapi.responses import Response
    
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    ) 