"""Heap-based priority scoring for detected issues."""

from __future__ import annotations

import heapq


ISSUE_WEIGHTS = {
    "infection": 45,
    "dehydration": 30,
    "stress": 15,
    "anxiety": 15,
    "fatigue": 10,
    "heart_rate_uptrend": 25,
}


def _risk_level(score: int) -> str:
    if score >= 70:
        return "HIGH"
    if score >= 35:
        return "MEDIUM"
    return "LOW"


def calculate_priority(issues: list[str]) -> tuple[int, str]:
    """Calculate total risk score and level using a max-heap simulation."""
    max_heap: list[int] = []

    for issue in issues:
        weight = ISSUE_WEIGHTS.get(issue, 5)
        heapq.heappush(max_heap, -weight)

    score = 0
    while max_heap:
        score += -heapq.heappop(max_heap)

    return score, _risk_level(score)
