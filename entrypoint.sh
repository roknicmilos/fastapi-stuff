#!/bin/sh
set -e

# Apply Alembic migrations
uv run alembic upgrade head

# Sync dependencies
uv sync

# Run FastAPI app
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
