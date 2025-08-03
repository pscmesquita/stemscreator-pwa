# Multi-stage build for minimal final image size
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages in builder stage
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage - minimal runtime image
FROM python:3.11-slim

WORKDIR /app

# Install only runtime dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy only essential application files
COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/

# Create necessary directories
RUN mkdir -p uploads results

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Expose port
EXPOSE $PORT

# Run with minimal gunicorn settings for Railway's 4GB limit
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "1", "--timeout", "600", "--max-requests", "50", "--preload", "app:app"]
