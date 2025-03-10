"""
Monitoring utilities for the MCP server.
Handles metrics collection, system health checks, and usage statistics.
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from prometheus_client import Counter, Histogram, Gauge
from sqlalchemy.orm import Session
from sqlalchemy import func
from loguru import logger

from app.models.api_key import APIKey, APIKeyUsage
from app.core.config import API_SERVICES

# Prometheus metrics
REQUEST_COUNT = Counter(
    "mcp_request_total",
    "Total request count",
    ["service", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "mcp_request_latency_seconds",
    "Request latency in seconds",
    ["service", "endpoint"]
)

ACTIVE_KEYS = Gauge(
    "mcp_active_api_keys",
    "Number of active API keys",
    ["service"]
)

class MonitoringService:
    """Service for monitoring system metrics and health."""
    
    @staticmethod
    async def get_system_health(db: Session) -> Dict:
        """
        Get system health metrics.
        """
        try:
            # Check database connection
            db.execute("SELECT 1")
            db_status = "healthy"
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            db_status = "unhealthy"
        
        return {
            "status": "healthy" if db_status == "healthy" else "unhealthy",
            "timestamp": datetime.utcnow(),
            "components": {
                "database": db_status,
                "api_services": {
                    service: "available"
                    for service in API_SERVICES.keys()
                }
            }
        }
    
    @staticmethod
    async def get_usage_statistics(
        db: Session,
        service_name: Optional[str] = None,
        days: int = 7
    ) -> Dict:
        """
        Get API usage statistics.
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Base query
        query = db.query(
            APIKeyUsage.api_key_id,
            func.count().label("request_count"),
            func.avg(APIKeyUsage.response_time).label("avg_response_time"),
            func.count().filter(APIKeyUsage.error_message != None).label("error_count")
        ).filter(APIKeyUsage.timestamp >= start_date)
        
        if service_name:
            query = query.join(APIKey).filter(APIKey.service_name == service_name)
        
        query = query.group_by(APIKeyUsage.api_key_id)
        
        # Get results
        results = query.all()
        
        # Format statistics
        stats = {
            "period_days": days,
            "total_requests": sum(r.request_count for r in results),
            "total_errors": sum(r.error_count for r in results),
            "avg_response_time": sum(r.avg_response_time for r in results) / len(results) if results else 0,
            "active_keys": len(results)
        }
        
        return stats
    
    @staticmethod
    async def get_rate_limit_status(
        db: Session,
        api_key_id: int
    ) -> Dict:
        """
        Get current rate limit status for an API key.
        """
        # Get API key
        api_key = db.query(APIKey).filter(APIKey.id == api_key_id).first()
        if not api_key:
            return {"error": "API key not found"}
        
        # Get recent usage
        one_minute_ago = datetime.utcnow() - timedelta(minutes=1)
        recent_usage = db.query(func.count()).filter(
            APIKeyUsage.api_key_id == api_key_id,
            APIKeyUsage.timestamp >= one_minute_ago
        ).scalar()
        
        return {
            "service": api_key.service_name,
            "rate_limit": api_key.rate_limit,
            "current_usage": recent_usage,
            "remaining": max(0, api_key.rate_limit - recent_usage),
            "reset_at": (one_minute_ago + timedelta(minutes=1)).isoformat()
        }
    
    @staticmethod
    async def get_error_report(
        db: Session,
        service_name: Optional[str] = None,
        days: int = 7
    ) -> List[Dict]:
        """
        Get error report for API usage.
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Query for errors
        query = db.query(
            APIKeyUsage
        ).filter(
            APIKeyUsage.timestamp >= start_date,
            APIKeyUsage.error_message != None
        )
        
        if service_name:
            query = query.join(APIKey).filter(APIKey.service_name == service_name)
        
        errors = query.order_by(APIKeyUsage.timestamp.desc()).all()
        
        return [{
            "timestamp": error.timestamp.isoformat(),
            "service": error.api_key.service_name,
            "endpoint": error.endpoint,
            "status": error.response_status,
            "error": error.error_message
        } for error in errors]
    
    @staticmethod
    def record_request(
        service: str,
        endpoint: str,
        status: int,
        duration: float
    ) -> None:
        """
        Record request metrics using Prometheus.
        """
        REQUEST_COUNT.labels(
            service=service,
            endpoint=endpoint,
            status=status
        ).inc()
        
        REQUEST_LATENCY.labels(
            service=service,
            endpoint=endpoint
        ).observe(duration)
    
    @staticmethod
    def update_active_keys(service: str, count: int) -> None:
        """
        Update active keys gauge.
        """
        ACTIVE_KEYS.labels(service=service).set(count) 