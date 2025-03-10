"""
Automated data collection script for Disney portfolio projects.
This script coordinates the collection of data from various sources and can be scheduled to run periodically.
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path
import pandas as pd
import requests
from dotenv import load_dotenv
import json

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_collection.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class DataCollector:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.raw_data_path = self.base_path / 'data' / 'raw'
        self.processed_data_path = self.base_path / 'data' / 'processed'
        
        # Create directories if they don't exist
        for path in [self.raw_data_path, self.processed_data_path]:
            path.mkdir(parents=True, exist_ok=True)
            
        # Initialize API keys
        self.tmdb_api_key = os.getenv('TMDB_API_KEY')
        self.theme_park_api_key = os.getenv('THEME_PARK_API_KEY')
        self.weather_api_key = os.getenv('WEATHER_API_KEY')
        
        if not all([self.tmdb_api_key, self.theme_park_api_key, self.weather_api_key]):
            raise ValueError("Missing required API keys in environment variables")

    def collect_disney_plus_data(self):
        """Collect Disney+ content data from TMDB API"""
        logger.info("Starting Disney+ content data collection...")
        try:
            # Implementation of TMDB API calls
            base_url = "https://api.themoviedb.org/3"
            headers = {
                "Authorization": f"Bearer {self.tmdb_api_key}",
                "Content-Type": "application/json;charset=utf-8"
            }
            
            # Get Disney+ content
            disney_content = []
            page = 1
            while True:
                response = requests.get(
                    f"{base_url}/discover/movie",
                    headers=headers,
                    params={
                        "with_watch_providers": "337",  # Disney+ provider ID
                        "watch_region": "US",
                        "page": page
                    }
                )
                data = response.json()
                if not data.get('results'):
                    break
                disney_content.extend(data['results'])
                page += 1
                
            # Save raw data
            timestamp = datetime.now().strftime('%Y%m%d')
            output_file = self.raw_data_path / 'disney_plus' / f'content_{timestamp}.json'
            output_file.parent.mkdir(exist_ok=True)
            
            with open(output_file, 'w') as f:
                json.dump(disney_content, f)
                
            logger.info(f"Collected {len(disney_content)} Disney+ content items")
            return True
            
        except Exception as e:
            logger.error(f"Error collecting Disney+ data: {str(e)}")
            return False

    def collect_theme_park_data(self):
        """Collect theme park wait times and weather data"""
        logger.info("Starting theme park data collection...")
        try:
            # Implementation of theme park API calls
            parks = ['WDW_MK', 'WDW_EP', 'WDW_HS', 'WDW_AK']
            
            for park in parks:
                response = requests.get(
                    f"https://api.themeparks.wiki/v1/parks/{park}/waittime",
                    headers={"Authorization": f"Bearer {self.theme_park_api_key}"}
                )
                data = response.json()
                
                # Save raw data
                timestamp = datetime.now().strftime('%Y%m%d_%H%M')
                output_file = self.raw_data_path / 'theme_parks' / park / f'wait_times_{timestamp}.json'
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_file, 'w') as f:
                    json.dump(data, f)
                    
            logger.info("Theme park data collection completed")
            return True
            
        except Exception as e:
            logger.error(f"Error collecting theme park data: {str(e)}")
            return False

    def collect_box_office_data(self):
        """Collect box office performance data"""
        logger.info("Starting box office data collection...")
        try:
            # Implementation of box office API calls
            base_url = "https://api.themoviedb.org/3"
            headers = {
                "Authorization": f"Bearer {self.tmdb_api_key}",
                "Content-Type": "application/json;charset=utf-8"
            }
            
            # Get Disney movies with box office data
            disney_movies = []
            page = 1
            while True:
                response = requests.get(
                    f"{base_url}/discover/movie",
                    headers=headers,
                    params={
                        "with_companies": "2",  # Disney company ID
                        "sort_by": "release_date.desc",
                        "page": page
                    }
                )
                data = response.json()
                if not data.get('results'):
                    break
                disney_movies.extend(data['results'])
                page += 1
                
            # Save raw data
            timestamp = datetime.now().strftime('%Y%m%d')
            output_file = self.raw_data_path / 'entertainment' / f'box_office_{timestamp}.json'
            output_file.parent.mkdir(exist_ok=True)
            
            with open(output_file, 'w') as f:
                json.dump(disney_movies, f)
                
            logger.info(f"Collected box office data for {len(disney_movies)} Disney movies")
            return True
            
        except Exception as e:
            logger.error(f"Error collecting box office data: {str(e)}")
            return False

    def run_all_collections(self):
        """Run all data collection tasks"""
        logger.info("Starting full data collection process...")
        
        results = {
            "disney_plus": self.collect_disney_plus_data(),
            "theme_parks": self.collect_theme_park_data(),
            "box_office": self.collect_box_office_data()
        }
        
        success_count = sum(1 for result in results.values() if result)
        logger.info(f"Data collection completed. {success_count}/3 tasks successful.")
        
        return results

if __name__ == "__main__":
    collector = DataCollector()
    collector.run_all_collections() 