import json
from typing import Any

import redis

from app.core.config import settings

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)


def set_cache(key: str, value: Any, ex: int | None = 3600) -> None:
    redis_client.set(key, json.dumps(value), ex=ex)


def get_cache(key: str) -> Any | None:
    cached_value = redis_client.get(key)
    if cached_value is None:
        return None
    return json.loads(cached_value)
