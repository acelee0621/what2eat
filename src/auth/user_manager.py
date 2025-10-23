# src/auth/user_manager.py
import uuid
from typing import Optional

from fastapi import Depends, Request
from redis.asyncio import Redis
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,    
    RedisStrategy    
)
from fastapi_users.authentication.strategy.db import AccessTokenDatabase,DatabaseStrategy
from fastapi_users.db import SQLAlchemyUserDatabase
from src.core.config import settings
from src.core.redis_db import get_auth_redis
from src.auth.dependencies import get_user_db, get_access_token_db

from src.auth.model import User, AccessToken

# 根据需要使用单个SECRET，或者拆分成不同的
# 分别用于重设密码及验证
SECRET = settings.jwt_secret


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
        

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/login")

# 数据库策略
def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)

# redis策略
def get_redis_strategy(auth_redis: Redis = Depends(get_auth_redis)) -> RedisStrategy:
    return RedisStrategy(auth_redis, lifetime_seconds=3600)

# 数据库认证后端
database_auth_backend = AuthenticationBackend(
    name="Database Strategy",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)

# Redis 认证后端
redis_auth_backend = AuthenticationBackend(
    name="Redis Strategy",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)


fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [redis_auth_backend])

# 默认为获取当前激活用户
get_current_user = fastapi_users.current_user(active=True)

""" 以下为不同的获取当前用户的策略，可根据需要选择 """

# 获取当前激活且已验证用户
current_verified_user = fastapi_users.current_user(active=True, verified=True)
# 获取当前激活且为超级用户
current_superuser = fastapi_users.current_user(active=True, superuser=True)