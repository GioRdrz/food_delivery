# Food Delivery Service API

A comprehensive food delivery service REST API built with FastAPI, featuring user authentication, restaurant management, meal ordering, and order tracking with status history.

## Features

- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control**: Three user roles (Customer, Restaurant Owner, Admin)
- **UUID Primary Keys**: All entities use UUID for enhanced security and scalability
- **Restaurant Management**: CRUD operations for restaurants
- **Meal Management**: CRUD operations for meals
- **Order Processing**: Complete order workflow with status tracking
- **Coupon System**: Percentage-based discount coupons
- **Order Status History**: Track all status changes with timestamps
- **Blocking System**: Admins can block users, restaurants, and meals
- **API Documentation**: Auto-generated OpenAPI/Swagger docs

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Validation**: Pydantic v2 with ConfigDict
- **Testing**: pytest
- **Logging**: Structured logging with file and console output

## Project Structure

```
food_delivery/
├── app/
│   ├── core/
│   │   └── security.py          # JWT and password utilities
│   ├── models/
│   │   ├── user.py              # User model
│   │   ├── restaurant.py        # Restaurant model
│   │   ├── meal.py              # Meal model
│   │   ├── order.py             # Order, OrderItem, OrderStatusHistory models
│   │   └── coupon.py            # Coupon model
│   ├── routers/
│   │   ├── auth.py              # Authentication endpoints
│   │   ├── users.py             # User management endpoints
│   │   ├── restaurants.py       # Restaurant endpoints
│   │   ├── meals.py             # Meal endpoints
│   │   ├── orders.py            # Order endpoints
│   │   └── coupons.py           # Coupon endpoints
│   ├── schemas/
│   │   └── ...                  # Pydantic schemas for validation
│   ├── services/
│   │   ├── user_service.py      # User business logic
│   │   ├── restaurant_service.py
│   │   ├── meal_service.py
│   │   ├── order_service.py
│   │   └── coupon_service.py
│   ├── config.py                # Settings management
│   ├── database.py              # Database configuration
│   ├── dependencies.py          # Dependency injection
│   └── main.py                  # FastAPI application
├── alembic/                     # Database migrations
├── tests/                       # Test suite
├── .env                         # Environment variables
├── requirements.txt             # Python dependencies
├── curl_collection.sh           # cURL commands for testing
└── README.md
```

## Installation

### Prerequisites

- Python 3.9+
- PostgreSQL 12+ (or Docker for easy setup)

### Setup

#### Option 1: Using Docker for PostgreSQL (Recommended)

1. **Start PostgreSQL with Docker Compose**
   ```bash
   docker-compose up -d
   ```

   This will start a PostgreSQL instance on port 5432 with the default credentials.

#### Option 2: Using Local PostgreSQL

If you prefer to use a local PostgreSQL installation, make sure it's running and create the database manually.

### Application Setup

1. **Clone the repository**
   ```bash
   cd food_delivery
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and configure your database and settings:
   ```
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/food_delivery
   SECRET_KEY=your-secret-key-here-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ADMIN_EMAIL=admin@fooddelivery.com
   ADMIN_PASSWORD=admin123
   ```

5. **Create database**
   ```bash
   createdb food_delivery
   ```

6. **Run migrations**
   ```bash
   alembic upgrade head
   ```

   > **Note**: The database uses UUID primary keys. See [UUID_MIGRATION.md](UUID_MIGRATION.md) for details.

## Running the Application

### Using Makefile (Recommended)

```bash
# See all available commands
make help

# Start PostgreSQL
make db-start

# Run migrations
make migrate

# Start development server
make run

# Run tests
make test
```

### Manual Commands

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## User Roles and Permissions

### Customer
- Register and login
- View all restaurants and meals
- Place orders
- View order history
- Cancel orders (only in PLACED status)
- Mark orders as RECEIVED

### Restaurant Owner
- All customer permissions
- Create, update, delete own restaurants
- Create, update, delete meals for own restaurants
- View orders for own restaurants
- Update order status (PROCESSING, IN_ROUTE, DELIVERED, CANCELED)

### Administrator
- All permissions
- CRUD operations on all users, restaurants, and meals
- Block/unblock users, restaurants, and meals
- View all orders
- Cannot be deleted (built-in admin account)

## Order Status Workflow

```
PLACED → CANCELED (by customer or owner)
PLACED → PROCESSING (by owner)
PROCESSING → CANCELED (by owner)
PROCESSING → IN_ROUTE (by owner)
IN_ROUTE → DELIVERED (by owner)
DELIVERED → RECEIVED (by customer)
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token

### Users
- `GET /users/me` - Get current user info
- `GET /users/` - List all users (admin only)
- `GET /users/{user_id}` - Get user by ID (admin only)
- `POST /users/` - Create user (admin only)
- `PUT /users/{user_id}` - Update user (admin only)
- `DELETE /users/{user_id}` - Delete user (admin only)

### Restaurants
- `GET /restaurants/` - List all restaurants
- `GET /restaurants/my-restaurants` - List own restaurants
- `GET /restaurants/{restaurant_id}` - Get restaurant details
- `POST /restaurants/` - Create restaurant
- `PUT /restaurants/{restaurant_id}` - Update restaurant
- `DELETE /restaurants/{restaurant_id}` - Delete restaurant

### Meals
- `GET /meals/` - List all meals
- `GET /meals/restaurant/{restaurant_id}` - List meals by restaurant
- `GET /meals/{meal_id}` - Get meal details
- `POST /meals/` - Create meal
- `PUT /meals/{meal_id}` - Update meal
- `DELETE /meals/{meal_id}` - Delete meal

### Orders
- `GET /orders/` - List orders (filtered by role)
- `GET /orders/my-orders` - List customer's orders
- `GET /orders/restaurant/{restaurant_id}` - List restaurant's orders
- `GET /orders/{order_id}` - Get order details
- `POST /orders/` - Create order
- `PATCH /orders/{order_id}/status` - Update order status
- `DELETE /orders/{order_id}` - Delete order (admin only)

### Coupons
- `GET /coupons/` - List all coupons (admin only)
- `GET /coupons/{coupon_id}` - Get coupon details (admin only)
- `POST /coupons/` - Create coupon (admin only)
- `PUT /coupons/{coupon_id}` - Update coupon (admin only)
- `DELETE /coupons/{coupon_id}` - Delete coupon (admin only)

## Testing

### Run all tests
```bash
pytest
```

### Run with coverage
```bash
pytest --cov=app tests/
```

### Run specific test file
```bash
pytest tests/test_auth.py
```

## cURL Collection

A comprehensive cURL collection is provided in `curl_collection.sh`. Make the script executable and run it:

```bash
chmod +x curl_collection.sh
./curl_collection.sh
```

This script demonstrates:
- User registration and authentication
- Restaurant and meal creation
- Order placement with coupons
- Order status updates through the complete workflow
- Admin operations

## Example Usage

### 1. Register and Login

```bash
# Register as customer
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "password": "password123",
    "role": "customer"
  }'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "password": "password123"
  }'
```

### 2. Create Restaurant (as owner)

```bash
curl -X POST "http://localhost:8000/restaurants/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Italian Restaurant",
    "description": "Authentic Italian cuisine"
  }'
```

### 3. Place Order (as customer)

```bash
curl -X POST "http://localhost:8000/orders/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "restaurant_id": 1,
    "items": [
      {"meal_id": 1, "quantity": 2},
      {"meal_id": 2, "quantity": 1}
    ],
    "tip_amount": "5.00",
    "coupon_code": "SAVE10"
  }'
```

## Default Admin Account

The application creates a built-in admin account on startup:
- **Email**: admin@fooddelivery.com (configurable in .env)
- **Password**: admin123 (configurable in .env)

**Important**: Change these credentials in production!

## Logging

The application includes comprehensive logging throughout all services and routers.

### Log Configuration

Configure logging via environment variables in `.env`:

```
LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Log Output

- **Console**: Colored output for easy reading during development
- **File**: Detailed logs saved to `logs/app.log`

### Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages (default)
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failures
- **CRITICAL**: Critical issues requiring immediate attention

### Log Files

Logs are stored in the `logs/` directory:
- `logs/app.log` - Main application log file

Log files are automatically created on startup and are excluded from version control.

## License

MIT

