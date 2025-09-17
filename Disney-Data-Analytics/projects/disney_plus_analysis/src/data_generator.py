"""
Advanced Disney+ Content Data Generator
Creates comprehensive synthetic dataset for content analytics and ML modeling
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from typing import Dict, List
import json
from pathlib import Path

class DisneyPlusDataGenerator:
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
        
        self.genres = [
            'Animation', 'Adventure', 'Family', 'Fantasy', 'Action', 'Comedy',
            'Drama', 'Documentary', 'Musical', 'Romance', 'Thriller', 'Science Fiction'
        ]
        
        self.disney_studios = [
            'Walt Disney Pictures', 'Pixar Animation Studios', 'Marvel Studios',
            'Lucasfilm', '20th Century Studios', 'Disney Channel', 'National Geographic'
        ]
        
        self.franchises = [
            'Marvel Cinematic Universe', 'Star Wars', 'Pixar', 'Disney Classics',
            'Toy Story', 'Cars', 'Frozen', 'Lion King', 'Pirates of the Caribbean'
        ]
    
    def generate_content_catalog(self, n_content: int = 1500) -> pd.DataFrame:
        """Generate comprehensive Disney+ content catalog"""
        
        content_data = []
        
        for i in range(n_content):
            # Basic content info
            content_type = np.random.choice(['Movie', 'Series', 'Documentary', 'Short'], 
                                          p=[0.4, 0.3, 0.2, 0.1])
            studio = np.random.choice(self.disney_studios)
            franchise = np.random.choice(self.franchises + [None]*6)  # 40% have franchise
            
            # Generate title
            if franchise:
                title = f"{franchise}: Episode {i+1}"
            else:
                title = f"Disney Original {i+1}"
            
            # Release timing
            release_date = datetime(2015, 1, 1) + timedelta(days=random.randint(0, 3285))
            disney_plus_date = max(release_date, datetime(2019, 11, 12))
            
            # Content characteristics
            genres = np.random.choice(self.genres, size=np.random.randint(1, 3), replace=False).tolist()
            
            # Duration and episodes
            if content_type == 'Movie':
                duration = np.random.normal(105, 25)
                duration = max(60, min(240, duration))
                episodes = 1
                seasons = 1
            elif content_type == 'Series':
                episodes = np.random.randint(8, 50)
                seasons = max(1, episodes // np.random.randint(8, 16))
                duration = np.random.normal(45, 15)
            else:
                duration = np.random.normal(60, 20)
                episodes = 1
                seasons = 1
            
            # Ratings and popularity
            imdb_rating = self._generate_realistic_rating(studio, franchise)
            
            # Viewing metrics
            total_views = self._calculate_views(studio, franchise, imdb_rating)
            completion_rate = max(0.4, min(1.0, 0.65 + (imdb_rating - 7) * 0.1))
            
            content_entry = {
                'content_id': f'DP_{i+10000}',
                'title': title,
                'content_type': content_type,
                'studio': studio,
                'franchise': franchise,
                'primary_genre': genres[0] if genres else 'Family',
                'all_genres': '|'.join(genres),
                'release_date': release_date.strftime('%Y-%m-%d'),
                'disney_plus_date': disney_plus_date.strftime('%Y-%m-%d'),
                'duration_minutes': round(duration),
                'episodes': episodes,
                'seasons': seasons,
                'imdb_rating': round(imdb_rating, 1),
                'total_views': int(total_views),
                'unique_viewers': int(total_views * 0.8),
                'completion_rate': round(completion_rate, 3),
                'average_watch_time': round(duration * completion_rate, 1),
                'engagement_score': round(np.random.uniform(0.1, 0.9), 3),
                'is_original': np.random.choice([True, False], p=[0.3, 0.7]),
                'production_budget': self._estimate_budget(content_type, studio, duration, episodes),
                'critic_score': round(max(0, min(100, imdb_rating * 10 + np.random.normal(0, 15))), 1)
            }
            
            content_data.append(content_entry)
        
        return pd.DataFrame(content_data)
    
    def _generate_realistic_rating(self, studio: str, franchise: str) -> float:
        """Generate realistic IMDB ratings"""
        base_rating = 6.5
        
        # Studio effects
        if studio == 'Pixar Animation Studios':
            base_rating += 1.2
        elif studio == 'Marvel Studios':
            base_rating += 0.8
        elif studio == 'National Geographic':
            base_rating += 0.9
        
        # Franchise bonus
        if franchise:
            base_rating += 0.5
        
        # Add variation
        rating = base_rating + np.random.normal(0, 0.8)
        return max(4.0, min(9.2, rating))
    
    def _calculate_views(self, studio: str, franchise: str, rating: float) -> int:
        """Calculate viewership based on content characteristics"""
        base_views = 500000
        
        # Studio multipliers
        if studio == 'Marvel Studios':
            base_views *= 3.0
        elif studio == 'Pixar Animation Studios':
            base_views *= 2.5
        elif studio == 'Lucasfilm':
            base_views *= 2.2
        
        # Franchise bonus
        if franchise:
            base_views *= 1.8
        
        # Rating effect
        base_views *= (rating / 7.0) ** 1.5
        
        return int(base_views * np.random.uniform(0.3, 3.0))
    
    def _estimate_budget(self, content_type: str, studio: str, duration: float, episodes: int) -> int:
        """Estimate production budget"""
        if content_type == 'Movie':
            if studio in ['Marvel Studios', 'Lucasfilm']:
                budget = 200_000_000
            elif studio == 'Pixar Animation Studios':
                budget = 150_000_000
            else:
                budget = 80_000_000
        else:
            budget = 10_000_000 * episodes
        
        return int(budget * np.random.uniform(0.7, 1.5))
    
    def save_data(self):
        """Generate and save all data"""
        print("🎬 Generating Disney+ content data...")
        
        content_df = self.generate_content_catalog(1500)
        
        # Save to both raw and processed
        content_df.to_csv(self.raw_path / 'disney_plus_content.csv', index=False)
        content_df.to_csv(self.processed_path / 'disney_plus_content_processed.csv', index=False)
        
        # Generate summary
        summary = {
            'total_content': int(len(content_df)),
            'avg_rating': float(content_df['imdb_rating'].mean()),
            'total_views': int(content_df['total_views'].sum()),
            'content_types': {k: int(v) for k, v in content_df['content_type'].value_counts().to_dict().items()}
        }
        
        with open(self.raw_path / 'summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"✅ Generated {len(content_df)} content items")
        print(f"📊 Average rating: {content_df['imdb_rating'].mean():.1f}")
        
        return content_df

if __name__ == "__main__":
    generator = DisneyPlusDataGenerator()
    generator.save_data()