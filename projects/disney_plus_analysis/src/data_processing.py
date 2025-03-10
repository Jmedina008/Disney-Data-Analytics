"""
Data processing script for Disney+ content analysis.
This script processes and cleans the collected data for analysis.
"""

import os
import pandas as pd
import numpy as np
from typing import Dict, List
from sklearn.preprocessing import LabelEncoder
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DisneyPlusDataProcessor:
    """Class to process and clean Disney+ content data."""
    
    def __init__(self):
        """Initialize the data processor."""
        self.label_encoders = {}
        
    def load_data(self, filename: str) -> pd.DataFrame:
        """
        Load data from CSV file.
        Args:
            filename: Input filename
        Returns:
            pd.DataFrame: Loaded data
        """
        input_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', filename)
        return pd.read_csv(input_path)
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the data by handling missing values and incorrect data types.
        Args:
            df: Input DataFrame
        Returns:
            pd.DataFrame: Cleaned DataFrame
        """
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        df['overview'] = df['overview'].fillna('')
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
        
        # Extract year from release_date
        df['release_year'] = df['release_date'].dt.year
        
        return df
    
    def encode_categorical_features(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Encode categorical features using LabelEncoder.
        Args:
            df: Input DataFrame
            columns: List of columns to encode
        Returns:
            pd.DataFrame: DataFrame with encoded features
        """
        df_encoded = df.copy()
        
        for col in columns:
            if col in df.columns:
                le = LabelEncoder()
                df_encoded[f'{col}_encoded'] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
                
        return df_encoded
    
    def calculate_content_metrics(self, df: pd.DataFrame) -> Dict:
        """
        Calculate various content metrics.
        Args:
            df: Input DataFrame
        Returns:
            Dict: Dictionary containing calculated metrics
        """
        metrics = {
            'total_content': len(df),
            'avg_rating': df['vote_average'].mean(),
            'content_by_year': df['release_year'].value_counts().to_dict(),
            'popular_genres': df['genre_ids'].value_counts().head(5).to_dict()
        }
        
        return metrics
    
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
    processor = DisneyPlusDataProcessor()
    
    # Load raw data
    raw_data = processor.load_data('disney_plus_content.csv')
    
    # Process data
    cleaned_data = processor.clean_data(raw_data)
    
    # Encode categorical features
    categorical_columns = ['original_language', 'genre_ids']
    processed_data = processor.encode_categorical_features(cleaned_data, categorical_columns)
    
    # Calculate metrics
    metrics = processor.calculate_content_metrics(processed_data)
    logger.info(f"Content metrics: {metrics}")
    
    # Save processed data
    processor.save_processed_data(processed_data, 'disney_plus_content_processed.csv')

if __name__ == "__main__":
    main() 