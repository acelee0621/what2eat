# src/auth/model.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTableUUID
from src.core.base_model import Base, DateTimeMixin


class User(SQLAlchemyBaseUserTableUUID, Base, DateTimeMixin):
    name: Mapped[str] = mapped_column(String(64), nullable=True)


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass
