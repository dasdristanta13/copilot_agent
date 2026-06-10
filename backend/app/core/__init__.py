"""Core module — Cross-cutting infrastructure concerns.

This package contains foundational components used by all domain modules:
- database.py    — Async SQLAlchemy engine, session factory, base model
- redis.py       — Redis connection pool management
- security.py    — JWT tokens, password hashing, encryption
- middleware.py   — CORS, RequestID, TenantContext, RateLimiting
- exceptions.py  — Structured exception hierarchy
- pagination.py  — Cursor and offset pagination utilities
- events.py      — In-process domain event bus
- permissions.py — RBAC permission evaluation engine
- tenant.py      — Multi-tenant context manager
- observability.py — OpenTelemetry + structured logging setup
- rate_limiter.py — Redis-based sliding window rate limiter
- base_model.py  — SQLAlchemy declarative base + mixins
"""
