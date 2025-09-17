"""
Disney+ Content Analytics Dashboard
Interactive Streamlit dashboard for exploring content performance and business insights
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path
import joblib
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Disney+ Content Analytics",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

class DisneyPlusDashboard:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.data_path = self.base_path / 'data' / 'processed'
        self.models_path = self.base_path / 'models'
        
    @st.cache_data
    def load_data(_self):
        """Load processed data with caching"""
        try:
            df = pd.read_csv(_self.data_path / 'disney_plus_content_processed.csv')
            studio_stats = pd.read_csv(_self.data_path / 'studio_performance_analysis.csv')
            return df, studio_stats
        except FileNotFoundError:
            st.error("❌ Data not found. Please run the data generation and processing scripts first.")
            return pd.DataFrame(), pd.DataFrame()
    
    @st.cache_data
    def load_insights(_self):
        """Load business insights with caching"""
        try:
            with open(_self.models_path / 'business_insights.json', 'r') as f:
                insights = json.load(f)
            return insights
        except FileNotFoundError:
            return {}
    
    def render_header(self):
        """Render dashboard header"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.title("🎬 Disney+ Content Analytics")
            st.markdown("### Comprehensive Analysis of Disney+ Content Performance")
            st.markdown("---")
    
    def render_sidebar(self, df):
        """Render sidebar with filters and controls"""
        st.sidebar.header("🔧 Dashboard Controls")
        
        # Filters
        st.sidebar.subheader("Filters")
        
        # Studio filter
        studios = ['All'] + list(df['studio'].unique())
        selected_studio = st.sidebar.selectbox("Studio", studios)
        
        # Content type filter
        content_types = ['All'] + list(df['content_type'].unique())
        selected_content_type = st.sidebar.selectbox("Content Type", content_types)
        
        # Genre filter
        genres = ['All'] + list(df['primary_genre'].unique())
        selected_genre = st.sidebar.selectbox("Genre", genres)
        
        # Rating filter
        rating_range = st.sidebar.slider(
            "IMDB Rating Range",
            float(df['imdb_rating'].min()),
            float(df['imdb_rating'].max()),
            (float(df['imdb_rating'].min()), float(df['imdb_rating'].max()))
        )
        
        # Apply filters
        filtered_df = df.copy()
        
        if selected_studio != 'All':
            filtered_df = filtered_df[filtered_df['studio'] == selected_studio]
        
        if selected_content_type != 'All':
            filtered_df = filtered_df[filtered_df['content_type'] == selected_content_type]
        
        if selected_genre != 'All':
            filtered_df = filtered_df[filtered_df['primary_genre'] == selected_genre]
        
        filtered_df = filtered_df[
            (filtered_df['imdb_rating'] >= rating_range[0]) & 
            (filtered_df['imdb_rating'] <= rating_range[1])
        ]
        
        return filtered_df
    
    def render_kpis(self, df, insights):
        """Render key performance indicators"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Content",
                f"{len(df):,}",
                delta=None
            )
        
        with col2:
            avg_rating = df['imdb_rating'].mean()
            st.metric(
                "Average Rating",
                f"{avg_rating:.1f}/10",
                delta=f"{avg_rating - 7.0:+.1f} vs industry avg"
            )
        
        with col3:
            total_views = df['total_views'].sum()
            st.metric(
                "Total Views",
                f"{total_views/1e9:.1f}B",
                delta=None
            )
        
        with col4:
            avg_completion = df['completion_rate'].mean()
            st.metric(
                "Avg Completion Rate",
                f"{avg_completion:.1%}",
                delta=f"{avg_completion - 0.65:+.1%} vs benchmark"
            )
    
    def render_studio_performance(self, df):
        """Render studio performance analysis"""
        st.subheader("🏢 Studio Performance Analysis")
        
        # Studio metrics
        studio_metrics = df.groupby('studio').agg({
            'total_views': ['sum', 'mean'],
            'imdb_rating': 'mean',
            'completion_rate': 'mean',
            'content_id': 'count'
        }).round(2)
        
        studio_metrics.columns = ['Total Views', 'Avg Views', 'Avg Rating', 'Avg Completion', 'Content Count']
        studio_metrics = studio_metrics.sort_values('Total Views', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Total views by studio
            fig = px.bar(
                x=studio_metrics.index,
                y=studio_metrics['Total Views'],
                title="Total Viewership by Studio",
                color=studio_metrics['Total Views'],
                color_continuous_scale="Blues"
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Rating vs Views scatter
            fig = px.scatter(
                df,
                x='imdb_rating',
                y='total_views',
                color='studio',
                size='production_budget',
                hover_data=['title', 'primary_genre'],
                title="Rating vs Viewership by Studio"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Studio performance table
        st.subheader("Studio Performance Summary")
        st.dataframe(studio_metrics, use_container_width=True)
    
    def render_content_analysis(self, df):
        """Render content performance analysis"""
        st.subheader("📊 Content Performance Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Genre performance
            genre_performance = df.groupby('primary_genre').agg({
                'total_views': 'mean',
                'imdb_rating': 'mean',
                'completion_rate': 'mean'
            }).round(2)
            
            fig = px.bar(
                x=genre_performance.index,
                y=genre_performance['total_views'],
                title="Average Viewership by Genre",
                color=genre_performance['imdb_rating'],
                color_continuous_scale="Viridis"
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Content type distribution
            content_dist = df['content_type'].value_counts()
            fig = px.pie(
                values=content_dist.values,
                names=content_dist.index,
                title="Content Type Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Time series analysis
        if 'release_date' in df.columns:
            df['release_date'] = pd.to_datetime(df['release_date'])
            monthly_releases = df.groupby(df['release_date'].dt.to_period('M')).size()
            
            fig = px.line(
                x=monthly_releases.index.astype(str),
                y=monthly_releases.values,
                title="Content Releases Over Time",
                labels={'x': 'Month', 'y': 'Number of Releases'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def render_franchise_analysis(self, df):
        """Render franchise vs independent content analysis"""
        st.subheader("🎯 Franchise vs Independent Content")
        
        franchise_comparison = df.groupby('is_franchise').agg({
            'total_views': ['mean', 'sum'],
            'imdb_rating': 'mean',
            'production_budget': 'mean',
            'completion_rate': 'mean',
            'content_id': 'count'
        }).round(2)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Franchise performance metrics
            franchise_labels = ['Independent', 'Franchise']
            
            fig = go.Figure()
            fig.add_bar(
                name='Avg Views',
                x=franchise_labels,
                y=franchise_comparison['total_views']['mean'],
                marker_color='lightblue'
            )
            fig.add_bar(
                name='Avg Rating (×100K)',
                x=franchise_labels,
                y=franchise_comparison['imdb_rating']['mean'] * 100000,
                marker_color='orange'
            )
            fig.update_layout(title="Franchise vs Independent Performance")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # ROI analysis
            if 'roi_estimate' in df.columns:
                roi_comparison = df.groupby('is_franchise')['roi_estimate'].mean()
                
                fig = px.bar(
                    x=['Independent', 'Franchise'],
                    y=roi_comparison.values,
                    title="Return on Investment Comparison",
                    color=roi_comparison.values,
                    color_continuous_scale="RdYlGn"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    def render_predictive_insights(self, df):
        """Render predictive model insights"""
        st.subheader("🤖 AI-Powered Insights")
        
        # Content success predictor
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Content Success Predictor")
            
            # Input form for prediction
            with st.form("prediction_form"):
                duration = st.slider("Duration (minutes)", 30, 240, 90)
                rating = st.slider("Expected IMDB Rating", 1.0, 10.0, 7.0)
                budget = st.selectbox("Production Budget", 
                                    ["Low (<$50M)", "Medium ($50-150M)", "High (>$150M)"])
                is_franchise = st.checkbox("Part of Franchise")
                is_premium = st.checkbox("Premium Studio (Marvel/Pixar/Lucasfilm)")
                
                if st.form_submit_button("Predict Success"):
                    budget_mapping = {"Low (<$50M)": 30000000, "Medium ($50-150M)": 100000000, "High (>$150M)": 200000000}
                    
                    # Simplified prediction logic
                    base_prediction = 1000000
                    
                    # Adjust based on inputs
                    base_prediction *= (rating / 7.0) ** 2
                    base_prediction *= (budget_mapping[budget] / 50000000) ** 0.5
                    
                    if is_franchise:
                        base_prediction *= 1.6
                    if is_premium:
                        base_prediction *= 1.4
                    
                    st.success(f"🎯 Predicted Viewership: {int(base_prediction):,} views")
                    
                    # Recommendations
                    recommendations = []
                    if not is_franchise:
                        recommendations.append("Consider franchise tie-ins for higher viewership")
                    if rating < 7.0:
                        recommendations.append("Focus on improving story and production quality")
                    if duration > 120:
                        recommendations.append("Consider shorter runtime for better completion rates")
                    
                    if recommendations:
                        st.info("💡 Recommendations: " + "; ".join(recommendations))
        
        with col2:
            # Feature importance (if available)
            try:
                with open(self.models_path / 'feature_importance.json', 'r') as f:
                    feature_importance = json.load(f)
                
                if 'viewership' in feature_importance:
                    importance_data = feature_importance['viewership'][:10]
                    features = [item['feature'] for item in importance_data]
                    importance = [item['importance'] for item in importance_data]
                    
                    fig = px.bar(
                        x=importance,
                        y=features,
                        orientation='h',
                        title="Top Factors Predicting Viewership Success",
                        labels={'x': 'Importance', 'y': 'Feature'}
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
            except:
                st.info("Run the ML pipeline to see feature importance analysis")
    
    def render_top_content(self, df):
        """Render top performing content"""
        st.subheader("🏆 Top Performing Content")
        
        # Top content by different metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Most Viewed")
            top_viewed = df.nlargest(10, 'total_views')[
                ['title', 'studio', 'primary_genre', 'imdb_rating', 'total_views']
            ]
            top_viewed['total_views'] = top_viewed['total_views'].apply(lambda x: f"{x:,}")
            st.dataframe(top_viewed, use_container_width=True)
        
        with col2:
            st.subheader("Highest Rated")
            top_rated = df.nlargest(10, 'imdb_rating')[
                ['title', 'studio', 'primary_genre', 'imdb_rating', 'total_views']
            ]
            top_rated['total_views'] = top_rated['total_views'].apply(lambda x: f"{x:,}")
            st.dataframe(top_rated, use_container_width=True)
    
    def render_business_recommendations(self, insights):
        """Render business recommendations"""
        st.subheader("💼 Strategic Business Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Content Strategy")
            
            if insights and 'revenue_drivers' in insights:
                franchise_premium = insights['revenue_drivers'].get('franchise_premium', 1.5)
                st.metric("Franchise Performance Premium", f"{franchise_premium:.1f}x", "vs independent content")
                
                st.markdown("**Key Recommendations:**")
                st.markdown("• Invest more in franchise content development")
                st.markdown("• Focus on Marvel and Pixar productions")
                st.markdown("• Optimize movie duration to 90-120 minutes")
                st.markdown("• Increase animation content for family engagement")
        
        with col2:
            st.subheader("Market Opportunities")
            
            if insights and 'market_opportunities' in insights:
                content_gaps = insights['market_opportunities'].get('content_gaps', [])
                
                st.markdown("**Content Gaps Identified:**")
                for gap in content_gaps:
                    st.markdown(f"• {gap}")
                
                st.markdown("**Revenue Optimization:**")
                st.markdown("• Target premium studios for new content")
                st.markdown("• Expand successful franchises")
                st.markdown("• Improve completion rates in underperforming genres")
    
    def run_dashboard(self):
        """Main dashboard execution"""
        # Header
        self.render_header()
        
        # Load data
        df, studio_stats = self.load_data()
        insights = self.load_insights()
        
        if df.empty:
            st.error("No data available. Please run the data generation scripts first.")
            return
        
        # Sidebar with filters
        filtered_df = self.render_sidebar(df)
        
        # Main dashboard content
        st.subheader(f"📈 Dashboard Overview ({len(filtered_df)} items)")
        
        # KPIs
        self.render_kpis(filtered_df, insights)
        
        st.markdown("---")
        
        # Main analysis sections
        tabs = st.tabs([
            "Studio Performance",
            "Content Analysis", 
            "Franchise Analysis",
            "AI Insights",
            "Top Content",
            "Business Strategy"
        ])
        
        with tabs[0]:
            self.render_studio_performance(filtered_df)
        
        with tabs[1]:
            self.render_content_analysis(filtered_df)
        
        with tabs[2]:
            self.render_franchise_analysis(filtered_df)
        
        with tabs[3]:
            self.render_predictive_insights(filtered_df)
        
        with tabs[4]:
            self.render_top_content(filtered_df)
        
        with tabs[5]:
            self.render_business_recommendations(insights)
        
        # Footer
        st.markdown("---")
        st.markdown("**Disney+ Content Analytics Dashboard** | Data Science Portfolio Project | Built with Streamlit & Plotly")

def main():
    """Run the Streamlit dashboard"""
    dashboard = DisneyPlusDashboard()
    dashboard.run_dashboard()

if __name__ == "__main__":
    main()