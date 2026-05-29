---
name: svelte-core
description: Svelte 核心基础技能，掌握组件编写、文件结构、项目启动和 Rune 概念，为深入学习 Svelte 打下坚实基础
---

# Svelte Core

## 任务目标
- 本 Skill 用于：掌握 Svelte 核心概念和组件基础
- 能力包含：.svelte 文件结构、项目创建、Rune 概念理解
- 触发条件：需要创建 Svelte 组件或初始化 Svelte 项目时

## 前置准备
- Node.js 18+ 环境
- npm/pnpm/bun 包管理器

## 操作步骤

### 创建 SvelteKit 项目
```bash
npx sv create myapp
cd myapp
npm install
npm run dev
```

### 使用 Vite 独立模式
```bash
npm create vite@latest myapp -- --template svelte
```

### .svelte 文件结构
```svelte
<script module>
  // 模块级逻辑（仅执行一次）
  let total = 0;
</script>

<script>
  // 实例级逻辑（每个组件实例执行）
  let count = $state(0);
</script>

<!-- 模板标记 -->
<div>{count}</div>

<style>
  /* 作用域样式 */
  div { color: blue; }
</style>
```

### Rune 概念
Rune 是 Svelte 5 引入的编译器指令，以 `$` 前缀标识：
- `$state` - 声明响应式状态
- `$derived` - 声明派生状态
- `$effect` - 声明副作用
- `$props` - 声明组件属性

## 资源索引
- 官方文档：https://svelte.dev/docs/svelte/overview
- 入门指南：https://svelte.dev/docs/svelte/getting-started
- Svelte 文件：https://svelte.dev/docs/svelte/svelte-files
- JS/TS 文件：https://svelte.dev/docs/svelte/svelte-js-files
- Rune 概念：https://svelte.dev/docs/svelte/what-are-runes

## 注意事项
- .svelte 文件中 script、style 和 markup 三部分都是可选的
- `<script module>` 中的代码仅在模块首次加载时执行一次
- Rune 无需导入，直接在 .svelte 和 .svelte.js/.svelte.ts 文件中使用
