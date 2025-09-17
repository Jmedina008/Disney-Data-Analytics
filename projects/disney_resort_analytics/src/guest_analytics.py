"""
Guest Analytics Engine

Started as simple guest clustering but turned into a full ML pipeline.
The feature engineering section got pretty complex - should refactor eventually.

TODO: satisfaction model could use better features
TODO: the recommendation logic is pretty basic
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
import warnings

# ML Libraries
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, mean_absolute_error, r2_score
import joblib

warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GuestAnalyticsEngine:
    """Main analytics class - does clustering, ML models, recommendations
    
    This got pretty big, maybe split the ML stuff into separate class later
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.data_path = self.base_path / 'data'
        self.raw_path = self.data_path / 'raw'
        self.processed_path = self.data_path / 'processed'
        self.models_path = self.base_path / 'models'
        
        # Create directories
        self.models_path.mkdir(exist_ok=True)
        self.processed_path.mkdir(exist_ok=True)
        
        # Initialize models and scalers
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        
        # TODO: experiment with different clustering algorithms
        # self.clustering_methods = ['kmeans', 'dbscan', 'hierarchical']  # not implemented yet
        
    def load_resort_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Load all resort operational data"""
        try:
            guests = pd.read_csv(self.raw_path / 'guest_profiles.csv')
            bookings = pd.read_csv(self.raw_path / 'resort_bookings.csv')
            dining = pd.read_csv(self.raw_path / 'dining_reservations.csv')
            amenities = pd.read_csv(self.raw_path / 'amenity_usage.csv')
            
            # Quick data check
            logger.info(f"✅ Loaded resort data: {len(guests)} guests, {len(bookings)} bookings")
            # print(f"DEBUG: Columns in bookings: {list(bookings.columns[:5])}...")  # debug
            return guests, bookings, dining, amenities
            
        except FileNotFoundError as e:
            logger.error(f"❌ Data files not found: {e}")
            raise
    
    def create_guest_analytics_dataset(self, guests: pd.DataFrame, bookings: pd.DataFrame, 
                                     dining: pd.DataFrame, amenities: pd.DataFrame) -> pd.DataFrame:
        """Create analytics dataset - lots of feature engineering here"""
        logger.info("🔧 Creating guest analytics dataset...")
        # TODO: this method is doing too much, should break it up
        
        # Merge guest data with bookings
        guest_bookings = guests.merge(bookings, on='guest_id', how='inner')
        # print(f"DEBUG: After merge got {len(guest_bookings)} records")  # left for debugging
        
        # Calculate dining and amenity metrics - these methods got complex
        dining_metrics = self._calculate_dining_metrics(dining)
        amenity_metrics = self._calculate_amenity_metrics(amenities)
        
        # Merge everything together
        analytics_df = guest_bookings.merge(dining_metrics, on='guest_id', how='left')
        analytics_df = analytics_df.merge(amenity_metrics, on='guest_id', how='left')
        
        # Fill missing values - probably should be more sophisticated
        analytics_df = analytics_df.fillna(0)  # simple fill for now
        
        # Engineer additional features
        analytics_df = self._engineer_guest_features(analytics_df)
        
        logger.info(f"✅ Created analytics dataset: {len(analytics_df)} records with {len(analytics_df.columns)} features")
        return analytics_df
    
    def _calculate_dining_metrics(self, dining: pd.DataFrame) -> pd.DataFrame:
        """Calculate guest dining behavior metrics"""
        dining_metrics = dining.groupby('guest_id').agg({
            'estimated_cost': ['sum', 'mean', 'count'],
            'party_size': 'mean'
        }).reset_index()
        
        # Flatten column names
        dining_metrics.columns = ['guest_id', 'total_dining_spend', 'avg_meal_cost', 
                                'total_dining_occasions', 'avg_dining_party_size']
        
        # Calculate dining patterns
        dining_by_time = dining.pivot_table(
            values='estimated_cost', index='guest_id', columns='meal_time', 
            aggfunc='sum', fill_value=0
        ).reset_index()
        
        # Merge dining patterns
        if not dining_by_time.empty:
            dining_metrics = dining_metrics.merge(dining_by_time, on='guest_id', how='left')
        
        return dining_metrics.fillna(0)
    
    def _calculate_amenity_metrics(self, amenities: pd.DataFrame) -> pd.DataFrame:
        """Calculate guest amenity usage patterns"""
        amenity_metrics = amenities.groupby('guest_id').agg({
            'cost': ['sum', 'mean', 'count'],
            'duration_minutes': ['sum', 'mean'],
            'satisfaction_impact': 'mean'
        }).reset_index()
        
        # Flatten column names
        amenity_metrics.columns = ['guest_id', 'total_amenity_spend', 'avg_amenity_cost',
                                 'total_amenity_usage', 'total_amenity_time', 
                                 'avg_amenity_duration', 'avg_satisfaction_impact']
        
        # Calculate amenity preferences
        amenity_usage = amenities.pivot_table(
            values='cost', index='guest_id', columns='amenity_type',
            aggfunc='sum', fill_value=0
        ).reset_index()
        
        # Add amenity preference columns
        for col in amenity_usage.columns:
            if col != 'guest_id':
                amenity_usage[f'{col}_usage'] = (amenity_usage[col] > 0).astype(int)
        
        # Merge amenity data
        if not amenity_usage.empty:
            amenity_metrics = amenity_metrics.merge(amenity_usage, on='guest_id', how='left')
        
        return amenity_metrics.fillna(0)
    
    def _engineer_guest_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer advanced guest behavior features"""
        
        # Convert date columns
        df['booking_date'] = pd.to_datetime(df['booking_date'])
        df['checkin_date'] = pd.to_datetime(df['checkin_date'])
        df['checkout_date'] = pd.to_datetime(df['checkout_date'])
        
        # Temporal features
        df['booking_month'] = df['booking_date'].dt.month
        df['checkin_month'] = df['checkin_date'].dt.month
        df['checkin_day_of_week'] = df['checkin_date'].dt.dayofweek
        df['is_weekend_checkin'] = (df['checkin_day_of_week'] >= 5).astype(int)
        
        # Financial behavior features
        df['spend_per_night'] = df['total_cost'] / df['stay_length']
        df['spend_per_person'] = df['total_cost'] / df['party_size']
        df['total_spend'] = df['total_cost'] + df.get('total_dining_spend', 0) + df.get('total_amenity_spend', 0)
        df['dining_ratio'] = df.get('total_dining_spend', 0) / (df['total_spend'] + 1)  # Avoid division by zero
        df['amenity_ratio'] = df.get('total_amenity_spend', 0) / (df['total_spend'] + 1)
        
        # Loyalty and experience features
        df['loyalty_score'] = df['loyalty_tier'].map({
            'None': 0, 'Silver': 1, 'Gold': 2, 'Platinum': 3
        }).fillna(0)
        
        df['experience_level'] = np.where(df['previous_visits'] == 0, 'First_Time',
                                np.where(df['previous_visits'] <= 2, 'Occasional', 
                                np.where(df['previous_visits'] <= 5, 'Regular', 'Frequent')))
        
        # Booking behavior features
        df['booking_lead_time_category'] = np.where(df['days_advance_booked'] <= 14, 'Last_Minute',
                                          np.where(df['days_advance_booked'] <= 60, 'Moderate',
                                          np.where(df['days_advance_booked'] <= 180, 'Early', 'Very_Early')))
        
        # Resort preference features
        df['resort_category'] = df['resort_name'].map({
            'Grand Floridian': 'Deluxe_Villa', 'Polynesian': 'Deluxe', 'Contemporary': 'Deluxe',
            'Wilderness Lodge': 'Deluxe', 'Beach Club': 'Deluxe', 'Coronado Springs': 'Moderate',
            'Port Orleans French Quarter': 'Moderate', 'Pop Century': 'Value', 'All Star Sports': 'Value'
        })
        
        # Special occasion features
        df['has_celebration'] = (df['celebration'].notna() & (df['celebration'] != 'None')).astype(int)
        df['celebration_type'] = df['celebration'].fillna('None')
        
        # Calculate guest value score (combination of spend, loyalty, and frequency)
        df['guest_value_score'] = (
            (df['total_spend'] / df['total_spend'].max()) * 0.4 +
            (df['loyalty_score'] / 3) * 0.3 +
            (np.minimum(df['previous_visits'], 10) / 10) * 0.3
        )
        
        return df
    
    # def _experimental_feature_selection(self, df):
    #     """Trying different feature selection methods - WIP"""
    #     # TODO: implement recursive feature elimination
    #     # from sklearn.feature_selection import RFE
    #     # rfe = RFE(RandomForestClassifier(), n_features_to_select=10)
    #     pass
    
    def perform_guest_segmentation(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Perform advanced guest segmentation using clustering"""
        logger.info("👥 Performing guest segmentation analysis...")
        
        # Select features for clustering
        clustering_features = [
            'lead_guest_age', 'party_size', 'stay_length', 'total_spend',
            'spend_per_night', 'loyalty_score', 'previous_visits',
            'dining_ratio', 'amenity_ratio', 'guest_value_score'
        ]
        
        # Prepare data for clustering
        X_cluster = df[clustering_features].fillna(0)
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_cluster)
        
        # Determine optimal number of clusters using elbow method
        inertias = []
        K_range = range(2, 11)
        for k in K_range:
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(X_scaled)
            inertias.append(kmeans.inertia_)
        
        # Choose optimal k (simplified - in practice, use elbow method)
        optimal_k = 6  # Based on business understanding
        
        # Perform clustering
        kmeans = KMeans(n_clusters=optimal_k, random_state=42)
        df['guest_cluster'] = kmeans.fit_predict(X_scaled)
        
        # Analyze clusters
        cluster_analysis = self._analyze_guest_clusters(df, clustering_features)
        
        # Save clustering model
        self.models['guest_segmentation'] = kmeans
        self.scalers['guest_segmentation'] = scaler
        
        # Save models
        joblib.dump(kmeans, self.models_path / 'guest_segmentation_model.pkl')
        joblib.dump(scaler, self.models_path / 'guest_segmentation_scaler.pkl')
        
        logger.info(f"✅ Guest segmentation complete: {optimal_k} clusters identified")
        return df, cluster_analysis
    
    def _analyze_guest_clusters(self, df: pd.DataFrame, features: List[str]) -> Dict:
        """Analyze characteristics of each guest cluster"""
        
        cluster_profiles = {}
        
        for cluster_id in sorted(df['guest_cluster'].unique()):
            cluster_data = df[df['guest_cluster'] == cluster_id]
            
            # Calculate cluster characteristics
            profile = {
                'cluster_id': int(cluster_id),
                'size': len(cluster_data),
                'percentage': round(len(cluster_data) / len(df) * 100, 1),
                'characteristics': {},
                'top_segments': cluster_data['segment'].value_counts().head(3).to_dict(),
                'preferred_resorts': cluster_data['resort_name'].value_counts().head(3).to_dict(),
                'average_metrics': {}
            }
            
            # Calculate average metrics for each feature
            for feature in features:
                profile['average_metrics'][feature] = round(cluster_data[feature].mean(), 2)
            
            # Determine cluster personality
            profile['cluster_name'] = self._assign_cluster_name(profile['average_metrics'])
            
            cluster_profiles[f'cluster_{cluster_id}'] = profile
        
        return cluster_profiles
    
    def _assign_cluster_name(self, metrics: Dict) -> str:
        """Assign descriptive names to clusters based on characteristics"""
        
        spend = metrics.get('total_spend', 0)
        loyalty = metrics.get('loyalty_score', 0)
        stay_length = metrics.get('stay_length', 0)
        party_size = metrics.get('party_size', 0)
        
        if spend > 8000 and loyalty >= 2:
            return "VIP Luxury Guests"
        elif spend > 5000 and stay_length > 7:
            return "Extended Stay Enthusiasts"
        elif party_size > 5:
            return "Large Family Groups"
        elif stay_length <= 3 and spend < 2000:
            return "Quick Visit Budget Guests"
        elif loyalty >= 1 and spend > 3000:
            return "Loyal Regular Visitors"
        else:
            return "Balanced Experience Seekers"
    
    def build_satisfaction_predictor(self, df: pd.DataFrame) -> Dict:
        """Build ML model to predict guest satisfaction"""
        logger.info("😊 Building guest satisfaction prediction model...")
        
        # Create satisfaction score based on multiple factors
        df['satisfaction_score'] = self._calculate_satisfaction_score(df)
        
        # Create satisfaction categories
        df['satisfaction_category'] = pd.cut(df['satisfaction_score'], 
                                           bins=[0, 0.6, 0.8, 1.0],
                                           labels=['Dissatisfied', 'Satisfied', 'Highly_Satisfied'])
        
        # Select features for prediction
        prediction_features = [
            'lead_guest_age', 'party_size', 'stay_length', 'spend_per_night',
            'loyalty_score', 'previous_visits', 'days_advance_booked',
            'seasonal_multiplier', 'is_weekend_checkin', 'has_celebration',
            'guest_cluster'
        ]
        
        # Prepare data
        X = df[prediction_features].fillna(0)
        y = df['satisfaction_category'].fillna('Satisfied')
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test)
        accuracy = model.score(X_test, y_test)
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': prediction_features,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        # Save model
        self.models['satisfaction_predictor'] = model
        joblib.dump(model, self.models_path / 'satisfaction_predictor.pkl')
        
        model_metrics = {
            'accuracy': round(accuracy, 3),
            'feature_importance': feature_importance.head(10).to_dict('records'),
            'model_type': 'Random Forest Classifier',
            'training_samples': len(X_train)
        }
        
        logger.info(f"✅ Satisfaction predictor built: {accuracy:.1%} accuracy")
        return model_metrics
    
    def _calculate_satisfaction_score(self, df: pd.DataFrame) -> pd.Series:
        """Calculate synthetic satisfaction score based on guest experience factors"""
        
        # Base satisfaction
        satisfaction = 0.7
        
        # Adjust based on spending vs expectations
        spend_ratio = df['total_spend'] / (df['annual_budget'] * 0.25)  # Assume 25% of annual budget per trip
        satisfaction += np.where(spend_ratio < 0.5, 0.1,  # Good value
                               np.where(spend_ratio > 1.5, -0.2, 0))  # Overspent
        
        # Loyalty tier benefits
        satisfaction += df['loyalty_score'] * 0.05
        
        # Special celebrations
        satisfaction += df['has_celebration'] * 0.1
        
        # Experience level (first-timers might have higher satisfaction)
        satisfaction += np.where(df['previous_visits'] == 0, 0.05, 0)
        
        # Resort category satisfaction
        resort_satisfaction = {
            'Deluxe_Villa': 0.1, 'Deluxe': 0.05, 'Moderate': 0, 'Value': -0.05
        }
        satisfaction += df['resort_category'].map(resort_satisfaction).fillna(0)
        
        # Random variation
        satisfaction += np.random.normal(0, 0.1, len(df))
        
        # Ensure bounds
        satisfaction = np.clip(satisfaction, 0.1, 1.0)
        
        return satisfaction
    
    def build_spending_predictor(self, df: pd.DataFrame) -> Dict:
        """Build model to predict guest spending patterns"""
        logger.info("💰 Building guest spending prediction model...")
        
        # Select features for spending prediction
        spending_features = [
            'lead_guest_age', 'party_size', 'stay_length', 'loyalty_score',
            'previous_visits', 'days_advance_booked', 'seasonal_multiplier',
            'guest_cluster', 'has_celebration'
        ]
        
        # Prepare data
        X = df[spending_features].fillna(0)
        y = df['total_spend']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test_scaled)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': spending_features,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        # Save model and scaler
        self.models['spending_predictor'] = model
        self.scalers['spending_predictor'] = scaler
        
        joblib.dump(model, self.models_path / 'spending_predictor.pkl')
        joblib.dump(scaler, self.models_path / 'spending_predictor_scaler.pkl')
        
        model_metrics = {
            'mae': round(mae, 2),
            'r2_score': round(r2, 3),
            'feature_importance': feature_importance.head(10).to_dict('records'),
            'model_type': 'Gradient Boosting Regressor',
            'training_samples': len(X_train)
        }
        
        logger.info(f"✅ Spending predictor built: R² = {r2:.3f}, MAE = ${mae:.0f}")
        return model_metrics
    
    def generate_guest_recommendations(self, df: pd.DataFrame, guest_id: int) -> Dict:
        """Generate personalized recommendations for a specific guest"""
        
        guest_data = df[df['guest_id'] == guest_id].iloc[0]
        cluster_id = guest_data['guest_cluster']
        
        # Find similar guests in same cluster
        similar_guests = df[df['guest_cluster'] == cluster_id]
        
        # Generate recommendations
        recommendations = {
            'guest_id': guest_id,
            'cluster': int(cluster_id),
            'recommendations': {
                'resort_suggestions': self._get_resort_recommendations(similar_guests, guest_data),
                'dining_suggestions': self._get_dining_recommendations(similar_guests, guest_data),
                'amenity_suggestions': self._get_amenity_recommendations(similar_guests, guest_data),
                'experience_optimization': self._get_experience_recommendations(guest_data)
            }
        }
        
        return recommendations
    
    def _get_resort_recommendations(self, similar_guests: pd.DataFrame, guest_data: pd.Series) -> List[Dict]:
        """Get resort recommendations based on similar guests"""
        popular_resorts = similar_guests['resort_name'].value_counts().head(3)
        
        recommendations = []
        for resort, count in popular_resorts.items():
            if resort != guest_data.get('resort_name'):  # Don't recommend current resort
                recommendations.append({
                    'resort': resort,
                    'popularity_score': round(count / len(similar_guests), 2),
                    'reason': f'Popular with {count} similar guests in your segment'
                })
        
        return recommendations
    
    def _get_dining_recommendations(self, similar_guests: pd.DataFrame, guest_data: pd.Series) -> List[str]:
        """Get dining recommendations based on guest preferences and similar guests"""
        
        # Based on guest segment preferences
        segment_dining = {
            'Young Couples': ['Fine dining restaurants', 'Romantic atmosphere venues', 'Wine bars'],
            'Families with Toddlers': ['Character dining', 'Buffet restaurants', 'Kid-friendly menus'],
            'Families with Teens': ['Quick service', 'International cuisine', 'Late night dining'],
            'Multi-Generation': ['Large table restaurants', 'Varied menu options', 'Accessible venues'],
            'Empty Nesters': ['Signature restaurants', 'Cultural cuisine', 'Wine experiences'],
            'Business Travelers': ['Quick service', 'Room service', 'Grab-and-go options'],
            'International Families': ['Cultural dining', 'Dietary accommodations', 'Authentic experiences']
        }
        
        return segment_dining.get(guest_data.get('segment', ''), ['Popular resort restaurants'])
    
    def _get_amenity_recommendations(self, similar_guests: pd.DataFrame, guest_data: pd.Series) -> List[str]:
        """Get amenity recommendations based on guest profile"""
        
        recommendations = []
        
        # Based on guest characteristics
        if guest_data.get('has_celebration', 0):
            recommendations.append('Spa services for celebration enhancement')
        
        if guest_data.get('party_size', 0) > 4:
            recommendations.append('Group activities and recreational facilities')
        
        if guest_data.get('loyalty_score', 0) >= 2:
            recommendations.append('Exclusive amenities and concierge services')
        
        if guest_data.get('stay_length', 0) > 5:
            recommendations.append('Extended stay amenities and relaxation services')
        
        return recommendations if recommendations else ['Popular resort amenities']
    
    def _get_experience_recommendations(self, guest_data: pd.Series) -> List[str]:
        """Get overall experience optimization recommendations"""
        
        recommendations = []
        
        # Based on booking patterns
        if guest_data.get('days_advance_booked', 0) < 30:
            recommendations.append('Consider booking dining reservations early for better availability')
        
        # Based on spending patterns
        spend_per_night = guest_data.get('spend_per_night', 0)
        if spend_per_night > 500:
            recommendations.append('Upgrade to concierge level for enhanced service')
        elif spend_per_night < 200:
            recommendations.append('Look for special offers and package deals')
        
        # Based on loyalty
        if guest_data.get('loyalty_score', 0) == 0:
            recommendations.append('Consider joining Disney loyalty program for benefits')
        
        return recommendations
    
    def save_analytics_results(self, df: pd.DataFrame, cluster_analysis: Dict, 
                             satisfaction_metrics: Dict, spending_metrics: Dict):
        """Save all analytics results"""
        try:
            # Save processed dataset
            df.to_csv(self.processed_path / 'guest_analytics_dataset.csv', index=False)
            
            # Save analysis results
            analytics_summary = {
                'generation_date': datetime.now().isoformat(),
                'total_guests_analyzed': len(df),
                'guest_segmentation': cluster_analysis,
                'satisfaction_model_performance': satisfaction_metrics,
                'spending_model_performance': spending_metrics,
                'key_insights': self._generate_key_insights(df, cluster_analysis)
            }
            
            with open(self.processed_path / 'analytics_summary.json', 'w') as f:
                json.dump(analytics_summary, f, indent=2, default=str)
            
            logger.info("✅ Analytics results saved successfully")
            
        except Exception as e:
            logger.error(f"❌ Error saving analytics results: {e}")
            raise
    
    def _generate_key_insights(self, df: pd.DataFrame, cluster_analysis: Dict) -> List[str]:
        """Generate key business insights from the analysis"""
        
        insights = []
        
        # Revenue insights
        total_revenue = df['total_spend'].sum()
        avg_spend = df['total_spend'].mean()
        insights.append(f"Total analyzed revenue: ${total_revenue:,.0f} across {len(df)} bookings")
        insights.append(f"Average guest spending: ${avg_spend:,.0f} per stay")
        
        # Segmentation insights
        largest_segment = max(cluster_analysis.keys(), 
                            key=lambda x: cluster_analysis[x]['size'])
        insights.append(f"Largest guest segment: {cluster_analysis[largest_segment]['cluster_name']} "
                       f"({cluster_analysis[largest_segment]['percentage']}% of guests)")
        
        # Loyalty insights
        loyalty_distribution = df['loyalty_tier'].value_counts(normalize=True)
        if 'None' in loyalty_distribution.index and loyalty_distribution['None'] > 0.5:
            insights.append("Opportunity: Over 50% of guests are not in loyalty program")
        
        # Satisfaction insights
        if 'satisfaction_score' in df.columns:
            avg_satisfaction = df['satisfaction_score'].mean()
            insights.append(f"Average guest satisfaction score: {avg_satisfaction:.2f}/1.0")
        
        return insights

def main():
    """Run comprehensive guest analytics pipeline"""
    engine = GuestAnalyticsEngine()
    
    print("👥 Starting Disney Resort Guest Analytics...")
    
    try:
        # Load data
        guests, bookings, dining, amenities = engine.load_resort_data()
        
        # Create analytics dataset
        analytics_df = engine.create_guest_analytics_dataset(guests, bookings, dining, amenities)
        
        # Perform guest segmentation
        analytics_df, cluster_analysis = engine.perform_guest_segmentation(analytics_df)
        
        # Build predictive models
        satisfaction_metrics = engine.build_satisfaction_predictor(analytics_df)
        spending_metrics = engine.build_spending_predictor(analytics_df)
        
        # Save results
        engine.save_analytics_results(analytics_df, cluster_analysis, 
                                    satisfaction_metrics, spending_metrics)
        
        # Generate sample recommendations
        sample_guest_id = analytics_df['guest_id'].iloc[0]
        recommendations = engine.generate_guest_recommendations(analytics_df, sample_guest_id)
        
        print("\n✅ Guest Analytics Pipeline Complete!")
        print(f"📊 Analyzed {len(analytics_df)} guest experiences")
        print(f"👥 Identified {len(cluster_analysis)} distinct guest segments")
        print(f"😊 Satisfaction model accuracy: {satisfaction_metrics['accuracy']:.1%}")
        print(f"💰 Spending model R²: {spending_metrics['r2_score']:.3f}")
        print(f"🎯 Sample recommendations generated for guest {sample_guest_id}")
        
    except Exception as e:
        logger.error(f"❌ Analytics pipeline failed: {e}")
        raise

if __name__ == "__main__":
    main()