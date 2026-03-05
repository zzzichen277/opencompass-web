[根目录](../../../CLAUDE.md) > **src** > **store**

# Store 状态管理模块文档

> 最后更新: 2026-03-05

## 模块职责

基于 Pinia 实现全局状态管理，包含以下子模块：
- **auth** - 用户认证状态
- **route** - 路由与菜单状态
- **theme** - 主题配置状态
- **tab** - 标签页状态
- **app** - 应用全局状态

## 入口与启动

**入口文件**: `src/index.ts`

```typescript
import { createPinia } from 'pinia';

export function setupStore(app: App) {
  const store = createPinia();
  store.use(resetSetupStore);
  app.use(store);
}
```

## 对外接口

### useAuthStore

用户认证状态管理。

```typescript
const authStore = useAuthStore();

// 状态
authStore.token          // 用户 Token
authStore.userInfo       // 用户信息
authStore.isLogin        // 是否已登录
authStore.isStaticSuper  // 是否超级管理员

// 方法
authStore.login(userName, password)  // 登录
authStore.resetStore()               // 重置状态
authStore.initUserInfo()             // 初始化用户信息
```

### useRouteStore

路由与菜单状态管理。

```typescript
const routeStore = useRouteStore();

// 状态
routeStore.menus           // 全局菜单
routeStore.breadcrumbs     // 面包屑
routeStore.cacheRoutes     // 缓存路由
routeStore.routeHome       // 首页路由

// 方法
routeStore.initConstantRoute()  // 初始化常量路由
routeStore.initAuthRoute()      // 初始化权限路由
routeStore.resetStore()         // 重置状态
```

### useThemeStore

主题配置状态管理。

```typescript
const themeStore = useThemeStore();

// 状态
themeStore.settings        // 主题配置
themeStore.darkMode        // 暗黑模式
themeStore.themeColors     // 主题颜色
themeStore.naiveTheme      // NaiveUI 主题

// 方法
themeStore.setThemeScheme(scheme)       // 设置主题模式
themeStore.toggleThemeScheme()          // 切换主题模式
themeStore.updateThemeColors(key, color) // 更新主题颜色
themeStore.setThemeLayout(mode)         // 设置布局模式
```

### useTabStore

标签页状态管理。

```typescript
const tabStore = useTabStore();

// 状态
tabStore.tabs           // 标签列表
tabStore.activeTab      // 当前激活标签

// 方法
tabStore.addTab(route)       // 添加标签
tabStore.removeTab(tabId)    // 移除标签
tabStore.clearTabs()         // 清空标签
tabStore.cacheTabs()         // 缓存标签
```

## 关键依赖与配置

### Store ID 枚举

```typescript
// src/enum/index.ts
export enum SetupStoreId {
  App = 'app-store',
  Theme = 'theme-store',
  Auth = 'auth-store',
  Route = 'route-store',
  Tab = 'tab-store'
}
```

### 持久化策略

- Token/RefreshToken: localStorage
- 用户信息: 内存（登录后获取）
- 主题配置: localStorage（页面关闭时保存）
- 标签页: localStorage（可选缓存）

## 数据模型

```typescript
// 用户信息
interface UserInfo {
  userId: string;
  userName: string;
  roles: string[];
  buttons: string[];
}

// 主题配置
interface ThemeSetting {
  themeScheme: 'light' | 'dark' | 'auto';
  themeColor: string;
  layout: { mode: LayoutMode; scrollMode: ScrollMode };
  header: HeaderConfig;
  tab: TabConfig;
  sider: SiderConfig;
  footer: FooterConfig;
  watermark: WatermarkConfig;
}

// 标签
interface Tab {
  id: string;
  label: string;
  routeKey: RouteKey;
  routePath: RoutePath;
  fullPath: string;
  fixedIndex?: number | null;
}
```

## 测试与质量

- 未配置单元测试
- 使用 Composition API + Setup 语法定义 Store

## 常见问题 (FAQ)

**Q: 如何重置某个 Store 状态？**
```typescript
authStore.$reset(); // 或 authStore.resetStore()
```

**Q: 如何在组件外使用 Store？**
确保在应用初始化后再调用，否则 Store 未注册。

## 相关文件清单

| 文件 | 说明 |
|------|------|
| `src/index.ts` | 主入口，Pinia 初始化 |
| `src/plugins/index.ts` | Store 插件 |
| `src/modules/auth/index.ts` | 认证状态 |
| `src/modules/route/index.ts` | 路由状态 |
| `src/modules/theme/index.ts` | 主题状态 |
| `src/modules/tab/index.ts` | 标签状态 |
| `src/modules/app/index.ts` | 应用状态 |

---

## 变更记录 (Changelog)

| 日期 | 变更内容 |
|------|----------|
| 2026-03-05 | 初始化模块文档 |