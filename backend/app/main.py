"""FastAPI application factory.

Creates and configures the FastAPI application with all middleware,
routers, and lifecycle hooks. Uses the factory pattern to support
testing with different configurations.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.config import get_settings
from app.core.database import engine
from app.core.object_store import ensure_buckets_exist, verify_minio_connection
from app.core.redis import close_redis_pools, get_cache_client


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan — startup and shutdown hooks.

    Startup:
        - Initialize and verify database connection pool
        - Initialize and verify Redis connection pool
        - Verify MinIO connection and ensure default buckets exist

    Shutdown:
        - Close database connections
        - Close Redis connection pools
    """
    settings = get_settings()

    # ── Startup ──────────────────────────────────────────────────────
    try:
        # Verify database connection
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))

        # Verify Redis connection
        redis_client = get_cache_client()
        await redis_client.ping()

        # Verify and initialize MinIO
        if not await verify_minio_connection():
            raise RuntimeError("MinIO object storage is unreachable")
        ensure_buckets_exist()
    except Exception as e:
        # We catch and log it, then raise to halt application startup
        import logging
        logging.error(f"Startup check failed: {e}")
        raise

    app.state.settings = settings

    yield

    # ── Shutdown ─────────────────────────────────────────────────────
    await close_redis_pools()
    await engine.dispose()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    settings = get_settings()

    app = FastAPI(
        title="Business Copilot Platform",
        description="Enterprise AI Operating System — API",
        version=settings.app_version,
        docs_url="/docs" if settings.app_debug else None,
        redoc_url="/redoc" if settings.app_debug else None,
        lifespan=lifespan,
    )

    # ── Middleware ────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # TODO: Phase 3 — Add RequestID middleware
    # TODO: Phase 3 — Add TenantContext middleware
    # TODO: Phase 3 — Add RateLimiting middleware

    # ── Routers ──────────────────────────────────────────────────────
    # TODO: Phase 3 — Include identity router (/auth, /users)
    # TODO: Phase 4 — Include tenants router (/organizations, /workspaces, /spaces)
    # TODO: Phase 6 — Include connectors router
    # TODO: Phase 7 — Include knowledge router
    # TODO: Phase 8 — Include semantic router
    # TODO: Phase 9 — Include agents router
    # TODO: Phase 10 — Include workflows router
    # TODO: Phase 11 — Include chat router
    # TODO: Phase 12 — Include finops router
    # TODO: Phase 13 — Include analytics router
    # TODO: Phase 14 — Include governance router
    # TODO: Phase 15 — Include marketplace router
    # TODO: Phase 15 — Include notifications router

    # ── Health Check ─────────────────────────────────────────────────
    @app.get("/health", tags=["System"])
    async def health_check() -> Any:
        """Verify API and core storage service connectivity."""
        postgres_status = "ok"
        redis_status = "ok"
        minio_status = "ok"

        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
        except Exception:
            postgres_status = "error"

        try:
            redis_client = get_cache_client()
            await redis_client.ping()
        except Exception:
            redis_status = "error"

        try:
            if not await verify_minio_connection():
                minio_status = "error"
        except Exception:
            minio_status = "error"

        is_healthy = all(
            status == "ok"
            for status in (postgres_status, redis_status, minio_status)
        )

        content = {
            "status": "ok" if is_healthy else "error",
            "version": settings.app_version,
            "environment": settings.app_env,
            "services": {
                "postgres": postgres_status,
                "redis": redis_status,
                "minio": minio_status,
            },
        }

        if is_healthy:
            return content
        return JSONResponse(status_code=503, content=content)

    return app
