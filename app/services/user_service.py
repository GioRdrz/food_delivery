from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.core.logger import get_logger

logger = get_logger(__name__)


class UserService:
    """Service for user-related business logic."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        logger.debug(f"Fetching user by email: {email}")
        user = self.db.query(User).filter(User.email == email).first()
        if user:
            logger.debug(f"User found: {user.id}")
        else:
            logger.debug(f"User not found for email: {email}")
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        logger.debug(f"Fetching user by ID: {user_id}")
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            logger.debug(f"User found: {user.email}")
        else:
            logger.warning(f"User not found with ID: {user_id}")
        return user
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        logger.info(f"Fetching users with skip={skip}, limit={limit}")
        users = self.db.query(User).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(users)} users")
        return users
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user."""
        logger.info(f"Creating new user with email: {user_data.email}, role: {user_data.role}")

        # Check if user already exists
        existing_user = self.get_user_by_email(user_data.email)
        if existing_user:
            logger.warning(f"Attempt to create user with existing email: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            role=user_data.role,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        logger.info(f"User created successfully: ID={db_user.id}, email={db_user.email}")
        return db_user
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """Update a user."""
        logger.info(f"Updating user: {user_id}")

        db_user = self.get_user_by_id(user_id)
        if not db_user:
            logger.error(f"User not found for update: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Check if email is being changed and if it's already taken
        if user_data.email and user_data.email != db_user.email:
            existing_user = self.get_user_by_email(user_data.email)
            if existing_user:
                logger.warning(f"Attempt to update to existing email: {user_data.email}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

        # Update fields
        update_data = user_data.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
            logger.debug("Password updated")

        for field, value in update_data.items():
            setattr(db_user, field, value)

        self.db.commit()
        self.db.refresh(db_user)
        logger.info(f"User updated successfully: {user_id}")
        return db_user
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user."""
        logger.info(f"Deleting user: {user_id}")

        db_user = self.get_user_by_id(user_id)
        if not db_user:
            logger.error(f"User not found for deletion: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        self.db.delete(db_user)
        self.db.commit()
        logger.info(f"User deleted successfully: {user_id}")
        return True

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user."""
        logger.info(f"Authenticating user: {email}")

        user = self.get_user_by_email(email)
        if not user:
            logger.warning(f"Authentication failed - user not found: {email}")
            return None
        if not verify_password(password, user.hashed_password):
            logger.warning(f"Authentication failed - invalid password: {email}")
            return None
        if not user.is_active or user.is_blocked:
            logger.warning(f"Authentication failed - user inactive or blocked: {email}")
            return None

        logger.info(f"User authenticated successfully: {email}")
        return user

    def create_admin_user(self, email: str, password: str) -> User:
        """Create an admin user (used for initial setup)."""
        logger.info(f"Creating admin user: {email}")

        existing_user = self.get_user_by_email(email)
        if existing_user:
            logger.info(f"Admin user already exists: {email}")
            return existing_user

        hashed_password = get_password_hash(password)
        db_user = User(
            email=email,
            hashed_password=hashed_password,
            full_name="Administrator",
            role=UserRole.ADMIN,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        logger.info(f"Admin user created successfully: {email}")
        return db_user

