# Quick Start Guide

## Installation

1. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Running the Tool

### Option 1: Simple Run
```bash
python main.py --data-dir data/Singrauli
```

### Option 2: With Example Script
```bash
python example.py
```

### Option 3: Step-by-Step
```bash
python example.py --step-by-step
```

## Expected Output

After running, you'll find:

1. **HTML Report**: `outputs/reports/mining_activity_report_*.html`
   - Open in web browser for full analysis

2. **Interactive Maps**: `outputs/visualizations/`
   - `classification_map.html` - Legal vs illegal mining
   - `dashboard.html` - Overview dashboard
   - `depth_heatmap.html` - Depth analysis
   - `volume_chart.html` - Volume comparison
   - `terrain_3d.html` - 3D visualization

## What the Tool Does

1. ✅ Loads satellite imagery (Sentinel-2, 10m)
2. ✅ Loads DEM data (SRTM, 30m)
3. ✅ Detects mining areas from annotations
4. ✅ Compares with authorized boundaries
5. ✅ Identifies legal vs illegal mining
6. ✅ Calculates mining depth and volume (Simpson's rule)
7. ✅ Generates 2D and 3D visualizations
8. ✅ Creates comprehensive HTML report

## Key Features

- **Automated Detection**: Uses COCO annotations from Roboflow
- **Boundary Analysis**: Identifies violations outside authorized zones
- **Volume Estimation**: Simpson's rule for accurate calculations
- **Interactive Viz**: Folium maps and Plotly charts
- **3D Terrain**: PyVista and Plotly 3D visualizations
- **Professional Reports**: HTML reports with statistics

## Troubleshooting

### Import Errors
```bash
pip install -r requirements.txt --upgrade
```

### No Output
- Check data directory exists: `data/Singrauli/`
- Verify TIF files are present
- Check console for error messages

### Visualization Issues
- For PyVista: `pip install pyvistaqt`
- Open HTML files in modern web browser

## Next Steps

1. Review the generated HTML report
2. Open interactive maps in browser
3. Customize `config.yaml` for your needs
4. Add your own boundary shapefiles
5. Process additional satellite imagery

## Need Help?

- Check `README.md` for detailed documentation
- Review `example.py` for code examples
- Examine output files for structure

---
Happy Mining Monitoring! 🏔️
