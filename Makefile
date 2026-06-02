.PHONY: help install dev-setup dev test test-unit test-integration lint fmt typecheck \
        migrate migration up down nuke clean

help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install all dependencies into the local venv
	uv sync

dev-setup: install ## First-time onboarding: install + pre-commit + .env
	uv run pre-commit install
	@if [ ! -f .env ]; then cp .env.example .env && echo "Created .env from .env.example — set SECRET_KEY before running."; fi

dev: ## Run the dev server with autoreload
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test: ## Run all tests with coverage
	uv run pytest --cov=app --cov-report=term-missing --cov-fail-under=80

test-unit: ## Run unit tests only
	uv run pytest tests/unit -v

test-integration: ## Run integration tests only
	uv run pytest tests/integration -v

lint: ## Check formatting and lint rules
	uv run ruff check .
	uv run ruff format --check .

fmt: ## Auto-format and apply safe lint fixes
	uv run ruff format .
	uv run ruff check --fix .

typecheck: ## Run mypy in strict mode against the app package
	uv run mypy app

migrate: ## Apply all pending Alembic migrations
	uv run alembic upgrade head

migration: ## Create a new auto-generated migration: `make migration m="add foo table"`
	@if [ -z "$(m)" ]; then echo "Usage: make migration m=\"description\""; exit 1; fi
	uv run alembic revision --autogenerate -m "$(m)"

up: ## Start the stack (Postgres + app) in the background; rebuilds if needed
	docker compose up -d --build

down: ## Stop the stack (containers + network); preserves volumes
	docker compose down

nuke: ## Remove this project's containers, network, volumes, and built image
	docker compose down -v --rmi all --remove-orphans

clean: ## Remove caches, coverage, and local DB files
	rm -rf .pytest_cache .ruff_cache .mypy_cache htmlcov .coverage coverage.xml
	rm -f *.db *.db-journal
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
