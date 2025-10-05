FROM python:3.11-slim

WORKDIR /app

# Install UV
RUN pip install uv

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Sync dependencies and run the application
CMD ["sh", "-c", "uv sync && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload"]
