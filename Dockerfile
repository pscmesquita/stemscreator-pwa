# Minimal Dockerfile for Railway - Under 1GB
FROM python:3.11-slim

WORKDIR /app

# Install only essential system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy minimal requirements (no AI dependencies)
COPY requirements-light.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app-light.py app.py
COPY templates/ ./templates/
COPY static/ ./static/

# Create necessary directories
RUN mkdir -p uploads results

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Expose port
EXPOSE $PORT

# Run with minimal gunicorn settings
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--timeout", "300", "app:app"]
