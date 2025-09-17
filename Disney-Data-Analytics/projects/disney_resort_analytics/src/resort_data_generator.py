"""
Disney Resort Data Generator

Generates fake data for the analytics pipeline. Started simple but got kind of complex...

TODO: The dining reservation logic is getting messy - need to refactor
TODO: Add more realistic seasonal booking patterns (spring break, etc)
NOTE: Some of the amenity pricing might be off - haven't validated against real Disney prices
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta, date
from typing import Dict, List, Tuple, Optional
import json
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# print("DEBUG: Logger initialized")  # left this in for troubleshooting

class DisneyResortDataGenerator:
    """Generate fake resort data for testing
    
    This class got pretty big - probably should split it up eventually
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.raw_path = self.base_path / 'data' / 'raw'
        self.processed_path = self.base_path / 'data' / 'processed'
        
        # Create directories
        self.raw_path.mkdir(parents=True, exist_ok=True)
        self.processed_path.mkdir(parents=True, exist_ok=True)
        
        # Set seeds so we get consistent data each run
        random.seed(42)
        np.random.seed(42)
        # TODO: make the seed configurable?
        
        # Resort data - got these from various Disney websites and forums
        # Some of the pricing might be outdated but should be close enough
        self.resorts = {
            'Grand Floridian': {
                'category': 'Deluxe Villa',
                'rooms': 847,
                'base_rate': 650,
                'amenities': ['spa', 'fine_dining', 'marina', 'wedding_chapel', 'childcare'],
                'transportation': ['monorail', 'boat'],
                'target_demographic': 'luxury_families'
            },
            'Polynesian': {
                'category': 'Deluxe',
                'rooms': 492,
                'base_rate': 550,
                'amenities': ['beach', 'luau', 'marina', 'spa', 'childcare'],
                'transportation': ['monorail', 'boat'],
                'target_demographic': 'families'
            },
            'Contemporary': {
                'category': 'Deluxe',
                'rooms': 655,
                'base_rate': 525,
                'amenities': ['marina', 'spa', 'convention_center', 'fine_dining'],
                'transportation': ['monorail', 'walking'],
                'target_demographic': 'business_leisure'
            },
            'Wilderness Lodge': {
                'category': 'Deluxe',
                'rooms': 729,
                'base_rate': 475,
                'amenities': ['nature_trails', 'hot_springs', 'marina', 'campfire'],
                'transportation': ['boat', 'bus'],
                'target_demographic': 'nature_families'
            },
            'Beach Club': {
                'category': 'Deluxe',
                'rooms': 583,
                'base_rate': 500,
                'amenities': ['beach_pool', 'spa', 'boardwalk', 'ice_cream'],
                'transportation': ['boat', 'walking'],
                'target_demographic': 'beach_families'
            },
            'Coronado Springs': {
                'category': 'Moderate',
                'rooms': 1917,
                'base_rate': 275,
                'amenities': ['convention_center', 'spa', 'lake', 'fitness'],
                'transportation': ['bus'],
                'target_demographic': 'business_budget'
            },
            'Port Orleans French Quarter': {
                'category': 'Moderate',
                'rooms': 1008,
                'base_rate': 225,
                'amenities': ['river', 'horse_carriage', 'beignets', 'pool'],
                'transportation': ['boat', 'bus'],
                'target_demographic': 'romantic_couples'
            },
            'Pop Century': {
                'category': 'Value',
                'rooms': 2880,
                'base_rate': 150,
                'amenities': ['themed_pools', 'food_court', 'arcade', 'laundry'],
                'transportation': ['bus', 'skyliner'],
                'target_demographic': 'budget_families'
            },
            'All Star Sports': {
                'category': 'Value',
                'rooms': 1920,
                'base_rate': 125,
                'amenities': ['themed_pools', 'food_court', 'arcade', 'sports'],
                'transportation': ['bus'],
                'target_demographic': 'sports_families'
            }
        }
        
        # Room Types
        self.room_types = {
            'Standard': {'capacity': 4, 'rate_multiplier': 1.0, 'probability': 0.6},
            'Pool View': {'capacity': 4, 'rate_multiplier': 1.2, 'probability': 0.15},
            'Park View': {'capacity': 4, 'rate_multiplier': 1.4, 'probability': 0.1},
            'Suite': {'capacity': 6, 'rate_multiplier': 2.0, 'probability': 0.08},
            'Villa': {'capacity': 8, 'rate_multiplier': 2.5, 'probability': 0.05},
            'Concierge': {'capacity': 4, 'rate_multiplier': 1.8, 'probability': 0.02}
        }
        
        # Guest Demographics
        self.guest_segments = {
            'Young Couples': {
                'age_range': (22, 35),
                'party_size': (2, 2),
                'budget_range': (2000, 5000),
                'stay_length': (3, 5),
                'preferences': ['romantic_dining', 'adult_activities', 'spa', 'fine_dining'],
                'probability': 0.15
            },
            'Families with Toddlers': {
                'age_range': (28, 40),
                'party_size': (3, 4),
                'budget_range': (3000, 7000),
                'stay_length': (4, 7),
                'preferences': ['character_dining', 'pool_time', 'early_dining', 'childcare'],
                'probability': 0.25
            },
            'Families with Teens': {
                'age_range': (35, 50),
                'party_size': (3, 5),
                'budget_range': (4000, 10000),
                'stay_length': (5, 8),
                'preferences': ['thrill_dining', 'late_dining', 'spa', 'recreation'],
                'probability': 0.20
            },
            'Multi-Generation': {
                'age_range': (45, 70),
                'party_size': (6, 10),
                'budget_range': (8000, 20000),
                'stay_length': (6, 10),
                'preferences': ['group_dining', 'accessible_options', 'varied_activities', 'concierge'],
                'probability': 0.15
            },
            'Empty Nesters': {
                'age_range': (50, 70),
                'party_size': (2, 2),
                'budget_range': (5000, 12000),
                'stay_length': (7, 14),
                'preferences': ['fine_dining', 'spa', 'cultural_activities', 'wine_experiences'],
                'probability': 0.12
            },
            'Business Travelers': {
                'age_range': (30, 55),
                'party_size': (1, 2),
                'budget_range': (2000, 6000),
                'stay_length': (2, 4),
                'preferences': ['quick_dining', 'fitness', 'business_services', 'efficiency'],
                'probability': 0.08
            },
            'International Families': {
                'age_range': (30, 50),
                'party_size': (4, 6),
                'budget_range': (6000, 15000),
                'stay_length': (8, 14),
                'preferences': ['cultural_dining', 'shopping', 'photography', 'unique_experiences'],
                'probability': 0.05
            }
        }
        
        # Dining Options
        self.restaurants = {
            'California Grill': {
                'resort': 'Contemporary',
                'type': 'Fine Dining',
                'cuisine': 'Contemporary American',
                'price_range': 'Signature',
                'capacity': 120,
                'avg_cost_pp': 85,
                'reservation_difficulty': 'High'
            },
            'Ohana': {
                'resort': 'Polynesian',
                'type': 'Character Dining',
                'cuisine': 'Polynesian',
                'price_range': 'Expensive',
                'capacity': 200,
                'avg_cost_pp': 65,
                'reservation_difficulty': 'Very High'
            },
            'Chef Mickeys': {
                'resort': 'Contemporary',
                'type': 'Character Dining',
                'cuisine': 'American Buffet',
                'price_range': 'Expensive',
                'capacity': 320,
                'avg_cost_pp': 62,
                'reservation_difficulty': 'Very High'
            },
            'Grand Floridian Cafe': {
                'resort': 'Grand Floridian',
                'type': 'Casual Dining',
                'cuisine': 'American',
                'price_range': 'Moderate',
                'capacity': 180,
                'avg_cost_pp': 45,
                'reservation_difficulty': 'Medium'
            },
            'Whispering Canyon': {
                'resort': 'Wilderness Lodge',
                'type': 'Family Dining',
                'cuisine': 'American BBQ',
                'price_range': 'Moderate',
                'capacity': 230,
                'avg_cost_pp': 48,
                'reservation_difficulty': 'Medium'
            },
            'Everything Pop': {
                'resort': 'Pop Century',
                'type': 'Quick Service',
                'cuisine': 'American Fast Food',
                'price_range': 'Budget',
                'capacity': 400,
                'avg_cost_pp': 15,
                'reservation_difficulty': 'None'
            }
        }
        
        # Amenity Services
        self.amenities = {
            'spa': {'base_cost': 120, 'duration': 90, 'satisfaction_impact': 0.3},
            'childcare': {'base_cost': 85, 'duration': 240, 'satisfaction_impact': 0.4},
            'marina': {'base_cost': 45, 'duration': 60, 'satisfaction_impact': 0.2},
            'fitness': {'base_cost': 0, 'duration': 45, 'satisfaction_impact': 0.1},
            'business_services': {'base_cost': 25, 'duration': 30, 'satisfaction_impact': 0.1},
            'laundry': {'base_cost': 15, 'duration': 120, 'satisfaction_impact': 0.05},
            'concierge': {'base_cost': 0, 'duration': 15, 'satisfaction_impact': 0.2}
        }
        
    def generate_guest_profiles(self, num_guests: int = 5000) -> pd.DataFrame:
        """Generate diverse guest profiles with realistic demographics"""
        logger.info(f"🏨 Generating {num_guests} guest profiles...")
        
        profiles = []
        guest_id = 10000
        
        for _ in range(num_guests):
            # Select guest segment
            segment_name = np.random.choice(
                list(self.guest_segments.keys()),
                p=[seg['probability'] for seg in self.guest_segments.values()]
            )
            segment = self.guest_segments[segment_name]
            
            # Generate demographics
            lead_guest_age = np.random.randint(segment['age_range'][0], segment['age_range'][1])
            party_size = np.random.randint(segment['party_size'][0], segment['party_size'][1] + 1)
            budget = np.random.uniform(segment['budget_range'][0], segment['budget_range'][1])
            
            # Generate preferences and characteristics
            loyalty_tier = np.random.choice(['None', 'Silver', 'Gold', 'Platinum'], 
                                          p=[0.4, 0.3, 0.2, 0.1])
            
            previous_visits = np.random.poisson(2) if loyalty_tier != 'None' else np.random.poisson(0.5)
            
            # Special needs/accessibility
            accessibility_needs = np.random.choice([True, False], p=[0.15, 0.85])
            
            # Celebration status
            celebration = np.random.choice([None, 'Birthday', 'Anniversary', 'Honeymoon', 'Graduation'],
                                         p=[0.7, 0.1, 0.08, 0.07, 0.05])
            
            profiles.append({
                'guest_id': guest_id,
                'segment': segment_name,
                'lead_guest_age': lead_guest_age,
                'party_size': party_size,
                'annual_budget': int(budget),
                'loyalty_tier': loyalty_tier,
                'previous_visits': previous_visits,
                'accessibility_needs': accessibility_needs,
                'celebration': celebration,
                'preferences': segment['preferences'],
                'avg_stay_length': np.random.uniform(segment['stay_length'][0], segment['stay_length'][1]),
                'price_sensitivity': np.random.uniform(0.3, 0.9),  # Higher = more price sensitive
                'service_expectations': np.random.uniform(0.5, 1.0)  # Higher = higher expectations
            })
            
            guest_id += 1
        
        df = pd.DataFrame(profiles)
        logger.info(f"✅ Generated guest profiles: {len(df)} records")
        return df
    
    def generate_bookings(self, guest_profiles: pd.DataFrame, months: int = 12) -> pd.DataFrame:
        """Generate booking data - this method does a lot, probably too much"""
        logger.info(f"📅 Generating {months} months of booking data...")
        # print(f"DEBUG: Got {len(guest_profiles)} guest profiles to work with")
        
        bookings = []
        booking_id = 50000  # arbitrary starting point
        start_dt = datetime.now() - timedelta(days=months * 30)
        
        # Generate seasonal booking patterns
        for month_offset in range(months):
            current_month = start_dt + timedelta(days=month_offset * 30)
            
            # Seasonal demand multipliers
            seasonal_demand = self._get_seasonal_demand(current_month)
            
            # Generate bookings for this month - 500 base is kinda arbitrary
            monthly_bookings = int(500 * seasonal_demand * np.random.uniform(0.8, 1.2))
            # if month_offset < 3:  # debug for first few months
            #     print(f"Month {month_offset}: {monthly_bookings} bookings, demand={seasonal_demand}")
            
            for _ in range(monthly_bookings):
                # Select guest
                guest = guest_profiles.sample(1).iloc[0]
                
                # Generate booking details
                booking_data = self._create_booking_record(booking_id, guest, current_month)
                bookings.append(booking_data)
                booking_id += 1
        
        df = pd.DataFrame(bookings)
        logger.info(f"✅ Generated bookings: {len(df)} records")
        return df
    
    def _create_booking_record(self, booking_id: int, guest: pd.Series, month: datetime) -> Dict:
        """Create individual booking record with realistic patterns"""
        
        # Select resort based on guest segment and budget
        suitable_resorts = self._filter_resorts_by_budget_and_preferences(guest)
        resort_name = np.random.choice(suitable_resorts)
        resort = self.resorts[resort_name]
        
        # Select room type
        room_type = np.random.choice(
            list(self.room_types.keys()),
            p=[rt['probability'] for rt in self.room_types.values()]
        )
        
        # Generate stay dates
        stay_length = max(1, int(np.random.normal(guest['avg_stay_length'], 1)))
        
        # Booking timing (advance booking patterns)
        days_advance = self._generate_booking_advance_days(guest['segment'], resort['category'])
        booking_date = month - timedelta(days=days_advance)
        checkin_date = month + timedelta(days=np.random.randint(0, 28))
        checkout_date = checkin_date + timedelta(days=stay_length)
        
        # Pricing calculation - this got complex over time
        base_rate = resort['base_rate']
        room_mult = self.room_types[room_type]['rate_multiplier']
        seasonal_mult = self._get_pricing_multiplier(checkin_date)
        
        daily_rate = base_rate * room_mult * seasonal_mult
        
        # Dynamic pricing adjustments - should probably be more sophisticated
        if guest['loyalty_tier'] in ['Gold', 'Platinum']:
            daily_rate *= 0.9  # 10% loyalty discount
        
        total_cost = daily_rate * stay_length  # simple multiplication for now
        
        # Booking channel
        channel = np.random.choice(['Direct Website', 'Disney App', 'Travel Agent', 'Phone'],
                                 p=[0.45, 0.25, 0.2, 0.1])
        
        # Payment and booking characteristics
        is_refundable = np.random.choice([True, False], p=[0.7, 0.3])
        special_requests = self._generate_special_requests(guest)
        
        return {
            'booking_id': booking_id,
            'guest_id': guest['guest_id'],
            'resort_name': resort_name,
            'room_type': room_type,
            'booking_date': booking_date.strftime('%Y-%m-%d'),
            'checkin_date': checkin_date.strftime('%Y-%m-%d'),
            'checkout_date': checkout_date.strftime('%Y-%m-%d'),
            'stay_length': stay_length,
            'daily_rate': round(daily_rate, 2),
            'total_cost': round(total_cost, 2),
            'party_size': guest['party_size'],
            'booking_channel': channel,
            'is_refundable': is_refundable,
            'special_requests': special_requests,
            'days_advance_booked': days_advance,
            'seasonal_multiplier': round(seasonal_mult, 2)  # keep track for analysis
        }
    
    def generate_dining_reservations(self, bookings: pd.DataFrame, guest_profiles: pd.DataFrame) -> pd.DataFrame:
        """Generate dining reservation patterns based on guest preferences and resort choice"""
        logger.info("🍽️ Generating dining reservations...")
        
        dining_reservations = []
        reservation_id = 70000
        
        for _, booking in bookings.iterrows():
            guest = guest_profiles[guest_profiles['guest_id'] == booking['guest_id']].iloc[0]
            
            # Determine dining frequency (meals per day)
            dining_frequency = self._get_dining_frequency(guest['segment'], booking['resort_name'])
            
            checkin = pd.to_datetime(booking['checkin_date'])
            stay_length = booking['stay_length']
            
            # Generate dining reservations for each day of stay
            for day in range(stay_length):
                current_date = checkin + timedelta(days=day)
                daily_meals = np.random.poisson(dining_frequency)
                
                for meal in range(daily_meals):
                    # Select restaurant based on preferences and resort
                    restaurant = self._select_restaurant(guest, booking['resort_name'])
                    
                    if restaurant:
                        dining_data = self._create_dining_reservation(
                            reservation_id, booking, guest, restaurant, current_date
                        )
                        dining_reservations.append(dining_data)
                        reservation_id += 1
        
        df = pd.DataFrame(dining_reservations)
        logger.info(f"✅ Generated dining reservations: {len(df)} records")
        return df
    
    def generate_amenity_usage(self, bookings: pd.DataFrame, guest_profiles: pd.DataFrame) -> pd.DataFrame:
        """Generate amenity and service usage patterns"""
        logger.info("🏊 Generating amenity usage data...")
        
        amenity_usage = []
        usage_id = 90000
        
        for _, booking in bookings.iterrows():
            guest = guest_profiles[guest_profiles['guest_id'] == booking['guest_id']].iloc[0]
            resort = self.resorts[booking['resort_name']]
            
            checkin = pd.to_datetime(booking['checkin_date'])
            stay_length = booking['stay_length']
            
            # Generate amenity usage for each day
            for day in range(stay_length):
                current_date = checkin + timedelta(days=day)
                
                # Determine which amenities guest might use
                for amenity in resort['amenities']:
                    if amenity in guest['preferences']:
                        use_probability = 0.4
                    else:
                        use_probability = 0.1
                    
                    if np.random.random() < use_probability:
                        usage_data = self._create_amenity_usage_record(
                            usage_id, booking, guest, amenity, current_date
                        )
                        amenity_usage.append(usage_data)
                        usage_id += 1
        
        df = pd.DataFrame(amenity_usage)
        logger.info(f"✅ Generated amenity usage: {len(df)} records")
        return df
    
    def _filter_resorts_by_budget_and_preferences(self, guest: pd.Series) -> List[str]:
        """Filter resorts based on guest budget and preferences"""
        suitable_resorts = []
        daily_budget = guest['annual_budget'] / (guest['avg_stay_length'] * 4)  # Assume 4 trips per year
        
        for resort_name, resort in self.resorts.items():
            if resort['base_rate'] <= daily_budget * 1.5:  # Allow some flexibility
                suitable_resorts.append(resort_name)
        
        return suitable_resorts if suitable_resorts else ['Pop Century']  # Fallback
    
    def _get_seasonal_demand(self, date: datetime) -> float:
        """Calculate seasonal demand multiplier"""
        month = date.month
        
        # Peak seasons
        if month in [6, 7, 8]:  # Summer
            return 1.4
        elif month in [11, 12, 1]:  # Holiday season
            return 1.6
        elif month in [3, 4]:  # Spring break
            return 1.2
        else:  # Off-peak
            return 0.8
    
    def _get_pricing_multiplier(self, date: datetime) -> float:
        """Calculate dynamic pricing multiplier based on demand"""
        base_multiplier = self._get_seasonal_demand(date)
        
        # Weekend premium
        if date.weekday() >= 5:
            base_multiplier *= 1.2
        
        # Special events (simplified)
        if date.month == 10:  # Halloween season
            base_multiplier *= 1.1
        elif date.month == 12 and date.day > 20:  # Christmas week
            base_multiplier *= 1.5
        
        return base_multiplier
    
    def _generate_booking_advance_days(self, segment: str, resort_category: str) -> int:
        """Generate realistic booking advance patterns"""
        if segment == 'Business Travelers':
            return np.random.randint(1, 30)
        elif resort_category == 'Deluxe Villa':
            return np.random.randint(60, 365)
        elif segment == 'International Families':
            return np.random.randint(90, 240)
        else:
            return np.random.randint(30, 180)
    
    def _generate_special_requests(self, guest: pd.Series) -> List[str]:
        """Generate realistic special requests"""
        requests = []
        
        if guest['celebration']:
            requests.append(f"celebrating_{guest['celebration'].lower()}")
        
        if guest['accessibility_needs']:
            requests.append('accessibility_required')
        
        if 'childcare' in guest['preferences']:
            requests.append('crib_needed')
        
        if guest['loyalty_tier'] in ['Gold', 'Platinum']:
            if np.random.random() < 0.3:
                requests.append('room_upgrade_request')
        
        return requests
    
    def _get_dining_frequency(self, segment: str, resort_name: str) -> float:
        """Calculate expected daily dining reservations"""
        base_frequency = {
            'Young Couples': 1.5,
            'Families with Toddlers': 2.0,
            'Families with Teens': 1.8,
            'Multi-Generation': 2.2,
            'Empty Nesters': 1.7,
            'Business Travelers': 1.0,
            'International Families': 2.5
        }
        
        frequency = base_frequency.get(segment, 1.5)
        
        # Resort category adjustment
        resort_category = self.resorts[resort_name]['category']
        if resort_category == 'Deluxe Villa':
            frequency *= 1.2
        elif resort_category == 'Value':
            frequency *= 0.7
        
        return frequency
    
    def _select_restaurant(self, guest: pd.Series, resort_name: str) -> Optional[str]:
        """Select restaurant based on guest preferences and location"""
        # Filter restaurants by location and preferences
        suitable_restaurants = []
        
        for restaurant_name, restaurant in self.restaurants.items():
            if restaurant['resort'] == resort_name or np.random.random() < 0.2:  # 20% chance of off-resort dining
                # Check if restaurant type matches preferences
                if any(pref in restaurant['type'].lower() or pref in restaurant['cuisine'].lower() 
                      for pref in guest['preferences']):
                    suitable_restaurants.append(restaurant_name)
        
        if suitable_restaurants:
            return np.random.choice(suitable_restaurants)
        
        # Fallback to any restaurant at resort
        resort_restaurants = [name for name, rest in self.restaurants.items() 
                            if rest['resort'] == resort_name]
        return np.random.choice(resort_restaurants) if resort_restaurants else None
    
    def _create_dining_reservation(self, reservation_id: int, booking: Dict, guest: pd.Series, 
                                 restaurant_name: str, date: datetime) -> Dict:
        """Create dining reservation record"""
        restaurant = self.restaurants[restaurant_name]
        
        # Generate reservation details
        party_size = min(booking['party_size'], 8)  # Restaurant capacity limits
        meal_time = np.random.choice(['Breakfast', 'Lunch', 'Dinner'], p=[0.2, 0.3, 0.5])
        
        # Calculate cost
        base_cost = restaurant['avg_cost_pp'] * party_size
        
        # Apply adjustments
        if guest['celebration']:
            base_cost *= 1.2  # Celebration surcharge
        
        if guest['loyalty_tier'] in ['Gold', 'Platinum']:
            base_cost *= 0.95  # Loyalty discount
        
        return {
            'reservation_id': reservation_id,
            'booking_id': booking['booking_id'],
            'guest_id': booking['guest_id'],
            'restaurant_name': restaurant_name,
            'reservation_date': date.strftime('%Y-%m-%d'),
            'meal_time': meal_time,
            'party_size': party_size,
            'estimated_cost': round(base_cost, 2),
            'cuisine_type': restaurant['cuisine'],
            'price_range': restaurant['price_range']
        }
    
    def _create_amenity_usage_record(self, usage_id: int, booking: Dict, guest: pd.Series,
                                   amenity: str, date: datetime) -> Dict:
        """Create amenity usage record"""
        if amenity not in self.amenities:
            return None
        
        amenity_info = self.amenities[amenity]
        
        # Generate usage details
        duration = int(np.random.normal(amenity_info['duration'], amenity_info['duration'] * 0.2))
        cost = amenity_info['base_cost']
        
        # Loyalty discounts
        if guest['loyalty_tier'] in ['Gold', 'Platinum'] and cost > 0:
            cost *= 0.9
        
        return {
            'usage_id': usage_id,
            'booking_id': booking['booking_id'],
            'guest_id': booking['guest_id'],
            'amenity_type': amenity,
            'usage_date': date.strftime('%Y-%m-%d'),
            'duration_minutes': duration,
            'cost': round(cost, 2) if cost > 0 else 0,
            'satisfaction_impact': amenity_info['satisfaction_impact']
        }
    
    def save_datasets(self, guest_profiles: pd.DataFrame, bookings: pd.DataFrame, 
                     dining: pd.DataFrame, amenities: pd.DataFrame):
        """Save all generated datasets"""
        try:
            # Save raw data
            guest_profiles.to_csv(self.raw_path / 'guest_profiles.csv', index=False)
            bookings.to_csv(self.raw_path / 'resort_bookings.csv', index=False)
            dining.to_csv(self.raw_path / 'dining_reservations.csv', index=False)
            amenities.to_csv(self.raw_path / 'amenity_usage.csv', index=False)
            
            # Generate summary statistics
            summary = {
                'generation_date': datetime.now().isoformat(),
                'total_guests': len(guest_profiles),
                'total_bookings': len(bookings),
                'total_dining_reservations': len(dining),
                'total_amenity_usage': len(amenities),
                'date_range': {
                    'start': bookings['checkin_date'].min(),
                    'end': bookings['checkout_date'].max()
                },
                'total_revenue': {
                    'room_revenue': int(bookings['total_cost'].sum()),
                    'dining_revenue': int(dining['estimated_cost'].sum()),
                    'amenity_revenue': int(amenities['cost'].sum())
                },
                'average_metrics': {
                    'stay_length': round(bookings['stay_length'].mean(), 2),
                    'party_size': round(bookings['party_size'].mean(), 2),
                    'advance_booking_days': round(bookings['days_advance_booked'].mean(), 1)
                }
            }
            
            with open(self.raw_path / 'generation_summary.json', 'w') as f:
                json.dump(summary, f, indent=2)
            
            logger.info("✅ All datasets saved successfully")
            logger.info(f"📊 Generated {len(guest_profiles):,} guest profiles")
            logger.info(f"🏨 Generated {len(bookings):,} resort bookings")  
            logger.info(f"🍽️ Generated {len(dining):,} dining reservations")
            logger.info(f"🏊 Generated {len(amenities):,} amenity usage records")
            logger.info(f"💰 Total simulated revenue: ${summary['total_revenue']['room_revenue'] + summary['total_revenue']['dining_revenue'] + summary['total_revenue']['amenity_revenue']:,}")
            
        except Exception as e:
            logger.error(f"❌ Error saving datasets: {e}")
            raise

def main():
    """Generate comprehensive Disney resort dataset"""
    generator = DisneyResortDataGenerator()
    
    print("🏨 Starting Disney Resort Data Generation...")
    
    # Generate datasets
    guest_profiles = generator.generate_guest_profiles(num_guests=5000)
    bookings = generator.generate_bookings(guest_profiles, months=12)
    dining = generator.generate_dining_reservations(bookings, guest_profiles)
    amenities = generator.generate_amenity_usage(bookings, guest_profiles)
    
    # Save all datasets
    generator.save_datasets(guest_profiles, bookings, dining, amenities)
    
    print("\n✅ Disney Resort Data Generation Complete!")
    print("🏨 Ready for guest analytics and revenue optimization")

if __name__ == "__main__":
    main()