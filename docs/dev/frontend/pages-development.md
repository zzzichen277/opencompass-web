# 前端页面开发文档

> 最后更新: 2026-03-05

## 概述

前端评测管理页面位于 `src/views/evaluation/` 目录，包含任务、模型、数据集、结果、模板五个功能模块。

## 目录结构

```
src/views/evaluation/
├── task/                     # 任务管理
│   └── index.vue
├── model/                    # 模型管理
│   └── index.vue
├── dataset/                  # 数据集管理
│   └── index.vue
├── result/                   # 结果展示
│   └── index.vue
└── template/                 # 模板管理
    └── index.vue
```

## 页面功能

### 1. 任务管理页面

**功能列表：**
- 任务列表展示（表格）
- 创建新任务（模态框表单）
- 启动/停止任务
- 查看任务详情
- 实时进度显示
- 任务日志查看

**核心代码：**

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { NButton, NTag, NProgress } from 'naive-ui';
import { fetchTasks, startTask, stopTask } from '@/service/api/evaluation';
import { useEvaluationWebSocket } from '@/hooks/business/useEvaluationWebSocket';

const tasks = ref([]);
const { subscribe, unsubscribe } = useEvaluationWebSocket();

// 获取任务列表
async function loadTasks() {
  const { data } = await fetchTasks();
  if (data) tasks.value = data;
}

// 订阅任务进度
function subscribeTask(taskId: string) {
  subscribe(taskId, {
    onProgress: (progress) => {
      const task = tasks.value.find(t => t.id === taskId);
      if (task) task.progress = progress;
    }
  });
}

onMounted(() => {
  loadTasks();
});
</script>
```

### 2. 模型管理页面

**功能列表：**
- 模型列表展示
- 添加新模型
- 编辑模型配置
- 删除模型
- 模型类型支持：HuggingFace、API、自定义

### 3. 数据集管理页面

**功能列表：**
- 数据集列表展示
- 内置数据集查看
- 上传自定义数据集
- 数据集配置编辑
- 删除数据集

### 4. 结果展示页面

**功能列表：**
- 评测结果列表
- 排行榜展示
- 结果详情图表
- 导出报告

### 5. 模板管理页面

**功能列表：**
- 模板列表
- 创建评测模板
- 从模板创建任务
- 编辑/删除模板

## 表格列定义示例

```typescript
// 任务表格列
const taskColumns = [
  { title: '任务名称', key: 'name' },
  { title: '模型', key: 'modelName' },
  { title: '状态', key: 'status', render: renderStatus },
  { title: '进度', key: 'progress', render: renderProgress },
  { title: '创建时间', key: 'createdAt' },
  { title: '操作', key: 'actions', render: renderActions }
];

// 状态渲染
function renderStatus(row: Task) {
  const statusMap = {
    pending: { type: 'default', text: '待执行' },
    running: { type: 'info', text: '执行中' },
    completed: { type: 'success', text: '已完成' },
    failed: { type: 'error', text: '失败' }
  };
  const s = statusMap[row.status];
  return h(NTag, { type: s.type }, () => s.text);
}

// 进度渲染
function renderProgress(row: Task) {
  return h(NProgress, {
    type: 'line',
    percentage: row.progress,
    status: row.status === 'failed' ? 'error' : undefined
  });
}
```

---

## 变更记录

| 日期 | 变更内容 |
|------|----------|
| 2026-03-05 | 初始化前端页面开发文档 |