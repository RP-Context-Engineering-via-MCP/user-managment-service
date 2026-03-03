"""FastAPI Application Entry Point.

This module creates and configures the FastAPI application instance,
including middleware setup, router registration, and application lifecycle
event handlers for database initialization.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.db_init import init_db
from app.core.logging_config import setup_logging
from app.core.database import init_db as init_async_db, close_db
from app.api.user_routes import router as user_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager.
    
    Handles startup and shutdown events:
    
    Startup:
    1. Initialize sync database schema (tables, seed data)
    2. Verify async database connection
    
    Shutdown:
    1. Close async database connections
    """
    # === STARTUP ===
    logger.info("Starting User Management Service...")
    
    # Initialize sync database schema and seed data
    init_db()
    logger.info("Database schema initialized")
    
    # Verify async database connection
    try:
        await init_async_db()
        logger.info("Async database connection verified")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise
    
    logger.info("User Management Service started successfully")
    
    yield  # Service is running
    
    # === SHUTDOWN ===
    logger.info("Shutting down User Management Service...")
    
    # Close async database connections
    await close_db()
    logger.info("Database connections closed")
    
    logger.info("User Management Service shutdown complete")


def create_app() -> FastAPI:
    """Create and configure FastAPI application instance.
    
    Sets up:
    - Logging configuration
    - FastAPI app with metadata and lifespan manager
    - CORS middleware for cross-origin requests
    - API route registration
    
    Returns:
        FastAPI: Configured application instance ready to serve requests.
    """
    # Initialize logging
    setup_logging()
    
    app = FastAPI(
        title="User Management Service",
        version="1.0.0",
        description="User authentication and management service with OAuth support",
        lifespan=lifespan
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(user_router)

    return app


app = create_app()


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {
        "status": "running",
        "service": "User Management Service",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check endpoint.
    
    Returns service health status including component states.
    """
    return {
        "status": "healthy",
        "service": "User Management Service",
        "version": "1.0.0",
        "components": {
            "http_server": "running",
            "database": "connected"
        }
    }