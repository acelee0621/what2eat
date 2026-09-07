# src/collections/router.py
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Path, Query, status
from loguru import logger

from src.auth.schemas import UserRead
from src.auth.user_manager import get_current_user
from src.collections.dependencies import get_dish_id
from src.collections.repository import CollectionRepository
from src.collections.schema import (
    CollectionCreate,
    CollectionResponse,
    CollectionUpdate,
)
from src.collections.service import CollectionService
from src.core.database import get_db

router = APIRouter(prefix="/collections", tags=["Collections"])


# 注入仓库 + 服务层
async def get_collection_service(session=Depends(get_db)) -> CollectionService:
    repository = CollectionRepository(session)
    return CollectionService(repository)


@router.post(
    "/", response_model=CollectionResponse, status_code=status.HTTP_201_CREATED
)
async def create_collection(
    collection_data: CollectionCreate,
    service: CollectionService = Depends(get_collection_service),
    current_user: UserRead = Depends(get_current_user),
) -> CollectionResponse:
    """创建收藏"""
    new_collection = await service.create_collection(collection_data, current_user)
    return new_collection


@router.get("/{collection_id}", response_model=CollectionResponse)
async def get_collection(
    collection_id: int = Path(..., description="收藏ID"),
    service: CollectionService = Depends(get_collection_service),
    current_user: UserRead = Depends(get_current_user),
) -> CollectionResponse:
    """获取单个收藏"""

    logger.debug(f"正在获取收藏 ID: {collection_id}")
    try:
        collection = await service.get_collection_by_id(collection_id, current_user)
        logger.info(f"获取到收藏, ID: {collection_id}")
        return collection
    except Exception as e:
        logger.error(f"获取 ID 为 {collection_id} 的收藏时出错: {e!s}")
        raise


@router.get("/", response_model=list[CollectionResponse])
async def list_collections(
    search: str | None = Query(None, description="搜索关键词"),
    order_by: Literal["id", "name", "created_at"] = Query("id", description="排序字段"),
    direction: Literal["asc", "desc"] = Query("asc", description="排序方向"),
    limit: int = Query(10, ge=1, le=500),
    offset: int = Query(0, ge=0),
    service: CollectionService = Depends(get_collection_service),
    current_user: UserRead = Depends(get_current_user),
) -> list[CollectionResponse]:
    """查询所有收藏"""
    collections = await service.list_collections(
        search=search,
        order_by=order_by,
        direction=direction,
        limit=limit,
        offset=offset,
        current_user=current_user,
    )
    return collections


@router.patch("/{collection_id}", response_model=CollectionResponse)
async def update_collection(
    collection_data: CollectionUpdate,
    collection_id: int = Path(..., description="收藏ID"),
    service: CollectionService = Depends(get_collection_service),
    current_user: UserRead = Depends(get_current_user),
) -> CollectionResponse:
    """更新收藏"""
    collection = await service.update_collection(
        collection_id, collection_data, current_user
    )
    return collection


@router.delete(
    "/{collection_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_collection(
    collection_id: int = Path(..., description="收藏ID"),
    service: CollectionService = Depends(get_collection_service),
    current_user: UserRead = Depends(get_current_user),
):
    """删除收藏"""

    await service.delete_collection(collection_id, current_user)


@router.post(
    "/{collection_id}/dishes/{dish_id}",
    response_model=CollectionResponse,
    status_code=status.HTTP_200_OK,
    summary="添加菜品到收藏夹",
)
async def add_dish_to_collection(
    collection_id: int,
    # dish_id: int,
    dish_id: Annotated[int, Depends(get_dish_id)],
    service: CollectionService = Depends(get_collection_service),
    current_user: UserRead = Depends(get_current_user),
) -> CollectionResponse:
    try:
        updated_collection = await service.add_dish_to_collection(
            collection_id, dish_id, current_user
        )
        logger.info(
            f"Added dish {dish_id} to collection {collection_id} for user {current_user.id}"
        )
        return updated_collection
    except Exception as e:
        logger.error(
            f"Failed to add dish {dish_id} to collection {collection_id}: {e!s}"
        )
        raise


@router.delete(
    "/{collection_id}/dishes/{dish_id}",
    response_model=CollectionResponse,
    status_code=status.HTTP_200_OK,
    summary="从收藏夹删除菜品",
)
async def remove_tag_from_note(
    collection_id: int,
    dish_id: int,
    service: CollectionService = Depends(get_collection_service),
    current_user: UserRead = Depends(get_current_user),
) -> CollectionResponse:
    try:
        updated_collection = await service.remove_dish_from_collection(
            collection_id, dish_id, current_user
        )
        logger.info(
            f"Removed dish {dish_id} from collection {collection_id} for user {current_user.id}"
        )
        return updated_collection
    except Exception as e:
        logger.error(
            f"Failed to remove dish {dish_id} from collection {collection_id}: {e!s}"
        )
        raise
