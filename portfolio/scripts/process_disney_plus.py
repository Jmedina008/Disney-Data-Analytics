"""
Process Disney+ content data from TMDB API.
This script processes raw API data and creates cleaned datasets for analysis.
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_raw_data(file_path: str) -> list:
    """Load raw JSON data from TMDB API."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading raw data: {e}")
        return []

def process_content(raw_data: list) -> pd.DataFrame:
    """Process raw content data into a structured DataFrame."""
    processed_data = []
    
    for item in raw_data:
        try:
            processed_item = {
                'id': item.get('id'),
                'title': item.get('title') or item.get('name'),
                'type': 'movie' if 'title' in item else 'series',
                'release_date': item.get('release_date') or item.get('first_air_date'),
                'popularity': item.get('popularity'),
                'vote_average': item.get('vote_average'),
                'vote_count': item.get('vote_count'),
                'genres': [g['name'] for g in item.get('genres', [])],
                'overview': item.get('overview'),
                'original_language': item.get('original_language')
            }
            processed_data.append(processed_item)
        except Exception as e:
            logging.warning(f"Error processing item {item.get('id')}: {e}")
            continue
    
    return pd.DataFrame(processed_data)

def calculate_metrics(df: pd.DataFrame) -> dict:
    """Calculate various metrics from the processed data."""
    metrics = {
        'total_titles': len(df),
        'movies_count': len(df[df['type'] == 'movie']),
        'series_count': len(df[df['type'] == 'series']),
        'avg_rating': df['vote_average'].mean(),
        'top_genres': df.explode('genres')['genres'].value_counts().head(5).to_dict(),
        'language_distribution': df['original_language'].value_counts().to_dict()
    }
    return metrics

def main():
    # Create necessary directories
    data_dir = Path('data')
    raw_dir = data_dir / 'raw'
    processed_dir = data_dir / 'processed'
    metrics_dir = data_dir / 'metrics'
    
    for dir_path in [data_dir, raw_dir, processed_dir, metrics_dir]:
        dir_path.mkdir(exist_ok=True)
    
    # Load and process data
    raw_data = load_raw_data(raw_dir / 'disney_plus_content.json')
    if not raw_data:
        logging.error("No data to process")
        return
    
    # Process content data
    df = process_content(raw_data)
    
    # Calculate metrics
    metrics = calculate_metrics(df)
    
    # Save processed data
    timestamp = datetime.now().strftime('%Y%m%d')
    df.to_csv(processed_dir / f'disney_plus_content_{timestamp}.csv', index=False)
    
    with open(metrics_dir / f'content_metrics_{timestamp}.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    logging.info("Data processing completed successfully")

if __name__ == '__main__':
    main() 