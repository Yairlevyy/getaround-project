FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD mlflow server \
    --host 0.0.0.0 \
    --port $PORT \
    --backend-store-uri $MLFLOW_DB_URL \
    --default-artifact-root $MLFLOW_ARTIFACT_ROOT