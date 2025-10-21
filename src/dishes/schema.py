from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field

# 公共字段基类
class DishBase(BaseModel):
    name: Annotated[str, Field(..., max_length=255, description="菜品名称")]
    description: Annotated[str | None, Field(None, description="菜品描述")]

# 创建模型
class DishCreate(DishBase):
    """用于创建菜品"""
    pass

# 更新模型（全部可选）
class DishUpdate(BaseModel):
    name: Annotated[str | None, Field(None, max_length=255, description="菜品名称")]
    description: Annotated[str | None, Field(None, description="菜品描述")]
    

# 响应模型（含时间戳）
class DishResponse(DishBase):
    id: int
    created_at: datetime
    

    model_config = {
        "from_attributes": True
    }