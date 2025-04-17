# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies required for some Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Download required NLTK data
RUN python -m nltk.downloader punkt wordnet averaged_perceptron_tagger

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy the rest of the project files
COPY . .

# Expose the port (Render uses this for routing)
EXPOSE 10000
ENV PORT=10000

# Start the Flask app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "api:app"]
