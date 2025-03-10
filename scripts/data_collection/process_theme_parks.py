"""
Data processing script for Disney theme park data.
Cleans and transforms raw theme park data for analysis.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

def load_raw_data(file_path: Path) -> List[Dict]:
    """Load raw theme park data from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def process_attractions(attractions: List[Dict]) -> pd.DataFrame:
    """Process attractions data into a DataFrame"""
    if not attractions:
        return pd.DataFrame()
    
    df = pd.DataFrame(attractions)
    
    # Clean and transform fields
    df['is_open'] = df['status'].apply(lambda x: x == 'OPERATING')
    df['last_updated'] = pd.to_datetime(df['last_updated'])
    
    # Extract categories and tags
    df['categories'] = df['categories'].fillna('').apply(lambda x: [cat['name'] for cat in x] if x else [])
    df['tags'] = df['tags'].fillna('').apply(lambda x: [tag['name'] for tag in x] if x else [])
    
    return df

def process_wait_times(wait_times: List[Dict]) -> pd.DataFrame:
    """Process wait time data into a DataFrame"""
    if not wait_times:
        return pd.DataFrame()
    
    df = pd.DataFrame(wait_times)
    
    # Convert timestamps
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Clean wait times
    df['wait_time'] = df['wait_time'].fillna(0)
    df['wait_time_minutes'] = df['wait_time'] / 60  # Convert to minutes
    
    return df

def clean_park_data(parks: List[Dict]) -> pd.DataFrame:
    """Clean and transform park data"""
    processed_parks = []
    
    for park in parks:
        # Process basic park info
        park_info = {
            'park_id': park['park_id'],
            'name': park['name'],
            'latitude': park['location']['latitude'],
            'longitude': park['location']['longitude']
        }
        
        # Process operating hours
        operating_hours = park.get('operating_hours', [])
        if operating_hours:
            park_info['opening_time'] = pd.to_datetime(operating_hours[0].get('open_time'))
            park_info['closing_time'] = pd.to_datetime(operating_hours[0].get('close_time'))
            park_info['is_open'] = operating_hours[0].get('is_open', False)
        
        # Process attractions
        attractions_df = process_attractions(park.get('attractions', []))
        if not attractions_df.empty:
            park_info['total_attractions'] = len(attractions_df)
            park_info['operating_attractions'] = len(attractions_df[attractions_df['is_open']])
            
            # Get attraction categories
            all_categories = [cat for cats in attractions_df['categories'] for cat in cats]
            park_info['attraction_categories'] = list(set(all_categories))
        
        # Process wait times
        wait_times_df = process_wait_times(park.get('wait_times', []))
        if not wait_times_df.empty:
            park_info['avg_wait_time'] = wait_times_df['wait_time_minutes'].mean()
            park_info['max_wait_time'] = wait_times_df['wait_time_minutes'].max()
            park_info['min_wait_time'] = wait_times_df['wait_time_minutes'].min()
        
        processed_parks.append(park_info)
    
    return pd.DataFrame(processed_parks)

def save_processed_data(df: pd.DataFrame, output_path: Path):
    """Save processed data to parquet format"""
    df.to_parquet(output_path, index=False)

def main():
    # Setup paths
    base_path = Path(__file__).parent.parent.parent
    raw_data_path = base_path / 'data' / 'raw' / 'theme_parks'
    processed_data_path = base_path / 'data' / 'processed' / 'theme_parks'
    processed_data_path.mkdir(parents=True, exist_ok=True)
    
    # Get latest raw data file
    raw_files = list(raw_data_path.glob('theme_park_data_*.json'))
    if not raw_files:
        print("No raw data files found")
        return
    
    latest_file = max(raw_files, key=lambda x: x.stat().st_mtime)
    print(f"Processing {latest_file}...")
    
    # Process data
    raw_data = load_raw_data(latest_file)
    processed_df = clean_park_data(raw_data)
    
    # Save processed data
    output_file = processed_data_path / f"theme_parks_processed_{datetime.now().strftime('%Y%m%d')}.parquet"
    print(f"Saving processed data to {output_file}...")
    save_processed_data(processed_df, output_file)
    
    print("Data processing completed!")
    print(f"Processed {len(processed_df)} parks")

if __name__ == "__main__":
    main() 