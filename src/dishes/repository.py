# src/dishes/repository.py
from typing import Mapping, Any

from sqlalchemy import select, or_, desc, asc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.dishes.model import Dish


class DishRepository:
    """数据库表仓库层"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, dish_data: Mapping[str, Any]) -> Dish:
        """创建数据"""
        dish = Dish(**dish_data)
        self.session.add(dish)
        await self.session.commit()
        await self.session.refresh(dish)
        return dish

    async def get_by_id(self, dish_id: int) -> Dish | None:
        """使用 id 获取数据"""
        dish = await self.session.get(Dish, dish_id)
        if not dish:
            return None
        return dish

    async def get_all(
        self,
        *,
        search: str | None = None,
        order_by: str = "id",
        direction: str = "asc",
        limit: int = 10,
        offset: int = 0,
    ) -> list[Dish]:
        """获取所有数据"""
        query = select(Dish)

        # 1. 搜索
        if search:
            pattern = f"%{search}%"
            query = query.where(
                or_(Dish.name.ilike(pattern), Dish.description.ilike(pattern))
            )

        # 2. 排序
        allowed_sort = {"id", "name", "created_at"}
        if order_by not in allowed_sort:
            order_by = "id"
        order_column = getattr(Dish, order_by, Dish.id)
        query = query.order_by(
            desc(order_column) if direction == "desc" else asc(order_column)
        )

        # 3. 分页
        limit = min(limit, 500)
        offset = max(offset, 0)
        paginated_query = query.offset(offset).limit(limit)
        items = list(await self.session.scalars(paginated_query))

        return items

    async def update(self, dish_data: Mapping[str, Any], dish_id: int) -> Dish | None:
        """更新数据"""
        dish = await self.session.get(Dish, dish_id)
        if not dish:
            return None

        for key, value in dish_data.items():
            setattr(dish, key, value)
        await self.session.commit()
        await self.session.refresh(dish)
        return dish

    async def delete(self, dish_id: int) -> bool:
        """删除数据"""
        dish = await self.session.get(Dish, dish_id)
        if not dish:
            return False

        await self.session.delete(dish)
        await self.session.commit()
        return True
