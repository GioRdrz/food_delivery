#!/bin/bash

################################################################################
# Food Delivery Service - API Data Seeding Script
################################################################################
# This script populates the database using the REST API endpoints.
# It creates test data including users, restaurants, meals, coupons, and orders.
#
# Prerequisites:
# - The API server must be running on http://localhost:8000
# - jq must be installed for JSON parsing (sudo apt-get install jq)
#
# Usage:
#   chmod +x seed_data_api.sh
#   ./seed_data_api.sh
################################################################################

set -e  # Exit on error

# Configuration
API_BASE_URL="${API_BASE_URL:-http://localhost:8000}"
ADMIN_EMAIL="admin@fooddelivery.com"
ADMIN_PASSWORD="admin123"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
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

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    print_error "jq is not installed. Please install it: sudo apt-get install jq"
    exit 1
fi

# Check if API is running
print_info "Checking if API is running at $API_BASE_URL..."
if ! curl -s -f "$API_BASE_URL/" > /dev/null; then
    print_error "API is not running at $API_BASE_URL"
    print_info "Please start the API server first: uvicorn app.main:app --reload"
    exit 1
fi
print_success "API is running"

################################################################################
# Step 1: Create Admin and Get Token
################################################################################
print_header "Step 1: Admin Authentication"

# Try to login as admin (admin might already exist)
print_info "Attempting to login as admin..."
ADMIN_TOKEN=$(curl -s -X POST "$API_BASE_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$ADMIN_EMAIL\",\"password\":\"$ADMIN_PASSWORD\"}" \
    | jq -r '.access_token // empty')

if [ -z "$ADMIN_TOKEN" ]; then
    print_warning "Admin login failed (admin might not exist yet)"
    print_info "Note: Admin user should be created during app startup"
    print_info "Continuing without admin token (some operations may fail)"
else
    print_success "Admin logged in successfully"
fi

################################################################################
# Step 2: Create Users
################################################################################
print_header "Step 2: Creating Users"

# Customer 1
print_info "Creating Customer 1: Alice Johnson..."
CUSTOMER1_RESPONSE=$(curl -s -X POST "$API_BASE_URL/auth/register" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "customer1@example.com",
        "password": "password123",
        "full_name": "Alice Johnson",
        "role": "customer"
    }')
CUSTOMER1_ID=$(echo "$CUSTOMER1_RESPONSE" | jq -r '.id // empty')
if [ -z "$CUSTOMER1_ID" ]; then
    print_error "Failed to create Customer 1"
    echo "$CUSTOMER1_RESPONSE" | jq '.'
    exit 1
fi
print_success "Created Customer 1: Alice Johnson (ID: $CUSTOMER1_ID)"

# Login Customer 1
CUSTOMER1_TOKEN=$(curl -s -X POST "$API_BASE_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"email":"customer1@example.com","password":"password123"}' \
    | jq -r '.access_token')
print_success "Customer 1 logged in"

# Customer 2
print_info "Creating Customer 2: Bob Smith..."
CUSTOMER2_RESPONSE=$(curl -s -X POST "$API_BASE_URL/auth/register" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "customer2@example.com",
        "password": "password123",
        "full_name": "Bob Smith",
        "role": "customer"
    }')
CUSTOMER2_ID=$(echo "$CUSTOMER2_RESPONSE" | jq -r '.id // empty')
if [ -z "$CUSTOMER2_ID" ]; then
    print_error "Failed to create Customer 2"
    exit 1
fi
print_success "Created Customer 2: Bob Smith (ID: $CUSTOMER2_ID)"

# Login Customer 2
CUSTOMER2_TOKEN=$(curl -s -X POST "$API_BASE_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"email":"customer2@example.com","password":"password123"}' \
    | jq -r '.access_token')
print_success "Customer 2 logged in"

# Restaurant Owner 1
print_info "Creating Restaurant Owner 1: Carlos Martinez..."
OWNER1_RESPONSE=$(curl -s -X POST "$API_BASE_URL/auth/register" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "owner1@example.com",
        "password": "password123",
        "full_name": "Carlos Martinez",
        "role": "restaurant_owner"
    }')
OWNER1_ID=$(echo "$OWNER1_RESPONSE" | jq -r '.id // empty')
if [ -z "$OWNER1_ID" ]; then
    print_error "Failed to create Restaurant Owner 1"
    exit 1
fi
print_success "Created Restaurant Owner 1: Carlos Martinez (ID: $OWNER1_ID)"

# Login Owner 1
OWNER1_TOKEN=$(curl -s -X POST "$API_BASE_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"email":"owner1@example.com","password":"password123"}' \
    | jq -r '.access_token')
print_success "Restaurant Owner 1 logged in"

# Restaurant Owner 2
print_info "Creating Restaurant Owner 2: Diana Chen..."
OWNER2_RESPONSE=$(curl -s -X POST "$API_BASE_URL/auth/register" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "owner2@example.com",
        "password": "password123",
        "full_name": "Diana Chen",
        "role": "restaurant_owner"
    }')
OWNER2_ID=$(echo "$OWNER2_RESPONSE" | jq -r '.id // empty')
if [ -z "$OWNER2_ID" ]; then
    print_error "Failed to create Restaurant Owner 2"
    exit 1
fi
print_success "Created Restaurant Owner 2: Diana Chen (ID: $OWNER2_ID)"

# Login Owner 2
OWNER2_TOKEN=$(curl -s -X POST "$API_BASE_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"email":"owner2@example.com","password":"password123"}' \
    | jq -r '.access_token')
print_success "Restaurant Owner 2 logged in"

################################################################################
# Step 3: Create Coupon (Admin only)
################################################################################
print_header "Step 3: Creating Coupon"

if [ -n "$ADMIN_TOKEN" ]; then
    print_info "Creating 10% discount coupon..."
    COUPON_RESPONSE=$(curl -s -X POST "$API_BASE_URL/coupons/" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $ADMIN_TOKEN" \
        -d '{
            "code": "WELCOME10",
            "discount_percentage": 10.00
        }')
    COUPON_ID=$(echo "$COUPON_RESPONSE" | jq -r '.id // empty')
    if [ -z "$COUPON_ID" ]; then
        print_warning "Failed to create coupon (might already exist or admin token invalid)"
    else
        print_success "Created Coupon: WELCOME10 (10% discount, ID: $COUPON_ID)"
    fi
else
    print_warning "Skipping coupon creation (no admin token)"
fi

################################################################################
# Step 4: Create Restaurants and Meals
################################################################################
print_header "Step 4: Creating Restaurants and Meals"

# Restaurant 1 - Bella Italia
print_info "Creating Restaurant 1: Bella Italia..."
RESTAURANT1_RESPONSE=$(curl -s -X POST "$API_BASE_URL/restaurants/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OWNER1_TOKEN" \
    -d '{
        "name": "Bella Italia",
        "description": "Authentic Italian cuisine with fresh ingredients"
    }')
RESTAURANT1_ID=$(echo "$RESTAURANT1_RESPONSE" | jq -r '.id // empty')
if [ -z "$RESTAURANT1_ID" ]; then
    print_error "Failed to create Restaurant 1"
    echo "$RESTAURANT1_RESPONSE" | jq '.'
    exit 1
fi
print_success "Created Restaurant 1: Bella Italia (ID: $RESTAURANT1_ID)"

# Meals for Restaurant 1
print_info "Adding meals to Bella Italia..."
MEAL1_1=$(curl -s -X POST "$API_BASE_URL/meals/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OWNER1_TOKEN" \
    -d "{
        \"name\": \"Margherita Pizza\",
        \"description\": \"Classic pizza with tomato, mozzarella, and basil\",
        \"price\": 12.99,
        \"restaurant_id\": \"$RESTAURANT1_ID\"
    }" | jq -r '.id')

MEAL1_2=$(curl -s -X POST "$API_BASE_URL/meals/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OWNER1_TOKEN" \
    -d "{
        \"name\": \"Spaghetti Carbonara\",
        \"description\": \"Creamy pasta with bacon and parmesan\",
        \"price\": 14.99,
        \"restaurant_id\": \"$RESTAURANT1_ID\"
    }" | jq -r '.id')

MEAL1_3=$(curl -s -X POST "$API_BASE_URL/meals/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OWNER1_TOKEN" \
    -d "{
        \"name\": \"Tiramisu\",
        \"description\": \"Classic Italian dessert\",
        \"price\": 6.99,
        \"restaurant_id\": \"$RESTAURANT1_ID\"
    }" | jq -r '.id')

print_success "Added 3 meals to Bella Italia"

# Restaurant 2 - Dragon Wok
print_info "Creating Restaurant 2: Dragon Wok..."
RESTAURANT2_RESPONSE=$(curl -s -X POST "$API_BASE_URL/restaurants/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OWNER2_TOKEN" \
    -d '{
        "name": "Dragon Wok",
        "description": "Modern Asian fusion with traditional flavors"
    }')
RESTAURANT2_ID=$(echo "$RESTAURANT2_RESPONSE" | jq -r '.id // empty')
if [ -z "$RESTAURANT2_ID" ]; then
    print_error "Failed to create Restaurant 2"
    exit 1
fi
print_success "Created Restaurant 2: Dragon Wok (ID: $RESTAURANT2_ID)"

# Meals for Restaurant 2
print_info "Adding meals to Dragon Wok..."
MEAL2_1=$(curl -s -X POST "$API_BASE_URL/meals/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OWNER2_TOKEN" \
    -d "{
        \"name\": \"Pad Thai\",
        \"description\": \"Stir-fried rice noodles with shrimp and peanuts\",
        \"price\": 13.99,
        \"restaurant_id\": \"$RESTAURANT2_ID\"
    }" | jq -r '.id')

MEAL2_2=$(curl -s -X POST "$API_BASE_URL/meals/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OWNER2_TOKEN" \
    -d "{
        \"name\": \"General Tso's Chicken\",
        \"description\": \"Crispy chicken in sweet and spicy sauce\",
        \"price\": 15.99,
        \"restaurant_id\": \"$RESTAURANT2_ID\"
    }" | jq -r '.id')

MEAL2_3=$(curl -s -X POST "$API_BASE_URL/meals/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OWNER2_TOKEN" \
    -d "{
        \"name\": \"Mango Sticky Rice\",
        \"description\": \"Sweet sticky rice with fresh mango\",
        \"price\": 7.99,
        \"restaurant_id\": \"$RESTAURANT2_ID\"
    }" | jq -r '.id')

print_success "Added 3 meals to Dragon Wok"

################################################################################
# Step 5: Create Orders
################################################################################
print_header "Step 5: Creating Orders"

# Order 1: Customer 1 → Restaurant 1 (with coupon, status: RECEIVED)
print_info "Creating Order 1: Customer 1 → Bella Italia (with 10% coupon)..."
ORDER1_RESPONSE=$(curl -s -X POST "$API_BASE_URL/orders/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $CUSTOMER1_TOKEN" \
    -d "{
        \"restaurant_id\": \"$RESTAURANT1_ID\",
        \"items\": [
            {\"meal_id\": \"$MEAL1_1\", \"quantity\": 1},
            {\"meal_id\": \"$MEAL1_2\", \"quantity\": 1}
        ],
        \"tip_amount\": 3.00,
        \"coupon_code\": \"WELCOME10\"
    }")
ORDER1_ID=$(echo "$ORDER1_RESPONSE" | jq -r '.id // empty')
if [ -z "$ORDER1_ID" ]; then
    print_error "Failed to create Order 1"
    echo "$ORDER1_RESPONSE" | jq '.'
else
    print_success "Created Order 1 (ID: $ORDER1_ID)"

    # Update status to PROCESSING
    print_info "Updating Order 1 status: PLACED → PROCESSING..."
    curl -s -X PATCH "$API_BASE_URL/orders/$ORDER1_ID/status" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $OWNER1_TOKEN" \
        -d '{"status": "processing"}' > /dev/null

    # Update status to IN_ROUTE
    print_info "Updating Order 1 status: PROCESSING → IN_ROUTE..."
    curl -s -X PATCH "$API_BASE_URL/orders/$ORDER1_ID/status" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $OWNER1_TOKEN" \
        -d '{"status": "in_route"}' > /dev/null

    # Update status to DELIVERED
    print_info "Updating Order 1 status: IN_ROUTE → DELIVERED..."
    curl -s -X PATCH "$API_BASE_URL/orders/$ORDER1_ID/status" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $OWNER1_TOKEN" \
        -d '{"status": "delivered"}' > /dev/null

    # Update status to RECEIVED
    print_info "Updating Order 1 status: DELIVERED → RECEIVED..."
    curl -s -X PATCH "$API_BASE_URL/orders/$ORDER1_ID/status" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $CUSTOMER1_TOKEN" \
        -d '{"status": "received"}' > /dev/null

    print_success "Order 1 status: RECEIVED"
fi

# Order 2: Customer 1 → Restaurant 2 (status: PLACED)
print_info "Creating Order 2: Customer 1 → Dragon Wok..."
ORDER2_RESPONSE=$(curl -s -X POST "$API_BASE_URL/orders/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $CUSTOMER1_TOKEN" \
    -d "{
        \"restaurant_id\": \"$RESTAURANT2_ID\",
        \"items\": [
            {\"meal_id\": \"$MEAL2_1\", \"quantity\": 1}
        ],
        \"tip_amount\": 2.00
    }")
ORDER2_ID=$(echo "$ORDER2_RESPONSE" | jq -r '.id // empty')
if [ -z "$ORDER2_ID" ]; then
    print_error "Failed to create Order 2"
    echo "$ORDER2_RESPONSE" | jq '.'
else
    print_success "Created Order 2 (ID: $ORDER2_ID, Status: PLACED)"
fi

# Order 3: Customer 2 → Restaurant 2 (status: IN_ROUTE)
print_info "Creating Order 3: Customer 2 → Dragon Wok..."
ORDER3_RESPONSE=$(curl -s -X POST "$API_BASE_URL/orders/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $CUSTOMER2_TOKEN" \
    -d "{
        \"restaurant_id\": \"$RESTAURANT2_ID\",
        \"items\": [
            {\"meal_id\": \"$MEAL2_2\", \"quantity\": 1}
        ],
        \"tip_amount\": 2.50
    }")
ORDER3_ID=$(echo "$ORDER3_RESPONSE" | jq -r '.id // empty')
if [ -z "$ORDER3_ID" ]; then
    print_error "Failed to create Order 3"
    echo "$ORDER3_RESPONSE" | jq '.'
else
    print_success "Created Order 3 (ID: $ORDER3_ID)"

    # Update status to PROCESSING
    print_info "Updating Order 3 status: PLACED → PROCESSING..."
    curl -s -X PATCH "$API_BASE_URL/orders/$ORDER3_ID/status" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $OWNER2_TOKEN" \
        -d '{"status": "processing"}' > /dev/null

    # Update status to IN_ROUTE
    print_info "Updating Order 3 status: PROCESSING → IN_ROUTE..."
    curl -s -X PATCH "$API_BASE_URL/orders/$ORDER3_ID/status" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $OWNER2_TOKEN" \
        -d '{"status": "in_route"}' > /dev/null

    print_success "Order 3 status: IN_ROUTE"
fi

################################################################################
# Step 6: Display Results
################################################################################
print_header "Step 6: Displaying Results"

# Orders by Restaurant Owner
echo ""
echo "🏪 Orders by Restaurant Owner:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

print_info "Bella Italia (Owner: Carlos Martinez):"
OWNER1_ORDERS=$(curl -s -X GET "$API_BASE_URL/orders/restaurant/$RESTAURANT1_ID" \
    -H "Authorization: Bearer $OWNER1_TOKEN")
echo "$OWNER1_ORDERS" | jq -r '.[] | "  📦 Order \(.id) - Status: \(.status) - Total: $\(.total_amount)"'
echo ""

print_info "Dragon Wok (Owner: Diana Chen):"
OWNER2_ORDERS=$(curl -s -X GET "$API_BASE_URL/orders/restaurant/$RESTAURANT2_ID" \
    -H "Authorization: Bearer $OWNER2_TOKEN")
echo "$OWNER2_ORDERS" | jq -r '.[] | "  📦 Order \(.id) - Status: \(.status) - Total: $\(.total_amount)"'
echo ""

# Orders by Customer
echo "👤 Orders by Customer:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

print_info "Alice Johnson (Customer 1):"
CUSTOMER1_ORDERS=$(curl -s -X GET "$API_BASE_URL/orders/my-orders" \
    -H "Authorization: Bearer $CUSTOMER1_TOKEN")
echo "$CUSTOMER1_ORDERS" | jq -r '.[] | "  📦 Order \(.id) - Status: \(.status) - Total: $\(.total_amount)"'
echo ""

print_info "Bob Smith (Customer 2):"
CUSTOMER2_ORDERS=$(curl -s -X GET "$API_BASE_URL/orders/my-orders" \
    -H "Authorization: Bearer $CUSTOMER2_TOKEN")
echo "$CUSTOMER2_ORDERS" | jq -r '.[] | "  📦 Order \(.id) - Status: \(.status) - Total: $\(.total_amount)"'
echo ""

################################################################################
# Step 7: Admin Capabilities Demonstration
################################################################################
print_header "Step 7: Admin Capabilities Demonstration"

if [ -z "$ADMIN_TOKEN" ]; then
    print_warning "Skipping admin demonstration (no admin token)"
else
    echo ""
    echo "🔧 Demonstrating Admin CRUD Operations:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # 1. List all users
    print_info "1. Listing all users (admin only)..."
    ALL_USERS=$(curl -s -X GET "$API_BASE_URL/users/" \
        -H "Authorization: Bearer $ADMIN_TOKEN")
    USER_COUNT=$(echo "$ALL_USERS" | jq '. | length')
    print_success "Found $USER_COUNT users in the system"
    echo "$ALL_USERS" | jq -r '.[] | "   • \(.full_name) (\(.email)) - Role: \(.role) - Blocked: \(.is_blocked)"'
    echo ""

    # 2. Create a new user via admin
    print_info "2. Creating a new user via admin endpoint..."
    NEW_USER_RESPONSE=$(curl -s -X POST "$API_BASE_URL/users/" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $ADMIN_TOKEN" \
        -d '{
            "email": "testuser@example.com",
            "password": "password123",
            "full_name": "Test User",
            "role": "customer"
        }')
    NEW_USER_ID=$(echo "$NEW_USER_RESPONSE" | jq -r '.id // empty')
    if [ -n "$NEW_USER_ID" ]; then
        print_success "Created new user: Test User (ID: $NEW_USER_ID)"
    else
        print_warning "User might already exist"
    fi
    echo ""

    # 3. Update a user (block Customer 2)
    print_info "3. Blocking Customer 2 (Bob Smith)..."
    CUSTOMER2_ID=$(echo "$ALL_USERS" | jq -r '.[] | select(.email == "customer2@example.com") | .id')
    if [ -n "$CUSTOMER2_ID" ]; then
        curl -s -X PUT "$API_BASE_URL/users/$CUSTOMER2_ID" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $ADMIN_TOKEN" \
            -d '{"is_blocked": true}' > /dev/null
        print_success "Customer 2 has been blocked"
    fi
    echo ""

    # 4. Verify blocked user
    print_info "4. Verifying blocked user status..."
    BLOCKED_USER=$(curl -s -X GET "$API_BASE_URL/users/$CUSTOMER2_ID" \
        -H "Authorization: Bearer $ADMIN_TOKEN")
    IS_BLOCKED=$(echo "$BLOCKED_USER" | jq -r '.is_blocked')
    if [ "$IS_BLOCKED" = "true" ]; then
        print_success "Confirmed: Customer 2 is blocked"
    fi
    echo ""

    # 5. Unblock the user
    print_info "5. Unblocking Customer 2..."
    curl -s -X PUT "$API_BASE_URL/users/$CUSTOMER2_ID" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $ADMIN_TOKEN" \
        -d '{"is_blocked": false}' > /dev/null
    print_success "Customer 2 has been unblocked"
    echo ""

    # 6. Block a restaurant
    print_info "6. Blocking Dragon Wok restaurant..."
    curl -s -X PUT "$API_BASE_URL/restaurants/$RESTAURANT2_ID" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $ADMIN_TOKEN" \
        -d '{"is_blocked": true}' > /dev/null
    print_success "Dragon Wok has been blocked"
    echo ""

    # 7. List restaurants with blocked ones
    print_info "7. Listing all restaurants (including blocked)..."
    ALL_RESTAURANTS=$(curl -s -X GET "$API_BASE_URL/restaurants/?include_blocked=true" \
        -H "Authorization: Bearer $ADMIN_TOKEN")
    echo "$ALL_RESTAURANTS" | jq -r '.[] | "   • \(.name) - Blocked: \(.is_blocked)"'
    echo ""

    # 8. Unblock the restaurant
    print_info "8. Unblocking Dragon Wok..."
    curl -s -X PUT "$API_BASE_URL/restaurants/$RESTAURANT2_ID" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $ADMIN_TOKEN" \
        -d '{"is_blocked": false}' > /dev/null
    print_success "Dragon Wok has been unblocked"
    echo ""

    # 9. Block a meal
    print_info "9. Blocking Pad Thai meal..."
    curl -s -X PUT "$API_BASE_URL/meals/$MEAL2_1" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $ADMIN_TOKEN" \
        -d '{"is_blocked": true}' > /dev/null
    print_success "Pad Thai has been blocked"
    echo ""

    # 10. List meals with blocked ones
    print_info "10. Listing all meals (including blocked)..."
    ALL_MEALS=$(curl -s -X GET "$API_BASE_URL/meals/?include_blocked=true" \
        -H "Authorization: Bearer $ADMIN_TOKEN")
    echo "$ALL_MEALS" | jq -r '.[] | "   • \(.name) - Price: $\(.price) - Blocked: \(.is_blocked)"'
    echo ""

    # 11. Unblock the meal
    print_info "11. Unblocking Pad Thai..."
    curl -s -X PUT "$API_BASE_URL/meals/$MEAL2_1" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $ADMIN_TOKEN" \
        -d '{"is_blocked": false}' > /dev/null
    print_success "Pad Thai has been unblocked"
    echo ""

    # 12. View all orders (admin can see all)
    print_info "12. Viewing all orders in the system (admin only)..."
    ALL_ORDERS=$(curl -s -X GET "$API_BASE_URL/orders/" \
        -H "Authorization: Bearer $ADMIN_TOKEN")
    ORDER_COUNT=$(echo "$ALL_ORDERS" | jq '. | length')
    print_success "Found $ORDER_COUNT orders in the system"
    echo "$ALL_ORDERS" | jq -r '.[] | "   • Order \(.id | .[0:8])... - Status: \(.status) - Total: $\(.total_amount)"'
    echo ""

    # 13. View order details with status history
    print_info "13. Viewing Order 1 details with status history..."
    ORDER1_DETAILS=$(curl -s -X GET "$API_BASE_URL/orders/$ORDER1_ID" \
        -H "Authorization: Bearer $ADMIN_TOKEN")
    echo "   Order ID: $(echo "$ORDER1_DETAILS" | jq -r '.id')"
    echo "   Status: $(echo "$ORDER1_DETAILS" | jq -r '.status')"
    echo "   Total: \$$(echo "$ORDER1_DETAILS" | jq -r '.total_amount')"
    echo "   Items: $(echo "$ORDER1_DETAILS" | jq -r '.items | length')"
    HISTORY_COUNT=$(echo "$ORDER1_DETAILS" | jq -r '.status_history | length')
    echo "   Status History ($HISTORY_COUNT changes):"
    echo "$ORDER1_DETAILS" | jq -r '.status_history[] | "      • \(.status) at \(.changed_at)"'
    echo ""

    # 14. Update coupon
    print_info "14. Updating coupon discount to 15%..."
    if [ -n "$COUPON_ID" ]; then
        curl -s -X PUT "$API_BASE_URL/coupons/$COUPON_ID" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $ADMIN_TOKEN" \
            -d '{"discount_percentage": 15.00}' > /dev/null
        print_success "Coupon updated to 15% discount"

        # Verify update
        UPDATED_COUPON=$(curl -s -X GET "$API_BASE_URL/coupons/$COUPON_ID" \
            -H "Authorization: Bearer $ADMIN_TOKEN")
        NEW_DISCOUNT=$(echo "$UPDATED_COUPON" | jq -r '.discount_percentage')
        echo "   Verified: Discount is now ${NEW_DISCOUNT}%"
    fi
    echo ""

    # 15. Delete the test user
    print_info "15. Deleting test user..."
    if [ -n "$NEW_USER_ID" ]; then
        curl -s -X DELETE "$API_BASE_URL/users/$NEW_USER_ID" \
            -H "Authorization: Bearer $ADMIN_TOKEN" > /dev/null
        print_success "Test user deleted"
    fi
    echo ""

    print_success "Admin capabilities demonstration complete!"
    echo ""
fi

################################################################################
# Summary
################################################################################
print_header "Summary"

print_success "All test data has been successfully created via API!"
echo ""
echo "📊 Summary:"
echo "  • 4 Users created (2 customers, 2 restaurant owners)"
echo "  • 1 Coupon created (WELCOME10 - 15% discount after admin update)"
echo "  • 2 Restaurants created with 3 meals each"
echo "  • 3 Orders created with different statuses"
echo "  • Admin capabilities demonstrated (CRUD, blocking/unblocking)"
echo ""
echo "🔑 Test Credentials:"
echo "  Admin:      admin@fooddelivery.com / admin123"
echo "  Customer 1: customer1@example.com / password123"
echo "  Customer 2: customer2@example.com / password123"
echo "  Owner 1:    owner1@example.com / password123"
echo "  Owner 2:    owner2@example.com / password123"
echo ""
echo "🌐 API Documentation: $API_BASE_URL/docs"
echo ""

