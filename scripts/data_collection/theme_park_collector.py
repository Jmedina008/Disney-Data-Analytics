"""
Theme Park Data Collector for Disney parks.
Fetches information about Disney theme parks, attractions, and wait times.
"""

import os
import json
from datetime import datetime
from pathlib import Path
import logging
from typing import Dict, List, Optional
import pandas as pd
import numpy as np

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ThemeParkCollector:
    def __init__(self):
        self.api_key = os.getenv('THEME_PARK_API_KEY')
        if not self.api_key:
            raise ValueError("THEME_PARK_API_KEY not found in environment variables")
        
        # Setup paths
        self.base_path = Path(__file__).parent.parent.parent
        self.raw_data_path = self.base_path / 'data' / 'raw' / 'theme_parks'
        self.raw_data_path.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('theme_park_collection.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Disney park IDs
        self.parks = {
            'magic_kingdom': 'WDW_MK',
            'epcot': 'WDW_EP',
            'hollywood_studios': 'WDW_HS',
            'animal_kingdom': 'WDW_AK',
            'disneyland': 'DLR_DL',
            'california_adventure': 'DLR_CA'
        }

    def fetch_park_data(self, park_id: str) -> Dict:
        """Fetch data for a specific park"""
        url = f"https://api.themeparks.wiki/v1/parks/{park_id}"
        
        try:
            response = requests.get(
                url,
                headers={'Authorization': f'Bearer {self.api_key}'}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching park data for {park_id}: {str(e)}")
            return {}

    def fetch_attractions(self, park_id: str) -> List[Dict]:
        """Fetch attractions for a specific park"""
        url = f"https://api.themeparks.wiki/v1/parks/{park_id}/attractions"
        
        try:
            response = requests.get(
                url,
                headers={'Authorization': f'Bearer {self.api_key}'}
            )
            response.raise_for_status()
            return response.json().get('attractions', [])
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching attractions for {park_id}: {str(e)}")
            return []

    def fetch_wait_times(self, park_id: str) -> List[Dict]:
        """Fetch current wait times for a specific park"""
        url = f"https://api.themeparks.wiki/v1/parks/{park_id}/waittimes"
        
        try:
            response = requests.get(
                url,
                headers={'Authorization': f'Bearer {self.api_key}'}
            )
            response.raise_for_status()
            return response.json().get('waittimes', [])
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching wait times for {park_id}: {str(e)}")
            return []

    def collect_park_data(self):
        """Collect data for all Disney parks"""
        park_data = []
        
        for park_name, park_id in self.parks.items():
            self.logger.info(f"Collecting data for {park_name}")
            
            # Get park information
            park_info = self.fetch_park_data(park_id)
            if not park_info:
                continue
            
            # Get attractions
            attractions = self.fetch_attractions(park_id)
            
            # Get wait times
            wait_times = self.fetch_wait_times(park_id)
            
            park_entry = {
                'park_id': park_id,
                'name': park_name,
                'location': {
                    'latitude': park_info.get('location', {}).get('latitude'),
                    'longitude': park_info.get('location', {}).get('longitude')
                },
                'operating_hours': park_info.get('operating_hours', []),
                'attractions': attractions,
                'wait_times': wait_times
            }
            
            park_data.append(park_entry)
        
        # Save collected data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.raw_data_path / f"theme_park_data_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(park_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Theme park data collection completed. Saved to {output_file}")
        
        # Create summary
        summary = {
            'total_parks': len(park_data),
            'total_attractions': sum(len(park['attractions']) for park in park_data),
            'parks': [
                {
                    'name': park['name'],
                    'attractions_count': len(park['attractions']),
                    'avg_wait_time': np.mean([wt['wait_time'] for wt in park['wait_times']]) 
                    if park['wait_times'] else 0
                }
                for park in park_data
            ]
        }
        
        # Save summary
        summary_file = self.raw_data_path / f"theme_park_summary_{timestamp}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        self.logger.info(f"Summary data saved to {summary_file}")

if __name__ == "__main__":
    collector = ThemeParkCollector()
    collector.collect_park_data() 