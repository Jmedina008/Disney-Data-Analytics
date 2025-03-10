"""
Automated report generator for Disney portfolio projects.
Generates comprehensive reports with insights and visualizations.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import logging
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from jinja2 import Environment, FileSystemLoader
import markdown2
import os

class ReportGenerator:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.analytics_path = self.base_path / 'data' / 'analytics'
        self.reports_path = self.base_path / 'reports'
        self.templates_path = Path(__file__).parent / 'templates'
        
        # Create necessary directories
        for path in [self.reports_path, self.templates_path]:
            path.mkdir(parents=True, exist_ok=True)
            
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Setup Jinja2 environment
        self.env = Environment(loader=FileSystemLoader(self.templates_path))

    def generate_disney_plus_report(self):
        """Generate Disney+ content analysis report"""
        try:
            # Load analysis results
            with open(self.analytics_path / 'disney_plus' / 'analysis_results.json', 'r') as f:
                analysis = json.load(f)
                
            # Create visualizations
            viz_path = self.reports_path / 'disney_plus' / 'visualizations'
            viz_path.mkdir(parents=True, exist_ok=True)
            
            # Generate plots
            self._create_genre_trend_plot(analysis['genre_trends'], viz_path)
            self._create_content_cluster_plot(analysis['content_clusters'], viz_path)
            
            # Generate report content
            report_data = {
                'title': 'Disney+ Content Analysis Report',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'genre_insights': self._generate_genre_insights(analysis['genre_trends']),
                'content_insights': self._generate_content_insights(analysis['content_clusters']),
                'viz_path': viz_path
            }
            
            # Render report
            template = self.env.get_template('disney_plus_report.html')
            report_html = template.render(**report_data)
            
            # Save report
            output_file = self.reports_path / 'disney_plus' / f'report_{datetime.now().strftime("%Y%m%d")}.html'
            with open(output_file, 'w') as f:
                f.write(report_html)
                
            self.logger.info(f"Disney+ report generated: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error generating Disney+ report: {str(e)}")
            return False

    def generate_theme_park_report(self):
        """Generate theme park analysis report"""
        try:
            # Load analysis results
            with open(self.analytics_path / 'theme_parks' / 'analysis_results.json', 'r') as f:
                analysis = json.load(f)
                
            # Create visualizations
            viz_path = self.reports_path / 'theme_parks' / 'visualizations'
            viz_path.mkdir(parents=True, exist_ok=True)
            
            # Generate plots for each park
            park_insights = {}
            for park, data in analysis.items():
                self._create_wait_time_plot(data['wait_patterns'], park, viz_path)
                self._create_forecast_plot(data['forecasts'], park, viz_path)
                park_insights[park] = self._generate_park_insights(data)
            
            # Generate report content
            report_data = {
                'title': 'Theme Park Wait Times Analysis Report',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'park_insights': park_insights,
                'viz_path': viz_path
            }
            
            # Render report
            template = self.env.get_template('theme_park_report.html')
            report_html = template.render(**report_data)
            
            # Save report
            output_file = self.reports_path / 'theme_parks' / f'report_{datetime.now().strftime("%Y%m%d")}.html'
            with open(output_file, 'w') as f:
                f.write(report_html)
                
            self.logger.info(f"Theme park report generated: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error generating theme park report: {str(e)}")
            return False

    def generate_box_office_report(self):
        """Generate box office performance report"""
        try:
            # Load analysis results
            with open(self.analytics_path / 'box_office' / 'analysis_results.json', 'r') as f:
                analysis = json.load(f)
                
            # Create visualizations
            viz_path = self.reports_path / 'box_office' / 'visualizations'
            viz_path.mkdir(parents=True, exist_ok=True)
            
            # Generate plots
            self._create_revenue_trend_plot(analysis['financial_metrics'], viz_path)
            self._create_franchise_performance_plot(analysis['franchise_performance'], viz_path)
            
            # Generate report content
            report_data = {
                'title': 'Box Office Performance Analysis Report',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'financial_insights': self._generate_financial_insights(analysis['financial_metrics']),
                'franchise_insights': self._generate_franchise_insights(analysis['franchise_performance']),
                'viz_path': viz_path
            }
            
            # Render report
            template = self.env.get_template('box_office_report.html')
            report_html = template.render(**report_data)
            
            # Save report
            output_file = self.reports_path / 'box_office' / f'report_{datetime.now().strftime("%Y%m%d")}.html'
            with open(output_file, 'w') as f:
                f.write(report_html)
                
            self.logger.info(f"Box office report generated: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error generating box office report: {str(e)}")
            return False

    def _create_genre_trend_plot(self, trends: Dict, viz_path: Path):
        """Create genre trends visualization"""
        fig = go.Figure()
        
        for genre, data in trends['trends'].items():
            fig.add_trace(go.Scatter(
                x=list(data.keys()),
                y=list(data.values()),
                name=genre,
                mode='lines+markers'
            ))
            
        fig.update_layout(
            title='Genre Trends Over Time',
            xaxis_title='Year',
            yaxis_title='Number of Titles',
            template='plotly_white'
        )
        
        fig.write_html(viz_path / 'genre_trends.html')

    def _create_wait_time_plot(self, patterns: Dict, park: str, viz_path: Path):
        """Create wait time patterns visualization"""
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=list(patterns['hourly_patterns'].keys()),
            y=list(patterns['hourly_patterns'].values()),
            name='Average Wait Time'
        ))
        
        fig.update_layout(
            title=f'Hourly Wait Time Patterns - {park}',
            xaxis_title='Hour of Day',
            yaxis_title='Average Wait Time (minutes)',
            template='plotly_white'
        )
        
        fig.write_html(viz_path / f'{park}_wait_times.html')

    def _create_revenue_trend_plot(self, metrics: Dict, viz_path: Path):
        """Create revenue trends visualization"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=list(metrics['yearly_revenue'].keys()),
            y=list(metrics['yearly_revenue'].values()),
            mode='lines+markers',
            name='Annual Revenue'
        ))
        
        fig.update_layout(
            title='Annual Box Office Revenue',
            xaxis_title='Year',
            yaxis_title='Revenue (USD)',
            template='plotly_white'
        )
        
        fig.write_html(viz_path / 'revenue_trends.html')

    def _generate_genre_insights(self, trends: Dict) -> str:
        """Generate insights from genre trends"""
        insights = []
        
        # Analyze growth rates
        growth_rates = trends['growth_rates']
        fastest_growing = max(growth_rates.items(), key=lambda x: x[1])
        declining = [genre for genre, rate in growth_rates.items() if rate < 0]
        
        insights.append(f"The fastest growing genre is {fastest_growing[0]} with {fastest_growing[1]:.1%} growth")
        if declining:
            insights.append(f"Declining genres: {', '.join(declining)}")
            
        return "\n".join(insights)

    def _generate_park_insights(self, data: Dict) -> str:
        """Generate insights from park data"""
        insights = []
        
        # Analyze wait patterns
        peak_hour = max(data['wait_patterns']['hourly_patterns'].items(), key=lambda x: x[1])
        insights.append(f"Peak wait times occur at {peak_hour[0]}:00 with average wait of {peak_hour[1]:.0f} minutes")
        
        # Analyze forecasts
        forecast = data['forecasts']['forecast']
        max_forecast = max(forecast.values())
        insights.append(f"Maximum forecasted wait time: {max_forecast:.0f} minutes")
        
        return "\n".join(insights)

    def _generate_financial_insights(self, metrics: Dict) -> str:
        """Generate insights from financial metrics"""
        insights = []
        
        total_revenue = metrics['metrics']['total_revenue']
        avg_revenue = metrics['metrics']['average_revenue']
        profitable_ratio = metrics['metrics']['profitable_ratio']
        
        insights.append(f"Total box office revenue: ${total_revenue:,.2f}")
        insights.append(f"Average revenue per movie: ${avg_revenue:,.2f}")
        insights.append(f"{profitable_ratio:.1%} of movies were profitable")
        
        return "\n".join(insights)

    def generate_all_reports(self):
        """Generate all reports"""
        self.logger.info("Starting report generation...")
        
        results = {
            'disney_plus': self.generate_disney_plus_report(),
            'theme_parks': self.generate_theme_park_report(),
            'box_office': self.generate_box_office_report()
        }
        
        success_count = sum(1 for result in results.values() if result)
        self.logger.info(f"Report generation completed. {success_count}/3 reports generated successfully.")
        
        return results

if __name__ == "__main__":
    generator = ReportGenerator()
    generator.generate_all_reports() 