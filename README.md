# FastAPI Stuff

A project that includes a FastAPI backend and a simple HTML/CSS/JS frontend served with Nginx.

## Prerequisites

- Docker and Docker Compose

## Quick Start

### Using Docker Compose

1.  Clone or navigate to the project directory:
    ```bash
    cd fastapi-stuff
    ```

2.  Run the services (in detached mode):
    ```bash
    docker compose up -d --build
    ```

3.  The applications will be available at:
    -   **Frontend**: [http://localhost:8080/](http://localhost:8080/)
    -   **Backend API**: [http://localhost:8000/](http://localhost:8000/)
    -   **Interactive API docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
    -   **Alternative API docs**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

4.  To stop the services:
    ```bash
    docker compose down
    ```

## Project Structure

-   `backend/`: Contains the FastAPI application.
-   `frontend/`: Contains the static frontend files (HTML, CSS, JS) and Nginx configuration.
-   `docker-compose.yml`: Defines the `fastapi`, `frontend`, `db`, and `redis` services.

## Development

The backend uses UV for dependency management inside the Docker container.
Dependencies are defined in `backend/pyproject.toml`.

To add new dependencies to the backend:

1.  Add the dependency using UV in the running container:
    ```bash
    docker compose exec fastapi uv add package-name
    ```

2.  For development dependencies:
    ```bash
    docker compose exec fastapi uv add --dev package-name
    ```

3.  Restart the container to ensure the new dependencies are properly loaded:
    ```bash
    docker compose restart fastapi
    ```

The dependencies will be automatically installed when the container starts
thanks to the `uv sync` command in the startup process.
