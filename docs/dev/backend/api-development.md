# 后端 API 开发文档

> 最后更新: 2026-03-05

## 概述

后端采用 FastAPI 框架，提供 RESTful API 和 WebSocket 实时通信。

## 目录结构

```
backend/
├── main.py                    # 应用入口
├── app/
│   ├── api/
│   │   ├── __init__.py       # 路由注册
│   │   └── endpoints/        # API 端点
│   │       ├── auth.py       # 认证接口
│   │       ├── models.py     # 模型管理
│   │       ├── datasets.py   # 数据集管理
│   │       ├── tasks.py      # 任务管理
│   │       ├── results.py    # 结果查询
│   │       ├── templates.py  # 模板管理
│   │       └── websocket.py  # WebSocket
│   ├── core/
│   │   ├── config.py         # 配置管理
│   │   ├── database.py       # 数据库连接
│   │   └── websocket.py      # WebSocket 管理器
│   ├── models/               # SQLAlchemy 模型
│   ├── schemas/              # Pydantic 模式
│   └── services/             # 业务逻辑层
```

## API 端点列表

### 1. 认证接口 (auth.py)

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/auth/login` | 用户登录 |
| GET | `/auth/getUserInfo` | 获取用户信息 |
| POST | `/auth/refreshToken` | 刷新令牌 |

**登录请求示例：**
```json
{
  "userName": "admin",
  "password": "admin123"
}
```

**登录响应示例：**
```json
{
  "token": "uuid-token-string",
  "refreshToken": "uuid-refresh-token-string"
}
```

**默认用户：**
- admin / admin123 (R_SUPER 角色)
- user / user123 (R_USER 角色)

### 2. 模型管理 (models.py)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/models` | 获取模型列表 |
| POST | `/models` | 创建模型 |
| GET | `/models/{model_id}` | 获取模型详情 |
| PUT | `/models/{model_id}` | 更新模型 |
| DELETE | `/models/{model_id}` | 删除模型 |

### 3. 数据集管理 (datasets.py)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/datasets` | 获取数据集列表 |
| GET | `/datasets/builtin` | 获取内置数据集 |
| POST | `/datasets/upload` | 上传数据集 |
| GET | `/datasets/{dataset_id}` | 获取数据集详情 |
| DELETE | `/datasets/{dataset_id}` | 删除数据集 |

### 4. 任务管理 (tasks.py)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/tasks` | 获取任务列表 |
| POST | `/tasks` | 创建任务 |
| GET | `/tasks/{task_id}` | 获取任务详情 |
| PUT | `/tasks/{task_id}` | 更新任务 |
| DELETE | `/tasks/{task_id}` | 删除任务 |
| POST | `/tasks/{task_id}/start` | 启动任务 |
| POST | `/tasks/{task_id}/stop` | 停止任务 |
| GET | `/tasks/{task_id}/logs` | 获取任务日志 |

### 5. 结果查询 (results.py)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/results/task/{task_id}` | 获取任务结果 |
| GET | `/results/leaderboard` | 获取排行榜 |
| GET | `/results/{result_id}` | 获取结果详情 |
| GET | `/results/{result_id}/details` | 获取结果详情 |
| GET | `/results/task/{task_id}/export` | 导出结果 |

### 6. 模板管理 (templates.py)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/templates` | 获取模板列表 |
| POST | `/templates` | 创建模板 |
| GET | `/templates/{template_id}` | 获取模板详情 |
| PUT | `/templates/{template_id}` | 更新模板 |
| DELETE | `/templates/{template_id}` | 删除模板 |

### 7. WebSocket (websocket.py)

**连接地址：** `ws://127.0.0.1:8001/api/v1/ws`

**消息类型：**
```json
// 进度更新
{
  "type": "progress",
  "taskId": "task-uuid",
  "progress": 50,
  "message": "正在评测..."
}

// 日志消息
{
  "type": "log",
  "taskId": "task-uuid",
  "level": "info",
  "message": "评测完成"
}
```

## 路由注册

```python
# app/api/__init__.py
from fastapi import APIRouter
from app.api.endpoints import auth, models, datasets, tasks, results, templates, websocket

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(models.router, prefix="/models", tags=["Models"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["Datasets"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(results.router, prefix="/results", tags=["Results"])
api_router.include_router(templates.router, prefix="/templates", tags=["Templates"])
api_router.include_router(websocket.router, tags=["WebSocket"])
```

## 配置管理

```python
# app/core/config.py
class Settings(BaseSettings):
    APP_NAME: str = "OpenCompass Web Backend"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = ["http://localhost:9527", "http://127.0.0.1:9527"]
    DATABASE_URL: str = "sqlite+aiosqlite:///./opencompass_web.db"
```

---

## 变更记录

| 日期 | 变更内容 |
|------|----------|
| 2026-03-05 | 初始化 API 开发文档 |