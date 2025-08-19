# syntax=docker/dockerfile:1

# 1) Build the React UI
FROM node:20-alpine AS ui
WORKDIR /ui
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm install
COPY frontend ./frontend
RUN cd frontend && npm run build

# 2) Python runtime + built UI
FROM python:3.11-slim
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY --from=ui /ui/frontend/dist ./frontend/dist
RUN mkdir -p /app/data
VOLUME ["/app/data"]
ENV VV_DATA_DIR=/app/data
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
