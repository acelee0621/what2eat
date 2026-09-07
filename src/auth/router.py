# src/auth/router.py
from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from src.auth.schemas import UserCreate, UserRead, UserUpdate
from src.auth.user_manager import database_auth_backend, redis_auth_backend


def register_fastapi_users_routes(
    app: FastAPI,
    fastapi_users: FastAPIUsers,
) -> None:
    """把 FastAPI-Users 的所有 router 挂到 app 上"""
    # Bearer 传输方式
    app.include_router(
        fastapi_users.get_auth_router(redis_auth_backend),
        prefix="/auth/jwt",
        tags=["auth"],
    )
    # Cookie 传输方式
    app.include_router(
        fastapi_users.get_auth_router(database_auth_backend),
        prefix="/auth/cookie",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_verify_router(UserRead),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_users_router(UserRead, UserUpdate),
        prefix="/users",
        tags=["users"],
    )
