#!/bin/bash

# Script to run the Food Delivery Service API

echo "Starting Food Delivery Service API..."
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "Warning: Virtual environment not activated!"
    echo "Please run: source venv/bin/activate"
    echo ""
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please copy .env.example to .env and configure it."
    exit 1
fi

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

