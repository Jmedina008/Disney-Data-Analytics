"""
Main FastAPI application for the Microservice Control Panel (MCP) server.
"""

import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from app.core.config import settings
from app.api.endpoints import api_keys, users, monitor, services
from app.middleware.api_key_middleware import APIKeyMiddleware
from app.db.session import engine
from app.models.api_key import Base as APIKeyBase
from app.models.user import Base as UserBase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
APIKeyBase.metadata.create_all(bind=engine)
UserBase.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Microservice Control Panel (MCP) server for managing API keys and services",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add API key middleware
app.add_middleware(APIKeyMiddleware)

# Mount Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Include API routers
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(api_keys.router, prefix="/api", tags=["api-keys"])
app.include_router(monitor.router, prefix="/api", tags=["monitoring"])
app.include_router(services.router, prefix="/api", tags=["services"])

@app.get("/")
async def root():
    """
    Root endpoint returning a welcome message.
    """
    return {
        "message": "Welcome to the Microservice Control Panel (MCP) server",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 