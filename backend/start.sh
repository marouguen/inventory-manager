#!/bin/bash

cd /app

echo "⏳ Running Alembic migrations..."
alembic upgrade head

echo "✅ Alembic migrations complete."

echo "👤 Checking for default admin user..."
export PYTHONPATH=/app
python ./scripts/init_admin.py

echo "🚀 Starting FastAPI app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
