FROM python:3.11-slim

# Create non-root user
RUN groupadd -g 1001 appuser && \
    useradd -u 1001 -g appuser appuser

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc && \
    rm -rf /var/lib/apt/lists/*

# Create writable directory for SQLite
RUN mkdir -p /app && chown -R appuser:appuser /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
