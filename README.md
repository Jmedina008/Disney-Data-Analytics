# Disney Data Analytics Portfolio

A comprehensive data analysis project focusing on Disney movies and theme parks, featuring data collection, processing, analysis, and visualization. Part of a larger data science portfolio.

## Project Overview

This project combines multiple data sources to provide insights into Disney's entertainment ecosystem:
- Movie data from TMDB API
- Theme park data from ThemeParks API
- Interactive visualizations using D3.js
- Data analysis using Python and Jupyter notebooks

## Features

- **Movie Analysis**
  - Box office performance tracking
  - Genre distribution analysis
  - Popularity and rating trends
  - Cast and crew analysis

- **Theme Park Analytics**
  - Real-time wait time tracking
  - Attraction popularity analysis
  - Park operation patterns
  - Visitor trend analysis

## Project Structure

```
.
├── data/
│   ├── raw/
│   │   ├── disney_plus/      # Movie data from TMDB
│   │   ├── box_office/       # Box office performance data
│   │   └── theme_parks/      # Theme park data
│   └── processed/
│       ├── disney_plus/      # Processed movie data
│       └── theme_parks/      # Processed park data
├── notebooks/
│   └── disney_plus/
│       └── analysis/
│           └── movie_analysis.ipynb
├── portfolio/
│   └── website/
│       └── app/
│           └── components/
│               └── visualizations/
│                   ├── MovieAnalytics.tsx
│                   ├── BoxOfficeChart.tsx
│                   ├── WaitTimePrediction.tsx
│                   └── StreamingTrendsChart.tsx
└── scripts/
    └── data_collection/
        ├── tmdb_collector.py
        ├── box_office_collector.py
        ├── theme_park_collector.py
        ├── process_movies.py
        └── process_theme_parks.py
```

## Data Collection

The project collects data from multiple sources:

1. **Movie Data (TMDB API)**
   - Basic movie information
   - Cast and crew details
   - Ratings and popularity metrics

2. **Box Office Data**
   - Revenue and budget information
   - Theater release information
   - Performance metrics

3. **Theme Park Data**
   - Attraction details
   - Wait times
   - Park operating hours

## Analysis Components

1. **Movie Analysis**
   - Box office performance trends
   - Genre popularity over time
   - Rating distribution
   - Cast and crew network analysis

2. **Theme Park Analysis**
   - Peak hours identification
   - Attraction popularity patterns
   - Seasonal trends
   - Capacity optimization insights

## Visualizations

The project includes interactive visualizations built with D3.js:
- Revenue charts
- Genre distribution
- Rating vs. Popularity scatter plots
- Theme park wait time heatmaps

## Setup and Usage

1. Clone the repository and install dependencies:
```bash
git clone <repository-url>
cd disney-data-analytics
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Collect data:
```bash
python scripts/data_collection/tmdb_collector.py
python scripts/data_collection/theme_park_collector.py
```

4. Process data:
```bash
python scripts/data_collection/process_movies.py
python scripts/data_collection/process_theme_parks.py
```

5. Run analysis:
```bash
jupyter notebook notebooks/disney_plus/analysis/movie_analysis.ipynb
```

## Technologies Used

- **Data Collection & Processing**
  - Python
  - pandas
  - NumPy
  - requests

- **Analysis**
  - Jupyter Notebook
  - matplotlib
  - seaborn
  - scikit-learn

- **Visualization**
  - D3.js
  - React/TypeScript
  - Framer Motion

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- TMDB API for movie data
- ThemeParks API for park data
- Disney for creating amazing entertainment experiences

## Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)
Project Link: [https://github.com/yourusername/disney-data-analytics](https://github.com/yourusername/disney-data-analytics)

---
*"All our dreams can come true if we have the courage to pursue them." - Walt Disney*
