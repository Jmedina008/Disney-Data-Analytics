"""
Disney Theme Park Operations Data Generator
Creates comprehensive synthetic dataset for park optimization and operational analytics
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import json
from pathlib import Path

class DisneyParkDataGenerator:
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
        
        # Disney park definitions
        self.parks = {
            'Magic Kingdom': {
                'capacity': 90000,
                'base_attendance': 60000,
                'lands': ['Main Street USA', 'Fantasyland', 'Tomorrowland', 'Frontierland', 'Adventureland', 'Liberty Square'],
                'signature_attractions': 15
            },
            'EPCOT': {
                'capacity': 85000,
                'base_attendance': 45000,
                'lands': ['Future World', 'World Showcase'],
                'signature_attractions': 12
            },
            'Hollywood Studios': {
                'capacity': 75000,
                'base_attendance': 40000,
                'lands': ['Echo Lake', 'Sunset Boulevard', 'Grand Avenue', 'Star Wars Galaxy Edge', 'Toy Story Land'],
                'signature_attractions': 10
            },
            'Animal Kingdom': {
                'capacity': 80000,
                'base_attendance': 35000,
                'lands': ['Oasis', 'Discovery Island', 'Africa', 'Asia', 'Dinoland USA', 'Pandora'],
                'signature_attractions': 8
            }
        }
        
        # Attraction types and characteristics
        self.attraction_types = {
            'Thrill Ride': {'base_capacity': 1800, 'duration': 4, 'popularity': 0.9},
            'Family Ride': {'base_capacity': 2200, 'duration': 6, 'popularity': 0.8},
            'Dark Ride': {'base_capacity': 2000, 'duration': 8, 'popularity': 0.85},
            'Show': {'base_capacity': 3000, 'duration': 25, 'popularity': 0.6},
            'Character Meet': {'base_capacity': 120, 'duration': 2, 'popularity': 0.7},
            'Walk Through': {'base_capacity': 800, 'duration': 15, 'popularity': 0.4}
        }
        
        # Weather conditions affecting attendance
        self.weather_conditions = {
            'Sunny': {'attendance_multiplier': 1.15, 'probability': 0.6},
            'Partly Cloudy': {'attendance_multiplier': 1.05, 'probability': 0.25},
            'Overcast': {'attendance_multiplier': 0.95, 'probability': 0.1},
            'Light Rain': {'attendance_multiplier': 0.7, 'probability': 0.04},
            'Heavy Rain': {'attendance_multiplier': 0.4, 'probability': 0.01}
        }
    
    def generate_attractions_data(self) -> pd.DataFrame:
        """Generate comprehensive attractions data for all Disney parks"""
        print("🎢 Generating attractions data...")
        
        attractions_data = []
        attraction_id = 1000
        
        # Famous Disney attractions with realistic characteristics
        famous_attractions = {
            'Magic Kingdom': [
                ('Space Mountain', 'Thrill Ride', 'Tomorrowland'),
                ('Pirates of the Caribbean', 'Dark Ride', 'Adventureland'), 
                ('Haunted Mansion', 'Dark Ride', 'Liberty Square'),
                ('Big Thunder Mountain', 'Thrill Ride', 'Frontierland'),
                ('It\'s a Small World', 'Family Ride', 'Fantasyland'),
                ('Jungle Cruise', 'Family Ride', 'Adventureland'),
                ('Seven Dwarfs Mine Train', 'Family Ride', 'Fantasyland'),
                ('Splash Mountain', 'Thrill Ride', 'Frontierland')
            ],
            'EPCOT': [
                ('Test Track', 'Thrill Ride', 'Future World'),
                ('Spaceship Earth', 'Dark Ride', 'Future World'),
                ('Soarin\'', 'Family Ride', 'Future World'),
                ('Frozen Ever After', 'Family Ride', 'World Showcase'),
                ('Mission: SPACE', 'Thrill Ride', 'Future World')
            ],
            'Hollywood Studios': [
                ('Rise of the Resistance', 'Dark Ride', 'Star Wars Galaxy Edge'),
                ('Millennium Falcon', 'Family Ride', 'Star Wars Galaxy Edge'),
                ('Toy Story Midway Mania', 'Family Ride', 'Toy Story Land'),
                ('Tower of Terror', 'Thrill Ride', 'Sunset Boulevard'),
                ('Rock \'n\' Roller Coaster', 'Thrill Ride', 'Sunset Boulevard')
            ],
            'Animal Kingdom': [
                ('Avatar Flight of Passage', 'Thrill Ride', 'Pandora'),
                ('Expedition Everest', 'Thrill Ride', 'Asia'),
                ('Kilimanjaro Safaris', 'Family Ride', 'Africa'),
                ('DINOSAUR', 'Thrill Ride', 'Dinoland USA')
            ]
        }
        
        for park_name, park_info in self.parks.items():
            # Add famous attractions
            for attraction_name, attraction_type, land in famous_attractions[park_name]:
                attraction_data = self._create_attraction_record(
                    attraction_id, attraction_name, park_name, land, attraction_type, is_signature=True
                )
                attractions_data.append(attraction_data)
                attraction_id += 1
            
            # Add additional generic attractions to reach target count
            remaining_attractions = park_info['signature_attractions'] - len(famous_attractions[park_name])
            for i in range(remaining_attractions):
                land = random.choice(park_info['lands'])
                attraction_type = np.random.choice(list(self.attraction_types.keys()), 
                                                 p=[0.2, 0.3, 0.25, 0.1, 0.1, 0.05])
                attraction_name = f"{park_name} {attraction_type} {i+1}"
                
                attraction_data = self._create_attraction_record(
                    attraction_id, attraction_name, park_name, land, attraction_type, is_signature=False
                )
                attractions_data.append(attraction_data)
                attraction_id += 1
        
        return pd.DataFrame(attractions_data)
    
    def _create_attraction_record(self, attraction_id: int, name: str, park: str, 
                                land: str, attraction_type: str, is_signature: bool) -> Dict:
        """Create individual attraction record with realistic characteristics"""
        type_info = self.attraction_types[attraction_type]
        
        # Adjust capacity based on signature status
        capacity_multiplier = 1.3 if is_signature else np.random.uniform(0.7, 1.2)
        hourly_capacity = int(type_info['base_capacity'] * capacity_multiplier)
        
        # Calculate operational metrics
        ride_duration = type_info['duration'] * np.random.uniform(0.8, 1.2)
        popularity_score = type_info['popularity'] * (1.4 if is_signature else np.random.uniform(0.6, 1.0))
        
        # Height and accessibility requirements
        height_requirement = self._determine_height_requirement(attraction_type, is_signature)
        accessibility_score = np.random.uniform(0.4, 0.9)
        
        # FastPass and Lightning Lane availability
        has_fastpass = is_signature or np.random.choice([True, False], p=[0.6, 0.4])
        lightning_lane_tier = self._determine_lightning_lane_tier(is_signature, popularity_score)
        
        return {
            'attraction_id': f'ATT_{attraction_id}',
            'attraction_name': name,
            'park': park,
            'land': land,
            'attraction_type': attraction_type,
            'is_signature': is_signature,
            'hourly_capacity': hourly_capacity,
            'ride_duration_minutes': round(ride_duration, 1),
            'popularity_score': round(popularity_score, 3),
            'height_requirement_inches': height_requirement,
            'accessibility_score': round(accessibility_score, 3),
            'has_fastpass': has_fastpass,
            'lightning_lane_tier': lightning_lane_tier,
            'operational_cost_hourly': int(np.random.uniform(200, 800)),
            'maintenance_score': round(np.random.uniform(0.7, 0.95), 3),
            'weather_sensitivity': round(np.random.uniform(0.1, 0.8), 3)
        }
    
    def _determine_height_requirement(self, attraction_type: str, is_signature: bool) -> int:
        """Determine height requirement based on attraction characteristics"""
        if attraction_type == 'Thrill Ride':
            return random.choice([40, 44, 46, 48]) if is_signature else random.choice([35, 40, 44])
        elif attraction_type in ['Family Ride', 'Dark Ride']:
            return random.choice([0, 32, 35, 40])
        else:
            return 0  # No height requirement
    
    def _determine_lightning_lane_tier(self, is_signature: bool, popularity: float) -> str:
        """Determine Lightning Lane tier based on attraction characteristics"""
        if not is_signature:
            return 'None'
        elif popularity > 0.8:
            return 'Individual'
        elif popularity > 0.6:
            return 'Genie+'
        else:
            return 'None'
    
    def generate_operational_data(self, attractions_df: pd.DataFrame, days: int = 90) -> pd.DataFrame:
        """Generate daily operational data for all attractions"""
        print(f"📊 Generating {days} days of operational data...")
        
        operational_data = []
        start_date = datetime.now() - timedelta(days=days)
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            # Determine day characteristics
            is_weekend = current_date.weekday() >= 5
            is_holiday = self._is_holiday_season(current_date)
            weather = self._generate_weather_for_date(current_date)
            
            # Calculate base attendance for each park
            park_attendance = self._calculate_park_attendance(current_date, weather, is_weekend, is_holiday)
            
            for _, attraction in attractions_df.iterrows():
                daily_data = self._generate_attraction_daily_data(
                    attraction, current_date, park_attendance[attraction['park']], weather
                )
                operational_data.append(daily_data)
        
        return pd.DataFrame(operational_data)
    
    def _is_holiday_season(self, date: datetime) -> bool:
        """Determine if date falls in Disney holiday season"""
        month = date.month
        # Holiday seasons: Christmas/New Year, Easter, Summer, Halloween
        holiday_periods = [
            (11, 15, 1, 15),  # Thanksgiving to New Year
            (3, 15, 4, 30),   # Spring Break/Easter
            (6, 1, 8, 31),    # Summer
            (9, 15, 11, 7)    # Halloween
        ]
        
        for start_month, start_day, end_month, end_day in holiday_periods:
            if (month == start_month and date.day >= start_day) or \
               (month == end_month and date.day <= end_day) or \
               (start_month < month < end_month):
                return True
        return False
    
    def _generate_weather_for_date(self, date: datetime) -> Dict:
        """Generate realistic weather for given date"""
        # Florida weather patterns
        month = date.month
        
        # Summer (June-September): More rain, hot
        if 6 <= month <= 9:
            weather_probs = [0.4, 0.2, 0.15, 0.2, 0.05]  # More rain in summer
            temp_range = (85, 95)
            humidity_range = (70, 90)
        # Winter (December-February): Cooler, less rain  
        elif month in [12, 1, 2]:
            weather_probs = [0.7, 0.25, 0.04, 0.01, 0.0]  # Less rain in winter
            temp_range = (65, 80)
            humidity_range = (50, 75)
        # Spring/Fall: Moderate
        else:
            weather_probs = [0.6, 0.25, 0.1, 0.04, 0.01]
            temp_range = (75, 85)
            humidity_range = (60, 80)
        
        condition = np.random.choice(list(self.weather_conditions.keys()), p=weather_probs)
        
        return {
            'condition': condition,
            'temperature': int(np.random.uniform(*temp_range)),
            'humidity': int(np.random.uniform(*humidity_range)),
            'attendance_multiplier': self.weather_conditions[condition]['attendance_multiplier']
        }
    
    def _calculate_park_attendance(self, date: datetime, weather: Dict, 
                                 is_weekend: bool, is_holiday: bool) -> Dict[str, int]:
        """Calculate expected attendance for each park on given date"""
        park_attendance = {}
        
        for park_name, park_info in self.parks.items():
            base_attendance = park_info['base_attendance']
            
            # Apply multipliers
            attendance = base_attendance * weather['attendance_multiplier']
            
            if is_weekend:
                attendance *= 1.4
            if is_holiday:
                attendance *= 1.6
            
            # Seasonal variations
            month = date.month
            if month in [6, 7, 8]:  # Summer peak
                attendance *= 1.3
            elif month in [11, 12]:  # Holiday season
                attendance *= 1.5
            elif month in [1, 2, 9]:  # Low season
                attendance *= 0.8
            
            # Add daily variation
            attendance *= np.random.uniform(0.85, 1.15)
            
            park_attendance[park_name] = min(int(attendance), park_info['capacity'])
        
        return park_attendance
    
    def _generate_attraction_daily_data(self, attraction: pd.Series, date: datetime, 
                                      park_attendance: int, weather: Dict) -> Dict:
        """Generate daily operational data for specific attraction"""
        
        # Calculate expected demand based on park attendance and attraction popularity
        base_demand = park_attendance * attraction['popularity_score'] * 0.7
        
        # Weather impact on outdoor attractions
        if attraction['weather_sensitivity'] > 0.5 and weather['condition'] in ['Light Rain', 'Heavy Rain']:
            demand_multiplier = 0.6 if weather['condition'] == 'Light Rain' else 0.3
            base_demand *= demand_multiplier
        
        # Lightning Lane impact
        if attraction['lightning_lane_tier'] != 'None':
            lightning_lane_usage = int(base_demand * 0.25)  # 25% use Lightning Lane
            standby_demand = base_demand - lightning_lane_usage
        else:
            lightning_lane_usage = 0
            standby_demand = base_demand
        
        # Calculate wait times
        hourly_capacity = attraction['hourly_capacity']
        capacity_utilization = min(base_demand / (hourly_capacity * 12), 1.5)  # 12 operating hours
        
        # Peak wait time calculation
        if capacity_utilization <= 0.8:
            avg_wait_time = 15 * capacity_utilization
        elif capacity_utilization <= 1.0:
            avg_wait_time = 15 + 45 * (capacity_utilization - 0.8) / 0.2
        else:
            avg_wait_time = 60 + 60 * (capacity_utilization - 1.0) / 0.5
        
        peak_wait_time = avg_wait_time * 1.8
        
        # Revenue calculations
        revenue_per_guest = self._calculate_revenue_per_guest(attraction, date.weekday() >= 5)
        total_revenue = int(base_demand * revenue_per_guest)
        
        # Operational metrics
        downtime_minutes = max(0, np.random.normal(20, 15))  # Average 20 min downtime
        guest_satisfaction = self._calculate_satisfaction(avg_wait_time, attraction['attraction_type'])
        
        return {
            'date': date.strftime('%Y-%m-%d'),
            'attraction_id': attraction['attraction_id'],
            'attraction_name': attraction['attraction_name'],
            'park': attraction['park'],
            'weather_condition': weather['condition'],
            'temperature': weather['temperature'],
            'park_attendance': park_attendance,
            'total_guests': int(base_demand),
            'lightning_lane_guests': lightning_lane_usage,
            'standby_guests': int(standby_demand),
            'avg_wait_time_minutes': round(avg_wait_time, 1),
            'peak_wait_time_minutes': round(peak_wait_time, 1),
            'capacity_utilization': round(capacity_utilization, 3),
            'downtime_minutes': round(downtime_minutes, 1),
            'guest_satisfaction_score': round(guest_satisfaction, 3),
            'revenue_generated': total_revenue,
            'operational_efficiency': round(min(1.0, hourly_capacity * 12 / max(base_demand, 1)), 3)
        }
    
    def _calculate_revenue_per_guest(self, attraction: pd.Series, is_weekend: bool) -> float:
        """Calculate estimated revenue per guest for attraction"""
        base_revenue = 0.5  # Base revenue per attraction experience
        
        # Premium attractions generate more revenue (merchandise, photos, etc.)
        if attraction['is_signature']:
            base_revenue *= 2.5
        
        # Lightning Lane revenue
        if attraction['lightning_lane_tier'] == 'Individual':
            base_revenue += 8  # Individual Lightning Lane cost
        elif attraction['lightning_lane_tier'] == 'Genie+':
            base_revenue += 1  # Portion of Genie+ revenue
        
        # Weekend premium
        if is_weekend:
            base_revenue *= 1.2
        
        return base_revenue
    
    def _calculate_satisfaction(self, wait_time: float, attraction_type: str) -> float:
        """Calculate guest satisfaction based on wait time and attraction type"""
        base_satisfaction = 0.8
        
        # Wait time impact
        if wait_time <= 15:
            wait_modifier = 0.2
        elif wait_time <= 30:
            wait_modifier = 0.1
        elif wait_time <= 60:
            wait_modifier = 0
        elif wait_time <= 90:
            wait_modifier = -0.1
        else:
            wait_modifier = -0.2
        
        # Attraction type satisfaction
        type_modifiers = {
            'Thrill Ride': 0.1,
            'Dark Ride': 0.05,
            'Family Ride': 0.0,
            'Show': -0.05,
            'Character Meet': 0.15,
            'Walk Through': -0.1
        }
        
        final_satisfaction = base_satisfaction + wait_modifier + type_modifiers.get(attraction_type, 0)
        return max(0.1, min(1.0, final_satisfaction))
    
    def save_all_data(self):
        """Generate and save all theme park data"""
        print("🏰 Starting Disney Theme Park Data Generation...\n")
        
        # Generate attractions data
        attractions_df = self.generate_attractions_data()
        
        # Generate operational data
        operational_df = self.generate_operational_data(attractions_df, days=90)
        
        # Save data
        attractions_df.to_csv(self.raw_path / 'park_attractions.csv', index=False)
        operational_df.to_csv(self.raw_path / 'park_operations.csv', index=False)
        
        # Generate summary
        summary = {
            'generation_date': datetime.now().isoformat(),
            'total_attractions': len(attractions_df),
            'parks_included': list(self.parks.keys()),
            'operational_days': len(operational_df['date'].unique()),
            'total_operational_records': len(operational_df),
            'avg_daily_attendance': {
                park: int(operational_df[operational_df['park'] == park]['park_attendance'].mean())
                for park in self.parks.keys()
            }
        }
        
        with open(self.raw_path / 'generation_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"✅ Generated {len(attractions_df)} attractions across {len(self.parks)} parks")
        print(f"📊 Created {len(operational_df):,} operational records over 90 days")
        print(f"🎯 Average daily park attendance: {operational_df['park_attendance'].mean():,.0f}")
        
        return attractions_df, operational_df

if __name__ == "__main__":
    generator = DisneyParkDataGenerator()
    attractions_df, operational_df = generator.save_all_data()
    
    print(f"\n🎢 Attractions Summary:")
    print(attractions_df.groupby(['park', 'attraction_type']).size().unstack(fill_value=0))
    
    print(f"\n📈 Operational Insights:")
    print(f"• Busiest park: {operational_df.groupby('park')['total_guests'].sum().idxmax()}")
    print(f"• Average wait time: {operational_df['avg_wait_time_minutes'].mean():.1f} minutes")
    print(f"• Guest satisfaction: {operational_df['guest_satisfaction_score'].mean():.3f}")
    print(f"• Total revenue generated: ${operational_df['revenue_generated'].sum():,.0f}")