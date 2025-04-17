FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m nltk.downloader punkt wordnet averaged_perceptron_tagger
RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 10000
ENV PORT=10000

CMD ["gunicorn", "--bind", "0.0.0.0:10000", "api:app"]
