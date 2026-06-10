"""Celery configuration module."""

from app.config import get_settings

settings = get_settings()

# Broker and backend configuration
broker_url = settings.CELERY_BROKER_URL
result_backend = settings.CELERY_RESULT_BACKEND

# Serialization
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "UTC"
enable_utc = True

# Task execution settings
task_acks_late = True
task_reject_on_worker_lost = True
worker_prefetch_multiplier = 1

# Queue definitions (matching §8.1 / §8.4 of the blueprint)
task_routes = {
    # Latency sensitive
    "app.domains.agents.tasks.*": {"queue": "agent.execute"},
    "app.domains.chat.tasks.*": {"queue": "agent.execute"},
    # Workflows
    "app.domains.workflows.tasks.execute_workflow_high": {"queue": "workflow.high"},
    "app.domains.workflows.tasks.*": {"queue": "workflow.medium"},
    # Connectors and sync
    "app.domains.connectors.tasks.*": {"queue": "connector.sync"},
    # Document processing / RAG
    "app.domains.knowledge.tasks.*": {"queue": "document.process"},
    # Notifications
    "app.domains.notifications.tasks.*": {"queue": "notifications"},
    # Cost & analytics aggregation
    "app.domains.analytics.tasks.*": {"queue": "analytics"},
    "app.domains.finops.tasks.aggregate_costs": {"queue": "analytics"},
    "app.domains.finops.tasks.generate_forecast": {"queue": "analytics"},
    # Maintenance & governance
    "app.domains.governance.tasks.*": {"queue": "maintenance"},
    "app.domains.finops.tasks.partition_maintenance": {"queue": "maintenance"},
}
