# Contributing to Business Copilot Platform

Welcome to the Business Copilot Platform repository! This guide details the local setup, developer tools, coding standards, and workflows.

---

## 1. Quick Start Setup

### Prerequisites
- **Python**: 3.13 or newer
- **Node.js**: v20 or newer
- **Docker & Compose**: For running PostgreSQL, Redis, and MinIO
- **uv**: Python package manager (`pip install uv` or follow [Astral Docs](https://docs.astral.sh/uv/))

### Initializing the Workspace
1. **Clone the repository** and navigate to the root directory.
2. **Install all dependencies** (Python & Node):
   ```bash
   make install
   ```
3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```
4. **Install pre-commit hooks**:
   ```bash
   make install-hooks
   ```

---

## 2. Common Development Commands

The root [`Makefile`](file:///c:/Users/ASUS/Documents/Projects/copilot_agent/Makefile) coordinates all commands.

| Target | Description |
|---|---|
| `make install` | Syncs backend and installs frontend node modules |
| `make install-hooks` | Configures git pre-commit hooks |
| `make dev` | Launches all Docker storage services, backend, worker, beat, and frontend |
| `make dev-backend` | Runs the FastAPI app directly (hot-reload on port 8000) |
| `make dev-frontend` | Runs the Vite dev server (port 5173) |
| `make dev-worker` | Runs the Celery worker with all queues active |
| `make lint` | Run Ruff on backend & test folders |
| `make format` | Formats Python code and auto-fixes Ruff issues |
| `make typecheck` | Run strict MyPy type checking |
| `make test` | Run pytest suite |
| `make ci` | Runs local sequence: lint → typecheck → test |
| `make clean` | Removes build, test, and typecheck cache directories |

---

## 3. Architecture Rules & Guidelines

### Modular Monolith (ADR-001)
The backend is structured into distinct, self-contained **domains** under `backend/app/domains/`. Each domain should follow:
1. `models.py` — SQLAlchemy ORM schemas inheriting from `BaseMixin`/`TenantMixin`.
2. `schemas.py` — Pydantic inputs and outputs.
3. `repository.py` — Data access layer isolating raw SQL/ORM constructs.
4. `service.py` — Domain-specific business logic.
5. `router.py` — HTTP routing.

### Crucial Dependency Rules
- **No Circular Imports**: Foundation modules (e.g. `core/`, `llm/`) must not import anything from `domains/`.
- **Foundational Domains Only**: Foundational modules like `identity/` and `tenants/` do not import other product domains.
- **Subscribers Over Direct Calls**: Operational domains like `finops/`, `analytics/`, and `governance/` interact via the in-process Event Bus (`app/core/events.py`) or Celery tasks, and should not be imported by main business logic.

---

## 4. Linting, Formatting, and Type Safety

All contributions must pass strict quality gates:
1. **Formatting & Linting (Python)**: Checked via Ruff. We target line lengths of 100 characters. Clean formatting is enforced.
2. **Type Safety (Python)**: Enforced via MyPy in strict mode (`--strict`). Explicit type annotations are required. Missing definitions or usage of `Any` without explicit permission will fail CI.
3. **Frontend Linting**: Controlled by ESLint flat config with Prettier plugin integration. Running `npm run format` inside `frontend/` auto-formats TSX and CSS.

---

## 5. Development Workflow Checklist

Before opening a pull request, ensure you have:
1. Formatted your code (`make format` and `npm run format` inside `frontend/`).
2. Checked type annotations (`make typecheck`).
3. Written unit tests for new service features under `backend/tests/` or domain `tests/` directories.
4. Confirmed all tests pass successfully (`make test`).
