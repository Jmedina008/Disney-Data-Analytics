"""
Disney Theme Park Operations Dashboard
Real-time operational analytics and management dashboard for Disney parks
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
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Disney Park Operations",
    page_icon="🏰",
    layout="wide",
    initial_sidebar_state="expanded"
)

class DisneyParkOperationsDashboard:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.data_path = self.base_path / 'data' / 'processed'
        self.models_path = self.base_path / 'models'
        
    @st.cache_data
    def load_operational_data(_self):
        """Load processed operational data with caching"""
        try:
            ops_df = pd.read_csv(_self.data_path / 'park_operations_processed.csv')
            attractions_df = pd.read_csv(_self.data_path / 'attraction_performance_metrics.csv')
            park_summary = pd.read_csv(_self.data_path / 'park_operational_summary.csv')
            
            return ops_df, attractions_df, park_summary
        except FileNotFoundError:
            st.error("❌ Data not found. Please run the data generation and processing scripts first.")
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
    @st.cache_data
    def load_insights(_self):
        """Load operational insights with caching"""
        try:
            with open(_self.models_path / 'operational_insights.json', 'r') as f:
                insights = json.load(f)
            return insights
        except FileNotFoundError:
            return {}
    
    def render_header(self):
        """Render dashboard header"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.title("🏰 Disney Park Operations Center")
            st.markdown("### Real-Time Operational Analytics & Management")
            st.markdown("---")
    
    def render_sidebar(self, ops_df):
        """Render sidebar with operational controls and filters"""
        st.sidebar.header("🎛️ Operations Control Center")
        
        # Current status overview
        st.sidebar.subheader("Current Status")
        current_date = datetime.now().strftime('%Y-%m-%d')
        st.sidebar.info(f"📅 **Date**: {current_date}")
        st.sidebar.info(f"🌡️ **Weather**: Partly Cloudy, 82°F")
        st.sidebar.info(f"👥 **Live Attendance**: 67,500 guests")
        
        # Operational filters
        st.sidebar.subheader("Data Filters")
        
        # Park filter
        parks = ['All Parks'] + list(ops_df['park'].unique())
        selected_park = st.sidebar.selectbox("Select Park", parks)
        
        # Date range filter
        ops_df['date'] = pd.to_datetime(ops_df['date'])
        date_range = st.sidebar.date_input(
            "Date Range",
            value=[ops_df['date'].min().date(), ops_df['date'].max().date()],
            min_value=ops_df['date'].min().date(),
            max_value=ops_df['date'].max().date()
        )
        
        # Weather condition filter
        weather_conditions = ['All Conditions'] + list(ops_df['weather_condition'].unique())
        selected_weather = st.sidebar.selectbox("Weather Condition", weather_conditions)
        
        # Alert thresholds
        st.sidebar.subheader("⚠️ Alert Thresholds")
        wait_time_threshold = st.sidebar.slider("Max Wait Time (min)", 30, 180, 120)
        satisfaction_threshold = st.sidebar.slider("Min Guest Satisfaction", 0.0, 1.0, 0.7)
        
        # Apply filters
        filtered_df = ops_df.copy()
        
        if selected_park != 'All Parks':
            filtered_df = filtered_df[filtered_df['park'] == selected_park]
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            filtered_df = filtered_df[
                (filtered_df['date'] >= pd.Timestamp(start_date)) & 
                (filtered_df['date'] <= pd.Timestamp(end_date))
            ]
        
        if selected_weather != 'All Conditions':
            filtered_df = filtered_df[filtered_df['weather_condition'] == selected_weather]
        
        return filtered_df, wait_time_threshold, satisfaction_threshold
    
    def render_operational_kpis(self, ops_df, insights):
        """Render key operational performance indicators"""
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            avg_wait = ops_df['avg_wait_time_minutes'].mean()
            st.metric(
                "Avg Wait Time",
                f"{avg_wait:.1f} min",
                delta=f"{avg_wait - 90:+.1f} vs target"
            )
        
        with col2:
            satisfaction = ops_df['guest_satisfaction_score'].mean()
            st.metric(
                "Guest Satisfaction",
                f"{satisfaction:.2%}",
                delta=f"{satisfaction - 0.75:+.1%} vs target"
            )
        
        with col3:
            avg_attendance = ops_df['park_attendance'].mean()
            st.metric(
                "Daily Attendance",
                f"{avg_attendance:,.0f}",
                delta=None
            )
        
        with col4:
            capacity_util = ops_df['capacity_utilization'].mean()
            st.metric(
                "Capacity Utilization",
                f"{capacity_util:.1%}",
                delta=f"{capacity_util - 0.8:+.1%} vs optimal"
            )
        
        with col5:
            revenue = ops_df['revenue_generated'].sum()
            st.metric(
                "Total Revenue",
                f"${revenue/1e6:.1f}M",
                delta=None
            )
    
    def render_realtime_monitoring(self, ops_df, wait_time_threshold, satisfaction_threshold):
        """Render real-time park monitoring"""
        st.subheader("📊 Real-Time Park Monitoring")
        
        # Current alerts
        high_wait_attractions = ops_df[ops_df['avg_wait_time_minutes'] > wait_time_threshold]
        low_satisfaction = ops_df[ops_df['guest_satisfaction_score'] < satisfaction_threshold]
        
        col1, col2 = st.columns(2)
        
        with col1:
            if len(high_wait_attractions) > 0:
                st.warning(f"⚠️ **{len(high_wait_attractions)} attractions** exceed wait time threshold")
                top_wait_issues = high_wait_attractions.nlargest(5, 'avg_wait_time_minutes')[
                    ['attraction_name', 'park', 'avg_wait_time_minutes']
                ]
                st.dataframe(top_wait_issues, use_container_width=True)
        
        with col2:
            if len(low_satisfaction) > 0:
                st.error(f"🔴 **{len(low_satisfaction)} operations** below satisfaction threshold")
                satisfaction_issues = low_satisfaction.nsmallest(5, 'guest_satisfaction_score')[
                    ['attraction_name', 'park', 'guest_satisfaction_score']
                ]
                st.dataframe(satisfaction_issues, use_container_width=True)
        
        # Live operational map
        st.subheader("🗺️ Live Operational Status")
        
        # Create operational status visualization
        park_status = ops_df.groupby('park').agg({
            'avg_wait_time_minutes': 'mean',
            'guest_satisfaction_score': 'mean',
            'capacity_utilization': 'mean',
            'total_guests': 'sum'
        }).reset_index()
        
        # Status color coding
        def get_status_color(wait_time, satisfaction):
            if wait_time > 120 or satisfaction < 0.6:
                return 'red'
            elif wait_time > 90 or satisfaction < 0.7:
                return 'orange'
            else:
                return 'green'
        
        park_status['status_color'] = park_status.apply(
            lambda x: get_status_color(x['avg_wait_time_minutes'], x['guest_satisfaction_score']), 
            axis=1
        )
        
        fig = px.scatter(
            park_status,
            x='avg_wait_time_minutes',
            y='guest_satisfaction_score',
            size='total_guests',
            color='status_color',
            hover_name='park',
            title="Park Operational Status Matrix",
            labels={
                'avg_wait_time_minutes': 'Average Wait Time (minutes)',
                'guest_satisfaction_score': 'Guest Satisfaction Score'
            }
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    def render_wait_time_analysis(self, ops_df):
        """Render wait time analysis and predictions"""
        st.subheader("⏱️ Wait Time Analysis & Optimization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Wait time trends by park
            wait_trends = ops_df.groupby(['date', 'park'])['avg_wait_time_minutes'].mean().reset_index()
            wait_trends['date'] = pd.to_datetime(wait_trends['date'])
            
            fig = px.line(
                wait_trends,
                x='date',
                y='avg_wait_time_minutes',
                color='park',
                title="Wait Time Trends by Park",
                labels={'avg_wait_time_minutes': 'Average Wait Time (minutes)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Wait time distribution
            fig = px.histogram(
                ops_df,
                x='avg_wait_time_minutes',
                color='park',
                title="Wait Time Distribution",
                nbins=30,
                labels={'avg_wait_time_minutes': 'Wait Time (minutes)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Wait time predictor
        st.subheader("🔮 Wait Time Predictor")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            pred_park = st.selectbox("Park", ops_df['park'].unique())
            pred_weather = st.selectbox("Weather", ops_df['weather_condition'].unique())
        
        with col2:
            pred_attendance = st.slider("Expected Attendance", 20000, 100000, 60000)
            pred_temperature = st.slider("Temperature (°F)", 60, 100, 80)
        
        with col3:
            is_weekend = st.checkbox("Weekend")
            is_holiday = st.checkbox("Holiday Season")
        
        if st.button("🎯 Predict Wait Times"):
            # Simplified prediction logic (in real implementation, would use trained ML model)
            base_wait = 45
            
            # Park multipliers
            park_multipliers = {
                'Magic Kingdom': 1.4,
                'Hollywood Studios': 1.2,
                'EPCOT': 1.0,
                'Animal Kingdom': 0.9
            }
            base_wait *= park_multipliers.get(pred_park, 1.0)
            
            # Attendance impact
            base_wait *= (pred_attendance / 60000) ** 0.8
            
            # Weather impact
            if pred_weather in ['Light Rain', 'Heavy Rain']:
                base_wait *= 0.7
            elif pred_weather == 'Sunny':
                base_wait *= 1.1
            
            # Day type impact
            if is_weekend:
                base_wait *= 1.3
            if is_holiday:
                base_wait *= 1.5
            
            predicted_wait = max(15, min(180, base_wait))
            
            st.success(f"🎯 **Predicted Average Wait Time**: {predicted_wait:.0f} minutes")
            
            # Recommendations
            recommendations = []
            if predicted_wait > 120:
                recommendations.append("🚨 Implement Lightning Lane dynamic pricing")
                recommendations.append("👥 Deploy additional staff to popular attractions")
                recommendations.append("📱 Push mobile notifications for wait time management")
            elif predicted_wait > 90:
                recommendations.append("⚡ Activate Lightning Lane promotions")
                recommendations.append("🎪 Deploy entertainment to queue areas")
            
            if recommendations:
                st.info("💡 **Recommendations**: " + " • ".join(recommendations))
    
    def render_revenue_optimization(self, ops_df):
        """Render revenue optimization analysis"""
        st.subheader("💰 Revenue Optimization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Revenue by park
            revenue_by_park = ops_df.groupby('park')['revenue_generated'].sum().sort_values(ascending=True)
            
            fig = px.bar(
                x=revenue_by_park.values,
                y=revenue_by_park.index,
                orientation='h',
                title="Revenue by Park",
                labels={'x': 'Revenue ($)', 'y': 'Park'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Revenue per guest trends
            ops_df['date'] = pd.to_datetime(ops_df['date'])
            revenue_trends = ops_df.groupby('date')['revenue_per_guest'].mean().reset_index()
            
            fig = px.line(
                revenue_trends,
                x='date',
                y='revenue_per_guest',
                title="Revenue per Guest Trends",
                labels={'revenue_per_guest': 'Revenue per Guest ($)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Lightning Lane effectiveness
        st.subheader("⚡ Lightning Lane Performance")
        
        ll_effectiveness = ops_df.groupby('park').agg({
            'lightning_lane_ratio': 'mean',
            'revenue_per_guest': 'mean',
            'guest_satisfaction_score': 'mean'
        }).reset_index()
        
        fig = px.scatter(
            ll_effectiveness,
            x='lightning_lane_ratio',
            y='revenue_per_guest',
            size='guest_satisfaction_score',
            color='park',
            title="Lightning Lane Usage vs Revenue Impact",
            labels={
                'lightning_lane_ratio': 'Lightning Lane Usage Rate',
                'revenue_per_guest': 'Revenue per Guest ($)'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def render_operational_scenarios(self):
        """Render operational scenario planning"""
        st.subheader("🎭 Operational Scenario Planning")
        
        try:
            with open(self.models_path / 'operational_insights.json', 'r') as f:
                insights = json.load(f)
            
            # Scenario simulation
            st.subheader("🔮 Scenario Simulator")
            
            col1, col2 = st.columns(2)
            
            with col1:
                scenario_attendance = st.slider("Scenario Attendance", 30000, 100000, 70000)
                scenario_weather = st.selectbox("Scenario Weather", 
                                               ["Sunny", "Partly Cloudy", "Light Rain", "Heavy Rain"])
            
            with col2:
                scenario_season = st.selectbox("Season", ["Regular", "Summer Peak", "Holiday Season"])
                scenario_day = st.selectbox("Day Type", ["Weekday", "Weekend"])
            
            if st.button("🎯 Simulate Scenario"):
                # Calculate scenario impacts
                base_satisfaction = 0.75
                base_wait_time = 60
                base_revenue = 500000
                
                # Attendance impact
                attendance_factor = scenario_attendance / 70000
                base_wait_time *= attendance_factor ** 0.8
                base_revenue *= attendance_factor
                
                # Weather impact
                weather_multipliers = {
                    "Sunny": {"satisfaction": 1.1, "wait": 1.0, "revenue": 1.1},
                    "Partly Cloudy": {"satisfaction": 1.0, "wait": 1.0, "revenue": 1.0},
                    "Light Rain": {"satisfaction": 0.8, "wait": 0.7, "revenue": 0.8},
                    "Heavy Rain": {"satisfaction": 0.6, "wait": 0.5, "revenue": 0.6}
                }
                
                multiplier = weather_multipliers[scenario_weather]
                base_satisfaction *= multiplier["satisfaction"]
                base_wait_time *= multiplier["wait"]
                base_revenue *= multiplier["revenue"]
                
                # Season impact
                if scenario_season == "Summer Peak":
                    base_satisfaction *= 0.9
                    base_wait_time *= 1.4
                    base_revenue *= 1.3
                elif scenario_season == "Holiday Season":
                    base_satisfaction *= 0.85
                    base_wait_time *= 1.6
                    base_revenue *= 1.5
                
                # Day type impact
                if scenario_day == "Weekend":
                    base_wait_time *= 1.2
                    base_revenue *= 1.2
                
                # Display results
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Predicted Satisfaction", f"{min(base_satisfaction, 1.0):.2%}")
                
                with col2:
                    st.metric("Predicted Wait Time", f"{base_wait_time:.0f} min")
                
                with col3:
                    st.metric("Predicted Revenue", f"${base_revenue:,.0f}")
                
                # Operational recommendations
                recommendations = []
                if base_wait_time > 120:
                    recommendations.append("Deploy maximum staffing levels")
                    recommendations.append("Implement premium Lightning Lane pricing")
                if base_satisfaction < 0.7:
                    recommendations.append("Activate guest experience enhancement protocols")
                if scenario_weather in ["Light Rain", "Heavy Rain"]:
                    recommendations.append("Prepare indoor alternatives and weather protection")
                
                if recommendations:
                    st.info("🎯 **Operational Recommendations**: \n• " + "\n• ".join(recommendations))
                    
        except FileNotFoundError:
            st.info("Run the ML pipeline to enable advanced scenario planning")
    
    def render_attraction_performance(self, attractions_df):
        """Render individual attraction performance analysis"""
        st.subheader("🎢 Attraction Performance Analysis")
        
        if not attractions_df.empty:
            # Top and bottom performers
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🏆 Top Performing Attractions")
                top_performers = attractions_df.nlargest(10, 'guest_satisfaction_score_mean')[
                    ['attraction_name_first', 'park_first', 'guest_satisfaction_score_mean', 'revenue_generated_sum']
                ]
                top_performers.columns = ['Attraction', 'Park', 'Satisfaction', 'Total Revenue']
                st.dataframe(top_performers, use_container_width=True)
            
            with col2:
                st.subheader("⚠️ Needs Attention")
                needs_attention = attractions_df.nsmallest(5, 'guest_satisfaction_score_mean')[
                    ['attraction_name_first', 'park_first', 'guest_satisfaction_score_mean', 'avg_wait_time_minutes_mean']
                ]
                needs_attention.columns = ['Attraction', 'Park', 'Satisfaction', 'Avg Wait Time']
                st.dataframe(needs_attention, use_container_width=True)
            
            # Performance correlation analysis
            fig = px.scatter(
                attractions_df,
                x='avg_wait_time_minutes_mean',
                y='guest_satisfaction_score_mean',
                size='revenue_generated_sum',
                color='park_first',
                hover_name='attraction_name_first',
                title="Wait Time vs Satisfaction by Attraction",
                labels={
                    'avg_wait_time_minutes_mean': 'Average Wait Time (minutes)',
                    'guest_satisfaction_score_mean': 'Guest Satisfaction Score'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def run_dashboard(self):
        """Main dashboard execution"""
        # Header
        self.render_header()
        
        # Load data
        ops_df, attractions_df, park_summary = self.load_operational_data()
        insights = self.load_insights()
        
        if ops_df.empty:
            st.error("No operational data available. Please run the data generation scripts first.")
            return
        
        # Sidebar with operational controls
        filtered_df, wait_threshold, satisfaction_threshold = self.render_sidebar(ops_df)
        
        # Main dashboard content
        st.subheader(f"📈 Operations Overview ({len(filtered_df):,} records)")
        
        # KPIs
        self.render_operational_kpis(filtered_df, insights)
        
        st.markdown("---")
        
        # Main operational tabs
        tabs = st.tabs([
            "🔴 Live Monitoring",
            "⏱️ Wait Time Management", 
            "💰 Revenue Optimization",
            "🎭 Scenario Planning",
            "🎢 Attraction Performance"
        ])
        
        with tabs[0]:
            self.render_realtime_monitoring(filtered_df, wait_threshold, satisfaction_threshold)
        
        with tabs[1]:
            self.render_wait_time_analysis(filtered_df)
        
        with tabs[2]:
            self.render_revenue_optimization(filtered_df)
        
        with tabs[3]:
            self.render_operational_scenarios()
        
        with tabs[4]:
            self.render_attraction_performance(attractions_df)
        
        # Footer
        st.markdown("---")
        st.markdown("**Disney Park Operations Center** | Real-Time Analytics for Guest Experience Excellence")

def main():
    """Run the park operations dashboard"""
    dashboard = DisneyParkOperationsDashboard()
    dashboard.run_dashboard()

if __name__ == "__main__":
    main()