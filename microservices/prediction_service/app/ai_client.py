import logging
import os

import httpx

logger = logging.getLogger("prediction_service.ai")
AI_QUERY_URL = os.getenv("BACKEND_AI_URL", "http://backend:8000/ai/query")
INTERNAL_SERVICE_TOKEN = os.getenv("INTERNAL_SERVICE_TOKEN", "")
DEFAULT_USER_ID = int(os.getenv("DEFAULT_USER_ID", "1"))


def build_query(issues: list[str]) -> str:
    return f"Explain health risks for: {', '.join(issues)}"


def _service_headers() -> dict[str, str]:
    if not INTERNAL_SERVICE_TOKEN:
        return {}
    return {"X-Internal-Token": INTERNAL_SERVICE_TOKEN}


def get_ai_explanation(
    issues: list[str],
    query: str | None = None,
    user_id: int | None = None,
) -> str:
    if not issues:
        return "No active issues detected."

    query_text = query or build_query(issues)
    uid = user_id if user_id is not None else DEFAULT_USER_ID

    try:
        body_json: dict = {"query": query_text, "user_id": uid}
        with httpx.Client(timeout=8.0) as client:
            response = client.post(
                AI_QUERY_URL,
                headers=_service_headers(),
                json=body_json,
            )
            response.raise_for_status()
            body = response.json()
            return body.get("answer", "No explanation returned.")
    except Exception as exc:
        logger.warning("AI explanation unavailable: %s", exc)
        return "Basic analysis: Possible health imbalance detected. Monitor your vitals."
