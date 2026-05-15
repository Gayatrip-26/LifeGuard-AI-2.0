from dataclasses import dataclass


@dataclass(frozen=True)
class TopicNames:
    health_ingestion: str = "lifeguard.health.ingestion"
    risk_predictions: str = "lifeguard.health.risk_predictions"
