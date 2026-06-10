"""Structured exception hierarchy for the platform.

All application exceptions inherit from CopilotError.
FastAPI exception handlers translate these into standardized JSON responses.

Hierarchy:
    CopilotError
    ├── AuthenticationError (401)
    ├── AuthorizationError (403)
    ├── NotFoundError (404)
    ├── ConflictError (409)
    ├── ValidationError (422)
    ├── RateLimitError (429)
    ├── QuotaExceededError (429)
    ├── BudgetExceededError (429)
    ├── ExternalServiceError (502)
    └── InternalError (500)
"""


class CopilotError(Exception):
    """Base exception for all platform errors."""

    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: dict[str, object] | None = None,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(CopilotError):
    """Authentication failed — invalid or expired credentials."""

    def __init__(self, message: str = "Authentication required") -> None:
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            status_code=401,
        )


class AuthorizationError(CopilotError):
    """Authorization failed — insufficient permissions."""

    def __init__(self, message: str = "Insufficient permissions") -> None:
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR",
            status_code=403,
        )


class NotFoundError(CopilotError):
    """Resource not found."""

    def __init__(self, resource_type: str, resource_id: str) -> None:
        super().__init__(
            message=f"{resource_type} not found: {resource_id}",
            error_code="NOT_FOUND",
            status_code=404,
            details={"resource_type": resource_type, "resource_id": resource_id},
        )


class ConflictError(CopilotError):
    """Resource conflict — duplicate or concurrent modification."""

    def __init__(self, message: str = "Resource conflict") -> None:
        super().__init__(
            message=message,
            error_code="CONFLICT",
            status_code=409,
        )


class ValidationError(CopilotError):
    """Input validation failed."""

    def __init__(
        self,
        message: str = "Validation error",
        details: dict[str, object] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=422,
            details=details,
        )


class RateLimitError(CopilotError):
    """Rate limit exceeded."""

    def __init__(self, retry_after: int = 60) -> None:
        super().__init__(
            message="Rate limit exceeded",
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=429,
            details={"retry_after_seconds": retry_after},
        )


class QuotaExceededError(CopilotError):
    """Resource quota exceeded."""

    def __init__(self, quota_type: str, limit: int) -> None:
        super().__init__(
            message=f"Quota exceeded for {quota_type} (limit: {limit})",
            error_code="QUOTA_EXCEEDED",
            status_code=429,
            details={"quota_type": quota_type, "limit": limit},
        )


class BudgetExceededError(CopilotError):
    """Budget threshold exceeded."""

    def __init__(self, budget_type: str, amount: float, limit: float) -> None:
        super().__init__(
            message=f"Budget exceeded for {budget_type}: ${amount:.2f} / ${limit:.2f}",
            error_code="BUDGET_EXCEEDED",
            status_code=429,
            details={
                "budget_type": budget_type,
                "current_amount": amount,
                "limit": limit,
            },
        )


class ExternalServiceError(CopilotError):
    """External service call failed (LLM, connector, etc)."""

    def __init__(self, service: str, message: str = "External service error") -> None:
        super().__init__(
            message=f"{service}: {message}",
            error_code="EXTERNAL_SERVICE_ERROR",
            status_code=502,
            details={"service": service},
        )
