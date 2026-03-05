# 前端 API 对接文档

> 最后更新: 2026-03-05

## 概述

API 服务层位于 `src/service/` 目录，负责与后端通信。

## 目录结构

```
src/service/
├── api/
│   ├── auth.ts           # 认证接口
│   └── evaluation.ts     # 评测接口
├── request/
│   ├── index.ts          # 请求封装
│   ├── shared.ts         # 共享方法
│   └── type.ts           # 类型定义
└── typings/
    └── api.d.ts          # API 类型声明
```

## 认证 API (auth.ts)

```typescript
import { localStg } from '@/utils/storage';
import { request } from '../request';

// 登录
export function fetchLogin(userName: string, password: string) {
  return request<Api.Auth.LoginToken>({
    url: '/api/v1/auth/login',
    method: 'post',
    data: { userName, password }
  });
}

// 获取用户信息
export function fetchGetUserInfo() {
  const token = localStg.get('token');
  return request<Api.Auth.UserInfo>({
    url: '/api/v1/auth/getUserInfo',
    method: 'get',
    params: { token }
  });
}

// 刷新令牌
export function fetchRefreshToken(refreshToken: string) {
  return request<Api.Auth.LoginToken>({
    url: '/api/v1/auth/refreshToken',
    method: 'post',
    data: { refreshToken }
  });
}
```

## 评测 API (evaluation.ts)

```typescript
import { request } from '../request';

// ========== 模型管理 ==========

export function fetchModels() {
  return request<Api.Evaluation.Model[]>({
    url: '/api/v1/models',
    method: 'get'
  });
}

export function fetchModel(id: string) {
  return request<Api.Evaluation.Model>({
    url: `/api/v1/models/${id}`,
    method: 'get'
  });
}

export function createModel(data: Partial<Api.Evaluation.Model>) {
  return request<Api.Evaluation.Model>({
    url: '/api/v1/models',
    method: 'post',
    data
  });
}

// ========== 数据集管理 ==========

export function fetchDatasets() {
  return request<Api.Evaluation.Dataset[]>({
    url: '/api/v1/datasets',
    method: 'get'
  });
}

export function fetchBuiltinDatasets() {
  return request<Api.Evaluation.Dataset[]>({
    url: '/api/v1/datasets/builtin',
    method: 'get'
  });
}

// ========== 任务管理 ==========

export function fetchTasks() {
  return request<Api.Evaluation.Task[]>({
    url: '/api/v1/tasks',
    method: 'get'
  });
}

export function startTask(taskId: string) {
  return request<void>({
    url: `/api/v1/tasks/${taskId}/start`,
    method: 'post'
  });
}

export function stopTask(taskId: string) {
  return request<void>({
    url: `/api/v1/tasks/${taskId}/stop`,
    method: 'post'
  });
}

// ========== 结果查询 ==========

export function fetchResults(taskId: string) {
  return request<Api.Evaluation.Result[]>({
    url: `/api/v1/results/task/${taskId}`,
    method: 'get'
  });
}

export function fetchLeaderboard() {
  return request<Api.Evaluation.LeaderboardItem[]>({
    url: '/api/v1/results/leaderboard',
    method: 'get'
  });
}
```

## 类型定义 (api.d.ts)

```typescript
declare namespace Api {
  namespace Auth {
    interface LoginToken {
      token: string;
      refreshToken: string;
    }

    interface UserInfo {
      userId: string;
      userName: string;
      roles: string[];
      buttons: string[];
    }
  }

  namespace Evaluation {
    interface Model {
      id: string;
      name: string;
      path: string;
      type: 'huggingface' | 'api' | 'custom';
      config: Record<string, any>;
      createdAt: string;
    }

    interface Task {
      id: string;
      name: string;
      modelId: string;
      datasetIds: string[];
      status: 'pending' | 'running' | 'completed' | 'failed';
      progress: number;
      createdAt: string;
    }

    interface Result {
      id: string;
      taskId: string;
      datasetName: string;
      metrics: Record<string, number>;
      details: Record<string, any>;
    }
  }
}
```

## 请求封装 (request/index.ts)

```typescript
import { createFlatRequest } from '@sa/axios';
import { localStg } from '@/utils/storage';

export const request = createFlatRequest(
  {
    baseURL,
    headers: {}
  },
  {
    // 直接返回响应数据
    transform(response) {
      return response.data;
    },
    // 请求拦截：添加 Token
    async onRequest(config) {
      const token = localStg.get('token');
      if (token) {
        Object.assign(config.headers, { Authorization: `Bearer ${token}` });
      }
      return config;
    },
    // 后端始终成功（直接返回数据）
    isBackendSuccess(_response) {
      return true;
    },
    // 错误处理
    onError(error) {
      window.$message?.error(error.message);
    }
  }
);
```

---

## 变更记录

| 日期 | 变更内容 |
|------|----------|
| 2026-03-05 | 初始化前端 API 对接文档 |