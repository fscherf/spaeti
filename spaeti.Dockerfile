FROM python:3.11-slim-bookworm

WORKDIR /app

COPY . .

RUN apt update && apt install -y git
RUN pip install --no-cache-dir -e .
