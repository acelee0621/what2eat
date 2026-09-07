# src/collections/repository.py
from collections.abc import Mapping
from typing import Any

from sqlalchemy import asc, desc, func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.collections.model import Collection
from src.core.exception import AlreadyExistsException, NotFoundException
from src.dishes.model import Dish


class CollectionRepository:
    """数据库表仓库层"""

    MAX_PAGE_SIZE = 500

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: Mapping[str, Any], current_user) -> Collection:
        """创建数据"""
        item = Collection(**data, user_id=current_user.id)
        self.session.add(item)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise AlreadyExistsException("Collection with this name already exists")
        await self.session.refresh(item)
        return item

    async def get_by_id(self, item_id: int, current_user) -> Collection:
        """使用 id 获取数据"""
        query = (
            select(Collection).where(
                Collection.id == item_id, Collection.user_id == current_user.id
            )
            # .options(selectinload(Collection.dishes))
            #  models里定义了lazy属性就无需这条
        )
        result = await self.session.scalars(query)
        item = result.one_or_none()
        if not item:
            raise NotFoundException(f"Collection with id {item_id} not found")
        return item

    async def get_all(
        self,
        *,
        search: str | None = None,
        order_by: str = "id",
        direction: str = "asc",
        limit: int = 10,
        offset: int = 0,
        current_user,
    ) -> tuple[list[Collection], int]:
        """获取所有数据"""

        query = select(Collection).where(Collection.user_id == current_user.id)

        # 1. 搜索
        if search:
            pattern = f"%{search}%"
            query = query.where(
                or_(Collection.name.ilike(pattern), Collection.note.ilike(pattern))
            )

        # 2. 排序
        allowed_sort = {"id", "name", "created_at"}
        if order_by not in allowed_sort:
            order_by = "id"
        order_column = getattr(Collection, order_by, Collection.id)
        query = query.order_by(
            desc(order_column) if direction == "desc" else asc(order_column)
        )

        # 3. 总数
        count_query = select(func.count()).select_from(query.order_by(None).subquery())
        total = (await self.session.scalar(count_query)) or 0

        # 34. 分页
        limit = min(limit, self.MAX_PAGE_SIZE)
        offset = max(offset, 0)
        paginated_query = query.offset(offset).limit(limit)

        items = list(await self.session.scalars(paginated_query))

        return items, total

    async def update(
        self, data: Mapping[str, Any], item_id: int, current_user
    ) -> Collection:
        """更新数据"""
        query = select(Collection).where(
            Collection.id == item_id, Collection.user_id == current_user.id
        )
        result = await self.session.scalars(query)
        item = result.one_or_none()
        if not item:
            raise NotFoundException(f"Collection with id {item_id} not found")

        for key, value in data.items():
            setattr(item, key, value)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def delete(self, item_id: int, current_user) -> None:
        """删除数据"""
        item = await self.session.get(Collection, item_id)
        if not item or item.user_id != current_user.id:
            raise NotFoundException(f"Collection with id {item_id} not found")

        await self.session.delete(item)
        await self.session.commit()

    async def add_dish_to_collection(
        self, collection_id: int, dish_id: int, current_user
    ) -> Collection:
        collection = await self.get_by_id(collection_id, current_user)

        query = select(Dish).where(Dish.id == dish_id)
        result = await self.session.scalars(query)
        dish = result.one_or_none()
        if not dish:
            raise NotFoundException(f"Dish with id {dish_id} not found")

        if dish in collection.dishes:
            raise AlreadyExistsException(
                f"Dish with id {dish_id} already associated with collection {collection_id}"
            )

        collection.dishes.append(dish)
        await self.session.commit()
        await self.session.refresh(collection)
        return collection

    async def remove_dish_from_collection(
        self, collection_id: int, dish_id: int, current_user
    ) -> Collection:
        collection = await self.get_by_id(collection_id, current_user)

        query = select(Dish).where(Dish.id == dish_id)
        result = await self.session.scalars(query)
        dish = result.one_or_none()
        if not dish:
            NotFoundException(f"Dish with id {dish_id} not found")

        if dish not in collection.dishes:
            raise NotFoundException(
                f"Dish with id {dish_id} not associated with note {collection_id}"
            )

        collection.dishes.remove(dish)
        await self.session.commit()
        await self.session.refresh(collection)
        return collection
