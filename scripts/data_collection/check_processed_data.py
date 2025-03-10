"""
Script to check the processed Disney movie data.
Displays key statistics and sample records.
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def main():
    # Load processed data
    base_path = Path(__file__).parent.parent.parent
    processed_data_path = base_path / 'data' / 'processed' / 'disney_plus' / f'disney_movies_processed_{datetime.now().strftime("%Y%m%d")}.parquet'
    
    print(f"Loading processed data from {processed_data_path}...")
    df = pd.read_parquet(processed_data_path)
    
    # Display basic information
    print("\nDataset Overview:")
    print(f"Total movies: {len(df)}")
    print(f"Time span: {df['release_year'].min()} - {df['release_year'].max()}")
    print(f"\nColumns available: {', '.join(df.columns)}")
    
    # Financial statistics
    print("\nFinancial Statistics:")
    print(f"Average budget: ${df['budget_millions'].mean():.2f}M")
    print(f"Average revenue: ${df['revenue_millions'].mean():.2f}M")
    print(f"Average ROI: {df['roi'].mean():.2f}%")
    
    # Top performing movies
    print("\nTop 5 Highest Grossing Movies:")
    top_revenue = df.nlargest(5, 'revenue_millions')[['title', 'release_year', 'revenue_millions', 'budget_millions']]
    print(top_revenue.to_string(index=False))
    
    # Most popular movies
    print("\nTop 5 Most Popular Movies:")
    top_popular = df.nlargest(5, 'popularity')[['title', 'release_year', 'popularity', 'vote_average']]
    print(top_popular.to_string(index=False))
    
    # Genre distribution
    print("\nGenre Distribution:")
    all_genres = [genre for genres in df['genres'] for genre in genres]
    genre_counts = pd.Series(all_genres).value_counts()
    print(genre_counts.head().to_string())

if __name__ == "__main__":
    main() 