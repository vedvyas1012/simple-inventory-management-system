#!/bin/bash

# Inventory Management System - Startup Script

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   Starting Inventory Management System...                 ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "✗ Virtual environment not found!"
    echo "  Creating virtual environment..."
    python3 -m venv venv
    echo "  Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
    echo "✓ Setup complete!"
    echo ""
fi

# Activate virtual environment
echo "→ Activating virtual environment..."
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "✗ .env file not found!"
    echo "  Please configure your database credentials in .env"
    exit 1
fi

# Start the application
echo "→ Starting Flask application..."
echo ""
python run.py
