import json

import httpx
from loguru import logger
from redis.asyncio import Redis

from src.weather.service import fetch_weather

CACHE_TTL = 60  # 缓存 60 秒，可根据 API 更新频率调节


async def fetch_weather_with_cache(client: httpx.AsyncClient, redis: Redis, city: str):
    cache_key = f"weather:{city}"

    logger.info(f"尝试从 Redis 获取缓存: {cache_key}")
    # 1) 尝试从 Redis 读取缓存
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached.encode("utf-8"))
    logger.info("缓存未命中，尝试从 API 获取数据")
    # 2) 调用原始 fetch_weather
    data = await fetch_weather(client, city)
    logger.info(f"从 API 获取到数据: {data}")
    if data is None:
        return None
    logger.info(f"数据写入缓存: {cache_key}")
    # 3) 写入缓存
    await redis.set(cache_key, json.dumps(data), ex=CACHE_TTL)
    return data
