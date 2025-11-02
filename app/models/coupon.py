from sqlalchemy import Column, Integer, String, Numeric, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Coupon(Base):
    """Coupon model for percentage discounts."""
    
    __tablename__ = "coupons"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False, index=True)
    discount_percentage = Column(Numeric(5, 2), nullable=False)  # e.g., 10.00 for 10%
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    orders = relationship("Order", back_populates="coupon")

