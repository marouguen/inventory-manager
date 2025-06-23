#!/bin/bash

cd /app

echo "⏳ Waiting for database to be ready..."
until pg_isready -h db -p 5432 -U postgres; do
  sleep 1
done

echo "⏳ Running Alembic migrations..."
alembic upgrade head

echo "✅ Alembic migrations complete."

echo "👤 Checking for default admin user..."
export PYTHONPATH=/app
python ./scripts/init_admin.py

echo "🚀 Starting FastAPI app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
