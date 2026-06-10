.PHONY: help dev test lint format typecheck migrate seed clean install

# Default target
help: ## Show this help message
	@echo "Business Copilot Platform — Development Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

install: ## Install all dependencies
	cd backend && uv sync
	cd frontend && npm install

install-hooks: ## Install pre-commit hooks
	pre-commit install

# ---------------------------------------------------------------------------
# Development
# ---------------------------------------------------------------------------

dev: ## Start full development stack (Docker Compose)
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

dev-backend: ## Start backend only (no Docker)
	cd backend && uv run uvicorn app.main:create_app --factory --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Start frontend only
	cd frontend && npm run dev

dev-worker: ## Start Celery worker (all queues)
	cd backend && uv run celery -A celery_app.app worker --loglevel=info -Q agent.execute,workflow.high,workflow.medium,connector.sync,document.process,notifications,analytics,maintenance

dev-beat: ## Start Celery Beat scheduler
	cd backend && uv run celery -A celery_app.app beat --loglevel=info

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

migrate: ## Run database migrations
	cd backend && uv run alembic upgrade head

migrate-create: ## Create a new migration (usage: make migrate-create MSG="add users table")
	cd backend && uv run alembic revision --autogenerate -m "$(MSG)"

migrate-down: ## Rollback one migration
	cd backend && uv run alembic downgrade -1

migrate-reset: ## Reset database to empty
	cd backend && uv run alembic downgrade base

seed: ## Seed database with development data
	cd backend && uv run python -m scripts.seed

# ---------------------------------------------------------------------------
# Quality
# ---------------------------------------------------------------------------

lint: ## Run linter (ruff)
	ruff check backend/ tests/

format: ## Format code (ruff)
	ruff format backend/ tests/
	ruff check --fix backend/ tests/

typecheck: ## Run type checker (mypy)
	mypy backend/app --config-file mypy.ini

# ---------------------------------------------------------------------------
# Testing
# ---------------------------------------------------------------------------

test: ## Run all tests
	cd backend && uv run pytest tests/ -v --tb=short

test-unit: ## Run unit tests only
	cd backend && uv run pytest tests/ -v --tb=short -m "not integration and not e2e"

test-integration: ## Run integration tests
	cd backend && uv run pytest tests/ -v --tb=short -m "integration"

test-cov: ## Run tests with coverage report
	cd backend && uv run pytest tests/ -v --tb=short --cov=app --cov-report=term-missing --cov-report=html

# ---------------------------------------------------------------------------
# CI (runs all checks in sequence)
# ---------------------------------------------------------------------------

ci: lint typecheck test ## Run full CI pipeline locally

# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------

clean: ## Clean generated files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf htmlcov/ .coverage

docker-clean: ## Remove all Docker containers and volumes
	docker compose -f docker-compose.yml -f docker-compose.dev.yml down -v --remove-orphans
