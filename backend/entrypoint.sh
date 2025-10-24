#!/bin/bash
set -e

# Ensure Python can import the project root (so `src` can be imported inside the container)
# This makes /app (the Docker WORKDIR) available on PYTHONPATH.
export PYTHONPATH="/app${PYTHONPATH:+:$PYTHONPATH}"

# Wait for Postgres to be ready
>&2 echo "Waiting for Postgres at $DB_HOST:$DB_PORT..."
until PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -p "$DB_PORT" -d "$DB_NAME" -c '\q' 2>/dev/null; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
>&2 echo "Postgres is up - continuing"

# Apply Alembic migrations
uv run alembic upgrade head

# Run FastAPI app
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
