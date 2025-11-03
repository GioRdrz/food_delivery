import pytest
from fastapi.testclient import TestClient


def test_register_customer(client: TestClient):
    """Test user registration."""
    response = client.post(
        "/auth/register",
        json={
            "email": "newuser@test.com",
            "password": "password123",
            "full_name": "New User",
            "role": "customer"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@test.com"
    assert data["role"] == "customer"
    assert "id" in data


def test_register_duplicate_email(client: TestClient, customer_user):
    """Test registration with duplicate email."""
    response = client.post(
        "/auth/register",
        json={
            "email": "customer@test.com",
            "password": "password123",
            "full_name": "Duplicate User",
            "role": "customer"
        }
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_login_success(client: TestClient, customer_user):
    """Test successful login."""
    response = client.post(
        "/auth/login",
        json={
            "email": "customer@test.com",
            "password": "customer123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient, customer_user):
    """Test login with wrong password."""
    response = client.post(
        "/auth/login",
        json={
            "email": "customer@test.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client: TestClient):
    """Test login with nonexistent user."""
    response = client.post(
        "/auth/login",
        json={
            "email": "nonexistent@test.com",
            "password": "password123"
        }
    )
    assert response.status_code == 401

