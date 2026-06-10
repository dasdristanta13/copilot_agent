# Business Copilot Platform — Enterprise AI Operating System

The Business Copilot Platform is a multi-tenant, high-performance Modular Monolith designed as an Enterprise AI Operating System. It integrates data connectors, multi-layer semantic representations, automated workflows, and RAG retrieval pipelines using state-of-the-art single-agent and multi-agent execution runtimes.

---

## 1. System Architecture

The platform follows a clean **Modular Monolith** architecture pattern ([ADR-001](file:///c:/Users/ASUS/Documents/Projects/copilot_agent/docs/ARCHITECTURE_DECISIONS.md)) to enforce strict boundary isolation between business modules, while keeping deployment overhead low.

```
                  +---------------------------------------+
                  |           React Frontend              |
                  |     (Vite + TypeScript + Tailwind v4) |
                  +-------------------+-------------------+
                                      | (HTTPS / SSE Streaming)
                                      v
                  +---------------------------------------+
                  |            FastAPI Gateway            |
                  |      CORS, Rate Limit, Auth, RBAC     |
                  +---+---------------+---------------+---+
                      |               |               |
         +------------v----+   +------v-----+   +-----v-------------+
         | Identity & Org  |   | Chat & SSE |   | Agent & Workflows |
         +-----------------+   +------------+   +-------------------+
                      |               |               |
                      +-------+-------+---------------+
                              | (Async / Queue routing)
                              v
                  +---------------------------------------+
                  |         Celery Worker Pools           |
                  |   Agent Execution, Sync, RAG, Beat    |
                  +-------------------+-------------------+
                                      |
       +------------------------------+------------------------------+
       |                              |                              |
       v (AsyncPG / Vector)           v (Redis DB 0-4)               v (S3 API)
+------+----------------+      +------+----------------+      +------+----------------+
|      PostgreSQL       |      |         Redis          |      |         MinIO          |
| pgvector, HNSW, UTF-8 |      | Cache, Session, Memory |      | Documents & Exports    |
+-----------------------+      +------------------------+      +------------------------+
```

### Key Subsystems
1. **Core API Gateway**: Powered by FastAPI, managing authentication, tenant-scoped database query filters, sliding-window rate limiters, and CORS middleware.
2. **LangGraph Agent Runtime**: A directed graph execution engine providing reasoning, planning, memory retrieval, and tool execution with strict input/output validators.
3. **Data Connector Framework**: Space-owned connectivity layers providing schema discovery, secure credential encryption (AES-256-GCM), and scheduled synchronization.
4. **Knowledge Platform (RAG)**: Document extraction (PDF, DOCX, XLSX) and hybrid retrieval pipelines combining pgvector cosine similarity search, keyword indexing, and custom rerankers.
5. **Semantic Layer**: A unified business glossary and KPI formula resolver translating natural language questions into database-scoped executable logic.
6. **Celery Worker Architecture**: 8 dedicated priority queues managing latency-sensitive tasks, recurring database cleanups, and heavy analytics aggregations.

---

## 2. Technology Stack

### Backend
- **Core Framework**: Python 3.13+, FastAPI, Pydantic v2
- **Database ORM**: SQLAlchemy 2.0 (Async), Alembic
- **Task Queue**: Celery, RedBeat (Redis scheduler backend)
- **Vector Search**: pgvector (PostgreSQL extension)
- **Object Storage**: MinIO (S3-compatible)
- **AI/Orchestration**: OpenAI API, LangGraph, tiktoken

### Frontend
- **Framework**: React 19, TypeScript, Vite
- **Styling**: Tailwind CSS v4
- **Linter & Formatter**: ESLint 9+ flat config, Prettier

---

## 3. Directory Layout

The codebase is organized as a monorepo workspace managed via `uv`:

```
.
├── .github/workflows/         # CI/CD pipelines
├── backend/                   # Backend Monolith package
│   ├── app/                   # Application source
│   │   ├── core/              # Foundational cross-cutting helpers (DB, Redis, etc.)
│   │   ├── domains/           # 14 business domain packages (Modular boundary)
│   │   └── llm/               # LLM Provider abstraction & cost calculators
│   ├── celery_app/            # Celery configurations and scheduler maps
│   ├── scripts/               # Seed, health checking, and migration utilities
│   └── pyproject.toml         # Backend dependencies
├── frontend/                  # React Vite client application
│   ├── src/
│   │   ├── api/               # API clients (TanStack Query)
│   │   ├── components/        # Shared presentation layers
│   │   └── features/          # Feature UI modules mirroring backend domains
│   └── package.json           # Frontend package descriptors
├── infra/                     # Infra configurations
│   └── docker/                # Multi-stage Dockerfiles (backend, worker, beat, frontend)
├── docker-compose.yml         # Base dev services
├── pyproject.toml             # UV virtual workspace manifest
└── CONTRIBUTING.md            # Local developer onboarding instructions
```

---

## 4. Local Development Setup

### 4.1 Prerequisites
Ensure your machine has the following tools installed:
- **Python 3.13**
- **Node.js v20**
- **Docker Engine & Compose**
- **uv** (Python package installer)

### 4.2 Installation
1. **Synchronize dependencies**:
   ```bash
   # Configures virtual environments and node_modules
   uv sync --all-extras --package business-copilot-backend
   cd frontend && npm install
   ```
2. **Setup environment parameters**:
   ```bash
   cp .env.example .env
   ```
3. **Configure Git Hooks**:
   ```bash
   pre-commit install
   ```

### 4.3 Running Services Locally

#### Using Docker Compose (Recommended)
Start the PostgreSQL database (port 5433), Redis (port 6380), and MinIO (console port 9001):
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

#### Running Applications Directly
- **Backend API Server** (runs on port 8000):
  ```bash
  cd backend
  uv run uvicorn app.main:create_app --factory --reload --host 0.0.0.0 --port 8000
  ```
- **Celery Worker**:
  ```bash
  cd backend
  uv run celery -A celery_app.app worker --loglevel=info
  ```
- **Celery Beat Scheduler**:
  ```bash
  cd backend
  uv run celery -A celery_app.app beat --loglevel=info
  ```
- **Vite Frontend Dev Client** (runs on port 5173):
  ```bash
  cd frontend
  npm run dev
  ```

---

## 5. Testing & Quality Standards

Quality gates are enforced locally and in the CI pipeline:

- **Linting & Formatting (Python)**:
  ```bash
  uv run ruff check backend/ tests/
  ```
- **Strict Type Checking (Python)**:
  ```bash
  uv run mypy backend/app --config-file mypy.ini
  ```
- **Backend Tests (Pytest)**:
  ```bash
  cd backend
  uv run pytest tests/
  ```
- **Frontend Checks**:
  ```bash
  cd frontend
  npm run lint
  npx tsc -b
  ```

For detailed contributions guidelines and API standards, consult [CONTRIBUTING.md](file:///c:/Users/ASUS/Documents/Projects/copilot_agent/CONTRIBUTING.md).
