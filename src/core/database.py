from typing import AsyncGenerator

from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.core.config import settings
from src.core.base_model import Base

# 创建数据库引擎和会话工厂
engine = create_async_engine(settings.database_url, **settings.engine_options)

SessionFactory = async_sessionmaker(
    class_=AsyncSession, autoflush=False, expire_on_commit=False, bind=engine
)


# 数据库依赖注入
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactory() as session:
        yield session


# 用于临时使用的创建数据库表的函数
# 请在生产环境中使用 Alembic 进行数据库迁移
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("数据库表创建成功。")
