# Pydantic v2 Migration

## Overview

The project has been updated to use Pydantic v2's `ConfigDict` instead of the deprecated class-based `Config` pattern.

## Changes Made

### Deprecated Pattern (Pydantic v1)

```python
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    email: str
    
    class Config:
        from_attributes = True
```

### New Pattern (Pydantic v2)

```python
from pydantic import BaseModel, ConfigDict

class UserResponse(BaseModel):
    id: int
    email: str
    
    model_config = ConfigDict(from_attributes=True)
```

## Files Updated

All schema files have been migrated to use `ConfigDict`:

1. **app/schemas/user.py**
   - `UserResponse` - Updated to use `model_config = ConfigDict(from_attributes=True)`

2. **app/schemas/restaurant.py**
   - `RestaurantResponse` - Updated to use `model_config = ConfigDict(from_attributes=True)`

3. **app/schemas/meal.py**
   - `MealResponse` - Updated to use `model_config = ConfigDict(from_attributes=True)`

4. **app/schemas/order.py**
   - `OrderItemResponse` - Updated to use `model_config = ConfigDict(from_attributes=True)`
   - `OrderStatusHistoryResponse` - Updated to use `model_config = ConfigDict(from_attributes=True)`
   - `OrderResponse` - Updated to use `model_config = ConfigDict(from_attributes=True)`

5. **app/schemas/coupon.py**
   - `CouponResponse` - Updated to use `model_config = ConfigDict(from_attributes=True)`

## Benefits

1. **No Deprecation Warnings**: Eliminates `PydanticDeprecatedSince20` warnings
2. **Future-Proof**: Compatible with Pydantic v2 and future versions
3. **Better Type Safety**: ConfigDict provides better IDE support and type checking
4. **Consistent with Best Practices**: Follows Pydantic v2 recommended patterns

## Testing

All tests pass successfully after the migration:

```bash
pytest tests/ -v
# 16 passed in 8.20s
```

## Configuration Settings

The project already uses Pydantic v2's `SettingsConfigDict` in `app/config.py`:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    # ... other settings ...
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )
```

## Migration Checklist

- [x] Updated all schema response classes to use `ConfigDict`
- [x] Added `ConfigDict` import to all schema files
- [x] Replaced `class Config:` with `model_config = ConfigDict(...)`
- [x] Verified no deprecation warnings
- [x] Ran all tests successfully
- [x] Verified schema imports work correctly

## References

- [Pydantic v2 Migration Guide](https://docs.pydantic.dev/latest/migration/)
- [Pydantic v2 Configuration](https://docs.pydantic.dev/latest/api/config/)
- [ConfigDict Documentation](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict)

## Summary

The migration from Pydantic v1's class-based `Config` to Pydantic v2's `ConfigDict` is complete. All schemas now use the modern pattern, eliminating deprecation warnings and ensuring compatibility with current and future versions of Pydantic.

