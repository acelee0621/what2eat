from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.exception import NotFoundException
from src.dishes.model import Dish


async def validate_dish(dish_id: int, session: AsyncSession) -> None:
    dish = await session.get(Dish, dish_id)
    if dish is None:
        raise NotFoundException(f"Dish with id {dish_id} not found")


async def get_dish_id(
    dish_id: Annotated[
        int | None, Path(description="使用此 ID 获取菜品，并添加至收藏.")
    ],
    session: AsyncSession = Depends(get_db),
) -> int | None:
    if dish_id is not None:
        await validate_dish(dish_id, session)
    return dish_id


# 使用方法
# dish_id: Annotated[int, Depends(get_dish_id)],
