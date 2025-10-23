FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for database client and builds
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project metadata so uv can install dependencies
COPY pyproject.toml uv.lock* ./

# Upgrade pip and install uv package manager
RUN pip install --upgrade pip \
    && pip install --no-cache-dir uv

# Ensure uv will create the venv in /app/.venv and make it available on PATH
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Use uv to sync/install dependencies (this will create /app/.venv)
RUN uv sync

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Make entrypoint.sh executable
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
