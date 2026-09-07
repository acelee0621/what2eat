# src/main.py
from fastapi import FastAPI, Response

from src.auth.router import register_fastapi_users_routes

# FastAPI Users 路由引入
from src.auth.user_manager import fastapi_users
from src.collections.router import router as collections_router
from src.core.config import settings
from src.core.exception import register_exception_handlers
from src.dishes.router import router as dishes_router
from src.lifespan import lifespan
from src.weather.router import router as weather_router

# from src.core.config import get_settings, Settings

# from dotenv import load_dotenv
# from pathlib import Path
# load_dotenv(Path(__file__).parent.parent / ".env")


app = FastAPI(
    app_name=settings.app_name,
    version="0.1.0",
    description="FastAPI 练习项目实战",
    lifespan=lifespan,
)

# 注册全局异常处理
register_exception_handlers(app)

# 注册 FastAPI-Users 路由
register_fastapi_users_routes(app, fastapi_users)

# 引入菜品路由
app.include_router(dishes_router)

# 引入收藏路由
app.include_router(collections_router)

# 引入天气路由
app.include_router(weather_router)

# 路由引入
# @app.get("/")
# def read_root(
#     # 使用 FastAPI 的依赖注入系统来获取配置实例
#     # FastAPI 会自动调用 get_settings()，由于缓存的存在，这几乎没有开销
#     settings: Settings = Depends(get_settings),
# ):
#     """
#     一个示例端点，演示如何访问配置。
#     """
#     return {
#         "message": f"Hello from the {settings.app_name}!",
#         # 演示如何使用在模型中动态计算的属性
#         "database_url": settings.database_url,
#         "jwt_secret": settings.jwt_secret,
#     }


@app.get("/health")
async def health_check(response: Response):
    response.status_code = 200
    return {"status": "ok 👍 "}
