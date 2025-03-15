# Data Collection and Processing Scripts

This directory contains Python scripts for collecting, processing, and preparing data for the Disney Data Analytics project.

## Directory Structure

```
scripts/
├── data_collection/
│   ├── tmdb_collector.py         # Collects movie data from TMDB API
│   ├── box_office_collector.py   # Collects box office performance data
│   ├── theme_park_collector.py   # Collects theme park data
│   ├── process_movies.py         # Processes raw movie data
│   └── process_theme_parks.py    # Processes raw theme park data
└── data_processing/
    └── prepare_analysis_data.py  # Prepares data for analysis notebooks
```

## Script Descriptions

### Data Collection

#### `tmdb_collector.py`
Collects movie data from The Movie Database (TMDB) API, focusing on Disney movies.

**Features:**
- Fetches movie details, cast, crew, and ratings
- Handles API rate limiting and pagination
- Saves raw data to JSON format
- Logs collection process for debugging

**Usage:**
```bash
python scripts/data_collection/tmdb_collector.py
```

#### `box_office_collector.py`
Collects box office performance data for Disney movies.

**Features:**
- Fetches financial data (budget, revenue)
- Matches data with TMDB movie IDs
- Handles missing data and edge cases
- Saves data in JSON format with proper type handling

**Usage:**
```bash
python scripts/data_collection/box_office_collector.py
```

#### `theme_park_collector.py`
Collects data about Disney theme parks, attractions, and wait times.

**Features:**
- Fetches park information and attraction details
- Collects historical and real-time wait data
- Handles API authentication and rate limits
- Saves data in structured JSON format

**Usage:**
```bash
python scripts/data_collection/theme_park_collector.py
```

### Data Processing

#### `process_movies.py`
Processes raw movie data into a clean, analysis-ready format.

**Features:**
- Cleans and transforms raw JSON data
- Handles missing values and outliers
- Normalizes text fields and dates
- Exports processed data to Parquet format

**Usage:**
```bash
python scripts/data_collection/process_movies.py
```

#### `process_theme_parks.py`
Processes raw theme park data for analysis.

**Features:**
- Cleans attraction and wait time data
- Aggregates data by time periods
- Handles seasonal and special event data
- Exports processed data to Parquet format

**Usage:**
```bash
python scripts/data_collection/process_theme_parks.py
```

#### `prepare_analysis_data.py`
Prepares final datasets for analysis notebooks by merging and enhancing processed data.

**Features:**
- Merges movie and box office data
- Creates derived features for analysis
- Prepares time series data structures
- Exports analysis-ready datasets

**Usage:**
```bash
python scripts/data_processing/prepare_analysis_data.py
```

## Requirements

These scripts require the following Python packages:
- pandas
- numpy
- requests
- python-dotenv
- pyarrow
- logging

Make sure to set up your environment variables in a `.env` file with the necessary API keys:
```
TMDB_API_KEY=your_tmdb_api_key
THEME_PARKS_API_KEY=your_theme_parks_api_key
```

## Output

- Raw data is saved to `data/raw/` directory
- Processed data is saved to `data/processed/` directory
- Logs are saved to the project root directory 