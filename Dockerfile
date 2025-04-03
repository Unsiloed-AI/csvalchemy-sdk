# Stage 1: Build environment
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies using pip
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime environment
FROM python:3.11-slim

WORKDIR /app

# Copy only the virtual environment from the builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY . .

# Ensure the virtual environment is used
ENV PATH="/opt/venv/bin:$PATH"

# Create necessary directories in one layer
RUN mkdir -p /app/{logs,outputs,temp}

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=80

# Expose the FastAPI port
EXPOSE $PORT

# Run the application with optimized uvicorn settings
# Using exec form with shell to allow environment variable expansion
CMD ["/bin/sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 2 --no-access-log"]
