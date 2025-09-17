"""
Disney+ Data Processing and Feature Engineering
Cleans and enriches the raw Disney+ content data for analysis and modeling
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from sklearn.preprocessing import StandardScaler, LabelEncoder
from scipy import stats
import warnings

warnings.filterwarnings('ignore')

class DisneyPlusDataProcessor:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.raw_path = self.base_path / 'data' / 'raw'
        self.processed_path = self.base_path / 'data' / 'processed'
        
        self.scaler = StandardScaler()
        self.label_encoders = {}
    
    def load_raw_data(self) -> pd.DataFrame:
        """Load raw Disney+ content data"""
        try:
            df = pd.read_csv(self.raw_path / 'disney_plus_content.csv')
            print(f"✅ Loaded {len(df)} content records from raw data")
            return df
        except FileNotFoundError:
            print("❌ Raw data not found. Please run data_generator.py first.")
            return pd.DataFrame()
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate the dataset"""
        print("🧹 Cleaning data...")
        
        # Handle missing values
        df = df.fillna({
            'franchise': 'Independent',
            'engagement_score': df['engagement_score'].median(),
            'completion_rate': df['completion_rate'].median()
        })
        
        # Convert date columns
        df['release_date'] = pd.to_datetime(df['release_date'])
        df['disney_plus_date'] = pd.to_datetime(df['disney_plus_date'])
        
        # Data validation
        df = df[df['imdb_rating'] >= 0]
        df = df[df['duration_minutes'] > 0]
        df = df[df['total_views'] >= 0]
        
        # Remove outliers
        df = self._remove_outliers(df, ['imdb_rating', 'total_views', 'duration_minutes'])
        
        print(f"✅ Data cleaned. {len(df)} records remaining")
        return df
    
    def _remove_outliers(self, df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """Remove statistical outliers using IQR method"""
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Keep outliers for certain cases (e.g., blockbuster movies)
            if col == 'total_views':
                df = df[df[col] >= lower_bound]  # Only remove unrealistically low values
            else:
                df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        
        return df
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create new features for modeling"""
        print("🔧 Engineering features...")
        
        # Time-based features
        current_date = datetime.now()
        df['days_since_release'] = (current_date - df['release_date']).dt.days
        df['days_on_disney_plus'] = (current_date - df['disney_plus_date']).dt.days
        df['release_year'] = df['release_date'].dt.year
        df['disney_plus_year'] = df['disney_plus_date'].dt.year
        
        # Content performance metrics
        df['views_per_day'] = df['total_views'] / np.maximum(df['days_on_disney_plus'], 1)
        df['engagement_per_minute'] = df['engagement_score'] / df['duration_minutes']
        df['roi_estimate'] = df['total_views'] / (df['production_budget'] / 1000000)  # Views per million spent
        
        # Categorical encoding for modeling
        df['is_franchise'] = df['franchise'] != 'Independent'
        df['is_premium_studio'] = df['studio'].isin(['Marvel Studios', 'Pixar Animation Studios', 'Lucasfilm'])
        
        # Content age categories
        df['content_age_category'] = pd.cut(df['days_since_release'], 
                                          bins=[0, 365, 1825, 3650, float('inf')],
                                          labels=['New', 'Recent', 'Established', 'Classic'])
        
        # Performance categories
        df['performance_category'] = pd.cut(df['total_views'], 
                                          bins=[0, 500000, 2000000, 10000000, float('inf')],
                                          labels=['Low', 'Medium', 'High', 'Blockbuster'])
        
        # Genre analysis
        df['genre_count'] = df['all_genres'].str.count('\\|') + 1
        df['is_animation'] = df['primary_genre'] == 'Animation'
        df['is_family_friendly'] = df['primary_genre'].isin(['Family', 'Animation', 'Adventure'])
        
        print(f"✅ Engineered {sum('_' in col or 'is_' in col or 'category' in col for col in df.columns)} new features")
        return df
    
    def create_studio_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create studio-level performance metrics"""
        print("🏢 Analyzing studio performance...")
        
        studio_stats = df.groupby('studio').agg({
            'content_id': 'count',
            'total_views': ['mean', 'sum', 'std'],
            'imdb_rating': 'mean',
            'completion_rate': 'mean',
            'engagement_score': 'mean',
            'production_budget': 'mean',
            'roi_estimate': 'mean'
        }).round(3)
        
        # Flatten column names
        studio_stats.columns = ['_'.join(col).strip() for col in studio_stats.columns]
        studio_stats = studio_stats.reset_index()
        
        # Rename columns for clarity
        studio_stats.rename(columns={
            'content_id_count': 'total_content',
            'total_views_mean': 'avg_views',
            'total_views_sum': 'total_studio_views',
            'total_views_std': 'views_std',
            'imdb_rating_mean': 'avg_rating',
            'completion_rate_mean': 'avg_completion_rate',
            'engagement_score_mean': 'avg_engagement',
            'production_budget_mean': 'avg_budget',
            'roi_estimate_mean': 'avg_roi'
        }, inplace=True)
        
        # Calculate market share
        total_views = studio_stats['total_studio_views'].sum()
        studio_stats['market_share'] = (studio_stats['total_studio_views'] / total_views * 100).round(2)
        
        return studio_stats
    
    def create_content_features_for_ml(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare features specifically for machine learning models"""
        print("🤖 Preparing ML features...")
        
        # Select relevant features for modeling
        ml_features = df.copy()
        
        # Encode categorical variables
        categorical_cols = ['studio', 'primary_genre', 'content_type', 'franchise']
        for col in categorical_cols:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
            ml_features[f'{col}_encoded'] = self.label_encoders[col].fit_transform(ml_features[col])
        
        # Select numerical features
        numerical_features = [
            'duration_minutes', 'episodes', 'seasons', 'imdb_rating',
            'completion_rate', 'engagement_score', 'production_budget',
            'days_since_release', 'days_on_disney_plus', 'genre_count',
            'views_per_day', 'engagement_per_minute', 'roi_estimate'
        ]
        
        # Add encoded categorical features
        encoded_features = [f'{col}_encoded' for col in categorical_cols]
        
        # Add boolean features
        boolean_features = [
            'is_original', 'is_franchise', 'is_premium_studio',
            'is_animation', 'is_family_friendly'
        ]
        
        # Combine all feature columns
        feature_columns = numerical_features + encoded_features + boolean_features
        
        # Create final feature matrix
        X = ml_features[feature_columns].fillna(0)
        y = ml_features['total_views']  # Target variable
        
        # Scale numerical features
        numerical_indices = list(range(len(numerical_features)))
        X_scaled = X.copy()
        X_scaled.iloc[:, numerical_indices] = self.scaler.fit_transform(X.iloc[:, numerical_indices])
        
        return X_scaled, y, feature_columns
    
    def save_processed_data(self, df: pd.DataFrame, studio_stats: pd.DataFrame):
        """Save all processed data"""
        print("💾 Saving processed data...")
        
        # Save main processed dataset
        df.to_csv(self.processed_path / 'disney_plus_content_processed.csv', index=False)
        
        # Save studio analysis
        studio_stats.to_csv(self.processed_path / 'studio_performance_analysis.csv', index=False)
        
        # Create summary statistics
        summary_stats = {
            'total_records': len(df),
            'date_range': {
                'earliest_release': df['release_date'].min().isoformat(),
                'latest_release': df['release_date'].max().isoformat()
            },
            'content_distribution': df['content_type'].value_counts().to_dict(),
            'studio_distribution': df['studio'].value_counts().to_dict(),
            'avg_metrics': {
                'rating': float(df['imdb_rating'].mean()),
                'views': int(df['total_views'].mean()),
                'completion_rate': float(df['completion_rate'].mean()),
                'engagement': float(df['engagement_score'].mean())
            }
        }
        
        import json
        with open(self.processed_path / 'processing_summary.json', 'w') as f:
            json.dump(summary_stats, f, indent=2, default=str)
        
        print("✅ All processed data saved successfully")
    
    def process_all(self) -> tuple:
        """Run the complete data processing pipeline"""
        print("🚀 Starting Disney+ data processing pipeline...\n")
        
        # Load raw data
        df = self.load_raw_data()
        if df.empty:
            return None, None
        
        # Process data
        df = self.clean_data(df)
        df = self.engineer_features(df)
        
        # Create analyses
        studio_stats = self.create_studio_analysis(df)
        X, y, features = self.create_content_features_for_ml(df)
        
        # Save results
        self.save_processed_data(df, studio_stats)
        
        print("\n🎉 Data processing completed successfully!")
        print(f"📈 Final dataset: {len(df)} records with {len(df.columns)} features")
        print(f"🏢 Studio analysis: {len(studio_stats)} studios analyzed")
        
        return df, studio_stats

if __name__ == "__main__":
    processor = DisneyPlusDataProcessor()
    df, studio_stats = processor.process_all()
    
    if df is not None:
        print("\n📊 Quick Dataset Overview:")
        print(f"Content Types: {dict(df['content_type'].value_counts())}")
        print(f"Top Studios by Content: {dict(df['studio'].value_counts().head(3))}")
        print(f"Average Rating: {df['imdb_rating'].mean():.2f}")
        print(f"Total Views: {df['total_views'].sum():,}")