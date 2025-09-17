"""
Enhanced Disney Theme Park Operations Data Generator
Realistic synthetic dataset with dynamic wait times, sophisticated Lightning Lane logic, 
and accurate weather impact modeling for advanced analytics and optimization
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import json
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedParkDataGenerator:
    """Advanced data generator with sophisticated operational modeling"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.raw_path = self.base_path / 'data' / 'raw'
        self.processed_path = self.base_path / 'data' / 'processed'
        
        # Create directories
        self.raw_path.mkdir(parents=True, exist_ok=True)
        self.processed_path.mkdir(parents=True, exist_ok=True)
        
        # Set seeds for reproducibility
        random.seed(42)
        np.random.seed(42)
        
        # Enhanced park definitions with realistic characteristics
        self.parks = {
            'Magic Kingdom': {
                'capacity': 90000,
                'base_attendance': 60000,
                'lands': ['Main Street USA', 'Fantasyland', 'Tomorrowland', 'Frontierland', 'Adventureland', 'Liberty Square'],
                'signature_attractions': 15,
                'crowd_flow_pattern': 'family_focused',  # Earlier arrivals, longer stays
                'peak_times': [(9, 11), (13, 15), (19, 21)]  # Multiple peaks
            },
            'EPCOT': {
                'capacity': 85000,
                'base_attendance': 45000,
                'lands': ['Future World', 'World Showcase'],
                'signature_attractions': 12,
                'crowd_flow_pattern': 'adult_focused',  # Later arrivals, focused touring
                'peak_times': [(10, 12), (16, 18)]  # Two distinct peaks
            },
            'Hollywood Studios': {
                'capacity': 75000,
                'base_attendance': 40000,
                'lands': ['Echo Lake', 'Sunset Boulevard', 'Grand Avenue', 'Star Wars Galaxy Edge', 'Toy Story Land'],
                'signature_attractions': 10,
                'crowd_flow_pattern': 'thrill_focused',  # Rope drop, strategic touring
                'peak_times': [(8, 10), (14, 16)]  # Early and afternoon peaks
            },
            'Animal Kingdom': {
                'capacity': 80000,
                'base_attendance': 35000,
                'lands': ['Oasis', 'Discovery Island', 'Africa', 'Asia', 'Dinoland USA', 'Pandora'],
                'signature_attractions': 8,
                'crowd_flow_pattern': 'nature_focused',  # Earlier closures, morning heavy
                'peak_times': [(8, 11), (15, 17)]  # Morning heavy, afternoon moderate
            }
        }
        
        # Enhanced attraction types with realistic characteristics
        self.attraction_types = {
            'Thrill Ride': {
                'base_capacity': 1800, 'duration': 4, 'base_popularity': 0.9,
                'wait_time_multiplier': 1.4, 'weather_sensitivity': 0.3,
                'time_of_day_variation': 'high'
            },
            'Family Ride': {
                'base_capacity': 2200, 'duration': 6, 'base_popularity': 0.8,
                'wait_time_multiplier': 1.2, 'weather_sensitivity': 0.2,
                'time_of_day_variation': 'medium'
            },
            'Dark Ride': {
                'base_capacity': 2000, 'duration': 8, 'base_popularity': 0.85,
                'wait_time_multiplier': 1.3, 'weather_sensitivity': 0.1,
                'time_of_day_variation': 'medium'
            },
            'Show': {
                'base_capacity': 3000, 'duration': 25, 'base_popularity': 0.6,
                'wait_time_multiplier': 0.6, 'weather_sensitivity': 0.05,
                'time_of_day_variation': 'low'
            },
            'Character Meet': {
                'base_capacity': 120, 'duration': 2, 'base_popularity': 0.7,
                'wait_time_multiplier': 2.0, 'weather_sensitivity': 0.4,
                'time_of_day_variation': 'high'
            },
            'Walk Through': {
                'base_capacity': 800, 'duration': 15, 'base_popularity': 0.4,
                'wait_time_multiplier': 0.3, 'weather_sensitivity': 0.6,
                'time_of_day_variation': 'low'
            }
        }
        
        # Enhanced weather conditions with realistic Florida patterns
        self.weather_conditions = {
            'Sunny': {
                'attendance_multiplier': 1.15, 'probability': 0.6,
                'outdoor_attraction_boost': 1.2, 'comfort_level': 0.9
            },
            'Partly Cloudy': {
                'attendance_multiplier': 1.05, 'probability': 0.25,
                'outdoor_attraction_boost': 1.1, 'comfort_level': 0.95
            },
            'Overcast': {
                'attendance_multiplier': 0.95, 'probability': 0.1,
                'outdoor_attraction_boost': 0.9, 'comfort_level': 0.8
            },
            'Light Rain': {
                'attendance_multiplier': 0.7, 'probability': 0.04,
                'outdoor_attraction_boost': 0.4, 'comfort_level': 0.6
            },
            'Heavy Rain': {
                'attendance_multiplier': 0.4, 'probability': 0.01,
                'outdoor_attraction_boost': 0.1, 'comfort_level': 0.3
            }
        }
        
        # Lightning Lane pricing tiers (realistic Disney pricing)
        self.lightning_lane_pricing = {
            'Individual': {
                'base_price': 12, 'surge_multiplier': 2.5, 'max_price': 27,
                'availability_limit': 0.4  # Only 40% of capacity available
            },
            'Genie+': {
                'base_price': 2, 'surge_multiplier': 1.5, 'max_price': 4,
                'availability_limit': 0.6  # 60% of capacity available
            }
        }
    
    def generate_attractions_data(self) -> pd.DataFrame:
        """Generate comprehensive attractions data with enhanced characteristics"""
        logger.info("🎢 Generating enhanced attractions data...")
        
        attractions_data = []
        attraction_id = 1000
        
        # Famous Disney attractions with realistic popularity and characteristics
        famous_attractions = {
            'Magic Kingdom': [
                ('Space Mountain', 'Thrill Ride', 'Tomorrowland', 0.95, True),
                ('Pirates of the Caribbean', 'Dark Ride', 'Adventureland', 0.90, False), 
                ('Haunted Mansion', 'Dark Ride', 'Liberty Square', 0.88, False),
                ('Big Thunder Mountain', 'Thrill Ride', 'Frontierland', 0.85, False),
                ('Seven Dwarfs Mine Train', 'Family Ride', 'Fantasyland', 0.98, True),
                ('Jungle Cruise', 'Family Ride', 'Adventureland', 0.75, False),
                ('It\'s a Small World', 'Family Ride', 'Fantasyland', 0.65, False),
                ('Splash Mountain', 'Thrill Ride', 'Frontierland', 0.92, True)
            ],
            'EPCOT': [
                ('Test Track', 'Thrill Ride', 'Future World', 0.88, True),
                ('Spaceship Earth', 'Dark Ride', 'Future World', 0.70, False),
                ('Soarin\'', 'Family Ride', 'Future World', 0.85, False),
                ('Frozen Ever After', 'Family Ride', 'World Showcase', 0.92, True),
                ('Mission: SPACE', 'Thrill Ride', 'Future World', 0.75, False)
            ],
            'Hollywood Studios': [
                ('Rise of the Resistance', 'Dark Ride', 'Star Wars Galaxy Edge', 0.99, True),
                ('Millennium Falcon', 'Family Ride', 'Star Wars Galaxy Edge', 0.87, True),
                ('Toy Story Midway Mania', 'Family Ride', 'Toy Story Land', 0.82, False),
                ('Tower of Terror', 'Thrill Ride', 'Sunset Boulevard', 0.86, False),
                ('Rock \'n\' Roller Coaster', 'Thrill Ride', 'Sunset Boulevard', 0.83, False)
            ],
            'Animal Kingdom': [
                ('Avatar Flight of Passage', 'Thrill Ride', 'Pandora', 0.97, True),
                ('Expedition Everest', 'Thrill Ride', 'Asia', 0.84, False),
                ('Kilimanjaro Safaris', 'Family Ride', 'Africa', 0.78, False),
                ('DINOSAUR', 'Thrill Ride', 'Dinoland USA', 0.72, False)
            ]
        }
        
        for park_name, park_info in self.parks.items():
            # Add famous attractions with realistic characteristics
            for attraction_name, attraction_type, land, popularity, is_outdoor in famous_attractions[park_name]:
                attraction_data = self._create_enhanced_attraction_record(
                    attraction_id, attraction_name, park_name, land, attraction_type, 
                    popularity, is_signature=True, is_outdoor=is_outdoor
                )
                attractions_data.append(attraction_data)
                attraction_id += 1
            
            # Add additional generic attractions
            remaining_attractions = park_info['signature_attractions'] - len(famous_attractions[park_name])
            for i in range(remaining_attractions):
                land = random.choice(park_info['lands'])
                attraction_type = np.random.choice(list(self.attraction_types.keys()), 
                                                 p=[0.2, 0.3, 0.25, 0.1, 0.1, 0.05])
                attraction_name = f"{park_name} {attraction_type} {i+1}"
                popularity = np.random.uniform(0.4, 0.8)
                is_outdoor = np.random.choice([True, False], p=[0.3, 0.7])
                
                attraction_data = self._create_enhanced_attraction_record(
                    attraction_id, attraction_name, park_name, land, attraction_type, 
                    popularity, is_signature=False, is_outdoor=is_outdoor
                )
                attractions_data.append(attraction_data)
                attraction_id += 1
        
        df = pd.DataFrame(attractions_data)
        logger.info(f"✅ Generated {len(df)} enhanced attractions with realistic characteristics")
        return df
    
    def _create_enhanced_attraction_record(self, attraction_id: int, name: str, park: str, 
                                         land: str, attraction_type: str, popularity: float,
                                         is_signature: bool, is_outdoor: bool) -> Dict:
        """Create enhanced attraction record with realistic characteristics"""
        type_info = self.attraction_types[attraction_type]
        
        # Enhanced capacity calculation
        capacity_multiplier = 1.3 if is_signature else np.random.uniform(0.7, 1.2)
        if is_outdoor:
            capacity_multiplier *= 0.9  # Outdoor attractions typically lower capacity
        hourly_capacity = int(type_info['base_capacity'] * capacity_multiplier)
        
        # Realistic operational metrics
        ride_duration = type_info['duration'] * np.random.uniform(0.8, 1.2)
        
        # Weather sensitivity based on outdoor status
        weather_sensitivity = 0.8 if is_outdoor else type_info['weather_sensitivity']
        
        # Lightning Lane tier determination with realistic logic
        lightning_lane_tier = self._determine_lightning_lane_tier_enhanced(
            is_signature, popularity, attraction_type
        )
        
        return {
            'attraction_id': f'ATT_{attraction_id}',
            'attraction_name': name,
            'park': park,
            'land': land,
            'attraction_type': attraction_type,
            'is_signature': is_signature,
            'is_outdoor': is_outdoor,
            'hourly_capacity': hourly_capacity,
            'ride_duration_minutes': round(ride_duration, 1),
            'popularity_score': round(popularity, 3),
            'height_requirement_inches': self._determine_height_requirement(attraction_type, is_signature),
            'accessibility_score': round(np.random.uniform(0.4, 0.9), 3),
            'lightning_lane_tier': lightning_lane_tier,
            'operational_cost_hourly': int(np.random.uniform(200, 800)),
            'maintenance_score': round(np.random.uniform(0.7, 0.95), 3),
            'weather_sensitivity': round(weather_sensitivity, 3),
            'time_of_day_pattern': type_info['time_of_day_variation'],
            'wait_time_multiplier': type_info['wait_time_multiplier']
        }
    
    def _determine_lightning_lane_tier_enhanced(self, is_signature: bool, popularity: float, attraction_type: str) -> str:
        """Enhanced Lightning Lane tier determination with realistic business logic"""
        if not is_signature or attraction_type in ['Show', 'Walk Through']:
            return 'None'
        
        # Ultra-popular attractions get Individual Lightning Lane
        if popularity >= 0.95:
            return 'Individual'
        # High-popularity signature attractions get Individual
        elif popularity >= 0.85 and attraction_type in ['Thrill Ride', 'Dark Ride']:
            return 'Individual' if np.random.random() < 0.7 else 'Genie+'
        # Moderate popularity signature attractions get Genie+
        elif popularity >= 0.65:
            return 'Genie+'
        else:
            return 'None'
    
    def generate_enhanced_operational_data(self, attractions_df: pd.DataFrame, days: int = 90) -> pd.DataFrame:
        """Generate realistic operational data with dynamic wait times and sophisticated modeling"""
        logger.info(f"📊 Generating {days} days of enhanced operational data...")
        
        operational_data = []
        start_date = datetime.now() - timedelta(days=days)
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            # Enhanced day characteristics
            is_weekend = current_date.weekday() >= 5
            is_holiday = self._is_holiday_season(current_date)
            weather = self._generate_enhanced_weather_for_date(current_date)
            
            # Calculate realistic park attendance
            park_attendance = self._calculate_enhanced_park_attendance(
                current_date, weather, is_weekend, is_holiday
            )
            
            # Generate hourly operational data for realistic wait time patterns
            for _, attraction in attractions_df.iterrows():
                # Generate data for different times of day (simplified to 3 time periods)
                for time_period in ['morning', 'afternoon', 'evening']:
                    daily_data = self._generate_enhanced_attraction_data(
                        attraction, current_date, park_attendance[attraction['park']], 
                        weather, time_period, is_weekend
                    )
                    operational_data.append(daily_data)
        
        df = pd.DataFrame(operational_data)
        logger.info(f"✅ Generated {len(df):,} enhanced operational records with realistic patterns")
        return df
    
    def _generate_enhanced_attraction_data(self, attraction: pd.Series, date: datetime, 
                                         park_attendance: int, weather: Dict, 
                                         time_period: str, is_weekend: bool) -> Dict:
        """Generate realistic attraction operational data with dynamic wait times"""
        
        # Time-of-day multipliers for realistic crowd flow
        time_multipliers = {
            'morning': {'base': 0.8, 'thrill': 1.2, 'family': 0.9},
            'afternoon': {'base': 1.3, 'thrill': 1.1, 'family': 1.4},
            'evening': {'base': 1.0, 'thrill': 0.9, 'family': 1.1}
        }
        
        # Calculate base demand with time-of-day variation
        attraction_type = attraction['attraction_type'].lower().replace(' ', '_')
        time_key = 'thrill' if 'thrill' in attraction_type else 'family'
        time_multiplier = time_multipliers[time_period].get(time_key, time_multipliers[time_period]['base'])
        
        base_demand = (park_attendance * attraction['popularity_score'] * 
                      time_multiplier * 0.3)  # 30% of park visitors per time period
        
        # Weather impact with outdoor sensitivity
        if attraction['is_outdoor'] and weather['condition'] in ['Light Rain', 'Heavy Rain']:
            weather_impact = weather['outdoor_attraction_boost']
            base_demand *= weather_impact
        
        # Lightning Lane sophisticated modeling
        ll_guests, standby_demand = self._calculate_lightning_lane_usage_enhanced(
            attraction, base_demand, time_period, is_weekend
        )
        
        # Realistic wait time calculation
        wait_times = self._calculate_realistic_wait_times(
            attraction, standby_demand, ll_guests, time_period
        )
        
        # Revenue calculation with dynamic pricing
        revenue = self._calculate_enhanced_revenue(
            attraction, base_demand, ll_guests, wait_times['avg'], is_weekend, time_period
        )
        
        # Enhanced operational metrics
        downtime = max(0, np.random.normal(15, 10))  # More realistic downtime
        satisfaction = self._calculate_enhanced_satisfaction(
            wait_times['avg'], weather['comfort_level'], attraction['attraction_type']
        )
        
        return {
            'date': date.strftime('%Y-%m-%d'),
            'time_period': time_period,
            'attraction_id': attraction['attraction_id'],
            'attraction_name': attraction['attraction_name'],
            'park': attraction['park'],
            'weather_condition': weather['condition'],
            'temperature': weather['temperature'],
            'park_attendance': park_attendance,
            'total_guests': int(base_demand),
            'lightning_lane_guests': ll_guests,
            'standby_guests': int(standby_demand),
            'avg_wait_time_minutes': wait_times['avg'],
            'peak_wait_time_minutes': wait_times['peak'],
            'min_wait_time_minutes': wait_times['min'],
            'capacity_utilization': wait_times['utilization'],
            'downtime_minutes': round(downtime, 1),
            'guest_satisfaction_score': round(satisfaction, 3),
            'revenue_generated': int(revenue),
            'operational_efficiency': round(min(1.0, attraction['hourly_capacity'] / max(base_demand/3, 1)), 3),
            'weather_impact_factor': weather['outdoor_attraction_boost'] if attraction['is_outdoor'] else 1.0,
            'time_of_day_factor': time_multiplier
        }
    
    def _calculate_realistic_wait_times(self, attraction: pd.Series, standby_demand: float, 
                                      ll_guests: int, time_period: str) -> Dict[str, float]:
        """Calculate realistic wait times with proper queueing theory"""
        
        hourly_capacity = attraction['hourly_capacity']
        
        # Effective capacity considering Lightning Lane
        effective_capacity = hourly_capacity - (ll_guests * 3)  # LL guests reduce standby capacity
        effective_capacity = max(effective_capacity, hourly_capacity * 0.3)  # Minimum 30% for standby
        
        # Utilization ratio
        utilization = standby_demand / effective_capacity if effective_capacity > 0 else 2.0
        
        # Realistic wait time calculation using queueing theory concepts
        if utilization <= 0.5:
            avg_wait = 5 + (utilization * 20)  # 5-15 minutes
        elif utilization <= 0.8:
            avg_wait = 15 + ((utilization - 0.5) * 100)  # 15-45 minutes
        elif utilization <= 1.0:
            avg_wait = 45 + ((utilization - 0.8) * 150)  # 45-75 minutes
        else:
            # Over capacity - exponential growth
            avg_wait = 75 + (min(utilization - 1.0, 1.0) * 100)  # 75-175 minutes max
        
        # Apply attraction-specific wait time multiplier
        avg_wait *= attraction['wait_time_multiplier']
        
        # Time period adjustments
        period_adjustments = {
            'morning': 0.8,  # Lower waits in morning
            'afternoon': 1.2,  # Higher waits in afternoon
            'evening': 1.0   # Normal waits in evening
        }
        avg_wait *= period_adjustments.get(time_period, 1.0)
        
        # Add realistic variance
        min_wait = max(0, avg_wait * 0.3)
        peak_wait = avg_wait * 1.8
        
        return {
            'avg': round(avg_wait, 1),
            'min': round(min_wait, 1),
            'peak': round(peak_wait, 1),
            'utilization': round(utilization, 3)
        }
    
    def _calculate_lightning_lane_usage_enhanced(self, attraction: pd.Series, base_demand: float, 
                                               time_period: str, is_weekend: bool) -> Tuple[int, float]:
        """Enhanced Lightning Lane usage calculation with realistic business logic"""
        
        if attraction['lightning_lane_tier'] == 'None':
            return 0, base_demand
        
        # Base usage rates by tier
        base_usage_rates = {
            'Individual': 0.15,  # 15% base usage for Individual LL
            'Genie+': 0.25      # 25% base usage for Genie+ LL
        }
        
        usage_rate = base_usage_rates[attraction['lightning_lane_tier']]
        
        # Adjustments for realistic usage patterns
        if is_weekend:
            usage_rate *= 1.3  # Higher usage on weekends
        
        if time_period == 'afternoon':
            usage_rate *= 1.4  # Peak usage in afternoon
        elif time_period == 'morning':
            usage_rate *= 0.8  # Lower usage in morning
        
        # Popularity adjustment - more popular attractions get higher LL usage
        popularity_multiplier = 0.5 + (attraction['popularity_score'] * 0.7)
        usage_rate *= popularity_multiplier
        
        # Capacity constraints
        max_ll_capacity = base_demand * self.lightning_lane_pricing[attraction['lightning_lane_tier']]['availability_limit']
        
        ll_guests = min(int(base_demand * usage_rate), int(max_ll_capacity))
        standby_demand = base_demand - ll_guests
        
        return ll_guests, standby_demand
    
    def _calculate_enhanced_revenue(self, attraction: pd.Series, total_guests: float, 
                                  ll_guests: int, avg_wait_time: float, is_weekend: bool, 
                                  time_period: str) -> float:
        """Calculate enhanced revenue with dynamic Lightning Lane pricing"""
        
        base_revenue = 0.5 * total_guests  # Base revenue per guest
        
        # Lightning Lane revenue with dynamic pricing
        ll_revenue = 0
        if attraction['lightning_lane_tier'] != 'None':
            tier_pricing = self.lightning_lane_pricing[attraction['lightning_lane_tier']]
            
            # Dynamic pricing based on demand (wait time proxy)
            demand_multiplier = 1.0
            if avg_wait_time > 60:
                demand_multiplier = min(tier_pricing['surge_multiplier'], 
                                      1 + (avg_wait_time - 60) / 60)
            
            ll_price = min(tier_pricing['base_price'] * demand_multiplier, 
                          tier_pricing['max_price'])
            
            # Time and weekend adjustments
            if is_weekend:
                ll_price *= 1.2
            if time_period == 'afternoon':
                ll_price *= 1.1
            
            ll_revenue = ll_guests * ll_price
        
        # Additional revenue for signature attractions (merchandise, photos)
        if attraction['is_signature']:
            base_revenue *= 2.0
        
        # Weekend premium
        if is_weekend:
            base_revenue *= 1.15
        
        return base_revenue + ll_revenue
    
    def _calculate_enhanced_satisfaction(self, wait_time: float, weather_comfort: float, 
                                       attraction_type: str) -> float:
        """Calculate guest satisfaction with multiple factors"""
        
        base_satisfaction = 0.8
        
        # Wait time impact (non-linear)
        if wait_time <= 10:
            wait_modifier = 0.2
        elif wait_time <= 30:
            wait_modifier = 0.1
        elif wait_time <= 60:
            wait_modifier = 0
        elif wait_time <= 90:
            wait_modifier = -0.15
        else:
            wait_modifier = -0.3
        
        # Weather comfort impact
        weather_modifier = (weather_comfort - 0.8) * 0.2
        
        # Attraction type satisfaction baseline
        type_modifiers = {
            'Thrill Ride': 0.1,
            'Family Ride': 0.05,
            'Dark Ride': 0.08,
            'Show': 0.02,
            'Character Meet': 0.15,
            'Walk Through': -0.05
        }
        
        type_modifier = type_modifiers.get(attraction_type, 0)
        
        final_satisfaction = base_satisfaction + wait_modifier + weather_modifier + type_modifier
        return max(0.1, min(1.0, final_satisfaction))
    
    def _generate_enhanced_weather_for_date(self, date: datetime) -> Dict:
        """Generate enhanced weather with realistic Florida patterns"""
        month = date.month
        
        # Enhanced seasonal weather patterns
        if 6 <= month <= 9:  # Summer - hot, humid, afternoon storms
            weather_probs = [0.3, 0.2, 0.15, 0.3, 0.05]
            temp_range = (88, 96)
            humidity_range = (75, 95)
        elif month in [12, 1, 2]:  # Winter - cooler, dry
            weather_probs = [0.7, 0.25, 0.04, 0.01, 0.0]
            temp_range = (65, 78)
            humidity_range = (45, 70)
        else:  # Spring/Fall - mild, moderate rain
            weather_probs = [0.55, 0.3, 0.1, 0.04, 0.01]
            temp_range = (75, 86)
            humidity_range = (55, 80)
        
        condition = np.random.choice(list(self.weather_conditions.keys()), p=weather_probs)
        weather_info = self.weather_conditions[condition]
        
        return {
            'condition': condition,
            'temperature': int(np.random.uniform(*temp_range)),
            'humidity': int(np.random.uniform(*humidity_range)),
            'attendance_multiplier': weather_info['attendance_multiplier'],
            'outdoor_attraction_boost': weather_info['outdoor_attraction_boost'],
            'comfort_level': weather_info['comfort_level']
        }
    
    def _calculate_enhanced_park_attendance(self, date: datetime, weather: Dict, 
                                          is_weekend: bool, is_holiday: bool) -> Dict[str, int]:
        """Calculate realistic park attendance with multiple factors"""
        park_attendance = {}
        
        for park_name, park_info in self.parks.items():
            base_attendance = park_info['base_attendance']
            
            # Weather impact
            attendance = base_attendance * weather['attendance_multiplier']
            
            # Day of week impact
            if is_weekend:
                attendance *= 1.35
            
            # Holiday impact with park-specific multipliers
            if is_holiday:
                holiday_multipliers = {
                    'Magic Kingdom': 1.8,  # Most popular during holidays
                    'EPCOT': 1.4,
                    'Hollywood Studios': 1.5,
                    'Animal Kingdom': 1.3
                }
                attendance *= holiday_multipliers[park_name]
            
            # Seasonal variations with park characteristics
            month = date.month
            seasonal_patterns = {
                'Magic Kingdom': {(6, 7, 8): 1.4, (11, 12): 1.6, (1, 2, 9): 0.75},
                'EPCOT': {(6, 7, 8): 1.2, (10, 11, 12): 1.4, (1, 2): 0.8},
                'Hollywood Studios': {(6, 7, 8): 1.3, (11, 12): 1.3, (1, 2): 0.7},
                'Animal Kingdom': {(6, 7, 8): 1.1, (11, 12): 1.2, (1, 2, 9): 0.8}
            }
            
            for months, multiplier in seasonal_patterns[park_name].items():
                if month in months:
                    attendance *= multiplier
                    break
            
            # Daily variation
            attendance *= np.random.uniform(0.88, 1.12)
            
            # Capacity constraints
            park_attendance[park_name] = min(int(attendance), park_info['capacity'])
        
        return park_attendance
    
    def _is_holiday_season(self, date: datetime) -> bool:
        """Enhanced holiday season detection"""
        month, day = date.month, date.day
        
        # More comprehensive holiday periods
        holiday_periods = [
            (11, 18, 1, 8),   # Thanksgiving to New Year
            (3, 10, 4, 25),   # Spring Break/Easter (extended)
            (5, 25, 8, 25),   # Summer season (extended)
            (9, 20, 11, 7),   # Halloween to early November
            (2, 10, 2, 20)    # Presidents Day week
        ]
        
        for start_month, start_day, end_month, end_day in holiday_periods:
            if start_month == end_month:
                if month == start_month and start_day <= day <= end_day:
                    return True
            else:
                if ((month == start_month and day >= start_day) or 
                    (month == end_month and day <= end_day) or 
                    (start_month < month < end_month)):
                    return True
        
        return False
    
    def save_data(self, attractions_df: pd.DataFrame, operations_df: pd.DataFrame):
        """Save enhanced datasets"""
        try:
            # Save raw data
            attractions_df.to_csv(self.raw_path / 'enhanced_park_attractions.csv', index=False)
            operations_df.to_csv(self.raw_path / 'enhanced_park_operations.csv', index=False)
            
            # Generate summary statistics
            summary = {
                'generation_date': datetime.now().isoformat(),
                'total_attractions': len(attractions_df),
                'total_operations': len(operations_df),
                'parks': list(self.parks.keys()),
                'data_features': {
                    'realistic_wait_times': True,
                    'dynamic_lightning_lane': True,
                    'weather_sensitivity': True,
                    'time_of_day_variations': True,
                    'seasonal_patterns': True
                },
                'avg_daily_attendance': int(operations_df.groupby(['date', 'park'])['park_attendance'].first().mean()),
                'total_revenue': int(operations_df['revenue_generated'].sum()),
                'avg_wait_time': round(operations_df['avg_wait_time_minutes'].mean(), 1),
                'satisfaction_score': round(operations_df['guest_satisfaction_score'].mean(), 3)
            }
            
            with open(self.raw_path / 'enhanced_generation_summary.json', 'w') as f:
                json.dump(summary, f, indent=2)
            
            logger.info("✅ Enhanced datasets saved successfully")
            logger.info(f"📊 Generated {len(operations_df):,} operational records")
            logger.info(f"🎢 {len(attractions_df)} attractions across {len(self.parks)} parks")
            logger.info(f"💰 Total revenue: ${summary['total_revenue']:,}")
            
        except Exception as e:
            logger.error(f"❌ Error saving data: {e}")
            raise

def main():
    """Generate enhanced Disney park dataset"""
    generator = AdvancedParkDataGenerator()
    
    print("🏰 Starting Enhanced Disney Park Data Generation...")
    
    # Generate attractions
    attractions_df = generator.generate_attractions_data()
    
    # Generate operational data (90 days, 3 time periods per day)
    operations_df = generator.generate_enhanced_operational_data(attractions_df, days=30)
    
    # Save datasets
    generator.save_data(attractions_df, operations_df)
    
    print("\n✅ Enhanced Disney Park Dataset Generation Complete!")
    print(f"📊 Ready for advanced analytics and optimization")

if __name__ == "__main__":
    main()