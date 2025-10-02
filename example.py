"""
Example script demonstrating how to use the Mining Monitoring Tool
"""

from pathlib import Path
import sys

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from main import MiningMonitoringTool


def run_simple_example():
    """Run a simple analysis example"""
    
    # Initialize the tool
    print("Initializing Mining Monitoring Tool...")
    tool = MiningMonitoringTool()
    
    # Specify data directory
    data_dir = "data/Singrauli"
    
    # Run complete analysis
    print("\nRunning complete analysis...")
    tool.run_full_analysis(data_dir)
    
    print("\n✓ Example completed successfully!")
    print("\nCheck the outputs/ directory for:")
    print("  - HTML report with comprehensive analysis")
    print("  - Interactive 2D maps")
    print("  - 3D terrain visualizations")
    print("  - Charts and statistics")


def run_step_by_step_example():
    """Run analysis step by step for more control"""
    
    tool = MiningMonitoringTool()
    data_dir = "data/Singrauli"
    
    # Step 1: Setup
    print("\n1. Setting up tool...")
    tool.setup(data_dir)
    
    # Step 2: Load data
    print("\n2. Loading data...")
    tool.load_data(data_dir)
    
    # Step 3: Detect mining areas
    print("\n3. Detecting mining areas...")
    tool.detect_mining_areas()
    print(f"   Found {len(tool.detected_polygons)} mining sites")
    
    # Step 4: Analyze boundaries
    print("\n4. Analyzing boundaries...")
    tool.analyze_boundaries()
    print(f"   Legal sites: {tool.statistics['num_legal_sites']}")
    print(f"   Illegal sites: {tool.statistics['num_illegal_sites']}")
    
    # Step 5: Calculate depth and volume
    print("\n5. Calculating depth and volume...")
    tool.calculate_depth_volume()
    
    total_volume = sum(r['volume_cubic_meters'] for r in tool.depth_results)
    print(f"   Total excavation: {total_volume:,.0f} cubic meters")
    
    # Step 6: Generate visualizations
    print("\n6. Generating visualizations...")
    tool.generate_visualizations()
    
    # Step 7: Generate report
    print("\n7. Generating report...")
    report_path = tool.generate_report()
    print(f"   Report saved to: {report_path}")
    
    print("\n✓ Step-by-step analysis completed!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--step-by-step":
        run_step_by_step_example()
    else:
        run_simple_example()
