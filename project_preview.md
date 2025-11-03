# Food Delivery Service API - Project Preview

## Task Scope and Expectations

Your task is to write a food delivery service API.

You need to write an API for a simple application where users can order meals from restaurants.

### User Authentication
- The user must be able to create an account and log in using the API
- Each user can have only one account (the user is identified by an email)

## User Roles and Permissions

Implement 2 roles with different permission levels:

### Customer
- Can see all restaurants
- Can place orders from restaurants

### Restaurant Owner
- Can CRUD (Create, Read, Update, Delete) restaurants and meals

## Data Models

### Restaurant
A restaurant should have:
- Name
- Description of the type of food they serve

### Meal
A meal should have:
- Name
- Description
- Price

### Order
Orders include:
- List of meals
- Date
- Total amount
- Status
- Custom tip amount (optional)
- Reference to a coupon for percentage discount (optional)

**Important:** An order should be placed for a single restaurant only, but it can have multiple meals.

**Note:** There is no need to handle payment of any kind or even to simulate payment handling.

## Order Status Flow

Restaurant owners and customers can change the order status respecting the flow and permissions below:

1. **Placed**: Once a customer places an order
2. **Canceled**: If the customer or restaurant owner cancels the order
3. **Processing**: Once the restaurant owner starts to make the meals
4. **In Route**: Once the meal is finished and the restaurant owner marks it's on the way
5. **Delivered**: Once the restaurant owner receives information that the meal was delivered by their staff
6. **Received**: Once the customer receives the meal and marks it as received

### Order History
- Orders should have a history of the date and time of the status change
- Customers should be able to browse their order history and view updated order status
- Customers and restaurant owners should be able to see a list of the orders

## Administrator Role

Implement an Administrator who can:
- CRUD users (of any role)
- CRUD restaurants
- CRUD meals
- Change all user/restaurant/meal information, including blocking

**Important:** The application should include one built-in admin account that cannot be deleted.

## API Requirements

### REST/GraphQL API
Make it possible to perform all user and admin actions via the API, including authentication.

In any case, you should be able to:
- Explain how a REST/GraphQL API works
- Demonstrate that by creating functional tests that use the REST/GraphQL Layer directly

Please be prepared to use REST/GraphQL clients like:
- Postman
- cURL
- etc.

for this purpose.

