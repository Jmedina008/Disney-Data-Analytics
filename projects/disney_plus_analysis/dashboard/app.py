"""
Streamlit dashboard for Disney+ content analysis.
This dashboard provides interactive visualizations of Disney+ content data.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List

# Set page config to use wide mode and add a favicon
st.set_page_config(
    page_title="Disney+ Content Analysis",
    page_icon="🏰",
    layout="wide"
)

# Custom CSS to style the dashboard with Disney-themed colors
st.markdown("""
    <style>
    .main {
        background-color: #122959;
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

class DisneyPlusDashboard:
    """Class to create and manage the Disney+ content analysis dashboard."""
    
    def __init__(self):
        """Initialize the dashboard."""
        self.data = self.load_data()
        
    @st.cache_data
    def load_data(self) -> pd.DataFrame:
        """
        Load processed data for the dashboard.
        Returns:
            pd.DataFrame: Processed Disney+ content data
        """
        data_path = os.path.join('..', 'data', 'processed', 'disney_plus_content_processed.csv')
        return pd.read_csv(data_path)
    
    def create_header(self):
        """Create the dashboard header."""
        st.title("🏰 Disney+ Content Analysis")
        st.markdown("""
        Explore insights about Disney+ content, viewing patterns, and recommendations.
        This interactive dashboard provides a comprehensive analysis of the streaming platform's offerings.
        """)
    
    def plot_content_distribution(self):
        """Create content distribution visualizations."""
        st.header("📊 Content Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Genre distribution
            fig_genre = px.pie(
                self.data,
                names='genre_ids',
                title='Content Distribution by Genre',
                hole=0.3
            )
            st.plotly_chart(fig_genre)
            
        with col2:
            # Release year distribution
            fig_year = px.histogram(
                self.data,
                x='release_year',
                title='Content by Release Year',
                nbins=20
            )
            st.plotly_chart(fig_year)
    
    def plot_ratings_analysis(self):
        """Create ratings analysis visualizations."""
        st.header("⭐ Ratings Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Average rating by genre
            fig_ratings = px.box(
                self.data,
                x='genre_ids',
                y='vote_average',
                title='Rating Distribution by Genre'
            )
            st.plotly_chart(fig_ratings)
            
        with col2:
            # Rating distribution
            fig_dist = px.histogram(
                self.data,
                x='vote_average',
                title='Rating Distribution',
                nbins=20
            )
            st.plotly_chart(fig_dist)
    
    def show_content_recommendations(self):
        """Display content recommendations."""
        st.header("🎬 Content Recommendations")
        
        # Add a genre selector
        selected_genre = st.selectbox(
            "Select a genre:",
            options=self.data['genre_ids'].unique()
        )
        
        # Filter and display top-rated content for selected genre
        genre_content = self.data[self.data['genre_ids'] == selected_genre]
        top_content = genre_content.nlargest(5, 'vote_average')
        
        st.write("Top Rated Content in Selected Genre:")
        for _, content in top_content.iterrows():
            st.write(f"- {content['title']} (Rating: {content['vote_average']})")
    
    def run_dashboard(self):
        """Run the complete dashboard."""
        self.create_header()
        self.plot_content_distribution()
        self.plot_ratings_analysis()
        self.show_content_recommendations()
        
        # Add footer
        st.markdown("---")
        st.markdown("Created with ❤️ using Streamlit and Python")

def main():
    """Main function to run the dashboard."""
    dashboard = DisneyPlusDashboard()
    dashboard.run_dashboard()

if __name__ == "__main__":
    main() 