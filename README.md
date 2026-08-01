# CHRONOS

> The AI engineer that writes tomorrow's incident report today.

CHRONOS is an AI-native engineering platform that evaluates pull requests before merge and produces pre-mortems, risk scores, rollback plans, and counter-PRs. It includes a complete offline Demo Mode with a seeded repository, incident corpus, RAG pipeline, and multi-agent swarm.

## Stack

- **Frontend:** React, TypeScript, Vite, Tailwind CSS, React Router, TanStack Query, Framer Motion, shadcn-style components
- **Backend:** FastAPI, SQLAlchemy 2, PostgreSQL, Alembic, Pydantic Settings

## Quick start

1. Copy `.env.example` to `.env` and set secrets.
2. Run `docker compose up --build`.
3. Open `http://localhost:5173`; API docs are at `http://localhost:8000/docs`.

The compose API startup applies migrations and seeds a deterministic demo account and repository. For local development, see [docs/development.md](docs/development.md).

For the hackathon walkthrough, see [Judge Demo Guide](docs/judge-demo.md). Architecture and deployment guidance are in [Architecture](docs/architecture.md) and [Deployment](docs/deployment.md).

## Architecture

`backend/orchestrator`, `backend/agents`, and `backend/rag` are intentionally dependency-isolated. Future providers should implement agent contracts there and persist only normalized results through services. HTTP handlers must not depend directly on an AI provider.

## Security notes

- Replace all development secrets before deployment.
- GitHub OAuth values are placeholders until configured.
- The demo login endpoint is development-only by default; set `ENABLE_DEMO_AUTH=false` in production.
