# app/core/config.py

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # Database
    DATABASE_URL: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "taxflow_db"
    DB_USER: str = "taxflow_user"
    DB_PASSWORD: str = "secure_password"
    
    # Application
    APP_NAME: str = "TaxFlow AI"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"  # Load from .env file
        case_sensitive = False

# Create global settings instance
settings = Settings()

# Test it
if __name__ == "__main__":
    print(f"Database URL: {settings.DATABASE_URL}")
    print(f"App Name: {settings.APP_NAME}")