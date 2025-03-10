"""
API endpoints for service integrations (TMDB, Weather, Disney Parks).
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from datetime import date

from app.db.session import get_db
from app.api.endpoints.users import get_current_active_user
from app.models.user import User
from app.models.api_key import APIKey
from app.services.tmdb import TMDBService
from app.services.weather import WeatherService, DISNEY_PARKS
from app.services.disney_parks import DisneyParksService, PARK_DESTINATIONS

router = APIRouter()

async def get_service(
    service_name: str,
    user: User,
    db: Session
) -> BaseService:
    """Get service instance with user's API key."""
    api_key = db.query(APIKey).filter(
        APIKey.owner_id == user.id,
        APIKey.service_name == service_name,
        APIKey.is_active == True
    ).first()
    
    if not api_key:
        raise HTTPException(
            status_code=404,
            detail=f"No active API key found for {service_name}"
        )
    
    if service_name == "tmdb":
        return TMDBService(api_key.encrypted_key)
    elif service_name == "weather":
        return WeatherService(api_key.encrypted_key)
    elif service_name == "disney_parks":
        return DisneyParksService(api_key.encrypted_key)
    else:
        raise HTTPException(status_code=400, detail="Invalid service")

# TMDB Endpoints
@router.get("/tmdb/search")
async def search_disney_content(
    query: str,
    content_type: str = Query("all", regex="^(movie|tv|all)$"),
    page: int = Query(1, gt=0),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Search for Disney content on TMDB."""
    service = await get_service("tmdb", current_user, db)
    try:
        return await service.search_disney_content(query, content_type, page)
    finally:
        await service.close()

@router.get("/tmdb/disney-plus")
async def get_disney_plus_content(
    content_type: str = Query("all", regex="^(movie|tv|all)$"),
    page: int = Query(1, gt=0),
    region: str = Query("US", min_length=2, max_length=2),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get content available on Disney+."""
    service = await get_service("tmdb", current_user, db)
    try:
        return await service.get_disney_plus_content(content_type, page, region)
    finally:
        await service.close()

@router.get("/tmdb/trending")
async def get_trending_disney(
    time_window: str = Query("week", regex="^(day|week)$"),
    content_type: str = Query("all", regex="^(movie|tv|all)$"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get trending Disney content."""
    service = await get_service("tmdb", current_user, db)
    try:
        return await service.get_trending_disney(time_window, content_type)
    finally:
        await service.close()

# Weather Endpoints
@router.get("/weather/current/{park_id}")
async def get_current_weather(
    park_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current weather for a Disney park."""
    if park_id not in DISNEY_PARKS:
        raise HTTPException(status_code=400, detail=f"Invalid park ID. Available parks: {list(DISNEY_PARKS.keys())}")
    
    service = await get_service("weather", current_user, db)
    try:
        return await service.get_current_weather(park_id)
    finally:
        await service.close()

@router.get("/weather/forecast/{park_id}")
async def get_weather_forecast(
    park_id: str,
    days: int = Query(3, ge=1, le=10),
    hour: Optional[int] = Query(None, ge=0, le=23),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get weather forecast for a Disney park."""
    if park_id not in DISNEY_PARKS:
        raise HTTPException(status_code=400, detail=f"Invalid park ID. Available parks: {list(DISNEY_PARKS.keys())}")
    
    service = await get_service("weather", current_user, db)
    try:
        return await service.get_forecast(park_id, days, hour)
    finally:
        await service.close()

@router.get("/weather/all-parks")
async def get_all_parks_weather(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current weather for all Disney parks."""
    service = await get_service("weather", current_user, db)
    try:
        return await service.get_all_parks_weather()
    finally:
        await service.close()

# Disney Parks Endpoints
@router.get("/parks/destinations/{destination_id}")
async def get_destination_info(
    destination_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get information about a Disney destination."""
    if destination_id not in PARK_DESTINATIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid destination ID. Available destinations: {list(PARK_DESTINATIONS.keys())}"
        )
    
    service = await get_service("disney_parks", current_user, db)
    try:
        return await service.get_destination_info(destination_id)
    finally:
        await service.close()

@router.get("/parks/{destination_id}/{park_id}/wait-times")
async def get_wait_times(
    destination_id: str,
    park_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current wait times for attractions."""
    if destination_id not in PARK_DESTINATIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid destination ID. Available destinations: {list(PARK_DESTINATIONS.keys())}"
        )
    
    if park_id not in PARK_DESTINATIONS[destination_id]["parks"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid park ID. Available parks: {list(PARK_DESTINATIONS[destination_id]['parks'].keys())}"
        )
    
    service = await get_service("disney_parks", current_user, db)
    try:
        return await service.get_wait_times(destination_id, park_id)
    finally:
        await service.close()

@router.get("/parks/{destination_id}/{park_id}/schedule")
async def get_park_hours(
    destination_id: str,
    park_id: str,
    start_date: date,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get park hours for a date range."""
    if destination_id not in PARK_DESTINATIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid destination ID. Available destinations: {list(PARK_DESTINATIONS.keys())}"
        )
    
    if park_id not in PARK_DESTINATIONS[destination_id]["parks"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid park ID. Available parks: {list(PARK_DESTINATIONS[destination_id]['parks'].keys())}"
        )
    
    service = await get_service("disney_parks", current_user, db)
    try:
        return await service.get_park_hours(destination_id, park_id, start_date, end_date)
    finally:
        await service.close()

@router.get("/parks/{destination_id}/{park_id}/attractions")
async def get_attractions(
    destination_id: str,
    park_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get list of attractions for a park."""
    if destination_id not in PARK_DESTINATIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid destination ID. Available destinations: {list(PARK_DESTINATIONS.keys())}"
        )
    
    if park_id not in PARK_DESTINATIONS[destination_id]["parks"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid park ID. Available parks: {list(PARK_DESTINATIONS[destination_id]['parks'].keys())}"
        )
    
    service = await get_service("disney_parks", current_user, db)
    try:
        return await service.get_attractions(destination_id, park_id)
    finally:
        await service.close()

@router.get("/parks/{destination_id}/{park_id}/dining")
async def get_dining(
    destination_id: str,
    park_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get list of dining options for a park."""
    if destination_id not in PARK_DESTINATIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid destination ID. Available destinations: {list(PARK_DESTINATIONS.keys())}"
        )
    
    if park_id not in PARK_DESTINATIONS[destination_id]["parks"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid park ID. Available parks: {list(PARK_DESTINATIONS[destination_id]['parks'].keys())}"
        )
    
    service = await get_service("disney_parks", current_user, db)
    try:
        return await service.get_dining(destination_id, park_id)
    finally:
        await service.close() 