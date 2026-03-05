[根目录](../../../CLAUDE.md) > **src** > **components**

# Components 组件模块文档

> 最后更新: 2026-03-05

## 模块职责

提供应用通用组件，按功能分类：
- **advanced** - 高级业务组件
- **common** - 公共基础组件
- **custom** - 自定义特殊组件

## 目录结构

```
components/
├── advanced/           # 高级组件
│   ├── table-column-setting.vue    # 表格列配置
│   └── table-header-operation.vue  # 表格头部操作
├── common/             # 公共组件
│   ├── app-provider.vue           # 应用 Provider
│   ├── dark-mode-container.vue    # 暗黑模式容器
│   ├── exception-base.vue         # 异常页面基类
│   ├── full-screen.vue            # 全屏切换
│   ├── icon-tooltip.vue           # 图标提示
│   ├── lang-switch.vue            # 语言切换
│   ├── menu-toggler.vue           # 菜单折叠
│   ├── pin-toggler.vue            # 标签固定
│   ├── reload-button.vue          # 刷新按钮
│   ├── system-logo.vue            # 系统 Logo
│   └── theme-schema-switch.vue    # 主题切换
└── custom/             # 自定义组件
    ├── better-scroll.vue          # 滚动容器
    ├── button-icon.vue            # 图标按钮
    ├── count-to.vue               # 数字滚动
    ├── look-forward.vue           # 敬请期待
    ├── soybean-avatar.vue         # 用户头像
    ├── svg-icon.vue               # SVG 图标
    └── wave-bg.vue                # 波浪背景
```

## 对外接口

### 组件自动注册

项目使用 `unplugin-vue-components` 自动注册组件，无需手动导入。

```vue
<template>
  <!-- 直接使用，无需 import -->
  <SystemLogo />
  <DarkModeContainer>
    content
  </DarkModeContainer>
</template>
```

### 主要组件说明

#### app-provider

应用全局 Provider，提供 NaiveUI 主题和消息注入。

```vue
<AppProvider>
  <router-view />
</AppProvider>
```

#### dark-mode-container

根据主题模式自动切换样式。

```vue
<DarkModeContainer class="custom">
  内容
</DarkModeContainer>
```

#### svg-icon

SVG 图标组件，支持本地和远程图标。

```vue
<!-- 本地图标 -->
<SvgIcon local-icon="logo" />

<!-- 远程图标（Iconify） -->
<SvgIcon icon="mdi:home" />
```

#### count-to

数字滚动动画组件。

```vue
<CountTo :end-value="1000" :duration="2000" />
```

## 关键依赖与配置

### 自动导入配置

```typescript
// build/plugins/unplugin.ts
Components({
  dts: 'src/typings/components.d.ts',
  extensions: ['vue'],
  include: [/\.vue$/, /\.vue\?vue/],
  resolvers: []
})
```

### 类型定义

组件类型自动生成到 `src/typings/components.d.ts`。

## 测试与质量

- 未配置组件单元测试
- 建议补充组件快照测试

## 常见问题 (FAQ)

**Q: 如何添加新组件？**
在对应目录创建 `.vue` 文件，组件会自动注册。

**Q: 为什么组件名必须大写？**
ESLint 规则要求模板中使用 PascalCase。

## 相关文件清单

| 文件 | 说明 |
|------|------|
| `src/typings/components.d.ts` | 组件类型定义（自动生成） |
| `advanced/*.vue` | 高级业务组件 |
| `common/*.vue` | 公共基础组件 |
| `custom/*.vue` | 自定义组件 |

---

## 变更记录 (Changelog)

| 日期 | 变更内容 |
|------|----------|
| 2026-03-05 | 初始化模块文档 |