"""
Data processing script for Disney Theme Park optimization.
Processes and analyzes collected wait times and weather data.
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from sklearn.preprocessing import StandardScaler
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ThemeParkDataProcessor:
    """Class to process and analyze theme park data."""
    
    def __init__(self):
        """Initialize the data processor."""
        self.scaler = StandardScaler()
        self.parks = [
            'magic_kingdom',
            'epcot',
            'hollywood_studios',
            'animal_kingdom'
        ]
    
    def load_data(self, start_date: str, end_date: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Load wait times and weather data for the specified date range.
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: Wait times and weather data
        """
        wait_times_dfs = []
        weather_dfs = []
        
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        current = start
        
        while current <= end:
            date_str = current.strftime('%Y-%m-%d')
            
            for park in self.parks:
                # Load wait times
                wait_times_file = os.path.join('data', 'raw', f'wait_times_{park}_{date_str}.csv')
                if os.path.exists(wait_times_file):
                    df = pd.read_csv(wait_times_file)
                    wait_times_dfs.append(df)
                
                # Load weather data
                weather_file = os.path.join('data', 'raw', f'weather_{park}_{date_str}.csv')
                if os.path.exists(weather_file):
                    df = pd.read_csv(weather_file)
                    weather_dfs.append(df)
            
            current += timedelta(days=1)
        
        wait_times_df = pd.concat(wait_times_dfs, ignore_index=True) if wait_times_dfs else pd.DataFrame()
        weather_df = pd.concat(weather_dfs, ignore_index=True) if weather_dfs else pd.DataFrame()
        
        return wait_times_df, weather_df
    
    def clean_wait_times(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and preprocess wait times data.
        Args:
            df: Wait times DataFrame
        Returns:
            pd.DataFrame: Cleaned wait times data
        """
        if df.empty:
            return df
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Add time-based features
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        # Handle missing values
        df['wait_time'] = df['wait_time'].fillna(df.groupby('attraction_name')['wait_time'].transform('mean'))
        
        # Create binary status column
        df['is_operating'] = (df['status'] == 'operating').astype(int)
        
        return df
    
    def clean_weather(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and preprocess weather data.
        Args:
            df: Weather DataFrame
        Returns:
            pd.DataFrame: Cleaned weather data
        """
        if df.empty:
            return df
        
        # Convert date and time columns
        df['date'] = pd.to_datetime(df['date'])
        df['hour'] = pd.to_datetime(df['time']).dt.hour
        
        # Select relevant features
        weather_features = [
            'temp_c', 'wind_kph', 'precip_mm', 'humidity',
            'cloud', 'feelslike_c', 'will_it_rain', 'chance_of_rain'
        ]
        
        # Keep only necessary columns
        cols_to_keep = ['date', 'hour', 'park'] + [col for col in weather_features if col in df.columns]
        df = df[cols_to_keep]
        
        # Handle missing values
        df = df.fillna(df.mean(numeric_only=True))
        
        return df
    
    def calculate_park_metrics(self, wait_times_df: pd.DataFrame) -> Dict:
        """
        Calculate various park performance metrics.
        Args:
            wait_times_df: Wait times DataFrame
        Returns:
            Dict: Dictionary containing calculated metrics
        """
        if wait_times_df.empty:
            return {}
        
        metrics = {
            'average_wait_time': wait_times_df['wait_time'].mean(),
            'max_wait_time': wait_times_df['wait_time'].max(),
            'operating_percentage': wait_times_df['is_operating'].mean() * 100,
            'busiest_hour': wait_times_df.groupby('hour')['wait_time'].mean().idxmax(),
            'busiest_attractions': wait_times_df.groupby('attraction_name')['wait_time'].mean().nlargest(5).to_dict()
        }
        
        return metrics
    
    def merge_data(self, wait_times_df: pd.DataFrame, weather_df: pd.DataFrame) -> pd.DataFrame:
        """
        Merge wait times and weather data.
        Args:
            wait_times_df: Wait times DataFrame
            weather_df: Weather DataFrame
        Returns:
            pd.DataFrame: Merged data
        """
        if wait_times_df.empty or weather_df.empty:
            return pd.DataFrame()
        
        # Convert timestamps to compatible format
        wait_times_df['date'] = wait_times_df['timestamp'].dt.date
        wait_times_df['hour'] = wait_times_df['timestamp'].dt.hour
        
        # Merge on date, hour, and park
        merged_df = pd.merge(
            wait_times_df,
            weather_df,
            on=['date', 'hour', 'park'],
            how='left'
        )
        
        return merged_df
    
    def save_processed_data(self, df: pd.DataFrame, filename: str) -> None:
        """
        Save processed data to CSV file.
        Args:
            df: DataFrame to save
            filename: Output filename
        """
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, filename)
        df.to_csv(output_path, index=False)
        logger.info(f"Processed data saved to {output_path}")

def main():
    """Main function to run data processing."""
    processor = ThemeParkDataProcessor()
    
    # Process data for the past week
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    # Load data
    wait_times_df, weather_df = processor.load_data(start_date, end_date)
    
    # Clean data
    wait_times_df = processor.clean_wait_times(wait_times_df)
    weather_df = processor.clean_weather(weather_df)
    
    # Merge data
    merged_df = processor.merge_data(wait_times_df, weather_df)
    
    # Calculate metrics
    metrics = processor.calculate_park_metrics(wait_times_df)
    logger.info(f"Park metrics: {metrics}")
    
    # Save processed data
    processor.save_processed_data(merged_df, 'theme_park_data_processed.csv')

if __name__ == "__main__":
    main() 