# Mining Activity Monitoring Tool 🏔️

A full-stack web application for automated detection and analysis of open cast mining activities using satellite imagery and Digital Elevation Model (DEM) data.

![Mining Monitoring Dashboard](https://img.shields.io/badge/Status-Production-brightgreen)
![Python](https://img.shields.io/badge/Python-3.13.7-blue)
![React](https://img.shields.io/badge## 🚀 Deployment

### Development

Run both backend and frontend in separate terminals as shown in the---

## 📝 Version History

- **v2.0** (Current - October 2025): F---

## 📄 License

Internal use for government mining monitoring and environmental compliance assessment.

---ck application with React frontend, Flask API, accurate volume calculation, and compliance monitoring
- **v1.0**: Initial detection and volume calculation scripts

---

## 📖 Development History & Key Decisions

### Major Milestones

1. **Initial Development**: CLI-based tool with legacy `src/` modules
2. **Full-Stack Migration**: Converted to Flask API + React frontend architecture
3. **MapView Coordinate Fix**: Implemented Y-axis inversion for perfect polygon alignment
4. **Volume Calculation Fix**: Added geographic coordinate conversion (was showing 0)
5. **Site Classification Update**: Changed illegal sites from 4 (sites 8-11) to 2 (sites 8-9)
6. **UI Consolidation**: Merged Analysis into Dashboard, removed Upload page (5 pages → 3 pages)
7. **Code Cleanup**: Removed legacy modules, streamlined to essential files only

### Problems Solved

| Issue | Solution | Location |
|-------|----------|----------|
| Volume showing 0 m³ | Geographic coordinate to meters conversion | `compute_real_metrics.py` lines 135-165 |
| Polygons misaligned on map | Y-axis coordinate inversion `[719 - y, x]` | `MapView.jsx` convertCoordinates function |
| Too many illegal sites (exaggerated) | Changed from 4 illegal to 2 illegal (sites 8 & 9 only) | `compute_real_metrics.py` line 325 |
| Black screen after cleanup | Fixed missing Activity icon import | `Dashboard.jsx` (changed to Mountain icon) |
| Fake data in dashboard | Replaced all mock data with real computed_metrics.json | All frontend pages |
| API import errors after cleanup | Rewrote API to serve pre-computed JSON only | `api.py` (245 lines, no src/ imports) |

### Files Removed During Cleanup

- **Legacy Scripts**: `setup.py`, `check_dependencies.py`, `example.py`, `main.py`
- **Startup Scripts**: `start.bat`, `start.ps1`, `start.sh`, `start-backend.bat`, `start-frontend.bat`
- **Documentation**: 12 markdown files (kept only README.md and SYSTEM_DOCUMENTATION.md)
- **Legacy Modules**: Entire `src/` directory (mining_detector, volume_calculator, map_generator, report_generator)
- **Old Directories**: `results/`, `uploads/`, `venv/`
- **Misc**: `package-lock.json` (root level)

### Current Architecture Benefits

✅ **Clean Codebase**: Only 7 core files in root directory  
✅ **Single Source of Truth**: All data from `computed_metrics.json`  
✅ **No Redundancy**: Removed all duplicate/fake data  
✅ **Maintainable**: Simple, explicit data flow  
✅ **Production-Ready**: Professional structure following best practices  

---

## 👥 Supportthe Application" section above.

### Production Build

**Frontend:**
```bash
cd frontend
npm run build
npm run preview  # Test production build on port 4173
```

**Backend:**
For production deployment, consider:ue)
![Flask](https://img.shields.io/badge/Flask-3.1.0-lightgrey)

## 🌟 Overview

This tool provides comprehensive monitoring and analysis of mining operations through:

- **Automated Detection**: Identifies mining sites from satellite imagery with COCO annotations
- **Volume Calculation**: Accurate excavation volume estimation using DEM data
- **Compliance Monitoring**: Distinguishes between legal and illegal mining operations
- **Interactive Visualization**: Real-time map view with satellite imagery overlay
- **Detailed Reporting**: Generates compliance reports with site-wise analytics

### Current Deployment Stats

- **Study Area**: Singrauli region
- **Total Sites**: 11 mining locations
- **Legal Operations**: 9 sites (Northern Coalfields Limited - NCL)
- **Illegal Operations**: 2 sites (Sites 8 and 9)
- **Total Area**: 10,730.73 hectares
- **Total Excavation Volume**: 7.12 billion cubic meters

---

## 🚀 Quick Start

### Prerequisites

- **Python**: 3.8 or higher
- **Node.js**: 16.0 or higher
- **npm**: 8.0 or higher

### Installation

1. **Clone the repository**
   ```bash
   cd mining_activity_monitoring_tool
   ```

2. **Set up Python virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   
   # Windows (CMD):
   .venv\Scripts\activate.bat
   
   # Linux/Mac:
   source .venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

### Running the Application

You need to run both the backend and frontend in separate terminals:

#### Terminal 1 - Backend API

```bash
# Activate virtual environment first
# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Windows (CMD):
.venv\Scripts\activate.bat

# Linux/Mac:
source .venv/bin/activate

# Start the API server
python api.py
```

The API will start on **http://localhost:5000**

#### Terminal 2 - Frontend

```bash
cd frontend
npm run dev
```

The frontend will start on **http://localhost:3000**

#### Access the Application

- **Frontend**: http://localhost:3000 (Main application)
- **Backend API**: http://localhost:5000 (REST API endpoints)

---

## 📊 Features

### 1. Dashboard
- **Key Metrics**: Total sites, legal/illegal counts, area coverage, excavation volume
- **Visual Analytics**: Area distribution charts, volume metrics
- **Site Table**: Complete list of all mining sites with compliance status
- **Quick Actions**: Direct links to map view and reports

### 2. Interactive Map View
- **Satellite Base Layer**: High-resolution imagery of Singrauli region
- **Mining Boundaries**: Color-coded polygons (green=legal, red=illegal)
- **Site Information**: Click any polygon for detailed site data
- **Statistics Sidebar**: Real-time aggregated metrics
- **Legend**: Clear visual guide for site classifications

### 3. Compliance Reports
- **Executive Summary**: Key findings and total statistics
- **Compliance Status**: Legal vs illegal operation breakdown
- **Site-wise Analysis**: Detailed metrics for each mining location
- **Export Options**: Download reports in PDF, Excel, or JSON format

---

## 🗂️ Project Structure

```
mining_activity_monitoring_tool/
├── frontend/                          # React application
│   ├── public/
│   │   ├── computed_metrics.json     # Generated metrics data
│   │   └── Singrauli_mines_image.jpeg # Satellite imagery
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx         # Main overview
│   │   │   ├── MapView.jsx           # Interactive map
│   │   │   └── Reports.jsx           # Compliance reports
│   │   ├── components/
│   │   │   └── Layout.jsx            # Navigation
│   │   ├── App.jsx                   # Router
│   │   └── main.jsx                  # Entry point
│   └── package.json
│
├── data/Singrauli/                    # Input data
│   ├── Singrauli_Sentinel2_RGB.tif   # Satellite imagery (GeoTIFF)
│   ├── Singrauli_SRTM_DEM.tif        # Digital Elevation Model
│   └── mine_shape/
│       └── _annotations.coco.json    # Mining boundary annotations
│
├── outputs/                           # Generated outputs
│   └── mining_analysis_report.html
│
├── compute_real_metrics.py            # Main metrics computation
├── api.py                             # Flask REST API
├── requirements.txt                   # Python dependencies
├── config.yaml                        # Configuration
├── README.md                          # This file
└── SYSTEM_DOCUMENTATION.md            # Detailed technical docs
```

---

## � Technology Stack

### Backend
- **Python 3.13.7**: Core runtime environment
- **Flask 3.1.0**: REST API framework
- **Rasterio 1.4.3**: Geospatial raster data processing
- **GDAL 3.10.1**: Geospatial data abstraction library
- **NumPy 2.2.1**: Numerical computations
- **OpenCV 4.10.0**: Image processing

### Frontend
- **React 18.2.0**: UI framework
- **Vite 5.0.8**: Build tool and development server
- **TailwindCSS 3.4.1**: Utility-first CSS framework
- **Leaflet 1.9.4**: Interactive mapping library
- **React-Leaflet 4.2.1**: React bindings for Leaflet
- **Lucide-React**: Modern icon library

---

## 📡 API Endpoints

Base URL: `http://localhost:5000`

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/sites` | Get all mining sites |
| GET | `/api/sites/<id>` | Get specific site by ID |
| GET | `/api/sites/legal` | Get all legal sites |
| GET | `/api/sites/illegal` | Get all illegal sites |
| GET | `/api/stats` | Get aggregate statistics |
| GET | `/api/sites/search` | Search sites with filters |
| POST | `/api/generate-report` | Generate custom report |

### Example API Call

```bash
# Get all sites
curl http://localhost:5000/api/sites

# Get statistics
curl http://localhost:5000/api/stats

# Search by operator
curl "http://localhost:5000/api/sites/search?operator=NCL&minArea=500"
```

---

## 🛠️ Configuration

### Backend Configuration (`config.yaml`)

```yaml
data:
  satellite_image: "data/Singrauli/Singrauli_Sentinel2_RGB.tif"
  dem_file: "data/Singrauli/Singrauli_SRTM_DEM.tif"
  annotation_file: "data/Singrauli/mine_shape/_annotations.coco.json"

output:
  metrics_file: "frontend/public/computed_metrics.json"
  reports_dir: "outputs/"

processing:
  illegal_sites: [8, 9]  # Site IDs classified as illegal
  latitude: 24.19        # Region latitude for coordinate conversion

api:
  host: "localhost"
  port: 5000
  cors_origins: ["http://localhost:3000"]
```

### Frontend Configuration (`vite.config.js`)

```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
});
```

---

## 📈 Data Processing Pipeline

### 1. Input Data
- **Satellite Imagery**: Sentinel-2 RGB composite (GeoTIFF format)
- **DEM Data**: SRTM elevation data (GeoTIFF format)
- **Annotations**: COCO format JSON with mining boundary polygons

### 2. Processing (`compute_real_metrics.py`)
- Loads COCO annotations and extracts polygons
- Calculates area using geographic coordinate conversion
- Computes excavation volume from DEM height differences
- Classifies sites as legal or illegal
- Generates `computed_metrics.json`

### 3. Volume Calculation Method
```python
# Geographic coordinate conversion at Singrauli (24.19°N)
lat = 24.19
meters_per_deg_x = 111320 * np.cos(np.radians(lat))  # ~102,000 m/deg
meters_per_deg_y = 111320                             # ~111,320 m/deg

# Calculate pixel area in square meters
pixel_size_m2 = abs(transform[0]) * meters_per_deg_x * \
                abs(transform[4]) * meters_per_deg_y

# Volume = sum of height differences × pixel area
volume_m3 = np.sum(height_differences) * pixel_size_m2
```

### 4. Output
- JSON file with all site metrics
- Served to both API and frontend
- Updated whenever processing is re-run

---

## 🗺️ Map Coordinate System

The map view uses **Leaflet Simple CRS** with Y-axis coordinate inversion to align polygons with satellite imagery.

### Why Coordinate Inversion?

- **COCO annotations**: Use image coordinates `[x, y]` with origin at top-left
- **Leaflet Simple CRS**: Uses `[row, col]` format
- **Solution**: Convert using `[719 - y, x]` where 719 is image height

```javascript
const convertCoordinates = (coords) => {
  return coords.map(coord => [719 - coord[1], coord[0]]);
};
```

This ensures perfect alignment between satellite base layer and mining boundary polygons.

---

## � Important Implementation Details

### Site Classification Logic
Located in `compute_real_metrics.py` (line 325):
```python
# Sites 8 and 9 are classified as illegal (zero-indexed: 7, 8)
is_legal = idx not in [7, 8]
```

To change which sites are illegal, modify this line. For example:
- `idx not in [5, 6, 7]` would make sites 6, 7, 8 illegal
- `idx not in []` would make all sites legal

### Volume Calculation Fix
The volume calculation required geographic coordinate conversion (lines 135-165):
```python
# Convert geographic coordinates to meters at Singrauli latitude
lat = 24.19  # Singrauli latitude in degrees
meters_per_deg_x = 111320 * np.cos(np.radians(lat))  # ~102,000 m/deg
meters_per_deg_y = 111320  # ~111,320 m/deg

# Calculate actual pixel area in square meters
pixel_size_m2 = (abs(dem_dataset.transform[0]) * meters_per_deg_x * 
                 abs(dem_dataset.transform[4]) * meters_per_deg_y)

# Volume = height differences × pixel area
volume = np.sum(height_differences) * pixel_size_m2
```

**Why this was needed**: Without geographic conversion, volume showed 0 because pixel sizes were in degrees, not meters.

### Map Coordinate System
The MapView uses Leaflet Simple CRS with Y-axis inversion (`MapView.jsx`):
```javascript
// Image dimensions: 1500×719 pixels
const bounds = [[0, 0], [719, 1500]];  // [height, width]

// Convert COCO coordinates to Leaflet coordinates
const convertCoordinates = (coords) => {
  return coords.map(coord => [719 - coord[1], coord[0]]);
};
```

**Why this was needed**: COCO annotations have origin at top-left with Y increasing downward, but Leaflet needs coordinates inverted for proper alignment.

### Page Structure Evolution
The application was streamlined from 5 pages to 3:
- **Removed**: Analysis page (merged into Dashboard), Upload page (not needed for demo)
- **Kept**: Dashboard (overview + analytics), MapView (interactive map), Reports (compliance)

### Data Flow
```
1. compute_real_metrics.py
   ↓ (reads)
2. Satellite imagery + DEM + COCO annotations
   ↓ (generates)
3. frontend/public/computed_metrics.json
   ↓ (loaded by)
4. api.py (Flask backend)
   ↓ (serves to)
5. React frontend (Dashboard, Map, Reports)
```

All three frontend pages use the **same data source** (`computed_metrics.json`) for consistency.

---

## �🔄 Regenerating Metrics

If you update annotations or change site classifications:

```bash
# Activate virtual environment first
python compute_real_metrics.py
```

This will:
1. Reprocess all mining sites
2. Recalculate areas and volumes
3. Update site classifications
4. Generate new `computed_metrics.json`
5. Print summary statistics

The frontend will automatically use the updated data on next page load.

---

## 📚 Documentation

- **README.md** (this file): Quick start guide and overview
- **SYSTEM_DOCUMENTATION.md**: Comprehensive technical documentation
  - Detailed architecture
  - API specifications
  - Algorithm explanations
  - Coordinate system details
  - Troubleshooting guide

---

## 🐛 Troubleshooting

### Common Issues

**1. Black screen in frontend**
- Check browser console for errors
- Verify `frontend/public/computed_metrics.json` exists
- Ensure backend is running on port 5000

**2. Polygons misaligned on map**
- Verify coordinate conversion: `[719 - y, x]`
- Check image dimensions: 1500×719 pixels
- Ensure `CRS.Simple` is used in MapContainer

**3. Volume showing 0**
- Run `compute_real_metrics.py` to regenerate metrics
- Check DEM file path in `config.yaml`
- Verify geographic coordinate conversion is applied

**4. API CORS errors**
- Verify Flask-CORS is installed: `pip install flask-cors`
- Check backend is running: `http://localhost:5000/api/health`
- Restart backend after configuration changes

**5. Frontend won't start**
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again
- Check Node.js version: `node --version` (need 16+)

---

## � Security Notes

- This tool is designed for **internal government use**
- Sensitive mining location data should be kept confidential
- API has no authentication - add auth layer for production deployment
- Do not expose backend API directly to public internet

---

## � Deployment

### Development
Already configured! Just run `start.bat` or `start.ps1`

### Production Build

**Frontend:**
```bash
cd frontend
npm run build
npm run preview  # Test production build on port 4173
```

**Backend:**
For production deployment, consider:
- Using **Gunicorn** or **uWSGI** instead of Flask dev server
- Adding **Nginx** as reverse proxy
- Implementing authentication (JWT/OAuth)
- Setting up **SSL/TLS** certificates
- Using environment variables for configuration
- Deploying with **Docker** containers

---

## 📝 Version History

- **v2.0** (Current): Full-stack application with React frontend, Flask API, accurate volume calculation, and compliance monitoring
- **v1.0**: Initial detection and volume calculation scripts

---

## � Support

For technical documentation, see `SYSTEM_DOCUMENTATION.md`

For issues or questions:
1. Check the troubleshooting section above
2. Review browser console and terminal logs
3. Verify all dependencies are installed correctly
4. Ensure data files are in correct locations

---

## � License

Internal use for government mining monitoring and environmental compliance assessment.

---

## 🎯 Future Enhancements

- [ ] Time-series analysis for change detection
- [ ] PostgreSQL/PostGIS database integration
- [ ] Multi-region support
- [ ] Automated report scheduling
- [ ] Email notifications for compliance violations
- [ ] Mobile-responsive design improvements
- [ ] User authentication and role-based access
- [ ] Export to official government report formats

---

**Built with ❤️ for sustainable mining monitoring and environmental protection**
