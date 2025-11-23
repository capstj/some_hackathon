#!/bin/bash
# WhisPay Setup Script for Linux/macOS

echo ""
echo "============================================================"
echo "WhisPay - Voice Banking Assistant Setup"
echo "============================================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "[1/6] Python detected:"
python3 --version
echo ""

# Create virtual environment
echo "[2/6] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
    echo "Virtual environment created successfully"
fi
echo ""

# Activate virtual environment
echo "[3/6] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi
echo ""

# Upgrade pip
echo "[4/6] Upgrading pip..."
pip install --upgrade pip --quiet
echo "pip upgraded"
echo ""

# Install dependencies
echo "[5/6] Installing dependencies (this may take a while)..."
echo "This step might take 5-10 minutes depending on your internet connection"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo ""
    echo "WARNING: Some dependencies failed to install"
    echo "You may need to install system dependencies:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-pyaudio portaudio19-dev"
    echo "  macOS: brew install portaudio"
    echo ""
else
    echo "Dependencies installed successfully"
fi
echo ""

# Create directories
echo "[6/6] Creating required directories..."
mkdir -p data/users/voice_prints
mkdir -p data/transactions
mkdir -p data/metrics
mkdir -p data/models
mkdir -p logs
echo "Directories created"
echo ""

# Copy environment file
if [ ! -f ".env" ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo ".env file created - please edit it with your settings"
else
    echo ".env file already exists"
fi
echo ""

echo "============================================================"
echo "Setup Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "  1. Edit .env file if needed (optional for demo)"
echo "  2. Run test: python test_setup.py"
echo "  3. Run demo: python run_demo.py"
echo "  4. Run full app: python run_whispay.py"
echo ""
echo "Note: To run WhisPay in future sessions:"
echo "  1. Open this folder in terminal"
echo "  2. Run: source venv/bin/activate"
echo "  3. Run: python run_whispay.py"
echo ""
