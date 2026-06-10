# CLAUDE.md

## Project Name

Business Copilot Platform

---

# Mission

Build an enterprise-grade AI Operating System that combines:

* Conversational AI
* User-created Agents
* Data Connectors
* Business Logic
* Semantic Layer
* Workflow Automation
* Cost Management
* Governance
* Collaboration

The platform should allow business users to create specialized AI employees that can reason, retrieve information, automate workflows, and collaborate across enterprise systems.

---

# Product Vision

The platform is not a chatbot.

The platform is an Enterprise AI Operating System.

Core entities:

1. Organizations
2. Workspaces
3. Spaces
4. Users
5. Agents
6. Connectors
7. Semantic Models
8. Business Rules
9. Workflows
10. Knowledge Bases

Everything in the platform should be built around these entities.

---

# Architecture Principles

## Principle 1

Business users should never need to code.

All complex functionality must be exposed through intuitive configuration interfaces.

---

## Principle 2

Platform Logic and Business Logic must always remain separate.

### Platform Logic

Examples:

* Authentication
* Authorization
* Agent Runtime
* Memory
* Workflow Execution
* Celery Tasks
* Cost Tracking
* Storage Management
* Sharing

### Business Logic

Examples:

* Revenue formulas
* KPI definitions
* Fiscal calendars
* Alert thresholds
* Customer segmentation
* Operational rules

Business Logic must always be configurable.

Never hardcode business logic.

---

## Principle 3

Everything is multi-tenant.

Every entity must belong to:

Organization
→ Workspace
→ Space

Data isolation is mandatory.

---

## Principle 4

Every action must be observable.

Track:

* User activity
* Agent executions
* Workflow executions
* Connector usage
* Costs
* Errors
* Latency

No black-box operations.

---

# Core Platform Modules

## Chat Engine

Responsibilities:

* Conversations
* Context management
* Retrieval
* Tool calling
* Citations
* Follow-up questions

---

## Agent Platform

Responsibilities:

* Agent creation
* Agent versioning
* Agent execution
* Agent sharing
* Agent analytics
* Agent archival

---

## Space Platform

Responsibilities:

* Connector isolation
* Knowledge isolation
* Semantic model isolation
* Workflow isolation

A user can have multiple spaces.

A space can contain:

* Multiple agents
* Multiple connectors
* Multiple workflows
* Multiple documents

Agents can move between spaces.

---

## Data Platform

Responsibilities:

* Connectors
* Document ingestion
* Semantic indexing
* Metadata catalog
* RAG pipelines

---

## Workflow Platform

Responsibilities:

* Scheduled jobs
* Event-driven workflows
* Approval workflows
* Notification workflows

Celery must be used.

---

## FinOps Platform

Responsibilities:

* Usage tracking
* Cost tracking
* Quotas
* Budget controls
* Cost forecasting

Every execution must be costed.

---

## Governance Platform

Responsibilities:

* RBAC
* Audit logs
* Compliance
* Data masking
* Security controls

---

# Technology Stack

## Backend

Python 3.13+

FastAPI

SQLAlchemy

Pydantic v2

LangGraph

OpenAI Responses API

Celery

Redis

PostgreSQL

pgvector

Alembic

---

## Frontend

React

TypeScript

TailwindCSS

TanStack Query

Zustand

React Hook Form

---

## Infrastructure

Docker

Docker Compose

GitHub Actions

Kubernetes

Prometheus

Grafana

OpenTelemetry

---

# Mandatory Engineering Standards

## Typing

All Python code must be fully typed.

No untyped public methods.

---

## Async

All APIs must use async implementations.

Avoid synchronous database access.

---

## Testing

Every feature must include:

* Unit Tests
* Integration Tests
* API Tests

Minimum backend coverage:

90%

---

## Error Handling

Every service must include:

* Retry handling
* Logging
* Structured exceptions

Never swallow exceptions.

---

## Security

Never store:

* Passwords
* Tokens
* Connector credentials

in plaintext.

Use encryption.

---

# Celery Requirements

Celery is mandatory.

Use Celery for:

* Workflow execution
* Scheduled reports
* Connector syncs
* Cost aggregation
* Usage aggregation
* Notifications
* Cleanup jobs
* Analytics generation

Never run long jobs in API requests.

---

# Alembic Requirements

All schema changes must use Alembic.

Never:

* Modify production schemas manually
* Execute direct DDL changes

Every model change requires:

1. SQLAlchemy update
2. Alembic migration
3. Migration test

---

# Storage Architecture

Users should never lose agents.

Agents must support:

* Active
* Archived
* Disabled

states.

Deleting agents should be rare.

Prefer archiving.

---

## Storage Layers

### PostgreSQL

Stores:

* Metadata
* Configurations
* Usage

### Object Storage

Stores:

* Documents
* Reports
* Exports

### Vector Storage

Stores:

* Embeddings
* Semantic data

---

# Quota Management

Quotas must be dynamic.

Supported quota levels:

* Organization
* Workspace
* User
* Space

Track:

* Documents
* Embeddings
* Reports
* Agents
* Workflows

Users should be allowed to create unlimited agents logically.

Old agents should move into archived state.

---

# Agent Analytics

Track:

* Executions
* Active Users
* Adoption
* Latency
* Success Rate
* Failure Rate
* Cost

Generate:

* Weekly reports
* Monthly reports
* Quarterly reports

The platform should recommend:

* Archive agent
* Delete agent
* Merge agents

based on usage.

---

# FinOps Requirements

Track costs at:

* Organization level
* Workspace level
* Space level
* User level
* Agent level
* Workflow level
* Connector level

Every operation should generate a cost event.

---

## UI Requirements

Users should always see:

Current Spend

Monthly Spend

Budget

Forecasted Spend

Remaining Budget

Progress Bars

---

# Agent Sharing

Agents must support:

* Private
* Shared
* Team
* Organization
* Marketplace

visibility levels.

---

## Permissions

Owner

Admin

Editor

Viewer

Executor

---

# Agent Marketplace

Support:

* Internal Marketplace
* Certified Agents
* Team Agents
* Published Agents

Agents must be cloneable.

Never allow direct editing of marketplace agents.

Clone first.

---

# Claude Skill Usage

Claude should automatically use:

* architecture-review
* backend-fastapi
* frontend-react
* postgres-sqlalchemy
* alembic-migrations
* celery-workflows
* langgraph-agents
* rag-engineering
* semantic-layer
* finops
* storage-quotas
* agent-analytics
* agent-sharing
* multi-tenancy
* security-review
* code-review
* test-generation
* documentation-writer

when generating code.

---

# Repository Structure

/docs
/backend
/frontend
/infra
/tests
/.claude

---

# Required Documentation

Claude must always consult:

1. MASTER_SPEC.md
2. SYSTEM_ARCHITECTURE.md
3. DATABASE_SCHEMA.md
4. AGENT_PLATFORM.md
5. DATA_PLATFORM.md
6. WORKFLOW_ENGINE.md
7. FINOPS.md
8. GOVERNANCE.md
9. API_SPEC.md
10. IMPLEMENTATION_PLAN.md

before major code generation.

---

# Definition of Done

A feature is complete only when:

* Code exists
* Tests exist
* APIs exist
* Documentation exists
* Logging exists
* Metrics exist
* Security checks exist
* Alembic migrations exist
* Celery jobs exist where applicable

Anything less is incomplete.

---

# Ultimate Goal

Create the operating system for enterprise intelligence.

The platform should allow every business user to create, deploy, manage, share, govern, and optimize AI employees across the organization without writing code.
