"""
TMDB Data Collector for Disney movies.
Fetches movie data from The Movie Database (TMDB) API.
"""

import os
import json
from datetime import datetime
from pathlib import Path
import logging
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TMDBCollector:
    def __init__(self):
        self.api_key = os.getenv('TMDB_API_KEY')
        if not self.api_key:
            raise ValueError("TMDB_API_KEY not found in environment variables")
        
        self.base_url = "https://api.themoviedb.org/3"
        self.company_id = 2  # Disney's company ID in TMDB
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json;charset=utf-8'
        }
        
        # Setup paths
        self.base_path = Path(__file__).parent.parent.parent
        self.raw_data_path = self.base_path / 'data' / 'raw' / 'disney_plus'
        self.raw_data_path.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('tmdb_collection.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def fetch_disney_movies(self, page: int = 1) -> Dict:
        """Fetch Disney movies from TMDB API"""
        url = f"{self.base_url}/discover/movie"
        params = {
            'with_companies': self.company_id,
            'page': page,
            'sort_by': 'primary_release_date.desc'
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching Disney movies: {str(e)}")
            return {}

    def fetch_movie_details(self, movie_id: int) -> Dict:
        """Fetch detailed information for a specific movie"""
        url = f"{self.base_url}/movie/{movie_id}"
        params = {
            'append_to_response': 'credits,keywords,videos,release_dates'
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching movie details for ID {movie_id}: {str(e)}")
            return {}

    def collect_data(self, max_pages: int = 10):
        """Collect Disney movie data and save to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        movies_data = []
        
        for page in range(1, max_pages + 1):
            self.logger.info(f"Fetching page {page} of {max_pages}")
            
            # Fetch movies list
            movies_page = self.fetch_disney_movies(page)
            if not movies_page.get('results'):
                break
            
            # Fetch detailed information for each movie
            for movie in movies_page['results']:
                movie_details = self.fetch_movie_details(movie['id'])
                if movie_details:
                    movies_data.append(movie_details)
            
            self.logger.info(f"Collected {len(movies_data)} movies so far")
        
        # Save collected data
        output_file = self.raw_data_path / f"disney_movies_{timestamp}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(movies_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Data collection completed. Saved to {output_file}")

if __name__ == "__main__":
    collector = TMDBCollector()
    collector.collect_data() 