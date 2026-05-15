"""Graph-based symptom relationship analysis."""

from __future__ import annotations

from typing import Any


SYMPTOM_GRAPH = {
    "high_heart_rate": ["stress", "anxiety"],
    "low_sleep": ["fatigue", "stress"],
    "high_temperature": ["infection", "dehydration"],
}


def analyze_symptoms(data: dict[str, Any]) -> list[str]:
    """Map current health signals to possible issues using a graph."""
    issues: set[str] = set()

    heart_rate = data.get("heart_rate")
    sleep_hours = data.get("sleep_hours")
    temperature = data.get("temperature")

    if isinstance(heart_rate, (int, float)) and heart_rate >= 100:
        issues.update(SYMPTOM_GRAPH["high_heart_rate"])

    if isinstance(sleep_hours, (int, float)) and sleep_hours < 6:
        issues.update(SYMPTOM_GRAPH["low_sleep"])

    if isinstance(temperature, (int, float)) and temperature >= 38:
        issues.update(SYMPTOM_GRAPH["high_temperature"])

    return sorted(issues)
