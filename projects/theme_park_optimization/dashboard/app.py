"""
Streamlit dashboard for Disney Theme Park optimization.
Visualizes wait times, crowd patterns, and provides optimization insights.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page config
st.set_page_config(
    page_title="Disney Theme Park Optimizer",
    page_icon="🎢",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #040714;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #0063e5;
        color: white;
    }
    .stSelectbox {
        color: #122959;
    }
    .stTitle {
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

class ThemeParkDashboard:
    """Class to create and manage the theme park optimization dashboard."""
    
    def __init__(self):
        """Initialize the dashboard."""
        self.load_data()
    
    def load_data(self):
        """Load processed theme park data."""
        try:
            data_path = os.path.join('..', 'data', 'processed', 'theme_park_data_processed.csv')
            self.data = pd.read_csv(data_path)
            self.data['date'] = pd.to_datetime(self.data['date'])
            self.parks = self.data['park'].unique()
        except Exception as e:
            st.error(f"Error loading data: {e}")
            self.data = pd.DataFrame()
            self.parks = []
    
    def create_header(self):
        """Create the dashboard header."""
        st.title("🎢 Disney Theme Park Optimizer")
        st.markdown("""
        Real-time analytics and insights for optimizing theme park operations and visitor experience.
        Monitor wait times, crowd patterns, and get AI-powered recommendations.
        """)
    
    def create_sidebar(self):
        """Create the sidebar with filters."""
        st.sidebar.title("Filters")
        
        selected_park = st.sidebar.selectbox(
            "Select Park",
            options=self.parks
        )
        
        selected_date = st.sidebar.date_input(
            "Select Date",
            value=datetime.now()
        )
        
        return selected_park, selected_date
    
    def plot_wait_times(self, park: str, date: datetime):
        """Plot wait time distributions and patterns."""
        st.header("⏰ Wait Time Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Average wait times by attraction
            park_data = self.data[self.data['park'] == park]
            fig_wait = px.bar(
                park_data.groupby('attraction_name')['wait_time'].mean().reset_index(),
                x='attraction_name',
                y='wait_time',
                title='Average Wait Times by Attraction',
                color='wait_time',
                color_continuous_scale='Viridis'
            )
            fig_wait.update_layout(
                xaxis_tickangle=-45,
                showlegend=False
            )
            st.plotly_chart(fig_wait)
        
        with col2:
            # Wait times by hour
            fig_hour = px.line(
                park_data.groupby('hour')['wait_time'].mean().reset_index(),
                x='hour',
                y='wait_time',
                title='Average Wait Times by Hour',
                line_shape='spline'
            )
            st.plotly_chart(fig_hour)
    
    def plot_crowd_patterns(self, park: str, date: datetime):
        """Plot crowd patterns and heatmaps."""
        st.header("👥 Crowd Patterns")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Crowd levels by day of week
            fig_crowd = px.box(
                self.data[self.data['park'] == park],
                x='day_of_week',
                y='wait_time',
                title='Crowd Levels by Day of Week'
            )
            st.plotly_chart(fig_crowd)
        
        with col2:
            # Operating status
            operating_data = self.data[self.data['park'] == park].groupby('attraction_name')['is_operating'].mean()
            fig_status = px.bar(
                operating_data,
                title='Attraction Availability',
                color=operating_data,
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig_status)
    
    def show_recommendations(self, park: str, date: datetime):
        """Display AI-powered recommendations."""
        st.header("🎯 Smart Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Optimal Visit Time")
            park_data = self.data[self.data['park'] == park]
            best_hour = park_data.groupby('hour')['wait_time'].mean().idxmin()
            
            st.info(f"""
            🕒 Best time to visit: {best_hour}:00
            
            Based on historical wait times and crowd patterns, this time typically
            has the shortest wait times and smallest crowds.
            """)
        
        with col2:
            st.subheader("Attraction Strategy")
            busy_attractions = park_data.groupby('attraction_name')['wait_time'].mean().nlargest(3)
            
            st.warning("""
            🎯 Recommended Strategy:
            1. Visit popular attractions early in the morning
            2. Use FastPass+ for these high-demand attractions:
            """)
            
            for attraction, wait_time in busy_attractions.items():
                st.write(f"- {attraction} (Avg. wait: {wait_time:.0f} min)")
    
    def show_weather_impact(self, park: str, date: datetime):
        """Display weather impact analysis."""
        st.header("🌦️ Weather Impact")
        
        if 'temp_c' in self.data.columns and 'wait_time' in self.data.columns:
            fig = px.scatter(
                self.data[self.data['park'] == park],
                x='temp_c',
                y='wait_time',
                title='Wait Times vs. Temperature',
                trendline="lowess"
            )
            st.plotly_chart(fig)
    
    def run_dashboard(self):
        """Run the complete dashboard."""
        self.create_header()
        
        if self.data.empty:
            st.warning("No data available. Please check the data source.")
            return
        
        selected_park, selected_date = self.create_sidebar()
        
        self.plot_wait_times(selected_park, selected_date)
        self.plot_crowd_patterns(selected_park, selected_date)
        self.show_recommendations(selected_park, selected_date)
        self.show_weather_impact(selected_park, selected_date)
        
        # Add footer
        st.markdown("---")
        st.markdown("Created with ❤️ using Python and Streamlit")

def main():
    """Main function to run the dashboard."""
    dashboard = ThemeParkDashboard()
    dashboard.run_dashboard()

if __name__ == "__main__":
    main() 