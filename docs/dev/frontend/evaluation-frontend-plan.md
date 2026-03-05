# OpenCompass 评测前端开发规划

> 创建时间: 2026-03-05
> 最后更新: 2026-03-05
> 状态: **Phase 2 进行中**

## 一、项目概述

### 1.1 项目目标

基于 OpenCompass 大模型评测框架，开发一套完整的 Web 可视化评测平台，复用现有 `frontend/` 前端项目，新建 FastAPI 后端服务，实现评测任务的创建、执行、监控和结果分析的全流程管理。

### 1.2 技术选型

| 层级 | 技术方案 | 版本要求 |
|------|----------|----------|
| 前端框架 | Vue 3 + Vite 7 + TypeScript | 复用现有 |
| UI 组件库 | NaiveUI | 复用现有 |
| 状态管理 | Pinia | 复用现有 |
| 后端框架 | FastAPI | Python 3.10+ |
| 数据库 | SQLite | 轻量级 |
| 实时通信 | WebSocket | FastAPI 内置 |
| 评测引擎 | OpenCompass | 主项目 |

### 1.3 项目结构

```
opencompass-web/
├── opencompass/          # 原评测框架（Python）
├── frontend/             # 前端项目（Vue3 + NaiveUI）
│   ├── src/
│   │   ├── views/
│   │   │   ├── evaluation/    # 新增：评测管理页面
│   │   │   ├── models/        # 新增：模型管理页面
│   │   │   ├── datasets/      # 新增：数据集管理页面
│   │   │   └── results/       # 新增：结果分析页面
│   │   └── service/api/       # 修改：对接新后端 API
│   └── ...
├── backend/              # 新增：后端服务目录
│   ├── app/
│   │   ├── api/              # API 路由
│   │   ├── core/             # 核心配置
│   │   ├── models/           # 数据模型
│   │   ├── services/         # 业务逻辑
│   │   └── tasks/            # 后台任务
│   ├── main.py               # 入口文件
│   └── requirements.txt
└── docs/                 # 文档
```

---

## 二、功能模块设计

### 2.1 模块总览

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenCompass Web Platform                 │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ 任务管理 │  │ 结果展示 │  │模型/数据集│  │ 历史记录 │        │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘        │
│       │           │            │            │              │
│  ┌────┴───────────┴────────────┴────────────┴────┐         │
│  │              后端 API 服务 (FastAPI)           │         │
│  └───────────────────────┬───────────────────────┘         │
│                          │                                  │
│  ┌───────────────────────┴───────────────────────┐         │
│  │           OpenCompass 评测引擎 (Python)         │         │
│  └───────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 任务管理模块

**核心功能**：
- 创建评测任务（选择模型、数据集、配置参数）
- 任务模板管理（保存常用配置）
- 任务执行控制（启动、暂停、停止、重试）
- 实时进度监控（WebSocket 推送）

**页面设计**：

| 页面 | 功能 | 优先级 |
|------|------|--------|
| 任务列表 | 展示所有任务，支持筛选、搜索、排序 | P0 |
| 创建任务 | 向导式任务配置，分步引导 | P0 |
| 任务详情 | 任务配置信息、执行状态、实时日志 | P0 |
| 模板管理 | 创建、编辑、删除任务模板 | P1 |

**任务配置项**：

```typescript
interface EvaluationTask {
  id: string;
  name: string;
  description?: string;
  models: ModelConfig[];          // 支持多模型
  datasets: DatasetConfig[];      // 支持多数据集
  accelerator: 'huggingface' | 'vllm' | 'lmdeploy';
  resources: {
    gpuCount: number;
    maxNumWorker: number;
    batchSize?: number;
  };
  evalConfig: {
    mode: 'gen' | 'ppl';
    maxOutLen?: number;
    batch_size?: number;
  };
  schedule: 'now' | 'later';
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
  createdAt: Date;
  updatedAt: Date;
}
```

### 2.3 结果展示模块

**核心功能**：
- 评测结果概览（总分、各维度得分）
- 排行榜对比（多模型横向对比）
- 详细日志查看（逐题分析）
- 图表可视化（雷达图、柱状图、折线图）
- 报告导出（PDF、Excel）

**页面设计**：

| 页面 | 功能 | 优先级 |
|------|------|--------|
| 结果概览 | 任务汇总、关键指标展示 | P0 |
| 排行榜 | 模型排名、数据集对比 | P0 |
| 详细结果 | 逐题答案、评分详情 | P0 |
| 可视化图表 | ECharts 图表展示 | P1 |
| 报告中心 | 生成、下载、管理报告 | P1 |

**结果数据结构**：

```typescript
interface EvaluationResult {
  taskId: string;
  modelId: string;
  datasetId: string;
  overallScore: number;
  metrics: Record<string, number>;
  details: {
    question: string;
    answer: string;
    prediction: string;
    score: number;
    reasoning?: string;
  }[];
  summary: {
    correct: number;
    total: number;
    accuracy: number;
  };
  completedAt: Date;
}
```

### 2.4 模型/数据集管理模块

**核心功能**：
- 模型列表管理（添加、编辑、删除）
- 数据集管理（内置数据集 + 自定义上传）
- 评测指标配置
- 资源配置模板

**页面设计**：

| 页面 | 功能 | 优先级 |
|------|------|--------|
| 模型列表 | 展示可用模型，支持搜索、筛选 | P0 |
| 添加模型 | 配置模型路径、推理参数 | P0 |
| 数据集列表 | 展示内置和自定义数据集 | P0 |
| 数据集详情 | 数据集信息、样例预览 | P1 |
| 上传数据集 | 自定义数据集上传 | P1 |

**模型配置结构**：

```typescript
interface ModelConfig {
  id: string;
  name: string;
  type: 'huggingface' | 'api' | 'custom';
  path?: string;                  // HuggingFace 模型路径
  apiConfig?: {
    baseUrl: string;
    apiKey: string;
    modelName: string;
  };
  parameters: {
    maxLength: number;
    temperature?: number;
    topP?: number;
  };
  tags: string[];
  createdAt: Date;
}
```

**数据集配置结构**：

```typescript
interface DatasetConfig {
  id: string;
  name: string;
  type: 'builtin' | 'custom';
  category: 'qa' | 'math' | 'code' | 'subjective' | 'reasoning';
  description: string;
  configPath?: string;            // OpenCompass 配置路径
  customData?: {
    format: 'json' | 'csv';
    path: string;
  };
  metrics: string[];
  sampleCount: number;
  tags: string[];
}
```

### 2.5 历史记录模块

**核心功能**：
- 历史评测记录查询
- 多任务对比分析
- 结果导出
- 收藏与标签

**页面设计**：

| 页面 | 功能 | 优先级 |
|------|------|--------|
| 历史记录 | 所有已完成任务列表 | P0 |
| 对比分析 | 选择多个任务进行对比 | P1 |
| 收藏夹 | 常用任务快速访问 | P2 |

---

## 三、后端 API 设计

### 3.1 API 概览

**基础路径**: `/api/v1`

| 模块 | 路径 | 说明 |
|------|------|------|
| 任务管理 | `/tasks` | 评测任务 CRUD |
| 模型管理 | `/models` | 模型配置管理 |
| 数据集管理 | `/datasets` | 数据集管理 |
| 结果查询 | `/results` | 评测结果查询 |
| 报告生成 | `/reports` | 报告生成与下载 |
| 系统配置 | `/system` | 系统设置 |
| WebSocket | `/ws` | 实时通信 |

### 3.2 核心 API 定义

#### 任务管理 API

```yaml
# 创建评测任务
POST /api/v1/tasks
Request:
  {
    "name": "string",
    "models": ["model_id_1", "model_id_2"],
    "datasets": ["dataset_id_1", "dataset_id_2"],
    "accelerator": "vllm",
    "resources": { "gpuCount": 4, "maxNumWorker": 2 },
    "evalConfig": { "mode": "gen", "maxOutLen": 2048 }
  }
Response:
  { "taskId": "uuid", "status": "pending" }

# 获取任务列表
GET /api/v1/tasks?page=1&size=20&status=running

# 获取任务详情
GET /api/v1/tasks/{taskId}

# 启动任务
POST /api/v1/tasks/{taskId}/start

# 停止任务
POST /api/v1/tasks/{taskId}/stop

# 获取任务日志
GET /api/v1/tasks/{taskId}/logs?offset=0&limit=100
```

#### 模型管理 API

```yaml
# 获取模型列表
GET /api/v1/models

# 添加模型
POST /api/v1/models
Request:
  {
    "name": "Qwen2.5-72B-Instruct",
    "type": "huggingface",
    "path": "Qwen/Qwen2.5-72B-Instruct",
    "parameters": { "maxLength": 8192 }
  }

# 更新模型
PUT /api/v1/models/{modelId}

# 删除模型
DELETE /api/v1/models/{modelId}
```

#### 数据集管理 API

```yaml
# 获取数据集列表
GET /api/v1/datasets?category=math&type=builtin

# 获取内置数据集（从 OpenCompass 配置加载）
GET /api/v1/datasets/builtin

# 上传自定义数据集
POST /api/v1/datasets/upload
Content-Type: multipart/form-data

# 获取数据集详情
GET /api/v1/datasets/{datasetId}
```

#### 结果查询 API

```yaml
# 获取任务结果
GET /api/v1/results/{taskId}

# 获取排行榜
GET /api/v1/results/leaderboard?dataset=mmlu

# 获取详细结果
GET /api/v1/results/{taskId}/details?page=1&size=50

# 导出结果
GET /api/v1/results/{taskId}/export?format=excel
```

### 3.3 WebSocket 协议

```typescript
// 客户端订阅任务进度
{
  "type": "subscribe",
  "taskId": "uuid"
}

// 服务端推送进度
{
  "type": "progress",
  "taskId": "uuid",
  "data": {
    "status": "running",
    "progress": 45.5,
    "currentDataset": "mmlu",
    "completedSamples": 455,
    "totalSamples": 1000,
    "eta": "00:15:30"
  }
}

// 服务端推送日志
{
  "type": "log",
  "taskId": "uuid",
  "data": {
    "timestamp": "2026-03-05T10:30:00Z",
    "level": "info",
    "message": "Evaluating sample 455/1000..."
  }
}

// 任务完成通知
{
  "type": "completed",
  "taskId": "uuid",
  "data": {
    "status": "completed",
    "results": { "overallScore": 85.5 }
  }
}
```

---

## 四、数据库设计

### 4.1 数据库架构（SQLite）

```sql
-- 模型表
CREATE TABLE models (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,  -- huggingface, api, custom
    path TEXT,
    api_config TEXT,     -- JSON
    parameters TEXT,     -- JSON
    tags TEXT,           -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 数据集表
CREATE TABLE datasets (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,  -- builtin, custom
    category TEXT,       -- qa, math, code, subjective, reasoning
    description TEXT,
    config_path TEXT,
    custom_data TEXT,    -- JSON
    metrics TEXT,        -- JSON array
    sample_count INTEGER,
    tags TEXT,           -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 评测任务表
CREATE TABLE evaluation_tasks (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    config TEXT,         -- JSON (models, datasets, resources, etc.)
    status TEXT DEFAULT 'pending',
    progress REAL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT
);

-- 评测结果表
CREATE TABLE evaluation_results (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    model_id TEXT NOT NULL,
    dataset_id TEXT NOT NULL,
    overall_score REAL,
    metrics TEXT,        -- JSON
    summary TEXT,        -- JSON
    details_path TEXT,   -- JSON 文件路径
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES evaluation_tasks(id),
    FOREIGN KEY (model_id) REFERENCES models(id),
    FOREIGN KEY (dataset_id) REFERENCES datasets(id)
);

-- 任务模板表
CREATE TABLE task_templates (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    config TEXT,         -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 评测日志表
CREATE TABLE evaluation_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    level TEXT,
    message TEXT,
    FOREIGN KEY (task_id) REFERENCES evaluation_tasks(id)
);

-- 系统配置表
CREATE TABLE system_config (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 五、开发计划

### 5.1 阶段划分

```
Phase 1: 基础框架搭建 (Week 1-2)
├── 后端项目初始化
├── 数据库设计与 ORM 配置
├── 基础 API 框架
└── 前端路由与布局调整

Phase 2: 核心功能开发 (Week 3-5)
├── 模型管理模块
├── 数据集管理模块
├── 任务创建与配置
└── 任务执行与监控

Phase 3: 结果展示开发 (Week 6-7)
├── 结果数据存储
├── 结果查询 API
├── 前端结果展示页面
└── 图表可视化

Phase 4: 高级功能开发 (Week 8-9)
├── 排行榜对比
├── 报告生成与导出
├── 任务模板管理
└── 历史记录与对比

Phase 5: 测试与优化 (Week 10)
├── 集成测试
├── 性能优化
├── 用户体验优化
└── 文档完善
```

### 5.2 详细任务清单

#### Phase 1: 基础框架搭建

| 任务 | 前置依赖 | 预估工时 | 负责模块 |
|------|----------|----------|----------|
| 创建 backend 目录结构 | 无 | 2h | 后端 |
| 配置 FastAPI 应用 | 目录结构 | 2h | 后端 |
| 配置 SQLAlchemy ORM | FastAPI | 3h | 后端 |
| 创建数据库模型 | ORM | 4h | 后端 |
| 实现基础 CRUD 操作 | 数据库模型 | 4h | 后端 |
| 前端路由配置调整 | 无 | 2h | 前端 |
| 前端布局调整 | 路由 | 3h | 前端 |
| API 服务封装 | 无 | 3h | 前端 |

#### Phase 2: 核心功能开发

| 任务 | 前置依赖 | 预估工时 | 负责模块 |
|------|----------|----------|----------|
| 模型管理 API | Phase 1 | 4h | 后端 |
| 数据集管理 API | Phase 1 | 4h | 后端 |
| 内置数据集加载器 | 数据集 API | 6h | 后端 |
| 任务创建 API | 模型/数据集 API | 4h | 后端 |
| OpenCompass 任务执行器 | 任务 API | 8h | 后端 |
| WebSocket 进度推送 | 任务执行器 | 4h | 后端 |
| 模型管理页面 | 模型 API | 6h | 前端 |
| 数据集管理页面 | 数据集 API | 6h | 前端 |
| 任务创建页面 | 任务 API | 8h | 前端 |
| 任务列表与详情页 | 任务 API | 6h | 前端 |

#### Phase 3: 结果展示开发

| 任务 | 前置依赖 | 预估工时 | 负责模块 |
|------|----------|----------|----------|
| 结果数据解析与存储 | Phase 2 | 6h | 后端 |
| 结果查询 API | 结果存储 | 4h | 后端 |
| 详细结果分页查询 | 结果 API | 3h | 后端 |
| 结果概览页面 | 结果 API | 6h | 前端 |
| 详细结果页面 | 结果 API | 6h | 前端 |
| ECharts 图表集成 | 结果 API | 4h | 前端 |

#### Phase 4: 高级功能开发

| 任务 | 前置依赖 | 预估工时 | 负责模块 |
|------|----------|----------|----------|
| 排行榜 API | Phase 3 | 4h | 后端 |
| 报告生成服务 | 结果 API | 6h | 后端 |
| PDF/Excel 导出 | 报告服务 | 4h | 后端 |
| 任务模板 API | Phase 2 | 3h | 后端 |
| 排行榜页面 | 排行榜 API | 4h | 前端 |
| 报告中心页面 | 报告 API | 4h | 前端 |
| 任务模板页面 | 模板 API | 4h | 前端 |
| 历史记录页面 | 结果 API | 3h | 前端 |

#### Phase 5: 测试与优化

| 任务 | 前置依赖 | 预估工时 | 负责模块 |
|------|----------|----------|----------|
| 后端单元测试 | Phase 4 | 6h | 后端 |
| 前端组件测试 | Phase 4 | 6h | 前端 |
| 集成测试 | 单元测试 | 4h | 全栈 |
| 性能优化 | 集成测试 | 4h | 全栈 |
| 文档编写 | 测试完成 | 4h | 全栈 |

### 5.3 总工时估算

| 阶段 | 后端工时 | 前端工时 | 总计 |
|------|----------|----------|------|
| Phase 1 | 15h | 8h | 23h |
| Phase 2 | 30h | 26h | 56h |
| Phase 3 | 13h | 16h | 29h |
| Phase 4 | 17h | 15h | 32h |
| Phase 5 | 10h | 10h | 20h |
| **总计** | **85h** | **75h** | **160h** |

---

## 六、风险与应对

### 6.1 技术风险

| 风险 | 影响 | 概率 | 应对措施 |
|------|------|------|----------|
| OpenCompass API 变动 | 高 | 中 | 封装适配层，隔离变化 |
| 大规模评测任务性能 | 高 | 中 | 任务队列 + 进度分片 |
| WebSocket 连接稳定性 | 中 | 低 | 心跳检测 + 自动重连 |
| SQLite 并发限制 | 中 | 低 | 写入队列 + 批量提交 |

### 6.2 项目风险

| 风险 | 影响 | 概率 | 应对措施 |
|------|------|------|----------|
| 需求变更 | 高 | 中 | 模块化设计，灵活扩展 |
| 开发周期延期 | 中 | 中 | 分阶段交付，核心优先 |
| 跨模块集成问题 | 高 | 低 | 接口先行，持续集成 |

---

## 七、验收标准

### 7.1 功能验收

- [ ] 能够创建、启动、停止评测任务
- [ ] 能够实时查看任务进度和日志
- [ ] 能够管理模型和数据集
- [ ] 能够查看评测结果和排行榜
- [ ] 能够生成和导出报告

### 7.2 性能验收

- [ ] 页面加载时间 < 2s
- [ ] API 响应时间 < 500ms
- [ ] 支持 10+ 并发评测任务
- [ ] WebSocket 连接稳定，延迟 < 1s

### 7.3 用户体验验收

- [ ] 操作流程直观，无需培训
- [ ] 错误提示清晰明确
- [ ] 支持中英文界面
- [ ] 响应式布局，支持不同屏幕尺寸

---

## 八、附录

### 8.1 OpenCompass 支持的主要数据集分类

| 类别 | 数据集示例 | 评测能力 |
|------|------------|----------|
| 通用知识 | MMLU, C-Eval, CMMLU | 知识问答 |
| 数学推理 | GSM8K, MATH, AIME | 数学能力 |
| 代码能力 | HumanEval, MBPP | 编程能力 |
| 长文本 | NeedleBench, RULER | 长上下文理解 |
| 推理能力 | BBH, MuSR | 复杂推理 |
| 主观评测 | CompassArena | 主观评价 |
| Agent能力 | ToolBench | 工具调用 |

### 8.2 参考资源

- [OpenCompass 文档](https://opencompass.readthedocs.io/)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [NaiveUI 组件库](https://www.naiveui.com/)
- [Vue 3 文档](https://vuejs.org/)

---

**文档版本**: v1.0
**最后更新**: 2026-03-05