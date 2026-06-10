"""FastAPI dependency injection providers.

Central location for all FastAPI Depends() callables:
    - get_db_session: Request-scoped async database session
    - get_current_user: Authenticated user from JWT
    - get_current_tenant: Organization context from JWT
    - require_permission: Permission check dependency factory

Built progressively across Phases 1-4.
"""

# TODO: Phase 1 — Implement get_db_session
# TODO: Phase 3 — Implement get_current_user
# TODO: Phase 3 — Implement get_current_tenant
# TODO: Phase 3 — Implement require_permission
