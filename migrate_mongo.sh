#!/bin/bash
set -e

echo "Starting MongoDB migration process..."

# Stop all running containers
echo "Stopping all running containers..."
docker-compose down -v

# Rebuild the containers with the new MongoDB configuration
echo "Rebuilding containers with MongoDB configuration..."
docker-compose build

# Start the services
echo "Starting services..."
docker-compose up -d

# Wait for services to start
echo "Waiting for services to start..."
sleep 15

# Run migrations for both services
echo "Running migrations for user_management_service..."
docker-compose exec user_management_service python manage.py makemigrations
docker-compose exec user_management_service python manage.py migrate

echo "Running migrations for core_service..."
docker-compose exec core_service python manage.py makemigrations
docker-compose exec core_service python manage.py migrate

# Run data migration scripts
echo "Running data migration for user_management_service..."
docker-compose exec user_management_service python migrate_to_mongodb.py

echo "Running data migration for core_service..."
docker-compose exec core_service python migrate_to_mongodb.py

echo "MongoDB migration completed successfully!" 