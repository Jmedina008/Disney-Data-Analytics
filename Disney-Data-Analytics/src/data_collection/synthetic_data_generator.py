"""
Synthetic Disney Data Generator
Creates realistic Disney movie, theme park, and streaming data for portfolio demonstration.
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from pathlib import Path
import random
from typing import Dict, List, Tuple

class DisneyDataGenerator:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.data_path = self.base_path / 'data' / 'samples'
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # Disney-specific data
        self.disney_studios = [
            'Walt Disney Pictures', 'Walt Disney Animation Studios', 'Pixar Animation Studios',
            'Marvel Studios', 'Lucasfilm', '20th Century Studios', 'Searchlight Pictures'
        ]
        
        self.genres = [
            'Animation', 'Adventure', 'Family', 'Fantasy', 'Action', 'Comedy', 
            'Drama', 'Science Fiction', 'Musical', 'Romance', 'Thriller'
        ]
        
        self.disney_franchises = [
            'Marvel Cinematic Universe', 'Star Wars', 'Toy Story', 'The Incredibles',
            'Cars', 'Frozen', 'Lion King', 'Aladdin', 'Beauty and the Beast', 
            'Pirates of the Caribbean', 'Alice in Wonderland', 'Jungle Book'
        ]
        
        # Theme park data
        self.disney_parks = {
            'WDW_MK': {'name': 'Magic Kingdom', 'location': 'Orlando, FL'},
            'WDW_EP': {'name': 'EPCOT', 'location': 'Orlando, FL'},
            'WDW_HS': {'name': 'Hollywood Studios', 'location': 'Orlando, FL'},
            'WDW_AK': {'name': 'Animal Kingdom', 'location': 'Orlando, FL'},
            'DLR_DL': {'name': 'Disneyland', 'location': 'Anaheim, CA'},
            'DLR_CA': {'name': 'California Adventure', 'location': 'Anaheim, CA'}
        }
        
    def generate_movie_data(self, num_movies: int = 200) -> pd.DataFrame:
        """Generate synthetic Disney movie data"""
        
        # Generate movie titles
        base_titles = [
            "The Magical Kingdom", "Enchanted Forest", "Ocean's Dream", "Sky Adventure",
            "The Lost Princess", "Dragon's Quest", "Starlight Journey", "Crystal Palace",
            "The Brave Knight", "Mystic Island", "Golden Crown", "Silver Moon",
            "The Secret Garden", "Rainbow Bridge", "Diamond Castle", "Emerald City",
            "The Flying Carpet", "Magic Lamp", "Treasure Map", "The Dancing Shoes"
        ]
        
        movies = []
        for i in range(num_movies):
            # Generate realistic release dates (1990-2024)
            start_date = datetime(1990, 1, 1)
            end_date = datetime(2024, 12, 31)
            time_between = end_date - start_date
            days_between = time_between.days
            random_days = random.randrange(days_between)
            release_date = start_date + timedelta(days=random_days)
            
            # Generate budget based on year (inflation adjusted)
            year = release_date.year
            base_budget = 50_000_000  # $50M base
            inflation_multiplier = (year - 1990) * 0.03 + 1  # 3% annual increase
            budget = base_budget * inflation_multiplier * random.uniform(0.5, 4.0)
            
            # Generate revenue with realistic patterns
            # Higher budgets generally correlate with higher revenue, but with variance
            budget_factor = budget / 100_000_000  # Normalize to $100M
            base_revenue = budget * random.uniform(1.5, 8.0)  # 1.5x to 8x return
            
            # Add seasonal effects (summer and holiday releases perform better)
            seasonal_multiplier = 1.0
            if release_date.month in [6, 7, 11, 12]:  # Summer and holidays
                seasonal_multiplier = random.uniform(1.2, 1.8)
            elif release_date.month in [1, 2, 9, 10]:  # Slower months
                seasonal_multiplier = random.uniform(0.7, 1.1)
                
            revenue = base_revenue * seasonal_multiplier
            
            # Generate other metrics
            runtime = random.randint(80, 180)  # 80-180 minutes
            vote_average = random.uniform(5.5, 9.0)
            vote_count = int(random.uniform(1000, 50000))
            popularity = random.uniform(10, 100)
            
            # Assign studio and franchise
            studio = random.choice(self.disney_studios)
            franchise = random.choice(self.disney_franchises + [None] * 5)  # 30% have franchise
            
            # Generate title
            if franchise and random.random() < 0.7:  # 70% chance to use franchise name
                title = f"{franchise}: {random.choice(base_titles)}"
            else:
                title = random.choice(base_titles) + f" {random.randint(1, 10)}"
            
            movie = {
                'id': 10000 + i,
                'title': title,
                'release_date': release_date.strftime('%Y-%m-%d'),
                'budget': int(budget),
                'revenue': int(revenue),
                'runtime': runtime,
                'vote_average': round(vote_average, 1),
                'vote_count': vote_count,
                'popularity': round(popularity, 1),
                'studio': studio,
                'franchise': franchise,
                'genres': random.sample(self.genres, random.randint(1, 3)),
                'production_countries': ['United States'] + random.sample(['Canada', 'United Kingdom'], random.randint(0, 1))
            }
            
            # Calculate derived metrics
            movie['roi'] = ((revenue - budget) / budget * 100) if budget > 0 else 0
            movie['profit'] = revenue - budget
            movie['budget_millions'] = budget / 1_000_000
            movie['revenue_millions'] = revenue / 1_000_000
            movie['release_year'] = release_date.year
            movie['release_month'] = release_date.month
            movie['is_sequel'] = 1 if any(char.isdigit() for char in title) else 0
            movie['is_franchise'] = 1 if franchise else 0
            
            movies.append(movie)
        
        df = pd.DataFrame(movies)
        
        # Add some realistic correlations
        # Pixar and Marvel tend to perform better
        pixar_mask = df['studio'] == 'Pixar Animation Studios'
        marvel_mask = df['studio'] == 'Marvel Studios'
        df.loc[pixar_mask, 'vote_average'] += random.uniform(0.3, 0.8)
        df.loc[marvel_mask, 'revenue'] *= random.uniform(1.2, 1.5)
        
        # Clamp values to realistic ranges
        df['vote_average'] = df['vote_average'].clip(1.0, 10.0)
        df['revenue'] = df['revenue'].clip(0, None)
        df['roi'] = df['roi'].clip(-90, 1000)  # -90% to 1000% ROI
        
        return df
    
    def generate_theme_park_data(self, days: int = 365) -> pd.DataFrame:
        """Generate synthetic theme park wait time data"""
        
        attractions = {
            'WDW_MK': [
                'Space Mountain', 'Pirates of the Caribbean', 'Haunted Mansion',
                'Big Thunder Mountain', 'Splash Mountain', 'It\'s a Small World',
                'Peter Pan\'s Flight', 'Seven Dwarfs Mine Train'
            ],
            'WDW_EP': [
                'Test Track', 'Soarin\'', 'Spaceship Earth', 'Frozen Ever After',
                'The Seas with Nemo & Friends', 'Journey Into Imagination'
            ],
            'WDW_HS': [
                'Rise of the Resistance', 'Millennium Falcon: Smugglers Run',
                'Tower of Terror', 'Rock \'n\' Roller Coaster', 'Toy Story Midway Mania'
            ],
            'WDW_AK': [
                'Avatar Flight of Passage', 'Expedition Everest', 'Kilimanjaro Safaris',
                'DINOSAUR', 'Kali River Rapids'
            ],
            'DLR_DL': [
                'Space Mountain', 'Pirates of the Caribbean', 'Indiana Jones Adventure',
                'Matterhorn Bobsleds', 'Star Wars: Rise of the Resistance'
            ],
            'DLR_CA': [
                'Guardians of the Galaxy', 'Incredicoaster', 'Soarin\' Around the World',
                'Cars Land Racers', 'Toy Story Midway Mania'
            ]
        }
        
        wait_times = []
        start_date = datetime.now() - timedelta(days=days)
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            is_weekend = current_date.weekday() >= 5
            is_holiday = current_date.month in [6, 7, 11, 12]  # Peak seasons
            
            for park_id, park_attractions in attractions.items():
                for attraction in park_attractions:
                    # Generate hourly wait times (park hours: 9 AM - 10 PM)
                    for hour in range(9, 22):
                        # Base wait time varies by attraction popularity
                        if 'Rise of the Resistance' in attraction or 'Avatar Flight' in attraction:
                            base_wait = random.randint(60, 180)  # Popular attractions
                        elif 'Space Mountain' in attraction or 'Pirates' in attraction:
                            base_wait = random.randint(30, 90)   # Classic attractions
                        else:
                            base_wait = random.randint(15, 60)   # Regular attractions
                        
                        # Adjust for time of day
                        time_multiplier = 1.0
                        if 10 <= hour <= 12 or 14 <= hour <= 17:  # Peak hours
                            time_multiplier = random.uniform(1.3, 1.8)
                        elif hour <= 9 or hour >= 20:  # Early/late hours
                            time_multiplier = random.uniform(0.5, 0.8)
                        
                        # Adjust for day type
                        day_multiplier = 1.0
                        if is_weekend:
                            day_multiplier *= random.uniform(1.2, 1.6)
                        if is_holiday:
                            day_multiplier *= random.uniform(1.3, 1.9)
                        
                        wait_time = int(base_wait * time_multiplier * day_multiplier)
                        wait_time = max(5, min(wait_time, 240))  # 5-240 minutes
                        
                        wait_times.append({
                            'timestamp': current_date.replace(hour=hour),
                            'park_id': park_id,
                            'park_name': self.disney_parks[park_id]['name'],
                            'attraction_name': attraction,
                            'wait_time': wait_time,
                            'is_weekend': is_weekend,
                            'is_holiday': is_holiday,
                            'hour': hour,
                            'day_of_week': current_date.strftime('%A'),
                            'month': current_date.month
                        })
        
        return pd.DataFrame(wait_times)
    
    def generate_streaming_data(self, num_titles: int = 150) -> pd.DataFrame:
        """Generate synthetic Disney+ streaming data"""
        
        content_types = ['Movie', 'Series', 'Documentary', 'Short']
        disney_plus_content = [
            'The Mandalorian', 'WandaVision', 'The Falcon and the Winter Soldier',
            'Loki', 'What If...?', 'Hawkeye', 'Moon Knight', 'Ms. Marvel',
            'Soul', 'Luca', 'Turning Red', 'Encanto', 'Moana', 'Frozen 2',
            'Toy Story 4', 'Incredibles 2', 'Finding Dory', 'Coco', 'Onward'
        ]
        
        streaming_data = []
        
        for i in range(num_titles):
            title = f"{random.choice(disney_plus_content)} {random.randint(1, 10)}"
            content_type = random.choice(content_types)
            
            # Generate viewership data
            total_views = random.randint(1_000_000, 100_000_000)
            completion_rate = random.uniform(0.6, 0.95)
            average_watch_time = random.randint(20, 120)  # minutes
            
            streaming_data.append({
                'title': title,
                'content_type': content_type,
                'release_date': (datetime.now() - timedelta(days=random.randint(1, 365*3))).strftime('%Y-%m-%d'),
                'total_views': total_views,
                'unique_viewers': int(total_views * random.uniform(0.7, 0.9)),
                'completion_rate': round(completion_rate, 3),
                'average_watch_time_minutes': average_watch_time,
                'total_watch_hours': int(total_views * average_watch_time / 60),
                'user_rating': round(random.uniform(3.5, 5.0), 1),
                'genres': random.sample(self.genres, random.randint(1, 3))
            })
        
        return pd.DataFrame(streaming_data)
    
    def save_all_data(self):
        """Generate and save all synthetic datasets"""
        
        print("🎬 Generating Disney movie data...")
        movies_df = self.generate_movie_data(200)
        movies_df.to_csv(self.data_path / 'disney_movies.csv', index=False)
        movies_df.to_parquet(self.data_path / 'disney_movies.parquet', index=False)
        
        print("🎡 Generating theme park data...")
        theme_park_df = self.generate_theme_park_data(365)
        theme_park_df.to_csv(self.data_path / 'theme_park_wait_times.csv', index=False)
        theme_park_df.to_parquet(self.data_path / 'theme_park_wait_times.parquet', index=False)
        
        print("📺 Generating streaming data...")
        streaming_df = self.generate_streaming_data(150)
        streaming_df.to_csv(self.data_path / 'disney_plus_content.csv', index=False)
        streaming_df.to_parquet(self.data_path / 'disney_plus_content.parquet', index=False)
        
        # Generate summary statistics
        summary = {
            'generation_date': datetime.now().isoformat(),
            'datasets': {
                'movies': {
                    'count': len(movies_df),
                    'date_range': f"{movies_df['release_date'].min()} to {movies_df['release_date'].max()}",
                    'total_revenue': f"${movies_df['revenue'].sum():,}",
                    'avg_budget': f"${movies_df['budget'].mean():.0f}"
                },
                'theme_parks': {
                    'count': len(theme_park_df),
                    'parks': len(theme_park_df['park_id'].unique()),
                    'attractions': len(theme_park_df['attraction_name'].unique()),
                    'avg_wait_time': f"{theme_park_df['wait_time'].mean():.1f} minutes"
                },
                'streaming': {
                    'count': len(streaming_df),
                    'total_views': f"{streaming_df['total_views'].sum():,}",
                    'avg_completion_rate': f"{streaming_df['completion_rate'].mean():.1%}"
                }
            }
        }
        
        with open(self.data_path / 'data_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"✅ All synthetic data generated and saved to {self.data_path}")
        print(f"📊 Generated {len(movies_df)} movies, {len(theme_park_df)} wait time records, {len(streaming_df)} streaming titles")
        
        return movies_df, theme_park_df, streaming_df

if __name__ == "__main__":
    generator = DisneyDataGenerator()
    generator.save_all_data()