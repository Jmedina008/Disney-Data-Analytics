"""
Weather API service for accessing weather data for Disney parks.
"""

from typing import Dict, List, Optional
from datetime import datetime, date

from app.services.base import BaseService

# Disney park locations
DISNEY_PARKS = {
    "magic_kingdom": {
        "lat": 28.4177,
        "lon": -81.5812,
        "name": "Magic Kingdom Park"
    },
    "epcot": {
        "lat": 28.3747,
        "lon": -81.5494,
        "name": "EPCOT"
    },
    "hollywood_studios": {
        "lat": 28.3578,
        "lon": -81.5583,
        "name": "Disney's Hollywood Studios"
    },
    "animal_kingdom": {
        "lat": 28.3589,
        "lon": -81.5908,
        "name": "Disney's Animal Kingdom"
    },
    "disneyland": {
        "lat": 33.8121,
        "lon": -117.9190,
        "name": "Disneyland Park"
    },
    "california_adventure": {
        "lat": 33.8061,
        "lon": -117.9215,
        "name": "Disney California Adventure"
    },
    "disneyland_paris": {
        "lat": 48.8722,
        "lon": 2.7758,
        "name": "Disneyland Paris"
    },
    "tokyo_disneyland": {
        "lat": 35.6329,
        "lon": 139.8804,
        "name": "Tokyo Disneyland"
    },
    "hong_kong_disneyland": {
        "lat": 22.3130,
        "lon": 114.0413,
        "name": "Hong Kong Disneyland"
    },
    "shanghai_disneyland": {
        "lat": 31.1434,
        "lon": 121.6579,
        "name": "Shanghai Disneyland"
    }
}

class WeatherService(BaseService):
    """Service for interacting with Weather API."""
    
    def __init__(self, api_key: bytes):
        """Initialize Weather service."""
        super().__init__(
            service_name="weather",
            base_url="https://api.weatherapi.com/v1",
            api_key=api_key
        )
    
    def _get_params(self, params: Optional[Dict] = None) -> Dict:
        """Get Weather API parameters."""
        base_params = {"key": self._api_key}
        if params:
            base_params.update(params)
        return base_params
    
    async def get_current_weather(self, park_id: str) -> Dict:
        """
        Get current weather for a Disney park.
        Args:
            park_id: Park identifier from DISNEY_PARKS
        """
        if park_id not in DISNEY_PARKS:
            raise ValueError(f"Invalid park ID. Available parks: {list(DISNEY_PARKS.keys())}")
        
        park = DISNEY_PARKS[park_id]
        params = self._get_params({
            "q": f"{park['lat']},{park['lon']}"
        })
        
        data = await self.get("current.json", params=params)
        data["park"] = park
        return data
    
    async def get_forecast(
        self,
        park_id: str,
        days: int = 3,
        hour: Optional[int] = None
    ) -> Dict:
        """
        Get weather forecast for a Disney park.
        Args:
            park_id: Park identifier from DISNEY_PARKS
            days: Number of days (1-10)
            hour: Specific hour (0-23) for hourly forecast
        """
        if park_id not in DISNEY_PARKS:
            raise ValueError(f"Invalid park ID. Available parks: {list(DISNEY_PARKS.keys())}")
        
        park = DISNEY_PARKS[park_id]
        params = self._get_params({
            "q": f"{park['lat']},{park['lon']}",
            "days": min(max(days, 1), 10)
        })
        
        data = await self.get("forecast.json", params=params)
        data["park"] = park
        
        # Filter for specific hour if requested
        if hour is not None:
            hour = max(0, min(hour, 23))
            for day in data.get("forecast", {}).get("forecastday", []):
                day["hour"] = [h for h in day.get("hour", []) if datetime.fromisoformat(h["time"]).hour == hour]
        
        return data
    
    async def get_historical_weather(
        self,
        park_id: str,
        target_date: date
    ) -> Dict:
        """
        Get historical weather data for a Disney park.
        Args:
            park_id: Park identifier from DISNEY_PARKS
            target_date: Historical date to retrieve
        """
        if park_id not in DISNEY_PARKS:
            raise ValueError(f"Invalid park ID. Available parks: {list(DISNEY_PARKS.keys())}")
        
        park = DISNEY_PARKS[park_id]
        params = self._get_params({
            "q": f"{park['lat']},{park['lon']}",
            "dt": target_date.isoformat()
        })
        
        data = await self.get("history.json", params=params)
        data["park"] = park
        return data
    
    async def get_all_parks_weather(self) -> List[Dict]:
        """Get current weather for all Disney parks."""
        results = []
        for park_id in DISNEY_PARKS:
            try:
                weather = await self.get_current_weather(park_id)
                results.append(weather)
            except Exception as e:
                logger.error(f"Error getting weather for {park_id}: {str(e)}")
        
        return results
    
    async def health_check(self) -> bool:
        """Check Weather API availability."""
        try:
            # Check weather for Magic Kingdom as a test
            await self.get_current_weather("magic_kingdom")
            return True
        except Exception:
            return False 