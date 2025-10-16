from datetime import datetime, timezone

from sqlalchemy import MetaData, func, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.core.config import settings


database_naming_convention = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class Base(DeclarativeBase):
    # 全局统一 metadata
    metadata = MetaData(naming_convention=database_naming_convention)


class DateTimeMixin:
    if settings.db_type == "postgres":
        # PostgreSQL 原生支持 now() 和 onupdate
        created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
            index=True,
        )
        updated_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )
    else:
        # SQLite: 使用 Python 层默认值模拟
        created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            # 插入时用应用层时间,生产环境推荐使用 Unix 时间戳
            default=datetime.now(timezone.utc),
            nullable=False,
            index=True,
        )
        updated_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=datetime.now(timezone.utc),
            onupdate=datetime.now(timezone.utc),
            nullable=False,
        )
