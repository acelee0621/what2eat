# app/lifespan.py
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TypedDict

from fastapi import FastAPI
from httpx import AsyncClient
from loguru import logger
from redis.asyncio import Redis

from src.core.redis_db import create_auth_redis, create_cache_redis

# from src.core.database import create_db_and_tables


class State(TypedDict):
    auth_redis: Redis
    cache_redis: Redis
    http_client: AsyncClient


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[State]:
    # -------- 启动 --------
    logger.info("应用启动，开始加载所有资源...")
    # await create_db_and_tables()

    auth_redis = create_auth_redis()
    cache_redis = create_cache_redis()
    logger.info("Redis 已就绪。")
    http_client = AsyncClient(timeout=10)

    # -------- 运行 --------
    yield State(auth_redis=auth_redis, cache_redis=cache_redis, http_client=http_client)

    # -------- 关闭 --------
    await auth_redis.aclose()
    await cache_redis.aclose()
    await http_client.aclose()

    logger.info("应用关闭，资源已释放。")
