# Food Delivery Service API

A comprehensive food delivery service REST API built with FastAPI, featuring user authentication, restaurant management, meal ordering, and order tracking with status history.

## Features

### Core Functionality
- 🔐 **JWT Authentication**: Secure token-based authentication with password hashing
- 👥 **Role-Based Access Control**: Three user roles (Customer, Restaurant Owner, Admin)
- 🏪 **Restaurant Management**: Full CRUD operations for restaurants
- 🍕 **Meal Management**: Full CRUD operations for meals with restaurant association
- 📦 **Order Processing**: Complete order workflow with status tracking
- 🎟️ **Coupon System**: Percentage-based discount coupons with validation
- 📊 **Order Status History**: Automatic tracking of all status changes with timestamps
- 🚫 **Blocking System**: Admins can block/unblock users, restaurants, and meals
- 📝 **Comprehensive Logging**: Structured logging with file and console output

### Technical Features
- 🆔 **UUID Primary Keys**: All entities use UUID for enhanced security and scalability
- 💾 **SQLite Database**: File-based database with no external dependencies
- 🔄 **Database Migrations**: Alembic migrations with batch mode for SQLite
- 📚 **API Documentation**: Auto-generated OpenAPI/Swagger and ReDoc documentation
- ✅ **Input Validation**: Pydantic v2 schemas for request/response validation
- 🧪 **Test Suite**: Comprehensive pytest test coverage
- 🚀 **Hot Reload**: Development server with automatic code reload
- 🎨 **Clean Architecture**: Separation of concerns with routers, services, and models

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (file-based, no external database required)
- **ORM**: SQLAlchemy with native Uuid type (CHAR(32) in SQLite, UUID in PostgreSQL)
- **Migrations**: Alembic with batch mode for SQLite
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
├── logs/                        # Application logs
├── .env                         # Environment variables
├── .env.example                 # Environment template
├── requirements.txt             # Python dependencies
├── setup.sh                     # Automated setup script
├── run.sh                       # Server startup script
├── seed_data_api.sh             # API-based test data seeding
├── Food_Delivery_API.postman_collection.json  # Postman collection (59 requests)
├── food_delivery.db             # SQLite database (created after setup)
└── README.md
```

## Installation

### Prerequisites

- Python 3.9+
- No external database required! (Uses SQLite)

### Quick Start (Recommended)

Run the automated setup script:

```bash
chmod +x setup.sh
./setup.sh
```

This script will:
- ✅ Create a Python virtual environment
- ✅ Install all dependencies
- ✅ Create the `.env` configuration file
- ✅ Initialize the SQLite database
- ✅ Run database migrations
- ✅ Test the database connection
- ✅ Make all scripts executable

Then start the server:

```bash
./run.sh
```

The server will start with:
- 🌐 API: `http://localhost:8000`
- 📚 Swagger UI: `http://localhost:8000/docs`
- 📚 ReDoc: `http://localhost:8000/redoc`
- 🔑 Admin: `admin@fooddelivery.com` / `admin123`

### Manual Setup

If you prefer manual installation:

1. **Clone the repository**
   ```bash
   cd food_delivery
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
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

   The default `.env` configuration uses SQLite (no changes needed):
   ```
   DATABASE_URL=sqlite:///./food_delivery.db
   SECRET_KEY=your-secret-key-here-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ADMIN_EMAIL=admin@fooddelivery.com
   ADMIN_PASSWORD=admin123
   LOG_LEVEL=INFO
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

   This will create the SQLite database file (`food_delivery.db`) with all tables.

   > **Note**: The database uses UUID primary keys stored as CHAR(32) (hex format without hyphens) in SQLite for efficiency.

6. **Start the development server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`

## Populating Test Data

To populate the database with comprehensive test data for development and testing:

```bash
# Make sure the API server is running first
./run.sh

# In another terminal, run the seed script
./seed_data_api.sh
```

### What the Seed Script Does

The `seed_data_api.sh` script demonstrates **real-world API usage** by making HTTP requests to all endpoints:

**Step 1: User Registration & Authentication**
- Creates 4 users (2 customers, 2 restaurant owners)
- Each user registers and authenticates with their own credentials
- Demonstrates proper JWT token-based authentication

**Step 2: Restaurant & Meal Creation**
- Restaurant owners create their own restaurants
- Each restaurant gets 3 different meals
- Demonstrates owner-specific resource creation

**Step 3: Coupon Creation**
- Admin creates a 10% discount coupon (code: WELCOME10)
- Demonstrates admin-only operations

**Step 4: Order Placement & Status Updates**
- Customer 1 places 2 orders (one with coupon, one without)
- Customer 2 places 1 order
- Orders progress through different statuses (PLACED → PROCESSING → IN_ROUTE → DELIVERED → RECEIVED)
- Demonstrates complete order lifecycle

**Step 5: Order Viewing by Role**
- Shows orders filtered by restaurant owner
- Shows orders filtered by customer
- Demonstrates role-based data access

**Step 6: Order Status History**
- Displays complete status change history for each order
- Shows timestamps for all status transitions

**Step 7: Admin Capabilities Demonstration**
- **User Management**: List, create, block/unblock, delete users
- **Restaurant Management**: Block/unblock restaurants
- **Meal Management**: Block/unblock meals
- **Order Management**: View all orders and status history
- **Coupon Management**: Update coupon discount percentage
- Demonstrates full admin CRUD operations

### Test Data Created

After running the seed script, you'll have:

- **Users**: 5 total (1 admin + 2 customers + 2 restaurant owners)
- **Restaurants**: 2 (Bella Italia, Dragon Wok)
- **Meals**: 6 total (3 per restaurant)
- **Coupons**: 1 (WELCOME10 - 15% discount after admin update)
- **Orders**: 3 with different statuses
- **Order Status History**: Complete audit trail for all orders

### Test Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@fooddelivery.com | admin123 |
| Customer 1 | customer1@example.com | password123 |
| Customer 2 | customer2@example.com | password123 |
| Owner 1 | owner1@example.com | password123 |
| Owner 2 | owner2@example.com | password123 |

### Prerequisites for Seed Script

The seed script requires:
- ✅ API server running on `http://localhost:8000`
- ✅ `jq` installed for JSON parsing (`sudo apt install jq` on Ubuntu/Debian)
- ✅ `curl` installed (usually pre-installed)

**Alternative**: Use the **Postman Collection** (`Food_Delivery_API.postman_collection.json`) for a GUI-based approach to testing the API. See the [API Documentation](#api-documentation) section for details.

## API Documentation

Once the server is running, you can access interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
  - Interactive API explorer
  - Try out endpoints directly from the browser
  - See request/response schemas

- **ReDoc**: http://localhost:8000/redoc
  - Clean, readable API documentation
  - Better for reading and understanding the API structure

### Postman Collection

A comprehensive **Postman Collection** is included for easy API testing and exploration:

📁 **File**: `Food_Delivery_API.postman_collection.json`

**Features**:
- ✅ **59 API requests** organized into 8 logical folders
- ✅ **Automatic token management** - Test scripts extract and save JWT tokens
- ✅ **Automatic ID management** - Saves resource IDs for subsequent requests
- ✅ **Complete workflow coverage** - From user registration to order delivery
- ✅ **Role-based testing** - Demonstrates customer, owner, and admin capabilities
- ✅ **Admin operations** - Full CRUD and blocking/unblocking features

**Collection Structure**:
1. **Authentication** (9 requests) - User registration and login for all roles
2. **Coupons (Admin)** (4 requests) - Coupon creation and management
3. **Restaurants** (5 requests) - Restaurant CRUD operations
4. **Meals** (7 requests) - Meal management by restaurant owners
5. **Orders** (9 requests) - Complete order lifecycle from creation to delivery
6. **Users (Admin)** (7 requests) - User management and blocking
7. **Admin Operations** (10 requests) - Blocking/unblocking resources, deletions

**How to Use**:
1. Import the collection into Postman:
   - `File → Import → Upload Files → Select Food_Delivery_API.postman_collection.json`
2. Set the `base_url` collection variable to `http://localhost:8000`
3. Run requests sequentially from top to bottom (or use Collection Runner)
4. Tokens and IDs are automatically saved and reused across requests

**Collection Variables** (auto-populated by test scripts):
- `base_url` - API base URL
- `admin_token`, `customer1_token`, `customer2_token`, `owner1_token`, `owner2_token`
- `restaurant1_id`, `restaurant2_id`
- `meal1_1_id`, `meal1_2_id`, `meal2_1_id`
- `order1_id`, `order2_id`
- `coupon_id`, `test_user_id`

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
- All permissions from Customer and Restaurant Owner roles
- **User Management**: CRUD operations on all users
- **Restaurant Management**: CRUD operations on all restaurants
- **Meal Management**: CRUD operations on all meals
- **Blocking System**: Block/unblock users, restaurants, and meals
- **Order Management**: View all orders in the system
- **Coupon Management**: Full CRUD operations on coupons
- **Protected**: Built-in admin account cannot be deleted

## Database Schema

The application uses SQLite with the following main entities:

### Tables

**users**
- `id` (UUID, Primary Key)
- `email` (String, Unique)
- `hashed_password` (String)
- `full_name` (String)
- `role` (Enum: customer, restaurant_owner, admin)
- `is_active` (Boolean)
- `is_blocked` (Boolean)
- `created_at` (DateTime)

**restaurants**
- `id` (UUID, Primary Key)
- `name` (String)
- `description` (String, Optional)
- `owner_id` (UUID, Foreign Key → users.id)
- `is_blocked` (Boolean)
- `created_at` (DateTime)

**meals**
- `id` (UUID, Primary Key)
- `name` (String)
- `description` (String, Optional)
- `price` (Decimal)
- `restaurant_id` (UUID, Foreign Key → restaurants.id)
- `is_blocked` (Boolean)
- `created_at` (DateTime)

**orders**
- `id` (UUID, Primary Key)
- `customer_id` (UUID, Foreign Key → users.id)
- `restaurant_id` (UUID, Foreign Key → restaurants.id)
- `status` (Enum: placed, processing, in_route, delivered, received, canceled)
- `subtotal` (Decimal)
- `discount_amount` (Decimal)
- `tip_amount` (Decimal)
- `total_amount` (Decimal)
- `delivery_address` (String)
- `coupon_id` (UUID, Foreign Key → coupons.id, Optional)
- `created_at` (DateTime)
- `updated_at` (DateTime)

**order_items**
- `id` (UUID, Primary Key)
- `order_id` (UUID, Foreign Key → orders.id)
- `meal_id` (UUID, Foreign Key → meals.id)
- `quantity` (Integer)
- `price_at_time` (Decimal)

**order_status_history**
- `id` (UUID, Primary Key)
- `order_id` (UUID, Foreign Key → orders.id)
- `status` (Enum: placed, processing, in_route, delivered, received, canceled)
- `changed_at` (DateTime)

**coupons**
- `id` (UUID, Primary Key)
- `code` (String, Unique)
- `discount_percentage` (Decimal)
- `is_active` (Boolean)
- `created_at` (DateTime)

### Relationships

- **User → Restaurants**: One-to-Many (owner_id)
- **Restaurant → Meals**: One-to-Many (restaurant_id)
- **User → Orders**: One-to-Many (customer_id)
- **Restaurant → Orders**: One-to-Many (restaurant_id)
- **Order → OrderItems**: One-to-Many (order_id)
- **Meal → OrderItems**: One-to-Many (meal_id)
- **Order → OrderStatusHistory**: One-to-Many (order_id)
- **Coupon → Orders**: One-to-Many (coupon_id)

> **Note**: UUIDs are stored as CHAR(32) in hex format (without hyphens) in SQLite for efficiency.

## Order Status Workflow

```
PLACED → CANCELED (by customer or owner)
PLACED → PROCESSING (by owner)
PROCESSING → CANCELED (by owner)
PROCESSING → IN_ROUTE (by owner)
IN_ROUTE → DELIVERED (by owner)
DELIVERED → RECEIVED (by customer)
```

**Status Descriptions:**
- **PLACED**: Order has been created and is awaiting restaurant confirmation
- **PROCESSING**: Restaurant is preparing the order
- **IN_ROUTE**: Order is out for delivery
- **DELIVERED**: Order has been delivered to the customer
- **RECEIVED**: Customer has confirmed receipt of the order
- **CANCELED**: Order has been canceled (by customer or restaurant)

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

The project includes a comprehensive test suite covering all major functionality.

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

### Test Coverage

The test suite covers:
- ✅ Authentication (registration, login, JWT tokens)
- ✅ User management (CRUD, permissions)
- ✅ Restaurant operations (CRUD, ownership)
- ✅ Meal operations (CRUD, restaurant association)
- ✅ Order workflow (creation, status updates, history)
- ✅ Coupon system (validation, discount calculation)
- ✅ Role-based access control (all three roles)
- ✅ Blocking system (users, restaurants, meals)

## Example API Usage

### 1. Register and Login

```bash
# Register as customer
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "password": "password123",
    "full_name": "John Doe",
    "role": "customer"
  }'

# Login and get JWT token
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "password": "password123"
  }' | jq -r '.access_token')

echo "Token: $TOKEN"
```

### 2. Create Restaurant (as restaurant owner)

```bash
# First, register as restaurant owner
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "owner@example.com",
    "password": "password123",
    "full_name": "Restaurant Owner",
    "role": "restaurant_owner"
  }'

# Login and get token
OWNER_TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "owner@example.com",
    "password": "password123"
  }' | jq -r '.access_token')

# Create restaurant
RESTAURANT=$(curl -s -X POST "http://localhost:8000/restaurants/" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Italian Restaurant",
    "description": "Authentic Italian cuisine"
  }')

RESTAURANT_ID=$(echo $RESTAURANT | jq -r '.id')
echo "Restaurant ID: $RESTAURANT_ID"
```

### 3. Add Meals to Restaurant

```bash
# Create a meal
MEAL=$(curl -s -X POST "http://localhost:8000/meals/" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Margherita Pizza\",
    \"description\": \"Classic Italian pizza\",
    \"price\": 12.99,
    \"restaurant_id\": \"$RESTAURANT_ID\"
  }")

MEAL_ID=$(echo $MEAL | jq -r '.id')
echo "Meal ID: $MEAL_ID"
```

### 4. Place Order (as customer)

```bash
# Create order with the meal
curl -X POST "http://localhost:8000/orders/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"restaurant_id\": \"$RESTAURANT_ID\",
    \"items\": [
      {\"meal_id\": \"$MEAL_ID\", \"quantity\": 2}
    ],
    \"tip_amount\": 5.00,
    \"delivery_address\": \"123 Main St, City, State 12345\"
  }"
```

### 5. Update Order Status (as restaurant owner)

```bash
# Get the order ID from the previous response, then update status
curl -X PATCH "http://localhost:8000/orders/$ORDER_ID/status" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "processing"
  }'
```

### 6. View Order History

```bash
# Customer views their orders
curl -X GET "http://localhost:8000/orders/my-orders" \
  -H "Authorization: Bearer $TOKEN"

# Restaurant owner views their restaurant's orders
curl -X GET "http://localhost:8000/orders/restaurant/$RESTAURANT_ID" \
  -H "Authorization: Bearer $OWNER_TOKEN"
```

### 7. Admin Operations

```bash
# Login as admin
ADMIN_TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@fooddelivery.com",
    "password": "admin123"
  }' | jq -r '.access_token')

# List all users
curl -X GET "http://localhost:8000/users/" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Block a user
curl -X PUT "http://localhost:8000/users/$USER_ID" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "is_blocked": true
  }'

# View all orders in the system
curl -X GET "http://localhost:8000/orders/" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

> **💡 Tip**: For a complete, working example of all API endpoints, run the `./seed_data_api.sh` script and examine its source code.

## Configuration

### Environment Variables

The application is configured via the `.env` file:

```bash
# Database
DATABASE_URL=sqlite:///./food_delivery.db

# JWT Authentication
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Admin Account
ADMIN_EMAIL=admin@fooddelivery.com
ADMIN_PASSWORD=admin123

# Logging
LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Default Admin Account

The application automatically creates a built-in admin account on startup:
- **Email**: `admin@fooddelivery.com` (configurable via `ADMIN_EMAIL`)
- **Password**: `admin123` (configurable via `ADMIN_PASSWORD`)

⚠️ **Important**: Change these credentials in production by updating the `.env` file!

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

## Troubleshooting

### Server won't start

**Problem**: `ModuleNotFoundError` or import errors

**Solution**: Make sure you've activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

**Problem**: `Database connection failed`

**Solution**: Run database migrations:
```bash
alembic upgrade head
```

---

**Problem**: Port 8000 already in use

**Solution**: Either kill the existing process or use a different port:
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn app.main:app --reload --port 8001
```

### Seed script fails

**Problem**: `jq: command not found`

**Solution**: Install jq:
```bash
# Ubuntu/Debian
sudo apt install jq

# macOS
brew install jq
```

---

**Problem**: `Connection refused` when running seed script

**Solution**: Make sure the API server is running first:
```bash
# Terminal 1
./run.sh

# Terminal 2 (wait for server to start)
./seed_data_api.sh
```

### Authentication issues

**Problem**: `401 Unauthorized` errors

**Solution**: Make sure you're including the JWT token in the Authorization header:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" http://localhost:8000/endpoint
```

---

**Problem**: Token expired

**Solution**: Login again to get a new token. Tokens expire after 30 minutes by default (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES` in `.env`).

### Database issues

**Problem**: Need to reset the database

**Solution**: Delete the database file and run migrations:
```bash
rm -f food_delivery.db
alembic upgrade head
```

---

**Problem**: Migration conflicts

**Solution**: Reset migrations and create a fresh one:
```bash
# Backup your data first!
rm -f food_delivery.db
rm -f alembic/versions/*.py
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Testing issues

**Problem**: Tests fail with database errors

**Solution**: The test suite uses an in-memory SQLite database. Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
pytest
```

## Development Tips

### Viewing the Database

You can inspect the SQLite database using the `sqlite3` command-line tool:

```bash
# Open database
sqlite3 food_delivery.db

# List all tables
.tables

# View users
SELECT id, email, role, is_blocked FROM users;

# View orders with status
SELECT substr(id, 1, 8) as order_id, status, total_amount FROM orders;

# View order status history
SELECT substr(order_id, 1, 8) as order_id, status, changed_at
FROM order_status_history
ORDER BY changed_at;

# Exit
.quit
```

### Making Database Changes

When you modify models:

1. Create a new migration:
   ```bash
   alembic revision --autogenerate -m "Description of changes"
   ```

2. Review the generated migration in `alembic/versions/`

3. Apply the migration:
   ```bash
   alembic upgrade head
   ```

### API Development Workflow

1. Make code changes
2. Server auto-reloads (if using `./run.sh` or `--reload` flag)
3. Test changes via Swagger UI at http://localhost:8000/docs
4. Write/update tests
5. Run tests: `pytest`

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write/update tests
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

MIT

