import os
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.kafka_producer import send_health_data
from lifeguard_shared.config import TopicNames

app = FastAPI(
    title="LifeGuard Ingestion Service",
    version="0.1.0",
    description="Starter microservice for real-time health data ingestion.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TOPICS = TopicNames()


class IngestionRequest(BaseModel):
    patient_id: str
    user_id: int | None = None
    heart_rate: float
    temperature: float
    stress_level: float
    sleep_hours: float
    timestamp: datetime


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": os.getenv("SERVICE_NAME", "ingestion_service"),
        "kafka_bootstrap_servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
    }


@app.post("/ingest")
def ingest_data(payload: IngestionRequest) -> dict:
    event = payload.model_dump()
    event["timestamp"] = payload.timestamp.isoformat()
    send_health_data(event)
    return {"status": "queued", "topic": TOPICS.health_ingestion, "data": event}
