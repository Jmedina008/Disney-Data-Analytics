"""
Disney+ Content Analytics - Main Pipeline
Orchestrates the complete data science workflow from data generation to dashboard deployment
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
    from data_generator import DisneyPlusDataGenerator
    from data_processor import DisneyPlusDataProcessor
    from models import DisneyPlusMLModels
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("Make sure all required packages are installed: pip install pandas numpy scikit-learn plotly streamlit")
    sys.exit(1)

def print_header():
    """Print pipeline header"""
    print("=" * 80)
    print("🎬 DISNEY+ CONTENT ANALYTICS PIPELINE")
    print("=" * 80)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("📊 Full Data Science Workflow: Generation → Processing → Modeling → Insights")
    print("-" * 80)

def print_section_header(section_name, step_number, total_steps):
    """Print section header"""
    print(f"\n{'='*20} STEP {step_number}/{total_steps}: {section_name.upper()} {'='*20}")

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def print_info(message):
    """Print info message"""
    print(f"ℹ️  {message}")

def run_data_generation():
    """Step 1: Generate synthetic Disney+ data"""
    print_section_header("Data Generation", 1, 4)
    
    try:
        generator = DisneyPlusDataGenerator()
        df = generator.save_data()
        
        if df is not None and not df.empty:
            print_success(f"Generated {len(df)} content records")
            print_info(f"Average rating: {df['imdb_rating'].mean():.2f}")
            print_info(f"Total viewership: {df['total_views'].sum():,}")
            return True
        else:
            print_error("Data generation failed")
            return False
            
    except Exception as e:
        print_error(f"Data generation error: {str(e)}")
        return False

def run_data_processing():
    """Step 2: Process and clean the data"""
    print_section_header("Data Processing & Feature Engineering", 2, 4)
    
    try:
        processor = DisneyPlusDataProcessor()
        df, studio_stats = processor.process_all()
        
        if df is not None and not df.empty:
            print_success(f"Processed {len(df)} records")
            print_success(f"Engineered {len(df.columns)} total features")
            print_success(f"Analyzed {len(studio_stats)} studios")
            return True
        else:
            print_error("Data processing failed")
            return False
            
    except Exception as e:
        print_error(f"Data processing error: {str(e)}")
        return False

def run_ml_modeling():
    """Step 3: Train ML models and generate insights"""
    print_section_header("Machine Learning & Predictive Analytics", 3, 4)
    
    try:
        ml_pipeline = DisneyPlusMLModels()
        results = ml_pipeline.run_full_pipeline()
        
        if results:
            # Extract key metrics
            best_r2 = max(results['viewership_models'].values(), key=lambda x: x['r2'])['r2']
            n_clusters = results['clustering']['optimal_k']
            
            print_success(f"Trained {len(results['viewership_models'])} prediction models")
            print_success(f"Best model R²: {best_r2:.3f}")
            print_success(f"Identified {n_clusters} content clusters")
            print_success("Generated business insights and recommendations")
            return True
        else:
            print_error("ML modeling failed")
            return False
            
    except Exception as e:
        print_error(f"ML modeling error: {str(e)}")
        return False

def run_dashboard_setup():
    """Step 4: Prepare dashboard for deployment"""
    print_section_header("Dashboard Setup", 4, 4)
    
    try:
        # Check if dashboard file exists
        dashboard_path = Path(__file__).parent / 'src' / 'dashboard.py'
        
        if dashboard_path.exists():
            print_success("Dashboard script ready")
            print_info("To launch dashboard: streamlit run src/dashboard.py")
            print_info("Dashboard will be available at: http://localhost:8501")
            return True
        else:
            print_error("Dashboard script not found")
            return False
            
    except Exception as e:
        print_error(f"Dashboard setup error: {str(e)}")
        return False

def generate_final_report():
    """Generate final pipeline report"""
    print("\n" + "=" * 80)
    print("📋 PIPELINE EXECUTION SUMMARY")
    print("=" * 80)
    
    # Check output files
    base_path = Path(__file__).parent
    output_files = [
        ('Raw Data', base_path / 'data' / 'raw' / 'disney_plus_content.csv'),
        ('Processed Data', base_path / 'data' / 'processed' / 'disney_plus_content_processed.csv'),
        ('Studio Analysis', base_path / 'data' / 'processed' / 'studio_performance_analysis.csv'),
        ('ML Models', base_path / 'models' / 'viewership_predictor.pkl'),
        ('Business Insights', base_path / 'models' / 'business_insights.json'),
        ('Dashboard', base_path / 'src' / 'dashboard.py')
    ]
    
    print("\n📁 Generated Files:")
    for name, filepath in output_files:
        if filepath.exists():
            if filepath.suffix == '.csv':
                try:
                    import pandas as pd
                    df = pd.read_csv(filepath)
                    size_info = f"({len(df)} records)"
                except:
                    size_info = f"({filepath.stat().st_size} bytes)"
            else:
                size_info = f"({filepath.stat().st_size} bytes)"
            
            print(f"  ✅ {name}: {filepath.name} {size_info}")
        else:
            print(f"  ❌ {name}: Missing")
    
    print(f"\n🎯 Key Business Insights:")
    
    try:
        import json
        insights_path = base_path / 'models' / 'business_insights.json'
        if insights_path.exists():
            with open(insights_path, 'r') as f:
                insights = json.load(f)
            
            content_perf = insights.get('content_performance', {})
            revenue_drivers = insights.get('revenue_drivers', {})
            
            print(f"  • Total Content Analyzed: {content_perf.get('total_content', 'N/A')}")
            print(f"  • Top Performing Studio: {content_perf.get('top_performing_studio', 'N/A')}")
            print(f"  • Most Engaging Genre: {content_perf.get('most_engaging_genre', 'N/A')}")
            print(f"  • Franchise Premium: {revenue_drivers.get('franchise_premium', 'N/A'):.1f}x")
    except:
        print("  • Business insights not available")
    
    print(f"\n🚀 Next Steps:")
    print("  1. Launch dashboard: streamlit run src/dashboard.py")
    print("  2. Explore interactive visualizations and filters")
    print("  3. Use the AI-powered content success predictor")
    print("  4. Review business recommendations for strategy")

def main():
    """Run the complete Disney+ analytics pipeline"""
    start_time = time.time()
    
    # Print header
    print_header()
    
    # Pipeline steps
    steps = [
        ("Data Generation", run_data_generation),
        ("Data Processing", run_data_processing), 
        ("ML Modeling", run_ml_modeling),
        ("Dashboard Setup", run_dashboard_setup)
    ]
    
    successful_steps = 0
    
    # Execute pipeline steps
    for step_name, step_function in steps:
        if step_function():
            successful_steps += 1
        else:
            print_error(f"Pipeline failed at: {step_name}")
            break
    
    # Calculate execution time
    execution_time = time.time() - start_time
    
    # Generate final report
    generate_final_report()
    
    print(f"\n⏱️  Total Execution Time: {execution_time:.2f} seconds")
    print(f"✅ Completed {successful_steps}/{len(steps)} pipeline steps")
    
    if successful_steps == len(steps):
        print("\n🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        print("Your Disney+ Content Analytics project is ready for demonstration.")
    else:
        print(f"\n⚠️  PIPELINE PARTIALLY COMPLETED ({successful_steps}/{len(steps)} steps)")
        print("Please check error messages above and resolve any issues.")
    
    print("=" * 80)

if __name__ == "__main__":
    main()