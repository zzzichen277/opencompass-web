[根目录](../../CLAUDE.md) > **packages** > **axios**

# @sa/axios 模块文档

> 最后更新: 2026-03-05

## 模块职责

提供 Axios HTTP 客户端的封装实现，支持：
- 请求/响应拦截器
- 自动重试机制
- 请求取消（AbortController）
- Token 自动刷新
- 统一错误处理
- 平铺响应格式（FlatRequest）

## 入口与启动

**入口文件**: `src/index.ts`

```typescript
export function createRequest(axiosConfig, options)     // 标准请求实例
export function createFlatRequest(axiosConfig, options) // 平铺响应请求实例
```

## 对外接口

### createRequest

创建标准请求实例，响应数据直接返回。

```typescript
const request = createRequest<ResponseData, ApiData, State>(axiosConfig, {
  transform(response) { return response.data; },
  async onRequest(config) { return config; },
  isBackendSuccess(response) { return response.data.code === '0000'; },
  async onBackendFail(response, instance) { /* 处理业务错误 */ },
  onError(error) { /* 处理请求错误 */ }
});
```

### createFlatRequest

创建平铺响应请求实例，返回 `{ data, error, response }` 格式。

```typescript
const request = createFlatRequest<ResponseData, ApiData, State>(axiosConfig, options);
const { data, error } = await request({ url: '/api/xxx' });
```

### 导出常量

- `BACKEND_ERROR_CODE` - 后端业务错误码
- `REQUEST_ID_KEY` - 请求 ID 头键名

## 关键依赖与配置

### 依赖

| 包名 | 用途 |
|------|------|
| `axios` | HTTP 客户端 |
| `axios-retry` | 自动重试 |
| `@sa/utils` | nanoid 生成 |

### 配置项 (RequestOption)

| 配置 | 说明 |
|------|------|
| `transform` | 响应数据转换 |
| `onRequest` | 请求拦截器 |
| `isBackendSuccess` | 判断业务成功 |
| `onBackendFail` | 业务失败处理 |
| `onError` | 错误处理 |
| `defaultState` | 默认状态 |

## 数据模型

```typescript
// 请求实例类型
type RequestInstance<ApiData, State> = {
  (config: CustomAxiosRequestConfig): Promise<ApiData>;
  cancelAllRequest: () => void;
  state: State;
};

// 平铺请求实例类型
type FlatRequestInstance<ResponseData, ApiData, State> = {
  (config: CustomAxiosRequestConfig): Promise<{
    data: ApiData | null;
    error: AxiosError | null;
    response: AxiosResponse | undefined;
  }>;
  cancelAllRequest: () => void;
  state: State;
};
```

## 测试与质量

- 未配置单元测试
- 使用 TypeScript 严格模式

## 常见问题 (FAQ)

**Q: 如何取消所有请求？**
```typescript
request.cancelAllRequest();
```

**Q: 如何实现 Token 刷新？**
在 `onBackendFail` 中检测 Token 过期码，调用刷新接口后重试请求。

## 相关文件清单

| 文件 | 说明 |
|------|------|
| `src/index.ts` | 主入口，导出 createRequest/createFlatRequest |
| `src/constant.ts` | 常量定义 |
| `src/options.ts` | 默认配置生成 |
| `src/shared.ts` | 共享工具函数 |
| `src/type.ts` | 类型定义 |

---

## 变更记录 (Changelog)

| 日期 | 变更内容 |
|------|----------|
| 2026-03-05 | 初始化模块文档 |