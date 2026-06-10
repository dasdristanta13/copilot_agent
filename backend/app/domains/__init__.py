"""Domain modules — Modular Monolith architecture (ADR-001).

Each domain module follows the standard structure:
    models.py      — SQLAlchemy ORM models
    schemas.py     — Pydantic request/response schemas
    repository.py  — Data access layer (async)
    service.py     — Business logic layer
    router.py      — FastAPI router (API endpoints)
    events.py      — Domain event definitions
    tasks.py       — Celery task definitions (if applicable)
    tests/         — Domain-specific tests

Domains:
    identity       — Auth, Users, Roles, Permissions
    tenants        — Organizations, Workspaces, Spaces
    agents         — Agent lifecycle, runtime, memory
    chat           — Conversations, messages, streaming
    connectors     — External data connectivity
    knowledge      — Documents, chunks, RAG
    semantic       — Business glossary, metrics
    workflows      — Automation, triggers, approvals
    finops         — Cost tracking, budgets, quotas
    analytics      — Usage analytics, health scores
    governance     — Audit, compliance, approvals
    marketplace    — Agent marketplace, templates
    notifications  — Notification delivery
"""
