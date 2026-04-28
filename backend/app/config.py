from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Syllabus to Coursera Recommender"
    app_env: str = "development"
    app_secret_key: str = Field(default="change-me-in-production")
    cors_origins: str = Field(default="*")

    database_url: str = Field(default="sqlite:///./app.db")

    jwt_algorithm: str = "HS256"
    jwt_exp_minutes: int = 60 * 8

    embedding_provider: str = "local-hash"
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536
    openai_api_key: str | None = None

    coursera_api_base_url: str = "https://api.coursera.org/api"
    coursera_api_token: str | None = None
    coursera_default_feed_path: str = "data/coursera_sample_feed.json"
    coursera_api_page_size: int = 100
    bootstrap_admin_email: str | None = None
    bootstrap_admin_password: str | None = None
    bootstrap_admin_name: str = "Admin User"
    bootstrap_admin_department: str = "Information Systems"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
