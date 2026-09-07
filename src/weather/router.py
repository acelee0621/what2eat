import httpx
from fastapi import APIRouter, Depends, Query
from redis.asyncio import Redis

from src.core.exception import NotFoundException
from src.core.redis_db import get_cache_redis
from src.weather.cache_weather import fetch_weather_with_cache
from src.weather.dependencies import get_http_client
from src.weather.schemas import WeatherResponse
from src.weather.service import fetch_weather

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("", response_model=WeatherResponse)
async def weather(
    city: str = Query(..., description="城市名称，例如: 北京"),
    client: httpx.AsyncClient = Depends(get_http_client),
):
    data = await fetch_weather(client, city)
    return data


@router.get("/cached", response_model=WeatherResponse)
async def weather_cached(
    city: str = Query(..., description="城市名称，例如: 北京"),
    client: httpx.AsyncClient = Depends(get_http_client),
    redis: Redis = Depends(get_cache_redis),
):
    data = await fetch_weather_with_cache(client, redis, city)
    if data is None:
        raise NotFoundException("无法获取该城市天气数据")
    return data
