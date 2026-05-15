import json
import logging
import os
import time

import httpx
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from app.ai_client import get_ai_explanation
from lifeguard_shared.config import TopicNames
from app.dsa_engine import analyze_symptoms, calculate_priority, detect_anomaly

BACKEND_BASE = os.getenv("BACKEND_URL", "http://backend:8000").rstrip("/")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
BACKEND_PREDICTION_SAVE_URL = os.getenv(
    "BACKEND_PREDICTION_SAVE_URL",
    f"{BACKEND_BASE}/prediction/save",
)
BACKEND_ALERT_URL = os.getenv("BACKEND_ALERT_URL", f"{BACKEND_BASE}/alert")
INTERNAL_SERVICE_TOKEN = os.getenv("INTERNAL_SERVICE_TOKEN", "")
DEFAULT_USER_ID = int(os.getenv("DEFAULT_USER_ID", "1"))

TOPICS = TopicNames()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("prediction_service.consumer")


def _service_headers() -> dict[str, str]:
    if not INTERNAL_SERVICE_TOKEN:
        return {}
    return {"X-Internal-Token": INTERNAL_SERVICE_TOKEN}


def _resolve_user_context(health_data: dict) -> tuple[int, str]:
    raw_uid = health_data.get("user_id")
    if raw_uid is None:
        user_id = DEFAULT_USER_ID
    else:
        user_id = int(raw_uid)
    patient_id = health_data.get("patient_id") or f"user_{user_id}"
    return user_id, patient_id


def create_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                TOPICS.health_ingestion,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                group_id="lifeguard-group",
                auto_offset_reset="latest",
                enable_auto_commit=True,
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            )
            logger.info("Connected to Kafka")
            return consumer

        except NoBrokersAvailable:
            logger.warning("Kafka not ready, retrying in 5 seconds...")
            time.sleep(5)


def send_critical_alert(patient_id: str, user_id: int) -> None:
    logger.warning(
        "🚨 ALERT: Critical health condition detected for %s",
        patient_id,
    )
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                BACKEND_ALERT_URL,
                headers=_service_headers(),
                json={
                    "user_id": user_id,
                    "patient_id": patient_id,
                    "message": "High health risk detected",
                },
            )
            response.raise_for_status()
    except Exception as exc:
        logger.error("Failed to POST /alert: %s", exc)


def maybe_fire_alert(prediction_output: dict) -> None:
    level = str(prediction_output.get("risk_level", "")).strip().upper()
    score = int(prediction_output.get("risk_score") or 0)

    if level == "HIGH" or score > 100:
        uid = int(prediction_output.get("user_id") or DEFAULT_USER_ID)
        send_critical_alert(prediction_output.get("patient_id", "unknown"), uid)


def run_consumer() -> None:
    consumer = create_consumer()

    logger.info("Kafka consumer started on topic: %s", TOPICS.health_ingestion)

    while True:
        try:
            for message in consumer:
                health_data = message.value

                logger.info("RECEIVED: %s", health_data)

                user_id, patient_id = _resolve_user_context(health_data)

                graph_issues = analyze_symptoms(health_data)
                trend_issues = detect_anomaly(health_data)
                issues = sorted(set(graph_issues + trend_issues))

                risk_score, risk_level = calculate_priority(issues)

                heart_rate = health_data.get("heart_rate", 0)
                temperature = health_data.get("temperature", 0)
                stress = health_data.get("stress_level", 0)
                sleep = health_data.get("sleep_hours", 0)

                extra_score = 0

                if 100 < heart_rate <= 120:
                    extra_score += 15
                elif heart_rate > 120:
                    extra_score += 30

                if 37.5 < temperature <= 38.5:
                    extra_score += 15
                elif temperature > 38.5:
                    extra_score += 30

                if 5 <= stress <= 7:
                    extra_score += 15
                elif stress > 7:
                    extra_score += 30

                if 4 <= sleep <= 5:
                    extra_score += 15
                elif sleep < 4:
                    extra_score += 30

                risk_score += extra_score

                if risk_score == 0:
                    risk_level = "LOW"
                elif risk_score <= 60:
                    risk_level = "MEDIUM"
                else:
                    risk_level = "HIGH"

                if not issues and risk_score == 0:
                    issues = ["normal"]

                prediction_output = {
                    "user_id": user_id,
                    "patient_id": patient_id,
                    "issues": issues,
                    "risk_score": risk_score,
                    "risk_level": risk_level,
                }

                logger.info("Prediction: %s", prediction_output)

                query = f"""
Patient has:
- Issues: {issues}
- Risk Level: {risk_level}
- Risk Score: {risk_score}

Explain health risks and give advice.
"""
                ai_explanation = get_ai_explanation(
                    issues,
                    query=query,
                    user_id=user_id,
                )

                payload = {
                    **prediction_output,
                    "ai_explanation": ai_explanation,
                }

                if persist_prediction(payload):
                    maybe_fire_alert(prediction_output)

        except Exception as e:
            logger.error("Error: %s", str(e))
            time.sleep(2)


def persist_prediction(payload: dict) -> bool:
    for attempt in range(3):
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.post(
                    BACKEND_PREDICTION_SAVE_URL,
                    headers=_service_headers(),
                    json=payload,
                )

            response.raise_for_status()
            return True

        except Exception as exc:
            logger.error("Attempt %d failed: %s", attempt + 1, exc)
            time.sleep(2)

    return False
