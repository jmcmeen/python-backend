# Python Backend Template

A clean, layered architecture template for Python backend projects built with FastAPI.

Based on the blueprint described in [The Architecture Blueprint Every Python Backend Project Needs](https://medium.com/the-pythonworld/the-architecture-blueprint-every-python-backend-project-needs-207216931123).

## Project Structure

```
app/
├── api/
│   └── v1/
│       ├── endpoints/       # Route handlers (thin wrappers, no business logic)
│       │   └── user.py
│       └── dependencies.py  # Dependency injection (auth, DB sessions, etc.)
├── core/
│   ├── config.py            # App settings via Pydantic BaseSettings + .env
│   └── security.py          # JWT, authentication, CORS setup
├── models/
│   └── user.py              # SQLAlchemy ORM models (database schema)
├── schemas/
│   └── user.py              # Pydantic models (API request/response contracts)
├── services/
│   └── user_service.py      # Business logic (framework-independent, testable)
├── repositories/
│   └── user_repo.py         # Data access abstraction (DB queries behind clean methods)
├── utils/
│   └── hashing.py           # Shared helpers (hashing, email, token generation)
└── main.py                  # App entrypoint: mount routers, middleware, startup
tests/
├── unit/                    # Isolated tests for services and utilities
└── integration/             # End-to-end API and database tests
migrations/                  # Alembic database migrations
requirements.txt
.env
```

## Architecture Layers

| Layer | Directory | Responsibility |
|-------|-----------|----------------|
| **API** | `app/api/` | Accept requests, validate input via schemas, delegate to services, return responses. No business logic. |
| **Core** | `app/core/` | Centralized config, security, CORS, logging, startup/shutdown handlers. |
| **Models** | `app/models/` | ORM entity definitions representing database tables. Evolve independently from schemas. |
| **Schemas** | `app/schemas/` | Pydantic models defining API contracts. Stable interface even as the DB changes. |
| **Services** | `app/services/` | Business logic. Framework-independent, testable in isolation. One service per domain entity. |
| **Repositories** | `app/repositories/` | Abstract raw DB operations behind clean methods. Enables swapping databases or mocking in tests. |
| **Utils** | `app/utils/` | Reusable helpers. Promote to a service if they grow too large. |

## Tech Stack

- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Migrations:** Alembic
- **Server:** Uvicorn
- **Config:** python-dotenv + Pydantic BaseSettings
- **Testing:** pytest, httpx, pytest-asyncio

## Principles

- **Separation of concerns** -- each layer has a single, clear responsibility
- **Testability** -- business logic is decoupled from the framework and database
- **Flexibility** -- swap the framework, database, or auth provider with minimal pain
- **Scalability** -- adding features doesn't require rewriting the core
- **Start minimal** -- add layers only as the project grows; clarity over ceremony

## Getting Started

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

## Agentic Development

This project includes a `CLAUDE.md` file that provides AI coding agents (Claude Code, Cursor, Copilot, etc.) with the context they need to make correct changes: architecture rules, directory conventions, common commands, and code style guidelines. When adding new domains, conventions, or non-obvious patterns, update `CLAUDE.md` so agents stay aligned with the project's expectations.
