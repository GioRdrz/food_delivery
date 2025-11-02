# Logging Documentation

This document describes the logging implementation in the Food Delivery Service API.

## Overview

The application uses Python's built-in `logging` module with a custom configuration that provides:

- **Structured logging** across all services and routers
- **Colored console output** for better readability during development
- **File-based logging** for production monitoring
- **Configurable log levels** via environment variables
- **Consistent log format** across the application

## Configuration

### Environment Variables

Configure logging in your `.env` file:

```env
LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Log Levels

| Level | Description | Use Case |
|-------|-------------|----------|
| **DEBUG** | Detailed diagnostic information | Development, troubleshooting |
| **INFO** | General informational messages | Normal operation tracking |
| **WARNING** | Warning messages for potential issues | Suspicious activity, deprecated features |
| **ERROR** | Error messages for failures | Failed operations, exceptions |
| **CRITICAL** | Critical issues requiring immediate attention | System failures, data corruption |

## Log Output

### Console Output

Console logs include colored output for easy visual scanning:

- **DEBUG**: Cyan
- **INFO**: Green
- **WARNING**: Yellow
- **ERROR**: Red
- **CRITICAL**: Magenta

Format:
```
2024-01-01 12:00:00 - app.services.user_service - INFO - User created successfully: ID=1, email=user@example.com
```

### File Output

Logs are written to `logs/app.log` with detailed information:

Format:
```
2024-01-01 12:00:00 - app.services.user_service - INFO - create_user:71 - User created successfully: ID=1, email=user@example.com
```

The file format includes:
- Timestamp
- Logger name (module path)
- Log level
- Function name and line number
- Log message

## Logging in Code

### Services

All services include comprehensive logging:

```python
from app.core.logger import get_logger

logger = get_logger(__name__)

class UserService:
    def create_user(self, user_data: UserCreate) -> User:
        logger.info(f"Creating new user with email: {user_data.email}")
        
        # ... business logic ...
        
        logger.info(f"User created successfully: ID={db_user.id}")
        return db_user
```

### Routers

All routers log incoming requests and responses:

```python
from app.core.logger import get_logger

logger = get_logger(__name__)

@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Registration attempt for email: {user_data.email}")
    # ... handle request ...
    logger.info(f"User registered successfully: {user.email}")
    return user
```

## What Gets Logged

### Authentication Events

- **INFO**: Successful login/registration
- **WARNING**: Failed login attempts, blocked users
- **ERROR**: Authentication errors

Example:
```
INFO - Login attempt for email: user@example.com
INFO - User authenticated successfully: user@example.com
WARNING - Failed login attempt for email: hacker@example.com
```

### User Management

- **INFO**: User creation, updates, deletions
- **WARNING**: Attempts to create duplicate users
- **ERROR**: User not found errors

Example:
```
INFO - Creating new user with email: user@example.com, role: customer
INFO - User created successfully: ID=1, email=user@example.com
WARNING - Attempt to create user with existing email: user@example.com
```

### Restaurant Operations

- **INFO**: Restaurant creation, updates
- **WARNING**: Permission violations
- **DEBUG**: Restaurant queries

Example:
```
INFO - Creating restaurant 'Italian Delight' for owner 2
INFO - Restaurant created successfully: ID=1, name='Italian Delight'
WARNING - User 3 with role customer attempted to create restaurant
```

### Order Processing

- **INFO**: Order creation, status changes
- **WARNING**: Invalid status transitions, permission violations
- **ERROR**: Order validation failures

Example:
```
INFO - Creating order for customer 1 at restaurant 1
INFO - Order created successfully: ID=1, total=45.99
WARNING - Non-customer user 2 attempted to place order
```

### Application Lifecycle

- **INFO**: Startup and shutdown events
- **ERROR**: Initialization failures

Example:
```
INFO - Starting Food Delivery Service API...
INFO - Creating database tables...
INFO - Database tables created successfully
INFO - Initializing admin user...
INFO - Admin user initialized successfully
INFO - Application startup complete
```

## Log File Management

### Location

All logs are stored in the `logs/` directory:
```
logs/
└── app.log
```

### Rotation

For production deployments, consider implementing log rotation:

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=10485760,  # 10MB
    backupCount=5
)
```

Or use external tools like `logrotate` on Linux:

```
/path/to/logs/app.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0644 user group
}
```

### Cleanup

Log files are excluded from version control via `.gitignore`:
```
logs/*.log
logs/*.txt
```

## Monitoring and Analysis

### Viewing Logs in Real-Time

```bash
# Follow the log file
tail -f logs/app.log

# Filter for errors
tail -f logs/app.log | grep ERROR

# Filter for specific user
tail -f logs/app.log | grep "user@example.com"
```

### Searching Logs

```bash
# Find all failed login attempts
grep "Failed login attempt" logs/app.log

# Find all orders created today
grep "$(date +%Y-%m-%d)" logs/app.log | grep "Order created"

# Count errors by type
grep ERROR logs/app.log | cut -d'-' -f4 | sort | uniq -c
```

### Log Analysis Tools

Consider using these tools for advanced log analysis:

- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Grafana Loki**
- **Splunk**
- **Datadog**
- **CloudWatch** (AWS)

## Best Practices

### Do's

✅ **Log important business events**
```python
logger.info(f"Order {order_id} status changed from {old_status} to {new_status}")
```

✅ **Log security events**
```python
logger.warning(f"Failed login attempt for email: {email}")
```

✅ **Log errors with context**
```python
logger.error(f"Failed to process payment for order {order_id}: {str(e)}")
```

✅ **Use appropriate log levels**
```python
logger.debug("Fetching user by ID: 123")  # Development only
logger.info("User created successfully")   # Normal operations
logger.warning("Deprecated API endpoint used")  # Potential issues
logger.error("Database connection failed")  # Errors
```

### Don'ts

❌ **Don't log sensitive information**
```python
# BAD
logger.info(f"User password: {password}")
logger.info(f"Credit card: {card_number}")

# GOOD
logger.info(f"User authenticated: {email}")
logger.info(f"Payment processed for order {order_id}")
```

❌ **Don't log in tight loops**
```python
# BAD
for item in items:
    logger.debug(f"Processing item {item.id}")  # Too verbose

# GOOD
logger.info(f"Processing {len(items)} items")
```

❌ **Don't use print() statements**
```python
# BAD
print("User created")

# GOOD
logger.info("User created")
```

## Troubleshooting

### Logs Not Appearing

1. Check LOG_LEVEL in `.env`
2. Verify logs directory exists and is writable
3. Check file permissions on `logs/app.log`

### Too Many Logs

1. Increase LOG_LEVEL to WARNING or ERROR
2. Implement log filtering
3. Set up log rotation

### Performance Impact

Logging has minimal performance impact, but for high-traffic applications:

1. Use async logging handlers
2. Buffer log writes
3. Use appropriate log levels (avoid DEBUG in production)

## Example Log Output

```
2024-01-01 12:00:00 - app.main - INFO - Starting Food Delivery Service API...
2024-01-01 12:00:00 - app.main - INFO - Creating database tables...
2024-01-01 12:00:00 - app.main - INFO - Database tables created successfully
2024-01-01 12:00:00 - app.main - INFO - Initializing admin user...
2024-01-01 12:00:00 - app.services.user_service - INFO - Creating admin user: admin@fooddelivery.com
2024-01-01 12:00:00 - app.services.user_service - INFO - Admin user created successfully: admin@fooddelivery.com
2024-01-01 12:00:00 - app.main - INFO - Application startup complete
2024-01-01 12:00:05 - app.routers.auth - INFO - Registration attempt for email: customer@example.com
2024-01-01 12:00:05 - app.services.user_service - INFO - Creating new user with email: customer@example.com, role: customer
2024-01-01 12:00:05 - app.services.user_service - INFO - User created successfully: ID=2, email=customer@example.com
2024-01-01 12:00:05 - app.routers.auth - INFO - User registered successfully: customer@example.com
2024-01-01 12:00:10 - app.routers.auth - INFO - Login attempt for email: customer@example.com
2024-01-01 12:00:10 - app.services.user_service - INFO - Authenticating user: customer@example.com
2024-01-01 12:00:10 - app.services.user_service - INFO - User authenticated successfully: customer@example.com
2024-01-01 12:00:10 - app.routers.auth - INFO - User logged in successfully: customer@example.com
```

## Summary

The logging system provides comprehensive visibility into application behavior, making it easier to:

- **Debug issues** during development
- **Monitor operations** in production
- **Track security events** and suspicious activity
- **Analyze performance** and usage patterns
- **Audit business operations** and compliance

All logs are structured, consistent, and easy to parse for automated analysis.

