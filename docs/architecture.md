# CHRONOS architecture

```mermaid
flowchart LR
  UI[React application] -->|REST / WebSocket| API[FastAPI]
  API --> INT[Repository intelligence]
  INT --> RAG[Embedding + vector store]
  INT --> CTX[AnalysisContext]
  CTX --> ORCH[Async agent orchestrator]
  ORCH --> AGENTS[Specialist agent swarm]
  AGENTS --> DEBATE[Immutable debate log]
  ORCH --> ARTIFACTS[Pre-mortem / rollback / counter PR]
  API --> DB[(PostgreSQL)]
  API --> DEMO[Offline demo seed]
```

The intelligence pipeline produces the sole input to agents. Agents never read GitHub or database state directly; they return typed findings through the orchestrator and DebateLog.
