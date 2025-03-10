"""
System test script for Disney portfolio projects.
Verifies all components are working correctly.
"""

import sys
import os
from pathlib import Path
import logging
import pandas as pd
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from data_collection.collect_all_data import DataCollector
from data_processing.data_processor import DataProcessor
from analytics.analyzer import DataAnalyzer
from reporting.report_generator import ReportGenerator

class SystemTester:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.collector = DataCollector()
        self.processor = DataProcessor()
        self.analyzer = DataAnalyzer()
        self.reporter = ReportGenerator()

    def test_data_collection(self):
        """Test data collection functionality"""
        self.logger.info("Testing data collection...")
        
        try:
            # Test Disney+ content collection
            self.logger.info("Testing Disney+ content collection...")
            disney_result = self.collector.collect_disney_plus_data()
            assert disney_result, "Disney+ content collection failed"
            
            # Test theme park data collection
            self.logger.info("Testing theme park data collection...")
            park_result = self.collector.collect_theme_park_data()
            assert park_result, "Theme park data collection failed"
            
            # Test box office data collection
            self.logger.info("Testing box office data collection...")
            box_office_result = self.collector.collect_box_office_data()
            assert box_office_result, "Box office data collection failed"
            
            self.logger.info("Data collection tests passed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Data collection test failed: {str(e)}")
            return False

    def test_data_processing(self):
        """Test data processing functionality"""
        self.logger.info("Testing data processing...")
        
        try:
            # Test data processing pipeline
            result = self.processor.process_all_data()
            assert result, "Data processing failed"
            
            # Verify processed files exist
            processed_files = [
                'disney_plus/content_latest.parquet',
                'theme_parks/WDW_MK_latest.parquet',
                'entertainment/box_office_latest.parquet'
            ]
            
            for file in processed_files:
                path = self.base_path / 'data' / 'processed' / file
                assert path.exists(), f"Processed file missing: {file}"
            
            self.logger.info("Data processing tests passed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Data processing test failed: {str(e)}")
            return False

    def test_analytics(self):
        """Test analytics functionality"""
        self.logger.info("Testing analytics...")
        
        try:
            # Test Disney+ content analysis
            disney_results = self.analyzer.analyze_disney_plus_content()
            assert disney_results, "Disney+ content analysis failed"
            
            # Test theme park analysis
            park_results = self.analyzer.analyze_theme_park_data()
            assert park_results, "Theme park analysis failed"
            
            # Test box office analysis
            box_office_results = self.analyzer.analyze_box_office_performance()
            assert box_office_results, "Box office analysis failed"
            
            # Verify analysis results exist
            analysis_files = [
                'disney_plus/analysis_results.json',
                'theme_parks/analysis_results.json',
                'box_office/analysis_results.json'
            ]
            
            for file in analysis_files:
                path = self.base_path / 'data' / 'analytics' / file
                assert path.exists(), f"Analysis file missing: {file}"
            
            self.logger.info("Analytics tests passed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Analytics test failed: {str(e)}")
            return False

    def test_reporting(self):
        """Test reporting functionality"""
        self.logger.info("Testing report generation...")
        
        try:
            # Test report generation
            results = self.reporter.generate_all_reports()
            
            # Verify all reports were generated
            assert results['disney_plus'], "Disney+ report generation failed"
            assert results['theme_parks'], "Theme park report generation failed"
            assert results['box_office'], "Box office report generation failed"
            
            # Verify report files exist
            today = datetime.now().strftime("%Y%m%d")
            report_files = [
                f'disney_plus/report_{today}.html',
                f'theme_parks/report_{today}.html',
                f'box_office/report_{today}.html'
            ]
            
            for file in report_files:
                path = self.base_path / 'reports' / file
                assert path.exists(), f"Report file missing: {file}"
            
            self.logger.info("Reporting tests passed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Reporting test failed: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all system tests"""
        self.logger.info("Starting system tests...")
        
        results = {
            'data_collection': self.test_data_collection(),
            'data_processing': self.test_data_processing(),
            'analytics': self.test_analytics(),
            'reporting': self.test_reporting()
        }
        
        # Print summary
        self.logger.info("\nTest Results Summary:")
        for component, passed in results.items():
            status = "PASSED" if passed else "FAILED"
            self.logger.info(f"{component}: {status}")
        
        # Calculate overall success
        success_rate = sum(1 for result in results.values() if result) / len(results)
        self.logger.info(f"\nOverall Success Rate: {success_rate:.1%}")
        
        return all(results.values())

if __name__ == "__main__":
    tester = SystemTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1) 