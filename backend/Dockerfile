FROM python:3.12-slim

# System dependencies for psycopg2 and other libraries
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

WORKDIR /app

# Copy all files into the image
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the FastAPI server
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/bin/bash", "/start.sh"]


