import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    UUID,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base_model import Base, DateTimeMixin

if TYPE_CHECKING:
    from src.auth.model import User
    from src.dishes.model import Dish


class Collection(Base, DateTimeMixin):
    __tablename__ = "collections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    # 外键
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    # 1. 与 User 的多对一关系
    user: Mapped["User"] = relationship("User", back_populates="collections")

    # 2. 与 Dish 的多对多关系
    dishes: Mapped[list["Dish"]] = relationship(
        "Dish",
        secondary="collection_dish",  # ← 字符串表名
        back_populates="collections",
        lazy="selectin",
    )


# 中间表
class CollectionDish(Base):
    __tablename__ = "collection_dish"
    __table_args__ = ({"comment": "收藏-菜品 中间表"},)

    collection_id: Mapped[int] = mapped_column(
        ForeignKey("collections.id", ondelete="CASCADE"), primary_key=True
    )
    dish_id: Mapped[int] = mapped_column(
        ForeignKey("dishes.id", ondelete="CASCADE"), primary_key=True
    )
