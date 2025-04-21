FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip --requirement requirements.txt
COPY telethon_fastapi .