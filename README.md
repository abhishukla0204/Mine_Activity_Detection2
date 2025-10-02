# Mining Activity Monitoring Tool 🏔️

A comprehensive software solution for automated detection and analysis of open cast mining activities using satellite imagery and Digital Elevation Models (DEM).

## 📋 Features

- **Automated Mining Detection**: Detect mining areas from satellite imagery (EO/SAR/Multispectral)
- **Boundary Compliance**: Compare detected areas with authorized mining boundaries
- **Illegal Mining Detection**: Automatically identify mining activities outside authorized zones
- **Depth & Volume Calculation**: Calculate mining depth and excavation volume using DEM data
- **Simpson's Rule Integration**: Accurate volume estimation using advanced numerical methods
- **2D Interactive Maps**: Visualize mining areas with interactive Folium maps
- **3D Terrain Visualization**: View mining activities in 3D using PyVista and Plotly
- **Automated Reporting**: Generate comprehensive HTML reports with statistics and visualizations
- **Multi-format Support**: Works with TIF, Shapefile, KML, GeoJSON formats

## 🎯 Project Background

Detection of open crust mining activity is crucial for:
- **Environmental Monitoring**: Track impact of mining operations
- **Legal Compliance**: Ensure mining stays within authorized boundaries
- **Resource Management**: Calculate excavation volumes for planning
- **Regulatory Oversight**: Provide data for government reporting

This tool uses freely available satellite data (Sentinel-2, SRTM DEM) to provide automated monitoring capabilities.

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download the repository**
   ```bash
   cd mining_activity_monitoring_tool
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📁 Data Structure

Organize your data as follows:

```
data/
├── Singrauli/
│   ├── Singrauli_Sentinel2_RGB.tif    # Satellite imagery (10m resolution)
│   ├── Singrauli_SRTM_DEM.tif         # Digital Elevation Model (30m)
│   ├── Singrauli_mines_image.jpeg     # Reference image
│   └── mine_shape/
│       └── _annotations.coco.json      # Mining area annotations
```

### Data Sources

- **Satellite Imagery**: Sentinel-2 (10m resolution) from Google Earth Engine
- **DEM**: SRTM (30m resolution) from Google Earth Engine
- **Annotations**: COCO format from Roboflow or manual annotations
- **Boundaries**: Optional Shapefile/KML for authorized mining areas

## 💻 Usage

### Quick Start

Run the complete analysis pipeline:

```bash
python main.py --data-dir data/Singrauli
```

### With Boundary File

If you have an authorized mining boundary:

```bash
python main.py --data-dir data/Singrauli --boundary path/to/boundary.shp
```

### Using Example Script

```bash
# Simple run
python example.py

# Step-by-step with detailed output
python example.py --step-by-step
```

## 📊 Output

The tool generates the following outputs:

### Reports (outputs/reports/)
- **HTML Report**: Comprehensive report with statistics, charts, and recommendations
- **JSON Data**: Machine-readable data export

### Visualizations (outputs/visualizations/)
- **classification_map.html**: Interactive 2D map showing legal/illegal mining
- **dashboard.html**: Overview dashboard with multiple charts
- **depth_heatmap.html**: Mining depth analysis
- **volume_chart.html**: Excavation volume comparison
- **terrain_3d.html**: 3D terrain visualization

## 🔧 Configuration

Create a `config.yaml` file to customize settings:

```yaml
data:
  singrauli_dir: data/Singrauli
  satellite_image: Singrauli_Sentinel2_RGB.tif
  dem_file: Singrauli_SRTM_DEM.tif
  
detection:
  min_area: 100  # Minimum mining area in pixels
  use_coco_annotations: true
  
depth_volume:
  reference_elevation: mean  # 'mean', 'median', or numeric value
  volume_method: simpsons    # 'simpsons', 'trapezoidal', 'montecarlo'
  
visualization:
  3d_view:
    vertical_exaggeration: 3.0
    
report:
  output_dir: outputs/reports
  format: html
```

Run with custom config:
```bash
python main.py --data-dir data/Singrauli --config config.yaml
```

## 📖 Modules

### 1. Data Loading (`src/utils/data_loader.py`)
- Load satellite imagery (TIF format)
- Load DEM data
- Parse COCO annotations
- Coordinate transformations

### 2. Mining Detection (`src/detection/mining_detector.py`)
- Extract mining polygons from annotations
- Image-based detection (threshold, clustering)
- Calculate polygon metrics
- Export to GeoJSON

### 3. Boundary Analysis (`src/detection/boundary_analyzer.py`)
- Load authorized boundaries
- Classify legal vs illegal mining
- Calculate area statistics
- Generate violation reports

### 4. Depth & Volume (`src/depth_volume/calculator.py`)
- Estimate reference elevation
- Calculate depth maps
- Volume estimation (Simpson's rule)
- Aggregate results

### 5. 2D Visualization (`src/visualization/map_2d.py`)
- Interactive Folium maps
- Plotly charts and dashboards
- Depth heatmaps
- Volume charts

### 6. 3D Visualization (`src/visualization/map_3d.py`)
- 3D terrain surfaces
- Depth profiles
- PyVista visualizations
- Volumetric excavation views

### 7. Report Generation (`src/report_generation/report_generator.py`)
- HTML report generation
- Statistics compilation
- Violation alerts
- Recommendations

## 🎓 Technical Details

### Mining Detection
- Uses COCO format annotations from Roboflow
- Supports multiple detection methods (supervised/unsupervised)
- Minimum area filtering to remove noise

### Volume Calculation
The tool uses **Simpson's 1/3 Rule** for accurate volume estimation:

```
Volume = (h×k/9) × Σ(depth × weight)
```

where weights follow the Simpson's 2D pattern:
```
1   4   1
4  16   4
1   4   1
```

### Depth Estimation
1. Reference elevation from surrounding non-mining areas
2. Depth = Reference Elevation - Current Elevation
3. Only positive depths (excavations) are considered

## 📈 Example Results

For the Singrauli dataset:
- **Total Mining Sites**: 11
- **Total Area**: ~150 hectares
- **Excavation Volume**: ~2-5 million cubic meters
- **Average Depth**: 10-30 meters
- **Maximum Depth**: 50+ meters

## 🛠️ Development

### Project Structure
```
mining_activity_monitoring_tool/
├── main.py                    # Main application
├── example.py                 # Example usage script
├── requirements.txt           # Dependencies
├── README.md                  # This file
├── src/
│   ├── utils/                # Data loading utilities
│   ├── detection/            # Mining detection modules
│   ├── depth_volume/         # Depth and volume calculation
│   ├── visualization/        # 2D and 3D visualization
│   └── report_generation/    # Report generation
├── data/                     # Input data
└── outputs/                  # Generated outputs
    ├── reports/
    └── visualizations/
```

### Adding Custom Detection Methods

Extend `MiningDetector` class:

```python
from src.detection import MiningDetector

class CustomDetector(MiningDetector):
    def custom_detection_method(self, image):
        # Your detection logic
        polygons = []
        # ... process image ...
        return polygons
```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional detection algorithms (ML/DL models)
- SAR imagery support
- Time-series analysis
- Change detection
- PDF report generation
- GUI interface

## 📝 Citation

If you use this tool in your research, please cite:

```
Mining Activity Monitoring Tool
Automated Detection and Analysis of Open Cast Mining
Using Satellite Imagery and DEM Data
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

2. **Memory Issues with Large Images**
   - Process smaller tiles
   - Reduce image resolution
   - Use more efficient data types

3. **Coordinate System Mismatches**
   - Ensure all data uses the same CRS
   - Use appropriate transformations

4. **PyVista Display Issues**
   ```bash
   pip install pyvistaqt
   ```

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review example scripts

## 📜 License

This project is for educational and research purposes.

## 🙏 Acknowledgments

- **Google Earth Engine** for satellite data
- **Roboflow** for annotation tools
- **Open-source geospatial community** for libraries

---

**Built with ❤️ for sustainable mining monitoring**

Last Updated: October 2025
