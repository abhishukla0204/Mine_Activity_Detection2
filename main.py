"""
Main application for Mining Activity Monitoring Tool
Integrates all modules and provides CLI interface
"""

import os
import sys
from pathlib import Path
import argparse
from typing import Dict, List
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.utils import DataLoader, Config
from src.detection import MiningDetector, BoundaryAnalyzer
from src.depth_volume import DepthVolumeCalculator
from src.visualization import Map2DVisualizer, Map3DVisualizer
from src.report_generation import ReportGenerator


class MiningMonitoringTool:
    """Main application class for mining activity monitoring"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize the monitoring tool
        
        Args:
            config_path: Path to configuration file
        """
        self.config = Config(config_path)
        self.data_loader = None
        self.detector = None
        self.boundary_analyzer = None
        self.depth_calculator = None
        self.visualizer_2d = None
        self.visualizer_3d = None
        self.report_generator = None
        
        # Data storage
        self.satellite_image = None
        self.dem = None
        self.satellite_metadata = None
        self.dem_metadata = None
        self.coco_data = None
        self.detected_polygons = None
        self.classification_result = None
        self.statistics = None
        self.depth_results = None
        self.violations = None
    
    def setup(self, data_dir: str):
        """
        Setup the tool with data directory
        
        Args:
            data_dir: Path to data directory
        """
        print("=" * 60)
        print("Mining Activity Monitoring Tool - Setup")
        print("=" * 60)
        
        # Initialize data loader
        self.data_loader = DataLoader(data_dir)
        
        # Initialize other components
        self.detector = MiningDetector(self.config.config.get('detection', {}))
        self.boundary_analyzer = BoundaryAnalyzer()
        self.visualizer_2d = Map2DVisualizer()
        self.visualizer_3d = Map3DVisualizer(
            vertical_exaggeration=self.config.get('visualization.3d_view.vertical_exaggeration', 3.0)
        )
        self.report_generator = ReportGenerator(
            output_dir=self.config.get('report.output_dir', 'outputs/reports')
        )
        
        print("✓ Tool components initialized")
    
    def load_data(self, data_dir: str):
        """
        Load all required data
        
        Args:
            data_dir: Path to data directory
        """
        print("\n" + "=" * 60)
        print("Loading Data")
        print("=" * 60)
        
        data_path = Path(data_dir)
        
        # Load satellite image
        satellite_path = data_path / self.config.get('data.satellite_image')
        print(f"Loading satellite image: {satellite_path}")
        self.satellite_image, self.satellite_metadata = self.data_loader.load_satellite_image(
            str(satellite_path)
        )
        print(f"✓ Satellite image loaded: {self.satellite_image.shape}")
        
        # Load DEM
        dem_path = data_path / self.config.get('data.dem_file')
        print(f"Loading DEM: {dem_path}")
        self.dem, self.dem_metadata = self.data_loader.load_dem(str(dem_path))
        print(f"✓ DEM loaded: {self.dem.shape}")
        
        # Load COCO annotations
        annotations_path = data_path / self.config.get('data.annotations_file')
        print(f"Loading annotations: {annotations_path}")
        self.coco_data = self.data_loader.load_coco_annotations(str(annotations_path))
        print(f"✓ Annotations loaded: {len(self.coco_data['annotations'])} annotations")
        
        print(f"\n✓ All data loaded successfully")
    
    def detect_mining_areas(self):
        """Detect mining areas from annotations or image"""
        print("\n" + "=" * 60)
        print("Detecting Mining Areas")
        print("=" * 60)
        
        if self.config.get('detection.use_coco_annotations', True):
            print("Using COCO annotations for mining detection")
            image_shape = (self.satellite_image.shape[0], self.satellite_image.shape[1])
            self.detected_polygons = self.detector.detect_from_annotations(
                self.coco_data, image_shape
            )
        else:
            print("Using image-based detection")
            self.detected_polygons = self.detector.detect_from_image(
                self.satellite_image, method='threshold'
            )
        
        print(f"✓ Detected {len(self.detected_polygons)} mining areas")
        
        # Calculate metrics
        metrics = self.detector.calculate_polygon_metrics(
            self.detected_polygons,
            pixel_size=10.0  # Sentinel-2 resolution
        )
        
        total_area_ha = sum(m['area_hectares'] for m in metrics)
        print(f"  Total mining area: {total_area_ha:.2f} hectares")
    
    def analyze_boundaries(self, boundary_path: str = None):
        """
        Analyze mining areas against authorized boundary
        
        Args:
            boundary_path: Optional path to boundary shapefile/KML
        """
        print("\n" + "=" * 60)
        print("Analyzing Boundaries")
        print("=" * 60)
        
        if boundary_path:
            print(f"Loading authorized boundary from: {boundary_path}")
            self.boundary_analyzer.load_authorized_boundary(boundary_path)
        else:
            # Create a test boundary (for demonstration)
            print("No boundary file provided - creating rectangular test boundary")
            # Get bounds from image
            h, w = self.satellite_image.shape[:2]
            # Create boundary that covers 80% of image (so some mines will be outside)
            margin = int(min(h, w) * 0.1)
            test_bounds = (margin, margin, w - margin, h - margin)
            test_boundary = self.boundary_analyzer.create_rectangular_boundary(test_bounds)
            self.boundary_analyzer.authorized_boundary = test_boundary
            print(f"✓ Test boundary created: {test_bounds}")
        
        # Classify mining areas
        print("Classifying mining areas...")
        self.classification_result = self.boundary_analyzer.classify_mining_areas(
            self.detected_polygons
        )
        
        print(f"✓ Classification complete:")
        print(f"  Legal sites: {len(self.classification_result['legal'])}")
        print(f"  Illegal sites: {len(self.classification_result['illegal'])}")
        print(f"  Partial violations: {len(self.classification_result['partial'])}")
        
        # Calculate statistics
        self.statistics = self.boundary_analyzer.calculate_area_statistics(
            self.classification_result,
            pixel_size=10.0
        )
        
        print(f"\n  Legal mining area: {self.statistics['legal_mining_area_hectares']:.2f} ha")
        print(f"  Illegal mining area: {self.statistics['illegal_mining_area_hectares']:.2f} ha")
        print(f"  Illegal mining %: {self.statistics['illegal_mining_percentage']:.1f}%")
        
        # Generate violation report
        self.violations = self.boundary_analyzer.generate_violation_report(
            self.classification_result, self.statistics
        )
        
        if self.violations:
            print(f"\n⚠️  {len(self.violations)} VIOLATIONS DETECTED!")
        else:
            print(f"\n✓ No violations - all mining within authorized boundary")
    
    def calculate_depth_volume(self):
        """Calculate mining depth and excavation volume"""
        print("\n" + "=" * 60)
        print("Calculating Depth and Volume")
        print("=" * 60)
        
        # Initialize calculator
        self.depth_calculator = DepthVolumeCalculator(
            self.dem,
            self.dem_metadata,
            pixel_size=30.0  # SRTM resolution
        )
        
        # Process all detected polygons
        print("Processing mining polygons...")
        self.depth_results = self.depth_calculator.process_multiple_polygons(
            self.detected_polygons,
            reference_method=self.config.get('depth_volume.reference_elevation', 'mean'),
            volume_method=self.config.get('depth_volume.volume_method', 'simpsons')
        )
        
        # Aggregate results
        aggregate = self.depth_calculator.aggregate_results(self.depth_results)
        
        print(f"\n✓ Depth and volume calculation complete:")
        print(f"  Total excavation volume: {aggregate['total_excavation_volume_cubic_meters']:,.0f} m³")
        print(f"  Average depth: {aggregate['average_depth_across_all_mines']:.1f} m")
        print(f"  Maximum depth: {aggregate['maximum_depth_across_all_mines']:.1f} m")
    
    def generate_visualizations(self, output_dir: str = "outputs/visualizations"):
        """
        Generate all visualizations
        
        Args:
            output_dir: Output directory for visualizations
        """
        print("\n" + "=" * 60)
        print("Generating Visualizations")
        print("=" * 60)
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 2D Classification Map
        print("Creating 2D classification map...")
        map_2d = self.visualizer_2d.create_classification_map(
            self.classification_result,
            self.statistics,
            output_path=str(output_path / "classification_map.html")
        )
        print(f"✓ Saved: {output_path / 'classification_map.html'}")
        
        # Depth heatmap
        print("Creating depth heatmap...")
        depth_fig = self.visualizer_2d.create_depth_heatmap(
            self.depth_results,
            output_path=str(output_path / "depth_heatmap.html")
        )
        print(f"✓ Saved: {output_path / 'depth_heatmap.html'}")
        
        # Volume chart
        print("Creating volume chart...")
        volume_fig = self.visualizer_2d.create_volume_chart(
            self.depth_results,
            output_path=str(output_path / "volume_chart.html")
        )
        print(f"✓ Saved: {output_path / 'volume_chart.html'}")
        
        # Dashboard
        print("Creating overview dashboard...")
        dashboard = self.visualizer_2d.create_overview_dashboard(
            self.classification_result,
            self.statistics,
            self.depth_results,
            output_path=str(output_path / "dashboard.html")
        )
        print(f"✓ Saved: {output_path / 'dashboard.html'}")
        
        # 3D visualization
        print("Creating 3D terrain visualization...")
        try:
            fig_3d = self.visualizer_3d.create_plotly_3d_surface(
                self.dem,
                self.detected_polygons,
                output_path=str(output_path / "terrain_3d.html")
            )
            print(f"✓ Saved: {output_path / 'terrain_3d.html'}")
        except Exception as e:
            print(f"⚠️  3D visualization failed: {e}")
        
        print(f"\n✓ All visualizations generated in: {output_path}")
    
    def generate_report(self):
        """Generate comprehensive report"""
        print("\n" + "=" * 60)
        print("Generating Report")
        print("=" * 60)
        
        # Compile report data
        self.report_generator.compile_report_data(
            self.classification_result,
            self.statistics,
            self.depth_results,
            self.violations
        )
        
        # Generate HTML report
        html_path = self.report_generator.generate_html_report()
        print(f"✓ HTML report: {html_path}")
        
        # Export JSON data
        json_path = self.report_generator.export_json_data()
        print(f"✓ JSON data: {json_path}")
        
        return html_path
    
    def run_full_analysis(self, data_dir: str, boundary_path: str = None):
        """
        Run complete analysis pipeline
        
        Args:
            data_dir: Path to data directory
            boundary_path: Optional path to boundary file
        """
        try:
            # Setup
            self.setup(data_dir)
            
            # Load data
            self.load_data(data_dir)
            
            # Detect mining areas
            self.detect_mining_areas()
            
            # Analyze boundaries
            self.analyze_boundaries(boundary_path)
            
            # Calculate depth and volume
            self.calculate_depth_volume()
            
            # Generate visualizations
            self.generate_visualizations()
            
            # Generate report
            report_path = self.generate_report()
            
            print("\n" + "=" * 60)
            print("Analysis Complete!")
            print("=" * 60)
            print(f"\n📊 Main Report: {report_path}")
            print(f"📁 Visualizations: outputs/visualizations/")
            print(f"📈 Dashboard: outputs/visualizations/dashboard.html")
            print("\n✓ Mining Activity Monitoring Complete!")
            
        except Exception as e:
            print(f"\n❌ Error during analysis: {e}")
            import traceback
            traceback.print_exc()
            raise


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Mining Activity Monitoring Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full analysis on Singrauli data
  python main.py --data-dir data/Singrauli
  
  # Run with custom boundary file
  python main.py --data-dir data/Singrauli --boundary boundary.shp
  
  # Run with custom config
  python main.py --data-dir data/Singrauli --config config.yaml
        """
    )
    
    parser.add_argument(
        '--data-dir',
        type=str,
        default='data/Singrauli',
        help='Path to data directory'
    )
    
    parser.add_argument(
        '--boundary',
        type=str,
        default=None,
        help='Path to authorized boundary shapefile/KML'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='outputs',
        help='Output directory for results'
    )
    
    args = parser.parse_args()
    
    # Print header
    print("\n" + "=" * 60)
    print("MINING ACTIVITY MONITORING TOOL")
    print("Automated Detection and Analysis of Open Cast Mining")
    print("=" * 60 + "\n")
    
    # Initialize tool
    tool = MiningMonitoringTool(config_path=args.config)
    
    # Run analysis
    tool.run_full_analysis(
        data_dir=args.data_dir,
        boundary_path=args.boundary
    )


if __name__ == "__main__":
    main()
