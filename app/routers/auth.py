from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.user_service import UserService
from app.core.security import create_access_token
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    logger.info(f"Registration attempt for email: {user_data.email}")
    user_service = UserService(db)
    user = user_service.create_user(user_data)
    logger.info(f"User registered successfully: {user.email}")
    return user


@router.post("/login", response_model=Token)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """Login and get access token."""
    logger.info(f"Login attempt for email: {credentials.email}")
    user_service = UserService(db)
    user = user_service.authenticate_user(credentials.email, credentials.password)

    if not user:
        logger.warning(f"Failed login attempt for email: {credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    logger.info(f"User logged in successfully: {credentials.email}")
    return {"access_token": access_token, "token_type": "bearer"}

