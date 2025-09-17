"""
Disney Theme Park Operations Data Processor
Processes and enriches theme park operational data for analytics and machine learning
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from sklearn.preprocessing import StandardScaler, LabelEncoder
import json
import warnings

warnings.filterwarnings('ignore')

class DisneyParkDataProcessor:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.raw_path = self.base_path / 'data' / 'raw'
        self.processed_path = self.base_path / 'data' / 'processed'
        
        self.scaler = StandardScaler()
        self.label_encoders = {}
    
    def load_raw_data(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Load raw park attractions and operational data"""
        try:
            attractions_df = pd.read_csv(self.raw_path / 'park_attractions.csv')
            operations_df = pd.read_csv(self.raw_path / 'park_operations.csv')
            
            print(f"✅ Loaded {len(attractions_df)} attractions and {len(operations_df):,} operational records")
            return attractions_df, operations_df
        except FileNotFoundError as e:
            print(f"❌ Raw data not found: {e}")
            print("Please run park_data_generator.py first.")
            return pd.DataFrame(), pd.DataFrame()
    
    def clean_operational_data(self, operations_df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate operational data"""
        print("🧹 Cleaning operational data...")
        
        # Convert date column
        operations_df['date'] = pd.to_datetime(operations_df['date'])
        
        # Handle missing values
        operations_df = operations_df.fillna({
            'avg_wait_time_minutes': operations_df['avg_wait_time_minutes'].median(),
            'guest_satisfaction_score': operations_df['guest_satisfaction_score'].median(),
            'downtime_minutes': 0,
            'revenue_generated': 0
        })
        
        # Data validation and outlier handling
        operations_df = operations_df[operations_df['total_guests'] >= 0]
        operations_df = operations_df[operations_df['avg_wait_time_minutes'] >= 0]
        operations_df = operations_df[operations_df['guest_satisfaction_score'] >= 0]
        
        # Remove extreme outliers (99th percentile)
        for col in ['avg_wait_time_minutes', 'total_guests', 'revenue_generated']:
            threshold = operations_df[col].quantile(0.99)
            operations_df = operations_df[operations_df[col] <= threshold]
        
        print(f"✅ Cleaned data: {len(operations_df):,} records remaining")
        return operations_df
    
    def engineer_operational_features(self, operations_df: pd.DataFrame) -> pd.DataFrame:
        """Engineer advanced features for operational analysis"""
        print("🔧 Engineering operational features...")
        
        # Time-based features
        operations_df['day_of_week'] = operations_df['date'].dt.day_name()
        operations_df['month'] = operations_df['date'].dt.month
        operations_df['quarter'] = operations_df['date'].dt.quarter
        operations_df['is_weekend'] = operations_df['date'].dt.weekday >= 5
        
        # Holiday and seasonal features
        operations_df['is_summer'] = operations_df['month'].isin([6, 7, 8])
        operations_df['is_holiday_season'] = operations_df['month'].isin([11, 12])
        operations_df['is_spring_break'] = ((operations_df['month'] == 3) & 
                                          (operations_df['date'].dt.day >= 15)) | \
                                         ((operations_df['month'] == 4) & 
                                          (operations_df['date'].dt.day <= 30))
        
        # Weather impact features
        operations_df['is_rain'] = operations_df['weather_condition'].isin(['Light Rain', 'Heavy Rain'])
        operations_df['is_perfect_weather'] = operations_df['weather_condition'] == 'Sunny'
        operations_df['temp_category'] = pd.cut(operations_df['temperature'], 
                                               bins=[0, 70, 80, 90, 100], 
                                               labels=['Cool', 'Mild', 'Warm', 'Hot'])
        
        # Operational efficiency metrics
        operations_df['wait_time_efficiency'] = np.where(
            operations_df['avg_wait_time_minutes'] <= 30, 'Excellent',
            np.where(operations_df['avg_wait_time_minutes'] <= 60, 'Good',
                    np.where(operations_df['avg_wait_time_minutes'] <= 90, 'Fair', 'Poor'))
        )
        
        # Revenue and performance metrics
        operations_df['revenue_per_guest'] = (operations_df['revenue_generated'] / 
                                             np.maximum(operations_df['total_guests'], 1))
        operations_df['satisfaction_category'] = pd.cut(operations_df['guest_satisfaction_score'],
                                                       bins=[0, 0.6, 0.8, 0.9, 1.0],
                                                       labels=['Poor', 'Fair', 'Good', 'Excellent'])
        
        # Capacity and demand analysis
        operations_df['demand_intensity'] = pd.cut(operations_df['capacity_utilization'],
                                                  bins=[0, 0.5, 0.8, 1.0, 2.0],
                                                  labels=['Low', 'Medium', 'High', 'Extreme'])
        
        # Lightning Lane effectiveness
        operations_df['lightning_lane_ratio'] = (operations_df['lightning_lane_guests'] / 
                                                 np.maximum(operations_df['total_guests'], 1))
        operations_df['has_lightning_lane'] = operations_df['lightning_lane_guests'] > 0
        
        print(f"✅ Engineered {operations_df.columns.size - 20} additional features")
        return operations_df
    
    def create_attraction_performance_metrics(self, operations_df: pd.DataFrame, 
                                             attractions_df: pd.DataFrame) -> pd.DataFrame:
        """Create comprehensive attraction performance metrics"""
        print("📊 Calculating attraction performance metrics...")
        
        # Merge operational data with attraction metadata
        merged_df = operations_df.merge(attractions_df, on='attraction_id', suffixes=('', '_meta'))
        
        # Calculate attraction-level aggregations
        attraction_metrics = merged_df.groupby('attraction_id').agg({
            'attraction_name': 'first',
            'park': 'first',
            'attraction_type': 'first',
            'is_signature': 'first',
            'total_guests': ['sum', 'mean', 'std'],
            'avg_wait_time_minutes': ['mean', 'max', 'std'],
            'guest_satisfaction_score': ['mean', 'std'],
            'revenue_generated': ['sum', 'mean'],
            'capacity_utilization': 'mean',
            'operational_efficiency': 'mean',
            'downtime_minutes': ['sum', 'mean']
        }).round(3)
        
        # Flatten column names
        attraction_metrics.columns = ['_'.join(col).strip() for col in attraction_metrics.columns]
        attraction_metrics = attraction_metrics.reset_index()
        
        # Calculate performance rankings
        attraction_metrics['revenue_rank'] = attraction_metrics['revenue_generated_sum'].rank(ascending=False)
        attraction_metrics['satisfaction_rank'] = attraction_metrics['guest_satisfaction_score_mean'].rank(ascending=False)
        attraction_metrics['efficiency_rank'] = attraction_metrics['operational_efficiency_mean'].rank(ascending=False)
        
        # Calculate composite performance score
        attraction_metrics['performance_score'] = (
            (attraction_metrics['guest_satisfaction_score_mean'] * 0.3) +
            (attraction_metrics['operational_efficiency_mean'] * 0.3) +
            ((1 - attraction_metrics['avg_wait_time_minutes_mean'] / 120) * 0.2) +
            (attraction_metrics['capacity_utilization_mean'] * 0.2)
        ).clip(0, 1)
        
        return attraction_metrics
    
    def create_park_operational_summary(self, operations_df: pd.DataFrame) -> pd.DataFrame:
        """Create park-level operational summary"""
        print("🏰 Creating park operational summaries...")
        
        park_summary = operations_df.groupby('park').agg({
            'park_attendance': ['mean', 'max', 'std'],
            'total_guests': ['sum', 'mean'],
            'avg_wait_time_minutes': ['mean', 'std'],
            'guest_satisfaction_score': ['mean', 'std'],
            'revenue_generated': ['sum', 'mean'],
            'capacity_utilization': 'mean',
            'operational_efficiency': 'mean'
        }).round(2)
        
        # Flatten columns
        park_summary.columns = ['_'.join(col).strip() for col in park_summary.columns]
        park_summary = park_summary.reset_index()
        
        # Calculate park rankings
        park_summary['revenue_rank'] = park_summary['revenue_generated_sum'].rank(ascending=False)
        park_summary['satisfaction_rank'] = park_summary['guest_satisfaction_score_mean'].rank(ascending=False)
        park_summary['efficiency_rank'] = park_summary['operational_efficiency_mean'].rank(ascending=False)
        
        return park_summary
    
    def create_weather_impact_analysis(self, operations_df: pd.DataFrame) -> pd.DataFrame:
        """Analyze weather impact on park operations"""
        print("🌤️ Analyzing weather impact...")
        
        weather_impact = operations_df.groupby('weather_condition').agg({
            'park_attendance': 'mean',
            'total_guests': 'mean',
            'avg_wait_time_minutes': 'mean',
            'guest_satisfaction_score': 'mean',
            'revenue_generated': 'mean',
            'capacity_utilization': 'mean'
        }).round(2)
        
        # Calculate relative impact (compared to sunny weather)
        sunny_baseline = weather_impact.loc['Sunny']
        weather_impact_relative = (weather_impact / sunny_baseline * 100).round(1)
        
        return weather_impact, weather_impact_relative
    
    def prepare_ml_features(self, operations_df: pd.DataFrame, attractions_df: pd.DataFrame) -> tuple:
        """Prepare features for machine learning models"""
        print("🤖 Preparing features for machine learning...")
        
        # Merge operational and attraction data
        ml_data = operations_df.merge(attractions_df, on='attraction_id', suffixes=('', '_attr'))
        
        # Select and engineer features for ML
        categorical_features = [
            'park', 'attraction_type', 'weather_condition', 'day_of_week',
            'temp_category', 'demand_intensity', 'lightning_lane_tier'
        ]
        
        numerical_features = [
            'park_attendance', 'temperature', 'hourly_capacity', 'popularity_score',
            'ride_duration_minutes', 'operational_cost_hourly', 'maintenance_score',
            'weather_sensitivity', 'capacity_utilization', 'lightning_lane_ratio'
        ]
        
        boolean_features = [
            'is_weekend', 'is_summer', 'is_holiday_season', 'is_rain',
            'is_signature', 'has_fastpass', 'has_lightning_lane'
        ]
        
        # Create feature matrix
        X = pd.DataFrame()
        
        # Add numerical features
        for feature in numerical_features:
            if feature in ml_data.columns:
                X[feature] = ml_data[feature].fillna(ml_data[feature].median())
        
        # Add boolean features
        for feature in boolean_features:
            if feature in ml_data.columns:
                X[feature] = ml_data[feature].astype(int)
        
        # One-hot encode categorical features
        for feature in categorical_features:
            if feature in ml_data.columns:
                dummies = pd.get_dummies(ml_data[feature], prefix=feature, drop_first=True)
                X = pd.concat([X, dummies], axis=1)
        
        # Target variables for different prediction tasks
        targets = {
            'wait_time': ml_data['avg_wait_time_minutes'].fillna(ml_data['avg_wait_time_minutes'].median()),
            'satisfaction': ml_data['guest_satisfaction_score'].fillna(ml_data['guest_satisfaction_score'].median()),
            'attendance': ml_data['total_guests'].fillna(0),
            'revenue': ml_data['revenue_generated'].fillna(0)
        }
        
        print(f"✅ Prepared {X.shape[1]} features for {len(X)} samples")
        return X, targets, ml_data
    
    def save_processed_data(self, operations_df: pd.DataFrame, attraction_metrics: pd.DataFrame,
                           park_summary: pd.DataFrame, weather_impact: pd.DataFrame):
        """Save all processed data"""
        print("💾 Saving processed data...")
        
        # Save main datasets
        operations_df.to_csv(self.processed_path / 'park_operations_processed.csv', index=False)
        attraction_metrics.to_csv(self.processed_path / 'attraction_performance_metrics.csv', index=False)
        park_summary.to_csv(self.processed_path / 'park_operational_summary.csv', index=False)
        weather_impact.to_csv(self.processed_path / 'weather_impact_analysis.csv', index=False)
        
        # Create processing summary
        summary_stats = {
            'processing_date': datetime.now().isoformat(),
            'total_operational_records': len(operations_df),
            'date_range': {
                'start': operations_df['date'].min().isoformat(),
                'end': operations_df['date'].max().isoformat(),
                'total_days': len(operations_df['date'].unique())
            },
            'parks_analyzed': operations_df['park'].nunique(),
            'attractions_analyzed': operations_df['attraction_id'].nunique(),
            'avg_daily_metrics': {
                'attendance': float(operations_df['park_attendance'].mean()),
                'wait_time': float(operations_df['avg_wait_time_minutes'].mean()),
                'satisfaction': float(operations_df['guest_satisfaction_score'].mean()),
                'revenue': float(operations_df['revenue_generated'].mean())
            }
        }
        
        with open(self.processed_path / 'processing_summary.json', 'w') as f:
            json.dump(summary_stats, f, indent=2, default=str)
        
        print("✅ All processed data saved successfully")
    
    def process_all_data(self) -> tuple:
        """Run complete data processing pipeline"""
        print("🚀 Starting Disney Theme Park Data Processing Pipeline...\n")
        
        # Load raw data
        attractions_df, operations_df = self.load_raw_data()
        if operations_df.empty:
            return None, None, None, None
        
        # Clean and process data
        operations_df = self.clean_operational_data(operations_df)
        operations_df = self.engineer_operational_features(operations_df)
        
        # Create analytical summaries
        attraction_metrics = self.create_attraction_performance_metrics(operations_df, attractions_df)
        park_summary = self.create_park_operational_summary(operations_df)
        weather_impact, weather_relative = self.create_weather_impact_analysis(operations_df)
        
        # Prepare ML features
        X, targets, ml_data = self.prepare_ml_features(operations_df, attractions_df)
        
        # Save processed data
        self.save_processed_data(operations_df, attraction_metrics, park_summary, weather_impact)
        
        print("\n🎉 Data processing completed successfully!")
        print(f"📊 Final dataset: {len(operations_df):,} operational records")
        print(f"🎢 Attraction metrics: {len(attraction_metrics)} attractions analyzed")
        print(f"🏰 Park summaries: {len(park_summary)} parks analyzed")
        
        return operations_df, attraction_metrics, park_summary, (X, targets)

if __name__ == "__main__":
    processor = DisneyParkDataProcessor()
    ops_df, attr_metrics, park_summary, ml_data = processor.process_all_data()
    
    if ops_df is not None:
        print(f"\n🎯 Key Insights:")
        print(f"• Busiest park: {ops_df.groupby('park')['total_guests'].sum().idxmax()}")
        print(f"• Average wait time: {ops_df['avg_wait_time_minutes'].mean():.1f} minutes")
        print(f"• Guest satisfaction: {ops_df['guest_satisfaction_score'].mean():.3f}")
        print(f"• Total revenue: ${ops_df['revenue_generated'].sum():,.0f}")
        print(f"• Weather impact: Rainy days reduce attendance by {(1-ops_df[ops_df['is_rain']]['total_guests'].mean()/ops_df[~ops_df['is_rain']]['total_guests'].mean())*100:.1f}%")