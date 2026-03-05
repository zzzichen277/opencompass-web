# OpenCompass Web 开发文档总览

> 最后更新: 2026-03-05

## 项目简介

OpenCompass Web 是一个基于 FastAPI + Vue 3 的评测管理平台，提供评测任务管理、结果展示、模型与数据集管理等功能。

## 技术栈

### 后端
- **框架**: FastAPI
- **数据库**: SQLite + SQLAlchemy (异步 ORM)
- **实时通信**: WebSocket
- **数据验证**: Pydantic

### 前端
- **框架**: Vue 3 + Vite 7 + TypeScript
- **UI 组件库**: NaiveUI
- **状态管理**: Pinia
- **图表库**: ECharts
- **HTTP 客户端**: Axios

## 目录结构

```
opencompass-web/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── api/               # API 路由
│   │   ├── core/              # 核心配置
│   │   ├── models/            # 数据库模型
│   │   ├── schemas/           # Pydantic 模式
│   │   ├── services/          # 业务逻辑
│   │   └── tasks/             # 任务执行器
│   └── main.py                # 应用入口
├── frontend/                   # 前端应用
│   ├── src/
│   │   ├── views/evaluation/  # 评测页面
│   │   ├── components/        # 组件
│   │   ├── service/           # API 服务
│   │   └── store/             # 状态管理
│   └── ...
└── docs/dev/                   # 开发文档
    ├── backend/               # 后端开发文档
    ├── frontend/              # 前端开发文档
    └── fixes/                 # 问题修复文档
```

## 文档索引

| 文档 | 说明 |
|------|------|
| [后端 API 开发](./backend/api-development.md) | API 端点设计与实现 |
| [后端数据库模型](./backend/database-models.md) | 数据库模型设计 |
| [后端 WebSocket](./backend/websocket.md) | WebSocket 实时通信 |
| [前端页面开发](./frontend/pages-development.md) | 评测页面开发 |
| [前端组件开发](./frontend/components-development.md) | 图表组件开发 |
| [前端 API 对接](./frontend/api-integration.md) | API 服务对接 |
| [问题修复记录](./fixes/bug-fixes.md) | 开发过程中的问题修复 |

## 快速启动

### 后端

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8001
```

### 前端

```bash
cd frontend
pnpm install
pnpm dev
```

### 默认账户

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | R_SUPER (超级管理员) |
| user | user123 | R_USER (普通用户) |

## API 端点

| 模块 | 路径 | 说明 |
|------|------|------|
| Auth | `/api/v1/auth/*` | 用户认证 |
| Models | `/api/v1/models/*` | 模型管理 |
| Datasets | `/api/v1/datasets/*` | 数据集管理 |
| Tasks | `/api/v1/tasks/*` | 评测任务 |
| Results | `/api/v1/results/*` | 评测结果 |
| Templates | `/api/v1/templates/*` | 任务模板 |
| WebSocket | `/api/v1/ws` | 实时通信 |

---

## 变更记录

| 日期 | 变更内容 |
|------|----------|
| 2026-03-05 | 初始化开发文档 |