FROM python:3.11-slim

WORKDIR /app

COPY microservices/ingestion_service/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --prefer-binary --timeout 100 -r requirements.txt
COPY microservices/ingestion_service/app ./app
COPY shared/python ./shared/python

ENV PYTHONPATH=/app:/app/shared/python

EXPOSE 8101

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8101"]
