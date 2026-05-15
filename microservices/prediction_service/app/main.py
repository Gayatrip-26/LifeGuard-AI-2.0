import logging
import os
import threading

from fastapi import FastAPI

from app.kafka_consumer import run_consumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("prediction_service")

app = FastAPI(
    title="LifeGuard Prediction Service",
    version="0.1.0",
    description="Starter microservice for risk prediction processing.",
)


@app.on_event("startup")
def start_consumer_thread() -> None:
    consumer_thread = threading.Thread(target=run_consumer, daemon=True, name="kafka-consumer")
    consumer_thread.start()
    logger.info("Background Kafka consumer thread started.")


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": os.getenv("SERVICE_NAME", "prediction_service"),
        "kafka_bootstrap_servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
    }
