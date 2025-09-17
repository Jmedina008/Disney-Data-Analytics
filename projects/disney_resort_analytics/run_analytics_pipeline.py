#!/usr/bin/env python3
"""
Main Pipeline Runner

Runs the whole analytics pipeline end-to-end. Started as a simple script but grew into
a proper pipeline manager with options and error handling.

Usage:
    python run_analytics_pipeline.py  # runs everything
    python run_analytics_pipeline.py --dashboard-only  # just launch dashboard
    
TODO: Add parallel processing for the ML steps
TODO: Better error recovery if one component fails
"""

import sys
import subprocess
import argparse
import time
from pathlib import Path

def run_command(command, description, cwd=None):
    """Execute a command and handle results"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    
    try:
        if cwd:
            result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, shell=True)
        else:
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
        
        if result.returncode == 0:
            print(f"✅ {description} - COMPLETED SUCCESSFULLY")
            if result.stdout:
                print("Output:")
                print(result.stdout[-500:])  # Show last 500 characters
        else:
            print(f"❌ {description} - FAILED")
            print("Error:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ {description} - EXCEPTION: {str(e)}")
        return False
    
    return True

def check_dependencies():
    """Check if we have all the required packages - saves headaches later"""
    print("\n🔍 Checking dependencies...")
    
    required_packages = [
        'pandas', 'numpy', 'scikit-learn', 
        'plotly', 'streamlit', 'faker'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - missing")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Auto-installing missing packages...")
        
        install_cmd = f"{sys.executable} -m pip install {' '.join(missing_packages)}"
        if not run_command(install_cmd, "Installing missing dependencies"):
            print("❌ Failed to install dependencies. Please install manually:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    
    print("✅ All dependencies are available!")
    return True

def main():
    """Main pipeline runner - coordinates everything"""
    
    print("🏨 Disney Resort Analytics Pipeline")
    print("=" * 50)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run Disney Resort Analytics Pipeline")
    parser.add_argument('--skip-data', action='store_true', help='Skip data generation step')
    parser.add_argument('--skip-analytics', action='store_true', help='Skip guest analytics step')
    parser.add_argument('--skip-revenue', action='store_true', help='Skip revenue optimization step')
    parser.add_argument('--dashboard-only', action='store_true', help='Launch dashboard only')
    parser.add_argument('--install-deps', action='store_true', help='Install dependencies from requirements.txt')
    
    args = parser.parse_args()
    
    # Make sure we're in the right place
    current_dir = Path.cwd()
    print(f"📁 Working directory: {current_dir}")
    
    # Install dependencies if requested
    if args.install_deps:
        if not run_command(f"{sys.executable} -m pip install -r requirements.txt", 
                          "Installing dependencies from requirements.txt"):
            print("❌ Failed to install dependencies")
            return
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed. Exiting...")
        return
    
    # Dashboard only mode
    if args.dashboard_only:
        print("\n🎯 Dashboard-only mode activated")
        print("📊 Launching Disney Resort Operations Dashboard...")
        run_command("streamlit run src/resort_dashboard.py", 
                   "Launching Resort Operations Dashboard")
        return
    
    # Pipeline execution
    success_count = 0
    total_steps = 4
    
    # Step 1: Generate Resort Data
    if not args.skip_data:
        print("\n" + "="*60)
        print("📊 STEP 1: GENERATING RESORT OPERATIONAL DATA")
        print("="*60)
        
        if run_command("python src/resort_data_generator.py", 
                      "Generating synthetic resort operational data"):
            success_count += 1
            print("✅ Resort data generation completed successfully")
            time.sleep(2)  # Brief pause
        else:
            print("❌ Data generation failed. Continuing with existing data...")
    else:
        print("\n⏭️  STEP 1: Skipped - Data generation")
        success_count += 1
    
    # Step 2: Guest Analytics
    if not args.skip_analytics:
        print("\n" + "="*60)
        print("🧠 STEP 2: GUEST ANALYTICS & SEGMENTATION")
        print("="*60)
        
        if run_command("python src/guest_analytics.py", 
                      "Running guest analytics and machine learning models"):
            success_count += 1
            print("✅ Guest analytics completed successfully")
            time.sleep(2)
        else:
            print("❌ Guest analytics failed. Continuing...")
    else:
        print("\n⏭️  STEP 2: Skipped - Guest analytics")
        success_count += 1
    
    # Step 3: Revenue Optimization
    if not args.skip_revenue:
        print("\n" + "="*60)
        print("💰 STEP 3: REVENUE OPTIMIZATION ANALYSIS")
        print("="*60)
        
        if run_command("python src/revenue_optimization.py", 
                      "Running revenue optimization models and analysis"):
            success_count += 1
            print("✅ Revenue optimization completed successfully")
            time.sleep(2)
        else:
            print("❌ Revenue optimization failed. Continuing...")
    else:
        print("\n⏭️  STEP 3: Skipped - Revenue optimization")
        success_count += 1
    
    # Step 4: Launch Dashboard
    print("\n" + "="*60)
    print("🖥️  STEP 4: LAUNCHING INTERACTIVE DASHBOARD")
    print("="*60)
    
    print("🎯 All pipeline steps completed!")
    print(f"📈 Success Rate: {success_count}/{total_steps} steps completed")
    
    # Final results summary
    print("\n" + "="*60)
    print("📊 PIPELINE EXECUTION SUMMARY")
    print("="*60)
    
    steps = [
        ("Resort Data Generation", not args.skip_data),
        ("Guest Analytics", not args.skip_analytics), 
        ("Revenue Optimization", not args.skip_revenue),
        ("Dashboard Launch", True)
    ]
    
    for step_name, was_run in steps:
        status = "✅ COMPLETED" if was_run else "⏭️  SKIPPED"
        print(f"{step_name:<25} {status}")
    
    print("\n🚀 Launching Disney Resort Operations Dashboard...")
    print("📱 The dashboard will open in your default web browser")
    print("🔗 Default URL: http://localhost:8501")
    print("\n💡 Use Ctrl+C to stop the dashboard when finished")
    
    # Launch the dashboard
    time.sleep(3)
    run_command("streamlit run src/resort_dashboard.py", 
               "Launching Disney Resort Operations Dashboard")

if __name__ == "__main__":
    main()