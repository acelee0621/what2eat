from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base_model import Base, DateTimeMixin

if TYPE_CHECKING:
    from src.collections.model import Collection


class Dish(Base, DateTimeMixin):
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    collections: Mapped[list["Collection"]] = relationship(
        "Collection",
        secondary="collection_dish",
        back_populates="dishes",
    )
