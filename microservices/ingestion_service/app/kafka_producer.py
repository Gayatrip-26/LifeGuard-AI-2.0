import json
import os
import time
from typing import Any

from kafka import KafkaProducer
from lifeguard_shared.config import TopicNames

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPICS = TopicNames()

producer = None


def get_producer():
    global producer

    if producer is not None:
        return producer

    for i in range(10):
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda value: json.dumps(value).encode("utf-8"),
            )
            print("✅ Kafka connected")
            return producer
        except Exception as e:
            print(f"⏳ Waiting for Kafka... attempt {i+1}")
            time.sleep(3)

    print("❌ Kafka not available, continuing without it")
    return None


def send_health_data(data: dict[str, Any]) -> None:
    producer_instance = get_producer()

    if producer_instance is None:
        print("⚠️ Kafka unavailable, skipping send")
        return

    producer_instance.send(TOPICS.health_ingestion, value=data)
    producer_instance.flush()