from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Bakery Shop API"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 15
    refresh_token_days: int = 7
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    public_base_url: str = "http://localhost:8000"
    image_storage_dir: str = "./storage/product-images"
    max_image_size_mb: int = 5
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
