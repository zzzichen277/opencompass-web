# OpenCompass 产品需求文档 (PRD)

## 文档信息

| 属性 | 内容 |
|------|------|
| 产品名称 | OpenCompass（司南） |
| 版本 | v0.5.2 |
| 文档版本 | v1.0 |
| 创建日期 | 2026-03-05 |
| 维护团队 | 上海人工智能实验室 |

---

## 1. 产品概述

### 1.1 产品定位

OpenCompass 是一个**一站式大语言模型评测平台**，旨在为大模型提供公平、开放、可复现的评测基准。作为 OpenCompass 2.0 生态的核心组件，它连接了 CompassKit（工具链）、CompassHub（评测资源中心）和 CompassRank（评测榜单），构建了完整的大模型评测生态系统。

### 1.2 目标用户

| 用户群体 | 使用场景 |
|---------|---------|
| **AI研究人员** | 评估自研模型性能，对比基准模型 |
| **算法工程师** | 模型迭代优化，性能回归测试 |
| **企业开发者** | 商业模型选型，API模型评估 |
| **学术机构** | 模型能力研究，学术论文实验 |
| **开源社区** | 模型贡献评测，社区基准对比 |

### 1.3 核心价值

- **公平性**：标准化评测流程，消除评测偏差
- **开放性**：开源框架，支持自定义模型和数据集
- **可复现性**：完整记录评测过程，确保结果可验证
- **全面性**：覆盖语言、知识、理解、推理、安全五大维度

---

## 2. 功能需求

### 2.1 核心功能模块

#### 2.1.1 模型支持系统

| 功能项 | 优先级 | 描述 |
|--------|--------|------|
| HuggingFace模型加载 | P0 | 支持Transformers格式的开源模型加载 |
| API模型集成 | P0 | 支持OpenAI、Claude、Gemini等商业API |
| 推理加速后端 | P1 | 集成vLLM、LMDeploy、TurboMind |
| 多模态模型 | P2 | 支持视觉语言模型评测 |
| 自定义模型 | P1 | 提供BaseModel接口供用户扩展 |

**模型类型覆盖：**

```
开源模型 → LLaMA、Qwen、InternLM、ChatGLM、Baichuan、Yi等
API模型  → OpenAI、Claude、Gemini、文心一言、通义千问等
加速后端 → vLLM、LMDeploy、TurboMind、LightLLM
```

#### 2.1.2 数据集管理系统

| 功能项 | 优先级 | 描述 |
|--------|--------|------|
| 预置数据集 | P0 | 内置70+标准评测数据集 |
| 数据集加载器 | P0 | 支持HuggingFace Datasets和ModelScope |
| 自定义数据集 | P1 | 提供BaseDataset接口供用户扩展 |
| 数据集配置 | P1 | 支持Python配置文件定义数据集 |

**评测维度覆盖：**

| 维度 | 示例数据集 |
|------|-----------|
| **语言能力** | CLUE、CMMLU、C-Eval |
| **知识能力** | MMLU、TruthfulQA、CommonsenseQA |
| **理解能力** | Reading Comprehension、RACE |
| **推理能力** | GSM8K、MATH、BBH |
| **安全能力** | SafetyBench、HarmfulQA |
| **代码能力** | HumanEval、MBPP |
| **长文本** | LongBench、NeedleInHaystack |

#### 2.1.3 评测引擎系统

| 功能项 | 优先级 | 描述 |
|--------|--------|------|
| 生成式评测 | P0 | 支持GenInferencer进行开放式生成评测 |
| 判别式评测 | P0 | 支持PPLInferencer进行困惑度评测 |
| 对话评测 | P0 | 支持ChatInferencer进行多轮对话评测 |
| Agent评测 | P1 | 支持Agent能力评测 |
| 对抗评测 | P2 | 支持AttackInferencer进行安全评测 |
| CoT评测 | P1 | 支持Chain-of-Thought推理评测 |
| ToT评测 | P2 | 支持Tree of Thoughts评测 |

#### 2.1.4 任务调度系统

| 功能项 | 优先级 | 描述 |
|--------|--------|------|
| 本地执行 | P0 | LocalRunner支持单机多GPU评测 |
| Slurm调度 | P0 | SlurmRunner支持集群分布式评测 |
| DLC调度 | P1 | DLCRunner支持阿里云DLC |
| 任务分区 | P0 | Partitioner智能划分评测任务 |
| 负载均衡 | P1 | 支持基于任务大小的负载均衡 |

#### 2.1.5 结果处理系统

| 功能项 | 优先级 | 描述 |
|--------|--------|------|
| 结果汇总 | P0 | Summarizer自动汇总评测结果 |
| 可视化报告 | P1 | 生成表格、图表形式的结果报告 |
| 结果对比 | P1 | 支持多模型横向对比 |
| 结果持久化 | P1 | 支持结果存储和回溯 |

### 2.2 配置系统

#### 2.2.1 配置架构

基于MMEngine配置系统，采用Python配置文件格式：

```python
# 示例配置结构
from mmengine.config import Config

# 模型配置
models = [
    dict(type='HuggingFace',
         path='meta-llama/Llama-2-7b-hf',
         max_out_len=512)
]

# 数据集配置
datasets = [
    dict(type='MMLUDataset',
         path='cais/mmlu')
]

# 评测配置
eval = dict(
    partitioner=dict(type='NaivePartitioner'),
    runner=dict(type='LocalRunner', max_num_workers=4)
)
```

#### 2.2.2 配置管理需求

| 功能项 | 描述 |
|--------|------|
| 预置配置 | 提供models/、datasets/目录下的标准配置 |
| 配置继承 | 支持配置文件继承和覆盖 |
| 配置验证 | 运行前验证配置有效性 |
| 配置可视化 | 支持配置内容的打印和检查 |

### 2.3 CLI交互系统

#### 2.3.1 命令行接口

```bash
# 基础评测命令
opencompass configs/eval_demo.py

# 主要参数
--max-num-workers     # 最大并行worker数
--work-dir            # 工作目录
--resume              # 恢复中断的评测
--slurm               # 启用Slurm调度
--debug               # 调试模式
```

#### 2.3.2 评测流程阶段

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Infer  │ -> │  Eval   │ -> │  Viz    │ -> │ Report  │
│ (推理)  │    │ (评估)  │    │ (可视化)│    │ (报告)  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

---

## 3. 非功能需求

### 3.1 性能需求

| 指标 | 目标值 |
|------|--------|
| 单GPU推理速度 | 与原生Transformers相当 |
| 分布式加速比 | 8卡并行效率 > 80% |
| 内存占用 | 支持单卡评测7B模型 |
| 数据集加载 | HF Datasets标准加载速度 |

### 3.2 可扩展性需求

| 需求 | 描述 |
|------|------|
| 新模型接入 | 继承BaseModel，实现generate/get_ppl接口 |
| 新数据集接入 | 继承BaseDataset，实现数据加载逻辑 |
| 新评估指标 | 注册到Registry即可使用 |
| 新推理后端 | 实现BaseRunner接口 |

### 3.3 兼容性需求

| 类型 | 支持范围 |
|------|---------|
| Python版本 | Python >= 3.8 |
| PyTorch版本 | torch >= 1.13.1 |
| Transformers版本 | transformers >= 4.29.1 |
| 操作系统 | Linux、macOS、Windows (WSL) |
| CUDA版本 | CUDA 11.x / 12.x |

### 3.4 可维护性需求

- **模块化设计**：核心组件解耦，支持独立更新
- **配置驱动**：行为通过配置控制，代码通用化
- **日志规范**：结构化日志输出，支持调试追踪
- **文档完善**：提供中英文文档、API文档、使用示例

---

## 4. 系统架构

### 4.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                      User Interface                          │
│              (CLI: opencompass / Python API)                 │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Configuration System                       │
│              (MMEngine Config + Registry)                    │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌─────────────────┐    ┌──────────────┐
│   Partitioner │    │     Runner      │    │  Summarizer  │
│  (任务划分)   │    │   (任务执行)     │    │  (结果汇总)  │
└──────────────┘    └─────────────────┘    └──────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌─────────────┐    ┌─────────────────┐    ┌─────────────┐
│   OpenICL   │    │     Models      │    │  Datasets   │
│  (推理引擎)  │    │    (模型层)     │    │  (数据集层)  │
└─────────────┘    └─────────────────┘    └─────────────┘
```

### 4.2 核心组件职责

| 组件 | 职责 | 关键文件 |
|------|------|---------|
| **CLI** | 命令行入口，参数解析 | `opencompass/cli/main.py` |
| **Config** | 配置管理，组件注册 | `opencompass/registry.py` |
| **Partitioner** | 任务划分，负载均衡 | `opencompass/partitioners/` |
| **Runner** | 任务调度，执行管理 | `opencompass/runners/` |
| **OpenICL** | 推理逻辑，评测流程 | `opencompass/openicl/` |
| **Models** | 模型封装，推理接口 | `opencompass/models/` |
| **Datasets** | 数据加载，预处理 | `opencompass/datasets/` |
| **Summarizer** | 结果汇总，报告生成 | `opencompass/summarizers/` |

### 4.3 数据流

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ Config  │ -> │ Partition│ -> │  Runner │ -> │  Task   │
│ (配置)  │    │ (分区)   │    │ (调度)  │    │ (执行)  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
                                                   │
                     ┌─────────────────────────────┘
                     ▼
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ Model   │ -> │ Infer   │ -> │  Eval   │ -> │ Results │
│ (模型)  │    │ (推理)  │    │ (评估)  │    │ (结果)  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

---

## 5. 技术规格

### 5.1 技术栈

| 层级 | 技术选型 | 用途 |
|------|---------|------|
| 配置管理 | MMEngine | 配置系统和注册器机制 |
| 深度学习 | PyTorch, Transformers | 模型加载和推理 |
| 数据处理 | datasets (HF) | 数据集加载和处理 |
| 分布式 | torch.distributed, Slurm | 多机多卡并行评测 |
| 推理加速 | vLLM, LMDeploy | 高性能推理后端 |
| API集成 | OpenAI SDK, HTTP Client | 商业API调用 |

### 5.2 核心接口设计

#### 5.2.1 模型接口 (BaseModel)

```python
class BaseModel:
    def generate(self, inputs, max_out_len: int) -> List[str]:
        """生成式推理接口"""
        raise NotImplementedError

    def get_ppl(self, inputs) -> List[float]:
        """困惑度推理接口"""
        raise NotImplementedError

    def get_token_len(self, text: str) -> int:
        """获取token长度"""
        raise NotImplementedError
```

#### 5.2.2 数据集接口 (BaseDataset)

```python
class BaseDataset:
    def load(self):
        """加载数据集"""
        raise NotImplementedError

    def __getitem__(self, index):
        """获取单条数据"""
        raise NotImplementedError

    def __len__(self):
        """数据集大小"""
        raise NotImplementedError
```

#### 5.2.3 运行器接口 (BaseRunner)

```python
class BaseRunner:
    def launch(self, tasks: List[Task]):
        """启动任务执行"""
        raise NotImplementedError

    def wait(self):
        """等待任务完成"""
        raise NotImplementedError
```

### 5.3 目录结构

```
opencompass/
├── cli/                    # CLI入口
│   ├── main.py            # 主入口
│   └── args.py            # 参数解析
├── configs/               # 预置配置
│   ├── models/           # 模型配置
│   ├── datasets/         # 数据集配置
│   └── summarizers/      # 汇总配置
├── models/               # 模型实现
│   ├── base.py           # 基类
│   ├── huggingface.py    # HF模型
│   ├── openai_api.py     # API模型
│   └── vllm.py           # vLLM后端
├── datasets/             # 数据集实现
│   ├── base.py           # 基类
│   └── *.py              # 各数据集实现
├── openicl/              # 核心评测引擎
│   ├── icl_inferencer/   # 推理器
│   ├── icl_retriever/    # 检索器
│   ├── icl_prompt_template/  # 提示模板
│   └── icl_evaluator/    # 评估器
├── partitioners/         # 任务分区器
├── runners/              # 任务运行器
├── tasks/                # 任务定义
├── summarizers/          # 结果汇总
├── evaluator/            # 评估逻辑
└── utils/                # 工具函数
```

---

## 6. 评测场景

### 6.1 基础评测场景

| 场景 | 配置示例 | 说明 |
|------|---------|------|
| 单模型单数据集 | `configs/eval_demo.py` | 快速验证 |
| 多模型对比 | `configs/eval_multi_model.py` | 模型选型 |
| 全量评测 | `configs/eval_all.py` | 完整能力评估 |

### 6.2 高级评测场景

| 场景 | 技术方案 | 说明 |
|------|---------|------|
| 分布式评测 | SlurmRunner | 大规模集群评测 |
| 推理加速 | vLLM/LMDeploy | 高吞吐评测 |
| 长文本评测 | LongBench | 长上下文能力 |
| 安全评测 | SafetyBench | 模型安全性 |
| 代码评测 | HumanEval/MBPP | 代码生成能力 |

---

## 7. 质量保证

### 7.1 测试要求

| 测试类型 | 覆盖要求 | 工具 |
|---------|---------|------|
| 单元测试 | 核心模块覆盖率 > 80% | pytest |
| 集成测试 | 关键流程全覆盖 | pytest |
| 端到端测试 | 主要评测场景 | 手动/CI |

### 7.2 代码规范

- Python代码遵循PEP 8规范
- 使用Black进行代码格式化
- 使用Flake8进行代码检查
- 使用isort进行导入排序

### 7.3 文档要求

| 文档类型 | 内容 |
|---------|------|
| README | 项目介绍、快速开始 |
| 用户指南 | 功能使用说明 |
| API文档 | 接口说明 |
| 开发指南 | 贡献指南、开发规范 |

---

## 8. 发布规划

### 8.1 版本路线

| 版本 | 时间 | 重点功能 |
|------|------|---------|
| v0.5.x | 当前 | 稳定性优化、数据集扩充 |
| v0.6.0 | Q2 2026 | 多模态评测支持 |
| v0.7.0 | Q3 2026 | 实时评测榜单 |
| v1.0.0 | Q4 2026 | 企业级功能 |

### 8.2 发布流程

1. **开发阶段**：功能开发、代码审查
2. **测试阶段**：单元测试、集成测试、回归测试
3. **预发布**：Release Candidate版本
4. **正式发布**：版本发布、文档更新、公告

---

## 9. 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 数据集版权问题 | 法律风险 | 审核数据集授权、提供版权说明 |
| 评测结果争议 | 声誉风险 | 公开评测方法、提供复现指南 |
| 依赖版本冲突 | 使用问题 | 版本锁定、Docker镜像 |
| 性能瓶颈 | 用户体验 | 推理加速优化、分布式支持 |

---

## 10. 附录

### 10.1 参考资源

- [OpenCompass GitHub](https://github.com/open-compass/opencompass)
- [OpenCompass 文档](https://opencompass.readthedocs.io/)
- [MMEngine 文档](https://mmengine.readthedocs.io/)

### 10.2 术语表

| 术语 | 解释 |
|------|------|
| PPL | Perplexity，困惑度，衡量语言模型预测能力 |
| In-Context Learning | 上下文学习，通过示例引导模型输出 |
| Few-shot | 少样本学习，提供少量示例 |
| Zero-shot | 零样本学习，不提供示例 |
| Slurm | Simple Linux Utility for Resource Management，作业调度系统 |

### 10.3 更新历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v1.0 | 2026-03-05 | 初始版本 |