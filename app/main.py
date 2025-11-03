from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import engine, SessionLocal, Base
from app.routers import auth, users, restaurants, meals, orders, coupons
from app.services.user_service import UserService
from app.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown."""
    logger.info("Starting Food Delivery Service API...")

    # Startup: Create tables and initialize admin user
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")

    # Create built-in admin user
    logger.info("Initializing admin user...")
    db = SessionLocal()
    try:
        user_service = UserService(db)
        user_service.create_admin_user(settings.ADMIN_EMAIL, settings.ADMIN_PASSWORD)
        logger.info("Admin user initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing admin user: {e}")
    finally:
        db.close()

    logger.info("Application startup complete")
    yield

    # Shutdown
    logger.info("Shutting down Food Delivery Service API...")


app = FastAPI(
    title="Food Delivery Service API",
    description="A comprehensive food delivery service API with user authentication, restaurant management, and order processing",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(restaurants.router)
app.include_router(meals.router)
app.include_router(orders.router)
app.include_router(coupons.router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Food Delivery Service API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

