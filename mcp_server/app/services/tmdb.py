"""
TMDB service for accessing movie and TV show data.
"""

from typing import Dict, List, Optional
from datetime import datetime

from app.services.base import BaseService

class TMDBService(BaseService):
    """Service for interacting with TMDB API."""
    
    def __init__(self, api_key: bytes):
        """Initialize TMDB service."""
        super().__init__(
            service_name="tmdb",
            base_url="https://api.themoviedb.org/3",
            api_key=api_key
        )
    
    def _get_headers(self, additional_headers: Optional[Dict] = None) -> Dict:
        """Get TMDB-specific headers."""
        headers = super()._get_headers(additional_headers)
        headers["Authorization"] = f"Bearer {self._api_key}"
        return headers
    
    async def search_disney_content(
        self,
        query: str,
        content_type: str = "all",
        page: int = 1
    ) -> Dict:
        """
        Search for Disney content.
        Args:
            query: Search query
            content_type: Type of content ('movie', 'tv', or 'all')
            page: Page number
        """
        # Company ID for Disney is 2
        params = {
            "query": query,
            "page": page,
            "with_companies": 2
        }
        
        if content_type == "movie":
            endpoint = "search/movie"
        elif content_type == "tv":
            endpoint = "search/tv"
        else:
            endpoint = "search/multi"
        
        return await self.get(endpoint, params=params)
    
    async def get_disney_plus_content(
        self,
        content_type: str = "all",
        page: int = 1,
        region: str = "US"
    ) -> Dict:
        """
        Get content available on Disney+.
        Args:
            content_type: Type of content ('movie', 'tv', or 'all')
            page: Page number
            region: Region code
        """
        # Disney+ provider ID is 337
        params = {
            "with_watch_providers": 337,
            "watch_region": region,
            "page": page
        }
        
        if content_type == "movie":
            endpoint = "discover/movie"
        elif content_type == "tv":
            endpoint = "discover/tv"
        else:
            # For 'all', we'll need to make two requests and combine results
            movies = await self.get("discover/movie", params=params)
            tv_shows = await self.get("discover/tv", params=params)
            
            return {
                "page": page,
                "results": movies.get("results", []) + tv_shows.get("results", []),
                "total_pages": max(
                    movies.get("total_pages", 0),
                    tv_shows.get("total_pages", 0)
                ),
                "total_results": (
                    movies.get("total_results", 0) +
                    tv_shows.get("total_results", 0)
                )
            }
        
        return await self.get(endpoint, params=params)
    
    async def get_content_details(
        self,
        content_id: int,
        content_type: str
    ) -> Dict:
        """
        Get detailed information about a specific movie or TV show.
        Args:
            content_id: TMDB ID
            content_type: Type of content ('movie' or 'tv')
        """
        params = {
            "append_to_response": "videos,images,credits,similar,watch/providers"
        }
        
        endpoint = f"{content_type}/{content_id}"
        return await self.get(endpoint, params=params)
    
    async def get_trending_disney(
        self,
        time_window: str = "week",
        content_type: str = "all"
    ) -> Dict:
        """
        Get trending Disney content.
        Args:
            time_window: Time window ('day' or 'week')
            content_type: Type of content ('movie', 'tv', or 'all')
        """
        endpoint = f"trending/{content_type}/{time_window}"
        
        # Get trending content and filter for Disney
        results = await self.get(endpoint)
        
        # Filter for Disney content (company ID 2)
        disney_content = []
        for item in results.get("results", []):
            details = await self.get_content_details(
                item["id"],
                "movie" if item.get("media_type") == "movie" else "tv"
            )
            if any(company.get("id") == 2 for company in details.get("production_companies", [])):
                disney_content.append(item)
        
        results["results"] = disney_content
        results["total_results"] = len(disney_content)
        
        return results
    
    async def get_upcoming_disney_releases(self, region: str = "US") -> Dict:
        """
        Get upcoming Disney movie releases.
        Args:
            region: Region code
        """
        params = {
            "with_companies": 2,  # Disney company ID
            "region": region
        }
        
        return await self.get("movie/upcoming", params=params)
    
    async def health_check(self) -> bool:
        """Check TMDB API availability."""
        try:
            await self.get("configuration")
            return True
        except Exception:
            return False 