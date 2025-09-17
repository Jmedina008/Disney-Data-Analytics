"""
Resort Operations Dashboard

Streamlit dashboard for the analytics project. Started simple but got pretty feature-rich.
Some of the styling is probably overdone but it looks decent.

TODO: The loading is a bit slow with all the data processing
TODO: Add filtering functionality (it's in the sidebar but doesn't actually filter yet)
NOTE: Some of the metrics calculations might be off - need to double-check
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="Disney Resort Operations Center",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #1f4e79, #2e86ab, #a23b72, #f18f01, #c73e1d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin: 20px 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .revenue-highlight {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .insight-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 15px 0;
    }
    
    .opportunity-card {
        background: #fff3cd;
        padding: 15px;
        border-radius: 8px;
        border: 2px solid #ffc107;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

class ResortOperationsDashboard:
    """Main dashboard class - handles all the Streamlit UI stuff
    
    This got pretty big with all the different chart types and metrics
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.data_path = self.base_path / 'data'
        self.raw_path = self.data_path / 'raw'
        self.processed_path = self.data_path / 'processed'
        
        # Resort data - copied from the data generator, should probably centralize this
        self.resort_info = {
            'Grand Floridian': {'category': 'Deluxe Villa', 'rooms': 847, 'icon': '🏰'},
            'Polynesian': {'category': 'Deluxe', 'rooms': 492, 'icon': '🌴'},
            'Contemporary': {'category': 'Deluxe', 'rooms': 655, 'icon': '🏢'},
            'Wilderness Lodge': {'category': 'Deluxe', 'rooms': 729, 'icon': '🏔️'},
            'Beach Club': {'category': 'Deluxe', 'rooms': 583, 'icon': '🏖️'},
            'Coronado Springs': {'category': 'Moderate', 'rooms': 1917, 'icon': '🏜️'},
            'Port Orleans French Quarter': {'category': 'Moderate', 'rooms': 1008, 'icon': '🎭'},
            'Pop Century': {'category': 'Value', 'rooms': 2880, 'icon': '📻'},
            'All Star Sports': {'category': 'Value', 'rooms': 1920, 'icon': '⚽'}
        }
    
    @st.cache_data
    def load_resort_data(_self):
        """Load data with caching - the _self thing is weird but required for Streamlit"""
        try:
            # Load raw operational data
            bookings = pd.read_csv(_self.raw_path / 'resort_bookings.csv')
            guests = pd.read_csv(_self.raw_path / 'guest_profiles.csv')
            dining = pd.read_csv(_self.raw_path / 'dining_reservations.csv')
            amenities = pd.read_csv(_self.raw_path / 'amenity_usage.csv')
            
            # Load processed analytics if available
            try:
                analytics_df = pd.read_csv(_self.processed_path / 'guest_analytics_dataset.csv')
                with open(_self.processed_path / 'analytics_summary.json', 'r') as f:
                    analytics_summary = json.load(f)
            except FileNotFoundError:
                analytics_df = pd.DataFrame()
                analytics_summary = {}
            
            # Load revenue optimization results if available
            try:
                with open(_self.processed_path / 'revenue_optimization_summary.json', 'r') as f:
                    revenue_summary = json.load(f)
            except FileNotFoundError:
                revenue_summary = {}
            
            return bookings, guests, dining, amenities, analytics_df, analytics_summary, revenue_summary
            
        except FileNotFoundError as e:
            st.error(f"❌ Data files not found. Please run data generation first.")
            # Return empty dataframes so the app doesn't crash
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), {}, {}
    
    def render_dashboard_header(self):
        """Render main dashboard header"""
        st.markdown('<h1 class="main-header">🏨 Disney Resort Operations Center</h1>', unsafe_allow_html=True)
        st.markdown("### Advanced Analytics for Resort Management Excellence")
        
        # Real-time status indicators
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.success("🟢 **All Systems Operational**")
        with col2:
            st.info(f"📅 **{datetime.now().strftime('%B %d, %Y')}**")
        with col3:
            st.info("🕐 **Live Dashboard** - Auto-refreshing")
        with col4:
            if st.button("🔄 Refresh Data"):
                st.cache_data.clear()
                st.rerun()
        
        st.markdown("---")
    
    def render_key_performance_indicators(self, bookings, guests, dining, amenities, revenue_summary):
        """KPI section - lots of calculations here, probably should optimize"""
        st.subheader("📊 Resort Performance Overview")
        
        # Calculate metrics - doing this every time the page loads, should probably cache
        total_bookings = len(bookings)
        total_guests = len(guests)
        total_room_revenue = bookings['total_cost'].sum()
        total_dining_revenue = dining['estimated_cost'].sum()
        total_amenity_revenue = amenities['cost'].sum()
        total_revenue = total_room_revenue + total_dining_revenue + total_amenity_revenue
        
        # print(f"DEBUG: Revenue breakdown - Room: ${total_room_revenue/1e6:.1f}M, Dining: ${total_dining_revenue/1e6:.1f}M")
        
        avg_stay_len = bookings['stay_length'].mean()  # shorter var name
        avg_party_sz = bookings['party_size'].mean()
        occ_rate = self._calculate_occupancy_rate(bookings)
        
        # Display KPIs in columns
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h2>💰 ${total_revenue/1e6:.1f}M</h2>
                <p><strong>Total Revenue</strong></p>
                <small>Room + Dining + Amenities</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h2>🏨 {total_bookings:,}</h2>
                <p><strong>Total Bookings</strong></p>
                <small>Across all resorts</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h2>📈 {occ_rate:.1%}</h2>
                <p><strong>Avg Occupancy</strong></p>
                <small>Capacity utilization</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h2>🛏️ {avg_stay_len:.1f} days</h2>
                <p><strong>Avg Stay Length</strong></p>
                <small>Guest visit duration</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            revenue_per_guest = total_revenue / total_guests if total_guests > 0 else 0
            st.markdown(f"""
            <div class="metric-card">
                <h2>💳 ${revenue_per_guest:,.0f}</h2>
                <p><strong>Revenue per Guest</strong></p>
                <small>Total spending average</small>
            </div>
            """, unsafe_allow_html=True)
    
    def render_revenue_optimization_insights(self, revenue_summary):
        """Display revenue optimization analysis"""
        st.subheader("💡 Revenue Optimization Insights")
        
        if revenue_summary and 'optimization_analysis' in revenue_summary:
            optimization = revenue_summary['optimization_analysis']
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### 🎯 Optimization Opportunities")
                
                if 'optimization_opportunities' in optimization:
                    for i, opp in enumerate(optimization['optimization_opportunities'], 1):
                        st.markdown(f"""
                        <div class="opportunity-card">
                            <strong>Opportunity {i}: {opp['description']}</strong><br>
                            <em>Estimated Impact: {opp['estimated_impact']}</em><br>
                            <small>Type: {opp['type'].replace('_', ' ').title()}</small>
                        </div>
                        """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("### 📈 Revenue Scenarios")
                
                if 'revenue_scenarios' in optimization:
                    total_potential = sum([scenario['revenue_uplift'] 
                                         for scenario in optimization['revenue_scenarios'].values()])
                    
                    st.markdown(f"""
                    <div class="revenue-highlight">
                        <h3>${total_potential/1e6:.1f}M</h3>
                        <p><strong>Total Optimization Potential</strong></p>
                        <small>Annual revenue uplift opportunity</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show individual scenarios
                    for scenario_name, scenario in optimization['revenue_scenarios'].items():
                        st.info(f"**{scenario_name.replace('_', ' ').title()}**: ${scenario['revenue_uplift']/1e6:.1f}M - {scenario['time_to_impact']}")
        else:
            st.info("🔄 Revenue optimization analysis not available. Run revenue optimization pipeline to see insights.")
    
    def render_guest_segmentation_analysis(self, analytics_summary):
        """Display guest segmentation insights"""
        st.subheader("👥 Guest Segmentation Analysis")
        
        if analytics_summary and 'guest_segmentation' in analytics_summary:
            segmentation = analytics_summary['guest_segmentation']
            
            # Create segmentation visualization
            cluster_data = []
            for cluster_id, cluster_info in segmentation.items():
                cluster_data.append({
                    'Segment': cluster_info['cluster_name'],
                    'Size': cluster_info['size'],
                    'Percentage': cluster_info['percentage'],
                    'Avg Spend': cluster_info['average_metrics'].get('total_spend', 0)
                })
            
            cluster_df = pd.DataFrame(cluster_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Segment size pie chart
                fig_pie = px.pie(cluster_df, values='Size', names='Segment', 
                               title="Guest Segment Distribution")
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Segment spending bar chart
                fig_bar = px.bar(cluster_df, x='Segment', y='Avg Spend',
                               title="Average Spending by Segment",
                               color='Avg Spend',
                               color_continuous_scale='viridis')
                fig_bar.update_xaxes(tickangle=45)
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Segment details
            st.markdown("### Segment Profiles")
            for cluster_id, cluster_info in segmentation.items():
                with st.expander(f"🎯 {cluster_info['cluster_name']} ({cluster_info['percentage']}% of guests)"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write("**Key Metrics:**")
                        for metric, value in cluster_info['average_metrics'].items():
                            if isinstance(value, (int, float)):
                                st.write(f"• {metric.replace('_', ' ').title()}: {value:,.2f}")
                    
                    with col_b:
                        st.write("**Preferred Resorts:**")
                        for resort, count in list(cluster_info['preferred_resorts'].items())[:3]:
                            st.write(f"• {resort}: {count} bookings")
        else:
            st.info("🔄 Guest segmentation analysis not available. Run guest analytics pipeline to see insights.")
    
    def render_operational_performance(self, bookings, dining, amenities):
        """Display operational performance metrics"""
        st.subheader("🏗️ Operational Performance Dashboard")
        
        # Convert dates for time series analysis
        bookings['checkin_date'] = pd.to_datetime(bookings['checkin_date'])
        
        # Resort performance comparison
        resort_metrics = bookings.groupby('resort_name').agg({
            'total_cost': ['sum', 'mean', 'count'],
            'stay_length': 'mean',
            'party_size': 'mean'
        }).round(2)
        
        resort_metrics.columns = ['Total Revenue', 'Avg Booking Value', 'Bookings Count', 
                                'Avg Stay Length', 'Avg Party Size']
        resort_metrics = resort_metrics.reset_index()
        
        # Resort performance visualization
        col1, col2 = st.columns(2)
        
        with col1:
            # Revenue by resort
            fig_resort_revenue = px.bar(
                resort_metrics, 
                x='resort_name', 
                y='Total Revenue',
                title="Total Revenue by Resort",
                color='Total Revenue',
                color_continuous_scale='blues'
            )
            fig_resort_revenue.update_xaxes(tickangle=45)
            st.plotly_chart(fig_resort_revenue, use_container_width=True)
        
        with col2:
            # Bookings by resort
            fig_bookings = px.pie(
                resort_metrics, 
                values='Bookings Count', 
                names='resort_name',
                title="Booking Distribution by Resort"
            )
            st.plotly_chart(fig_bookings, use_container_width=True)
        
        # Time series analysis
        st.markdown("### 📈 Booking Trends Over Time")
        
        # Monthly booking trends
        monthly_bookings = bookings.set_index('checkin_date').resample('M').agg({
            'total_cost': 'sum',
            'booking_id': 'count'
        }).reset_index()
        
        monthly_bookings['month'] = monthly_bookings['checkin_date'].dt.strftime('%Y-%m')
        
        fig_trends = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Revenue trend
        fig_trends.add_trace(
            go.Scatter(x=monthly_bookings['month'], y=monthly_bookings['total_cost'], 
                      name="Revenue", line=dict(color='blue')),
            secondary_y=False,
        )
        
        # Booking count trend
        fig_trends.add_trace(
            go.Scatter(x=monthly_bookings['month'], y=monthly_bookings['booking_id'], 
                      name="Bookings", line=dict(color='red')),
            secondary_y=True,
        )
        
        fig_trends.update_xaxes(title_text="Month")
        fig_trends.update_yaxes(title_text="Revenue ($)", secondary_y=False)
        fig_trends.update_yaxes(title_text="Number of Bookings", secondary_y=True)
        fig_trends.update_layout(title_text="Monthly Revenue and Booking Trends")
        
        st.plotly_chart(fig_trends, use_container_width=True)
    
    def render_dining_amenity_analytics(self, dining, amenities):
        """Display dining and amenity performance"""
        st.subheader("🍽️ Dining & Amenity Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Restaurant Performance")
            restaurant_performance = dining.groupby('restaurant_name').agg({
                'estimated_cost': ['sum', 'mean', 'count']
            }).round(2)
            
            restaurant_performance.columns = ['Total Revenue', 'Avg Cost', 'Reservations']
            restaurant_performance = restaurant_performance.reset_index()
            
            # Top restaurants by revenue
            top_restaurants = restaurant_performance.nlargest(5, 'Total Revenue')
            
            fig_restaurants = px.bar(
                top_restaurants,
                x='restaurant_name',
                y='Total Revenue',
                title="Top 5 Restaurants by Revenue",
                color='Total Revenue',
                color_continuous_scale='greens'
            )
            fig_restaurants.update_xaxes(tickangle=45)
            st.plotly_chart(fig_restaurants, use_container_width=True)
        
        with col2:
            st.markdown("#### Amenity Utilization")
            amenity_performance = amenities.groupby('amenity_type').agg({
                'cost': ['sum', 'mean', 'count'],
                'duration_minutes': 'mean'
            }).round(2)
            
            amenity_performance.columns = ['Total Revenue', 'Avg Cost', 'Usage Count', 'Avg Duration']
            amenity_performance = amenity_performance.reset_index()
            
            fig_amenities = px.scatter(
                amenity_performance,
                x='Usage Count',
                y='Total Revenue',
                size='Avg Duration',
                color='amenity_type',
                title="Amenity Performance: Usage vs Revenue",
                hover_data=['Avg Cost']
            )
            st.plotly_chart(fig_amenities, use_container_width=True)
        
        # Dining patterns by time
        st.markdown("#### Dining Patterns")
        dining_by_time = dining.groupby('meal_time')['estimated_cost'].agg(['sum', 'count']).reset_index()
        dining_by_time.columns = ['Meal Time', 'Revenue', 'Reservations']
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            fig_meal_revenue = px.pie(dining_by_time, values='Revenue', names='Meal Time',
                                    title="Revenue Distribution by Meal Time")
            st.plotly_chart(fig_meal_revenue, use_container_width=True)
        
        with col_b:
            fig_meal_count = px.bar(dining_by_time, x='Meal Time', y='Reservations',
                                  title="Reservations by Meal Time",
                                  color='Reservations', color_continuous_scale='oranges')
            st.plotly_chart(fig_meal_count, use_container_width=True)
    
    def render_predictive_insights(self, analytics_summary):
        """Display predictive model insights"""
        st.subheader("🔮 Predictive Analytics Insights")
        
        if analytics_summary:
            col1, col2 = st.columns(2)
            
            with col1:
                if 'satisfaction_model_performance' in analytics_summary:
                    satisfaction_perf = analytics_summary['satisfaction_model_performance']
                    st.markdown("#### Guest Satisfaction Predictor")
                    st.info(f"**Model Accuracy**: {satisfaction_perf.get('accuracy', 0):.1%}")
                    
                    if 'feature_importance' in satisfaction_perf:
                        # Feature importance chart
                        features_df = pd.DataFrame(satisfaction_perf['feature_importance'])
                        
                        fig_features = px.bar(
                            features_df.head(8), 
                            x='importance', 
                            y='feature',
                            orientation='h',
                            title="Top Factors Affecting Guest Satisfaction",
                            color='importance',
                            color_continuous_scale='viridis'
                        )
                        st.plotly_chart(fig_features, use_container_width=True)
            
            with col2:
                if 'spending_model_performance' in analytics_summary:
                    spending_perf = analytics_summary['spending_model_performance']
                    st.markdown("#### Spending Predictor")
                    st.info(f"**Model R² Score**: {spending_perf.get('r2_score', 0):.3f}")
                    st.info(f"**Prediction Error**: ${spending_perf.get('mae', 0):,.0f}")
                    
                    if 'feature_importance' in spending_perf:
                        # Spending prediction features
                        spend_features_df = pd.DataFrame(spending_perf['feature_importance'])
                        
                        fig_spend_features = px.bar(
                            spend_features_df.head(6), 
                            x='importance', 
                            y='feature',
                            orientation='h',
                            title="Top Factors Affecting Guest Spending",
                            color='importance',
                            color_continuous_scale='reds'
                        )
                        st.plotly_chart(fig_spend_features, use_container_width=True)
            
            # Key insights
            if 'key_insights' in analytics_summary:
                st.markdown("### 💡 Key Business Insights")
                for insight in analytics_summary['key_insights']:
                    st.markdown(f"""
                    <div class="insight-card">
                        <strong>📈 Business Insight:</strong> {insight}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("🔄 Predictive analytics not available. Run guest analytics pipeline to see model insights.")
    
    def render_sidebar_controls(self, bookings):
        """Render sidebar with dashboard controls"""
        st.sidebar.header("🎛️ Dashboard Controls")
        
        # Date range filter
        if not bookings.empty:
            bookings['checkin_date'] = pd.to_datetime(bookings['checkin_date'])
            min_date = bookings['checkin_date'].min().date()
            max_date = bookings['checkin_date'].max().date()
            
            st.sidebar.subheader("📅 Date Range")
            date_range = st.sidebar.date_input(
                "Select Date Range",
                value=[min_date, max_date],
                min_value=min_date,
                max_value=max_date
            )
        
        # Resort filter
        st.sidebar.subheader("🏨 Resort Selection")
        resort_options = ['All Resorts'] + list(self.resort_info.keys())
        selected_resorts = st.sidebar.multiselect(
            "Choose Resorts",
            resort_options,
            default=['All Resorts']
        )
        
        # Guest segment filter
        st.sidebar.subheader("👥 Guest Segments")
        segment_options = ['All Segments', 'Young Couples', 'Families with Toddlers', 
                          'Families with Teens', 'Multi-Generation', 'Empty Nesters',
                          'Business Travelers', 'International Families']
        selected_segments = st.sidebar.multiselect(
            "Choose Segments",
            segment_options,
            default=['All Segments']
        )
        
        # Dashboard refresh
        st.sidebar.subheader("🔄 Data Management")
        if st.sidebar.button("Refresh All Data"):
            st.cache_data.clear()
            st.success("✅ Dashboard data refreshed!")
            time.sleep(1)
            st.rerun()
        
        # Export options
        st.sidebar.subheader("📊 Export Options")
        st.sidebar.info("Export functionality would connect to data pipeline for report generation")
        
        return date_range if not bookings.empty else None, selected_resorts, selected_segments
    
    def _calculate_occupancy_rate(self, bookings):
        """Calculate occupancy rate - this calculation is probably not perfect but close enough"""
        if bookings.empty:
            return 0.0
        
        # TODO: this calculation doesn't account for different room types properly
        total_rooms = sum([info['rooms'] for info in self.resort_info.values()])
        total_room_nights = bookings['stay_length'].sum()
        total_capacity = total_rooms * len(bookings['checkin_date'].unique()) if len(bookings) > 0 else total_rooms
        
        occ_rate = total_room_nights / total_capacity if total_capacity > 0 else 0
        return min(occ_rate, 1.0)  # cap at 100%

def main():
    """Main dashboard application"""
    dashboard = ResortOperationsDashboard()
    
    # Load data
    bookings, guests, dining, amenities, analytics_df, analytics_summary, revenue_summary = dashboard.load_resort_data()
    
    # Render dashboard
    dashboard.render_dashboard_header()
    
    # Sidebar controls
    date_filter, resort_filter, segment_filter = dashboard.render_sidebar_controls(bookings)
    
    # Main dashboard content
    if not bookings.empty:
        # Key Performance Indicators
        dashboard.render_key_performance_indicators(bookings, guests, dining, amenities, revenue_summary)
        
        # Revenue optimization insights
        dashboard.render_revenue_optimization_insights(revenue_summary)
        
        # Guest segmentation analysis
        dashboard.render_guest_segmentation_analysis(analytics_summary)
        
        # Operational performance
        dashboard.render_operational_performance(bookings, dining, amenities)
        
        # Dining and amenity analytics
        dashboard.render_dining_amenity_analytics(dining, amenities)
        
        # Predictive insights
        dashboard.render_predictive_insights(analytics_summary)
        
    else:
        st.error("❌ No data available. Please run the data generation pipeline first.")
        st.info("Run the following commands to generate data:")
        st.code("""
        # Generate resort data
        python src/resort_data_generator.py
        
        # Run guest analytics
        python src/guest_analytics.py
        
        # Run revenue optimization
        python src/revenue_optimization.py
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p><strong>🏨 Disney Resort Operations Center</strong></p>
        <p>Advanced Analytics for Resort Management Excellence</p>
        <p><em>Optimizing guest experiences through data-driven insights</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()