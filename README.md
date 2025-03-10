# Disney Data Analytics Portfolio

A comprehensive data science portfolio showcasing analytics projects focused on Disney's various business segments.

## 🎯 Projects

### 1. Disney+ Content Analysis
- Streaming content analysis
- Viewer engagement metrics
- Content recommendation system
- Genre and rating distribution

### 2. Theme Park Optimization
- Wait time analysis
- Crowd prediction models
- Attraction popularity metrics
- Seasonal trend analysis

### 3. Entertainment Analytics
- Box office performance analysis
- Movie success factors
- Revenue prediction models
- Franchise performance metrics

## 🛠️ Technical Architecture

### Data Collection
- Automated data collection pipelines
- API integrations (TMDB, Theme Parks API)
- Data validation and quality checks
- Scheduled updates

### Processing & Analysis
- Python data processing scripts
- Statistical analysis
- Machine learning models
- Jupyter notebooks for analysis

### Visualization & Reporting
- Interactive dashboards
- Real-time metrics
- Custom visualization components
- Automated reporting

## 🚀 Getting Started

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Jmedina008/Disney-Data-Analytics.git
   cd Disney-Data-Analytics
   ```

2. **Set Up Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure API Keys**
   - Create a `.env` file
   - Add required API keys (see `.env.example`)

4. **Run Data Collection**
   ```bash
   python scripts/data_collection/collect_data.py
   ```

5. **View Analysis**
   - Open Jupyter notebooks in `notebooks/` directory
   - Run analysis scripts in `scripts/analytics/`

## 📊 Project Structure

```
├── data/
│   ├── raw/          # Raw data from APIs
│   ├── processed/    # Cleaned and processed data
│   └── analytics/    # Analysis results
├── notebooks/
│   ├── disney_plus/
│   ├── theme_parks/
│   └── entertainment/
├── scripts/
│   ├── data_collection/
│   ├── analytics/
│   ├── monitoring/
│   └── deployment/
└── reports/
    └── data_quality/
```

## 🔧 Technologies Used

- **Languages**: Python, SQL, TypeScript
- **Data Processing**: Pandas, NumPy
- **Analysis**: Scikit-learn, SciPy
- **Visualization**: Plotly, D3.js
- **Web Framework**: FastAPI, Next.js
- **Database**: PostgreSQL
- **Infrastructure**: Docker, GitHub Actions

## 📈 Features

- Real-time data collection
- Automated quality checks
- Interactive visualizations
- API key management
- Scheduled reports
- Performance monitoring

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

For any questions or feedback, please reach out through:
- GitHub Issues
- [Your Contact Information]

---
*"All our dreams can come true if we have the courage to pursue them." - Walt Disney*
