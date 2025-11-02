from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from app.models.order import OrderStatus


class OrderItemCreate(BaseModel):
    """Schema for creating an order item."""
    meal_id: int
    quantity: int = Field(..., gt=0)


class OrderItemResponse(BaseModel):
    """Schema for order item response."""
    id: int
    meal_id: int
    quantity: int
    price_at_order: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrderStatusHistoryResponse(BaseModel):
    """Schema for order status history response."""
    id: int
    status: OrderStatus
    changed_at: datetime
    changed_by_user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    """Schema for creating an order."""
    restaurant_id: int
    items: List[OrderItemCreate] = Field(..., min_length=1)
    tip_amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    coupon_code: Optional[str] = None


class OrderUpdate(BaseModel):
    """Schema for updating an order."""
    tip_amount: Optional[Decimal] = Field(None, ge=0)


class OrderStatusUpdate(BaseModel):
    """Schema for updating order status."""
    status: OrderStatus


class OrderResponse(BaseModel):
    """Schema for order response."""
    id: int
    customer_id: int
    restaurant_id: int
    status: OrderStatus
    total_amount: Decimal
    tip_amount: Decimal
    coupon_id: Optional[int] = None
    created_at: datetime
    items: List[OrderItemResponse] = []
    status_history: List[OrderStatusHistoryResponse] = []

    model_config = ConfigDict(from_attributes=True)

