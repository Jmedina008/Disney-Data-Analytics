# Disney Data Science Portfolio

A comprehensive data science portfolio showcasing analytics and insights from Disney's entertainment ecosystem.

## Projects

### 1. Disney+ Content Analysis
- **Description**: Analysis of streaming content trends, genre popularity, and viewer engagement
- **Technologies**: Python, Pandas, Scikit-learn, TMDB API
- **Key Features**:
  - Genre trend analysis and growth prediction
  - Content clustering and recommendation engine
  - Automated daily data collection and analysis
  - Interactive visualizations using Plotly

### 2. Theme Park Optimization
- **Description**: Wait time analysis and prediction for Disney World parks
- **Technologies**: Python, SARIMA, Machine Learning
- **Key Features**:
  - Real-time wait time monitoring
  - Predictive modeling for crowd levels
  - Cross-park analysis and insights
  - 15-minute interval data updates

### 3. Entertainment Analytics
- **Description**: Box office performance analysis and franchise insights
- **Technologies**: Python, Statistical Analysis, Financial Modeling
- **Key Features**:
  - Revenue and ROI analysis
  - Franchise performance tracking
  - Seasonal trend analysis
  - Success factor identification

## Technical Architecture

### Data Collection
- Automated data collection from multiple APIs
- Scheduled updates using APScheduler
- Robust error handling and logging
- Data validation and cleaning pipeline

### Analysis Pipeline
- Advanced statistical analysis
- Machine learning models
- Time series forecasting
- Automated insight generation

### Reporting System
- Interactive HTML reports
- Real-time dashboards
- Beautiful visualizations
- Automated report generation

## Setup Instructions

1. Clone the repository:
```bash
git clone [repository-url]
cd portfolio
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r scripts/data_collection/requirements.txt
```

4. Set up environment variables:
Create a `.env` file with your API keys:
```
TMDB_API_KEY=your_tmdb_api_key
THEME_PARK_API_KEY=your_theme_park_api_key
WEATHER_API_KEY=your_weather_api_key
```

5. Initialize the data collection:
```bash
python scripts/data_collection/collect_all_data.py
```

6. Start the analysis pipeline:
```bash
python scripts/analytics/analyzer.py
```

7. Generate reports:
```bash
python scripts/reporting/report_generator.py
```

## Project Structure
```
portfolio/
├── data/
│   ├── raw/          # Raw collected data
│   ├── processed/    # Cleaned and transformed data
│   └── analytics/    # Analysis results
├── notebooks/        # Jupyter notebooks for analysis
├── reports/         # Generated HTML reports
├── scripts/
│   ├── data_collection/
│   ├── data_processing/
│   ├── analytics/
│   └── reporting/
└── website/         # Portfolio website
```

## Technologies Used
- **Data Collection**: Requests, APScheduler
- **Data Processing**: Pandas, NumPy
- **Analysis**: Scikit-learn, StatsModels, TextBlob
- **Visualization**: Plotly, Seaborn
- **Reporting**: Jinja2, TailwindCSS
- **Storage**: Parquet, JSON

## Future Enhancements
- Real-time dashboard updates
- Advanced ML model deployment
- Mobile app integration
- API endpoint creation

## Contact
[Your Name]
[Your Email]
[LinkedIn Profile]
[GitHub Profile] 