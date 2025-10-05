FROM python:3.11-slim

WORKDIR /app

# Install UV
RUN pip install uv

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Make entrypoint.sh executable
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
