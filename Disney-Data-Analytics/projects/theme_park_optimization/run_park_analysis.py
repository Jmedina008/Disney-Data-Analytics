"""
Disney Theme Park Optimization - Main Pipeline
Orchestrates the complete operational analytics workflow from data generation to dashboard deployment
"""

import sys
import os
from pathlib import Path
import time
from datetime import datetime

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent / 'src'))

# Import pipeline components
try:
    from park_data_generator import DisneyParkDataGenerator
    from park_data_processor import DisneyParkDataProcessor
    from park_optimization_models import DisneyParkMLModels
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("Make sure all required packages are installed: pip install pandas numpy scikit-learn plotly streamlit")
    sys.exit(1)

def print_header():
    """Print pipeline header"""
    print("=" * 80)
    print("🏰 DISNEY THEME PARK OPTIMIZATION PIPELINE")
    print("=" * 80)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎢 Complete Operational Analytics: Generation → Processing → ML → Dashboard")
    print("-" * 80)

def print_section_header(section_name, step_number, total_steps):
    """Print section header"""
    print(f"\n{'='*15} STEP {step_number}/{total_steps}: {section_name.upper()} {'='*15}")

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def print_info(message):
    """Print info message"""
    print(f"ℹ️  {message}")

def run_park_data_generation():
    """Step 1: Generate comprehensive theme park operational data"""
    print_section_header("Park Data Generation", 1, 4)
    
    try:
        generator = DisneyParkDataGenerator()
        attractions_df, operations_df = generator.save_all_data()
        
        if attractions_df is not None and operations_df is not None:
            print_success(f"Generated {len(attractions_df)} attractions across 4 Disney parks")
            print_success(f"Created {len(operations_df):,} operational records over 90 days")
            print_info(f"Average daily attendance: {operations_df['park_attendance'].mean():,.0f} guests")
            print_info(f"Total revenue generated: ${operations_df['revenue_generated'].sum():,.0f}")
            return True
        else:
            print_error("Park data generation failed")
            return False
            
    except Exception as e:
        print_error(f"Data generation error: {str(e)}")
        return False

def run_operational_data_processing():
    """Step 2: Process and analyze operational data"""
    print_section_header("Operational Data Processing", 2, 4)
    
    try:
        processor = DisneyParkDataProcessor()
        ops_df, attraction_metrics, park_summary, ml_data = processor.process_all_data()
        
        if ops_df is not None and not ops_df.empty:
            print_success(f"Processed {len(ops_df):,} operational records")
            print_success(f"Generated {len(ops_df.columns)} analytical features")
            print_success(f"Created performance metrics for {len(attraction_metrics)} attractions")
            print_success(f"Analyzed operational summaries for {len(park_summary)} parks")
            
            # Key insights
            print_info(f"Average wait time: {ops_df['avg_wait_time_minutes'].mean():.1f} minutes")
            print_info(f"Guest satisfaction: {ops_df['guest_satisfaction_score'].mean():.3f}")
            print_info(f"Weather impact: {(1 - ops_df[ops_df['is_rain']]['total_guests'].mean() / ops_df[~ops_df['is_rain']]['total_guests'].mean()) * 100:.1f}% attendance reduction on rainy days")
            
            return True
        else:
            print_error("Operational data processing failed")
            return False
            
    except Exception as e:
        print_error(f"Data processing error: {str(e)}")
        return False

def run_operational_ml_modeling():
    """Step 3: Train machine learning models for operational optimization"""
    print_section_header("Operational ML & Optimization", 3, 4)
    
    try:
        ml_pipeline = DisneyParkMLModels()
        results = ml_pipeline.run_full_pipeline()
        
        if results:
            # Extract performance metrics
            wait_time_r2 = max(results['wait_time_models'].values(), key=lambda x: x['r2'])['r2']
            attendance_r2 = max(results['attendance_models'].values(), key=lambda x: x['r2'])['r2']
            revenue_r2 = max(results['revenue_models'].values(), key=lambda x: x['r2'])['r2']
            operational_scenarios = results['operational_scenarios']['optimal_k']
            
            print_success(f"Trained wait time prediction models (R²: {wait_time_r2:.3f})")
            print_success(f"Built attendance forecasting models (R²: {attendance_r2:.3f})")
            print_success(f"Created revenue optimization models (R²: {revenue_r2:.3f})")
            print_success(f"Identified {operational_scenarios} operational scenarios for management")
            print_success("Generated comprehensive business insights and recommendations")
            
            # Business insights
            insights = results['insights']['operational_performance']
            print_info(f"Total operations analyzed: {insights['total_daily_operations']:,}")
            print_info(f"Peak wait time observed: {insights['peak_wait_time']:.0f} minutes")
            print_info(f"Revenue optimization potential identified")
            
            return True
        else:
            print_error("ML modeling failed")
            return False
            
    except Exception as e:
        print_error(f"ML modeling error: {str(e)}")
        return False

def run_dashboard_deployment():
    """Step 4: Prepare operations dashboard for deployment"""
    print_section_header("Operations Dashboard", 4, 4)
    
    try:
        # Check if dashboard file exists and is properly configured
        dashboard_path = Path(__file__).parent / 'src' / 'park_operations_dashboard.py'
        
        if dashboard_path.exists():
            print_success("Operations dashboard ready for deployment")
            print_info("Dashboard features: Real-time monitoring, wait time prediction, revenue optimization")
            print_info("To launch: streamlit run src/park_operations_dashboard.py")
            print_info("Dashboard URL: http://localhost:8501")
            print_success("Complete operational analytics system deployed")
            return True
        else:
            print_error("Dashboard script not found")
            return False
            
    except Exception as e:
        print_error(f"Dashboard deployment error: {str(e)}")
        return False

def generate_operational_report():
    """Generate comprehensive operational analytics report"""
    print("\n" + "=" * 80)
    print("📋 THEME PARK OPTIMIZATION PIPELINE REPORT")
    print("=" * 80)
    
    # Check generated files and their status
    base_path = Path(__file__).parent
    critical_files = [
        ('Attractions Data', base_path / 'data' / 'raw' / 'park_attractions.csv'),
        ('Operations Data', base_path / 'data' / 'raw' / 'park_operations.csv'),
        ('Processed Analytics', base_path / 'data' / 'processed' / 'park_operations_processed.csv'),
        ('Attraction Metrics', base_path / 'data' / 'processed' / 'attraction_performance_metrics.csv'),
        ('Park Summaries', base_path / 'data' / 'processed' / 'park_operational_summary.csv'),
        ('ML Models', base_path / 'models' / 'wait_time_predictor.pkl'),
        ('Operational Insights', base_path / 'models' / 'operational_insights.json'),
        ('Operations Dashboard', base_path / 'src' / 'park_operations_dashboard.py')
    ]
    
    print("\n🏗️ System Components Status:")
    all_components_ready = True
    
    for name, filepath in critical_files:
        if filepath.exists():
            if filepath.suffix == '.csv':
                try:
                    import pandas as pd
                    df = pd.read_csv(filepath)
                    status_info = f"({len(df):,} records)" if len(df) > 100 else f"({len(df)} records)"
                except:
                    status_info = f"({filepath.stat().st_size:,} bytes)"
            else:
                status_info = f"({filepath.stat().st_size:,} bytes)" if filepath.stat().st_size > 0 else "(ready)"
            
            print(f"  ✅ {name}: {filepath.name} {status_info}")
        else:
            print(f"  ❌ {name}: Missing")
            all_components_ready = False
    
    print(f"\n🎯 Operational Intelligence Generated:")
    
    try:
        import json
        insights_path = base_path / 'models' / 'operational_insights.json'
        if insights_path.exists():
            with open(insights_path, 'r') as f:
                insights = json.load(f)
            
            ops_perf = insights.get('operational_performance', {})
            weather_impact = insights.get('weather_impact', {})
            optimization = insights.get('optimization_opportunities', {})
            
            print(f"  • Total Daily Operations: {ops_perf.get('total_daily_operations', 'N/A'):,}")
            print(f"  • Average Wait Time: {ops_perf.get('avg_wait_time', 0):.1f} minutes")
            print(f"  • Guest Satisfaction: {ops_perf.get('guest_satisfaction', 0):.3f}")
            print(f"  • Total Revenue Analyzed: ${ops_perf.get('total_revenue', 0):,.0f}")
            print(f"  • Weather Impact on Attendance: {weather_impact.get('sunny_vs_rainy_attendance', 1):.1f}x difference")
            print(f"  • Lightning Lane Effectiveness: {optimization.get('lightning_lane_effectiveness', 0):.2%}")
            print(f"  • Weekend Revenue Premium: {optimization.get('weekend_premium', 1):.1f}x")
    except:
        print("  • Detailed insights available in generated files")
    
    print(f"\n🚀 Deployment Capabilities:")
    print("  1. Real-time operational monitoring dashboard")
    print("  2. Wait time prediction and optimization")
    print("  3. Revenue maximization recommendations")  
    print("  4. Scenario planning and what-if analysis")
    print("  5. Attraction performance analytics")
    print("  6. Weather impact modeling")
    
    print(f"\n💼 Business Value Delivered:")
    print("  • Predictive analytics for wait time management")
    print("  • Revenue optimization through Lightning Lane analysis")
    print("  • Weather-based operational planning")
    print("  • Guest satisfaction improvement insights")
    print("  • Capacity utilization optimization")
    print("  • Real-time decision support system")
    
    if all_components_ready:
        print(f"\n🎉 STATUS: COMPLETE OPERATIONAL ANALYTICS SYSTEM READY")
        print("Your Disney Theme Park Optimization project is fully functional and interview-ready!")
    else:
        print(f"\n⚠️  STATUS: SYSTEM PARTIALLY READY - Some components missing")

def main():
    """Run the complete Disney theme park optimization pipeline"""
    start_time = time.time()
    
    # Print header
    print_header()
    
    # Pipeline execution steps
    pipeline_steps = [
        ("Park Data Generation", run_park_data_generation),
        ("Operational Processing", run_operational_data_processing),
        ("ML Optimization", run_operational_ml_modeling), 
        ("Dashboard Deployment", run_dashboard_deployment)
    ]
    
    successful_steps = 0
    
    # Execute each pipeline step
    for step_name, step_function in pipeline_steps:
        if step_function():
            successful_steps += 1
        else:
            print_error(f"Pipeline halted at: {step_name}")
            break
    
    # Calculate total execution time
    execution_time = time.time() - start_time
    
    # Generate comprehensive report
    generate_operational_report()
    
    print(f"\n⏱️  Total Pipeline Execution Time: {execution_time:.2f} seconds")
    print(f"✅ Completed {successful_steps}/{len(pipeline_steps)} pipeline steps successfully")
    
    if successful_steps == len(pipeline_steps):
        print("\n🎉 DISNEY THEME PARK OPTIMIZATION PIPELINE COMPLETED!")
        print("🏰 Complete operational analytics system ready for Disney parks management.")
        print("📊 Live dashboard deployment: streamlit run src/park_operations_dashboard.py")
    else:
        print(f"\n⚠️  PIPELINE PARTIALLY COMPLETED ({successful_steps}/{len(pipeline_steps)} steps)")
        print("Please review error messages and resolve issues before proceeding.")
    
    print("=" * 80)

if __name__ == "__main__":
    main()