"""Application Configuration Module.

This module defines application-wide configuration settings using Pydantic BaseSettings.
Settings are loaded from environment variables or .env file and include:
- Database connection configuration
- JWT authentication settings  
- OAuth provider credentials

All sensitive values should be provided via environment variables in production.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application configuration settings.
    
    Loads configuration from environment variables or .env file.
    Provides type validation and default values for application settings.
    """
    # Database
    DATABASE_URL: str

    # Application
    APP_NAME: str = "User Management Service"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # JWT Authentication
    JWT_SECRET_KEY: str = "your-secret-key-change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # OAuth Providers
    GITHUB_CLIENT_ID: Optional[str] = None
    GITHUB_CLIENT_SECRET: Optional[str] = None
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
