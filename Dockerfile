FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY wait-for-it.sh ./
RUN chmod +x ./wait-for-it.sh