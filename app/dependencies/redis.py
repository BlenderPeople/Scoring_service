from __future__ import annotations

from typing import Optional

import redis.asyncio as redis

_redis_client: Optional[redis.Redis] = None


def get_redis() -> redis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis(host="redis", decode_responses=True)
    return _redis_client

