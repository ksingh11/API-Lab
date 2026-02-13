#!/bin/bash

echo "🧪 API Zero to Hero - Starting Local Setup"
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create instance directory for SQLite
if [ ! -d "instance" ]; then
    echo "Creating instance directory for database..."
    mkdir instance
    echo "✅ Instance directory created"
fi

# Check if database exists
if [ ! -f "instance/apilab.db" ]; then
    echo "📦 No database found. Initializing..."
    
    # Initialize database
    python3 -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('✅ Database initialized')"
    
    # Seed database
    echo "🌱 Seeding database with test data..."
    python3 seed.py
else
    echo "✅ Database already exists at instance/apilab.db"
fi
echo ""

# Start the server
echo "======================================"
echo "🚀 Starting API Zero to Hero..."
echo "======================================"
echo ""
echo "📍 Local URL:  http://localhost:5000"
echo "📍 API Base:   http://localhost:5000/api"
echo "📍 Dashboard:  http://localhost:5000"
echo ""
echo "🔑 Test Credentials:"
echo "   Admin:  admin@apilab.dev / admin123"
echo "   User:   testuser@apilab.dev / test123"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
