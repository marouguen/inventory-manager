FROM python:3.12-slim

# System dependencies for psycopg2 and other libraries
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

WORKDIR /app

# ✅ Copy start.sh properly
COPY start.sh /start.sh
RUN chmod +x /start.sh

# ✅ Then copy the rest of the app
COPY . .
RUN apt-get update && apt-get install -y postgresql-client

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the app
CMD ["/bin/bash", "/start.sh"]
