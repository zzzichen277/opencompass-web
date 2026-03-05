# OpenCompass Web Backend

基于 FastAPI 的 OpenCompass 评测平台后端服务。

## 技术栈

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite
- WebSocket

## 目录结构

```
backend/
├── app/
│   ├── api/           # API 路由
│   ├── core/          # 核心配置
│   ├── models/        # 数据库模型
│   ├── schemas/       # Pydantic 模型
│   ├── services/      # 业务逻辑
│   └── tasks/         # 后台任务
├── main.py            # 应用入口
└── requirements.txt   # 依赖
```

## 开发

```bash
# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn main:app --reload --port 8000
```