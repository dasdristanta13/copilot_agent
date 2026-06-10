"""SQLAlchemy base model with standard mixins.

All domain models inherit from these mixins to ensure consistent
schema patterns across the platform.

Mixins:
    BaseMixin:       id (UUID v7), created_at, updated_at
    TenantMixin:     organization_id (mandatory tenant isolation)
    AuditMixin:      created_by, updated_by (user tracking)
    SoftDeleteMixin: deleted_at (prefer archival over deletion)
    VersionedMixin:  version (optimistic concurrency control)
"""

import uuid
from datetime import datetime
from typing import Any, ClassVar

from sqlalchemy import DateTime, Integer, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from uuid_utils import uuid7


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for all models."""

    type_annotation_map: ClassVar[dict[type, Any]] = {
        uuid.UUID: UUID(as_uuid=True),
        datetime: DateTime(timezone=True),
    }


class BaseMixin:
    """Standard fields for all tables: UUID primary key + timestamps."""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid7,
        server_default=text("gen_random_uuid()"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("now()"),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("now()"),
        onupdate=text("now()"),
        nullable=False,
    )


class TenantMixin:
    """Multi-tenant isolation — every tenant-scoped entity gets this.

    The organization_id is indexed and used by the tenant filter middleware
    to enforce data isolation at the query level.
    """

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        index=True,
        nullable=False,
    )


class AuditMixin:
    """Track which user created and last updated a record."""

    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    updated_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )


class SoftDeleteMixin:
    """Soft delete support — prefer archival over hard deletion (ADR-014).

    Records with a non-null deleted_at are excluded from standard queries
    via the repository layer's default filter.
    """

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )


class VersionedMixin:
    """Optimistic concurrency control via version counter.

    Increment version on every update. If the version in the UPDATE WHERE
    clause doesn't match, a concurrent modification has occurred.
    """

    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        server_default=text("1"),
        nullable=False,
    )
