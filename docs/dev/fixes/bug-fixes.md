# 问题修复记录文档

> 最后更新: 2026-03-05

## 概述

记录开发过程中遇到的问题及解决方案。

---

## 2026-03-05 API 路径前缀缺失

### 问题描述

前端登录请求返回 404 错误：
```
Request URL: http://localhost:9527/proxy-default/auth/login
Status Code: 404 Not Found
```

### 问题原因

前端 API 路径缺少 `/api/v1` 前缀：
- 实际请求：`/auth/login`
- 后端路径：`/api/v1/auth/login`

### 解决方案

修改 `frontend/src/service/api/auth.ts`，添加正确的路径前缀：

```typescript
// 修改前
export function fetchLogin(userName: string, password: string) {
  return request<Api.Auth.LoginToken>({
    url: '/auth/login',  // ❌ 缺少前缀
    method: 'post',
    data: { userName, password }
  });
}

// 修改后
export function fetchLogin(userName: string, password: string) {
  return request<Api.Auth.LoginToken>({
    url: '/api/v1/auth/login',  // ✅ 添加前缀
    method: 'post',
    data: { userName, password }
  });
}
```

同时修复其他接口：
- `/auth/login` → `/api/v1/auth/login`
- `/auth/getUserInfo` → `/api/v1/auth/getUserInfo`
- `/auth/refreshToken` → `/api/v1/auth/refreshToken`

---

## 2026-03-05 Token 参数格式错误

### 问题描述

获取用户信息返回 401 错误：
```
Request URL: http://127.0.0.1:9527/proxy-default/api/v1/auth/getUserInfo?token=%22uuid-token%22
Status Code: 401 Unauthorized
```

URL 中 token 参数带有额外的双引号（`%22` 是双引号编码）。

### 问题原因

使用 `localStorage.getItem('SOY_token')` 直接获取存储值，返回的是 JSON 字符串（带引号）：
```javascript
// localStorage 存储的是 JSON 字符串
localStorage.getItem('SOY_token')  // "\"uuid-token\""

// 实际传递的值
token: "\"uuid-token\""  // 带引号的字符串
```

### 解决方案

使用 `localStg.get('token')` 方法，它会自动解析 JSON：

```typescript
// 修改前
export function fetchGetUserInfo() {
  const token = localStorage.getItem('SOY_token');  // ❌ 返回带引号的字符串
  return request<Api.Auth.UserInfo>({
    url: '/api/v1/auth/getUserInfo',
    method: 'get',
    params: { token }
  });
}

// 修改后
import { localStg } from '@/utils/storage';

export function fetchGetUserInfo() {
  const token = localStg.get('token');  // ✅ 自动解析 JSON，返回正确值
  return request<Api.Auth.UserInfo>({
    url: '/api/v1/auth/getUserInfo',
    method: 'get',
    params: { token }
  });
}
```

**原理说明：**

`localStg` 封装了存储操作，在存储时 `JSON.stringify`，获取时 `JSON.parse`：
```typescript
// packages/utils/src/storage.ts
set(key, value) {
  const json = JSON.stringify(value);
  stg.setItem(`${prefix}${key}`, json);
},
get(key) {
  const json = stg.getItem(`${prefix}${key}`);
  return JSON.parse(json);  // 自动解析
}
```

---

## 2026-03-05 请求响应格式不匹配

### 问题描述

前端请求成功但显示错误，因为前端期望后端返回 `{ code, data }` 格式，但后端直接返回数据。

### 问题原因

前端 `@sa/axios` 封装期望后端返回标准格式：
```typescript
interface Response<T> {
  code: string;
  data: T;
  msg: string;
}
```

但后端直接返回数据：
```json
{ "token": "xxx", "refreshToken": "xxx" }
```

### 解决方案

修改 `frontend/src/service/request/index.ts`：

```typescript
export const request = createFlatRequest(
  { baseURL, headers: {} },
  {
    // 直接返回响应数据
    transform(response: AxiosResponse<App.Service.Response<any>>) {
      return response.data;  // 直接返回，不检查 code
    },
    // 始终返回 true
    isBackendSuccess(_response) {
      return true;  // 后端直接返回数据，视为成功
    },
    // 其他配置...
  }
);
```

---

## 2026-03-05 requirements.txt 依赖安装失败

### 问题描述

安装后端依赖时报错：
```
ERROR: Could not build wheels for opencompass, weasyprint
```

### 解决方案

从 `requirements.txt` 移除有问题的依赖：
```
# 移除
# opencompass>=0.5.0
# weasyprint>=60.2
```

保留核心依赖即可运行开发环境。

---

## 总结

| 日期 | 问题 | 解决方案 |
|------|------|----------|
| 2026-03-05 | API 路径前缀缺失 | 添加 `/api/v1` 前缀 |
| 2026-03-05 | Token 参数格式错误 | 使用 `localStg.get()` |
| 2026-03-05 | 请求响应格式不匹配 | 修改 `transform` 和 `isBackendSuccess` |
| 2026-03-05 | 依赖安装失败 | 移除问题依赖 |

---

## 变更记录

| 日期 | 变更内容 |
|------|----------|
| 2026-03-05 | 初始化问题修复文档 |