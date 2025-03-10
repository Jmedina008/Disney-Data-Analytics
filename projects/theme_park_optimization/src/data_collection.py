"""
Data collection script for Disney Theme Park optimization.
Collects wait times, weather data, and park information from various sources.
"""

import os
import json
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ThemeParkDataCollector:
    """Class to collect theme park data from various sources."""
    
    def __init__(self):
        """Initialize the data collector with API keys and base URLs."""
        self.weather_api_key = os.getenv('WEATHER_API_KEY')
        self.theme_park_api_key = os.getenv('THEME_PARK_API_KEY')
        self.base_weather_url = "https://api.weatherapi.com/v1"
        self.parks = {
            'magic_kingdom': {'lat': 28.4177, 'lon': -81.5812},
            'epcot': {'lat': 28.3747, 'lon': -81.5494},
            'hollywood_studios': {'lat': 28.3578, 'lon': -81.5575},
            'animal_kingdom': {'lat': 28.3589, 'lon': -81.5908}
        }
    
    def fetch_weather_data(self, park: str, date: str) -> pd.DataFrame:
        """
        Fetch weather data for a specific park and date.
        Args:
            park: Park name
            date: Date in YYYY-MM-DD format
        Returns:
            pd.DataFrame: Weather data
        """
        try:
            params = {
                'key': self.weather_api_key,
                'q': f"{self.parks[park]['lat']},{self.parks[park]['lon']}",
                'dt': date
            }
            
            response = requests.get(f"{self.base_weather_url}/history.json", params=params)
            response.raise_for_status()
            
            data = response.json()
            weather_data = pd.DataFrame(data['forecast']['forecastday'][0]['hour'])
            weather_data['park'] = park
            weather_data['date'] = date
            
            return weather_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather data: {e}")
            return pd.DataFrame()
    
    def fetch_wait_times(self, park: str) -> pd.DataFrame:
        """
        Fetch current wait times for attractions in a park.
        Args:
            park: Park name
        Returns:
            pd.DataFrame: Wait time data
        """
        try:
            # This would typically use a theme park API
            # For now, we'll create simulated data
            attractions = self._get_park_attractions(park)
            current_time = datetime.now()
            
            wait_times = []
            for attraction in attractions:
                wait_time = {
                    'attraction_name': attraction,
                    'wait_time': np.random.randint(5, 120),
                    'timestamp': current_time,
                    'park': park,
                    'status': 'operating' if np.random.random() > 0.1 else 'closed'
                }
                wait_times.append(wait_time)
            
            return pd.DataFrame(wait_times)
            
        except Exception as e:
            logger.error(f"Error fetching wait times: {e}")
            return pd.DataFrame()
    
    def _get_park_attractions(self, park: str) -> List[str]:
        """
        Get list of attractions for a park.
        Args:
            park: Park name
        Returns:
            List[str]: List of attraction names
        """
        # This would typically come from an API or database
        attractions = {
            'magic_kingdom': [
                'Space Mountain',
                'Big Thunder Mountain Railroad',
                'Haunted Mansion',
                'Pirates of the Caribbean',
                'It\'s a Small World'
            ],
            'epcot': [
                'Soarin\'',
                'Test Track',
                'Mission: SPACE',
                'Spaceship Earth',
                'Frozen Ever After'
            ],
            'hollywood_studios': [
                'The Twilight Zone Tower of Terror',
                'Star Tours',
                'Slinky Dog Dash',
                'Rise of the Resistance',
                'Mickey & Minnie\'s Runaway Railway'
            ],
            'animal_kingdom': [
                'Expedition Everest',
                'Kilimanjaro Safaris',
                'Avatar Flight of Passage',
                'Dinosaur',
                'Kali River Rapids'
            ]
        }
        return attractions.get(park, [])
    
    def collect_historical_data(self, start_date: str, end_date: str) -> None:
        """
        Collect historical data for all parks.
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
        """
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        current = start
        
        while current <= end:
            date_str = current.strftime('%Y-%m-%d')
            
            for park in self.parks:
                # Collect weather data
                weather_data = self.fetch_weather_data(park, date_str)
                if not weather_data.empty:
                    self._save_data(weather_data, f'weather_{park}_{date_str}.csv')
                
                # Collect wait times (simulated historical data)
                wait_times = self.fetch_wait_times(park)
                if not wait_times.empty:
                    self._save_data(wait_times, f'wait_times_{park}_{date_str}.csv')
            
            current += timedelta(days=1)
    
    def _save_data(self, data: pd.DataFrame, filename: str) -> None:
        """
        Save collected data to CSV file.
        Args:
            data: DataFrame to save
            filename: Output filename
        """
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, filename)
        data.to_csv(output_path, index=False)
        logger.info(f"Data saved to {output_path}")

def main():
    """Main function to run data collection."""
    collector = ThemeParkDataCollector()
    
    # Collect data for the past week
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    collector.collect_historical_data(start_date, end_date)

if __name__ == "__main__":
    main() 