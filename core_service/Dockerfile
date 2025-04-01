# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY core_service/ .

# Run migrations and start the server
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8001 core_service.wsgi:application"]