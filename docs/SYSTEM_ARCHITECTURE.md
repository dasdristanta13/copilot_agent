# SYSTEM_ARCHITECTURE.md

# Business Copilot Platform Architecture

---

# Purpose

This document defines the complete technical architecture for the Business Copilot Platform.

This architecture must support:

* Multi-tenancy
* Agentic workflows
* Enterprise data connectivity
* AI-powered analytics
* Workflow automation
* Cost tracking
* Governance
* Enterprise scale

---

# Architectural Principles

## Principle 1: API First

Everything must be exposed through APIs.

No direct service-to-database access outside owned boundaries.

---

## Principle 2: Event Driven

Long-running operations must execute asynchronously.

Examples:

* Agent execution
* Connector synchronization
* Report generation
* Cost aggregation
* Usage aggregation

---

## Principle 3: Multi-Tenant

Every resource belongs to:

Organization
→ Workspace
→ Space

Tenant isolation is mandatory.

---

## Principle 4: Stateless APIs

FastAPI services should remain stateless.

State belongs in:

* PostgreSQL
* Redis
* Object Storage
* Vector Store

---

## Principle 5: AI Native

The system should assume AI execution is a first-class capability.

All services should be designed around:

* Agents
* Workflows
* Memory
* Retrieval

---

# High-Level Architecture

```mermaid
flowchart TB

User[Users]

UI[React Frontend]

Gateway[FastAPI Gateway]

Auth[Auth Service]

Chat[Conversation Service]

Agent[Agent Runtime]

Workflow[Workflow Engine]

Connector[Connector Platform]

Semantic[Semantic Layer]

Memory[Memory Service]

RAG[RAG Engine]

Usage[Usage Analytics]

FinOps[Cost Tracking]

Audit[Audit Service]

Celery[Celery Workers]

Redis[(Redis)]

Postgres[(PostgreSQL)]

Vector[(pgvector)]

Object[(Object Storage)]

OpenAI[OpenAI]

Salesforce[Salesforce]

Snowflake[Snowflake]

SharePoint[SharePoint]

User --> UI

UI --> Gateway

Gateway --> Auth

Gateway --> Chat

Gateway --> Agent

Agent --> Workflow

Agent --> Connector

Agent --> Semantic

Agent --> Memory

Agent --> RAG

RAG --> Vector

Memory --> Redis

Connector --> Salesforce

Connector --> Snowflake

Connector --> SharePoint

Agent --> OpenAI

Workflow --> Celery

Celery --> Postgres

Celery --> Redis

Usage --> Postgres

FinOps --> Postgres

Audit --> Postgres

Chat --> Postgres

Agent --> Postgres

Gateway --> Usage

Gateway --> Audit

Gateway --> FinOps
```

---

# Service Architecture

## Frontend Layer

Technology:

* React
* TypeScript
* Tailwind
* TanStack Query

Responsibilities:

* Chat UI
* Agent Builder
* Workflow Builder
* Dashboards
* Cost Tracking UI
* Administration

---

# API Gateway

Technology:

FastAPI

Responsibilities:

* Authentication
* Authorization
* Request validation
* Routing
* Rate limiting

No business logic should exist here.

---

# Authentication Service

Responsibilities:

* Login
* SSO
* OAuth
* JWT
* Session Management

Supported Providers:

* Google
* Microsoft
* Okta
* Azure AD

---

# Conversation Service

Responsibilities:

* Chat Sessions
* Message History
* Context Window Management
* Citations
* Follow-up Questions

Stores:

* Conversations
* Messages

---

# Agent Runtime Service

This is the heart of the platform.

Responsibilities:

* Agent Execution
* Planning
* Tool Calling
* Memory Retrieval
* Reflection
* Self Correction

---

# Agent Runtime Flow

```mermaid
sequenceDiagram

participant User
participant Chat
participant Planner
participant Memory
participant Connector
participant OpenAI

User->>Chat: Ask Question

Chat->>Planner: Create Plan

Planner->>Memory: Retrieve Context

Memory-->>Planner: Context

Planner->>Connector: Get Data

Connector-->>Planner: Results

Planner->>OpenAI: Reason

OpenAI-->>Planner: Response

Planner-->>Chat: Final Answer

Chat-->>User: Response
```

---

# Multi-Agent Architecture

```mermaid
flowchart LR

Supervisor[Supervisor Agent]

Sales[Sales Agent]

Finance[Finance Agent]

Ops[Operations Agent]

Forecast[Forecast Agent]

Supervisor --> Sales

Supervisor --> Finance

Supervisor --> Ops

Finance --> Forecast
```

Capabilities:

* Delegation
* Specialist agents
* Task routing
* Aggregation

---

# Space Architecture

A Space is an isolated execution environment.

Contains:

* Agents
* Connectors
* Documents
* Semantic Models
* Workflows

---

```mermaid
flowchart TB

Workspace

SpaceA[Sales Space]

SpaceB[Finance Space]

SpaceC[Operations Space]

Agent1

Agent2

Agent3

Conn1

Conn2

Conn3

Workspace --> SpaceA
Workspace --> SpaceB
Workspace --> SpaceC

SpaceA --> Agent1
SpaceA --> Conn1

SpaceB --> Agent2
SpaceB --> Conn2

SpaceC --> Agent3
SpaceC --> Conn3
```

---

# Connector Platform

Responsibilities:

* Authentication
* Synchronization
* Metadata Discovery
* Query Execution

Supported Types:

## Databases

* PostgreSQL
* Snowflake
* BigQuery
* Redshift

## SaaS

* Salesforce
* HubSpot
* SAP

## Documents

* SharePoint
* Google Drive
* OneDrive

## APIs

* REST
* GraphQL

---

# Connector Execution Flow

```mermaid
flowchart LR

Agent

Connector

Cache

External

Agent --> Connector

Connector --> Cache

Connector --> External

External --> Connector

Connector --> Agent
```

---

# Semantic Layer

Purpose:

Translate business language into data operations.

Example:

Revenue

↓

Net Sales - Returns

---

Components:

* Business Glossary
* KPI Definitions
* Semantic Mapping
* Metric Registry

---

# RAG Architecture

```mermaid
flowchart TB

Document

Chunking

Embedding

VectorStore

Retriever

LLM

Document --> Chunking

Chunking --> Embedding

Embedding --> VectorStore

Retriever --> VectorStore

Retriever --> LLM
```

---

# Memory Architecture

Memory Types:

## Conversation Memory

Current chat session

---

## Agent Memory

Agent-specific knowledge

---

## Workspace Memory

Shared team memory

---

## Semantic Memory

Business definitions

---

# Workflow Engine

Responsibilities:

* Scheduling
* Automation
* Notifications
* Approvals

---

# Workflow Architecture

```mermaid
flowchart LR

Trigger

Workflow

Task1

Task2

Task3

Notification

Trigger --> Workflow

Workflow --> Task1

Task1 --> Task2

Task2 --> Task3

Task3 --> Notification
```

---

# Celery Architecture

Mandatory Component

Used For:

* Workflow Execution
* Agent Execution
* Connector Sync
* Cost Aggregation
* Usage Aggregation
* Report Generation
* Notifications

---

```mermaid
flowchart TB

FastAPI

Redis

Celery

Worker1

Worker2

Worker3

FastAPI --> Redis

Redis --> Celery

Celery --> Worker1

Celery --> Worker2

Celery --> Worker3
```

---

# Celery Queues

## High Priority

* Agent Execution

## Medium Priority

* Workflow Execution

## Low Priority

* Reports
* Analytics
* Cleanup

---

# Database Architecture

Primary Database:

PostgreSQL

---

Stores:

* Users
* Organizations
* Workspaces
* Spaces
* Agents
* Connectors
* Workflows
* Usage Events
* Cost Events

---

# Vector Database

Technology:

pgvector

Stores:

* Embeddings
* Semantic Models
* Knowledge Chunks

---

# Redis Architecture

Stores:

* Cache
* Session State
* Celery Broker
* Temporary Memory

---

# Object Storage

Stores:

* Documents
* PDFs
* Reports
* Exports
* Uploaded Files

Recommended:

* S3
* MinIO

---

# Usage Analytics Architecture

Track:

* Agent Runs
* User Activity
* Connector Calls
* Workflow Runs

---

```mermaid
flowchart LR

Events

UsagePipeline

Warehouse

Dashboard

Events --> UsagePipeline

UsagePipeline --> Warehouse

Warehouse --> Dashboard
```

---

# FinOps Architecture

Track Costs By:

* Organization
* Workspace
* Space
* User
* Agent
* Workflow
* Connector

---

Cost Sources:

* LLM Calls
* Embeddings
* Storage
* Connector Calls
* Workflow Executions

---

```mermaid
flowchart LR

Execution

CostCollector

CostEvents

Dashboard

Execution --> CostCollector

CostCollector --> CostEvents

CostEvents --> Dashboard
```

---

# Agent Analytics Architecture

Metrics:

* Usage
* Adoption
* Latency
* Errors
* Success Rate
* Cost

Generate:

* Weekly Reports
* Monthly Reports
* Quarterly Reports

---

# Governance Architecture

Components:

## RBAC

Permissions

## Audit

Activity Logging

## Compliance

Policies

## Data Security

Masking

Encryption

---

# Observability Architecture

Technology:

* OpenTelemetry
* Prometheus
* Grafana

---

Track:

* Latency
* Errors
* Queue Depth
* Token Usage
* Cost

---

```mermaid
flowchart LR

Services

Metrics

Prometheus

Grafana

Services --> Metrics

Metrics --> Prometheus

Prometheus --> Grafana
```

---

# Deployment Architecture

```mermaid
flowchart TB

Internet

LoadBalancer

FrontendPods

APIPods

WorkerPods

Redis

Postgres

ObjectStorage

Internet --> LoadBalancer

LoadBalancer --> FrontendPods

LoadBalancer --> APIPods

APIPods --> Redis

APIPods --> Postgres

WorkerPods --> Redis

WorkerPods --> Postgres

WorkerPods --> ObjectStorage
```

---

# Scalability Strategy

Scale Independently:

* API Pods
* Agent Workers
* Connector Workers
* Workflow Workers

Avoid monolithic scaling.

---

# Future Architecture

Planned:

* Multi-region
* Model routing
* Dedicated vector clusters
* Event bus
* Agent-to-agent communication protocol
* Enterprise marketplace

---

# Architecture Decisions

ADR-001

Use FastAPI

ADR-002

Use PostgreSQL + pgvector

ADR-003

Use Redis

ADR-004

Use Celery

ADR-005

Use Alembic

ADR-006

Use LangGraph

ADR-007

Use OpenAI Responses API

ADR-008

Use Space-based isolation

ADR-009

Use Agent Archival instead of Hard Deletion

ADR-010

Use FinOps as a first-class platform capability
