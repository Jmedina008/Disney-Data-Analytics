"""
Data processing script for Disney movie data.
Cleans and transforms raw movie data for analysis.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

def load_raw_data(file_path: Path) -> List[Dict]:
    """Load raw movie data from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_box_office_data(file_path: Path) -> Dict[int, Dict]:
    """Load box office data from JSON file and index by movie ID"""
    with open(file_path, 'r', encoding='utf-8') as f:
        box_office_list = json.load(f)
        return {item['movie_id']: item for item in box_office_list}

def clean_movie_data(movies: List[Dict], box_office_data: Dict[int, Dict]) -> pd.DataFrame:
    """Clean and transform movie data"""
    df = pd.DataFrame(movies)
    
    # Merge box office data
    df['box_office'] = df['id'].map(lambda x: box_office_data.get(x, {}))
    
    # Convert dates
    df['release_date'] = pd.to_datetime(df['release_date'])
    df['release_year'] = df['release_date'].dt.year
    df['release_month'] = df['release_date'].dt.month
    
    # Clean monetary values and merge with box office data
    df['budget'] = df.apply(lambda row: row['box_office'].get('budget', row['budget']) if row['box_office'] else row['budget'], axis=1)
    df['revenue'] = df.apply(lambda row: row['box_office'].get('revenue', row['revenue']) if row['box_office'] else row['revenue'], axis=1)
    df['budget'] = df['budget'].fillna(0)
    df['revenue'] = df['revenue'].fillna(0)
    df['budget_millions'] = df['budget'] / 1_000_000
    df['revenue_millions'] = df['revenue'] / 1_000_000
    
    # Calculate ROI
    df['roi'] = np.where(
        df['budget'] > 0,
        (df['revenue'] - df['budget']) / df['budget'] * 100,
        0
    )
    
    # Extract box office specific fields
    df['vote_count'] = df.apply(lambda row: row['box_office'].get('vote_count', 0) if row['box_office'] else 0, axis=1)
    df['vote_average'] = df.apply(lambda row: row['box_office'].get('vote_average', 0.0) if row['box_office'] else 0.0, axis=1)
    df['popularity'] = df.apply(lambda row: row['box_office'].get('popularity', 0.0) if row['box_office'] else 0.0, axis=1)
    
    # Extract genres
    df['genres'] = df['genres'].apply(lambda x: [genre['name'] for genre in x] if x else [])
    
    # Extract production countries
    df['production_countries'] = df['production_countries'].apply(
        lambda x: [country['name'] for country in x] if x else []
    )
    
    # Clean runtime
    df['runtime'] = df['runtime'].fillna(0)
    df['runtime_hours'] = df['runtime'] / 60
    
    # Extract keywords
    df['keywords'] = df['keywords'].apply(
        lambda x: [kw['name'] for kw in x['keywords']] if x and 'keywords' in x else []
    )
    
    # Extract cast and crew
    df['cast'] = df['credits'].apply(
        lambda x: [cast['name'] for cast in x['cast'][:5]] if x and 'cast' in x else []
    )
    df['director'] = df['credits'].apply(
        lambda x: next((crew['name'] for crew in x['crew'] 
                       if crew['job'] == 'Director'), None) 
        if x and 'crew' in x else None
    )
    
    # Drop intermediate columns
    df = df.drop(['box_office'], axis=1)
    
    return df

def save_processed_data(df: pd.DataFrame, output_path: Path):
    """Save processed data to parquet format"""
    df.to_parquet(output_path, index=False)

def main():
    # Setup paths
    base_path = Path(__file__).parent.parent.parent
    raw_data_path = base_path / 'data' / 'raw' / 'disney_plus' / 'disney_movies_20250309_231327.json'
    box_office_path = base_path / 'data' / 'raw' / 'box_office' / 'box_office_data_20250309_231911.json'
    processed_data_path = base_path / 'data' / 'processed' / 'disney_plus'
    processed_data_path.mkdir(parents=True, exist_ok=True)
    
    # Process data
    print("Loading raw data...")
    raw_data = load_raw_data(raw_data_path)
    
    print("Loading box office data...")
    box_office_data = load_box_office_data(box_office_path)
    
    print("Cleaning and transforming data...")
    processed_df = clean_movie_data(raw_data, box_office_data)
    
    # Save processed data
    output_file = processed_data_path / f"disney_movies_processed_{datetime.now().strftime('%Y%m%d')}.parquet"
    print(f"Saving processed data to {output_file}...")
    save_processed_data(processed_df, output_file)
    
    print("Data processing completed!")
    print(f"Processed {len(processed_df)} movies")

if __name__ == "__main__":
    main() 