# Dockerfile which can be used for deploying the bot as a Docker container.

FROM python:3.10-slim

RUN pip install --no-cache-dir --upgrade pip

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY sources.yml .

CMD ["python", "src/main.py"]