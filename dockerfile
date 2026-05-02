# Use Python 3.11 as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for psycopg2 and other tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Set PYTHONPATH so the 'src' folder is recognized
ENV PYTHONPATH=/app

# Default command (can be overridden in docker-compose)
CMD ["python", "-m", "src.models.predict"]