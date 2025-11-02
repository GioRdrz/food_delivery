import pytest
from fastapi.testclient import TestClient


def test_create_restaurant_as_owner(client: TestClient, restaurant_owner_token):
    """Test creating a restaurant as a restaurant owner."""
    response = client.post(
        "/restaurants/",
        json={
            "name": "Test Restaurant",
            "description": "Italian cuisine"
        },
        headers={"Authorization": f"Bearer {restaurant_owner_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Restaurant"
    assert data["description"] == "Italian cuisine"


def test_create_restaurant_as_customer(client: TestClient, customer_token):
    """Test that customers cannot create restaurants."""
    response = client.post(
        "/restaurants/",
        json={
            "name": "Test Restaurant",
            "description": "Italian cuisine"
        },
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 403


def test_list_restaurants(client: TestClient, restaurant_owner_token, customer_token):
    """Test listing restaurants."""
    # Create a restaurant
    client.post(
        "/restaurants/",
        json={"name": "Test Restaurant", "description": "Italian cuisine"},
        headers={"Authorization": f"Bearer {restaurant_owner_token}"}
    )
    
    # List as customer
    response = client.get(
        "/restaurants/",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Test Restaurant"


def test_update_restaurant_as_owner(client: TestClient, restaurant_owner_token):
    """Test updating a restaurant as the owner."""
    # Create restaurant
    create_response = client.post(
        "/restaurants/",
        json={"name": "Test Restaurant", "description": "Italian cuisine"},
        headers={"Authorization": f"Bearer {restaurant_owner_token}"}
    )
    restaurant_id = create_response.json()["id"]
    
    # Update restaurant
    response = client.put(
        f"/restaurants/{restaurant_id}",
        json={"name": "Updated Restaurant"},
        headers={"Authorization": f"Bearer {restaurant_owner_token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Restaurant"


def test_delete_restaurant(client: TestClient, restaurant_owner_token):
    """Test deleting a restaurant."""
    # Create restaurant
    create_response = client.post(
        "/restaurants/",
        json={"name": "Test Restaurant", "description": "Italian cuisine"},
        headers={"Authorization": f"Bearer {restaurant_owner_token}"}
    )
    restaurant_id = create_response.json()["id"]
    
    # Delete restaurant
    response = client.delete(
        f"/restaurants/{restaurant_id}",
        headers={"Authorization": f"Bearer {restaurant_owner_token}"}
    )
    assert response.status_code == 204

