from sqlalchemy import Column, String, ForeignKey, Boolean, Uuid
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class Restaurant(Base):
    """Restaurant model."""

    __tablename__ = "restaurants"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    owner_id = Column(Uuid, ForeignKey("users.id"), nullable=False)
    is_blocked = Column(Boolean, default=False, nullable=False)

    # Relationships
    owner = relationship("User", back_populates="restaurants")
    meals = relationship("Meal", back_populates="restaurant", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="restaurant", cascade="all, delete-orphan")

