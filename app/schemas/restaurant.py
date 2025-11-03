from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID


class RestaurantBase(BaseModel):
    """Base restaurant schema."""
    name: str = Field(..., min_length=1)
    description: Optional[str] = None


class RestaurantCreate(RestaurantBase):
    """Schema for creating a restaurant."""
    pass


class RestaurantUpdate(BaseModel):
    """Schema for updating a restaurant."""
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    is_blocked: Optional[bool] = None


class RestaurantResponse(RestaurantBase):
    """Schema for restaurant response."""
    id: UUID
    owner_id: UUID
    is_blocked: bool

    model_config = ConfigDict(from_attributes=True)

