FROM python:3.12-slim

# Install system packages required by psycopg2 and others
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
