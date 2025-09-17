# 🚀 Installation Guide

## Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **Node.js**: 16 or higher (for web dashboard)
- **Memory**: 8GB RAM recommended
- **Storage**: 2GB free space

### Required Software
- Git
- Python package manager (pip)
- Jupyter Notebook
- VS Code or similar editor (recommended)

## Quick Installation

### 1. Clone Repository
```bash
git clone https://github.com/Jmedina008/Disney-Data-Analytics.git
cd Disney-Data-Analytics
```

### 2. Python Environment Setup
```bash
# Create virtual environment (recommended)
python -m venv disney-analytics-env

# Activate virtual environment
# Windows:
disney-analytics-env\Scripts\activate
# macOS/Linux:
source disney-analytics-env/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Generate Sample Data
```bash
python generate_sample_data.py
```

### 4. Launch Analysis Environment
```bash
# Start Jupyter Notebook
jupyter notebook notebooks/

# Or launch JupyterLab
jupyter lab
```

### 5. Web Dashboard (Optional)
```bash
cd web
npm install
npm start
```

## Verification

### Test Data Generation
```python
import pandas as pd

# Verify data exists
df = pd.read_csv('data/samples/disney_movies.csv')
print(f"✅ Loaded {len(df)} movies")
print(f"📊 Revenue range: ${df['revenue'].min():,} - ${df['revenue'].max():,}")
```

### Test Analysis
```bash
# Run sample analysis
python -c "import src.analysis.movie_analyzer as ma; print('✅ Analysis modules working')"
```

## Troubleshooting

### Common Issues

#### Python Import Errors
```bash
# If imports fail, ensure you're in the right directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### Missing Dependencies
```bash
# Install specific packages if needed
pip install pandas numpy matplotlib seaborn scikit-learn
```

#### Jupyter Kernel Issues
```bash
# Install kernel in virtual environment
python -m ipykernel install --user --name disney-analytics --display-name "Disney Analytics"
```

#### Data Issues
```bash
# Regenerate data if corrupted
rm -rf data/samples/*
python generate_sample_data.py
```

## Development Setup

### For Contributors
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Run tests
pytest tests/
```

### Environment Variables
Create `.env` file:
```
TMDB_API_KEY=your_key_here
THEME_PARK_API_KEY=your_key_here
DATABASE_URL=sqlite:///disney_analytics.db
```

## Next Steps

1. 📊 **Start with Analysis**: Open `notebooks/01_disney_movie_analysis.ipynb`
2. 🎨 **View Visualizations**: Run the web dashboard
3. 🔍 **Explore Data**: Check `data/samples/` directory
4. 📈 **Custom Analysis**: Create new notebooks in `notebooks/`

---
*Installation complete! Ready for Disney data magic! ✨*