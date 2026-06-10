# ARCHITECTURE_DECISIONS.md

# Architecture Decision Records (ADR)

---

# Purpose

This document captures the reasoning behind major architectural decisions.

Goals:

* Prevent architectural drift
* Maintain consistency
* Avoid repeated debates
* Guide future contributors
* Provide context for Claude Code and Codex

---

# ADR-001

## Decision

Use a Modular Monolith initially.

---

## Why

Advantages:

* Faster development
* Simpler deployment
* Easier debugging
* Lower operational overhead

---

## Structure

```text
backend/

agents/
connectors/
workflows/
semantic/
finops/
governance/
analytics/
```

---

## Future

Selective extraction into microservices.

---

# ADR-002

## Decision

Use FastAPI as backend framework.

---

## Why

Advantages:

* Async support
* Strong typing
* OpenAPI generation
* Excellent Python ecosystem

---

## Alternatives Rejected

* Flask
* Django
* Tornado

---

# ADR-003

## Decision

Use PostgreSQL as primary database.

---

## Why

Advantages:

* Mature
* Reliable
* Strong transactional support
* JSONB support

---

## Alternatives Rejected

* MongoDB
* MySQL

---

# ADR-004

## Decision

Use pgvector.

---

## Why

Advantages:

* Single database architecture
* Simpler operations
* Shared transactions

---

## Alternatives Rejected

* Pinecone
* Weaviate
* Qdrant

---

## Revisit When

Embedding volume exceeds operational limits.

---

# ADR-005

## Decision

Use Redis.

---

## Purpose

* Cache
* Session Store
* Celery Broker
* Memory Layer

---

# ADR-006

## Decision

Use Celery.

---

## Why

Needed for:

* Workflow execution
* Agent execution
* Sync jobs
* Reporting

---

## Alternatives Considered

Temporal

---

## Reason Rejected

Temporal introduces additional complexity early.

---

## Revisit When

Workflow orchestration becomes highly complex.

---

# ADR-007

## Decision

Use Alembic for all migrations.

---

## Rule

No manual schema modifications.

---

## Required Process

```bash
alembic revision --autogenerate
alembic upgrade head
```

---

# ADR-008

## Decision

Use LangGraph for agent orchestration.

---

## Why

Supports:

* Planning
* Memory
* Tool execution
* Multi-agent systems

---

## Alternatives Rejected

Pure LangChain

Custom orchestration

---

# ADR-009

## Decision

Use OpenAI Responses API.

---

## Why

Unified interface for:

* Tools
* Reasoning
* Structured output

---

## Future

Provider abstraction required.

---

# ADR-010

## Decision

Implement LLM Provider Layer.

---

## Purpose

Avoid vendor lock-in.

---

## Interface

```python
class LLMProvider:
    async def generate()
    async def stream()
```

---

## Future Providers

* OpenAI
* Anthropic
* Google
* Azure OpenAI

---

# ADR-011

## Decision

Spaces are the primary organizational boundary.

---

## Hierarchy

```text
Organization
→ Workspace
→ Space
```

---

## Why

Allows:

* Isolation
* Ownership
* Collaboration

---

# ADR-012

## Decision

Use Space-based connector ownership.

---

## Why

Connectors are shared resources.

Avoid duplication.

---

# ADR-013

## Decision

Agents belong to Spaces.

---

## Why

Provides:

* Governance
* Sharing
* Cost attribution

---

# ADR-014

## Decision

Never hard-delete agents by default.

---

## Lifecycle

```text
Draft

Published

Active

Archived
```

---

## Why

Protects user work.

---

# ADR-015

## Decision

Unlimited logical agents.

---

## Implementation

Archive old agents.

Track storage quotas separately.

---

# ADR-016

## Decision

Separate Platform Logic from Business Logic.

---

## Platform Logic

Authentication

Workflows

Storage

Permissions

---

## Business Logic

KPIs

Metrics

Revenue formulas

Thresholds

---

# ADR-017

## Decision

Business Logic stored as configuration.

---

## Never

Hardcode tenant rules.

---

# ADR-018

## Decision

Use Semantic Layer.

---

## Why

Business users should never see:

* Table names
* Join paths
* Database schemas

---

# ADR-019

## Decision

Every agent execution generates telemetry.

---

## Required Events

Usage Event

Cost Event

Audit Event

Trace Event

---

# ADR-020

## Decision

FinOps is a first-class domain.

---

## Why

AI costs are variable.

Cost transparency is mandatory.

---

# ADR-021

## Decision

Track costs at every hierarchy level.

---

```text
Organization

Workspace

Space

User

Agent

Workflow
```

---

# ADR-022

## Decision

Hybrid RAG architecture.

---

## Components

Vector Search

Keyword Search

Metadata Filtering

Reranking

---

## Why

Higher retrieval quality.

---

# ADR-023

## Decision

Use Metadata Catalog.

---

## Purpose

Discoverability

Lineage

Governance

---

# ADR-024

## Decision

Every connector implements common SDK.

---

## Required Methods

```python
connect()
validate()
discover_schema()
sync()
search()
execute()
```

---

# ADR-025

## Decision

Use Object Storage.

---

## Stores

Documents

Exports

Reports

---

## Recommended

S3

MinIO

---

# ADR-026

## Decision

Workflow execution must be asynchronous.

---

## Never

Run long workflows in request lifecycle.

---

# ADR-027

## Decision

Use Celery Beat for scheduling.

---

## Examples

Daily Reports

Connector Syncs

Budget Monitoring

---

# ADR-028

## Decision

Every resource supports versioning.

---

## Resources

Agents

Workflows

Semantic Models

Business Rules

---

# ADR-029

## Decision

Every resource supports auditability.

---

## Requirement

All changes tracked.

---

# ADR-030

## Decision

Use RBAC.

---

## Roles

Platform Admin

Workspace Admin

Space Admin

Analyst

Viewer

---

# ADR-031

## Decision

Permission checks occur in service layer.

---

## Never

Trust frontend authorization.

---

# ADR-032

## Decision

Marketplace uses clone model.

---

## Rule

Marketplace agents cannot be edited directly.

Clone first.

---

# ADR-033

## Decision

All sensitive credentials encrypted.

---

## Examples

Connector credentials

API keys

Tokens

---

# ADR-034

## Decision

OpenTelemetry everywhere.

---

## Track

Latency

Errors

Usage

Costs

---

# ADR-035

## Decision

Prometheus + Grafana.

---

## Why

Industry standard observability.

---

# ADR-036

## Decision

Every major action emits domain events.

---

## Examples

AgentCreated

WorkflowExecuted

ConnectorSynced

---

# ADR-037

## Decision

Usage analytics built from events.

---

## Never

Query operational tables directly for analytics.

---

# ADR-038

## Decision

Partition high-volume tables.

---

## Tables

usage_events

cost_events

audit_logs

agent_executions

workflow_runs

---

# ADR-039

## Decision

Frontend is React + TypeScript.

---

## Why

Large ecosystem.

Strong typing.

---

# ADR-040

## Decision

Chat is primary UX.

---

## Principle

Everything should ultimately be executable through conversational interactions.

---

# Future ADRs

Reserve IDs:

ADR-041 to ADR-100

Potential topics:

* Agent learning
* Knowledge graph
* Graph RAG
* Temporal migration
* Event bus adoption
* Real-time collaboration
* Multi-region deployment
* Dedicated vector cluster
* Agent certification framework
* Agent-to-agent protocol

---

# Final Rule

When future implementation choices conflict with these ADRs:

1. Create a new ADR.
2. Explain rationale.
3. Record migration strategy.
4. Never silently change architecture.

This document is the long-term architectural memory of the Business Copilot Platform.
