# Data Science Notebooks

This directory contains Jupyter notebooks for data collection, analysis, and visualization of Disney-themed data science projects.

## Project Structure

```
notebooks/
├── disney_plus/              # Disney+ Content Analysis
│   ├── data_collection/     # Scripts for collecting streaming data
│   ├── analysis/           # Data analysis and insights
│   └── visualization/      # Interactive visualizations
├── theme_parks/             # Theme Park Optimization
│   ├── data_collection/     # Wait times and weather data collection
│   ├── analysis/           # Predictive modeling and analysis
│   └── visualization/      # Interactive dashboards
└── entertainment/           # Entertainment Analytics
    ├── data_collection/     # Box office and media data collection
    ├── analysis/           # Performance analysis
    └── visualization/      # Revenue and trend visualizations
```

## Setup Instructions

1. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with your API keys:
```
TMDB_API_KEY=your_tmdb_api_key
THEME_PARK_API_KEY=your_theme_park_api_key
WEATHER_API_KEY=your_weather_api_key
NEWS_API_KEY=your_news_api_key
```

## Data Collection

### Disney+ Content
- `tmdb_data_collection.ipynb`: Collects streaming content data from TMDB API
- Includes metadata, ratings, and availability information

### Theme Parks
- `wait_times_collection.ipynb`: Collects real-time wait times data
- Combines with weather data for predictive modeling

### Entertainment
- `box_office_collection.ipynb`: Collects box office performance data
- Includes revenue, budget, and media coverage information

## Analysis

### Disney+ Content
- Content distribution analysis
- Genre and language trends
- Viewer engagement metrics

### Theme Parks
- Wait time prediction models
- Weather impact analysis
- Crowd flow optimization

### Entertainment
- Box office performance analysis
- Franchise success patterns
- Release strategy optimization

## Visualization

Each project includes interactive visualizations using:
- Matplotlib and Seaborn for static plots
- Plotly for interactive charts
- D3.js for web-based visualizations

## Data Storage

Collected and processed data is stored in:
- `../data/raw/`: Raw data from APIs
- `../data/processed/`: Cleaned and transformed data
- `../data/analytics/`: Analysis results and metrics

## Contributing

1. Create a new branch for your analysis
2. Add notebooks to the appropriate project directory
3. Include clear documentation and comments
4. Update requirements.txt if new dependencies are added 