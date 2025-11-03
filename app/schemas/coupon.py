from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal
from uuid import UUID


class CouponBase(BaseModel):
    """Base coupon schema."""
    code: str = Field(..., min_length=1)
    discount_percentage: Decimal = Field(..., gt=0, le=100)


class CouponCreate(CouponBase):
    """Schema for creating a coupon."""
    pass


class CouponUpdate(BaseModel):
    """Schema for updating a coupon."""
    code: Optional[str] = Field(None, min_length=1)
    discount_percentage: Optional[Decimal] = Field(None, gt=0, le=100)
    is_active: Optional[bool] = None


class CouponResponse(CouponBase):
    """Schema for coupon response."""
    id: UUID
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

