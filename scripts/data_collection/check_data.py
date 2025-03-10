import json
from pathlib import Path

# Read the data file
data_file = Path(__file__).parent.parent.parent / 'data' / 'raw' / 'disney_plus' / 'disney_movies_20250309_231327.json'
with open(data_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Print summary
print(f"Total movies collected: {len(data)}")
print("\nFirst movie details:")
first_movie = data[0]
print(f"Title: {first_movie['title']}")
print(f"Release Date: {first_movie['release_date']}")
print(f"Overview: {first_movie['overview'][:200]}...")
print(f"\nLast movie details:")
last_movie = data[-1]
print(f"Title: {last_movie['title']}")
print(f"Release Date: {last_movie['release_date']}")
print(f"Overview: {last_movie['overview'][:200]}...") 