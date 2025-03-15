import pandas as pd
import numpy as np
from datetime import datetime
import os

class DataProcessor:
    def __init__(self, raw_data_path, processed_data_path):
        """Initialize data processor with input and output paths."""
        self.raw_data_path = raw_data_path
        self.processed_data_path = processed_data_path
        
        # Create output directories if they don't exist
        for path in [
            f"{processed_data_path}/disney_plus",
            f"{processed_data_path}/theme_parks",
            f"{processed_data_path}/entertainment"
        ]:
            os.makedirs(path, exist_ok=True)

    def process_movie_data(self):
        """Process movie data for analysis."""
        try:
            # Load raw movie data
            df = pd.read_json(f"{self.raw_data_path}/disney_plus/disney_movies_raw.json")
            
            # Clean and transform data
            df['release_date'] = pd.to_datetime(df['release_date'])
            df['year'] = df['release_date'].dt.year
            df['month'] = df['release_date'].dt.month
            
            # Calculate derived metrics
            df['roi'] = (df['revenue'] - df['budget']) / df['budget'] * 100
            df['profit'] = df['revenue'] - df['budget']
            
            # Clean genre data
            df['genres'] = df['genres'].fillna('[]').apply(eval).apply(lambda x: '|'.join([g['name'] for g in x]))
            
            # Save processed data
            output_path = f"{self.processed_data_path}/disney_plus/movies_processed.parquet"
            df.to_parquet(output_path)
            print(f"Processed movie data saved to {output_path}")
            
        except Exception as e:
            print(f"Error processing movie data: {e}")

    def process_theme_park_data(self):
        """Process theme park data for analysis."""
        try:
            # Load raw theme park data
            df = pd.read_json(f"{self.raw_data_path}/theme_parks/wait_times_raw.json")
            
            # Clean and transform data
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.day_name()
            df['is_weekend'] = df['timestamp'].dt.dayofweek.isin([5, 6])
            
            # Calculate rolling averages
            df['wait_time_ma'] = df.groupby('attraction_name')['wait_time'].transform(
                lambda x: x.rolling(window=24, min_periods=1).mean()
            )
            
            # Save processed data
            output_path = f"{self.processed_data_path}/theme_parks/wait_times_processed.parquet"
            df.to_parquet(output_path)
            print(f"Processed theme park data saved to {output_path}")
            
        except Exception as e:
            print(f"Error processing theme park data: {e}")

    def process_streaming_data(self):
        """Process streaming platform data for analysis."""
        try:
            # Load raw streaming data
            df = pd.read_json(f"{self.raw_data_path}/disney_plus/streaming_data_raw.json")
            
            # Clean and transform data
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['watch_date'] = df['timestamp'].dt.date
            
            # Calculate engagement metrics
            df['completion_rate'] = df['watched_duration'] / df['total_duration'] * 100
            df['is_completed'] = df['completion_rate'] >= 90
            
            # Save processed data
            output_path = f"{self.processed_data_path}/disney_plus/streaming_processed.parquet"
            df.to_parquet(output_path)
            print(f"Processed streaming data saved to {output_path}")
            
        except Exception as e:
            print(f"Error processing streaming data: {e}")

    def process_industry_data(self):
        """Process entertainment industry data for analysis."""
        try:
            # Load raw industry data
            df = pd.read_json(f"{self.raw_data_path}/entertainment/industry_data_raw.json")
            
            # Clean and transform data
            df['date'] = pd.to_datetime(df['date'])
            df['year'] = df['date'].dt.year
            df['quarter'] = df['date'].dt.quarter
            
            # Calculate market share
            df['market_share'] = df.groupby('year')['revenue'].transform(
                lambda x: x / x.sum() * 100
            )
            
            # Save processed data
            output_path = f"{self.processed_data_path}/entertainment/industry_processed.parquet"
            df.to_parquet(output_path)
            print(f"Processed industry data saved to {output_path}")
            
        except Exception as e:
            print(f"Error processing industry data: {e}")

    def process_franchise_data(self):
        """Process franchise performance data for analysis."""
        try:
            # Load raw franchise data
            df = pd.read_json(f"{self.raw_data_path}/entertainment/franchise_data_raw.json")
            
            # Clean and transform data
            df['date'] = pd.to_datetime(df['date'])
            df['year'] = df['date'].dt.year
            
            # Calculate total revenue and revenue share
            df['total_revenue'] = df['box_office_revenue'] + df['merchandise_revenue'] + df['licensing_revenue']
            for col in ['box_office_revenue', 'merchandise_revenue', 'licensing_revenue']:
                df[f"{col}_share"] = df[col] / df['total_revenue'] * 100
            
            # Save processed data
            output_path = f"{self.processed_data_path}/entertainment/franchise_processed.parquet"
            df.to_parquet(output_path)
            print(f"Processed franchise data saved to {output_path}")
            
        except Exception as e:
            print(f"Error processing franchise data: {e}")

    def process_all(self):
        """Process all datasets."""
        print("Starting data processing pipeline...")
        self.process_movie_data()
        self.process_theme_park_data()
        self.process_streaming_data()
        self.process_industry_data()
        self.process_franchise_data()
        print("Data processing pipeline completed.")

def main():
    # Set up paths
    raw_data_path = "data/raw"
    processed_data_path = "data/processed"
    
    # Initialize processor
    processor = DataProcessor(raw_data_path, processed_data_path)
    
    # Run processing pipeline
    processor.process_all()

if __name__ == "__main__":
    main() 