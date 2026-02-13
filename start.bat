@echo off
echo 🧪 API Lab - Starting Local Setup
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.11 or higher.
    pause
    exit /b 1
)
echo ✅ Python found
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo ✅ Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo ✅ Dependencies installed
echo.

REM Create instance directory for SQLite
if not exist "instance" (
    echo Creating instance directory for database...
    mkdir instance
    echo ✅ Instance directory created
)

REM Check if database exists
if not exist "instance\apilab.db" (
    echo 📦 No database found. Initializing...
    
    REM Initialize database
    python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('✅ Database initialized')"
    
    REM Seed database
    echo 🌱 Seeding database with test data...
    python seed.py
) else (
    echo ✅ Database already exists at instance\apilab.db
)
echo.

REM Start the server
echo ======================================
echo 🚀 Starting API Lab...
echo ======================================
echo.
echo 📍 Local URL:  http://localhost:5000
echo 📍 API Base:   http://localhost:5000/api
echo 📍 Dashboard:  http://localhost:5000
echo.
echo 🔑 Test Credentials:
echo    Admin:  admin@apilab.dev / admin123
echo    User:   testuser@apilab.dev / test123
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
