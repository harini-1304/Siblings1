#!/bin/bash
# ProConnect Backend Setup Script for macOS/Linux

echo ""
echo "============================================================"
echo "     ProConnect Backend Setup"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher from https://www.python.org"
    exit 1
fi

echo "Step 1: Creating Virtual Environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "Step 2: Activating Virtual Environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

echo ""
echo "Step 3: Installing Dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"

echo ""
echo "Step 4: Checking Environment Configuration..."
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found"
    echo "Please create .env file with your MongoDB credentials"
else
    echo "✓ .env file found"
fi

echo ""
echo "============================================================"
echo "Setup Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "   1. Update .env file with your MongoDB connection string"
echo "   2. Run: python app.py"
echo ""
echo "MongoDB Connection String should look like:"
echo "mongodb+srv://username:password@cluster.mongodb.net/?appName=Cluster0"
echo ""
