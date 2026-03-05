# 后端数据库模型文档

> 最后更新: 2026-03-05

## 概述

使用 SQLAlchemy 异步 ORM，基于 SQLite 数据库。

## 模型列表

### 1. Model (模型)

```python
# app/models/model.py
class Model(Base):
    __tablename__ = "models"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, comment="模型名称")
    path = Column(String, nullable=False, comment="模型路径")
    type = Column(String, nullable=False, comment="模型类型: huggingface, api, custom")
    config = Column(JSON, default={}, comment="模型配置")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### 2. Dataset (数据集)

```python
# app/models/dataset.py
class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, comment="数据集名称")
    type = Column(String, nullable=False, comment="类型: builtin, custom")
    path = Column(String, comment="数据集路径")
    config = Column(JSON, default={}, comment="数据集配置")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### 3. EvaluationTask (评测任务)

```python
# app/models/task.py
class EvaluationTask(Base):
    __tablename__ = "evaluation_tasks"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, comment="任务名称")
    model_id = Column(String, ForeignKey("models.id"))
    dataset_ids = Column(JSON, default=[], comment="数据集ID列表")
    config = Column(JSON, default={}, comment="评测配置")
    status = Column(String, default="pending", comment="状态: pending, running, completed, failed")
    progress = Column(Float, default=0.0, comment="进度 0-100")
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, comment="开始时间")
    completed_at = Column(DateTime, comment="完成时间")
```

### 4. EvaluationResult (评测结果)

```python
# app/models/result.py
class EvaluationResult(Base):
    __tablename__ = "evaluation_results"

    id = Column(String, primary_key=True)
    task_id = Column(String, ForeignKey("evaluation_tasks.id"))
    dataset_name = Column(String, comment="数据集名称")
    metrics = Column(JSON, default={}, comment="评测指标")
    details = Column(JSON, default={}, comment="详细结果")
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 5. TaskTemplate (任务模板)

```python
# app/models/template.py
class TaskTemplate(Base):
    __tablename__ = "task_templates"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, comment="模板名称")
    description = Column(String, comment="模板描述")
    config = Column(JSON, default={}, comment="模板配置")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### 6. EvaluationLog (评测日志)

```python
# app/models/log.py
class EvaluationLog(Base):
    __tablename__ = "evaluation_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String, ForeignKey("evaluation_tasks.id"))
    level = Column(String, default="info", comment="日志级别")
    message = Column(String, comment="日志内容")
    created_at = Column(DateTime, default=datetime.utcnow)
```

## ER 图

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Model     │────▶│ EvaluationTask  │◀────│   Dataset        │
│             │     │                 │     │                  │
│ id          │     │ id              │     │ id               │
│ name        │     │ name            │     │ name             │
│ path        │     │ model_id (FK)   │     │ type             │
│ type        │     │ dataset_ids     │     │ path             │
│ config      │     │ status          │     │ config           │
└─────────────┘     │ progress        │     └──────────────────┘
                    │ config          │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐     ┌──────────────────┐
                    │EvaluationResult │     │ EvaluationLog    │
                    │                 │     │                  │
                    │ id              │     │ id               │
                    │ task_id (FK)    │     │ task_id (FK)     │
                    │ dataset_name    │     │ level            │
                    │ metrics         │     │ message          │
                    │ details         │     │ created_at       │
                    └─────────────────┘     └──────────────────┘
```

## 数据库初始化

```python
# app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    await engine.dispose()
```

---

## 变更记录

| 日期 | 变更内容 |
|------|----------|
| 2026-03-05 | 初始化数据库模型文档 |