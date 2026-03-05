[根目录](../../../CLAUDE.md) > **src** > **layouts**

# Layouts 布局模块文档

> 最后更新: 2026-03-05

## 模块职责

管理应用布局系统，包括：
- 基础布局容器
- 空白布局
- 全局头部、侧边栏、标签页、底部栏
- 主题配置面板
- 全局搜索

## 目录结构

```
layouts/
├── base-layout/
│   └── index.vue          # 基础布局容器
├── blank-layout/
│   └── index.vue          # 空白布局（登录页等）
└── modules/               # 布局子模块
    ├── global-breadcrumb/ # 面包屑
    ├── global-content/    # 内容区域
    ├── global-footer/     # 底部栏
    ├── global-header/     # 头部
    │   ├── index.vue
    │   └── components/
    ├── global-logo/       # Logo
    ├── global-menu/       # 菜单
    │   ├── index.vue
    │   ├── context/
    │   └── modules/       # 菜单样式变体
    ├── global-search/     # 全局搜索
    ├── global-sider/      # 侧边栏
    ├── global-tab/        # 标签页
    │   ├── index.vue
    │   └── context-menu.vue
    └── theme-drawer/      # 主题配置面板
        └── modules/       # 配置子面板
```

## 对外接口

### 布局组件

#### base-layout

标准后台布局，包含头部、侧边栏、标签页、内容区、底部栏。

```vue
<template>
  <BaseLayout>
    <router-view />
  </BaseLayout>
</template>
```

#### blank-layout

空白布局，无任何装饰，用于登录、异常页面等。

```vue
<template>
  <BlankLayout>
    <router-view />
  </BlankLayout>
</template>
```

### 布局模式

支持多种布局模式：

| 模式 | 说明 |
|------|------|
| `vertical` | 垂直布局（经典后台） |
| `vertical-mix` | 垂直混合布局 |
| `horizontal` | 水平布局 |
| `horizontal-mix` | 水平混合布局 |

### 子模块组件

#### global-header

全局头部，包含 Logo、菜单折叠按钮、面包屑、搜索、语言切换、主题切换、用户头像。

#### global-menu

全局菜单，根据布局模式自动切换样式：
- `vertical-menu` - 垂直菜单
- `vertical-mix-menu` - 垂直混合菜单
- `horizontal-menu` - 水平菜单

#### global-tab

标签页管理，支持：
- Chrome 风格
- 按钮风格
- 右键菜单（关闭、固定、刷新）

#### theme-drawer

主题配置面板，分类：
- **外观** - 主题模式、颜色、圆角
- **布局** - 布局模式、头部、侧边栏、标签页配置
- **通用** - 水印、多语言
- **预设** - 主题预设选择

## 关键依赖与配置

### 主题配置

布局各部分尺寸由主题 Store 控制：

```typescript
themeStore.settings.header.height   // 头部高度
themeStore.settings.sider.width     // 侧边栏宽度
themeStore.settings.tab.height      // 标签页高度
themeStore.settings.footer.height   // 底部栏高度
```

### 响应式布局

使用 `@sa/materials` 的 AdminLayout 组件处理响应式逻辑。

## 数据模型

```typescript
// 头部配置
interface HeaderProps {
  showLogo?: boolean;
  showMenuToggler?: boolean;
  showMenu?: boolean;
}

// 菜单项
interface Menu {
  key: string;
  label: string;
  i18nKey?: I18nKey;
  routeKey: RouteKey;
  routePath: RoutePath;
  icon?: () => VNode;
  children?: Menu[];
}

// 标签页
interface Tab {
  id: string;
  label: string;
  routeKey: RouteKey;
  fullPath: string;
  fixedIndex?: number | null;
}
```

## 测试与质量

- 未配置单元测试
- 布局样式使用 SCSS + UnoCSS

## 常见问题 (FAQ)

**Q: 如何修改布局模式？**
通过主题配置面板或 `themeStore.setThemeLayout(mode)`。

**Q: 如何隐藏标签页？**
设置 `themeStore.settings.tab.visible = false`。

**Q: 如何添加新的菜单项？**
在对应的路由 meta 中配置 `icon`、`title`、`order`。

## 相关文件清单

| 文件 | 说明 |
|------|------|
| `base-layout/index.vue` | 基础布局 |
| `blank-layout/index.vue` | 空白布局 |
| `modules/global-header/index.vue` | 头部 |
| `modules/global-menu/index.vue` | 菜单 |
| `modules/global-tab/index.vue` | 标签页 |
| `modules/global-sider/index.vue` | 侧边栏 |
| `modules/theme-drawer/index.vue` | 主题面板 |

---

## 变更记录 (Changelog)

| 日期 | 变更内容 |
|------|----------|
| 2026-03-05 | 初始化模块文档 |