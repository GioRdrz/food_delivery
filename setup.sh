#!/bin/bash

# Setup script for Food Delivery Service API

echo "=== Food Delivery Service API Setup ==="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
echo "Virtual environment created!"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "Virtual environment activated!"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "Dependencies installed!"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo ".env file created! Please edit it with your database credentials."
else
    echo ".env file already exists."
fi
echo ""

# Make scripts executable
echo "Making scripts executable..."
chmod +x run.sh
chmod +x curl_collection.sh
echo "Scripts are now executable!"
echo ""

echo "=== Setup Complete! ==="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your database credentials"
echo "2. Create PostgreSQL database: createdb food_delivery"
echo "3. Run migrations: alembic revision --autogenerate -m 'Initial migration' && alembic upgrade head"
echo "4. Start the server: ./run.sh"
echo "5. Visit http://localhost:8000/docs for API documentation"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"

