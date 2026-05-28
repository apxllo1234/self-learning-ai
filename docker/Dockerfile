FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ src/
COPY tests/ tests/
COPY docs/ docs/

# Create data directory
RUN mkdir -p /app/data/memory

# Set environment
ENV PYTHONUNBUFFERED=1

# Run tests
CMD ["pytest", "tests/", "-v"]