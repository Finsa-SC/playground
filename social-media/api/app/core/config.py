from functools import lru_cache
from pathlib import Path
from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", "../env/api.env"), extra="ignore")
    app_name: str = "FinSky API"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: SecretStr = SecretStr("postgresql+asyncpg://finsky:change-me@db:5432/finsky")
    jwt_secret_key: SecretStr = SecretStr("development-only-change-this-secret-key")
    access_token_expire_minutes: int = 30
    media_root: Path = Path("/app/storage/media")
    max_upload_size_mb: int = 50
    cors_origins: list[str] = []

    @field_validator("access_token_expire_minutes")
    @classmethod
    def token_lifetime_positive(cls, value: int) -> int:
        if value < 1:
            raise ValueError("access token lifetime must be positive")
        return value

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
