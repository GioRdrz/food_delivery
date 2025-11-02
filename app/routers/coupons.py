from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.coupon import CouponCreate, CouponUpdate, CouponResponse
from app.services.coupon_service import CouponService
from app.models.user import User
from app.dependencies import get_current_user, get_current_admin

from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/coupons", tags=["Coupons"])


@router.get("/", response_model=List[CouponResponse])
def list_coupons(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """List all coupons (admin only)."""
    coupon_service = CouponService(db)
    coupons = coupon_service.get_coupons(skip=skip, limit=limit)
    return coupons


@router.get("/{coupon_id}", response_model=CouponResponse)
def get_coupon(
    coupon_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get a specific coupon (admin only)."""
    coupon_service = CouponService(db)
    coupon = coupon_service.get_coupon_by_id(coupon_id)
    
    if not coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coupon not found"
        )
    
    return coupon


@router.post("/", response_model=CouponResponse, status_code=status.HTTP_201_CREATED)
def create_coupon(
    coupon_data: CouponCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new coupon (admin only)."""
    coupon_service = CouponService(db)
    coupon = coupon_service.create_coupon(coupon_data)
    return coupon


@router.put("/{coupon_id}", response_model=CouponResponse)
def update_coupon(
    coupon_id: int,
    coupon_data: CouponUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update a coupon (admin only)."""
    coupon_service = CouponService(db)
    coupon = coupon_service.update_coupon(coupon_id, coupon_data)
    return coupon


@router.delete("/{coupon_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coupon(
    coupon_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete a coupon (admin only)."""
    coupon_service = CouponService(db)
    coupon_service.delete_coupon(coupon_id)
    return None

