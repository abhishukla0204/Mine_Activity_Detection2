# Mining Activity Monitoring Tool - Real Data Integration

## Summary of Changes

### 1. Fixed Black Screen Issue
**Problem**: Map was showing black screen due to coordinate system mismatch.

**Solution**:
- Changed from geographic coordinates to Leaflet's `CRS.Simple` (pixel-based)
- Set proper image bounds: `[0, 0]` to `[719, 1500]` matching your 719×1500px image
- Adjusted polygon coordinates to use `[y, x]` format directly from COCO annotations
- Disabled zoom/pan to keep map static

### 2. Created Real Computation Module (`compute_real_metrics.py`)
**Purpose**: Calculate actual mining metrics using your real data instead of fake values.

**Data Sources Used**:
1. **Singrauli_mines_image.jpeg** (1500×719 px) - Base satellite imagery
2. **_annotations.coco.json** - Mine boundary polygons (11 sites)
3. **Singrauli_SRTM_DEM.tif** (854×409 px) - Digital Elevation Model for depth/volume
4. **Singrauli_Sentinel2_RGB.tif** (2558×1225 px) - High-res RGB satellite data

**Metrics Computed**:
- ✅ **Real Area**: Calculated from COCO polygons mapped to geographic coordinates
  - Converts image pixels → degrees → square meters → hectares
  - Accounts for latitude (24.19°N) in coordinate conversion
  
- ✅ **Real Perimeter**: Polygon perimeter in kilometers

- ✅ **Depth**: Calculated from DEM elevation differences
  - Max elevation (reference) - Min elevation (pit bottom)
  
- ✅ **Volume**: Excavation volume in cubic meters
  - Sum of elevation differences × pixel area
  
- ⚠️ **Material Type**: Basic RGB analysis (can be enhanced with ML)

### 3. Real Results Generated

**Total Mining Activity in Singrauli:**
- **Total Mines**: 11 sites
- **Legal Sites**: 7 (6,206.90 hectares)
- **Illegal Sites**: 4 (4,523.83 hectares)
- **Total Area**: 10,730.73 hectares (~107 km²)

**Individual Mine Examples**:
- **Objects**: 1,084.47 ha, 205m depth
- **Mine8**: 1,978.57 ha, 279m depth (largest)
- **Mine2**: 428.24 ha, 183m depth

### 4. Frontend Integration

**MapView Updates**:
- Loads `computed_metrics.json` (real data) if available
- Falls back to `mine_annotations.json` (COCO raw data) if not computed
- Displays real metrics: area_hectares, depth_m, volume_m3, perimeter_km
- Maintains backward compatibility with old data format

**File Locations**:
```
frontend/public/
├── singrauli_satellite.jpg       # Base map image
├── mine_annotations.json          # COCO polygon data
└── computed_metrics.json          # Real computed metrics ⭐
```

### 5. How to Recompute Metrics

Whenever you update the data or want to recalculate:

```powershell
# From project root:
.venv\Scripts\python.exe compute_real_metrics.py
```

This will:
1. Read all your data files (DEM, RGB, COCO annotations)
2. Calculate real-world metrics
3. Save results to `frontend/public/computed_metrics.json`
4. Frontend auto-loads the new data (refresh page)

### 6. Coordinate System Mapping

**Challenge**: Three different coordinate systems need alignment:
- Image space: 1500×719 pixels (JPEG)
- DEM space: 854×409 pixels (GeoTIFF)
- Geographic space: ~82.62-82.72°E, 24.15-24.24°N (lat/lon)

**Solution**:
```python
# Image pixel → Geographic degrees
deg_per_pixel_x = (lon_max - lon_min) / image_width
deg_per_pixel_y = (lat_max - lat_min) / image_height

# Geographic degrees → Meters (at 24.19°N latitude)
meters_per_deg_lat = 111,320 m
meters_per_deg_lon = 111,320 × cos(24.19°) ≈ 101,543 m

# Final area calculation
area_m² = pixel_area × deg_per_pixel_x × deg_per_pixel_y × meters_per_deg_lat × meters_per_deg_lon
```

### 7. Next Steps / Enhancements

**Completed** ✅:
- Real area calculation
- Real depth calculation  
- Real perimeter calculation
- Coordinate system alignment
- Frontend integration

**Can Be Enhanced** 🔄:
- **Volume calculation**: Currently simplified, can use more sophisticated DEM analysis
- **Material detection**: Add ML model for coal/overburden/vegetation classification
- **Change detection**: Compare satellite images over time
- **Compliance scoring**: ML-based assessment of legal vs illegal indicators
- **Temporal analysis**: Track mining expansion over months/years

### 8. Module Architecture

```
compute_real_metrics.py
├── RealMiningMetricsCalculator
│   ├── __init__()              # Load COCO, DEM, RGB data
│   ├── pixel_to_geo_coords()   # Coordinate transformation
│   ├── calculate_pixel_area()  # Area calculation with CRS handling
│   ├── polygon_from_segmentation()  # COCO → Shapely polygon
│   ├── calculate_mine_volume() # DEM-based volume estimation
│   ├── analyze_mine_material() # RGB-based material inference
│   ├── compute_all_metrics()   # Main processing loop
│   └── save_results()          # Export to JSON
```

### 9. Data Quality Notes

**DEM Resolution**: ~27.37 meters/pixel
- Good for macro-level depth analysis
- May not capture fine details (equipment, small pits)

**RGB Resolution**: Higher (~10m/pixel estimated)
- Better for visual analysis
- Can be used for more detailed material classification

**Coordinate Accuracy**: ±30m typical for SRTM DEM
- Sufficient for mine site boundaries
- May have slight offsets between datasets

### 10. Testing the Frontend

1. **Start Backend** (if not running):
   ```powershell
   .venv\Scripts\python.exe api.py
   ```

2. **Start Frontend** (if not running):
   ```powershell
   cd frontend
   npm run dev
   ```

3. **Navigate to**: `http://localhost:5173/map`

4. **Expected Behavior**:
   - Satellite image as background
   - 11 colored polygons (7 green legal, 4 red illegal)
   - Click polygons to see real metrics
   - Static map (no zoom/pan)

### 11. Troubleshooting

**Black screen?**
- Check browser console for errors
- Verify `/singrauli_satellite.jpg` loads (Network tab)
- Check Leaflet CSS is loaded

**No polygons?**
- Check `/computed_metrics.json` exists
- Verify coordinates array in JSON
- Check browser console for fetch errors

**Wrong areas/volumes?**
- Re-run `compute_real_metrics.py`
- Check CRS of input GeoTIFFs
- Verify COCO annotations are in correct pixel space

---

## Files Modified/Created

**Created**:
- ✅ `compute_real_metrics.py` - Real metrics computation engine
- ✅ `frontend/public/computed_metrics.json` - Real data output
- ✅ `frontend/public/mine_annotations.json` - COCO data copy
- ✅ `frontend/public/singrauli_satellite.jpg` - Base map image

**Modified**:
- ✅ `frontend/src/pages/MapView.jsx` - Load real data, fix coordinates

**Unchanged** (still functional):
- ✅ Backend API (`api.py`)
- ✅ All other Python modules
- ✅ Dashboard, Reports, Analysis pages
