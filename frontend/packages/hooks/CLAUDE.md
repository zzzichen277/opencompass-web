[根目录](../../CLAUDE.md) > **packages** > **hooks**

# @sa/hooks 模块文档

> 最后更新: 2026-03-05

## 模块职责

提供通用的 Vue Composition API Hooks，支持：
- 布尔状态管理
- 加载状态管理
- 倒计时功能
- 上下文共享
- SVG 图标渲染
- 表格数据管理

## 入口与启动

**入口文件**: `src/index.ts`

```typescript
export { useBoolean, useLoading, useCountDown, useContext, useSvgIconRender, useTable };
```

## 对外接口

### useBoolean

布尔状态管理 Hook。

```typescript
const { bool, setBool, setTrue, setFalse, toggle } = useBoolean(false);
```

### useLoading

加载状态管理 Hook。

```typescript
const { loading, startLoading, endLoading } = useLoading(false);
```

### useCountDown

倒计时 Hook。

```typescript
const { count, counting, startCount, stopCount } = useCountDown(60);
```

### useContext

上下文共享 Hook，用于跨组件共享状态。

```typescript
const { context, setContext, getContext } = useContext(key);
```

### useSvgIconRender

SVG 图标渲染 Hook。

```typescript
const { SvgIconVNode } = useSvgIconRender(h);
```

### useTable

表格数据管理 Hook，支持分页、排序、筛选。

```typescript
const { data, loading, pagination, getData } = useTable(fetchApi);
```

## 关键依赖与配置

### 依赖

| 包名 | 用途 |
|------|------|
| `vue` | 响应式 API |

## 数据模型

```typescript
// useBoolean 返回类型
interface BooleanReturnType {
  bool: Ref<boolean>;
  setBool: (value: boolean) => void;
  setTrue: () => void;
  setFalse: () => void;
  toggle: () => void;
}

// useLoading 返回类型
interface LoadingReturnType {
  loading: Ref<boolean>;
  startLoading: () => void;
  endLoading: () => void;
}

// useTable 配置
interface TableConfig {
  immediate?: boolean;
  pageSize?: number;
  api: (params: any) => Promise<any>;
}
```

## 测试与质量

- 未配置单元测试
- 使用 TypeScript 严格模式

## 相关文件清单

| 文件 | 说明 |
|------|------|
| `src/index.ts` | 主入口 |
| `src/use-boolean.ts` | 布尔状态 Hook |
| `src/use-loading.ts` | 加载状态 Hook |
| `src/use-count-down.ts` | 倒计时 Hook |
| `src/use-context.ts` | 上下文 Hook |
| `src/use-svg-icon-render.ts` | SVG 渲染 Hook |
| `src/use-table.ts` | 表格管理 Hook |

---

## 变更记录 (Changelog)

| 日期 | 变更内容 |
|------|----------|
| 2026-03-05 | 初始化模块文档 |