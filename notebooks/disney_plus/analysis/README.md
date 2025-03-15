# Disney+ Analysis Notebooks

This directory contains Jupyter notebooks for analyzing various aspects of Disney's movie and streaming content.

## Notebooks Overview

### 1. [Movie Analysis](movie_analysis.ipynb)

A comprehensive analysis of Disney movies with advanced statistical tests and visualizations.

**Key Components:**
- Box office performance analysis (revenue, budget, ROI)
- Genre distribution and performance metrics
- Temporal analysis of release patterns and seasonal performance
- Audience analysis (ratings, popularity)
- Advanced statistical tests:
  - Hypothesis testing comparing high vs. low budget movies
  - ANOVA for revenue differences across release quarters
  - Multiple regression analysis for predicting movie revenue
  - Time series analysis of revenue trends
  - Chi-square tests for genre and revenue associations

**Data Sources:**
- TMDB API for movie metadata
- Box Office data for financial performance

### 2. [Streaming Analytics](streaming_analytics.ipynb)

Analysis of Disney+ streaming platform performance and content engagement.

**Key Components:**
- Content popularity metrics
- Viewer engagement patterns
- Platform growth analysis
- Content performance by category
- Seasonal viewing trends

**Data Sources:**
- Disney+ streaming data
- Content metadata from TMDB

### 3. [Theme Park Analysis](theme_park_analysis.ipynb)

Analysis of Disney theme parks with a focus on attraction performance and visitor patterns.

**Key Components:**
- Attraction popularity analysis
- Wait time patterns and predictions
- Visitor flow analysis
- Seasonal attendance trends
- Correlation between movie releases and park attendance

**Data Sources:**
- Theme Parks API for attraction data
- Historical wait time data

## Usage

To run these notebooks:

1. Ensure you have the required dependencies installed:
```bash
pip install -r requirements.txt
```

2. Make sure you have collected and processed the necessary data:
```bash
python scripts/data_collection/tmdb_collector.py
python scripts/data_collection/box_office_collector.py
python scripts/data_collection/process_movies.py
```

3. Launch Jupyter Notebook or Jupyter Lab:
```bash
jupyter notebook
```

4. Navigate to the desired notebook and run the cells sequentially.

## Output

The analysis results are saved to the `reports/` directory:
- Visualizations are saved as PNG files in `reports/figures/`
- Summary statistics are saved as CSV files in `reports/` 