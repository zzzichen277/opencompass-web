[根目录](../../CLAUDE.md) > **packages** > **materials**

# @sa/materials 模块文档

> 最后更新: 2026-03-05

## 模块职责

提供后台管理系统的核心 UI 组件，包括：
- AdminLayout：后台布局容器
- PageTab：页面标签组件
- SimpleScrollbar：简化滚动条组件

## 入口与启动

**入口文件**: `src/index.ts`

```typescript
export { AdminLayout, LAYOUT_SCROLL_EL_ID, LAYOUT_MAX_Z_INDEX, PageTab, SimpleScrollbar };
```

## 对外接口

### AdminLayout

后台管理布局容器组件，支持多种布局模式。

```vue
<template>
  <AdminLayout>
    <!-- 页面内容 -->
  </AdminLayout>
</template>
```

**Props**:
- `mode` - 布局模式（vertical/horizontal/等）
- `fixedHeader` - 固定头部
- `fixedSider` - 固定侧边栏

**导出常量**:
- `LAYOUT_SCROLL_EL_ID` - 布局滚动元素 ID
- `LAYOUT_MAX_Z_INDEX` - 布局最大 z-index

### PageTab

页面标签组件，支持多种样式（Chrome 风格、按钮风格）。

```vue
<template>
  <PageTab :tab="tab" :active="isActive" @click="handleClick" />
</template>
```

**Props**:
- `tab` - 标签数据对象
- `active` - 是否激活
- `mode` - 标签样式模式

### SimpleScrollbar

简化滚动条组件。

```vue
<template>
  <SimpleScrollbar>
    <!-- 滚动内容 -->
  </SimpleScrollbar>
</template>
```

## 关键依赖与配置

### 依赖

| 包名 | 用途 |
|------|------|
| `vue` | Vue 3 框架 |
| `@sa/color` | 颜色处理 |

## 数据模型

```typescript
// 标签数据
interface Tab {
  id: string;
  label: string;
  routeKey: RouteKey;
  routePath: RoutePath;
  fullPath: string;
  icon?: string;
  fixedIndex?: number | null;
}

// 布局模式
type LayoutMode = 'vertical' | 'vertical-mix' | 'horizontal' | 'horizontal-mix';
```

## 测试与质量

- 未配置单元测试
- 使用 CSS Modules 管理样式

## 常见问题 (FAQ)

**Q: 如何自定义布局滚动？**
使用 `LAYOUT_SCROLL_EL_ID` 获取滚动元素进行操作。

**Q: 如何切换标签样式？**
通过 `mode` 属性切换：`chrome` | `button`

## 相关文件清单

| 文件 | 说明 |
|------|------|
| `src/index.ts` | 主入口 |
| `src/libs/admin-layout/index.ts` | 布局组件 |
| `src/libs/admin-layout/index.vue` | 布局 Vue 组件 |
| `src/libs/admin-layout/shared.ts` | 布局共享逻辑 |
| `src/libs/page-tab/index.ts` | 标签组件入口 |
| `src/libs/page-tab/*.vue` | 标签样式组件 |
| `src/libs/simple-scrollbar/index.ts` | 滚动条组件 |
| `src/types/index.ts` | 类型定义 |

---

## 变更记录 (Changelog)

| 日期 | 变更内容 |
|------|----------|
| 2026-03-05 | 初始化模块文档 |