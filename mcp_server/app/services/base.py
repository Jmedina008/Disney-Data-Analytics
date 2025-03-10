"""
Base service class for external API integrations.
"""

import aiohttp
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
from loguru import logger

from app.core.config import settings
from app.core.monitoring import MonitoringService
from app.core.security import decrypt_api_key

class BaseService:
    """Base class for external API services."""
    
    def __init__(
        self,
        service_name: str,
        base_url: str,
        api_key: bytes,
        session: Optional[aiohttp.ClientSession] = None
    ):
        """
        Initialize service.
        Args:
            service_name: Name of the service
            base_url: Base URL for API requests
            api_key: Encrypted API key
            session: Optional aiohttp session
        """
        self.service_name = service_name
        self.base_url = base_url.rstrip('/')
        self._api_key = decrypt_api_key(api_key)
        self._session = session or aiohttp.ClientSession()
    
    async def close(self):
        """Close the HTTP session."""
        if self._session and not self._session.closed:
            await self._session.close()
    
    def _get_headers(self, additional_headers: Optional[Dict] = None) -> Dict:
        """
        Get request headers.
        Args:
            additional_headers: Additional headers to include
        Returns:
            Dict: Headers for the request
        """
        headers = {
            "Accept": "application/json",
            "User-Agent": f"Disney-Portfolio-MCP/{settings.PROJECT_NAME}"
        }
        if additional_headers:
            headers.update(additional_headers)
        return headers
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.
        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            headers: Request headers
            json_data: JSON request body
            timeout: Request timeout in seconds
        Returns:
            Dict: Response data
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        start_time = datetime.utcnow()
        
        try:
            async with self._session.request(
                method=method,
                url=url,
                params=params,
                headers=self._get_headers(headers),
                json=json_data,
                timeout=timeout
            ) as response:
                duration = (datetime.utcnow() - start_time).total_seconds()
                
                # Record metrics
                MonitoringService.record_request(
                    service=self.service_name,
                    endpoint=endpoint,
                    status=response.status,
                    duration=duration
                )
                
                # Log request details
                logger.info(
                    f"API Request: {method} {url} - Status: {response.status} - Duration: {duration:.2f}s"
                )
                
                # Handle response
                if response.status == 429:
                    logger.warning(f"{self.service_name} rate limit exceeded")
                    raise Exception("Rate limit exceeded")
                
                response.raise_for_status()
                return await response.json()
                
        except asyncio.TimeoutError:
            logger.error(f"{self.service_name} request timeout: {url}")
            raise
        except Exception as e:
            logger.error(f"{self.service_name} request error: {str(e)}")
            raise
    
    async def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make GET request."""
        return await self._make_request("GET", endpoint, **kwargs)
    
    async def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make POST request."""
        return await self._make_request("POST", endpoint, **kwargs)
    
    async def put(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make PUT request."""
        return await self._make_request("PUT", endpoint, **kwargs)
    
    async def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make DELETE request."""
        return await self._make_request("DELETE", endpoint, **kwargs)
    
    async def health_check(self) -> bool:
        """
        Check if the service is available.
        Returns:
            bool: True if service is available
        """
        try:
            # Make a simple request to check service availability
            await self.get("status")
            return True
        except Exception:
            return False 