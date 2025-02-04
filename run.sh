#!/bin/bash

# Export required environment variables
export DOCKER_HOST="unix://${XDG_RUNTIME_DIR}/docker.sock"

# Clean up
echo "Cleaning up existing containers..."
docker-compose down -v
docker-compose down 

# Create network if it doesn't exist
docker network create app-network 2>/dev/null || true

# Create init-scripts directory and set up wait-for-db script
mkdir -p init-scripts
chmod +x backend/wait-for-db.sh

# Start postgres first
echo "Starting PostgreSQL..."
docker-compose up --build -d postgres-db

# Wait for PostgreSQL to be ready
echo "Waiting for database to be ready..."
until docker-compose exec -T postgres-db pg_isready -U myuser; do
    echo "Database is unavailable - sleeping"
    sleep 2
done

echo "Database is ready!"

# Start all services
echo "Starting all services..."
docker-compose up --build --remove-orphans