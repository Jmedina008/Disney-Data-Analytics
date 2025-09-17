"""
Quick synthetic data generator for Disney portfolio
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from pathlib import Path
import random

# Set random seed for reproducible data
random.seed(42)
np.random.seed(42)

# Create data directory
data_dir = Path('data/samples')
data_dir.mkdir(parents=True, exist_ok=True)

# Disney movie data
print("🎬 Generating Disney movie data...")

studios = ['Walt Disney Pictures', 'Pixar Animation Studios', 'Marvel Studios', 'Lucasfilm']
genres = ['Animation', 'Adventure', 'Family', 'Fantasy', 'Action', 'Comedy', 'Drama']
franchises = ['Marvel Cinematic Universe', 'Star Wars', 'Toy Story', 'Frozen', 'Lion King']

movies = []
for i in range(100):
    # Generate realistic dates
    release_date = datetime(2000, 1, 1) + timedelta(days=random.randint(0, 8766))  # 24 years
    year = release_date.year
    
    # Budget increases over time with inflation
    base_budget = 80_000_000 * (1 + (year - 2000) * 0.04)  # 4% annual increase
    budget = int(base_budget * random.uniform(0.3, 3.0))
    
    # Revenue correlated with budget but with high variance
    revenue_multiplier = random.uniform(0.8, 6.0)  # Some flops, some blockbusters
    revenue = int(budget * revenue_multiplier)
    
    # Other metrics
    runtime = random.randint(85, 150)
    vote_average = random.uniform(6.0, 8.8)
    vote_count = random.randint(5000, 100000)
    popularity = random.uniform(20, 95)
    
    studio = random.choice(studios)
    franchise = random.choice(franchises + [None] * 3)  # 40% have franchise
    
    # Generate title
    base_titles = ["Adventure", "Quest", "Journey", "Dream", "Magic", "Kingdom", "Princess", "Hero"]
    title_base = random.choice(base_titles)
    if franchise:
        title = f"{franchise}: {title_base} {random.randint(1, 5)}"
    else:
        title = f"Disney's {title_base} {random.randint(1, 10)}"
    
    movie = {
        'id': 10000 + i,
        'title': title,
        'release_date': release_date.strftime('%Y-%m-%d'),
        'budget': budget,
        'revenue': revenue,
        'runtime': runtime,
        'vote_average': round(vote_average, 1),
        'vote_count': vote_count,
        'popularity': round(popularity, 1),
        'studio': studio,
        'franchise': franchise,
        'genres': random.sample(genres, random.randint(1, 3)),
        'roi': ((revenue - budget) / budget * 100) if budget > 0 else 0,
        'profit': revenue - budget,
        'budget_millions': budget / 1_000_000,
        'revenue_millions': revenue / 1_000_000,
        'release_year': year,
        'release_month': release_date.month,
        'is_franchise': 1 if franchise else 0
    }
    
    movies.append(movie)

# Create DataFrame and enhance correlations
movies_df = pd.DataFrame(movies)

# Marvel and Pixar tend to perform better
marvel_mask = movies_df['studio'] == 'Marvel Studios'
pixar_mask = movies_df['studio'] == 'Pixar Animation Studios'
movies_df.loc[marvel_mask, 'revenue'] *= 1.4
movies_df.loc[pixar_mask, 'vote_average'] += 0.6

# Recalculate derived metrics after adjustments
movies_df['roi'] = ((movies_df['revenue'] - movies_df['budget']) / movies_df['budget'] * 100)
movies_df['profit'] = movies_df['revenue'] - movies_df['budget']
movies_df['revenue_millions'] = movies_df['revenue'] / 1_000_000

# Clamp values
movies_df['vote_average'] = movies_df['vote_average'].clip(3.0, 10.0)
movies_df['roi'] = movies_df['roi'].clip(-80, 800)

# Save data
movies_df.to_csv(data_dir / 'disney_movies.csv', index=False)
movies_df.to_json(data_dir / 'disney_movies.json', orient='records', indent=2)

print(f"✅ Generated {len(movies_df)} movies")
print(f"📊 Total revenue: ${movies_df['revenue'].sum():,}")
print(f"💰 Average budget: ${movies_df['budget'].mean():.0f}")

# Generate summary
summary = {
    'generation_date': datetime.now().isoformat(),
    'total_movies': len(movies_df),
    'date_range': f"{movies_df['release_date'].min()} to {movies_df['release_date'].max()}",
    'total_revenue': int(movies_df['revenue'].sum()),
    'avg_budget': int(movies_df['budget'].mean()),
    'studios': movies_df['studio'].value_counts().to_dict(),
    'top_grossing': movies_df.nlargest(5, 'revenue')[['title', 'revenue_millions']].to_dict('records')
}

with open(data_dir / 'data_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print(f"📁 Data saved to {data_dir}")
print("🚀 Ready for analysis!")