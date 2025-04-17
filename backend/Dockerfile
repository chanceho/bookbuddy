FROM python:3.12-slim 

WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY . .

# Explicitly set the PORT and bind to 0.0.0.0
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8000} api:app"]