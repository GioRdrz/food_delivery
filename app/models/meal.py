from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Meal(Base):
    """Meal model."""
    
    __tablename__ = "meals"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    is_blocked = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    restaurant = relationship("Restaurant", back_populates="meals")
    order_items = relationship("OrderItem", back_populates="meal")

