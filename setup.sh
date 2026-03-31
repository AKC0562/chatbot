#!/bin/bash
# Advanced Chatbot Setup Script for Linux/Mac

echo "============================================"
echo "Nexus AI - Advanced Chatbot Setup"
echo "============================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "[1/4] Python version:"
python3 --version
echo ""

# Create virtual environment
echo "[2/4] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created successfully!"
else
    echo "Virtual environment already exists. Skipping..."
fi
echo ""

# Activate virtual environment and install dependencies
echo "[3/4] Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "Dependencies installed successfully!"
echo ""

# Display next steps
echo "[4/4] Setup Complete!"
echo ""
echo "============================================"
echo "Next Steps:"
echo "============================================"
echo ""
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Start the backend server:"
echo "   python server/app.py"
echo ""
echo "3. Open the frontend in your browser:"
echo "   - Open: client/index.html"
echo "   - Or serve with: python -m http.server 8000 --directory client"
echo ""
echo "4. Access at: http://localhost:8000"
echo ""
echo "============================================"
echo ""
