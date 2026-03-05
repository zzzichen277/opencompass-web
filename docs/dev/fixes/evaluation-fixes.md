# 评测管理问题修复记录

> 最后更新: 2026-03-05

## 修复概要

| 序号 | 问题 | 状态 |
|------|------|------|
| 1 | API 模块导出缺失 | ✅ 已修复 |
| 2 | API 路径前缀不统一 | ✅ 已修复 |
| 3 | WebSocket 消息格式 | ✅ 已确认正确 |
| 4 | 路由配置缺失 | ✅ 已确认存在 |
| 5 | 菜单国际化显示异常 | ✅ 已修复 |

---

## 问题 1: API 模块导出缺失

### 问题描述

`src/service/api/index.ts` 缺少 `evaluation` 模块导出，导致其他模块无法使用评测 API。

### 解决方案

```typescript
// 修改前
export * from './auth';
export * from './route';

// 修改后
export * from './auth';
export * from './route';
export * from './evaluation';
```

---

## 问题 2: API 路径前缀不统一

### 问题描述

- `auth.ts` 直接写 `/api/v1/auth/xxx`
- `evaluation.ts` 使用 `${API_PREFIX}/xxx`

### 解决方案

统一使用 `API_PREFIX` 常量管理路径前缀：

```typescript
// auth.ts
const API_PREFIX = '/api/v1';

export function fetchLogin(userName: string, password: string) {
  return request<Api.Auth.LoginToken>({
    url: `${API_PREFIX}/auth/login`,
    method: 'post',
    data: { userName, password }
  });
}
```

---

## 问题 3: WebSocket 消息格式

### 确认结果

后端和前端消息格式已对齐：

**后端发送格式：**
```json
{
  "type": "progress",
  "task_id": "xxx",
  "timestamp": "2026-03-05T10:00:00",
  "data": {
    "progress": 50,
    "status": "running"
  }
}
```

**前端期望格式：**
```typescript
interface WSMessage {
  type: 'progress' | 'log' | 'completed' | 'subscribed' | 'pong';
  task_id: string;
  timestamp: string;
  data: Record<string, any>;
}
```

格式一致，无需修改。

---

## 问题 4: 路由配置

### 确认结果

路由配置已存在于 `src/router/elegant/routes.ts`：

```typescript
{
  name: 'evaluation',
  path: '/evaluation',
  component: 'layout.base',
  meta: {
    title: 'evaluation',
    i18nKey: 'route.evaluation',
    icon: 'mdi:clipboard-check-outline',
    order: 2
  },
  children: [
    { name: 'evaluation_task', path: '/evaluation/task', ... },
    { name: 'evaluation_model', path: '/evaluation/model', ... },
    { name: 'evaluation_dataset', path: '/evaluation/dataset', ... },
    { name: 'evaluation_result', path: '/evaluation/result', ... },
    { name: 'evaluation_template', path: '/evaluation/template', ... }
  ]
}
```

组件导入也已配置：

```typescript
evaluation_task: () => import("@/views/evaluation/task/index.vue"),
evaluation_model: () => import("@/views/evaluation/model/index.vue"),
// ...
```

---

## 问题 5: 菜单国际化显示异常

### 问题描述

评测管理子菜单显示 `route.evaluation_dataset` 而非中文。

### 问题原因

路由配置使用下划线格式 `evaluation_dataset`，但国际化文件使用连字符格式 `evaluation-dataset`，导致匹配失败。

### 解决方案

在国际化文件中添加下划线格式的 key：

```typescript
// zh-cn.ts
route: {
  // ...原有配置
  evaluation_task: '任务管理',
  evaluation_model: '模型管理',
  evaluation_dataset: '数据集管理',
  evaluation_result: '评测结果',
  evaluation_template: '评测模板'
}

// en-us.ts
route: {
  // ...原有配置
  evaluation_task: 'Tasks',
  evaluation_model: 'Models',
  evaluation_dataset: 'Datasets',
  evaluation_result: 'Results',
  evaluation_template: 'Templates'
}
```

---

## 变更记录

| 日期 | 变更内容 |
|------|----------|
| 2026-03-05 | 修复 API 模块导出 |
| 2026-03-05 | 统一 API 路径前缀 |
| 2026-03-05 | 确认 WebSocket 格式正确 |
| 2026-03-05 | 确认路由配置完整 |
| 2026-03-05 | 修复菜单国际化显示 |