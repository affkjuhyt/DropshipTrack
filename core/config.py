from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import validator

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Dropship Tracker"
    
    # Environment Settings
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    # Database Settings
    DATABASE_URL: str
    REPLICA_URL: Optional[str] = None
    
    # Redis Settings
    REDIS_URL: str
    
    # Kafka Settings
    KAFKA_BROKER: str
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: list = ["http://localhost:8000", "http://localhost:3000", "http://localhost:3001"]
    
    # Default Currency Settings
    DEFAULT_CURRENCY_CODE_LENGTH: int = 3
    DEFAULT_MAX_DIGITS: int = 12  # Maximum number of digits for decimal fields
    DEFAULT_DECIMAL_PLACES: int = 2  # Number of decimal places for currency
    LANGUAGE_CODE: str = "en-us"
    
    @validator("ENVIRONMENT")
    def validate_environment(cls, v: str) -> str:
        if v not in ["development", "production", "test"]:
            raise ValueError("Invalid environment")
        return v
    
    @validator("DATABASE_URL")
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith("postgresql://"):
            raise ValueError("DATABASE_URL must be a PostgreSQL connection string")
        return v
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
