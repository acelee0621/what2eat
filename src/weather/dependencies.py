from typing import cast

from fastapi import Request
from httpx import AsyncClient


# HTTP 客户端依赖
async def get_http_client(request: Request) -> AsyncClient:
    return cast(AsyncClient, request.state.http_client)
