#!/bin/bash

cd /app

echo "⏳ Waiting for database to be ready..."
until pg_isready -h inventory_db -p 5432 -U postgres; do
  sleep 1
done

echo "📦 PWD: $(pwd)"
echo "📁 Contents:"
ls -al

echo "⏳ Running Alembic migrations..."
alembic upgrade head

echo "✅ Alembic migrations complete."

echo "👤 Checking for default admin user..."
export PYTHONPATH=/app
python ./scripts/init_admin.py

echo "🚀 Starting FastAPI app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
