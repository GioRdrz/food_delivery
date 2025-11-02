from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.meal import Meal
from app.models.user import User, UserRole
from app.schemas.meal import MealCreate, MealUpdate
from app.services.restaurant_service import RestaurantService
from app.core.logger import get_logger

logger = get_logger(__name__)


class MealService:
    """Service for meal-related business logic."""
    
    def __init__(self, db: Session):
        self.db = db
        self.restaurant_service = RestaurantService(db)
    
    def get_meal_by_id(self, meal_id: int) -> Optional[Meal]:
        """Get a meal by ID."""
        return self.db.query(Meal).filter(Meal.id == meal_id).first()
    
    def get_meals(self, skip: int = 0, limit: int = 100, include_blocked: bool = False) -> List[Meal]:
        """Get all meals with pagination."""
        query = self.db.query(Meal)
        if not include_blocked:
            query = query.filter(Meal.is_blocked == False)
        return query.offset(skip).limit(limit).all()
    
    def get_meals_by_restaurant(self, restaurant_id: int, include_blocked: bool = False) -> List[Meal]:
        """Get all meals for a specific restaurant."""
        query = self.db.query(Meal).filter(Meal.restaurant_id == restaurant_id)
        if not include_blocked:
            query = query.filter(Meal.is_blocked == False)
        return query.all()
    
    def create_meal(self, meal_data: MealCreate, current_user: User) -> Meal:
        """Create a new meal."""
        # Check if restaurant exists
        restaurant = self.restaurant_service.get_restaurant_by_id(meal_data.restaurant_id)
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )
        
        # Check permissions: owner can create meals for their restaurant, admin can create for any
        if current_user.role != UserRole.ADMIN and restaurant.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        db_meal = Meal(
            name=meal_data.name,
            description=meal_data.description,
            price=meal_data.price,
            restaurant_id=meal_data.restaurant_id,
        )
        self.db.add(db_meal)
        self.db.commit()
        self.db.refresh(db_meal)
        return db_meal
    
    def update_meal(self, meal_id: int, meal_data: MealUpdate, current_user: User) -> Meal:
        """Update a meal."""
        db_meal = self.get_meal_by_id(meal_id)
        if not db_meal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meal not found"
            )
        
        # Check permissions
        restaurant = self.restaurant_service.get_restaurant_by_id(db_meal.restaurant_id)
        if current_user.role != UserRole.ADMIN and restaurant.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        # Update fields
        update_data = meal_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_meal, field, value)
        
        self.db.commit()
        self.db.refresh(db_meal)
        return db_meal
    
    def delete_meal(self, meal_id: int, current_user: User) -> bool:
        """Delete a meal."""
        db_meal = self.get_meal_by_id(meal_id)
        if not db_meal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meal not found"
            )
        
        # Check permissions
        restaurant = self.restaurant_service.get_restaurant_by_id(db_meal.restaurant_id)
        if current_user.role != UserRole.ADMIN and restaurant.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        self.db.delete(db_meal)
        self.db.commit()
        return True

