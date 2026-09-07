# src/collections/service.py
from src.collections.repository import CollectionRepository
from src.collections.schema import (
    CollectionCreate,
    CollectionResponse,
    CollectionUpdate,
)


class CollectionService:
    """业务逻辑层（Service Layer）"""

    def __init__(self, repository: CollectionRepository):
        self.repository = repository

    async def create_collection(
        self, data: CollectionCreate, current_user
    ) -> CollectionResponse:
        """创建收藏，处理唯一约束冲突"""
        dict_data = data.model_dump()
        item = await self.repository.create(dict_data, current_user)
        return CollectionResponse.model_validate(item)

    async def get_collection_by_id(
        self, item_id: int, current_user
    ) -> CollectionResponse:
        """通过 ID 获取收藏"""
        item = await self.repository.get_by_id(item_id, current_user)
        return CollectionResponse.model_validate(item)

    async def list_collections(
        self,
        *,
        search: str | None = None,
        order_by: str = "id",
        direction: str = "asc",
        limit: int = 10,
        offset: int = 0,
        current_user,
    ) -> list[CollectionResponse]:
        """查询所有收藏"""
        items, total = await self.repository.get_all(
            search=search,
            order_by=order_by,
            direction=direction,
            limit=limit,
            offset=offset,
            current_user=current_user,
        )
        # TODO: 未来需要分页信息时可使用 total
        return [CollectionResponse.model_validate(item) for item in items]

    async def update_collection(
        self, item_id: int, item_data: CollectionUpdate, current_user
    ) -> CollectionResponse:
        """更新收藏"""
        update_data = item_data.model_dump(exclude_unset=True, exclude_none=True)
        updated = await self.repository.update(update_data, item_id, current_user)
        return CollectionResponse.model_validate(updated)

    async def delete_collection(self, item_id: int, current_user) -> None:
        """删除收藏"""

        await self.repository.delete(item_id, current_user)

    async def add_dish_to_collection(
        self, collection_id: int, dish_id: int, current_user
    ) -> CollectionResponse:
        result = await self.repository.add_dish_to_collection(
            collection_id, dish_id, current_user
        )
        return CollectionResponse.model_validate(result)

    async def remove_dish_from_collection(
        self, collection_id: int, dish_id: int, current_user
    ) -> CollectionResponse:
        note = await self.repository.remove_dish_from_collection(
            collection_id, dish_id, current_user
        )
        return CollectionResponse.model_validate(note)
