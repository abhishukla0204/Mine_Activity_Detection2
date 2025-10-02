# Daily Usage Guide

## Starting the Application

### Terminal 1 - Backend (Flask API)
```powershell
# Navigate to project
cd C:\Abhinav_Shukla\Project2\mining_activity_monitoring_tool

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start backend
python api.py
```

Wait for: `Running on http://127.0.0.1:5000`

---

### Terminal 2 - Frontend (React)
```powershell
# Navigate to frontend
cd C:\Abhinav_Shukla\Project2\mining_activity_monitoring_tool\frontend

# Start frontend
npm run dev
```

Wait for: `Local: http://localhost:5173/`

---

## Access Application

Open browser: **http://localhost:5173**

---

## Stopping the Application

1. Press `Ctrl+C` in Terminal 1 (Backend)
2. Press `Ctrl+C` in Terminal 2 (Frontend)
3. Run `deactivate` in Terminal 1 to exit venv

---

## Quick Health Check

```powershell
curl http://localhost:5000/api/health
```

Should return: `{"status":"healthy","version":"1.0.0"}`

---

## First Time Setup?

See **MANUAL_SETUP.md** for complete installation instructions.
