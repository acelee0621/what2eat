# src/auth/model.py
from typing import TYPE_CHECKING

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTableUUID
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base_model import Base, DateTimeMixin

if TYPE_CHECKING:
    from src.collections.model import Collection


class User(SQLAlchemyBaseUserTableUUID, Base, DateTimeMixin):
    name: Mapped[str] = mapped_column(String(64), nullable=True)

    collections: Mapped[list["Collection"]] = relationship(
        back_populates="user",  # 双向
        cascade="all, delete",  # 关键：User 被删时自动删 collections
        passive_deletes=True,  # 让数据库外键 ON DELETE CASCADE 生效
    )


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass
