"""
Advanced analytics module for Disney portfolio projects.
Implements sophisticated analysis techniques for content, theme parks, and box office data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Dict, List, Optional, Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
from textblob import TextBlob
import plotly.graph_objects as go
import plotly.express as px
import json

class DataAnalyzer:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.processed_path = self.base_path / 'data' / 'processed'
        self.analytics_path = self.base_path / 'data' / 'analytics'
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def analyze_disney_plus_content(self) -> Dict:
        """Analyze Disney+ content trends and patterns"""
        try:
            # Load processed data
            df = pd.read_parquet(self.processed_path / 'disney_plus' / 'content_latest.parquet')
            
            # Genre analysis
            genre_trends = self._analyze_genre_trends(df)
            
            # Content release patterns
            release_patterns = self._analyze_release_patterns(df)
            
            # Rating analysis
            rating_analysis = self._analyze_ratings(df)
            
            # Content clustering
            content_clusters = self._cluster_content(df)
            
            results = {
                'genre_trends': genre_trends,
                'release_patterns': release_patterns,
                'rating_analysis': rating_analysis,
                'content_clusters': content_clusters
            }
            
            # Save results
            self._save_analysis_results('disney_plus', results)
            return results
            
        except Exception as e:
            self.logger.error(f"Error analyzing Disney+ content: {str(e)}")
            return {}

    def analyze_theme_park_data(self) -> Dict:
        """Analyze theme park wait times and patterns"""
        try:
            results = {}
            for park in ['WDW_MK', 'WDW_EP', 'WDW_HS', 'WDW_AK']:
                df = pd.read_parquet(self.processed_path / 'theme_parks' / f'{park}_latest.parquet')
                
                # Wait time patterns
                wait_patterns = self._analyze_wait_patterns(df)
                
                # Peak time analysis
                peak_times = self._analyze_peak_times(df)
                
                # Ride popularity analysis
                popularity = self._analyze_ride_popularity(df)
                
                # Wait time forecasting
                forecasts = self._forecast_wait_times(df)
                
                results[park] = {
                    'wait_patterns': wait_patterns,
                    'peak_times': peak_times,
                    'popularity': popularity,
                    'forecasts': forecasts
                }
            
            # Save results
            self._save_analysis_results('theme_parks', results)
            return results
            
        except Exception as e:
            self.logger.error(f"Error analyzing theme park data: {str(e)}")
            return {}

    def analyze_box_office_performance(self) -> Dict:
        """Analyze box office performance and trends"""
        try:
            df = pd.read_parquet(self.processed_path / 'entertainment' / 'box_office_latest.parquet')
            
            # Financial analysis
            financial_metrics = self._analyze_financial_metrics(df)
            
            # Success factors
            success_factors = self._analyze_success_factors(df)
            
            # Seasonal patterns
            seasonal_trends = self._analyze_seasonal_trends(df)
            
            # Franchise analysis
            franchise_performance = self._analyze_franchises(df)
            
            results = {
                'financial_metrics': financial_metrics,
                'success_factors': success_factors,
                'seasonal_trends': seasonal_trends,
                'franchise_performance': franchise_performance
            }
            
            # Save results
            self._save_analysis_results('box_office', results)
            return results
            
        except Exception as e:
            self.logger.error(f"Error analyzing box office data: {str(e)}")
            return {}

    def _analyze_genre_trends(self, df: pd.DataFrame) -> Dict:
        """Analyze content genre trends over time"""
        genre_df = df.explode('genre_list')
        genre_trends = genre_df.groupby(['release_year', 'genre_list']).size().unstack(fill_value=0)
        
        # Calculate genre growth rates
        growth_rates = (genre_trends.iloc[-1] - genre_trends.iloc[0]) / genre_trends.iloc[0]
        
        return {
            'trends': genre_trends.to_dict(),
            'growth_rates': growth_rates.to_dict()
        }

    def _analyze_wait_patterns(self, df: pd.DataFrame) -> Dict:
        """Analyze wait time patterns"""
        # Hourly patterns
        hourly_avg = df.groupby('hour')['wait_time'].mean()
        
        # Day of week patterns
        daily_avg = df.groupby('day_of_week')['wait_time'].mean()
        
        # Weekend vs weekday
        weekend_comparison = df.groupby('is_weekend')['wait_time'].agg(['mean', 'std'])
        
        return {
            'hourly_patterns': hourly_avg.to_dict(),
            'daily_patterns': daily_avg.to_dict(),
            'weekend_comparison': weekend_comparison.to_dict()
        }

    def _analyze_financial_metrics(self, df: pd.DataFrame) -> Dict:
        """Analyze financial performance metrics"""
        metrics = {
            'total_revenue': df['revenue'].sum(),
            'average_revenue': df['revenue'].mean(),
            'median_roi': df['roi'].median(),
            'profitable_ratio': (df['profit'] > 0).mean()
        }
        
        # Revenue trends by year
        yearly_revenue = df.groupby('release_year')['revenue'].sum()
        
        # ROI distribution
        roi_quartiles = df['roi'].quantile([0.25, 0.5, 0.75])
        
        return {
            'metrics': metrics,
            'yearly_revenue': yearly_revenue.to_dict(),
            'roi_distribution': roi_quartiles.to_dict()
        }

    def _forecast_wait_times(self, df: pd.DataFrame) -> Dict:
        """Forecast wait times using SARIMA model"""
        # Prepare time series data
        time_series = df.set_index('last_update')['wait_time'].resample('15T').mean()
        
        # Fit SARIMA model
        model = SARIMAX(time_series, order=(1, 1, 1), seasonal_order=(1, 1, 1, 96))
        results = model.fit()
        
        # Generate forecasts
        forecast = results.forecast(steps=96)  # 24 hours ahead
        
        return {
            'forecast': forecast.to_dict(),
            'model_params': results.params.to_dict()
        }

    def _cluster_content(self, df: pd.DataFrame) -> Dict:
        """Cluster content based on features"""
        # Prepare features for clustering
        numeric_features = ['vote_average', 'popularity']
        X = df[numeric_features].fillna(0)
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Apply K-means clustering
        kmeans = KMeans(n_clusters=5, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)
        
        # Analyze clusters
        cluster_stats = pd.DataFrame({
            'cluster': clusters,
            'title': df['title']
        }).groupby('cluster').agg(['count'])
        
        return {
            'cluster_assignments': dict(enumerate(clusters)),
            'cluster_stats': cluster_stats.to_dict()
        }

    def _save_analysis_results(self, category: str, results: Dict):
        """Save analysis results to file"""
        output_dir = self.analytics_path / category
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f'analysis_results.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

if __name__ == "__main__":
    analyzer = DataAnalyzer()
    analyzer.analyze_disney_plus_content()
    analyzer.analyze_theme_park_data()
    analyzer.analyze_box_office_performance() 