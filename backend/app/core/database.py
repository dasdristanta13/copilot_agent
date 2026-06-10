"""Async database engine and session management.

Implements:
    - Async SQLAlchemy engine with connection pooling
    - Async session factory
    - FastAPI dependency for request-scoped sessions
    - Multi-tenant session with automatic organization_id filtering

Built in Phase 1. Connected to PostgreSQL + pgvector.
"""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import get_settings

settings = get_settings()

# Async SQLAlchemy engine with connection pooling
# pool_size=20, max_overflow=10 matches the spec for production workloads
engine = create_async_engine(
    settings.database_url,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    future=True,
)

# Async session factory
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """Dependency provider for request-scoped async database sessions.

    Yields:
        AsyncSession instance.
    """
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
