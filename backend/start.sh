#!/bin/bash

# Wish Wall Backend Startup Script

set -e

echo "Starting Wish Wall Backend..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Python version: $(python3 --version)"

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations (if using)
echo "Running database setup..."
if [ -f "migrate.py" ]; then
    python migrate.py
fi

# Start the application
echo "Starting application server..."
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
