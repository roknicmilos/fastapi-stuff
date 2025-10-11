#!/bin/bash
set -e

# Wait for Postgres to be ready
>&2 echo "Waiting for Postgres at $DB_HOST:$DB_PORT..."
until PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -p "$DB_PORT" -d "$DB_NAME" -c '\q' 2>/dev/null; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
>&2 echo "Postgres is up - continuing"

# Apply Alembic migrations
uv run alembic upgrade head

# Sync dependencies
uv sync

# Run FastAPI app
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
