#!/bin/bash

# Mining Activity Monitoring Tool - Startup Script (Linux/Mac)
# Starts both Flask API backend and React frontend

echo "================================================"
echo "  Mining Activity Monitoring Tool - Startup"
echo "================================================"
echo ""

# Check if Python is installed
echo "[1/4] Checking Python installation..."
if command -v python3 &> /dev/null; then
    echo "✓ Python found: $(python3 --version)"
else
    echo "✗ Python not found. Please install Python 3.8+"
    exit 1
fi

# Check if Node.js is installed
echo "[2/4] Checking Node.js installation..."
if command -v node &> /dev/null; then
    echo "✓ Node.js found: $(node --version)"
else
    echo "✗ Node.js not found. Please install Node.js 16+"
    exit 1
fi

# Install Python dependencies
echo "[3/4] Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ Python dependencies installed"
else
    echo "✗ Failed to install Python dependencies"
    exit 1
fi

# Install Node.js dependencies
echo "[4/4] Installing Node.js dependencies..."
cd frontend
npm install
if [ $? -eq 0 ]; then
    echo "✓ Node.js dependencies installed"
else
    echo "✗ Failed to install Node.js dependencies"
    cd ..
    exit 1
fi
cd ..

echo ""
echo "================================================"
echo "  Starting Services..."
echo "================================================"
echo ""

# Start Flask API in background
echo "Starting Flask API backend (port 5000)..."
python3 api.py &
API_PID=$!
sleep 3
echo "✓ Flask API started (PID: $API_PID)"

# Start React frontend in background
echo "Starting React frontend (port 5173)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
sleep 5
cd ..
echo "✓ React frontend started (PID: $FRONTEND_PID)"

echo ""
echo "================================================"
echo "  Services Running!"
echo "================================================"
echo ""
echo "  Frontend: http://localhost:5173"
echo "  Backend API: http://localhost:5000"
echo ""
echo "  Press Ctrl+C to stop all services"
echo "================================================"
echo ""

# Cleanup function
cleanup() {
    echo ""
    echo "Stopping services..."
    kill $API_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✓ Services stopped"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT TERM

# Wait
wait
