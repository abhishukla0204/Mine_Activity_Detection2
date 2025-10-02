@echo off
REM Mining Activity Monitoring Tool - Simple Startup Script
REM Starts both Flask API backend and React frontend

echo ================================================
echo   Mining Activity Monitoring Tool - Startup
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8+
    pause
    exit /b 1
)
echo [1/4] Python found

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found. Please install Node.js 16+
    pause
    exit /b 1
)
echo [2/4] Node.js found

REM Install Python dependencies
echo [3/4] Installing Python dependencies...
pip install -r requirements.txt >nul 2>&1
if %errorlevel% equ 0 (
    echo Python dependencies installed
) else (
    echo Warning: Some Python dependencies may have failed
)

REM Install Node.js dependencies
echo [4/4] Installing Node.js dependencies...
cd frontend
call npm install >nul 2>&1
if %errorlevel% equ 0 (
    echo Node.js dependencies installed
) else (
    echo Warning: Some Node.js dependencies may have failed
)
cd ..

echo.
echo ================================================
echo   Starting Services...
echo ================================================
echo.

REM Start Flask API in background
echo Starting Flask API backend (port 5000)...
start "Mining API" cmd /k python api.py

REM Wait a bit for API to start
timeout /t 3 /nobreak >nul

REM Start React frontend
echo Starting React frontend (port 5173)...
cd frontend
start "Mining Frontend" cmd /k npm run dev
cd ..

echo.
echo ================================================
echo   Services Started!
echo ================================================
echo.
echo   Frontend: http://localhost:5173
echo   Backend API: http://localhost:5000
echo.
echo   Two terminal windows have opened.
echo   Close them to stop the services.
echo ================================================
echo.

pause
