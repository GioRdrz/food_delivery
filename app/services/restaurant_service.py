from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.restaurant import Restaurant
from app.models.user import User, UserRole
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate
from app.core.logger import get_logger

logger = get_logger(__name__)


class RestaurantService:
    """Service for restaurant-related business logic."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_restaurant_by_id(self, restaurant_id: int) -> Optional[Restaurant]:
        """Get a restaurant by ID."""
        return self.db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    
    def get_restaurants(self, skip: int = 0, limit: int = 100, include_blocked: bool = False) -> List[Restaurant]:
        """Get all restaurants with pagination."""
        query = self.db.query(Restaurant)
        if not include_blocked:
            query = query.filter(Restaurant.is_blocked == False)
        return query.offset(skip).limit(limit).all()
    
    def get_restaurants_by_owner(self, owner_id: int) -> List[Restaurant]:
        """Get all restaurants owned by a specific user."""
        return self.db.query(Restaurant).filter(Restaurant.owner_id == owner_id).all()
    
    def create_restaurant(self, restaurant_data: RestaurantCreate, owner: User) -> Restaurant:
        """Create a new restaurant."""
        logger.info(f"Creating restaurant '{restaurant_data.name}' for owner {owner.id}")

        # Only restaurant owners can create restaurants (or admins)
        if owner.role not in [UserRole.RESTAURANT_OWNER, UserRole.ADMIN]:
            logger.warning(f"User {owner.id} with role {owner.role} attempted to create restaurant")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only restaurant owners can create restaurants"
            )

        db_restaurant = Restaurant(
            name=restaurant_data.name,
            description=restaurant_data.description,
            owner_id=owner.id,
        )
        self.db.add(db_restaurant)
        self.db.commit()
        self.db.refresh(db_restaurant)
        logger.info(f"Restaurant created successfully: ID={db_restaurant.id}, name='{db_restaurant.name}'")
        return db_restaurant
    
    def update_restaurant(self, restaurant_id: int, restaurant_data: RestaurantUpdate, current_user: User) -> Restaurant:
        """Update a restaurant."""
        db_restaurant = self.get_restaurant_by_id(restaurant_id)
        if not db_restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )
        
        # Check permissions: owner can update their own restaurant, admin can update any
        if current_user.role != UserRole.ADMIN and db_restaurant.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        # Update fields
        update_data = restaurant_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_restaurant, field, value)
        
        self.db.commit()
        self.db.refresh(db_restaurant)
        return db_restaurant
    
    def delete_restaurant(self, restaurant_id: int, current_user: User) -> bool:
        """Delete a restaurant."""
        db_restaurant = self.get_restaurant_by_id(restaurant_id)
        if not db_restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )
        
        # Check permissions
        if current_user.role != UserRole.ADMIN and db_restaurant.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        self.db.delete(db_restaurant)
        self.db.commit()
        return True

