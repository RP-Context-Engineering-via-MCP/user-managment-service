"""Database Initialization Module.

This module handles database schema creation for the User Management Service.
Ensures all ORM models are registered with SQLAlchemy.

All operations are idempotent and safe to run multiple times.
"""

from app.core.database import engine, Base

# Import user model to ensure it's registered with SQLAlchemy
from app.models import user


def init_db() -> None:
    """Initialize complete database schema.
    
    Creates all tables from ORM model metadata.
    Safe to run multiple times - operation is idempotent.
    Call during application startup to ensure database readiness.
    
    Raises:
        Exception: If schema creation fails.
    """
    Base.metadata.create_all(bind=engine)