# API Documentation

Complete API documentation for the Food Delivery Service.

## Base URL

```
http://localhost:8000
```

## Authentication

All endpoints except `/auth/register` and `/auth/login` require authentication using JWT Bearer tokens.

Include the token in the Authorization header:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

## Response Format

All responses are in JSON format.

### Success Response
```json
{
  "id": 1,
  "field": "value"
}
```

### Error Response
```json
{
  "detail": "Error message"
}
```

## Endpoints

### Authentication

#### Register User
```http
POST /auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe",
  "role": "customer"  // customer, restaurant_owner, admin
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "customer",
  "is_active": true,
  "is_blocked": false
}
```

#### Login
```http
POST /auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### Users

#### Get Current User
```http
GET /users/me
```

**Headers:** `Authorization: Bearer TOKEN`

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "customer",
  "is_active": true,
  "is_blocked": false
}
```

#### List All Users (Admin Only)
```http
GET /users/?skip=0&limit=100
```

**Headers:** `Authorization: Bearer ADMIN_TOKEN`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "customer",
    "is_active": true,
    "is_blocked": false
  }
]
```

#### Update User (Admin Only)
```http
PUT /users/{user_id}
```

**Headers:** `Authorization: Bearer ADMIN_TOKEN`

**Request Body:**
```json
{
  "email": "newemail@example.com",
  "full_name": "New Name",
  "is_blocked": true
}
```

**Response:** `200 OK`

---

### Restaurants

#### List Restaurants
```http
GET /restaurants/?skip=0&limit=100&include_blocked=false
```

**Headers:** `Authorization: Bearer TOKEN`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Italian Delight",
    "description": "Authentic Italian cuisine",
    "owner_id": 2,
    "is_blocked": false
  }
]
```

#### Get Restaurant
```http
GET /restaurants/{restaurant_id}
```

**Headers:** `Authorization: Bearer TOKEN`

**Response:** `200 OK`

#### Create Restaurant
```http
POST /restaurants/
```

**Headers:** `Authorization: Bearer OWNER_TOKEN`

**Request Body:**
```json
{
  "name": "Italian Delight",
  "description": "Authentic Italian cuisine"
}
```

**Response:** `201 Created`

#### Update Restaurant
```http
PUT /restaurants/{restaurant_id}
```

**Headers:** `Authorization: Bearer OWNER_TOKEN`

**Request Body:**
```json
{
  "name": "Updated Name",
  "description": "Updated description",
  "is_blocked": false
}
```

**Response:** `200 OK`

#### Delete Restaurant
```http
DELETE /restaurants/{restaurant_id}
```

**Headers:** `Authorization: Bearer OWNER_TOKEN`

**Response:** `204 No Content`

---

### Meals

#### List Meals
```http
GET /meals/?skip=0&limit=100&include_blocked=false
```

**Headers:** `Authorization: Bearer TOKEN`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Margherita Pizza",
    "description": "Classic pizza",
    "price": "12.99",
    "restaurant_id": 1,
    "is_blocked": false
  }
]
```

#### List Meals by Restaurant
```http
GET /meals/restaurant/{restaurant_id}
```

**Headers:** `Authorization: Bearer TOKEN`

**Response:** `200 OK`

#### Create Meal
```http
POST /meals/
```

**Headers:** `Authorization: Bearer OWNER_TOKEN`

**Request Body:**
```json
{
  "name": "Margherita Pizza",
  "description": "Classic pizza with tomato and mozzarella",
  "price": "12.99",
  "restaurant_id": 1
}
```

**Response:** `201 Created`

#### Update Meal
```http
PUT /meals/{meal_id}
```

**Headers:** `Authorization: Bearer OWNER_TOKEN`

**Request Body:**
```json
{
  "name": "Updated Pizza",
  "price": "13.99",
  "is_blocked": false
}
```

**Response:** `200 OK`

---

### Orders

#### List Orders
```http
GET /orders/?skip=0&limit=100
```

**Headers:** `Authorization: Bearer TOKEN`

**Response:** `200 OK`
- Customers see their own orders
- Restaurant owners see orders for their restaurants
- Admins see all orders

#### Get My Orders (Customer)
```http
GET /orders/my-orders
```

**Headers:** `Authorization: Bearer CUSTOMER_TOKEN`

**Response:** `200 OK`

#### Get Restaurant Orders
```http
GET /orders/restaurant/{restaurant_id}
```

**Headers:** `Authorization: Bearer OWNER_TOKEN`

**Response:** `200 OK`

#### Create Order
```http
POST /orders/
```

**Headers:** `Authorization: Bearer CUSTOMER_TOKEN`

**Request Body:**
```json
{
  "restaurant_id": 1,
  "items": [
    {
      "meal_id": 1,
      "quantity": 2
    },
    {
      "meal_id": 2,
      "quantity": 1
    }
  ],
  "tip_amount": "5.00",
  "coupon_code": "SAVE10"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "customer_id": 1,
  "restaurant_id": 1,
  "status": "placed",
  "total_amount": "39.48",
  "tip_amount": "5.00",
  "coupon_id": 1,
  "created_at": "2024-01-01T12:00:00",
  "items": [
    {
      "id": 1,
      "meal_id": 1,
      "quantity": 2,
      "price_at_order": "12.99"
    }
  ],
  "status_history": [
    {
      "id": 1,
      "status": "placed",
      "changed_at": "2024-01-01T12:00:00",
      "changed_by_user_id": 1
    }
  ]
}
```

#### Update Order Status
```http
PATCH /orders/{order_id}/status
```

**Headers:** `Authorization: Bearer TOKEN`

**Request Body:**
```json
{
  "status": "processing"
}
```

**Valid Status Transitions:**
- `placed` → `canceled` (customer or owner)
- `placed` → `processing` (owner)
- `processing` → `canceled` (owner)
- `processing` → `in_route` (owner)
- `in_route` → `delivered` (owner)
- `delivered` → `received` (customer)

**Response:** `200 OK`

---

### Coupons (Admin Only)

#### List Coupons
```http
GET /coupons/?skip=0&limit=100
```

**Headers:** `Authorization: Bearer ADMIN_TOKEN`

**Response:** `200 OK`

#### Create Coupon
```http
POST /coupons/
```

**Headers:** `Authorization: Bearer ADMIN_TOKEN`

**Request Body:**
```json
{
  "code": "SAVE10",
  "discount_percentage": "10.00"
}
```

**Response:** `201 Created`

#### Update Coupon
```http
PUT /coupons/{coupon_id}
```

**Headers:** `Authorization: Bearer ADMIN_TOKEN`

**Request Body:**
```json
{
  "code": "SAVE20",
  "discount_percentage": "20.00",
  "is_active": true
}
```

**Response:** `200 OK`

---

## Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Request successful, no content to return
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required or failed
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error

## Error Codes

Common error responses:

### Authentication Error
```json
{
  "detail": "Could not validate credentials"
}
```

### Permission Error
```json
{
  "detail": "Not enough permissions"
}
```

### Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Resource Not Found
```json
{
  "detail": "Restaurant not found"
}
```

