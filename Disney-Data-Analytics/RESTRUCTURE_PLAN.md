# Repository Restructure Plan

## Current Issues
- Duplicate portfolio structures (`portfolio/` and `portfolio_website/`)
- Overlapping notebook directories
- Inconsistent naming conventions
- MCP server component not integrated

## New Clean Structure
```
Disney-Data-Analytics/
├── README.md                          # Main portfolio README
├── requirements.txt                   # Core dependencies
├── setup.py                          # Package installation
├── .env.example                       # Environment variables template
├── 
├── data/                              # Data storage (gitignored except samples)
│   ├── raw/                          # Raw data from APIs
│   ├── processed/                    # Cleaned, analysis-ready data
│   ├── samples/                      # Sample datasets for demo
│   └── outputs/                      # Analysis results
├── 
├── src/                              # Main source code
│   ├── __init__.py
│   ├── data_collection/              # Data collection modules
│   ├── data_processing/              # Data cleaning and transformation
│   ├── analysis/                     # Statistical analysis modules
│   ├── models/                       # Machine learning models
│   ├── visualization/                # Plotting and chart generation
│   └── utils/                        # Helper functions
├── 
├── notebooks/                        # Jupyter notebooks for analysis
│   ├── 01_data_exploration.ipynb
│   ├── 02_movie_analysis.ipynb
│   ├── 03_theme_park_analysis.ipynb
│   ├── 04_streaming_analysis.ipynb
│   └── 05_predictive_modeling.ipynb
├── 
├── web/                              # Portfolio website
│   ├── package.json
│   ├── src/
│   ├── public/
│   └── components/
├── 
├── api/                              # FastAPI backend
│   ├── main.py
│   ├── routers/
│   ├── models/
│   └── schemas/
├── 
├── tests/                            # Test suite
│   ├── test_data_collection.py
│   ├── test_analysis.py
│   └── test_api.py
├── 
├── docs/                             # Documentation
│   ├── installation.md
│   ├── usage.md
│   ├── api_reference.md
│   └── case_studies/
└── 
└── scripts/                          # Utility scripts
    ├── setup_environment.py
    ├── run_pipeline.py
    └── deploy.py
```

## Migration Steps
1. Create new structure
2. Move files to appropriate locations
3. Update imports and paths
4. Remove duplicate directories
5. Update documentation