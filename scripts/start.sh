#!/bin/bash

echo "Starting Company API with Docker Compose..."

# Проверка наличия docker-compose
if ! command -v docker compose &> /dev/null; then
    echo "Error: docker compose not found. Please install Docker and docker compose."
    exit 1
fi

# Запуск сервисов
docker-compose up -d

echo "Services started:"
echo "- API: http://localhost:8000"
echo "- API Docs: http://localhost:8000/api/docs"
echo "- Database: localhost:5432"

# Ожидание запуска API
echo "Waiting for API to be ready..."
until curl -s http://localhost:8000/health > /dev/null; do
    sleep 2
done

echo "Company API is ready!"