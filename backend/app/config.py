"""Application configuration via Pydantic BaseSettings.

All configuration is loaded from environment variables with sensible defaults
for local development. In production, values are injected via container env
or secret mounts.
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────────────────────────
    app_name: str = "business-copilot"
    app_env: Literal["development", "staging", "production"] = "development"
    app_debug: bool = True
    app_version: str = "0.1.0"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_log_level: str = "DEBUG"

    # ── Security ─────────────────────────────────────────────────────────
    secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 7

    # ── Database ─────────────────────────────────────────────────────────
    postgres_host: str = "localhost"
    postgres_port: int = 5433
    postgres_user: str = "copilot"
    postgres_password: str = "copilot_dev_password"
    postgres_db: str = "copilot"

    @property
    def database_url(self) -> str:
        """Async database URL for SQLAlchemy."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def database_url_sync(self) -> str:
        """Sync database URL for Alembic migrations."""
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    # ── Redis ────────────────────────────────────────────────────────────
    redis_host: str = "localhost"
    redis_port: int = 6380
    redis_password: str = ""

    redis_broker_db: int = 0
    redis_cache_db: int = 1
    redis_session_db: int = 2
    redis_ratelimit_db: int = 3
    redis_memory_db: int = 4

    @property
    def redis_url(self) -> str:
        """Base Redis URL."""
        auth = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{auth}{self.redis_host}:{self.redis_port}"

    @property
    def celery_broker_url(self) -> str:
        """Celery broker URL (Redis DB 0)."""
        return f"{self.redis_url}/{self.redis_broker_db}"

    # ── Object Storage ───────────────────────────────────────────────────
    minio_host: str = "localhost"
    minio_port: int = 9000
    minio_root_user: str = "copilot"
    minio_root_password: str = "copilot_minio_password"
    minio_bucket_documents: str = "documents"
    minio_bucket_reports: str = "reports"
    minio_bucket_exports: str = "exports"

    # ── OpenAI ───────────────────────────────────────────────────────────
    openai_api_key: str = ""
    openai_default_model: str = "gpt-4o-mini"
    openai_analysis_model: str = "gpt-4o"
    openai_embedding_model: str = "text-embedding-3-small"

    # ── CORS ─────────────────────────────────────────────────────────────
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origin_list(self) -> list[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    # ── Encryption ───────────────────────────────────────────────────────
    encryption_key: str = "change-me-in-production"


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings singleton."""
    return Settings()
