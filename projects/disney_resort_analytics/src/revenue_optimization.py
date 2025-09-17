"""
Revenue Optimization Engine

Started with simple occupancy forecasting but grew into full revenue optimization.
The pricing models are decent but could use better demand elasticity.

TODO: Add more sophisticated time series models (ARIMA, LSTM)
TODO: The revenue scenarios are pretty basic - need better sensitivity analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime, timedelta, date
from typing import Dict, List, Tuple, Optional
import json
import warnings

# ML and optimization libraries
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy.optimize import minimize
import joblib

warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RevenueOptimizationEngine:
    """Revenue optimization - forecasting, pricing, scenario analysis
    
    This got pretty complex with all the different optimization strategies
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.data_path = self.base_path / 'data'
        self.raw_path = self.data_path / 'raw'
        self.processed_path = self.data_path / 'processed'
        self.models_path = self.base_path / 'models'
        
        # Create directories
        self.models_path.mkdir(exist_ok=True)
        
        # Initialize models and scalers
        self.models = {}
        self.scalers = {}
        
        # Experimental: trying different optimization approaches
        # self.optimization_methods = ['gradient_descent', 'genetic_algorithm']  # not ready yet
        
        # Resort capacity and characteristics
        self.resort_info = {
            'Grand Floridian': {'rooms': 847, 'base_rate': 650, 'category': 'Deluxe Villa'},
            'Polynesian': {'rooms': 492, 'base_rate': 550, 'category': 'Deluxe'},
            'Contemporary': {'rooms': 655, 'base_rate': 525, 'category': 'Deluxe'},
            'Wilderness Lodge': {'rooms': 729, 'base_rate': 475, 'category': 'Deluxe'},
            'Beach Club': {'rooms': 583, 'base_rate': 500, 'category': 'Deluxe'},
            'Coronado Springs': {'rooms': 1917, 'base_rate': 275, 'category': 'Moderate'},
            'Port Orleans French Quarter': {'rooms': 1008, 'base_rate': 225, 'category': 'Moderate'},
            'Pop Century': {'rooms': 2880, 'base_rate': 150, 'category': 'Value'},
            'All Star Sports': {'rooms': 1920, 'base_rate': 125, 'category': 'Value'}
        }
    
    def load_revenue_data(self) -> pd.DataFrame:
        """Load booking and guest data for revenue analysis"""
        try:
            bookings = pd.read_csv(self.raw_path / 'resort_bookings.csv')
            guests = pd.read_csv(self.raw_path / 'guest_profiles.csv')
            dining = pd.read_csv(self.raw_path / 'dining_reservations.csv')
            amenities = pd.read_csv(self.raw_path / 'amenity_usage.csv')
            
            # Merge for comprehensive revenue view
            revenue_df = bookings.merge(guests[['guest_id', 'segment', 'loyalty_tier', 'annual_budget']], on='guest_id')
            
            # Add ancillary revenue
            dining_revenue = dining.groupby('booking_id')['estimated_cost'].sum().reset_index()
            dining_revenue.columns = ['booking_id', 'dining_revenue']
            
            amenity_revenue = amenities.groupby('booking_id')['cost'].sum().reset_index()
            amenity_revenue.columns = ['booking_id', 'amenity_revenue']
            
            revenue_df = revenue_df.merge(dining_revenue, on='booking_id', how='left')
            revenue_df = revenue_df.merge(amenity_revenue, on='booking_id', how='left')
            
            # Fill missing values
            revenue_df['dining_revenue'] = revenue_df['dining_revenue'].fillna(0)
            revenue_df['amenity_revenue'] = revenue_df['amenity_revenue'].fillna(0)
            
            # Calculate total revenue per booking
            revenue_df['total_revenue'] = revenue_df['total_cost'] + revenue_df['dining_revenue'] + revenue_df['amenity_revenue']
            
            logger.info(f"✅ Loaded revenue data: {len(revenue_df)} bookings, ${revenue_df['total_revenue'].sum():,.0f} total revenue")
            # print(f"DEBUG: Average revenue per booking: ${revenue_df['total_revenue'].mean():.2f}")
            return revenue_df
    
    def _experimental_demand_elasticity(self, price_data):
        """Experimental demand elasticity calculation - not working yet"""
        # TODO: implement proper demand curve analysis
        # This is supposed to calculate price sensitivity but the math is tricky
        pass
        # elasticity = np.log(quantity_change) / np.log(price_change)
        # return elasticity
            
        except FileNotFoundError as e:
            logger.error(f"❌ Revenue data files not found: {e}")
            raise
    
    def prepare_occupancy_data(self, revenue_df: pd.DataFrame) -> pd.DataFrame:
        """Prepare occupancy data - this method got pretty long"""
        logger.info("📊 Preparing occupancy forecasting dataset...")
        # TODO: optimize this - it's slow with lots of data
        
        # Convert dates
        revenue_df['checkin_date'] = pd.to_datetime(revenue_df['checkin_date'])
        revenue_df['checkout_date'] = pd.to_datetime(revenue_df['checkout_date'])
        
        # Generate daily occupancy data - this loop is expensive but works
        occupancy_records = []
        
        for _, booking in revenue_df.iterrows():
            current_date = booking['checkin_date']
            while current_date < booking['checkout_date']:
                occupancy_records.append({
                    'date': current_date,
                    'resort_name': booking['resort_name'],
                    'rooms_occupied': 1,
                    'revenue': booking['total_revenue'] / booking['stay_length'],
                    'room_rate': booking['daily_rate'],
                    'guest_segment': booking['segment'],
                    'loyalty_tier': booking['loyalty_tier'],
                    'days_advance': booking['days_advance_booked'],
                    'seasonal_multiplier': booking['seasonal_multiplier']
                })
                current_date += timedelta(days=1)
        
        occupancy_df = pd.DataFrame(occupancy_records)
        
        # Aggregate by date and resort
        daily_occupancy = occupancy_df.groupby(['date', 'resort_name']).agg({
            'rooms_occupied': 'sum',
            'revenue': 'sum',
            'room_rate': 'mean',
            'days_advance': 'mean',
            'seasonal_multiplier': 'mean'
        }).reset_index()
        
        # Add capacity and occupancy rate
        daily_occupancy['total_rooms'] = daily_occupancy['resort_name'].map(
            {resort: info['rooms'] for resort, info in self.resort_info.items()}
        )
        daily_occupancy['occupancy_rate'] = daily_occupancy['rooms_occupied'] / daily_occupancy['total_rooms']
        daily_occupancy['occupancy_rate'] = daily_occupancy['occupancy_rate'].clip(0, 1)
        
        # Add temporal features
        daily_occupancy['day_of_week'] = daily_occupancy['date'].dt.dayofweek
        daily_occupancy['month'] = daily_occupancy['date'].dt.month
        daily_occupancy['day_of_year'] = daily_occupancy['date'].dt.dayofyear
        daily_occupancy['is_weekend'] = (daily_occupancy['day_of_week'] >= 5).astype(int)
        
        # Add holiday indicators (simplified)
        daily_occupancy['is_holiday_period'] = daily_occupancy['month'].isin([6, 7, 8, 11, 12]).astype(int)
        
        logger.info(f"✅ Occupancy dataset prepared: {len(daily_occupancy)} resort-days")
        return daily_occupancy
    
    def build_occupancy_forecasting_model(self, occupancy_df: pd.DataFrame) -> Dict:
        """Build occupancy forecasting models - one per resort"""
        logger.info("🏨 Building occupancy forecasting model...")
        # Note: tried different algorithms, GradientBoosting worked best
        
        # Select features for occupancy prediction
        feature_columns = [
            'day_of_week', 'month', 'day_of_year', 'is_weekend', 
            'is_holiday_period', 'seasonal_multiplier', 'days_advance'
        ]
        
        # Build separate models for each resort - they have different patterns
        models = {}
        model_performance = {}
        
        for resort_name in occupancy_df['resort_name'].unique():
            resort_data = occupancy_df[occupancy_df['resort_name'] == resort_name].copy()
            resort_data = resort_data.sort_values('date')
            
            if len(resort_data) < 50:  # Skip if insufficient data
                continue
            
            # Prepare features and target
            X = resort_data[feature_columns]
            y = resort_data['occupancy_rate']
            
            # Time series split for validation
            tscv = TimeSeriesSplit(n_splits=3)
            
            # Train model
            model = GradientBoostingRegressor(n_estimators=100, random_state=42)
            
            # Cross-validation
            cv_scores = []
            for train_idx, test_idx in tscv.split(X):
                X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
                y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
                
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                cv_scores.append(r2_score(y_test, y_pred))
            
            # Final model training
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            models[resort_name] = model
            model_performance[resort_name] = {
                'mae': round(mae, 4),
                'r2_score': round(r2, 3),
                'cv_mean': round(np.mean(cv_scores), 3),
                'training_samples': len(X_train)
            }
        
        # Save models
        self.models['occupancy_forecasting'] = models
        for resort_name, model in models.items():
            joblib.dump(model, self.models_path / f'occupancy_forecasting_{resort_name.replace(" ", "_")}.pkl')
        
        avg_r2 = np.mean([perf['r2_score'] for perf in model_performance.values()])
        logger.info(f"✅ Occupancy forecasting models built: Average R² = {avg_r2:.3f}")
        
        return {
            'model_type': 'Gradient Boosting per Resort',
            'models_trained': len(models),
            'average_r2': round(avg_r2, 3),
            'resort_performance': model_performance
        }
    
    def build_dynamic_pricing_model(self, revenue_df: pd.DataFrame) -> Dict:
        """Build dynamic pricing optimization model"""
        logger.info("💰 Building dynamic pricing optimization model...")
        
        # Prepare pricing features
        revenue_df['checkin_date'] = pd.to_datetime(revenue_df['checkin_date'])
        
        # Engineer pricing features
        revenue_df['day_of_week'] = revenue_df['checkin_date'].dt.dayofweek
        revenue_df['month'] = revenue_df['checkin_date'].dt.month
        revenue_df['is_weekend'] = (revenue_df['day_of_week'] >= 5).astype(int)
        revenue_df['is_holiday_month'] = revenue_df['month'].isin([6, 7, 8, 11, 12]).astype(int)
        
        # Add demand indicators
        revenue_df['booking_lead_category'] = pd.cut(revenue_df['days_advance_booked'], 
                                                   bins=[0, 14, 60, 180, 365], 
                                                   labels=['Last_Minute', 'Normal', 'Early', 'Very_Early'])
        
        # Encode categorical variables
        revenue_df = pd.get_dummies(revenue_df, columns=['resort_name', 'room_type', 'segment', 'booking_lead_category'], prefix_sep='_')
        
        # Select features for pricing
        feature_columns = [col for col in revenue_df.columns if 
                          col.startswith(('resort_name_', 'room_type_', 'segment_', 'booking_lead_category_')) or
                          col in ['day_of_week', 'month', 'is_weekend', 'is_holiday_month', 
                                'party_size', 'stay_length', 'seasonal_multiplier', 'annual_budget']]
        
        X = revenue_df[feature_columns].fillna(0)
        y = revenue_df['daily_rate']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train pricing model
        pricing_model = GradientBoostingRegressor(n_estimators=150, learning_rate=0.1, random_state=42)
        pricing_model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = pricing_model.predict(X_test_scaled)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': feature_columns,
            'importance': pricing_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        # Save model and scaler
        self.models['dynamic_pricing'] = pricing_model
        self.scalers['dynamic_pricing'] = scaler
        
        joblib.dump(pricing_model, self.models_path / 'dynamic_pricing_model.pkl')
        joblib.dump(scaler, self.models_path / 'dynamic_pricing_scaler.pkl')
        
        model_metrics = {
            'model_type': 'Gradient Boosting Regressor',
            'mae': round(mae, 2),
            'r2_score': round(r2, 3),
            'training_samples': len(X_train),
            'top_features': feature_importance.head(10).to_dict('records')
        }
        
        logger.info(f"✅ Dynamic pricing model built: R² = {r2:.3f}, MAE = ${mae:.2f}")
        return model_metrics
    
    def calculate_revenue_optimization_scenarios(self, revenue_df: pd.DataFrame) -> Dict:
        """Calculate revenue optimization scenarios and recommendations"""
        logger.info("🎯 Calculating revenue optimization scenarios...")
        
        optimization_results = {}
        
        # Current performance baseline
        current_metrics = {
            'total_revenue': revenue_df['total_revenue'].sum(),
            'avg_daily_rate': revenue_df['daily_rate'].mean(),
            'avg_total_spend': revenue_df['total_revenue'].mean(),
            'bookings_count': len(revenue_df)
        }
        
        # Revenue optimization by segment
        segment_analysis = revenue_df.groupby('segment').agg({
            'total_revenue': ['sum', 'mean', 'count'],
            'daily_rate': 'mean',
            'stay_length': 'mean',
            'dining_revenue': 'mean',
            'amenity_revenue': 'mean'
        }).round(2)
        
        # Identify optimization opportunities
        opportunities = self._identify_revenue_opportunities(revenue_df)
        
        # Calculate potential revenue uplift scenarios
        scenarios = self._calculate_optimization_scenarios(revenue_df, current_metrics)
        
        optimization_results = {
            'current_performance': current_metrics,
            'segment_analysis': segment_analysis.to_dict(),
            'optimization_opportunities': opportunities,
            'revenue_scenarios': scenarios,
            'recommendations': self._generate_revenue_recommendations(revenue_df, opportunities)
        }
        
        logger.info(f"✅ Revenue optimization analysis complete")
        return optimization_results
    
    def _identify_revenue_opportunities(self, df: pd.DataFrame) -> List[Dict]:
        """Identify specific revenue optimization opportunities"""
        opportunities = []
        
        # 1. Pricing optimization by demand
        low_occupancy_high_price = df[
            (df['seasonal_multiplier'] < 1.0) & (df['daily_rate'] > df.groupby('resort_name')['daily_rate'].transform('median'))
        ]
        if len(low_occupancy_high_price) > 0:
            opportunities.append({
                'type': 'pricing_optimization',
                'description': 'Lower prices during low-demand periods to increase occupancy',
                'potential_bookings': len(low_occupancy_high_price),
                'estimated_impact': '8-12% occupancy increase'
            })
        
        # 2. Ancillary revenue opportunities
        low_ancillary_spenders = df[
            (df['dining_revenue'] + df['amenity_revenue']) < df['total_cost'] * 0.2
        ]
        if len(low_ancillary_spenders) > 0:
            opportunities.append({
                'type': 'ancillary_revenue',
                'description': 'Increase dining and amenity spending through targeted offers',
                'potential_guests': len(low_ancillary_spenders),
                'estimated_impact': '15-25% ancillary revenue increase'
            })
        
        # 3. Length of stay optimization
        short_stays = df[df['stay_length'] < 3]
        if len(short_stays) > 0:
            opportunities.append({
                'type': 'length_of_stay',
                'description': 'Incentivize longer stays through package deals',
                'potential_bookings': len(short_stays),
                'estimated_impact': '20-30% revenue per guest increase'
            })
        
        # 4. Loyalty program optimization
        non_loyalty_high_spenders = df[
            (df['loyalty_tier'] == 'None') & (df['total_revenue'] > df['total_revenue'].quantile(0.7))
        ]
        if len(non_loyalty_high_spenders) > 0:
            opportunities.append({
                'type': 'loyalty_conversion',
                'description': 'Convert high-spending guests to loyalty program',
                'potential_members': len(non_loyalty_high_spenders),
                'estimated_impact': '10-15% lifetime value increase'
            })
        
        return opportunities
    
    def _calculate_optimization_scenarios(self, df: pd.DataFrame, baseline: Dict) -> Dict:
        """Calculate specific revenue optimization scenarios"""
        
        scenarios = {}
        
        # Scenario 1: Dynamic pricing optimization
        scenarios['dynamic_pricing'] = {
            'description': 'Implement advanced dynamic pricing based on demand',
            'revenue_uplift': baseline['total_revenue'] * 0.08,  # 8% increase
            'implementation_effort': 'Medium',
            'time_to_impact': '3-6 months'
        }
        
        # Scenario 2: Personalized upselling
        scenarios['personalized_upselling'] = {
            'description': 'AI-driven personalized room and service upselling',
            'revenue_uplift': baseline['total_revenue'] * 0.12,  # 12% increase
            'implementation_effort': 'High',
            'time_to_impact': '6-12 months'
        }
        
        # Scenario 3: Package optimization
        scenarios['package_optimization'] = {
            'description': 'Optimize dining and amenity packages based on guest preferences',
            'revenue_uplift': baseline['total_revenue'] * 0.15,  # 15% increase
            'implementation_effort': 'Medium',
            'time_to_impact': '3-6 months'
        }
        
        # Scenario 4: Advanced forecasting
        scenarios['demand_forecasting'] = {
            'description': 'Implement advanced demand forecasting for capacity optimization',
            'revenue_uplift': baseline['total_revenue'] * 0.06,  # 6% increase
            'implementation_effort': 'Low',
            'time_to_impact': '1-3 months'
        }
        
        return scenarios
    
    def _generate_revenue_recommendations(self, df: pd.DataFrame, opportunities: List[Dict]) -> List[Dict]:
        """Generate actionable revenue optimization recommendations"""
        
        recommendations = []
        
        # High-impact recommendations based on opportunities
        for opportunity in opportunities:
            if opportunity['type'] == 'pricing_optimization':
                recommendations.append({
                    'priority': 'High',
                    'category': 'Pricing Strategy',
                    'action': 'Implement demand-based dynamic pricing',
                    'expected_impact': '8-12% revenue increase',
                    'timeline': '2-3 months'
                })
            
            elif opportunity['type'] == 'ancillary_revenue':
                recommendations.append({
                    'priority': 'Medium',
                    'category': 'Service Optimization',
                    'action': 'Develop personalized dining and amenity recommendations',
                    'expected_impact': '15-25% ancillary revenue growth',
                    'timeline': '3-4 months'
                })
        
        # Always include these strategic recommendations
        recommendations.extend([
            {
                'priority': 'High',
                'category': 'Guest Segmentation',
                'action': 'Develop segment-specific pricing and service strategies',
                'expected_impact': '10-15% guest satisfaction and revenue increase',
                'timeline': '1-2 months'
            },
            {
                'priority': 'Medium',
                'category': 'Technology Enhancement',
                'action': 'Implement real-time revenue management dashboard',
                'expected_impact': '5-8% operational efficiency improvement',
                'timeline': '2-3 months'
            }
        ])
        
        return recommendations
    
    def save_revenue_optimization_results(self, occupancy_metrics: Dict, pricing_metrics: Dict, 
                                        optimization_results: Dict):
        """Save all revenue optimization results"""
        try:
            # Save comprehensive results
            revenue_summary = {
                'generation_date': datetime.now().isoformat(),
                'occupancy_forecasting_performance': occupancy_metrics,
                'dynamic_pricing_performance': pricing_metrics,
                'optimization_analysis': optimization_results,
                'total_revenue_analyzed': optimization_results['current_performance']['total_revenue'],
                'optimization_potential': sum([scenario['revenue_uplift'] 
                                             for scenario in optimization_results['revenue_scenarios'].values()])
            }
            
            with open(self.processed_path / 'revenue_optimization_summary.json', 'w') as f:
                json.dump(revenue_summary, f, indent=2, default=str)
            
            logger.info("✅ Revenue optimization results saved successfully")
            
        except Exception as e:
            logger.error(f"❌ Error saving revenue optimization results: {e}")
            raise

def main():
    """Run comprehensive revenue optimization pipeline"""
    engine = RevenueOptimizationEngine()
    
    print("💰 Starting Disney Resort Revenue Optimization...")
    
    try:
        # Load revenue data
        revenue_df = engine.load_revenue_data()
        
        # Prepare occupancy data and build forecasting model
        occupancy_df = engine.prepare_occupancy_data(revenue_df)
        occupancy_metrics = engine.build_occupancy_forecasting_model(occupancy_df)
        
        # Build dynamic pricing model
        pricing_metrics = engine.build_dynamic_pricing_model(revenue_df.copy())
        
        # Calculate revenue optimization scenarios
        optimization_results = engine.calculate_revenue_optimization_scenarios(revenue_df)
        
        # Save all results
        engine.save_revenue_optimization_results(occupancy_metrics, pricing_metrics, optimization_results)
        
        print("\n✅ Revenue Optimization Pipeline Complete!")
        print(f"💰 Analyzed ${optimization_results['current_performance']['total_revenue']:,.0f} in revenue")
        print(f"🏨 Built occupancy models for {occupancy_metrics['models_trained']} resorts")
        print(f"📊 Dynamic pricing model R²: {pricing_metrics['r2_score']:.3f}")
        print(f"🎯 Identified {len(optimization_results['optimization_opportunities'])} optimization opportunities")
        print(f"📈 Potential revenue uplift: ${optimization_results.get('optimization_potential', 0):,.0f}")
        
    except Exception as e:
        logger.error(f"❌ Revenue optimization pipeline failed: {e}")
        raise

if __name__ == "__main__":
    main()