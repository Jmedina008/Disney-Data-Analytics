"""
Process theme park wait times and weather data.
This script combines wait time data with weather conditions and generates predictions.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import logging
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_wait_times(file_path: str) -> pd.DataFrame:
    """Load wait times data from CSV file."""
    try:
        df = pd.read_csv(file_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        logging.error(f"Error loading wait times data: {e}")
        return pd.DataFrame()

def load_weather_data(file_path: str) -> pd.DataFrame:
    """Load weather data from CSV file."""
    try:
        df = pd.read_csv(file_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        logging.error(f"Error loading weather data: {e}")
        return pd.DataFrame()

def merge_data(wait_times_df: pd.DataFrame, weather_df: pd.DataFrame) -> pd.DataFrame:
    """Merge wait times and weather data based on timestamp."""
    try:
        merged_df = pd.merge_asof(
            wait_times_df.sort_values('timestamp'),
            weather_df.sort_values('timestamp'),
            on='timestamp',
            tolerance=pd.Timedelta('1H')
        )
        return merged_df
    except Exception as e:
        logging.error(f"Error merging data: {e}")
        return pd.DataFrame()

def prepare_features(df: pd.DataFrame) -> tuple:
    """Prepare features for wait time prediction model."""
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    df['month'] = df['timestamp'].dt.month
    
    feature_columns = [
        'hour', 'day_of_week', 'is_weekend', 'month',
        'temperature', 'humidity', 'precipitation_probability'
    ]
    
    return df[feature_columns], df['wait_time']

def train_model(X: pd.DataFrame, y: pd.Series) -> tuple:
    """Train a random forest model for wait time prediction."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    metrics = {
        'mse': mean_squared_error(y_test, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
        'r2': r2_score(y_test, y_pred)
    }
    
    return model, metrics

def main():
    # Create necessary directories
    data_dir = Path('data')
    raw_dir = data_dir / 'raw'
    processed_dir = data_dir / 'processed'
    models_dir = data_dir / 'models'
    
    for dir_path in [data_dir, raw_dir, processed_dir, models_dir]:
        dir_path.mkdir(exist_ok=True)
    
    # Load data
    wait_times_df = load_wait_times(raw_dir / 'wait_times.csv')
    weather_df = load_weather_data(raw_dir / 'weather_data.csv')
    
    if wait_times_df.empty or weather_df.empty:
        logging.error("Missing required data")
        return
    
    # Merge and process data
    merged_df = merge_data(wait_times_df, weather_df)
    if merged_df.empty:
        logging.error("Failed to merge data")
        return
    
    # Prepare features and train model
    X, y = prepare_features(merged_df)
    model, metrics = train_model(X, y)
    
    # Save processed data and model
    timestamp = datetime.now().strftime('%Y%m%d')
    merged_df.to_csv(processed_dir / f'theme_park_data_{timestamp}.csv', index=False)
    joblib.dump(model, models_dir / f'wait_time_model_{timestamp}.joblib')
    
    # Save metrics
    with open(processed_dir / f'model_metrics_{timestamp}.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    logging.info("Data processing and model training completed successfully")
    logging.info(f"Model metrics: {metrics}")

if __name__ == '__main__':
    main() 