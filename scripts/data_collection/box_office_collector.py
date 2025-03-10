"""
Box Office Data Collector for Disney movies.
Fetches box office data from TMDB API and combines with movie details.
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

class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy types"""
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                          np.int16, np.int32, np.int64, np.uint8,
                          np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)
        return super().default(obj)

class BoxOfficeCollector:
    def __init__(self):
        self.api_key = os.getenv('TMDB_API_KEY')
        if not self.api_key:
            raise ValueError("TMDB_API_KEY not found in environment variables")
        
        self.base_url = "https://api.themoviedb.org/3"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json;charset=utf-8'
        }
        
        # Setup paths
        self.base_path = Path(__file__).parent.parent.parent
        self.raw_data_path = self.base_path / 'data' / 'raw' / 'box_office'
        self.raw_data_path.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('box_office_collection.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def fetch_movie_financials(self, movie_id: int) -> Dict:
        """Fetch financial details for a specific movie"""
        url = f"{self.base_url}/movie/{movie_id}"
        params = {
            'append_to_response': 'release_dates,alternative_titles'
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching movie financials for ID {movie_id}: {str(e)}")
            return {}

    def collect_box_office_data(self):
        """Collect box office data for Disney movies"""
        # First, load existing movie data
        movies_file = self.base_path / 'data' / 'raw' / 'disney_plus' / 'disney_movies_20250309_231327.json'
        with open(movies_file, 'r', encoding='utf-8') as f:
            movies_data = json.load(f)
        
        box_office_data = []
        
        for movie in movies_data:
            movie_id = movie['id']
            self.logger.info(f"Fetching box office data for {movie['title']} (ID: {movie_id})")
            
            financials = self.fetch_movie_financials(movie_id)
            if financials:
                box_office_entry = {
                    'movie_id': movie_id,
                    'title': movie['title'],
                    'release_date': movie['release_date'],
                    'budget': financials.get('budget', 0),
                    'revenue': financials.get('revenue', 0),
                    'runtime': financials.get('runtime', 0),
                    'status': financials.get('status', ''),
                    'popularity': financials.get('popularity', 0),
                    'vote_average': financials.get('vote_average', 0),
                    'vote_count': financials.get('vote_count', 0),
                    'genres': [g['name'] for g in financials.get('genres', [])],
                    'production_countries': [c['name'] for c in financials.get('production_countries', [])]
                }
                
                # Add release dates by country
                release_dates = financials.get('release_dates', {}).get('results', [])
                for country_data in release_dates:
                    country = country_data.get('iso_3166_1', '')
                    dates = country_data.get('release_dates', [])
                    if dates:
                        box_office_entry[f'release_date_{country}'] = dates[0].get('release_date', '')
                
                box_office_data.append(box_office_entry)
        
        # Save collected data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.raw_data_path / f"box_office_data_{timestamp}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(box_office_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Box office data collection completed. Saved to {output_file}")
        
        # Create a summary DataFrame
        df = pd.DataFrame(box_office_data)
        summary = {
            'total_movies': int(len(df)),
            'total_revenue': float(df['revenue'].sum()),
            'avg_revenue': float(df['revenue'].mean()),
            'avg_budget': float(df['budget'].mean()),
            'highest_grossing': str(df.loc[df['revenue'].idxmax(), 'title']),
            'most_expensive': str(df.loc[df['budget'].idxmax(), 'title']),
            'best_rated': str(df.loc[df['vote_average'].idxmax(), 'title']),
            'most_popular': str(df.loc[df['popularity'].idxmax(), 'title'])
        }
        
        # Save summary
        summary_file = self.raw_data_path / f"box_office_summary_{timestamp}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, cls=NumpyEncoder)
        
        self.logger.info(f"Summary data saved to {summary_file}")

if __name__ == "__main__":
    collector = BoxOfficeCollector()
    collector.collect_box_office_data() 