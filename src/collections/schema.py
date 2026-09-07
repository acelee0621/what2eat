from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field

from src.dishes.schema import DishResponse


# 公共字段基类
class CollectionBase(BaseModel):
    name: Annotated[str, Field(..., max_length=255, description="收藏名称")]
    note: Annotated[str | None, Field(None, description="收藏描述")]


# 创建模型
class CollectionCreate(CollectionBase):
    """用于创建收藏"""


# 更新模型（全部可选）
class CollectionUpdate(BaseModel):
    name: Annotated[str | None, Field(None, max_length=255, description="收藏名称")]
    note: Annotated[str | None, Field(None, description="收藏描述")]


# 响应模型（含时间戳）
class CollectionResponse(CollectionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    dishes: list["DishResponse"]

    model_config = {"from_attributes": True}


# 查询参数模型
class CollectionQueryParams(BaseModel):
    """菜品列表查询参数"""

    search: Annotated[
        str | None, Field(description="搜索关键词，可根据名称或描述进行模糊匹配")
    ] = None

    order_by: Annotated[
        Literal["id", "name", "created_at"],
        Field(description="排序字段，可选：id、name、created_at"),
    ] = "id"

    direction: Annotated[
        Literal["asc", "desc"],
        Field(description="排序方向，可选：asc（升序）、desc（降序）"),
    ] = "asc"

    limit: Annotated[
        int, Field(ge=1, le=500, description="每页返回的最大条数（1-500）")
    ] = 10

    offset: Annotated[int, Field(ge=0, description="查询偏移量，用于分页")] = 0
