"""Sliding window trend detection for patient vitals."""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Any


WINDOW_SIZE = 5
_heart_rate_history: dict[str, deque[float]] = defaultdict(lambda: deque(maxlen=WINDOW_SIZE))


def detect_anomaly(data: dict[str, Any]) -> list[str]:
    """Maintain last N readings and detect simple continuous-rise anomalies."""
    patient_id = str(data.get("patient_id", "unknown"))
    heart_rate = data.get("heart_rate")

    if not isinstance(heart_rate, (int, float)):
        return []

    history = _heart_rate_history[patient_id]
    history.append(float(heart_rate))

    if len(history) < WINDOW_SIZE:
        return []

    is_increasing = all(history[idx] < history[idx + 1] for idx in range(len(history) - 1))
    if is_increasing:
        return ["heart_rate_uptrend"]
    return []
