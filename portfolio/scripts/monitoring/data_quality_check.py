"""
Data quality monitoring script for Disney portfolio projects.
Checks data completeness, accuracy, and consistency.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional

class DataQualityMonitor:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.processed_path = self.base_path / 'data' / 'processed'
        self.reports_path = self.base_path / 'reports' / 'data_quality'
        
        # Create reports directory
        self.reports_path.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('data_quality.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def check_disney_plus_data(self) -> Dict:
        """Check Disney+ content data quality"""
        try:
            df = pd.read_parquet(self.processed_path / 'disney_plus' / 'content_latest.parquet')
            
            # Check completeness
            completeness = {
                col: (1 - df[col].isnull().mean()) * 100 
                for col in df.columns
            }
            
            # Check data ranges
            ranges = {
                'vote_average': {
                    'min': df['vote_average'].min(),
                    'max': df['vote_average'].max(),
                    'valid': df['vote_average'].between(0, 10).mean() * 100
                }
            }
            
            # Check date validity
            date_validity = {
                'release_date': {
                    'min': df['release_date'].min(),
                    'max': df['release_date'].max(),
                    'future_dates': (df['release_date'] > datetime.now()).mean() * 100
                }
            }
            
            return {
                'completeness': completeness,
                'ranges': ranges,
                'date_validity': date_validity,
                'total_records': len(df)
            }
            
        except Exception as e:
            self.logger.error(f"Error checking Disney+ data: {str(e)}")
            return {}

    def check_theme_park_data(self) -> Dict:
        """Check theme park data quality"""
        try:
            results = {}
            for park in ['WDW_MK', 'WDW_EP', 'WDW_HS', 'WDW_AK']:
                df = pd.read_parquet(self.processed_path / 'theme_parks' / f'{park}_latest.parquet')
                
                # Check completeness
                completeness = {
                    col: (1 - df[col].isnull().mean()) * 100 
                    for col in df.columns
                }
                
                # Check wait time validity
                wait_time_validity = {
                    'negative_times': (df['wait_time'] < 0).mean() * 100,
                    'extreme_times': (df['wait_time'] > 300).mean() * 100,
                    'avg_wait': df['wait_time'].mean()
                }
                
                # Check timestamp recency
                latest_update = df['last_update'].max()
                time_lag = datetime.now() - latest_update
                
                results[park] = {
                    'completeness': completeness,
                    'wait_time_validity': wait_time_validity,
                    'data_freshness': {
                        'latest_update': latest_update,
                        'hours_since_update': time_lag.total_seconds() / 3600
                    },
                    'total_records': len(df)
                }
                
            return results
            
        except Exception as e:
            self.logger.error(f"Error checking theme park data: {str(e)}")
            return {}

    def check_box_office_data(self) -> Dict:
        """Check box office data quality"""
        try:
            df = pd.read_parquet(self.processed_path / 'entertainment' / 'box_office_latest.parquet')
            
            # Check completeness
            completeness = {
                col: (1 - df[col].isnull().mean()) * 100 
                for col in df.columns
            }
            
            # Check financial data validity
            financial_validity = {
                'negative_revenue': (df['revenue'] < 0).mean() * 100,
                'negative_budget': (df['budget'] < 0).mean() * 100,
                'zero_budget': (df['budget'] == 0).mean() * 100,
                'unrealistic_roi': (df['roi'] > 10).mean() * 100
            }
            
            # Check date ranges
            date_ranges = {
                'min_date': df['release_date'].min(),
                'max_date': df['release_date'].max(),
                'future_releases': (df['release_date'] > datetime.now()).mean() * 100
            }
            
            return {
                'completeness': completeness,
                'financial_validity': financial_validity,
                'date_ranges': date_ranges,
                'total_records': len(df)
            }
            
        except Exception as e:
            self.logger.error(f"Error checking box office data: {str(e)}")
            return {}

    def generate_quality_report(self):
        """Generate comprehensive data quality report"""
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'disney_plus': self.check_disney_plus_data(),
                'theme_parks': self.check_theme_park_data(),
                'box_office': self.check_box_office_data()
            }
            
            # Save report
            report_file = self.reports_path / f'quality_report_{datetime.now().strftime("%Y%m%d")}.json'
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            # Log summary
            self.log_quality_summary(report)
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating quality report: {str(e)}")
            return {}

    def log_quality_summary(self, report: Dict):
        """Log summary of data quality issues"""
        self.logger.info("\nData Quality Summary:")
        
        # Disney+ summary
        if report.get('disney_plus'):
            disney_data = report['disney_plus']
            self.logger.info("\nDisney+ Content:")
            self.logger.info(f"Total records: {disney_data.get('total_records', 0)}")
            self.logger.info(f"Average completeness: {np.mean(list(disney_data.get('completeness', {}).values())):.1f}%")
            
        # Theme parks summary
        if report.get('theme_parks'):
            self.logger.info("\nTheme Parks:")
            for park, data in report['theme_parks'].items():
                self.logger.info(f"\n{park}:")
                self.logger.info(f"Total records: {data.get('total_records', 0)}")
                self.logger.info(f"Hours since update: {data.get('data_freshness', {}).get('hours_since_update', 0):.1f}")
                
        # Box office summary
        if report.get('box_office'):
            box_office_data = report['box_office']
            self.logger.info("\nBox Office:")
            self.logger.info(f"Total records: {box_office_data.get('total_records', 0)}")
            self.logger.info(f"Average completeness: {np.mean(list(box_office_data.get('completeness', {}).values())):.1f}%")

if __name__ == "__main__":
    monitor = DataQualityMonitor()
    monitor.generate_quality_report() 