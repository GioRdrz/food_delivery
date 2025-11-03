from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantResponse
from app.services.restaurant_service import RestaurantService
from app.models.user import User, UserRole
from app.dependencies import get_current_user, get_current_admin

from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.get("/", response_model=List[RestaurantResponse])
def list_restaurants(
    skip: int = 0,
    limit: int = 100,
    include_blocked: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all restaurants. Customers see only active restaurants."""
    restaurant_service = RestaurantService(db)
    
    # Only admins can see blocked restaurants
    if include_blocked and current_user.role != UserRole.ADMIN:
        include_blocked = False
    
    restaurants = restaurant_service.get_restaurants(skip=skip, limit=limit, include_blocked=include_blocked)
    return restaurants


@router.get("/my-restaurants", response_model=List[RestaurantResponse])
def list_my_restaurants(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List restaurants owned by the current user."""
    if current_user.role not in [UserRole.RESTAURANT_OWNER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only restaurant owners can access this endpoint"
        )
    
    restaurant_service = RestaurantService(db)
    restaurants = restaurant_service.get_restaurants_by_owner(current_user.id)
    return restaurants


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(
    restaurant_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific restaurant."""
    restaurant_service = RestaurantService(db)
    restaurant = restaurant_service.get_restaurant_by_id(restaurant_id)

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )

    # Customers cannot see blocked restaurants
    if restaurant.is_blocked and current_user.role == UserRole.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )

    return restaurant


@router.post("/", response_model=RestaurantResponse, status_code=status.HTTP_201_CREATED)
def create_restaurant(
    restaurant_data: RestaurantCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new restaurant (restaurant owners and admins only)."""
    restaurant_service = RestaurantService(db)
    restaurant = restaurant_service.create_restaurant(restaurant_data, current_user)
    return restaurant


@router.put("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(
    restaurant_id: UUID,
    restaurant_data: RestaurantUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a restaurant (owner or admin only)."""
    restaurant_service = RestaurantService(db)
    restaurant = restaurant_service.update_restaurant(restaurant_id, restaurant_data, current_user)
    return restaurant


@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(
    restaurant_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a restaurant (owner or admin only)."""
    restaurant_service = RestaurantService(db)
    restaurant_service.delete_restaurant(restaurant_id, current_user)
    return None

