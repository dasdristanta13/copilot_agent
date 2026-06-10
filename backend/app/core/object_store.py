"""MinIO S3-compatible Object Storage Client wrapper.

Handles bucket initialization, object uploads/downloads, presigned URLs,
and health checks.

Built in Phase 1.
"""

import asyncio

from minio import Minio

from app.config import get_settings

settings = get_settings()

# Initialize MinIO client
# Secure is set to False for local docker-compose development
minio_client = Minio(
    endpoint=f"{settings.minio_host}:{settings.minio_port}",
    access_key=settings.minio_root_user,
    secret_key=settings.minio_root_password,
    secure=False,
)


def ensure_buckets_exist() -> None:
    """Ensure default S3 buckets exist on storage initialization."""
    buckets = [
        settings.minio_bucket_documents,
        settings.minio_bucket_reports,
        settings.minio_bucket_exports,
    ]
    for bucket in buckets:
        if not minio_client.bucket_exists(bucket):
            minio_client.make_bucket(bucket)


async def verify_minio_connection() -> bool:
    """Check connection status to MinIO in a threadpool."""
    try:
        await asyncio.to_thread(minio_client.list_buckets)
        return True
    except Exception:
        return False
