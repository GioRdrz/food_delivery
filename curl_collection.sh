#!/bin/bash

# Food Delivery Service API - cURL Collection
# This script contains example cURL commands to test all API endpoints

BASE_URL="http://localhost:8000"

echo "=== Food Delivery Service API - cURL Collection ==="
echo ""

# Variables to store tokens
ADMIN_TOKEN=""
CUSTOMER_TOKEN=""
OWNER_TOKEN=""

echo "1. Health Check"
curl -X GET "$BASE_URL/health"
echo -e "\n"

echo "2. Register Customer"
curl -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "password": "customer123",
    "full_name": "John Customer",
    "role": "customer"
  }'
echo -e "\n"

echo "3. Register Restaurant Owner"
curl -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "owner@example.com",
    "password": "owner123",
    "full_name": "Jane Owner",
    "role": "restaurant_owner"
  }'
echo -e "\n"

echo "4. Login as Admin (default credentials from .env)"
ADMIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@fooddelivery.com",
    "password": "admin123"
  }')
ADMIN_TOKEN=$(echo $ADMIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
echo $ADMIN_RESPONSE
echo -e "\n"

echo "5. Login as Customer"
CUSTOMER_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "password": "customer123"
  }')
CUSTOMER_TOKEN=$(echo $CUSTOMER_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
echo $CUSTOMER_RESPONSE
echo -e "\n"

echo "6. Login as Restaurant Owner"
OWNER_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "owner@example.com",
    "password": "owner123"
  }')
OWNER_TOKEN=$(echo $OWNER_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
echo $OWNER_RESPONSE
echo -e "\n"

echo "7. Get Current User Info (Customer)"
curl -X GET "$BASE_URL/users/me" \
  -H "Authorization: Bearer $CUSTOMER_TOKEN"
echo -e "\n"

echo "8. Create Restaurant (as Owner)"
RESTAURANT_RESPONSE=$(curl -s -X POST "$BASE_URL/restaurants/" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Italian Delight",
    "description": "Authentic Italian cuisine"
  }')
RESTAURANT_ID=$(echo $RESTAURANT_RESPONSE | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
echo $RESTAURANT_RESPONSE
echo -e "\n"

echo "9. List All Restaurants (as Customer)"
curl -X GET "$BASE_URL/restaurants/" \
  -H "Authorization: Bearer $CUSTOMER_TOKEN"
echo -e "\n"

echo "10. Create Meal (as Owner)"
MEAL1_RESPONSE=$(curl -s -X POST "$BASE_URL/meals/" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Margherita Pizza\",
    \"description\": \"Classic pizza with tomato and mozzarella\",
    \"price\": \"12.99\",
    \"restaurant_id\": $RESTAURANT_ID
  }")
MEAL1_ID=$(echo $MEAL1_RESPONSE | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
echo $MEAL1_RESPONSE
echo -e "\n"

echo "11. Create Another Meal (as Owner)"
MEAL2_RESPONSE=$(curl -s -X POST "$BASE_URL/meals/" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Spaghetti Carbonara\",
    \"description\": \"Creamy pasta with bacon\",
    \"price\": \"14.99\",
    \"restaurant_id\": $RESTAURANT_ID
  }")
MEAL2_ID=$(echo $MEAL2_RESPONSE | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
echo $MEAL2_RESPONSE
echo -e "\n"

echo "12. List Meals by Restaurant"
curl -X GET "$BASE_URL/meals/restaurant/$RESTAURANT_ID" \
  -H "Authorization: Bearer $CUSTOMER_TOKEN"
echo -e "\n"

echo "13. Create Coupon (as Admin)"
COUPON_RESPONSE=$(curl -s -X POST "$BASE_URL/coupons/" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "SAVE10",
    "discount_percentage": "10.00"
  }')
echo $COUPON_RESPONSE
echo -e "\n"

echo "14. Create Order (as Customer)"
ORDER_RESPONSE=$(curl -s -X POST "$BASE_URL/orders/" \
  -H "Authorization: Bearer $CUSTOMER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"restaurant_id\": $RESTAURANT_ID,
    \"items\": [
      {\"meal_id\": $MEAL1_ID, \"quantity\": 2},
      {\"meal_id\": $MEAL2_ID, \"quantity\": 1}
    ],
    \"tip_amount\": \"5.00\",
    \"coupon_code\": \"SAVE10\"
  }")
ORDER_ID=$(echo $ORDER_RESPONSE | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
echo $ORDER_RESPONSE
echo -e "\n"

echo "15. Get Order Details"
curl -X GET "$BASE_URL/orders/$ORDER_ID" \
  -H "Authorization: Bearer $CUSTOMER_TOKEN"
echo -e "\n"

echo "16. List Customer Orders"
curl -X GET "$BASE_URL/orders/my-orders" \
  -H "Authorization: Bearer $CUSTOMER_TOKEN"
echo -e "\n"

echo "17. Update Order Status to Processing (as Owner)"
curl -X PATCH "$BASE_URL/orders/$ORDER_ID/status" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "processing"
  }'
echo -e "\n"

echo "18. Update Order Status to In Route (as Owner)"
curl -X PATCH "$BASE_URL/orders/$ORDER_ID/status" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_route"
  }'
echo -e "\n"

echo "19. Update Order Status to Delivered (as Owner)"
curl -X PATCH "$BASE_URL/orders/$ORDER_ID/status" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "delivered"
  }'
echo -e "\n"

echo "20. Update Order Status to Received (as Customer)"
curl -X PATCH "$BASE_URL/orders/$ORDER_ID/status" \
  -H "Authorization: Bearer $CUSTOMER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "received"
  }'
echo -e "\n"

echo "21. List All Users (as Admin)"
curl -X GET "$BASE_URL/users/" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
echo -e "\n"

echo "22. Update Restaurant (as Owner)"
curl -X PUT "$BASE_URL/restaurants/$RESTAURANT_ID" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Italian Delight - Updated",
    "description": "The best Italian cuisine in town"
  }'
echo -e "\n"

echo "23. Block User (as Admin)"
curl -X PUT "$BASE_URL/users/2" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "is_blocked": true
  }'
echo -e "\n"

echo "=== cURL Collection Complete ==="

