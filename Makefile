.PHONY: help setup install db-start db-stop db-create migrate run test test-cov clean curl-test

help:
	@echo "Food Delivery Service API - Available Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup        - Complete setup (venv, install, env file)"
	@echo "  make install      - Install Python dependencies"
	@echo ""
	@echo "Database:"
	@echo "  make db-start     - Start PostgreSQL with Docker"
	@echo "  make db-stop      - Stop PostgreSQL container"
	@echo "  make db-create    - Create database"
	@echo "  make migrate      - Run database migrations"
	@echo ""
	@echo "Development:"
	@echo "  make run          - Start development server"
	@echo "  make test         - Run tests"
	@echo "  make test-cov     - Run tests with coverage"
	@echo "  make curl-test    - Run cURL test collection"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        - Remove cache and temp files"

setup:
	@echo "Setting up Food Delivery Service API..."
	python3 -m venv venv
	@echo "Virtual environment created!"
	@echo "Activate it with: source venv/bin/activate"
	@echo "Then run: make install"

install:
	pip install --upgrade pip
	pip install -r requirements.txt
	@if [ ! -f .env ]; then cp .env.example .env; echo ".env file created!"; fi
	@echo "Installation complete!"

db-start:
	@echo "Starting PostgreSQL with Docker..."
	docker-compose up -d
	@echo "PostgreSQL is running on port 5432"

db-stop:
	@echo "Stopping PostgreSQL..."
	docker-compose down
	@echo "PostgreSQL stopped"

db-create:
	@echo "Creating database..."
	createdb food_delivery || echo "Database may already exist"

migrate:
	@echo "Running database migrations..."
	alembic revision --autogenerate -m "Auto migration"
	alembic upgrade head
	@echo "Migrations complete!"

run:
	@echo "Starting development server..."
	uvicorn app.main:app --reload

test:
	@echo "Running tests..."
	pytest -v

test-cov:
	@echo "Running tests with coverage..."
	pytest --cov=app --cov-report=html --cov-report=term tests/
	@echo "Coverage report generated in htmlcov/index.html"

curl-test:
	@echo "Running cURL test collection..."
	@chmod +x curl_collection.sh
	./curl_collection.sh

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage
	@echo "Cleanup complete!"

