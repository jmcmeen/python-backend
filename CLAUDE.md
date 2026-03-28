# CLAUDE.md

## Project Overview

This is a Python backend template using a layered architecture with FastAPI, SQLAlchemy, Pydantic, and Alembic.

## Architecture Rules

- **Endpoints are thin wrappers.** `app/api/` handlers must only validate input (via schemas), call a service, and return a response. No business logic in route handlers.
- **Business logic lives in services.** `app/services/` contains all domain logic. Services must be framework-independent and testable in isolation -- no FastAPI or SQLAlchemy imports.
- **Repositories abstract data access.** `app/repositories/` wraps all ORM/database calls behind clean method signatures. Never use raw ORM queries outside of repositories.
- **Schemas are not models.** `app/schemas/` (Pydantic) defines API contracts. `app/models/` (SQLAlchemy) defines database tables. They evolve independently.
- **Utils stay small.** If a utility in `app/utils/` grows complex, promote it to a service.
- **`main.py` is wiring only.** Mount routers, set up middleware, run startup hooks. Nothing else.

## Directory Conventions

- API versioning: `app/api/v1/`, `app/api/v2/`, etc.
- One file per domain entity in models, schemas, services, and repositories (e.g., `user.py`, `user_service.py`, `user_repo.py`).
- Tests mirror the source structure: `tests/unit/` for services/utils, `tests/integration/` for API and DB tests.
- Database migrations go in `migrations/` (Alembic).

## Tech Stack

- FastAPI + Uvicorn
- SQLAlchemy (ORM) + Alembic (migrations)
- Pydantic (validation and settings via BaseSettings)
- pytest + httpx + pytest-asyncio (testing)

## Commands

```bash
# Run dev server
uvicorn app.main:app --reload

# Run tests
pytest

# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/

# Create a migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

## Code Style

- Follow PEP 8.
- Use type hints on all function signatures.
- Async endpoints and services where appropriate.
- Keep imports organized: stdlib, third-party, local.

## Key Principles

- Separation of concerns: each layer has one job.
- Start minimal: don't create layers until they're needed.
- Testability: decouple business logic from framework and database.
- Clarity over ceremony.
