# Quick Start Guide

This guide will help you get the Food Delivery Service API up and running in minutes.

## Prerequisites

- Python 3.9 or higher
- PostgreSQL 12 or higher
- Git (optional)

## Step 1: Setup

Run the setup script to create a virtual environment and install dependencies:

```bash
chmod +x setup.sh
./setup.sh
```

Or manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Step 2: Configure Environment

Edit the `.env` file with your database credentials:

```bash
nano .env  # or use your preferred editor
```

Update the `DATABASE_URL`:
```
DATABASE_URL=postgresql://YOUR_USER:YOUR_PASSWORD@localhost:5432/food_delivery
```

## Step 3: Create Database

```bash
createdb food_delivery
```

Or using psql:
```bash
psql -U postgres
CREATE DATABASE food_delivery;
\q
```

## Step 4: Run Migrations

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Step 5: Start the Server

```bash
./run.sh
```

Or manually:
```bash
uvicorn app.main:app --reload
```

The API will be available at: **http://localhost:8000**

## Step 6: Explore the API

### Option 1: Interactive API Documentation

Open your browser and visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Option 2: Use the cURL Collection

```bash
./curl_collection.sh
```

### Option 3: Manual Testing

1. **Login as Admin** (default credentials):
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@fooddelivery.com",
    "password": "admin123"
  }'
```

2. **Register a Customer**:
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "password": "password123",
    "full_name": "John Doe",
    "role": "customer"
  }'
```

3. **Register a Restaurant Owner**:
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "owner@example.com",
    "password": "password123",
    "full_name": "Jane Smith",
    "role": "restaurant_owner"
  }'
```

## Step 7: Run Tests

```bash
pytest
```

For coverage report:
```bash
pytest --cov=app tests/
```

## Common Issues

### Database Connection Error

If you get a database connection error:
1. Make sure PostgreSQL is running: `sudo systemctl status postgresql`
2. Check your DATABASE_URL in `.env`
3. Verify database exists: `psql -l`

### Import Errors

Make sure you're in the virtual environment:
```bash
source venv/bin/activate
```

### Port Already in Use

If port 8000 is already in use, specify a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

## What's Next?

- Read the full [README.md](README.md) for detailed documentation
- Explore the API endpoints in the Swagger UI
- Check out the test files in `tests/` for usage examples
- Review the architecture in `app/` directory

## Default Accounts

The application creates a default admin account:
- **Email**: admin@fooddelivery.com
- **Password**: admin123

**⚠️ Important**: Change these credentials in production!

## Project Structure Overview

```
food_delivery/
├── app/                    # Application code
│   ├── routers/           # API endpoints
│   ├── services/          # Business logic
│   ├── models/            # Database models
│   └── schemas/           # Pydantic schemas
├── tests/                 # Test suite
├── alembic/              # Database migrations
└── curl_collection.sh    # API testing script
```

## Support

For issues or questions, please refer to the [README.md](README.md) file.

