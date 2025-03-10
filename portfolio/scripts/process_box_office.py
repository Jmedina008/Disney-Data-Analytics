"""
Process box office performance data for Disney movies.
This script combines TMDB data with box office performance data and generates analytics.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import logging
import json
from typing import Dict, List

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_tmdb_data(file_path: str) -> pd.DataFrame:
    """Load movie data from TMDB API."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    except Exception as e:
        logging.error(f"Error loading TMDB data: {e}")
        return pd.DataFrame()

def load_box_office_data(file_path: str) -> pd.DataFrame:
    """Load box office data from CSV file."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        logging.error(f"Error loading box office data: {e}")
        return pd.DataFrame()

def process_financial_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process and calculate financial metrics."""
    try:
        df['profit'] = df['revenue'] - df['budget']
        df['roi'] = (df['profit'] / df['budget']) * 100
        df['revenue_per_budget'] = df['revenue'] / df['budget']
        
        # Adjust for inflation (simplified)
        current_year = datetime.now().year
        df['years_since_release'] = current_year - pd.to_datetime(df['release_date']).dt.year
        df['budget_adjusted'] = df['budget'] * (1.02 ** df['years_since_release'])
        df['revenue_adjusted'] = df['revenue'] * (1.02 ** df['years_since_release'])
        
        return df
    except Exception as e:
        logging.error(f"Error processing financial data: {e}")
        return df

def calculate_franchise_metrics(df: pd.DataFrame) -> Dict:
    """Calculate metrics for movie franchises."""
    franchise_metrics = {}
    
    try:
        franchises = df.groupby('franchise').agg({
            'budget': 'sum',
            'revenue': 'sum',
            'profit': 'sum',
            'vote_average': 'mean',
            'title': 'count'
        }).round(2)
        
        franchises = franchises.rename(columns={'title': 'movie_count'})
        franchises['avg_profit_per_movie'] = (franchises['profit'] / 
                                            franchises['movie_count']).round(2)
        
        franchise_metrics = franchises.to_dict(orient='index')
    except Exception as e:
        logging.error(f"Error calculating franchise metrics: {e}")
    
    return franchise_metrics

def analyze_seasonal_performance(df: pd.DataFrame) -> Dict:
    """Analyze movie performance by release season."""
    seasonal_metrics = {}
    
    try:
        df['release_month'] = pd.to_datetime(df['release_date']).dt.month
        df['season'] = pd.cut(df['release_month'],
                            bins=[0, 3, 6, 9, 12],
                            labels=['Winter', 'Spring', 'Summer', 'Fall'])
        
        seasonal = df.groupby('season').agg({
            'revenue': 'mean',
            'profit': 'mean',
            'vote_average': 'mean',
            'title': 'count'
        }).round(2)
        
        seasonal = seasonal.rename(columns={'title': 'movie_count'})
        seasonal_metrics = seasonal.to_dict(orient='index')
    except Exception as e:
        logging.error(f"Error analyzing seasonal performance: {e}")
    
    return seasonal_metrics

def main():
    # Create necessary directories
    data_dir = Path('data')
    raw_dir = data_dir / 'raw'
    processed_dir = data_dir / 'processed'
    analytics_dir = data_dir / 'analytics'
    
    for dir_path in [data_dir, raw_dir, processed_dir, analytics_dir]:
        dir_path.mkdir(exist_ok=True)
    
    # Load data
    tmdb_df = load_tmdb_data(raw_dir / 'disney_movies.json')
    box_office_df = load_box_office_data(raw_dir / 'box_office_data.csv')
    
    if tmdb_df.empty or box_office_df.empty:
        logging.error("Missing required data")
        return
    
    # Merge and process data
    merged_df = pd.merge(tmdb_df, box_office_df, on='movie_id', how='inner')
    processed_df = process_financial_data(merged_df)
    
    # Calculate metrics
    franchise_metrics = calculate_franchise_metrics(processed_df)
    seasonal_metrics = analyze_seasonal_performance(processed_df)
    
    # Save processed data and metrics
    timestamp = datetime.now().strftime('%Y%m%d')
    processed_df.to_csv(processed_dir / f'movie_performance_{timestamp}.csv', index=False)
    
    analytics = {
        'franchise_performance': franchise_metrics,
        'seasonal_performance': seasonal_metrics,
        'top_performers': processed_df.nlargest(10, 'profit')[
            ['title', 'revenue', 'budget', 'profit', 'roi']
        ].to_dict(orient='records'),
        'summary_stats': {
            'total_movies': len(processed_df),
            'total_revenue': processed_df['revenue'].sum(),
            'total_profit': processed_df['profit'].sum(),
            'avg_roi': processed_df['roi'].mean(),
            'median_budget': processed_df['budget'].median()
        }
    }
    
    with open(analytics_dir / f'box_office_analytics_{timestamp}.json', 'w') as f:
        json.dump(analytics, f, indent=2)
    
    logging.info("Data processing and analytics completed successfully")

if __name__ == '__main__':
    main() 