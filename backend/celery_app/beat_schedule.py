"""Celery Beat scheduler tasks definition."""

from celery.schedules import crontab

SCHEDULE = {
    "cost_aggregation_hourly": {
        "task": "app.domains.finops.tasks.aggregate_costs",
        "schedule": crontab(minute="0"),
        "options": {"queue": "analytics"},
    },
    "budget_check": {
        "task": "app.domains.finops.tasks.budget_check",
        "schedule": crontab(minute="*/15"),
        "options": {"queue": "analytics"},
    },
    "nightly_aggregation": {
        "task": "app.domains.analytics.tasks.nightly_aggregation",
        "schedule": crontab(hour="2", minute="0"),
        "options": {"queue": "analytics"},
    },
    "weekly_report_generation": {
        "task": "app.domains.analytics.tasks.generate_weekly_report",
        "schedule": crontab(day_of_week="1", hour="6", minute="0"),
        "options": {"queue": "analytics"},
    },
    "monthly_report_generation": {
        "task": "app.domains.analytics.tasks.monthly_report_generation",  # Future implementation
        "schedule": crontab(day_of_month="1", hour="6", minute="0"),
        "options": {"queue": "analytics"},
    },
    "forecast_generation": {
        "task": "app.domains.finops.tasks.generate_forecast",
        "schedule": crontab(hour="3", minute="0"),
        "options": {"queue": "analytics"},
    },
    "agent_health_calculation": {
        "task": "app.domains.agents.tasks.calculate_health_scores",  # Future implementation
        "schedule": crontab(hour="4", minute="0"),
        "options": {"queue": "analytics"},
    },
    "archival_check": {
        "task": "app.domains.finops.tasks.archival_check",  # Future implementation
        "schedule": crontab(hour="5", minute="0"),
        "options": {"queue": "maintenance"},
    },
    "partition_maintenance": {
        "task": "app.domains.finops.tasks.partition_maintenance",
        "schedule": crontab(hour="1", minute="0"),
        "options": {"queue": "maintenance"},
    },
    "credential_rotation_check": {
        "task": "app.domains.connectors.tasks.credential_rotation_check",  # Future implementation
        "schedule": crontab(hour="6", minute="0"),
        "options": {"queue": "maintenance"},
    },
    "compliance_scan": {
        "task": "app.domains.governance.tasks.compliance_scan",  # Future implementation
        "schedule": crontab(day_of_week="0", hour="3", minute="0"),
        "options": {"queue": "maintenance"},
    },
    "retention_enforcement": {
        "task": "app.domains.governance.tasks.retention_enforcement",
        "schedule": crontab(hour="2", minute="30"),
        "options": {"queue": "maintenance"},
    },
    "storage_usage_calculation": {
        "task": "app.domains.finops.tasks.storage_usage_calculation",  # Future implementation
        "schedule": crontab(hour="3", minute="30"),
        "options": {"queue": "analytics"},
    },
    "quota_sync": {
        "task": "app.domains.finops.tasks.quota_sync",  # Future implementation
        "schedule": crontab(minute="*/5"),
        "options": {"queue": "analytics"},
    },
}
