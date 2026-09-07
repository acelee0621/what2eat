# src/auth/schemas.py
import uuid
from datetime import datetime

from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[uuid.UUID]):
    name: str = Field(max_length=64)
    created_at: datetime
    updated_at: datetime


class UserCreate(schemas.BaseUserCreate):
    name: str | None = Field(None, max_length=64)


class UserUpdate(schemas.BaseUserUpdate):
    name: str | None = Field(None, max_length=64)
