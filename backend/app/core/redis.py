"""Redis connection pool management.

Manages 5 logical Redis databases per blueprint §7:
    DB 0: Celery Broker (noeviction)
    DB 1: Application Cache (allkeys-lru)
    DB 2: Session Store (volatile-ttl)
    DB 3: Rate Limiting (volatile-ttl)
    DB 4: Agent Memory (allkeys-lru)

Built in Phase 1.
"""


from redis.asyncio import ConnectionPool, Redis

from app.config import get_settings

settings = get_settings()

# Logical pools mapped by database index
_pools: dict[int, ConnectionPool] = {}


def get_redis_pool(db: int) -> ConnectionPool:
    """Get or create a ConnectionPool for a specific Redis DB.

    Uses setting.redis_url as the base and appends the database index.
    """
    if db not in _pools:
        # Base URL: redis://[:password]@host:port
        pool_url = f"{settings.redis_url}/{db}"
        _pools[db] = ConnectionPool.from_url(
            pool_url,
            max_connections=50,
            decode_responses=True,
        )
    return _pools[db]


def get_redis_client(db: int) -> Redis:
    """Get an active Redis client for a specific database index."""
    pool = get_redis_pool(db)
    return Redis(connection_pool=pool)


def get_cache_client() -> Redis:
    """Get client for DB 1: Application Cache (allkeys-lru)."""
    return get_redis_client(settings.redis_cache_db)


def get_session_client() -> Redis:
    """Get client for DB 2: Session Store (volatile-ttl)."""
    return get_redis_client(settings.redis_session_db)


def get_rate_limit_client() -> Redis:
    """Get client for DB 3: Rate Limiting (volatile-ttl)."""
    return get_redis_client(settings.redis_ratelimit_db)


def get_memory_client() -> Redis:
    """Get client for DB 4: Agent Memory (allkeys-lru)."""
    return get_redis_client(settings.redis_memory_db)


async def close_redis_pools() -> None:
    """Disconnect all active connection pools on application shutdown."""
    for pool in _pools.values():
        await pool.disconnect()
    _pools.clear()
