[根目录](../../../CLAUDE.md) > **src** > **router**

# Router 路由模块文档

> 最后更新: 2026-03-05

## 模块职责

管理应用路由系统，包括：
- 路由配置与生成
- 路由守卫
- 权限控制
- 页面切换进度条
- 文档标题更新

## 入口与启动

**入口文件**: `src/index.ts`

```typescript
import { createRouter, createWebHistory } from 'vue-router';

export const router = createRouter({
  history: createWebHistory(VITE_BASE_URL),
  routes: createBuiltinVueRoutes()
});

export async function setupRouter(app: App) {
  app.use(router);
  createRouterGuard(router);
  await router.isReady();
}
```

## 对外接口

### router 实例

Vue Router 实例，支持所有标准 API。

```typescript
import { router } from '@/router';

router.push({ name: 'home' });
router.replace({ path: '/login' });
router.currentRoute.value; // 当前路由
```

### 路由守卫

通过 `createRouterGuard` 注册三类守卫：

1. **进度条守卫** - 页面切换时显示进度条
2. **路由守卫** - 处理权限、登录状态
3. **标题守卫** - 更新文档标题

## 关键依赖与配置

### elegant-router

项目使用 `@elegant-router/vue` 自动生成路由：

```
src/views/
├── _builtin/
│   ├── login/index.vue    -> login
│   ├── 403/index.vue      -> 403
│   ├── 404/index.vue      -> 404
│   └── 500/index.vue      -> 500
└── home/
    └── index.vue          -> home
```

### 路由模式

```typescript
// 环境变量控制
VITE_AUTH_ROUTE_MODE=static   // 静态路由（开发推荐）
VITE_AUTH_ROUTE_MODE=dynamic  // 动态路由（生产推荐）
VITE_ROUTER_HISTORY_MODE=history | hash | memory
```

### 路由元信息

```typescript
interface RouteMeta {
  title: string;           // 页面标题
  i18nKey?: I18nKey;       // 国际化 Key
  icon?: string;           // 菜单图标
  order?: number;          // 菜单排序
  roles?: string[];        // 访问角色
  constant?: boolean;      // 是否常量路由
  href?: string;           // 外链地址
  hideInMenu?: boolean;    // 隐藏菜单
  hideInBreadcrumb?: boolean; // 隐藏面包屑
}
```

## 数据模型

```typescript
// 路由守卫流程
beforeEach:
  1. initRoute() - 初始化路由
  2. 检查登录状态
  3. 检查路由权限
  4. 允许/拒绝访问

// 静态路由生成
createStaticRoutes() -> {
  constantRoutes, // 常量路由（无需登录）
  authRoutes      // 权限路由（需要登录）
}

// 动态路由获取
fetchGetUserRoutes() -> { routes, home }
```

## 测试与质量

- 未配置单元测试
- 路由生成依赖 `pnpm gen-route` 命令

## 常见问题 (FAQ)

**Q: 如何添加新页面？**
1. 在 `src/views/` 下创建 Vue 组件
2. 运行 `pnpm gen-route` 生成路由
3. 配置路由 meta 信息

**Q: 如何控制页面权限？**
在路由 meta 中添加 `roles` 数组，守卫会自动检查。

**Q: 外链如何配置？**
```typescript
{
  name: 'external',
  meta: { href: 'https://example.com' }
}
```

## 相关文件清单

| 文件 | 说明 |
|------|------|
| `src/index.ts` | 主入口 |
| `src/guard/index.ts` | 守卫注册 |
| `src/guard/route.ts` | 路由权限守卫 |
| `src/guard/progress.ts` | 进度条守卫 |
| `src/guard/title.ts` | 标题守卫 |
| `src/routes/index.ts` | 路由生成 |
| `src/routes/builtin.ts` | 内置路由 |
| `src/elegant/routes.ts` | 自动生成路由 |
| `src/elegant/imports.ts` | 自动生成导入 |
| `src/elegant/transform.ts` | 路由转换 |

---

## 变更记录 (Changelog)

| 日期 | 变更内容 |
|------|----------|
| 2026-03-05 | 初始化模块文档 |