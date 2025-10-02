# 🚀 SETUP & RUN GUIDE

## Quick Setup (Windows)

### Option 1: Automated Startup (Recommended)

**Double-click:** `start.bat`

This will:
1. ✅ Check Python & Node.js
2. ✅ Install dependencies
3. ✅ Start Flask API (port 5000)
4. ✅ Start React frontend (port 5173)
5. ✅ Open two terminal windows

**Then open browser:** http://localhost:5173

---

### Option 2: Manual Startup (Two Terminals)

#### Terminal 1 - Backend
```batch
start-backend.bat
```
OR
```powershell
python api.py
```

#### Terminal 2 - Frontend
```batch
start-frontend.bat
```
OR
```powershell
cd frontend
npm run dev
```

---

## First Time Setup

### Step 1: Install Prerequisites

#### Python 3.8+
Download from: https://www.python.org/downloads/
- ✅ Check "Add Python to PATH" during installation

#### Node.js 16+
Download from: https://nodejs.org/
- ✅ Choose LTS version
- ✅ Include npm package manager

#### Verify Installation
```powershell
python --version   # Should show 3.8 or higher
node --version     # Should show 16.0 or higher
npm --version      # Should show 7.0 or higher
```

---

### Step 2: Install Dependencies

#### Python Dependencies
```powershell
pip install -r requirements.txt
```

**This installs:**
- Flask & Flask-CORS (API server)
- Rasterio & GeoPandas (geospatial processing)
- OpenCV & NumPy (image processing)
- Folium & Plotly (visualization)
- And 20+ more packages

**If you get errors:**
```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install individual packages if needed
pip install flask flask-cors
pip install rasterio geopandas
pip install opencv-python numpy scipy
```

#### Node.js Dependencies
```powershell
cd frontend
npm install
cd ..
```

**This installs:**
- React & Vite (frontend framework)
- Tailwind CSS (styling)
- Chart.js & Leaflet (visualizations)
- Framer Motion (animations)
- And more...

**If you get errors:**
```powershell
cd frontend
# Clear cache and reinstall
rm -r node_modules
rm package-lock.json
npm install
cd ..
```

---

## Running the Application

### Method 1: One-Click (Easiest)

```batch
start.bat
```

Two windows will open:
1. **Backend Terminal** - Shows Flask API logs
2. **Frontend Terminal** - Shows Vite dev server

**Access:**
- Frontend: http://localhost:5173
- API: http://localhost:5000

---

### Method 2: Separate Scripts

**Terminal 1:**
```batch
start-backend.bat
```

**Terminal 2:**
```batch
start-frontend.bat
```

---

### Method 3: Manual Commands

**Terminal 1 - Backend:**
```powershell
python api.py
```

Expected output:
```
 * Serving Flask app 'api'
 * Debug mode: on
WARNING: This is a development server.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```

Expected output:
```
VITE v5.0.0  ready in 500 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
➜  press h to show help
```

---

## Troubleshooting

### Problem: "Python not found"
**Solution:**
```powershell
# Add Python to PATH or use full path
C:\Python39\python.exe api.py
```

### Problem: "npm not found"
**Solution:**
```powershell
# Restart terminal after installing Node.js
# Or add to PATH: C:\Program Files\nodejs\
```

### Problem: "Cannot import name 'MapVisualizer2D'"
**Solution:** ✅ Already fixed! The class names are now correct.

### Problem: "Port 5000 already in use"
**Solution:**
```powershell
# Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Problem: "Port 5173 already in use"
**Solution:**
```powershell
# Find and kill process on port 5173
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

### Problem: "Module not found" errors
**Solution:**
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
cd frontend
npm install --force
cd ..
```

### Problem: Flask CORS errors
**Solution:** ✅ Already configured in `api.py`

### Problem: Frontend can't connect to API
**Check:**
1. Backend is running on port 5000
2. Visit http://localhost:5000/api/health
3. Should return: `{"status":"healthy","version":"1.0.0"}`

---

## Verify Everything Works

### 1. Check Backend
```powershell
# In browser or curl:
curl http://localhost:5000/api/health
```

Expected response:
```json
{"status":"healthy","version":"1.0.0"}
```

### 2. Check Frontend
Open browser: http://localhost:5173

You should see:
- ✅ Dark-themed dashboard
- ✅ Sidebar navigation
- ✅ Statistics cards
- ✅ Charts

### 3. Test API
```powershell
curl http://localhost:5000/api/stats
```

Expected response:
```json
{
  "total_analyses": 0,
  "total_sites": 11,
  "total_area": 152.4,
  ...
}
```

---

## Project Structure

```
mining_activity_monitoring_tool/
│
├── start.bat                  ← Use this!
├── start-backend.bat          ← Backend only
├── start-frontend.bat         ← Frontend only
├── api.py                     ← Flask API server
├── main.py                    ← CLI tool
├── requirements.txt           ← Python packages
│
├── frontend/
│   ├── src/
│   │   ├── pages/            ← React pages
│   │   ├── components/       ← React components
│   │   └── App.jsx           ← Router
│   ├── package.json          ← Node packages
│   └── vite.config.js        ← Vite config
│
├── src/                       ← Python modules
│   ├── utils/
│   ├── detection/
│   ├── depth_volume/
│   ├── visualization/
│   └── report_generation/
│
└── data/                      ← Sample data
    └── Singrauli/
```

---

## Next Steps

### 1. Run the Application
```batch
start.bat
```

### 2. Open Browser
```
http://localhost:5173
```

### 3. Explore Features
- 📊 Dashboard - View statistics
- 🗺️ Map View - Interactive visualization
- 📈 Analysis - Real-time progress
- 📑 Reports - Browse reports
- 📤 Upload - Upload your data

### 4. Test with Sample Data
```powershell
python main.py --satellite data/Singrauli/Singrauli_Sentinel2_RGB.tif --dem data/Singrauli/Singrauli_SRTM_DEM.tif --annotations data/Singrauli/mine_shape/_annotations.coco.json --output_dir results/
```

---

## Production Deployment

### Frontend (Vercel/Netlify)
```powershell
cd frontend
npm run build
# Deploy 'dist' folder
```

### Backend (Heroku/Railway)
```powershell
# Create Procfile:
echo "web: python api.py" > Procfile
# Deploy repository
```

---

## Common Commands

```powershell
# Start everything
start.bat

# Just backend
start-backend.bat

# Just frontend  
start-frontend.bat

# Run CLI analysis
python main.py --help

# Check API health
curl http://localhost:5000/api/health

# Build frontend for production
cd frontend && npm run build

# Run tests (if added)
pytest tests/
```

---

## Support

**Documentation:**
- `README_COMPLETE.md` - Full project docs
- `API_DOCUMENTATION.md` - API reference
- `FRONTEND_COMPLETION.md` - Frontend guide
- `QUICK_START_CARD.md` - Quick reference

**Issues:**
1. Check terminal output for errors
2. Verify all dependencies installed
3. Check if ports are available
4. Review documentation

---

## ✅ Checklist

Before running:
- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`cd frontend && npm install`)
- [ ] Ports 5000 and 5173 available

To run:
- [ ] Run `start.bat`
- [ ] Wait for both servers to start
- [ ] Open http://localhost:5173
- [ ] See dashboard with dark theme

---

**Ready to go! Run `start.bat` and enjoy your mining monitoring tool! 🛰️**
