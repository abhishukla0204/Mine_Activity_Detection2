# 🛰️ Mining Activity Monitoring Tool

## Complete Web-Based Solution for Illegal Mining Detection

An advanced, full-stack application for automated detection and monitoring of open-cast mining activities using satellite imagery, machine learning, and geospatial analysis. Features a modern React frontend with dark theme and a powerful Python backend.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![React](https://img.shields.io/badge/react-18.2-61dafb)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 🌟 Features

### Backend Capabilities
- ✅ **Automated Mining Detection** - Extract mining areas from satellite imagery using COCO annotations
- ✅ **Boundary Compliance Analysis** - Identify illegal mining outside authorized zones
- ✅ **Accurate Volume Calculation** - Simpson's Rule integration for excavation volume
- ✅ **Multi-Source Data Support** - Sentinel-2 (10m), SRTM DEM (30m), SAR imagery
- ✅ **2D Interactive Maps** - Folium-based web maps with classification layers
- ✅ **3D Terrain Visualization** - PyVista 3D rendering of mining sites
- ✅ **Comprehensive Reports** - HTML reports with statistics and recommendations
- ✅ **RESTful API** - Flask backend for frontend integration

### Frontend Features
- 🎨 **Modern Dark Theme** - Professional glassmorphism design
- 📊 **Interactive Dashboard** - Real-time statistics and charts
- 🗺️ **Leaflet Map View** - Interactive geospatial visualization
- 📤 **Drag-and-Drop Upload** - Easy file management
- 📈 **Real-Time Analysis** - Live progress tracking
- 📑 **Report Viewer** - Browse and download reports
- 🎭 **Smooth Animations** - Framer Motion effects
- 📱 **Responsive Design** - Works on desktop and tablet

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    React Frontend                       │
│  (Vite + Tailwind CSS + Dark Theme)                     │
│  - Dashboard │ Map View │ Analysis │ Reports │ Upload  │
└─────────────────────┬───────────────────────────────────┘
                      │ REST API (JSON)
┌─────────────────────▼───────────────────────────────────┐
│                  Flask API Backend                      │
│            (CORS-enabled, async workers)                │
│  /upload │ /analyze │ /status │ /results │ /download   │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│              Python Analysis Modules                    │
│  ┌──────────────┬──────────────┬──────────────┐        │
│  │ Data Loader  │ Detector     │ Analyzer     │        │
│  │ (Rasterio)   │ (OpenCV)     │ (GeoPandas)  │        │
│  └──────────────┴──────────────┴──────────────┘        │
│  ┌──────────────┬──────────────┬──────────────┐        │
│  │ Calculator   │ 2D Maps      │ 3D Viewer    │        │
│  │ (Simpson's)  │ (Folium)     │ (PyVista)    │        │
│  └──────────────┴──────────────┴──────────────┘        │
│  ┌──────────────────────────────────────────────┐      │
│  │        Report Generator (HTML + PDF)         │      │
│  └──────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm 7 or higher
- GDAL libraries (for rasterio)

### Quick Start (Recommended)

#### Windows (PowerShell)
```powershell
./start.ps1
```

#### Linux/Mac (Bash)
```bash
chmod +x start.sh
./start.sh
```

This will:
1. Install all Python dependencies
2. Install all Node.js dependencies
3. Start Flask API backend (port 5000)
4. Start React frontend (port 5173)

### Manual Installation

#### 1. Backend Setup
```bash
# Clone repository
git clone <repository-url>
cd mining_activity_monitoring_tool

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install Python dependencies
pip install -r requirements.txt
```

#### 2. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Return to root
cd ..
```

---

## 🚀 Usage

### Option 1: Web Application (Recommended)

#### Start Services
```powershell
# Windows
./start.ps1

# Linux/Mac
./start.sh
```

Access the application:
- **Frontend**: http://localhost:5173
- **API**: http://localhost:5000/api

#### Workflow
1. **Upload Data**: Drag and drop satellite imagery, DEM, and annotations
2. **Configure Analysis**: Choose volume calculation method
3. **Run Analysis**: Monitor real-time progress
4. **View Results**: Interactive maps, charts, and statistics
5. **Download Reports**: HTML reports, GeoJSON, and visualizations

### Option 2: Python CLI

```bash
python main.py \
  --satellite data/Singrauli/Singrauli_Sentinel2_RGB.tif \
  --dem data/Singrauli/Singrauli_SRTM_DEM.tif \
  --annotations data/Singrauli/mine_shape/_annotations.coco.json \
  --output_dir results/
```

### Option 3: API Integration

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API reference.

**Quick Example:**
```python
import requests

API_BASE = "http://localhost:5000/api"

# Upload files
files = {
    'satellite': open('satellite.tif', 'rb'),
    'dem': open('dem.tif', 'rb'),
    'annotations': open('annotations.json', 'rb')
}
response = requests.post(f"{API_BASE}/upload", files=files)
job_id = response.json()['job_id']

# Start analysis
requests.post(f"{API_BASE}/analyze/{job_id}")

# Get results
results = requests.get(f"{API_BASE}/results/{job_id}").json()
```

---

## 📂 Project Structure

```
mining_activity_monitoring_tool/
│
├── frontend/                      # React Frontend
│   ├── src/
│   │   ├── components/           # Reusable components
│   │   │   ├── Layout.jsx        # Main layout with sidebar
│   │   │   ├── StatCard.jsx      # Animated stat cards
│   │   │   └── AreaChart.jsx     # Chart.js wrapper
│   │   ├── pages/                # Main pages
│   │   │   ├── Dashboard.jsx     # Main dashboard
│   │   │   ├── MapView.jsx       # Leaflet map
│   │   │   ├── Analysis.jsx      # Real-time analysis
│   │   │   ├── Reports.jsx       # Report viewer
│   │   │   └── Upload.jsx        # File upload
│   │   ├── App.jsx               # Router setup
│   │   └── main.jsx              # Entry point
│   ├── package.json              # Node dependencies
│   ├── tailwind.config.js        # Dark theme config
│   └── vite.config.js            # Vite config
│
├── src/                          # Python Backend
│   ├── utils/
│   │   └── data_loader.py        # Load TIF, DEM, COCO
│   ├── detection/
│   │   ├── mining_detector.py    # Polygon extraction
│   │   └── boundary_analyzer.py  # Legal/illegal classification
│   ├── depth_volume/
│   │   └── calculator.py         # Simpson's Rule volume
│   ├── visualization/
│   │   ├── map_2d.py             # Folium maps
│   │   └── map_3d.py             # PyVista 3D
│   └── report_generation/
│       └── report_generator.py   # HTML reports
│
├── api.py                        # Flask REST API
├── main.py                       # CLI application
├── requirements.txt              # Python dependencies
├── start.ps1                     # Windows startup script
├── start.sh                      # Linux/Mac startup script
├── README.md                     # This file
└── API_DOCUMENTATION.md          # API reference
```

---

## 🛠️ Technology Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.8+ | Core language |
| Rasterio | 1.3+ | Geospatial raster I/O |
| GeoPandas | 0.14+ | Vector operations |
| Shapely | 2.0+ | Polygon geometry |
| OpenCV | 4.8+ | Image processing |
| NumPy/SciPy | Latest | Numerical computing |
| Folium | 0.14+ | 2D web maps |
| Plotly | 5.17+ | Interactive charts |
| PyVista | 0.42+ | 3D visualization |
| Flask | 3.0+ | REST API |
| Flask-CORS | 4.0+ | CORS handling |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.2 | UI framework |
| Vite | 5.0 | Build tool |
| Tailwind CSS | 3.3 | Utility-first styling |
| Framer Motion | 10.16 | Animations |
| React Router | 6.20 | Navigation |
| Chart.js | 4.4 | Charts |
| Leaflet | 1.9 | Interactive maps |
| Axios | 1.6 | HTTP client |
| Lucide React | Latest | Icons |

---

## 📊 Sample Data

The project includes sample data from Singrauli, Madhya Pradesh:
- **Sentinel-2 RGB**: 10m resolution satellite imagery
- **SRTM DEM**: 30m Digital Elevation Model
- **COCO Annotations**: 11 mining sites manually annotated

### Data Format Requirements

#### Satellite Imagery (.tif)
- Format: GeoTIFF with georeferencing
- Bands: RGB or multispectral
- Resolution: 10m recommended
- Projection: Any (will be reprojected)

#### DEM (.tif)
- Format: Single-band GeoTIFF
- Units: Meters
- Resolution: 30m recommended
- Projection: Match satellite imagery

#### Annotations (.json)
- Format: COCO JSON
- Required fields: `images`, `annotations`, `categories`
- Polygon format: `[x1, y1, x2, y2, ...]`

#### Boundary (optional, .shp/.geojson)
- Format: Shapefile or GeoJSON
- Geometry: Polygon/MultiPolygon
- Projection: Any (will be reprojected)

---

## 🧮 Volume Calculation Methods

### Simpson's Rule (Default)
Most accurate for irregular surfaces. Uses 2D Simpson's 1/3 rule with weighted integration:

```python
Weight Matrix = [[1,  4,  1],
                 [4, 16,  4],
                 [1,  4,  1]]

Volume = (Δx × Δy / 36) × Σ(depth × weight)
```

### Trapezoidal Rule
Faster but less accurate. Good for large datasets.

### Monte Carlo Method
Statistical estimation using random sampling.

---

## 📸 Screenshots

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)
*Real-time statistics, charts, and recent analysis*

### Map View
![Map View](docs/screenshots/map.png)
*Interactive Leaflet map with legal/illegal classification*

### Analysis Progress
![Analysis](docs/screenshots/analysis.png)
*Live progress tracking with step-by-step updates*

### Reports
![Reports](docs/screenshots/reports.png)
*Comprehensive HTML reports with visualizations*

---

## 🔧 Configuration

### Frontend Configuration
Edit `frontend/vite.config.js`:
```javascript
export default {
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
}
```

### Backend Configuration
Edit `api.py`:
```python
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
```

### Theme Customization
Edit `frontend/tailwind.config.js`:
```javascript
colors: {
  'dark-bg': '#0a0e1a',      // Main background
  'dark-surface': '#141824',  // Card background
  'primary-500': '#667eea',   // Primary color
  'accent-purple': '#764ba2'  // Accent color
}
```

---

## 🧪 Testing

### Run Python Tests
```bash
pytest tests/ -v
```

### Run Frontend Tests
```bash
cd frontend
npm test
```

### Test API Endpoints
```bash
# Health check
curl http://localhost:5000/api/health

# Get statistics
curl http://localhost:5000/api/stats

# List jobs
curl http://localhost:5000/api/jobs
```

---

## 📈 Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Data Loading | ~2s | 10m Sentinel-2 + 30m DEM |
| Detection | ~3s | 11 mining sites |
| Boundary Analysis | ~1s | Spatial operations |
| Volume Calculation | ~5s | Simpson's Rule |
| Visualization | ~4s | Folium + Plotly |
| Report Generation | ~2s | HTML compilation |
| **Total Pipeline** | **~17s** | Complete analysis |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

## 👥 Authors

- **Abhinav Shukla** - Initial work

---

## 🙏 Acknowledgments

- Sentinel-2 imagery from ESA Copernicus program
- SRTM DEM data from NASA
- Mining annotations created for educational purposes
- Built with amazing open-source libraries

---

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details
- See [QUICKSTART.md](QUICKSTART.md) for quick start guide

---

## 🔮 Future Enhancements

- [ ] Real-time satellite imagery integration
- [ ] Machine learning-based detection (YOLO, Mask R-CNN)
- [ ] WebSocket for live updates
- [ ] User authentication and authorization
- [ ] Multi-user support with database
- [ ] Email/SMS alerts for violations
- [ ] PDF report generation
- [ ] Export to ArcGIS/QGIS formats
- [ ] Mobile app (React Native)
- [ ] Drone imagery support

---

**Built with ❤️ for environmental monitoring and compliance**
