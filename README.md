# 今天吃什么（What to Eat）：FastAPI 实战项目演示计划

## 项目概述

本项目旨在构建一个以 **“今天吃什么”（What to Eat）** 为主题的完整 FastAPI 实战示例，覆盖从基础 CRUD 到本地 AI 模型接入的完整开发路径。

项目起点从最基础的数据库表设计与增删改查演示出发，逐步扩展出用户认证、收藏系统、外部天气接口调用、AI 菜品推荐等核心模块。使用模块化与可插拔式架构设计。

## 🧱 技术栈（Tech Stack）

- **语言与框架**：Python 3.13.8 · FastAPI
    
- **数据库与 ORM**：SQLAlchemy 2.0（异步） · Alembic
    
- **认证系统**：FastAPI Users
    
- **缓存服务**：Redis   
    
- **HTTP 客户端**：httpx.AsyncClient（用于天气 API）
    
- **AI 模型调用**：Ollama（如 qwen3:8b）
    
- **包与环境管理**：uv
    
- **容器化支持**：Docker · Docker Compose
    
- **架构设计**：Repository → Service → Router 分层结构




## 🧭 一、项目总体目标

构建一个从最基础 CRUD 演示逐步扩展到：

> **具备用户登录、收藏功能、天气查询与 AI 推荐“今天吃什么”** 的完整 FastAPI 实战练习项目。

整体采用模块化设计，方便后续的数据库迁移、用户认证、外部 API 调用与 AI 推理。

---

## 🧩 二、阶段规划概览

| 阶段            | 名称        | 核心目标                                             | 关键技术点                        |
| ------------- | --------- | ------------------------------------------------ | ---------------------------- |
| **阶段 1**      | CRUD 基础   | 纯 FastAPI + SQLAlchemy 2.0 实现 Dish 增删改查          | 模型定义、路由、Pydantic schema、依赖注入 |
| **阶段 2**      | 用户认证      | 引入 FastAPI Users + Redis Token Strategy 实现用户登录注册 | JWT 认证、依赖保护路由                |
| **阶段 3**      | 收藏系统      | 新建 Collection 表，建立用户与 Dish 关联                    | 外键关系、联表查询、当前用户操作             |
| **阶段 4**      | 外部 API 集成 | 接入公开天气 API （如 Open-Weather ）                     | `httpx.AsyncClient` 调用与缓存    |
| **阶段 5**      | AI 推荐扩展   | 本地 Ollama 模型综合天气 + 收藏记录输出推荐                      | 推理调用、本地模型管理 (OpenLLM/Ollama) |
| **阶段 6 (可选)** | 异步任务 + 通知 | TaskIQ  + RabbitMQ 做定时天气更新或推荐推送                  | 后台任务、消息队列、WebSocket 通知       |

---

## 🏗️ 三、数据模型设计

### 1️⃣ 公共菜品 `Dish`

```python
class Dish(Base):
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    # 后期须补充唯一字段
```

> 公共表，无 user_id，后续 CRUD 演示的核心。

---

### 2️⃣ 用户表 `User`

由 FastAPI Users 自动生成，可含：

- `id` (UUID)
    
- `email`、`hashed_password`
    
- `is_active`、`is_verified`
    

---

### 3️⃣ 收藏表 `Collection`

```python
class Collection(Base):
    __tablename__ = "collections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    dish_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("dishes.id"), nullable=False
    )
    note: Mapped[str | None] = mapped_column(Text)

    # 单向导航，不级联、不删除孤儿
    dish: Mapped["Dish"] = relationship()
    __table_args__ = (
        UniqueConstraint("user_id", "dish_id")
    )
    # 后期需补充唯一约束，相同项仅可收藏一次
```

> 用于保存用户收藏的菜品；支持备注或打分。

### 4️⃣ （可选）天气日志 `WeatherLog`

```python
class WeatherLog(Base):
    __tablename__ = "weather_logs"

    id = Column(Integer, primary_key=True)
    city = Column(String(50))
    date = Column(Date, default=date.today)
    temperature = Column(Float)
    condition = Column(String(50))
```

> 后续 AI 推荐模块可读取最近天气数据。
---

## ⚙️ 四、阶段性开发细节

### 🌱 阶段 1：CRUD 演示

- 创建 `Dish` 模型与 Pydantic schema；
    
- 编写 `GET /dishes`、`POST /dishes`、`PATCH /dishes/{id}`、`DELETE /dishes/{id}`；
    
- 演示：
    
    - SQLAlchemy 2.0 声明式映射；
        
    - 依赖注入 `AsyncSession`；
        
    - 路由分层（router/service/repository）；
        
    - Alembic 初始化与迁移。
        

🎯 演示重点：**CRUD 核心逻辑**、模型 → schema → 路由 → 数据库 完整链路。

---

### 🔐 阶段 2：用户系统接入

- 安装并配置 FastAPI Users；
    
- 使用 RedisStrategy 或 DatabaseStrategy；
    
- 创建用户注册、登录接口；
    
- 保护 `Collection` 相关路由。

- 简易RBAC 管理员及普通用户。仅管理员可删除公共数据。
    

🎯 演示重点：**依赖注入 `current_user`** 与 路由保护。

---

### 📚 阶段 3：收藏系统

- 新建 `Collection` 表；
    
- 实现：
    
    - `POST /collections/` → 收藏菜品；
        
    - `GET /collections/me` → 查看我的收藏；
        
    - `DELETE /collections/{id}` → 取消收藏；
        
- Join 查询 `Collection → Dish` 返回详细信息。
    

🎯 演示重点：**多表关系、用户上下文、业务分层设计**。

---

### ☁️ 阶段 4：外部 API 集成

	- 选用免费天气 API （如 Open-Weather）；
    
- 封装 `WeatherService` 模块：
    
    ```python
    async def get_weather(city: str) -> dict:
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://api.openweathermap.org/data/2.5", params={...})
            return resp.json()
    ```
    
- 可选：缓存结果到 Redis。
    

🎯 演示重点：**异步 HTTP 请求、第三方 API 集成、缓存**。

---

### 🤖 阶段 5：AI 推荐扩展

- 调用 Ollama 本地模型 (`deepseek-r1:7b`)；
    
- 读取：
    
    - 当前天气 信息；
        
    - 用户收藏历史；
        
- 生成文本推荐：
    
    ```python
    prompt = f"根据今天{city}的天气（{condition} {temperature}℃），从以下收藏菜中推荐适合的三道菜：{dish_list}"
    ```
    
- 响应 → FastAPI 路由 `/recommendations`
    

🎯 演示重点：**FastAPI 中的本地 LLM 调用**。

---

### ⏰ 阶段 6（可选）：异步任务与通知

- 使用 TaskIQ  + RabbitMQ；
    
- 实现定时任务更新天气 → 插入 `WeatherLog`；
    
- 或推送推荐消息到 WebSocket 端点。
    

🎯 演示重点：**后台任务与消息驱动架构**。

---


下面给出一份“即拿即用”的目录说明 + 最小代码骨架，帮你把 6 个子模块（users / dish / weather / ai / tasks / ws）真正“跑”起来。  
所有子包都遵循同一套套路：  
`router.py` → 写路由  
`schemas.py` → 写 Pydantic 模型  
`service.py` → 写业务/ORM 调用  
`__init__.py` → 暴露 router  
然后在 `main.py` 里 `include_router` 即可。

----------------------------------------

# 项目结构计划

```plain
src/
├── core/                 # 全局基础设施
│   ├── __init__.py
│   ├── config.py        # 单例 Settings
│   ├── db.py            # SQLAlchemy 引擎/会话
│   └── deps.py          # 共享依赖（get_db、get_current_user 等）
├── users/
├── dish/                # 菜品管理
│   ├── __init__.py      
│   ├── router.py        # 暴露 router
│   ├── schemas.py
│   ├── models.py        # SQLAlchemy User 表
│   ├── repository.py
│   └── service.py
├── collections/         # 收藏模块
├── weather/             # 天气查询
├── ai/                  # 调用大模型
├── tasks/               # Celery 异步任务
└── ws/                  # WebSocket 通知
└──  main.py              # FastAPI 实例 + 挂载路由
```

----------------------------------------

