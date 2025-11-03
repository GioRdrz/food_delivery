from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.schemas.meal import MealCreate, MealUpdate, MealResponse
from app.services.meal_service import MealService
from app.models.user import User, UserRole
from app.dependencies import get_current_user

from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/meals", tags=["Meals"])


@router.get("/", response_model=List[MealResponse])
def list_meals(
    skip: int = 0,
    limit: int = 100,
    include_blocked: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all meals. Customers see only active meals."""
    meal_service = MealService(db)
    
    # Only admins can see blocked meals
    if include_blocked and current_user.role != UserRole.ADMIN:
        include_blocked = False
    
    meals = meal_service.get_meals(skip=skip, limit=limit, include_blocked=include_blocked)
    return meals


@router.get("/restaurant/{restaurant_id}", response_model=List[MealResponse])
def list_meals_by_restaurant(
    restaurant_id: UUID,
    include_blocked: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all meals for a specific restaurant."""
    meal_service = MealService(db)

    # Only admins can see blocked meals
    if include_blocked and current_user.role != UserRole.ADMIN:
        include_blocked = False

    meals = meal_service.get_meals_by_restaurant(restaurant_id, include_blocked=include_blocked)
    return meals


@router.get("/{meal_id}", response_model=MealResponse)
def get_meal(
    meal_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific meal."""
    meal_service = MealService(db)
    meal = meal_service.get_meal_by_id(meal_id)

    if not meal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal not found"
        )

    # Customers cannot see blocked meals
    if meal.is_blocked and current_user.role == UserRole.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal not found"
        )

    return meal


@router.post("/", response_model=MealResponse, status_code=status.HTTP_201_CREATED)
def create_meal(
    meal_data: MealCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new meal (restaurant owners and admins only)."""
    meal_service = MealService(db)
    meal = meal_service.create_meal(meal_data, current_user)
    return meal


@router.put("/{meal_id}", response_model=MealResponse)
def update_meal(
    meal_id: UUID,
    meal_data: MealUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a meal (owner or admin only)."""
    meal_service = MealService(db)
    meal = meal_service.update_meal(meal_id, meal_data, current_user)
    return meal


@router.delete("/{meal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meal(
    meal_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a meal (owner or admin only)."""
    meal_service = MealService(db)
    meal_service.delete_meal(meal_id, current_user)
    return None

