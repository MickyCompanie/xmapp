from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

current_dir = Path(__file__).resolve().parent
env_path = current_dir.parent.parent / ".env"

class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    VERSION: str
    PREFIX: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRY: int
    REFRESH_TOKEN_EXPIRY: int

    model_config = SettingsConfigDict(
        env_file=env_path,
        env_file_encoding="utf-8",
        extra="ignore"
        )
    
Config = Settings()