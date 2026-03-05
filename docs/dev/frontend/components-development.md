# 前端组件开发文档

> 最后更新: 2026-03-05

## 概述

自定义图表组件位于 `src/components/custom/` 目录，基于 ECharts 实现数据可视化。

## 目录结构

```
src/components/custom/
├── evaluation-radar-chart/   # 雷达图组件
│   └── index.vue
├── evaluation-bar-chart/     # 柱状图组件
│   └── index.vue
└── evaluation-compare-chart/ # 对比图组件
    └── index.vue
```

## 组件列表

### 1. 雷达图组件 (EvaluationRadarChart)

**用途：** 展示多维度评测指标

**Props：**

```typescript
interface Props {
  data: {
    indicators: Array<{ name: string; max: number }>;
    values: Array<{ name: string; value: number[] }>;
  };
  title?: string;
  height?: string;
}
```

**使用示例：**

```vue
<template>
  <EvaluationRadarChart
    :data="radarData"
    title="模型能力雷达图"
    height="400px"
  />
</template>

<script setup>
import EvaluationRadarChart from '@/components/custom/evaluation-radar-chart/index.vue';

const radarData = {
  indicators: [
    { name: '推理能力', max: 100 },
    { name: '代码能力', max: 100 },
    { name: '数学能力', max: 100 },
    { name: '语言理解', max: 100 },
    { name: '知识问答', max: 100 }
  ],
  values: [
    { name: 'GPT-4', value: [95, 88, 92, 96, 94] },
    { name: 'Claude', value: [92, 90, 88, 95, 92] }
  ]
};
</script>
```

### 2. 柱状图组件 (EvaluationBarChart)

**用途：** 展示评测分数对比

**Props：**

```typescript
interface Props {
  data: {
    categories: string[];
    series: Array<{ name: string; data: number[] }>;
  };
  title?: string;
  height?: string;
  horizontal?: boolean;
}
```

**使用示例：**

```vue
<template>
  <EvaluationBarChart
    :data="barData"
    title="数据集评测分数"
    horizontal
  />
</template>

<script setup>
const barData = {
  categories: ['MMLU', 'HellaSwag', 'ARC', 'TruthfulQA'],
  series: [
    { name: 'GPT-4', data: [86.4, 95.3, 96.3, 85.6] },
    { name: 'Claude', data: [84.2, 94.1, 95.8, 83.2] }
  ]
};
</script>
```

### 3. 对比图组件 (EvaluationCompareChart)

**用途：** 展示多个模型的横向对比

**Props：**

```typescript
interface Props {
  models: Array<{
    name: string;
    metrics: Record<string, number>;
  }>;
  title?: string;
  height?: string;
}
```

**使用示例：**

```vue
<template>
  <EvaluationCompareChart
    :models="compareData"
    title="模型对比"
  />
</template>

<script setup>
const compareData = [
  {
    name: 'GPT-4',
    metrics: { MMLU: 86.4, HellaSwag: 95.3, ARC: 96.3 }
  },
  {
    name: 'Claude',
    metrics: { MMLU: 84.2, HellaSwag: 94.1, ARC: 95.8 }
  }
];
</script>
```

## ECharts 配置封装

```typescript
// 通用 ECharts 配置
const baseOption = {
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'shadow' }
  },
  legend: {
    bottom: 0
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '15%',
    containLabel: true
  },
  xAxis: { type: 'category' },
  yAxis: { type: 'value' }
};
```

## 响应式处理

```vue
<script setup>
import { useElementSize } from '@vueuse/core';
import * as echarts from 'echarts';

const chartRef = ref<HTMLElement>();
const { width, height } = useElementSize(chartRef);

// 监听尺寸变化，自动调整图表
watch([width, height], () => {
  chart?.resize();
});
</script>
```

---

## 变更记录

| 日期 | 变更内容 |
|------|----------|
| 2026-03-05 | 初始化前端组件开发文档 |