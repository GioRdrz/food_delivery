from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal


class MealBase(BaseModel):
    """Base meal schema."""
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)


class MealCreate(MealBase):
    """Schema for creating a meal."""
    restaurant_id: int


class MealUpdate(BaseModel):
    """Schema for updating a meal."""
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0)
    is_blocked: Optional[bool] = None


class MealResponse(MealBase):
    """Schema for meal response."""
    id: int
    restaurant_id: int
    is_blocked: bool

    model_config = ConfigDict(from_attributes=True)

