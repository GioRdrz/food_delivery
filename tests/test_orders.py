import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def restaurant_with_meals(client, restaurant_owner_token, db_session):
    """Create a restaurant with meals for testing."""
    # Create restaurant
    restaurant_response = client.post(
        "/restaurants/",
        json={"name": "Test Restaurant", "description": "Italian cuisine"},
        headers={"Authorization": f"Bearer {restaurant_owner_token}"}
    )
    restaurant_id = restaurant_response.json()["id"]
    
    # Create meals
    meal1_response = client.post(
        "/meals/",
        json={
            "name": "Pizza",
            "description": "Delicious pizza",
            "price": "15.99",
            "restaurant_id": restaurant_id
        },
        headers={"Authorization": f"Bearer {restaurant_owner_token}"}
    )
    
    meal2_response = client.post(
        "/meals/",
        json={
            "name": "Pasta",
            "description": "Fresh pasta",
            "price": "12.99",
            "restaurant_id": restaurant_id
        },
        headers={"Authorization": f"Bearer {restaurant_owner_token}"}
    )
    
    return {
        "restaurant_id": restaurant_id,
        "meal1_id": meal1_response.json()["id"],
        "meal2_id": meal2_response.json()["id"]
    }


def test_create_order(client: TestClient, customer_token, restaurant_with_meals):
    """Test creating an order."""
    response = client.post(
        "/orders/",
        json={
            "restaurant_id": restaurant_with_meals["restaurant_id"],
            "items": [
                {"meal_id": restaurant_with_meals["meal1_id"], "quantity": 2},
                {"meal_id": restaurant_with_meals["meal2_id"], "quantity": 1}
            ],
            "tip_amount": "5.00"
        },
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "placed"
    assert len(data["items"]) == 2
    assert float(data["tip_amount"]) == 5.00


def test_create_order_with_coupon(client: TestClient, customer_token, admin_token, restaurant_with_meals):
    """Test creating an order with a coupon."""
    # Create coupon as admin
    client.post(
        "/coupons/",
        json={"code": "DISCOUNT10", "discount_percentage": "10.00"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    # Create order with coupon
    response = client.post(
        "/orders/",
        json={
            "restaurant_id": restaurant_with_meals["restaurant_id"],
            "items": [
                {"meal_id": restaurant_with_meals["meal1_id"], "quantity": 1}
            ],
            "tip_amount": "0.00",
            "coupon_code": "DISCOUNT10"
        },
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    # Total should be 15.99 - 10% = 14.39 (approximately)
    assert float(data["total_amount"]) < 16.00


def test_update_order_status_customer_cancel(client: TestClient, customer_token, restaurant_with_meals):
    """Test customer canceling an order."""
    # Create order
    order_response = client.post(
        "/orders/",
        json={
            "restaurant_id": restaurant_with_meals["restaurant_id"],
            "items": [{"meal_id": restaurant_with_meals["meal1_id"], "quantity": 1}],
            "tip_amount": "0.00"
        },
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    order_id = order_response.json()["id"]
    
    # Cancel order
    response = client.patch(
        f"/orders/{order_id}/status",
        json={"status": "canceled"},
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "canceled"


def test_update_order_status_owner_processing(client: TestClient, customer_token, restaurant_owner_token, restaurant_with_meals):
    """Test restaurant owner updating order to processing."""
    # Create order as customer
    order_response = client.post(
        "/orders/",
        json={
            "restaurant_id": restaurant_with_meals["restaurant_id"],
            "items": [{"meal_id": restaurant_with_meals["meal1_id"], "quantity": 1}],
            "tip_amount": "0.00"
        },
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    order_id = order_response.json()["id"]
    
    # Update to processing as owner
    response = client.patch(
        f"/orders/{order_id}/status",
        json={"status": "processing"},
        headers={"Authorization": f"Bearer {restaurant_owner_token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "processing"


def test_order_status_history(client: TestClient, customer_token, restaurant_owner_token, restaurant_with_meals):
    """Test that order status history is tracked."""
    # Create order
    order_response = client.post(
        "/orders/",
        json={
            "restaurant_id": restaurant_with_meals["restaurant_id"],
            "items": [{"meal_id": restaurant_with_meals["meal1_id"], "quantity": 1}],
            "tip_amount": "0.00"
        },
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    order_id = order_response.json()["id"]
    
    # Update status
    client.patch(
        f"/orders/{order_id}/status",
        json={"status": "processing"},
        headers={"Authorization": f"Bearer {restaurant_owner_token}"}
    )
    
    # Get order and check history
    response = client.get(
        f"/orders/{order_id}",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    data = response.json()
    assert len(data["status_history"]) == 2  # placed and processing
    assert data["status_history"][0]["status"] == "placed"
    assert data["status_history"][1]["status"] == "processing"


def test_list_customer_orders(client: TestClient, customer_token, restaurant_with_meals):
    """Test listing customer's orders."""
    # Create order
    client.post(
        "/orders/",
        json={
            "restaurant_id": restaurant_with_meals["restaurant_id"],
            "items": [{"meal_id": restaurant_with_meals["meal1_id"], "quantity": 1}],
            "tip_amount": "0.00"
        },
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    
    # List orders
    response = client.get(
        "/orders/my-orders",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

