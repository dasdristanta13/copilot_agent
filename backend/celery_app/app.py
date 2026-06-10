"""Celery application factory and instance."""

from celery import Celery

from celery_app import beat_schedule, config

# Initialize Celery app
app = Celery("business-copilot")

# Load configuration
app.config_from_object(config)

# Register periodic beat schedule
app.conf.beat_schedule = beat_schedule.SCHEDULE

# Task auto-discovery across domain modules
app.autodiscover_tasks(
    [
        "app.domains.agents",
        "app.domains.connectors",
        "app.domains.knowledge",
        "app.domains.workflows",
        "app.domains.finops",
        "app.domains.analytics",
        "app.domains.governance",
        "app.domains.notifications",
    ]
)
