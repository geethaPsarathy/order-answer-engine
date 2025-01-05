import asyncio
from redis.asyncio import Redis
import json

# Initialize Redis connection
redis = Redis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)

async def get_from_cache(key: str):
    """
    Retrieve data from Redis cache.
    """
    cached_data = await redis.get(key)
    if cached_data:
        return json.loads(cached_data)
    return None

async def set_to_cache(key: str, value: dict, ttl: int = 3600):
    """
    Store data in Redis cache with an optional TTL (default: 1 hour).
    """
    await redis.set(key, json.dumps(value), ex=ttl)
