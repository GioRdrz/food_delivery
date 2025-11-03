#!/bin/bash

################################################################################
# Food Delivery Service API - Setup Script
################################################################################
# This script sets up the development environment for the Food Delivery API.
# It creates a virtual environment, installs dependencies, configures the
# database, and prepares the application for first run.
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo "================================================================================"
    echo "  $1"
    echo "================================================================================"
    echo ""
}

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

print_header "Food Delivery Service API - Setup"

################################################################################
# Step 1: Check Python Version
################################################################################
print_info "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed!"
    exit 1
fi

python_version=$(python3 --version 2>&1 | awk '{print $2}')
print_success "Python version: $python_version"
echo ""

################################################################################
# Step 2: Create Virtual Environment
################################################################################
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists, skipping creation..."
else
    print_info "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created!"
fi
echo ""

################################################################################
# Step 3: Activate Virtual Environment and Install Dependencies
################################################################################
print_info "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated!"
echo ""

print_info "Upgrading pip..."
pip install --upgrade pip --quiet
print_success "Pip upgraded!"
echo ""

print_info "Installing dependencies from requirements.txt..."
pip install -r requirements.txt --quiet
print_success "Dependencies installed!"
echo ""

################################################################################
# Step 4: Create .env File
################################################################################
if [ ! -f .env ]; then
    print_info "Creating .env file from .env.example..."
    cp .env.example .env
    print_success ".env file created!"
    print_warning "You can edit .env to customize settings (optional for SQLite)"
else
    print_warning ".env file already exists, skipping..."
fi
echo ""

################################################################################
# Step 5: Initialize Database
################################################################################
print_info "Initializing SQLite database..."

# Remove old database if exists (for clean setup)
if [ -f "food_delivery.db" ]; then
    print_warning "Existing database found. Removing for clean setup..."
    rm -f food_delivery.db
fi

# Run migrations
print_info "Running database migrations..."
alembic upgrade head
print_success "Database initialized and migrations applied!"
echo ""

################################################################################
# Step 6: Make Scripts Executable
################################################################################
print_info "Making scripts executable..."
chmod +x run.sh
chmod +x seed_data_api.sh
print_success "Scripts are now executable!"
echo ""

################################################################################
# Step 7: Test Database Connection
################################################################################
print_info "Testing database connection..."
python3 -c "
from app.database import SessionLocal, engine
from app.models.user import User

try:
    db = SessionLocal()
    # Try to query users (should work even if empty)
    users = db.query(User).count()
    print(f'✅ Database connection successful! Found {users} users.')
    db.close()
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    exit(1)
"
echo ""

################################################################################
# Summary
################################################################################
print_header "Setup Complete!"

print_success "Your Food Delivery Service API is ready to use!"
echo ""
echo "📊 What was set up:"
echo "  • Python virtual environment (venv/)"
echo "  • All Python dependencies installed"
echo "  • SQLite database (food_delivery.db)"
echo "  • Database migrations applied"
echo "  • Configuration file (.env)"
echo ""
echo "🚀 Next Steps:"
echo ""
echo "1. Start the API server:"
echo "   ./run.sh"
echo ""
echo "2. Populate with test data (optional):"
echo "   ./seed_data_api.sh"
echo "   Note: Make sure the API server is running first!"
echo ""
echo "3. Access the API documentation:"
echo "   http://localhost:8000/docs (Swagger UI)"
echo "   http://localhost:8000/redoc$ (ReDoc)"
echo ""
echo "4. Default admin credentials:"
echo "   Email:    admin@fooddelivery.com"
echo "   Password: admin123"
echo ""
echo "💡 Tips:"
echo "  • To activate the virtual environment manually:"
echo "    source venv/bin/activate"
echo ""
echo "  • To run tests:"
echo "    pytest"
echo ""
echo "  • To view logs, check the console output when running ./run.sh"
echo ""
print_success "Happy coding! 🎉"
echo ""

