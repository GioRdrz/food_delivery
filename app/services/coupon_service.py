from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID

from app.models.coupon import Coupon
from app.schemas.coupon import CouponCreate, CouponUpdate
from app.core.logger import get_logger

logger = get_logger(__name__)


class CouponService:
    """Service for coupon-related business logic."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_coupon_by_id(self, coupon_id: UUID) -> Optional[Coupon]:
        """Get a coupon by ID."""
        return self.db.query(Coupon).filter(Coupon.id == coupon_id).first()
    
    def get_coupon_by_code(self, code: str) -> Optional[Coupon]:
        """Get a coupon by code."""
        return self.db.query(Coupon).filter(Coupon.code == code).first()
    
    def get_coupons(self, skip: int = 0, limit: int = 100) -> List[Coupon]:
        """Get all coupons with pagination."""
        return self.db.query(Coupon).offset(skip).limit(limit).all()
    
    def create_coupon(self, coupon_data: CouponCreate) -> Coupon:
        """Create a new coupon."""
        # Check if coupon code already exists
        existing_coupon = self.get_coupon_by_code(coupon_data.code)
        if existing_coupon:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coupon code already exists"
            )
        
        db_coupon = Coupon(
            code=coupon_data.code,
            discount_percentage=coupon_data.discount_percentage,
        )
        self.db.add(db_coupon)
        self.db.commit()
        self.db.refresh(db_coupon)
        return db_coupon
    
    def update_coupon(self, coupon_id: UUID, coupon_data: CouponUpdate) -> Coupon:
        """Update a coupon."""
        db_coupon = self.get_coupon_by_id(coupon_id)
        if not db_coupon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coupon not found"
            )
        
        # Check if code is being changed and if it already exists
        if coupon_data.code and coupon_data.code != db_coupon.code:
            existing_coupon = self.get_coupon_by_code(coupon_data.code)
            if existing_coupon:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Coupon code already exists"
                )
        
        # Update fields
        update_data = coupon_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_coupon, field, value)
        
        self.db.commit()
        self.db.refresh(db_coupon)
        return db_coupon
    
    def delete_coupon(self, coupon_id: UUID) -> bool:
        """Delete a coupon."""
        db_coupon = self.get_coupon_by_id(coupon_id)
        if not db_coupon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coupon not found"
            )

        self.db.delete(db_coupon)
        self.db.commit()
        return True

