# src/auth/dependencies.py
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.model import AccessToken, User
from src.core.database import get_db

""" --- FastAPI Users 专用依赖 --- """


# 获取用户数据库依赖
async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User)


# 获取访问令牌数据库依赖
async def get_access_token_db(
    session: AsyncSession = Depends(get_db),
):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)
