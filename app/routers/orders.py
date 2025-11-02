from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.services.order_service import OrderService
from app.services.restaurant_service import RestaurantService
from app.models.user import User, UserRole
from app.dependencies import get_current_user

from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=List[OrderResponse])
def list_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List orders based on user role."""
    order_service = OrderService(db)
    
    if current_user.role == UserRole.ADMIN:
        # Admins see all orders
        orders = order_service.get_orders(skip=skip, limit=limit)
    elif current_user.role == UserRole.CUSTOMER:
        # Customers see their own orders
        orders = order_service.get_orders_by_customer(current_user.id)
    elif current_user.role == UserRole.RESTAURANT_OWNER:
        # Restaurant owners see orders for their restaurants
        restaurant_service = RestaurantService(db)
        restaurants = restaurant_service.get_restaurants_by_owner(current_user.id)
        orders = []
        for restaurant in restaurants:
            orders.extend(order_service.get_orders_by_restaurant(restaurant.id))
    else:
        orders = []
    
    return orders


@router.get("/my-orders", response_model=List[OrderResponse])
def list_my_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List orders for the current customer."""
    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can access this endpoint"
        )
    
    order_service = OrderService(db)
    orders = order_service.get_orders_by_customer(current_user.id)
    return orders


@router.get("/restaurant/{restaurant_id}", response_model=List[OrderResponse])
def list_restaurant_orders(
    restaurant_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List orders for a specific restaurant (owner or admin only)."""
    restaurant_service = RestaurantService(db)
    restaurant = restaurant_service.get_restaurant_by_id(restaurant_id)
    
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    
    # Check permissions
    if current_user.role != UserRole.ADMIN and restaurant.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    order_service = OrderService(db)
    orders = order_service.get_orders_by_restaurant(restaurant_id)
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific order."""
    order_service = OrderService(db)
    order = order_service.get_order_by_id(order_id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.CUSTOMER and order.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not your order"
        )
    elif current_user.role == UserRole.RESTAURANT_OWNER:
        restaurant_service = RestaurantService(db)
        restaurant = restaurant_service.get_restaurant_by_id(order.restaurant_id)
        if restaurant.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not your restaurant's order"
            )
    
    return order


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new order (customers only)."""
    order_service = OrderService(db)
    order = order_service.create_order(order_data, current_user)
    return order


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update order status."""
    order_service = OrderService(db)
    order = order_service.update_order_status(order_id, status_data, current_user)
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an order (admin only)."""
    order_service = OrderService(db)
    order_service.delete_order(order_id, current_user)
    return None

