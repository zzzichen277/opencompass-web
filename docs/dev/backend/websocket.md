# WebSocket 实时通信文档

> 最后更新: 2026-03-05

## 概述

WebSocket 用于实时推送任务进度和日志信息。

## 连接管理

```python
# app/core/websocket.py
from fastapi import WebSocket
from typing import Dict, Set
import json

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, task_id: str = None):
        await websocket.accept()
        if task_id:
            if task_id not in self.active_connections:
                self.active_connections[task_id] = set()
            self.active_connections[task_id].add(websocket)

    def disconnect(self, websocket: WebSocket, task_id: str = None):
        if task_id and task_id in self.active_connections:
            self.active_connections[task_id].discard(websocket)

    async def send_progress(self, task_id: str, progress: float, **kwargs):
        message = {
            "type": "progress",
            "taskId": task_id,
            "progress": progress,
            **kwargs
        }
        await self._broadcast(task_id, message)

    async def send_log(self, task_id: str, level: str, message: str):
        msg = {
            "type": "log",
            "taskId": task_id,
            "level": level,
            "message": message
        }
        await self._broadcast(task_id, msg)

    async def _broadcast(self, task_id: str, message: dict):
        if task_id in self.active_connections:
            dead_connections = set()
            for connection in self.active_connections[task_id]:
                try:
                    await connection.send_json(message)
                except:
                    dead_connections.add(connection)
            self.active_connections[task_id] -= dead_connections

ws_manager = WebSocketManager()
```

## WebSocket 端点

```python
# app/api/endpoints/websocket.py
from fastapi import APIRouter, WebSocket, Query

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    taskId: str = Query(None)
):
    await ws_manager.connect(websocket, taskId)
    try:
        while True:
            data = await websocket.receive_text()
            # 处理客户端消息（心跳等）
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, taskId)
```

## 消息格式

### 进度更新

```json
{
  "type": "progress",
  "taskId": "task-uuid",
  "progress": 50.5,
  "message": "正在评测 MMLU 数据集...",
  "currentDataset": "MMLU",
  "totalDatasets": 5
}
```

### 日志消息

```json
{
  "type": "log",
  "taskId": "task-uuid",
  "level": "info",
  "message": "评测完成",
  "timestamp": "2026-03-05T10:30:00Z"
}
```

### 状态变更

```json
{
  "type": "status",
  "taskId": "task-uuid",
  "status": "completed",
  "message": "任务执行完成"
}
```

## 与任务执行器集成

```python
# main.py - 应用启动时注册回调
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    # 注册 WebSocket 回调
    task_executor.register_progress_callback(
        lambda task_id, progress, **kwargs: ws_manager.send_progress(task_id, progress, **kwargs)
    )
    task_executor.register_log_callback(
        lambda task_id, level, message: ws_manager.send_log(task_id, level, message)
    )

    yield
    await close_db()
```

---

## 变更记录

| 日期 | 变更内容 |
|------|----------|
| 2026-03-05 | 初始化 WebSocket 文档 |