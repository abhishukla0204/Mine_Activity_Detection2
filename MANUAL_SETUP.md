# Manual Setup Instructions

## Prerequisites

- Python 3.8+ installed
- Node.js 16+ installed
- npm 7+ installed

Check versions:
```powershell
python --version
node --version
npm --version
```

---

## Step 1: Create Virtual Environment

```powershell
# Navigate to project directory
cd C:\Abhinav_Shukla\Project2\mining_activity_monitoring_tool

# Create virtual environment
python -m venv venv

# Activate virtual environment (PowerShell)
.\venv\Scripts\Activate.ps1

# You should see (venv) in your prompt like:
# (venv) PS C:\Abhinav_Shukla\Project2\mining_activity_monitoring_tool>
```

**Note:** If you get execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Step 2: Install Python Dependencies

```powershell
# Make sure venv is activated (you should see (venv) in prompt)

# Upgrade pip first
python -m pip install --upgrade pip

# Install all dependencies from requirements.txt
pip install -r requirements.txt
```

**This installs:**
- Flask & Flask-CORS (API)
- Rasterio & GeoPandas (geospatial)
- OpenCV & NumPy (image processing)
- Folium & Plotly (visualization)
- Pandas, Matplotlib, Pillow (data & imaging)
- And more...

**If you encounter errors**, install packages individually:
```powershell
# Core API
pip install flask flask-cors

# Geospatial
pip install rasterio geopandas shapely pyproj fiona

# Image processing
pip install opencv-python numpy scipy pillow

# Visualization
pip install folium plotly matplotlib seaborn

# Utilities
pip install pandas tqdm pyyaml python-dotenv jinja2
```

---

## Step 3: Install Frontend Dependencies

```powershell
# Navigate to frontend directory
cd frontend

# Install all Node.js packages
npm install

# This installs React, Vite, Tailwind CSS, Chart.js, Leaflet, etc.

# Go back to project root
cd ..
```

---

## Step 4: Start Backend (Terminal 1)

```powershell
# Navigate to project root
cd C:\Abhinav_Shukla\Project2\mining_activity_monitoring_tool

# Activate virtual environment if not already activated
.\venv\Scripts\Activate.ps1

# Start Flask API
python api.py
```

**Expected output:**
```
 * Serving Flask app 'api'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Running on http://10.83.0.199:5000
Press CTRL+C to quit
 * Debugger is active!
```

✅ **Backend is running when you see "Running on http://127.0.0.1:5000"**

---

## Step 5: Start Frontend (Terminal 2)

**Open a NEW terminal/PowerShell window**

```powershell
# Navigate to frontend directory
cd C:\Abhinav_Shukla\Project2\mining_activity_monitoring_tool\frontend

# Start Vite development server
npm run dev
```

**Expected output:**
```
VITE v5.0.0  ready in 500 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
➜  press h to show help
```

✅ **Frontend is running when you see "Local: http://localhost:5173/"**

---

## Step 6: Access Application

Open your browser and go to: **http://localhost:5173**

You should see:
- 🎨 Dark-themed dashboard
- 📊 Statistics cards showing mining data
- 🗺️ Sidebar navigation
- 📈 Charts and visualizations

---

## Verify Everything Works

### Test 1: Backend Health Check
```powershell
curl http://localhost:5000/api/health
```

**Expected response:**
```json
{"status":"healthy","version":"1.0.0"}
```

### Test 2: Get Statistics
```powershell
curl http://localhost:5000/api/stats
```

**Expected response:**
```json
{
  "total_analyses": 0,
  "total_sites": 11,
  "total_area": 152.4,
  "legal_area": 98.6,
  "illegal_area": 53.8,
  ...
}
```

### Test 3: Frontend Navigation
- Click "Dashboard" - See overview
- Click "Map View" - See Leaflet map
- Click "Analysis" - See progress tracker
- Click "Reports" - Browse reports
- Click "Upload Data" - File upload interface

---

## Stop Services

### Stop Backend (Terminal 1)
Press `Ctrl + C` in the backend terminal

### Stop Frontend (Terminal 2)
Press `Ctrl + C` in the frontend terminal

### Deactivate Virtual Environment
```powershell
deactivate
```

---

## Daily Usage

### Starting Work
```powershell
# Terminal 1 - Backend
cd C:\Abhinav_Shukla\Project2\mining_activity_monitoring_tool
.\venv\Scripts\Activate.ps1
python api.py

# Terminal 2 - Frontend (new window)
cd C:\Abhinav_Shukla\Project2\mining_activity_monitoring_tool\frontend
npm run dev

# Open browser: http://localhost:5173
```

### Stopping Work
- Press `Ctrl+C` in both terminals
- Run `deactivate` in Terminal 1

---

## Troubleshooting

### Virtual Environment Not Activating
```powershell
# PowerShell execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again
.\venv\Scripts\Activate.ps1
```

### Module Not Found Errors
```powershell
# Activate venv first
.\venv\Scripts\Activate.ps1

# Reinstall requirements
pip install -r requirements.txt
```

### Port Already in Use
```powershell
# Find process on port 5000
netstat -ano | findstr :5000

# Kill process
taskkill /PID <PID> /F

# Same for port 5173
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

### Frontend Won't Start
```powershell
cd frontend

# Remove node_modules and reinstall
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

---

## Project Structure

```
mining_activity_monitoring_tool/
│
├── venv/                      ← Virtual environment (DO NOT COMMIT)
├── api.py                     ← Flask API backend
├── main.py                    ← CLI tool
├── requirements.txt           ← Python dependencies
│
├── frontend/
│   ├── node_modules/         ← Node packages (DO NOT COMMIT)
│   ├── src/                  ← React source code
│   ├── package.json          ← Frontend dependencies
│   └── vite.config.js        ← Vite configuration
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

## Important Notes

1. **Always activate venv** before running Python commands
2. **Keep both terminals open** while using the application
3. **Virtual environment** keeps packages isolated from global Python
4. **Don't commit** `venv/` or `node_modules/` to git
5. **Use two separate terminals** - one for backend, one for frontend

---

## Quick Reference

```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# Deactivate venv
deactivate

# Start backend
python api.py

# Start frontend
cd frontend && npm run dev

# Check backend
curl http://localhost:5000/api/health

# Access app
http://localhost:5173
```

---

✅ **Setup Complete!** You now have a proper virtual environment with all dependencies installed locally.
