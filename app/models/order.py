from sqlalchemy import Column, ForeignKey, Numeric, DateTime, Enum as SQLEnum, Uuid
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

from app.database import Base


class OrderStatus(str, enum.Enum):
    """Order status enumeration."""
    PLACED = "placed"
    CANCELED = "canceled"
    PROCESSING = "processing"
    IN_ROUTE = "in_route"
    DELIVERED = "delivered"
    RECEIVED = "received"


class Order(Base):
    """Order model."""

    __tablename__ = "orders"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    customer_id = Column(Uuid, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(Uuid, ForeignKey("restaurants.id"), nullable=False)
    status = Column(SQLEnum(OrderStatus), nullable=False, default=OrderStatus.PLACED)
    total_amount = Column(Numeric(10, 2), nullable=False)
    tip_amount = Column(Numeric(10, 2), default=0.00, nullable=False)
    coupon_id = Column(Uuid, ForeignKey("coupons.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    customer = relationship("User", back_populates="orders")
    restaurant = relationship("Restaurant", back_populates="orders")
    coupon = relationship("Coupon", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    status_history = relationship("OrderStatusHistory", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    """Order item model for meals in an order."""

    __tablename__ = "order_items"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    order_id = Column(Uuid, ForeignKey("orders.id"), nullable=False)
    meal_id = Column(Uuid, ForeignKey("meals.id"), nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False, default=1)
    price_at_order = Column(Numeric(10, 2), nullable=False)  # Store price at time of order

    # Relationships
    order = relationship("Order", back_populates="items")
    meal = relationship("Meal", back_populates="order_items")


class OrderStatusHistory(Base):
    """Order status history model for tracking status changes."""

    __tablename__ = "order_status_history"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    order_id = Column(Uuid, ForeignKey("orders.id"), nullable=False)
    status = Column(SQLEnum(OrderStatus), nullable=False)
    changed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    changed_by_user_id = Column(Uuid, ForeignKey("users.id"), nullable=True)

    # Relationships
    order = relationship("Order", back_populates="status_history")

