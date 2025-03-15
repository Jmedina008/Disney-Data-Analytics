# Disney Data Analytics Portfolio

A comprehensive data analysis project focusing on Disney movies and theme parks, featuring data collection, processing, analysis, and visualization. Part of a larger data science portfolio.

## Project Overview

This project combines multiple data sources to provide insights into Disney's entertainment ecosystem:
- Movie data from TMDB API
- Box office performance data
- Theme park data from ThemeParks API
- Interactive visualizations using D3.js
- Advanced statistical analysis using Python and Jupyter notebooks

## Features

- **Movie Analysis**
  - Box office performance tracking
  - Genre distribution analysis
  - Popularity and rating trends
  - Cast and crew analysis
  - Advanced statistical tests and predictive modeling

- **Theme Park Analytics**
  - Real-time wait time tracking
  - Attraction popularity analysis
  - Park operation patterns
  - Visitor trend analysis
  - Seasonal decomposition of attendance data

- **Streaming Analytics**
  - Content popularity metrics
  - Viewer engagement analysis
  - Platform performance indicators
  - Content recommendation patterns

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
│   ├── disney_plus/
│   │   └── analysis/
│   │       ├── movie_analysis.ipynb      # Comprehensive movie analysis with statistical tests
│   │       ├── streaming_analytics.ipynb # Streaming platform analysis
│   │       └── theme_park_analysis.ipynb # Theme park data analysis
│   ├── entertainment/
│   │   └── analysis/
│   │       ├── franchise_analysis.ipynb  # Analysis of Disney franchises
│   │       └── industry_analysis.ipynb   # Entertainment industry analysis
│   └── theme_parks/
│       └── analysis/
│           └── theme_park_analysis.ipynb # Detailed theme park analysis
├── portfolio/
│   └── website/
│       └── app/
│           ├── components/
│           │   ├── Footer.tsx
│           │   ├── Navbar.tsx
│           │   └── visualizations/
│           │       ├── MovieAnalytics.tsx
│           │       ├── BoxOfficeChart.tsx
│           │       ├── WaitTimePrediction.tsx
│           │       └── StreamingTrendsChart.tsx
│           ├── layout.tsx
│           └── page.tsx
├── reports/
│   ├── figures/              # Generated visualizations
│   └── disney_movie_analysis_results.csv # Summary of analysis findings
└── scripts/
    ├── data_collection/
    │   ├── tmdb_collector.py
    │   ├── box_office_collector.py
    │   ├── theme_park_collector.py
    │   ├── process_movies.py
    │   └── process_theme_parks.py
    └── data_processing/
        └── prepare_analysis_data.py
```

## Data Collection

The project collects data from multiple sources:

1. **Movie Data (TMDB API)**
   - Basic movie information (title, release date, runtime)
   - Cast and crew details
   - Ratings and popularity metrics
   - Genre classification

2. **Box Office Data**
   - Revenue and budget information
   - Theater release information
   - Performance metrics
   - ROI calculations

3. **Theme Park Data**
   - Attraction details
   - Wait times
   - Park operating hours
   - Visitor demographics

## Analysis Components

1. **Movie Analysis**
   - Box office performance trends
   - Genre popularity over time
   - Rating distribution
   - Cast and crew network analysis
   - **Advanced Statistical Tests**:
     - Hypothesis testing (t-tests) comparing high vs. low budget movies
     - ANOVA to analyze revenue differences across release quarters
     - Multiple regression analysis for predicting movie revenue
     - Time series analysis of revenue trends
     - Chi-square tests for genre and revenue associations

2. **Theme Park Analysis**
   - Peak hours identification
   - Attraction popularity patterns
   - Seasonal trends
   - Capacity optimization insights
   - Wait time prediction models

3. **Streaming Analytics**
   - Content engagement metrics
   - Viewer retention analysis
   - Platform growth patterns
   - Content performance by category
   - Seasonal viewing trends

## Visualizations

The project includes interactive visualizations built with D3.js:
- Revenue charts and budget vs. revenue scatter plots
- Genre distribution and performance metrics
- Rating vs. Popularity scatter plots
- Theme park wait time heatmaps
- Time series decomposition of revenue trends
- Regression coefficient visualizations

## Key Findings

Some notable insights from our analysis:

- High-budget Disney movies show statistically significant higher revenue compared to low-budget productions
- Certain genres consistently outperform others in terms of ROI
- Seasonal patterns in movie releases correlate with box office performance
- Theme park attendance shows strong correlation with movie release schedules
- Viewer engagement on streaming platforms peaks during specific seasonal periods

## Setup and Usage

1. Clone the repository and install dependencies:
```bash
git clone https://github.com/Jmedina008/Disney-Data-Analytics.git
cd Disney-Data-Analytics
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
python scripts/data_collection/box_office_collector.py
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
  - pyarrow

- **Analysis**
  - Jupyter Notebook
  - matplotlib
  - seaborn
  - scikit-learn
  - scipy
  - statsmodels

- **Visualization**
  - D3.js
  - React/TypeScript
  - Framer Motion

- **Statistical Testing**
  - Hypothesis testing (t-tests)
  - ANOVA
  - Multiple regression
  - Time series analysis
  - Chi-square tests

## Future Enhancements

- Implement machine learning models to predict movie success based on various features
- Develop real-time dashboard for monitoring theme park wait times
- Expand analysis to include competitor comparison
- Create interactive web application for exploring the data
- Integrate natural language processing for sentiment analysis of movie reviews

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- TMDB API for movie data
- ThemeParks API for park data
- Disney for creating amazing entertainment experiences
- Open source community for the tools and libraries used

## Contact

Josh Medina - [@joshmedina](https://twitter.com/joshmedina)
Project Link: [https://github.com/Jmedina008/Disney-Data-Analytics](https://github.com/Jmedina008/Disney-Data-Analytics)

---
*"All our dreams can come true if we have the courage to pursue them." - Walt Disney*
