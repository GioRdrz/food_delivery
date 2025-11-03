#!/bin/bash

################################################################################
# Food Delivery Service API - Run Script
################################################################################
# This script starts the Food Delivery Service API server with hot-reload
# enabled for development. It performs pre-flight checks and provides helpful
# information about the running server.
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_header() {
    echo ""
    echo -e "${CYAN}================================================================================${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}================================================================================${NC}"
    echo ""
}

################################################################################
# Pre-flight Checks
################################################################################
print_header "Food Delivery Service API - Starting Server"

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    print_warning "Virtual environment not activated!"
    print_info "Attempting to activate virtual environment..."

    if [ -d "venv" ]; then
        source venv/bin/activate
        print_success "Virtual environment activated!"
    else
        print_error "Virtual environment not found!"
        echo ""
        echo "Please run the setup script first:"
        echo "  ./setup.sh"
        exit 1
    fi
else
    print_success "Virtual environment is active"
fi
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    print_error ".env file not found!"
    echo ""
    echo "Please run the setup script first:"
    echo "  ./setup.sh"
    echo ""
    echo "Or manually create .env from .env.example:"
    echo "  cp .env.example .env"
    exit 1
fi
print_success ".env file found"
echo ""

# Check if database exists
if [ ! -f "food_delivery.db" ]; then
    print_warning "Database file not found!"
    print_info "Creating database and running migrations..."
    alembic upgrade head
    print_success "Database initialized!"
else
    print_success "Database file found"
fi
echo ""

# Check if uvicorn is installed
if ! command -v uvicorn &> /dev/null; then
    print_error "uvicorn is not installed!"
    echo ""
    echo "Please install dependencies:"
    echo "  pip install -r requirements.txt"
    exit 1
fi
print_success "uvicorn is installed"
echo ""

################################################################################
# Server Information
################################################################################
print_header "Server Information"

echo "🌐 Server will start on:"
echo "   http://localhost:8000"
echo ""
echo "📚 API Documentation:"
echo "   Swagger UI: http://localhost:8000/docs"
echo "   ReDoc:      http://localhost:8000/redoc"
echo ""
echo "🔑 Default Admin Credentials:"
echo "   Email:    admin@fooddelivery.com"
echo "   Password: admin123"
echo ""
echo "💡 Features:"
echo "   • Hot-reload enabled (code changes auto-restart server)"
echo "   • SQLite database (food_delivery.db)"
echo "   • JWT authentication"
echo "   • Role-based access control (Customer, Restaurant Owner, Admin)"
echo ""
echo "🛑 To stop the server:"
echo "   Press Ctrl+C"
echo ""

print_info "Starting server..."
echo ""
echo -e "================================================================================"
echo ""

################################################################################
# Run the Application
################################################################################
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

