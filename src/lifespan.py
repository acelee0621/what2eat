# app/lifespan.py
from typing import TypedDict
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from redis.asyncio import Redis
from loguru import logger

from src.core.redis_db import create_auth_redis, create_cache_redis

# from src.core.database import create_db_and_tables


class State(TypedDict, total=False):
    auth_redis: Redis
    cache_redis: Redis


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[State]:
    # -------- 启动 --------
    logger.info("应用启动，开始加载所有资源...")
    # await create_db_and_tables()

    auth_redis = create_auth_redis()
    cache_redis = create_cache_redis()
    logger.info("Redis 已就绪。")

    # -------- 运行 --------
    yield State(auth_redis=auth_redis, cache_redis=cache_redis)

    # -------- 关闭 --------
    await auth_redis.aclose()
    await cache_redis.aclose()

    logger.info("应用关闭，资源已释放。")
