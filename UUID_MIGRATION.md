# UUID Migration Documentation

## Overview

The Food Delivery Service API has been migrated from using integer-based primary keys to UUID (Universally Unique Identifier) based primary keys across all database tables.

## Migration Date

**Completed:** November 2, 2024

## Why UUID?

### Benefits

1. **Global Uniqueness**: UUIDs are globally unique, eliminating the risk of ID collisions across distributed systems
2. **Security**: UUIDs are non-sequential, making it harder to enumerate or predict resource IDs
3. **Scalability**: UUIDs can be generated independently without database coordination
4. **Distributed Systems**: Better support for microservices and distributed architectures
5. **Data Privacy**: Harder to infer business metrics (e.g., number of users) from IDs

### Trade-offs

1. **Storage**: UUIDs require 16 bytes vs 4 bytes for integers
2. **Readability**: UUIDs are less human-readable than sequential integers
3. **Index Performance**: Slightly larger index sizes (mitigated by using UUID v4)

## Changes Made

### Database Models

All SQLAlchemy models were updated to use UUID primary keys:

**Before:**
```python
from sqlalchemy import Column, Integer

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
```

**After:**
```python
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
```

### Affected Tables

All 7 database tables were migrated:

1. **users**
   - `id`: INTEGER → UUID

2. **restaurants**
   - `id`: INTEGER → UUID
   - `owner_id`: INTEGER → UUID (FK to users.id)

3. **meals**
   - `id`: INTEGER → UUID
   - `restaurant_id`: INTEGER → UUID (FK to restaurants.id)

4. **orders**
   - `id`: INTEGER → UUID
   - `customer_id`: INTEGER → UUID (FK to users.id)
   - `restaurant_id`: INTEGER → UUID (FK to restaurants.id)
   - `coupon_id`: INTEGER → UUID (FK to coupons.id)

5. **order_items**
   - `id`: INTEGER → UUID
   - `order_id`: INTEGER → UUID (FK to orders.id)
   - `meal_id`: INTEGER → UUID (FK to meals.id)

6. **order_status_history**
   - `id`: INTEGER → UUID
   - `order_id`: INTEGER → UUID (FK to orders.id)
   - `changed_by_user_id`: INTEGER → UUID (FK to users.id)

7. **coupons**
   - `id`: INTEGER → UUID

### Pydantic Schemas

All Pydantic schemas were updated to use UUID type:

**Before:**
```python
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    email: str
```

**After:**
```python
from pydantic import BaseModel
from uuid import UUID

class UserResponse(BaseModel):
    id: UUID
    email: str
```

### API Routers

All FastAPI router path parameters were updated:

**Before:**
```python
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    ...
```

**After:**
```python
from uuid import UUID

@router.get("/{user_id}")
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    ...
```

### Service Layer

All service methods were updated with UUID type hints:

**Before:**
```python
def get_user_by_id(self, user_id: int) -> Optional[User]:
    return self.db.query(User).filter(User.id == user_id).first()
```

**After:**
```python
from uuid import UUID

def get_user_by_id(self, user_id: UUID) -> Optional[User]:
    return self.db.query(User).filter(User.id == user_id).first()
```

## Files Modified

### Models (6 files)
- `app/models/user.py`
- `app/models/restaurant.py`
- `app/models/meal.py`
- `app/models/order.py`
- `app/models/coupon.py`

### Schemas (5 files)
- `app/schemas/user.py`
- `app/schemas/restaurant.py`
- `app/schemas/meal.py`
- `app/schemas/order.py`
- `app/schemas/coupon.py`

### Routers (6 files)
- `app/routers/auth.py`
- `app/routers/users.py`
- `app/routers/restaurants.py`
- `app/routers/meals.py`
- `app/routers/orders.py`
- `app/routers/coupons.py`

### Services (5 files)
- `app/services/user_service.py`
- `app/services/restaurant_service.py`
- `app/services/meal_service.py`
- `app/services/order_service.py`
- `app/services/coupon_service.py`

## Database Migration

### Migration Strategy

Due to the incompatibility between INTEGER and UUID types, a fresh database schema was created:

1. **Dropped** all existing tables
2. **Created** new Alembic migration: `718209df302e_initial_uuid_schema.py`
3. **Applied** migration to create tables with UUID columns

### Migration File

Location: `alembic/versions/718209df302e_initial_uuid_schema.py`

This migration creates all tables with UUID primary keys and foreign keys from scratch.

## API Changes

### Request/Response Format

**Before:**
```json
{
  "id": 123,
  "email": "user@example.com"
}
```

**After:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com"
}
```

### URL Path Parameters

**Before:**
```
GET /api/users/123
```

**After:**
```
GET /api/users/550e8400-e29b-41d4-a716-446655440000
```

## Testing

### Verification

A test was performed to verify UUID functionality:

```python
import uuid
from app.models.user import User

# Create user with UUID
test_user = User(
    id=uuid.uuid4(),
    email='test@example.com',
    ...
)
db.add(test_user)
db.commit()

# Query by UUID
queried_user = db.query(User).filter(User.id == test_user.id).first()
assert queried_user.id == test_user.id  # ✅ Success
```

### Test Results

✅ All database tables created with UUID columns  
✅ UUID generation working correctly  
✅ UUID queries working correctly  
✅ Foreign key relationships maintained  
✅ API endpoints accepting UUID parameters  
✅ Pydantic validation working with UUIDs  

## Breaking Changes

⚠️ **This is a breaking change** - existing data cannot be automatically migrated from INTEGER to UUID.

### Impact

1. **Database**: Requires fresh database creation or manual data migration
2. **API Clients**: Must update to use UUID format in requests
3. **Stored References**: Any stored integer IDs are now invalid

### Migration Path for Existing Data

If you have existing data to preserve:

1. Export data from old schema
2. Generate new UUIDs for each record
3. Update foreign key references
4. Import into new UUID-based schema

## Usage Examples

### Creating Records

```python
import uuid
from app.models.user import User

# UUID is auto-generated
user = User(
    email="user@example.com",
    # id will be automatically set to uuid.uuid4()
)

# Or specify UUID explicitly
user = User(
    id=uuid.uuid4(),
    email="user@example.com"
)
```

### Querying Records

```python
from uuid import UUID

# Query by UUID
user_id = UUID("550e8400-e29b-41d4-a716-446655440000")
user = db.query(User).filter(User.id == user_id).first()

# Query by UUID string (converted automatically)
user_id_str = "550e8400-e29b-41d4-a716-446655440000"
user = db.query(User).filter(User.id == UUID(user_id_str)).first()
```

### API Requests

```bash
# Get user by UUID
curl http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000

# Create order with UUID references
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "restaurant_id": "550e8400-e29b-41d4-a716-446655440000",
    "items": [
      {
        "meal_id": "660e8400-e29b-41d4-a716-446655440001",
        "quantity": 2
      }
    ]
  }'
```

## Best Practices

1. **Let the database generate UUIDs**: Use `default=uuid.uuid4` in models
2. **Use UUID type hints**: Always use `from uuid import UUID` for type safety
3. **Validate UUID format**: FastAPI automatically validates UUID format in path parameters
4. **Index UUID columns**: UUIDs are indexed for performance (already configured)
5. **Use string representation**: When logging or displaying UUIDs, use `str(uuid_value)`

## Rollback

To rollback to integer IDs (not recommended):

1. Revert all code changes to use `Integer` instead of `UUID`
2. Create new Alembic migration
3. Drop and recreate database

## Support

For questions or issues related to the UUID migration, please contact the development team.

---

**Migration Status:** ✅ Complete  
**Database Schema Version:** `718209df302e_initial_uuid_schema`  
**Compatibility:** PostgreSQL 9.4+

