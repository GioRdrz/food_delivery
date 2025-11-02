from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from decimal import Decimal
from datetime import datetime
from uuid import UUID

from app.models.order import Order, OrderItem, OrderStatusHistory, OrderStatus
from app.models.user import User, UserRole
from app.schemas.order import OrderCreate, OrderUpdate, OrderStatusUpdate
from app.services.meal_service import MealService
from app.services.restaurant_service import RestaurantService
from app.services.coupon_service import CouponService
from app.core.logger import get_logger

logger = get_logger(__name__)


class OrderService:
    """Service for order-related business logic."""
    
    def __init__(self, db: Session):
        self.db = db
        self.meal_service = MealService(db)
        self.restaurant_service = RestaurantService(db)
        self.coupon_service = CouponService(db)
    
    def get_order_by_id(self, order_id: UUID) -> Optional[Order]:
        """Get an order by ID."""
        return self.db.query(Order).filter(Order.id == order_id).first()

    def get_orders(self, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get all orders with pagination."""
        return self.db.query(Order).offset(skip).limit(limit).all()

    def get_orders_by_customer(self, customer_id: UUID) -> List[Order]:
        """Get all orders for a specific customer."""
        return self.db.query(Order).filter(Order.customer_id == customer_id).all()

    def get_orders_by_restaurant(self, restaurant_id: UUID) -> List[Order]:
        """Get all orders for a specific restaurant."""
        return self.db.query(Order).filter(Order.restaurant_id == restaurant_id).all()
    
    def create_order(self, order_data: OrderCreate, customer: User) -> Order:
        """Create a new order."""
        logger.info(f"Creating order for customer {customer.id} at restaurant {order_data.restaurant_id}")

        # Verify customer role
        if customer.role != UserRole.CUSTOMER:
            logger.warning(f"Non-customer user {customer.id} attempted to place order")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only customers can place orders"
            )
        
        # Verify restaurant exists
        restaurant = self.restaurant_service.get_restaurant_by_id(order_data.restaurant_id)
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )
        
        if restaurant.is_blocked:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Restaurant is blocked"
            )
        
        # Verify all meals exist and belong to the same restaurant
        total_amount = Decimal("0.00")
        meal_items = []
        
        for item in order_data.items:
            meal = self.meal_service.get_meal_by_id(item.meal_id)
            if not meal:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Meal with ID {item.meal_id} not found"
                )
            
            if meal.is_blocked:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Meal {meal.name} is blocked"
                )
            
            if meal.restaurant_id != order_data.restaurant_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="All meals must be from the same restaurant"
                )
            
            item_total = meal.price * item.quantity
            total_amount += item_total
            meal_items.append((meal, item.quantity))
        
        # Apply coupon if provided
        coupon_id = None
        if order_data.coupon_code:
            coupon = self.coupon_service.get_coupon_by_code(order_data.coupon_code)
            if not coupon:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Coupon not found"
                )
            if not coupon.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Coupon is not active"
                )
            
            discount = total_amount * (coupon.discount_percentage / 100)
            total_amount -= discount
            coupon_id = coupon.id
        
        # Add tip
        total_amount += order_data.tip_amount
        
        # Create order
        db_order = Order(
            customer_id=customer.id,
            restaurant_id=order_data.restaurant_id,
            status=OrderStatus.PLACED,
            total_amount=total_amount,
            tip_amount=order_data.tip_amount,
            coupon_id=coupon_id,
        )
        self.db.add(db_order)
        self.db.flush()  # Get the order ID
        
        # Create order items
        for meal, quantity in meal_items:
            order_item = OrderItem(
                order_id=db_order.id,
                meal_id=meal.id,
                quantity=quantity,
                price_at_order=meal.price,
            )
            self.db.add(order_item)
        
        # Create initial status history
        status_history = OrderStatusHistory(
            order_id=db_order.id,
            status=OrderStatus.PLACED,
            changed_by_user_id=customer.id,
        )
        self.db.add(status_history)
        
        self.db.commit()
        self.db.refresh(db_order)
        return db_order
    
    def update_order_status(self, order_id: UUID, status_data: OrderStatusUpdate, current_user: User) -> Order:
        """Update order status with permission and workflow validation."""
        db_order = self.get_order_by_id(order_id)
        if not db_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Validate status transition
        self._validate_status_transition(db_order, status_data.status, current_user)
        
        # Update status
        db_order.status = status_data.status
        
        # Add to status history
        status_history = OrderStatusHistory(
            order_id=db_order.id,
            status=status_data.status,
            changed_by_user_id=current_user.id,
        )
        self.db.add(status_history)
        
        self.db.commit()
        self.db.refresh(db_order)
        return db_order
    
    def _validate_status_transition(self, order: Order, new_status: OrderStatus, user: User):
        """Validate if the status transition is allowed."""
        current_status = order.status
        
        # Define allowed transitions
        allowed_transitions = {
            OrderStatus.PLACED: [OrderStatus.CANCELED, OrderStatus.PROCESSING],
            OrderStatus.PROCESSING: [OrderStatus.CANCELED, OrderStatus.IN_ROUTE],
            OrderStatus.IN_ROUTE: [OrderStatus.DELIVERED],
            OrderStatus.DELIVERED: [OrderStatus.RECEIVED],
            OrderStatus.CANCELED: [],  # Terminal state
            OrderStatus.RECEIVED: [],  # Terminal state
        }
        
        if new_status not in allowed_transitions.get(current_status, []):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot transition from {current_status} to {new_status}"
            )
        
        # Check permissions for status changes
        restaurant = self.restaurant_service.get_restaurant_by_id(order.restaurant_id)
        
        # Customer can only cancel (from PLACED) or mark as RECEIVED (from DELIVERED)
        if user.role == UserRole.CUSTOMER:
            if user.id != order.customer_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not your order"
                )
            if new_status not in [OrderStatus.CANCELED, OrderStatus.RECEIVED]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Customers can only cancel orders or mark them as received"
                )
            if new_status == OrderStatus.CANCELED and current_status != OrderStatus.PLACED:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Can only cancel orders that are in PLACED status"
                )
        
        # Restaurant owner can cancel, process, mark in route, or delivered
        elif user.role == UserRole.RESTAURANT_OWNER:
            if user.id != restaurant.owner_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not your restaurant's order"
                )
            if new_status == OrderStatus.RECEIVED:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only customers can mark orders as received"
                )
        
        # Admin can do anything (no additional checks needed)
    
    def delete_order(self, order_id: UUID, current_user: User) -> bool:
        """Delete an order (admin only)."""
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can delete orders"
            )

        db_order = self.get_order_by_id(order_id)
        if not db_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        self.db.delete(db_order)
        self.db.commit()
        return True

