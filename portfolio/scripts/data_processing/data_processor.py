"""
Data processing module for Disney portfolio projects.
Handles data validation, cleaning, and transformation for all data sources.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from sklearn.preprocessing import StandardScaler
from pandas.api.types import is_numeric_dtype

class DataProcessor:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.raw_path = self.base_path / 'data' / 'raw'
        self.processed_path = self.base_path / 'data' / 'processed'
        self.analytics_path = self.base_path / 'data' / 'analytics'
        
        # Create necessary directories
        for path in [self.raw_path, self.processed_path, self.analytics_path]:
            path.mkdir(parents=True, exist_ok=True)
            
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def validate_disney_plus_data(self, data: List[Dict]) -> List[Dict]:
        """Validate Disney+ content data"""
        valid_data = []
        required_fields = {'id', 'title', 'overview', 'release_date', 'vote_average'}
        
        for item in data:
            if not all(field in item for field in required_fields):
                self.logger.warning(f"Missing required fields in item {item.get('id', 'unknown')}")
                continue
                
            try:
                # Validate date format
                datetime.strptime(item['release_date'], '%Y-%m-%d')
                
                # Validate numeric fields
                if not (0 <= float(item['vote_average']) <= 10):
                    raise ValueError("Invalid vote average")
                    
                valid_data.append(item)
            except (ValueError, TypeError) as e:
                self.logger.warning(f"Validation failed for item {item.get('id', 'unknown')}: {str(e)}")
                
        return valid_data

    def clean_disney_plus_data(self, data: List[Dict]) -> pd.DataFrame:
        """Clean and transform Disney+ content data"""
        df = pd.DataFrame(data)
        
        # Convert dates
        df['release_date'] = pd.to_datetime(df['release_date'])
        df['release_year'] = df['release_date'].dt.year
        df['release_month'] = df['release_date'].dt.month
        
        # Clean text fields
        text_columns = ['title', 'overview']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].fillna('').str.strip()
                
        # Handle numeric fields
        numeric_columns = ['vote_average', 'vote_count', 'popularity']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
        # Create genre lists
        if 'genres' in df.columns:
            df['genre_list'] = df['genres'].apply(lambda x: [g['name'] for g in x] if isinstance(x, list) else [])
            
        return df

    def validate_theme_park_data(self, data: Dict) -> Dict:
        """Validate theme park wait times data"""
        required_fields = {'id', 'name', 'waitTime', 'status', 'lastUpdate'}
        
        if not isinstance(data, dict) or 'rides' not in data:
            raise ValueError("Invalid theme park data format")
            
        valid_rides = []
        for ride in data['rides']:
            if all(field in ride for field in required_fields):
                try:
                    # Validate wait time
                    wait_time = int(ride['waitTime'])
                    if wait_time < 0:
                        raise ValueError
                        
                    # Validate timestamp
                    datetime.fromisoformat(ride['lastUpdate'].replace('Z', '+00:00'))
                    
                    valid_rides.append(ride)
                except (ValueError, TypeError):
                    self.logger.warning(f"Invalid data for ride {ride.get('id', 'unknown')}")
                    
        data['rides'] = valid_rides
        return data

    def clean_theme_park_data(self, data: Dict) -> pd.DataFrame:
        """Clean and transform theme park wait times data"""
        rides_data = []
        
        for ride in data['rides']:
            ride_info = {
                'ride_id': ride['id'],
                'name': ride['name'],
                'wait_time': ride['waitTime'],
                'status': ride['status'],
                'last_update': pd.to_datetime(ride['lastUpdate']),
                'park': data.get('park', ''),
                'is_open': ride['status'] == 'OPERATING'
            }
            rides_data.append(ride_info)
            
        df = pd.DataFrame(rides_data)
        
        # Add time-based features
        df['hour'] = df['last_update'].dt.hour
        df['day_of_week'] = df['last_update'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].isin([5, 6])
        
        # Handle missing values
        df['wait_time'] = df['wait_time'].fillna(0)
        
        return df

    def validate_box_office_data(self, data: List[Dict]) -> List[Dict]:
        """Validate box office performance data"""
        valid_data = []
        required_fields = {'id', 'title', 'release_date', 'revenue', 'budget'}
        
        for movie in data:
            if not all(field in movie for field in required_fields):
                self.logger.warning(f"Missing required fields in movie {movie.get('id', 'unknown')}")
                continue
                
            try:
                # Validate numeric fields
                revenue = float(movie['revenue'])
                budget = float(movie['budget'])
                if revenue < 0 or budget < 0:
                    raise ValueError("Invalid financial data")
                    
                # Validate date
                datetime.strptime(movie['release_date'], '%Y-%m-%d')
                
                valid_data.append(movie)
            except (ValueError, TypeError) as e:
                self.logger.warning(f"Validation failed for movie {movie.get('id', 'unknown')}: {str(e)}")
                
        return valid_data

    def clean_box_office_data(self, data: List[Dict]) -> pd.DataFrame:
        """Clean and transform box office data"""
        df = pd.DataFrame(data)
        
        # Convert dates
        df['release_date'] = pd.to_datetime(df['release_date'])
        df['release_year'] = df['release_date'].dt.year
        df['release_month'] = df['release_date'].dt.month
        
        # Handle financial data
        financial_columns = ['revenue', 'budget']
        for col in financial_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
        # Calculate derived metrics
        df['profit'] = df['revenue'] - df['budget']
        df['roi'] = (df['profit'] / df['budget']).replace([np.inf, -np.inf], np.nan)
        
        # Clean text fields
        text_columns = ['title', 'overview']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].fillna('').str.strip()
                
        return df

    def process_all_data(self):
        """Process all collected data"""
        try:
            # Process Disney+ content data
            latest_content = self._get_latest_file(self.raw_path / 'disney_plus', 'content_*.json')
            if latest_content:
                with open(latest_content, 'r') as f:
                    content_data = json.load(f)
                valid_content = self.validate_disney_plus_data(content_data)
                content_df = self.clean_disney_plus_data(valid_content)
                content_df.to_parquet(self.processed_path / 'disney_plus' / 'content_latest.parquet')
                
            # Process theme park data
            for park in ['WDW_MK', 'WDW_EP', 'WDW_HS', 'WDW_AK']:
                latest_wait_times = self._get_latest_file(self.raw_path / 'theme_parks' / park, 'wait_times_*.json')
                if latest_wait_times:
                    with open(latest_wait_times, 'r') as f:
                        wait_times_data = json.load(f)
                    valid_wait_times = self.validate_theme_park_data(wait_times_data)
                    wait_times_df = self.clean_theme_park_data(valid_wait_times)
                    wait_times_df.to_parquet(self.processed_path / 'theme_parks' / f'{park}_latest.parquet')
                    
            # Process box office data
            latest_box_office = self._get_latest_file(self.raw_path / 'entertainment', 'box_office_*.json')
            if latest_box_office:
                with open(latest_box_office, 'r') as f:
                    box_office_data = json.load(f)
                valid_box_office = self.validate_box_office_data(box_office_data)
                box_office_df = self.clean_box_office_data(valid_box_office)
                box_office_df.to_parquet(self.processed_path / 'entertainment' / 'box_office_latest.parquet')
                
            self.logger.info("All data processed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing data: {str(e)}")
            return False

    def _get_latest_file(self, directory: Path, pattern: str) -> Optional[Path]:
        """Get the most recent file matching the pattern in the directory"""
        files = list(directory.glob(pattern))
        return max(files, default=None, key=lambda x: x.stat().st_mtime)

if __name__ == "__main__":
    processor = DataProcessor()
    processor.process_all_data() 