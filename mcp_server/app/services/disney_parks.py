"""
Disney Parks API service for accessing park data.
"""

from typing import Dict, List, Optional
from datetime import datetime, date

from app.services.base import BaseService

# Park IDs and their destinations
PARK_DESTINATIONS = {
    "wdw": {
        "name": "Walt Disney World",
        "parks": {
            "magic-kingdom": "Magic Kingdom Park",
            "epcot": "EPCOT",
            "hollywood-studios": "Disney's Hollywood Studios",
            "animal-kingdom": "Disney's Animal Kingdom"
        }
    },
    "dlr": {
        "name": "Disneyland Resort",
        "parks": {
            "disneyland": "Disneyland Park",
            "california-adventure": "Disney California Adventure"
        }
    },
    "dlp": {
        "name": "Disneyland Paris",
        "parks": {
            "disneyland-paris": "Disneyland Park",
            "walt-disney-studios": "Walt Disney Studios Park"
        }
    },
    "tdr": {
        "name": "Tokyo Disney Resort",
        "parks": {
            "tokyo-disneyland": "Tokyo Disneyland",
            "tokyo-disneysea": "Tokyo DisneySea"
        }
    },
    "hkdl": {
        "name": "Hong Kong Disneyland",
        "parks": {
            "hong-kong-disneyland": "Hong Kong Disneyland"
        }
    },
    "sdl": {
        "name": "Shanghai Disney Resort",
        "parks": {
            "shanghai-disneyland": "Shanghai Disneyland"
        }
    }
}

class DisneyParksService(BaseService):
    """Service for interacting with Disney Parks API."""
    
    def __init__(self, api_key: bytes):
        """Initialize Disney Parks service."""
        super().__init__(
            service_name="disney_parks",
            base_url="https://api.disneyparks.com/v1",
            api_key=api_key
        )
    
    def _get_headers(self, additional_headers: Optional[Dict] = None) -> Dict:
        """Get Disney Parks API headers."""
        headers = super()._get_headers(additional_headers)
        headers["Authorization"] = f"Bearer {self._api_key}"
        return headers
    
    async def get_destination_info(self, destination_id: str) -> Dict:
        """
        Get information about a Disney destination.
        Args:
            destination_id: Destination ID from PARK_DESTINATIONS
        """
        if destination_id not in PARK_DESTINATIONS:
            raise ValueError(f"Invalid destination ID. Available destinations: {list(PARK_DESTINATIONS.keys())}")
        
        return await self.get(f"destinations/{destination_id}")
    
    async def get_park_info(self, destination_id: str, park_id: str) -> Dict:
        """
        Get information about a specific park.
        Args:
            destination_id: Destination ID from PARK_DESTINATIONS
            park_id: Park ID from destination's parks
        """
        if destination_id not in PARK_DESTINATIONS:
            raise ValueError(f"Invalid destination ID. Available destinations: {list(PARK_DESTINATIONS.keys())}")
        
        if park_id not in PARK_DESTINATIONS[destination_id]["parks"]:
            raise ValueError(f"Invalid park ID. Available parks: {list(PARK_DESTINATIONS[destination_id]['parks'].keys())}")
        
        return await self.get(f"destinations/{destination_id}/parks/{park_id}")
    
    async def get_wait_times(self, destination_id: str, park_id: str) -> List[Dict]:
        """
        Get current wait times for attractions.
        Args:
            destination_id: Destination ID from PARK_DESTINATIONS
            park_id: Park ID from destination's parks
        """
        if destination_id not in PARK_DESTINATIONS:
            raise ValueError(f"Invalid destination ID. Available destinations: {list(PARK_DESTINATIONS.keys())}")
        
        if park_id not in PARK_DESTINATIONS[destination_id]["parks"]:
            raise ValueError(f"Invalid park ID. Available parks: {list(PARK_DESTINATIONS[destination_id]['parks'].keys())}")
        
        return await self.get(f"destinations/{destination_id}/parks/{park_id}/wait-times")
    
    async def get_park_hours(
        self,
        destination_id: str,
        park_id: str,
        start_date: date,
        end_date: Optional[date] = None
    ) -> List[Dict]:
        """
        Get park hours for a date range.
        Args:
            destination_id: Destination ID from PARK_DESTINATIONS
            park_id: Park ID from destination's parks
            start_date: Start date
            end_date: End date (optional, defaults to start_date)
        """
        if destination_id not in PARK_DESTINATIONS:
            raise ValueError(f"Invalid destination ID. Available destinations: {list(PARK_DESTINATIONS.keys())}")
        
        if park_id not in PARK_DESTINATIONS[destination_id]["parks"]:
            raise ValueError(f"Invalid park ID. Available parks: {list(PARK_DESTINATIONS[destination_id]['parks'].keys())}")
        
        params = {
            "start": start_date.isoformat()
        }
        if end_date:
            params["end"] = end_date.isoformat()
        
        return await self.get(
            f"destinations/{destination_id}/parks/{park_id}/schedule",
            params=params
        )
    
    async def get_attractions(self, destination_id: str, park_id: str) -> List[Dict]:
        """
        Get list of attractions for a park.
        Args:
            destination_id: Destination ID from PARK_DESTINATIONS
            park_id: Park ID from destination's parks
        """
        if destination_id not in PARK_DESTINATIONS:
            raise ValueError(f"Invalid destination ID. Available destinations: {list(PARK_DESTINATIONS.keys())}")
        
        if park_id not in PARK_DESTINATIONS[destination_id]["parks"]:
            raise ValueError(f"Invalid park ID. Available parks: {list(PARK_DESTINATIONS[destination_id]['parks'].keys())}")
        
        return await self.get(f"destinations/{destination_id}/parks/{park_id}/attractions")
    
    async def get_entertainment(self, destination_id: str, park_id: str) -> List[Dict]:
        """
        Get list of entertainment options for a park.
        Args:
            destination_id: Destination ID from PARK_DESTINATIONS
            park_id: Park ID from destination's parks
        """
        if destination_id not in PARK_DESTINATIONS:
            raise ValueError(f"Invalid destination ID. Available destinations: {list(PARK_DESTINATIONS.keys())}")
        
        if park_id not in PARK_DESTINATIONS[destination_id]["parks"]:
            raise ValueError(f"Invalid park ID. Available parks: {list(PARK_DESTINATIONS[destination_id]['parks'].keys())}")
        
        return await self.get(f"destinations/{destination_id}/parks/{park_id}/entertainment")
    
    async def get_dining(self, destination_id: str, park_id: str) -> List[Dict]:
        """
        Get list of dining options for a park.
        Args:
            destination_id: Destination ID from PARK_DESTINATIONS
            park_id: Park ID from destination's parks
        """
        if destination_id not in PARK_DESTINATIONS:
            raise ValueError(f"Invalid destination ID. Available destinations: {list(PARK_DESTINATIONS.keys())}")
        
        if park_id not in PARK_DESTINATIONS[destination_id]["parks"]:
            raise ValueError(f"Invalid park ID. Available parks: {list(PARK_DESTINATIONS[destination_id]['parks'].keys())}")
        
        return await self.get(f"destinations/{destination_id}/parks/{park_id}/dining")
    
    async def health_check(self) -> bool:
        """Check Disney Parks API availability."""
        try:
            # Check WDW as a test
            await self.get_destination_info("wdw")
            return True
        except Exception:
            return False 