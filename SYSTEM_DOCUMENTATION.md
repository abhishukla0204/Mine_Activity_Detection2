# Mining Activity Monitoring Tool - System Documentation

## 📑 Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Data Processing Pipeline](#data-processing-pipeline)
5. [API Endpoints](#api-endpoints)
6. [Frontend Components](#frontend-components)
7. [Coordinate System](#coordinate-system)
8. [Computation Methodology](#computation-methodology)
9. [File Structure](#file-structure)
10. [Configuration](#configuration)

---

## System Overview

The Mining Activity Monitoring Tool is a full-stack web application designed for automated detection and analysis of open cast mining activities. It processes satellite imagery and Digital Elevation Model (DEM) data to identify mining sites, calculate excavation metrics, and provide compliance monitoring.

### Key Capabilities

- **Automated Mining Detection**: Processes COCO-annotated satellite imagery to identify mining boundaries
- **Volume Calculation**: Uses DEM data with geographic coordinate conversion for accurate excavation volume estimation
- **Compliance Monitoring**: Distinguishes between legal and illegal mining operations
- **Interactive Visualization**: Real-time map view with satellite imagery overlay and polygon boundaries
- **Comprehensive Reporting**: Generates detailed analytics and compliance reports

### Current Deployment

- **Study Area**: Singrauli region
- **Total Sites**: 11 mining sites
- **Legal Sites**: 9 (operated by Northern Coalfields Limited - NCL)
- **Illegal Sites**: 2 (Sites 8 and 9)
- **Total Area**: 10,730.73 hectares
- **Total Excavation Volume**: 7.12 billion cubic meters

---

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                       Frontend Layer                         │
│  React 18.2 + Vite 5.0 + TailwindCSS + Leaflet.js          │
│  Ports: 3000 (dev), 4173 (preview)                          │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/REST
┌─────────────────────────────────────────────────────────────┐
│                       Backend Layer                          │
│  Flask API + Flask-CORS                                      │
│  Port: 5000                                                  │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                    Data Processing Layer                     │
│  Rasterio + GDAL + NumPy + OpenCV                           │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                       Data Storage                           │
│  - Satellite Imagery (GeoTIFF)                              │
│  - DEM Data (GeoTIFF)                                       │
│  - Annotations (COCO JSON)                                  │
│  - Computed Metrics (JSON)                                  │
│  - Generated Reports (HTML/PDF)                             │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

1. **Data Ingestion**: COCO annotations + Satellite imagery + DEM data
2. **Processing**: `compute_real_metrics.py` generates metrics and stores in JSON
3. **API Layer**: Flask serves computed metrics and metadata via REST endpoints
4. **Frontend**: React components fetch data and render interactive visualizations
5. **User Interaction**: Dashboard analytics, map exploration, report generation

---

## Technology Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.13.7 | Core runtime |
| Flask | 3.1.0 | REST API framework |
| Flask-CORS | 5.0.0 | Cross-origin resource sharing |
| Rasterio | 1.4.3 | Geospatial raster data I/O |
| GDAL | 3.10.1 | Geospatial data abstraction |
| NumPy | 2.2.1 | Numerical computations |
| OpenCV | 4.10.0 | Image processing |
| Pillow | 11.0.0 | Image manipulation |
| pyproj | 3.7.0 | Coordinate transformations |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.2.0 | UI framework |
| Vite | 5.0.8 | Build tool and dev server |
| TailwindCSS | 3.4.1 | Utility-first CSS |
| Leaflet | 1.9.4 | Interactive maps |
| React-Leaflet | 4.2.1 | React bindings for Leaflet |
| Lucide-React | 0.263.1 | Icon library |
| React-Router-DOM | 6.20.1 | Client-side routing |

---

## Data Processing Pipeline

### Input Data Structure

```
data/Singrauli/
├── Singrauli_Sentinel2_RGB.tif      # Satellite imagery (1500×719 pixels)
├── Singrauli_SRTM_DEM.tif           # Digital Elevation Model
├── Singrauli_mines_image.jpeg       # Visual reference
└── mine_shape/
    ├── _annotations.coco.json       # Mining boundary annotations
    └── Singrauli_mines_image_jpeg.rf.*.jpg
```

### Processing Workflow (`compute_real_metrics.py`)

#### 1. Data Loading
```python
# Load COCO annotations
with open(annotation_file) as f:
    coco_data = json.load(f)

# Load satellite imagery
img_dataset = rasterio.open(satellite_image)

# Load DEM data
dem_dataset = rasterio.open(dem_file)
```

#### 2. Polygon Extraction
- Extracts segmentation polygons from COCO annotations
- Converts COCO format (list of points) to coordinate arrays
- Creates separate polygon for each annotated mining site

#### 3. Area Calculation
```python
# Geographic coordinate conversion at Singrauli latitude (24.19°N)
lat = 24.19
meters_per_deg_x = 111320 * np.cos(np.radians(lat))  # ~102,000 m/deg
meters_per_deg_y = 111320                             # ~111,320 m/deg

# Calculate pixel size in square meters
pixel_size_m2 = (abs(transform[0]) * meters_per_deg_x * 
                 abs(transform[4]) * meters_per_deg_y)

# Calculate area
area_pixels = np.sum(mask)
area_m2 = area_pixels * pixel_size_m2
area_hectares = area_m2 / 10000
```

#### 4. Volume Calculation
```python
# Extract height values within mining polygon
heights = dem_band[mask > 0]
min_height = np.min(heights)

# Calculate volume below surface level
height_differences = min_height - heights
height_differences[height_differences < 0] = 0

# Volume = sum of height differences × pixel area
volume_m3 = np.sum(height_differences) * pixel_size_m2
```

#### 5. Site Classification
```python
# Sites 8 and 9 are classified as illegal
is_legal = idx not in [7, 8]  # Zero-indexed, so 7=site8, 8=site9

site_data = {
    "id": idx + 1,
    "name": f"Site {idx + 1}",
    "type": "legal" if is_legal else "illegal",
    "operator": "Northern Coalfields Limited (NCL)" if is_legal else "Unauthorized",
    "area": area_hectares,
    "volume": volume_m3,
    "depth": max_depth
}
```

#### 6. Output Generation
- Creates `frontend/public/computed_metrics.json`
- Includes metadata (totals, counts) and per-site metrics
- Used by both API and frontend for data consistency

---

## API Endpoints

Base URL: `http://localhost:5000`

### 1. Health Check
```http
GET /api/health
```
**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00"
}
```

### 2. Get All Sites
```http
GET /api/sites
```
**Response:**
```json
{
  "sites": [
    {
      "id": 1,
      "name": "Site 1",
      "type": "legal",
      "operator": "Northern Coalfields Limited (NCL)",
      "area": 752.45,
      "volume": 423156789,
      "depth": 145.2,
      "coordinates": [[...], [...]]
    }
  ],
  "total": 11
}
```

### 3. Get Site by ID
```http
GET /api/sites/<id>
```
**Response:**
```json
{
  "id": 1,
  "name": "Site 1",
  "type": "legal",
  "operator": "Northern Coalfields Limited (NCL)",
  "area": 752.45,
  "volume": 423156789,
  "depth": 145.2,
  "coordinates": [[...], [...]]
}
```

### 4. Get Mining Statistics
```http
GET /api/stats
```
**Response:**
```json
{
  "total_sites": 11,
  "legal_sites": 9,
  "illegal_sites": 2,
  "total_area": 10730.73,
  "total_volume": 7119969518,
  "legal_area": 8933.60,
  "illegal_area": 1797.13,
  "average_depth": 234.5
}
```

### 5. Get Legal Sites
```http
GET /api/sites/legal
```

### 6. Get Illegal Sites
```http
GET /api/sites/illegal
```

### 7. Search Sites
```http
GET /api/sites/search?operator=NCL&minArea=500&maxArea=1500
```
**Query Parameters:**
- `operator`: Filter by operator name
- `minArea`: Minimum area in hectares
- `maxArea`: Maximum area in hectares
- `minDepth`: Minimum depth in meters
- `maxDepth`: Maximum depth in meters

### 8. Generate Report
```http
POST /api/generate-report
Content-Type: application/json

{
  "site_ids": [1, 2, 3],
  "format": "html"
}
```

---

## Frontend Components

### Page Structure

```
App (Router)
├── Layout (Navigation + Sidebar)
│   ├── Dashboard (/)
│   ├── MapView (/map)
│   └── Reports (/reports)
```

### 1. Dashboard (`src/pages/Dashboard.jsx`)

**Purpose**: Main overview with key metrics and site table

**Data Source**: `computed_metrics.json`

**Sections**:
- **Stats Cards**: Total sites, legal/illegal counts, total area, total volume
- **Area Distribution**: Progress bars showing legal vs illegal area breakdown
- **Excavation Summary**: Volume metrics with visual indicators
- **Mining Sites Table**: All 11 sites with compliance status
- **Quick Actions**: Links to Map View and Reports

**Key Code**:
```jsx
useEffect(() => {
  fetch('/computed_metrics.json')
    .then(res => res.json())
    .then(data => setMiningData(data));
}, []);
```

### 2. MapView (`src/pages/MapView.jsx`)

**Purpose**: Interactive map with satellite imagery and mining boundaries

**Key Features**:
- Leaflet Simple CRS for pixel-based coordinates
- Y-axis coordinate inversion: `[719 - y, x]`
- Satellite imagery as base layer (1500×719px)
- Color-coded polygons (green=legal, red=illegal)
- Popup info cards on polygon click
- Legend in statistics sidebar

**Coordinate System**:
```jsx
const bounds = [[0, 0], [719, 1500]];

const convertCoordinates = (coords) => {
  return coords.map(coord => [719 - coord[1], coord[0]]);
};
```

**Polygon Rendering**:
```jsx
<Polygon
  positions={convertCoordinates(site.coordinates)}
  pathOptions={{
    color: site.type === 'legal' ? '#10b981' : '#ef4444',
    fillOpacity: 0.3
  }}
>
  <Popup>
    <div className="p-2">
      <h3>{site.name}</h3>
      <p>Area: {site.area.toFixed(2)} ha</p>
      <p>Volume: {(site.volume / 1e9).toFixed(2)} B m³</p>
    </div>
  </Popup>
</Polygon>
```

### 3. Reports (`src/pages/Reports.jsx`)

**Purpose**: Compliance reporting and analysis export

**Sections**:
- **Report Summary**: Metadata and assessment info
- **Executive Summary**: Key findings from computed metrics
- **Compliance Status**: Legal/illegal breakdown with cards
- **Site-wise Breakdown**: First 5 sites with detailed metrics
- **Export Options**: Download as PDF, Excel, or JSON

---

## Coordinate System

### Challenge

Leaflet uses standard map coordinates `[lat, lon]`, but our satellite image is a raster with pixel coordinates. The COCO annotations use image coordinates `[x, y]` where:
- `x`: 0 to 1500 (width)
- `y`: 0 to 719 (height)
- Origin: Top-left corner

### Solution: Leaflet Simple CRS + Y-axis Inversion

```jsx
// Map bounds in [row, col] format
const bounds = [[0, 0], [719, 1500]];  // [height, width]

// Coordinate conversion function
const convertCoordinates = (coords) => {
  // coords format: [[x1, y1], [x2, y2], ...]
  // Leaflet Simple CRS expects: [[row, col], ...]
  // row = 719 - y (invert Y-axis)
  // col = x
  return coords.map(coord => [719 - coord[1], coord[0]]);
};

// Map configuration
<MapContainer
  crs={CRS.Simple}
  bounds={bounds}
  style={{ height: '100%', width: '100%' }}
>
  <ImageOverlay
    url="/Singrauli_mines_image.jpeg"
    bounds={bounds}
  />
</MapContainer>
```

### Why Y-axis Inversion?

- **Image coordinates**: Y increases downward (top=0, bottom=719)
- **Leaflet Simple CRS**: Row increases downward, but polygons appear correctly only with inversion
- **Formula**: `leaflet_row = image_height - coco_y = 719 - y`

This ensures perfect alignment between satellite imagery and mining boundary polygons.

---

## Computation Methodology

### Geographic Coordinate Conversion

At Singrauli's latitude (24.19°N), degrees are converted to meters:

```python
lat = 24.19  # degrees North

# Meters per degree of longitude (varies by latitude)
meters_per_deg_x = 111320 * np.cos(np.radians(lat))
# Result: ~102,000 m/degree

# Meters per degree of latitude (constant)
meters_per_deg_y = 111320
```

### Volume Estimation

Uses a height-difference method:

1. Extract all elevation values within mining polygon from DEM
2. Find minimum elevation (deepest point)
3. Calculate height difference for each pixel: `min_height - pixel_height`
4. Sum all height differences and multiply by pixel area in m²
5. Result: Total excavation volume in cubic meters

This method assumes the original ground level was at the minimum observed height, providing a conservative volume estimate.

### Accuracy Considerations

- **DEM Resolution**: SRTM has ~30m resolution, suitable for large mining areas
- **Coordinate Precision**: Geographic conversion accurate to <0.1%
- **Volume Method**: Conservative estimate (actual volume may be higher)
- **Temporal Factor**: Single-time snapshot, not tracking changes over time

---

## File Structure

```
mining_activity_monitoring_tool/
├── frontend/                          # React application
│   ├── public/
│   │   ├── computed_metrics.json     # Generated metrics data
│   │   └── Singrauli_mines_image.jpeg # Satellite base layer
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx         # Main overview page
│   │   │   ├── MapView.jsx           # Interactive map
│   │   │   └── Reports.jsx           # Compliance reports
│   │   ├── components/
│   │   │   └── Layout.jsx            # Navigation wrapper
│   │   ├── App.jsx                   # Router configuration
│   │   └── main.jsx                  # Entry point
│   ├── package.json
│   └── vite.config.js
│
├── data/Singrauli/                    # Input data
│   ├── Singrauli_Sentinel2_RGB.tif   # Satellite imagery
│   ├── Singrauli_SRTM_DEM.tif        # Elevation data
│   └── mine_shape/
│       └── _annotations.coco.json    # Mining boundaries
│
├── src/                               # Source modules (legacy)
│   ├── mining_detector.py
│   ├── volume_calculator.py
│   ├── map_generator.py
│   └── report_generator.py
│
├── outputs/                           # Generated outputs
│   ├── detected_mining_areas.tif
│   ├── unauthorized_mining.tif
│   └── mining_analysis_report.html
│
├── compute_real_metrics.py            # Main metrics computation
├── api.py                             # Flask REST API
├── requirements.txt                   # Python dependencies
├── config.yaml                        # Configuration file
├── start.bat / start.sh               # Startup scripts
└── README.md / SYSTEM_DOCUMENTATION.md
```

---

## Configuration

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
  latitude: 24.19        # Singrauli latitude for coordinate conversion

api:
  host: "localhost"
  port: 5000
  cors_origins: ["http://localhost:3000", "http://localhost:4173"]
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

## Maintenance and Updates

### Updating Mining Site Classifications

Edit `compute_real_metrics.py` line 325:
```python
# Current: Sites 8 and 9 are illegal
is_legal = idx not in [7, 8]  # Zero-indexed

# To change, modify the list:
is_legal = idx not in [5, 6, 7]  # Would make sites 6, 7, 8 illegal
```

Then regenerate metrics:
```bash
python compute_real_metrics.py
```

### Adding New Study Areas

1. Place data in `data/<region_name>/`:
   - Satellite imagery (GeoTIFF)
   - DEM file (GeoTIFF)
   - COCO annotations JSON

2. Update `config.yaml` with new paths

3. Update frontend coordinate bounds in `MapView.jsx`

4. Run `compute_real_metrics.py`

### Performance Optimization

- **Backend**: Consider caching computed metrics in memory
- **Frontend**: Implement lazy loading for large polygon datasets
- **Database**: For large-scale deployments, migrate from JSON to PostgreSQL/PostGIS

---

## Troubleshooting

### Common Issues

1. **Black Screen in Frontend**
   - Check browser console for errors
   - Verify `computed_metrics.json` exists in `frontend/public/`
   - Ensure all icon imports are correct

2. **Misaligned Polygons on Map**
   - Verify Y-axis coordinate inversion: `[719 - y, x]`
   - Check image dimensions match bounds: `[[0, 0], [719, 1500]]`
   - Confirm CRS.Simple is used in MapContainer

3. **Volume Showing 0**
   - Verify DEM file is loaded correctly
   - Check geographic coordinate conversion is applied
   - Ensure pixel size calculation uses latitude-specific values

4. **API CORS Errors**
   - Verify Flask-CORS is installed
   - Check `cors_origins` in configuration includes frontend URL
   - Restart Flask server after configuration changes

---

## Version History

- **v1.0** (Initial): Basic detection and volume calculation
- **v2.0** (Current): Full-stack application with React frontend, Flask API, accurate volume calculation, and compliance monitoring

## Contributors

Developed for mining activity monitoring and environmental compliance assessment.

## License

Internal use for government mining monitoring purposes.
