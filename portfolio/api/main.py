"""
FastAPI backend for Disney Data Science Portfolio.
Provides endpoints for data visualization and analysis.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import pandas as pd
import json
from pathlib import Path

app = FastAPI(
    title="Disney Data Science Portfolio API",
    description="API endpoints for Disney+ content, theme park, and entertainment analytics",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data paths
DATA_DIR = Path("../data")
PROCESSED_DIR = DATA_DIR / "processed"
ANALYTICS_DIR = DATA_DIR / "analytics"

# API Models
class StreamingTrends(BaseModel):
    labels: List[str]
    datasets: List[Dict[str, Any]]

class WaitTimeData(BaseModel):
    hour: int
    actual: float
    predicted: float

class BoxOfficeData(BaseModel):
    title: str
    budget: float
    revenue: float
    profit: float

@app.get("/")
async def root():
    return {"message": "Disney Data Science Portfolio API"}

# Disney+ Content Endpoints
@app.get("/api/disney-plus/trends", response_model=StreamingTrends)
async def get_streaming_trends():
    try:
        # Load the latest processed data
        files = list(PROCESSED_DIR.glob("disney_plus_content_*.csv"))
        if not files:
            raise HTTPException(status_code=404, detail="No streaming data found")
        
        latest_file = max(files, key=lambda x: x.stat().st_mtime)
        df = pd.read_csv(latest_file)
        
        # Process data for visualization
        monthly_counts = df.groupby([pd.to_datetime(df['release_date']).dt.strftime('%Y-%m')]).agg({
            'type': 'count'
        }).reset_index()
        
        return {
            "labels": monthly_counts['release_date'].tolist(),
            "datasets": [
                {
                    "label": "Total Content",
                    "data": monthly_counts['type'].tolist(),
                    "borderColor": "#0077C8",
                    "backgroundColor": "rgba(0, 119, 200, 0.1)"
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Theme Park Endpoints
@app.get("/api/theme-parks/wait-times/{attraction}", response_model=List[WaitTimeData])
async def get_wait_times(attraction: str):
    try:
        # Load the latest processed data
        files = list(PROCESSED_DIR.glob("theme_park_data_*.csv"))
        if not files:
            raise HTTPException(status_code=404, detail="No wait time data found")
        
        latest_file = max(files, key=lambda x: x.stat().st_mtime)
        df = pd.read_csv(latest_file)
        
        # Filter for specific attraction and process data
        attraction_data = df[df['attraction'] == attraction]
        if attraction_data.empty:
            raise HTTPException(status_code=404, detail=f"No data found for {attraction}")
        
        # Group by hour and calculate averages
        hourly_data = attraction_data.groupby('hour').agg({
            'wait_time': 'mean',
            'predicted_wait_time': 'mean'
        }).reset_index()
        
        return [
            {
                "hour": int(row['hour']),
                "actual": float(row['wait_time']),
                "predicted": float(row['predicted_wait_time'])
            }
            for _, row in hourly_data.iterrows()
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Entertainment Analytics Endpoints
@app.get("/api/entertainment/box-office", response_model=List[BoxOfficeData])
async def get_box_office_data():
    try:
        # Load the latest analytics data
        files = list(ANALYTICS_DIR.glob("box_office_analytics_*.json"))
        if not files:
            raise HTTPException(status_code=404, detail="No box office data found")
        
        latest_file = max(files, key=lambda x: x.stat().st_mtime)
        with open(latest_file) as f:
            data = json.load(f)
        
        return data['top_performers']
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Additional endpoints for metrics and analysis
@app.get("/api/disney-plus/metrics")
async def get_streaming_metrics():
    try:
        files = list(PROCESSED_DIR.glob("content_metrics_*.json"))
        if not files:
            raise HTTPException(status_code=404, detail="No metrics data found")
        
        latest_file = max(files, key=lambda x: x.stat().st_mtime)
        with open(latest_file) as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/theme-parks/metrics")
async def get_park_metrics():
    try:
        files = list(PROCESSED_DIR.glob("model_metrics_*.json"))
        if not files:
            raise HTTPException(status_code=404, detail="No metrics data found")
        
        latest_file = max(files, key=lambda x: x.stat().st_mtime)
        with open(latest_file) as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 