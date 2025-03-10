"""
Configuration settings for the MCP server.
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator
import secrets

class Settings(BaseSettings):
    """Server configuration settings."""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Disney Portfolio MCP Server"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS
    CORS_ORIGINS: List[AnyHttpUrl] = []
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: str | None = None
    
    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, any]) -> any:
        if isinstance(v, str):
            return v
        return f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}/{values.get('POSTGRES_DB')}"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    
    # External APIs
    TMDB_API_BASE_URL: str = "https://api.themoviedb.org/3"
    WEATHER_API_BASE_URL: str = "https://api.weatherapi.com/v1"
    DISNEY_PARKS_API_BASE_URL: str = "https://api.disneyparks.com/v1"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Encryption
    ENCRYPTION_KEY: str = secrets.token_urlsafe(32)
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# Create settings instance
settings = Settings()

# API Key Services
API_SERVICES = {
    "tmdb": {
        "name": "TMDB API",
        "base_url": settings.TMDB_API_BASE_URL,
        "docs_url": "https://developer.themoviedb.org/docs",
        "required_fields": ["api_key"]
    },
    "weather": {
        "name": "Weather API",
        "base_url": settings.WEATHER_API_BASE_URL,
        "docs_url": "https://www.weatherapi.com/docs/",
        "required_fields": ["api_key"]
    },
    "disney_parks": {
        "name": "Disney Parks API",
        "base_url": settings.DISNEY_PARKS_API_BASE_URL,
        "docs_url": "https://disneyparks.disney.go.com/docs/",
        "required_fields": ["api_key", "client_id"]
    }
} 