# FastAPI Project

A simple FastAPI project with a single endpoint that returns a "hello world"
message.

## Prerequisites

- Docker and Docker Compose

## Quick Start

### Using Docker Compose

1. Clone or navigate to the project directory:
   ```bash
   cd fastapi-stuff
   ```

2. Build and run the FastAPI service:
   ```bash
   docker compose up --build
   ```

3. The API will be available at:
    - Main endpoint: http://localhost:8000/
    - Interactive API docs: http://localhost:8000/docs
    - Alternative API docs: http://localhost:8000/redoc

4. To stop the service:
   ```bash
   docker compose down
   ```

## Development

The project uses UV for dependency management inside the Docker container.
Dependencies are defined in `pyproject.toml`.

To add new dependencies:

1. Add the dependency using UV in the running container:
   ```bash
   docker compose exec fastapi uv add package-name
   ```

2. For development dependencies:
   ```bash
   docker compose exec fastapi uv add --dev package-name
   ```

3. Restart the container to ensure the new dependencies are properly loaded:
   ```bash
   docker compose restart fastapi
   ```

The dependencies will be automatically installed when the container starts
thanks to the `uv sync` command in the startup process.
