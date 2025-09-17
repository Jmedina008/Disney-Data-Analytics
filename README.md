# 🏰 Disney Data Analytics Portfolio

A comprehensive portfolio of Disney-themed data analytics projects, featuring advanced machine learning, revenue optimization, and guest experience analytics. From streaming content analysis to theme park operations and resort management.

## 🎯 Portfolio Overview

This portfolio showcases three distinct Disney analytics projects, each demonstrating different aspects of data science and business intelligence:

### 🏨 **NEW: Disney Resort Guest Experience & Revenue Analytics** 
**Our newest and most comprehensive project** - A complete resort operations analytics pipeline featuring:
- Advanced guest segmentation using machine learning
- Revenue optimization models and dynamic pricing
- Predictive analytics for guest satisfaction and spending
- Interactive Streamlit dashboard for operations management
- 25,000+ synthetic bookings across 9 Disney resort properties

### 🎬 Disney+ Content Analytics
Streaming platform analysis with movie performance, genre trends, and content optimization insights.

### 🎢 Theme Park Operations Optimization
Data-driven analysis of park operations, visitor patterns, and attraction performance.

## 🚀 Featured Projects

### 🏨 [Disney Resort Analytics](projects/disney_resort_analytics/) - **⭐ FEATURED PROJECT**
Complete resort operations analytics system with ML-driven insights:
- **Guest Segmentation**: 7 distinct guest personas using K-means clustering
- **Predictive Models**: Guest satisfaction (>85% accuracy) and spending prediction
- **Revenue Optimization**: Dynamic pricing and occupancy forecasting
- **Interactive Dashboard**: Comprehensive operations management interface
- **Full Pipeline**: Automated data generation → analytics → optimization → visualization

**Quick Start:**
```bash
cd projects/disney_resort_analytics/
python run_analytics_pipeline.py  # Runs complete pipeline
```

### 🎬 [Disney+ Content Analytics](projects/disney_plus_analysis/)
- Box office performance and genre analysis
- Advanced statistical testing (t-tests, ANOVA, regression)
- Content popularity and rating trends
- Predictive modeling for movie success

### 🎢 [Theme Park Optimization](projects/theme_park_optimization/)
- Wait time analysis and prediction
- Visitor flow optimization
- Seasonal pattern analysis
- Capacity planning insights

## 📁 Portfolio Structure

```
disney-data-analytics/
├── projects/
│   ├── disney_resort_analytics/     # ⭐ FEATURED: Complete resort analytics pipeline
│   │   ├── src/
│   │   │   ├── resort_data_generator.py  # Synthetic data generation
│   │   │   ├── guest_analytics.py        # ML guest segmentation
│   │   │   ├── revenue_optimization.py   # Dynamic pricing models
│   │   │   └── resort_dashboard.py       # Interactive Streamlit dashboard
│   │   ├── run_analytics_pipeline.py # One-click pipeline execution
│   │   └── README.md                 # Comprehensive project docs
│   ├── disney_plus_analysis/        # Streaming content analytics
│   └── theme_park_optimization/     # Park operations analysis
├── notebooks/                       # Jupyter analysis notebooks
├── data/                           # Shared datasets
├── src/                            # Common utilities
├── web/                            # Portfolio website
└── scripts/                        # Data collection scripts
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

## 🚀 Quick Start

### Try the Featured Project (Disney Resort Analytics)
```bash
# Clone the repository
git clone https://github.com/Jmedina008/Disney-Data-Analytics.git
cd Disney-Data-Analytics

# Run the complete resort analytics pipeline
cd projects/disney_resort_analytics/
python run_analytics_pipeline.py --install-deps

# This will:
# 1. Install dependencies automatically
# 2. Generate 25,000+ synthetic resort bookings
# 3. Run ML guest segmentation and predictive models
# 4. Perform revenue optimization analysis
# 5. Launch interactive dashboard at http://localhost:8501
```

### Explore Other Projects
```bash
# Disney+ Content Analytics
cd projects/disney_plus_analysis/
jupyter notebook

# Theme Park Optimization
cd projects/theme_park_optimization/
jupyter notebook
```

## 🛠️ Technologies Used

- **Machine Learning & Analytics**: Python, pandas, scikit-learn, numpy
- **Visualization**: Streamlit, Plotly, matplotlib, seaborn
- **Statistical Analysis**: scipy, statsmodels, hypothesis testing
- **Web Development**: React, TypeScript, Next.js
- **Data Processing**: Jupyter notebooks, synthetic data generation

## 🔮 What's Next

- **Real-time Data Integration**: Connect resort analytics to live booking systems
- **Advanced ML Models**: Implement deep learning for guest behavior prediction
- **Mobile Dashboard**: React Native app for on-the-go resort management
- **Competitive Analysis**: Expand to Universal Studios and other resort competitors
- **Natural Language Processing**: Guest review sentiment analysis integration

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
