# 框架配置指南

本指南提供 WXT 支持的 5 个框架（Vanilla、Vue、React、Svelte、Solid）的完整配置方法、示例代码和最佳实践。

## 官方导航链接

- [Frontend Frameworks](https://wxt.dev/guide/essentials/frontend-frameworks.html) - 前端框架集成完整指南
- [Vue](https://wxt.dev/guide/frontend-frameworks/vue.html) - Vue 框架集成
- [React](https://wxt.dev/guide/frontend-frameworks/react.html) - React 框架集成
- [Svelte](https://wxt.dev/guide/frontend-frameworks/svelte.html) - Svelte 框架集成
- [Solid](https://wxt.dev/guide/frontend-frameworks/solid.html) - Solid 框架集成

---

## 框架概览

| 框架 | 推荐度 | 特点 | 学习曲线 | 包大小 |
|------|--------|------|----------|--------|
| **Svelte** | ⭐⭐⭐⭐⭐ | 轻量、高性能、编译时优化 | 平缓 | 最小 |
| **Solid** | ⭐⭐⭐⭐⭐ | 细粒度响应式、高性能 | 中等 | 小 |
| **Vue** | ⭐⭐⭐⭐ | 生态成熟、渐进式框架 | 平缓 | 中等 |
| **React** | ⭐⭐⭐⭐ | 生态庞大、虚拟 DOM | 陡峭 | 中等 |
| **Vanilla** | ⭐⭐⭐ | 无框架、简单直接 | 平缓 | 最小 |

## 一、Svelte（强烈推荐）

Svelte 是一个编译型框架，在构建时生成高效的 Vanilla JavaScript，非常适合浏览器扩展。

### 1.1 初始化 Svelte 项目

**方式一：使用 WXT 初始化（推荐）**

```bash
bunx wxt@latest init
```

选择模板时选择 **Svelte**。

**方式二：手动创建**

```bash
# 创建项目
mkdir my-extension
cd my-extension

# 初始化 package.json
bun init

# 安装 WXT 和 Svelte 依赖
bun i -D wxt svelte @sveltejs/vite-plugin-svelte

# 创建项目结构
mkdir -p entrypoints/popup src/components
```

### 1.2 安装依赖

**完整依赖列表：**

```bash
bun i -D \
  wxt \
  svelte \
  @sveltejs/vite-plugin-svelte \
  svelte-preprocess \
  typescript \
  @tsconfig/svelte
```

### 1.3 配置 wxt.config.ts

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  modules: ['@wxt-dev/module-svelte'],
});
```

### 1.4 配置 tsconfig.json

```json
{
  "extends": "@tsconfig/svelte/tsconfig.json",
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "lib": ["ESNext", "DOM"],
    "strict": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "types": ["wxt/client-types"]
  },
  "include": ["**/*.ts", "**/*.svelte", "wxt.config.ts"]
}
```

### 1.5 创建 Svelte 入口点

**弹出页面入口点（popup.html）：**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Popup</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="./popup.ts"></script>
</body>
</html>
```

**弹出页面逻辑（popup.ts）：**

```typescript
import App from './App.svelte';

const app = new App({
  target: document.getElementById('app')!,
});

export default app;
```

**弹出页面组件（App.svelte）：**

```svelte
<script lang="ts">
  let count = 0;

  function increment() {
    count += 1;
  }

  function decrement() {
    count -= 1;
  }
</script>

<main>
  <h1>Svelte Counter</h1>
  <p>Count: {count}</p>
  <button on:click={increment}>+</button>
  <button on:click={decrement}>-</button>
</main>

<style>
  main {
    padding: 1rem;
    font-family: system-ui, sans-serif;
  }

  h1 {
    margin: 0 0 1rem 0;
    font-size: 1.5rem;
  }

  p {
    margin: 1rem 0;
    font-size: 1.2rem;
  }

  button {
    padding: 0.5rem 1rem;
    margin: 0 0.5rem;
    border: none;
    border-radius: 4px;
    background: #3b82f6;
    color: white;
    cursor: pointer;
  }

  button:hover {
    background: #2563eb;
  }
</style>
```

### 1.6 使用 Svelte Store

**创建 store（src/store.ts）：**

```typescript
import { writable } from 'svelte/store';

export const count = writable(0);
```

**在组件中使用：**

```svelte
<script lang="ts">
  import { count } from '../store';

  function increment() {
    count.update(n => n + 1);
  }
</script>

<main>
  <p>Count: {$count}</p>
  <button on:click={increment}>Increment</button>
</main>
```

### 1.7 Svelte 最佳实践

**组件划分：**

```
src/
├── components/          # UI 组件
│   ├── Button.svelte
│   ├── Input.svelte
│   └── Card.svelte
├── features/           # 功能组件
│   ├── Counter/
│   │   ├── Counter.svelte
│   │   └── counterStore.ts
│   └── Theme/
│       └── Theme.svelte
└── lib/                # 工具函数
    ├── api.ts
    └── utils.ts
```

**类型定义：**

```typescript
// src/types.ts
export interface User {
  id: string;
  name: string;
  email: string;
}

export interface CounterState {
  value: number;
  max: number;
}
```

**完整示例：**查看 [Svelte 示例项目](../examples/svelte/)

---

## 二、Solid（强烈推荐）

SolidJS 是一个高性能的响应式框架，使用细粒度响应式系统，非常适合浏览器扩展。

### 2.1 初始化 Solid 项目

**方式一：使用 WXT 初始化（推荐）**

```bash
bunx wxt@latest init
```

选择模板时选择 **Solid**。

**方式二：手动创建**

```bash
# 创建项目
mkdir my-extension
cd my-extension

# 初始化 package.json
bun init

# 安装依赖
bun i -D wxt solid-js solid-styled-jsx babel-preset-solid

# 创建项目结构
mkdir -p entrypoints/popup src/components
```

### 2.2 安装依赖

```bash
bun i -D \
  wxt \
  solid-js \
  solid-styled-jsx \
  babel-preset-solid \
  typescript
```

### 2.3 配置 wxt.config.ts

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  modules: ['@wxt-dev/module-solid'],
});
```

### 2.4 配置 tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "lib": ["ESNext", "DOM", "DOM.Iterable"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "types": ["wxt/client-types"],
    "jsx": "preserve",
    "jsxImportSource": "solid-js"
  },
  "include": ["**/*.ts", "**/*.tsx", "wxt.config.ts"]
}
```

### 2.5 创建 Solid 入口点

**弹出页面入口点（popup.html）：**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Popup</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="./popup.tsx"></script>
</body>
</html>
```

**弹出页面逻辑（popup.tsx）：**

```typescript
import { render } from 'solid-js/web';
import App from './App';

render(() => <App />, document.getElementById('app')!);
```

**弹出页面组件（App.tsx）：**

```typescript
import { createSignal } from 'solid-js';

export default function App() {
  const [count, setCount] = createSignal(0);

  const increment = () => setCount(c => c + 1);
  const decrement = () => setCount(c => c - 1);

  return (
    <main>
      <h1>Solid Counter</h1>
      <p>Count: {count()}</p>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </main>
  );
}
```

### 2.6 使用 Solid Store

**创建 store（src/store.ts）：**

```typescript
import { createStore, produce } from 'solid-js/store';

export const [state, setState] = createStore({
  count: 0,
  user: null as { name: string } | null,
});

export function increment() {
  setState('count', c => c + 1);
}

export function decrement() {
  setState('count', c => c - 1);
}
```

**在组件中使用：**

```typescript
import { state, increment, decrement } from '../store';

export default function Counter() {
  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  );
}
```

### 2.7 Solid 最佳实践

**组件划分：**

```
src/
├── components/          # UI 组件
│   ├── Button.tsx
│   ├── Input.tsx
│   └── Card.tsx
├── features/           # 功能组件
│   ├── Counter/
│   │   ├── Counter.tsx
│   │   └── counterStore.ts
│   └── Theme/
│       └── Theme.tsx
└── lib/                # 工具函数
    ├── api.ts
    └── utils.ts
```

**完整示例：**查看 [Solid 示例项目](../examples/solid/)

---

## 三、Vue

Vue 是一个渐进式框架，适合对 Vue 生态熟悉的开发者。

### 3.1 初始化 Vue 项目

**方式一：使用 WXT 初始化（推荐）**

```bash
bunx wxt@latest init
```

选择模板时选择 **Vue**。

**方式二：手动创建**

```bash
# 创建项目
mkdir my-extension
cd my-extension

# 初始化 package.json
bun init

# 安装依赖
bun i -D wxt vue @vitejs/plugin-vue

# 创建项目结构
mkdir -p entrypoints/popup src/components
```

### 3.2 安装依赖

```bash
bun i -D \
  wxt \
  vue \
  @vitejs/plugin-vue \
  typescript
```

### 3.3 配置 wxt.config.ts

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  modules: ['@wxt-dev/module-vue'],
});
```

### 3.4 创建 Vue 入口点

**弹出页面入口点（popup.html）：**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Popup</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="./popup.ts"></script>
</body>
</html>
```

**弹出页面逻辑（popup.ts）：**

```typescript
import { createApp } from 'vue';
import App from './App.vue';

createApp(App).mount('#app');
```

**弹出页面组件（App.vue）：**

```vue
<script setup lang="ts">
import { ref } from 'vue';

const count = ref(0);

const increment = () => count.value++;
const decrement = () => count.value--;
</script>

<template>
  <main>
    <h1>Vue Counter</h1>
    <p>Count: {{ count }}</p>
    <button @click="increment">+</button>
    <button @click="decrement">-</button>
  </main>
</template>

<style>
  main {
    padding: 1rem;
    font-family: system-ui, sans-serif;
  }
</style>
```

### 3.5 使用 Pinia Store

**创建 store（src/store.ts）：**

```typescript
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0);

  function increment() {
    count.value++;
  }

  function decrement() {
    count.value--;
  }

  return { count, increment, decrement };
});
```

**在组件中使用：**

```vue
<script setup lang="ts">
import { useCounterStore } from '../store';

const counter = useCounterStore();
</script>

<template>
  <div>
    <p>Count: {{ counter.count }}</p>
    <button @click="counter.increment">+</button>
    <button @click="counter.decrement">-</button>
  </div>
</template>
```

**完整示例：**查看 [Vue 示例项目](../examples/vue/)

---

## 四、React

React 是最流行的前端框架，适合熟悉 React 生态的开发者。

### 4.1 初始化 React 项目

**方式一：使用 WXT 初始化（推荐）**

```bash
bunx wxt@latest init
```

选择模板时选择 **React**。

**方式二：手动创建**

```bash
# 创建项目
mkdir my-extension
cd my-extension

# 初始化 package.json
bun init

# 安装依赖
bun i -D wxt react react-dom @vitejs/plugin-react

# 创建项目结构
mkdir -p entrypoints/popup src/components
```

### 4.2 安装依赖

```bash
bun i -D \
  wxt \
  react \
  react-dom \
  @vitejs/plugin-react \
  typescript
```

### 4.3 配置 wxt.config.ts

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  modules: ['@wxt-dev/module-react'],
});
```

### 4.4 创建 React 入口点

**弹出页面入口点（popup.html）：**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Popup</title>
</head>
<body>
  <div id="root"></div>
  <script type="module" src="./popup.tsx"></script>
</body>
</html>
```

**弹出页面逻辑（popup.tsx）：**

```typescript
import { createRoot } from 'react-dom/client';
import App from './App';

const root = createRoot(document.getElementById('root')!);
root.render(<App />);
```

**弹出页面组件（App.tsx）：**

```typescript
import { useState } from 'react';

export default function App() {
  const [count, setCount] = useState(0);

  const increment = () => setCount(c => c + 1);
  const decrement = () => setCount(c => c - 1);

  return (
    <main>
      <h1>React Counter</h1>
      <p>Count: {count}</p>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </main>
  );
}
```

### 4.5 使用 Zustand Store

**创建 store（src/store.ts）：**

```typescript
import { create } from 'zustand';

interface CounterState {
  count: number;
  increment: () => void;
  decrement: () => void;
}

export const useCounterStore = create<CounterState>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
}));
```

**在组件中使用：**

```typescript
import { useCounterStore } from '../store';

export default function Counter() {
  const { count, increment, decrement } = useCounterStore();

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  );
}
```

**完整示例：**查看 [React 示例项目](../examples/react/)

---

## 五、Vanilla

Vanilla 适合简单项目或需要完全控制所有代码的开发者。

### 5.1 初始化 Vanilla 项目

**使用 WXT 初始化：**

```bash
bunx wxt@latest init
```

选择模板时选择 **Vanilla**。

### 5.2 创建 Vanilla 入口点

**弹出页面入口点（popup.html）：**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Popup</title>
</head>
<body>
  <h1>Vanilla Counter</h1>
  <p>Count: <span id="count">0</span></p>
  <button id="increment">+</button>
  <button id="decrement">-</button>
  <script type="module" src="./popup.ts"></script>
</body>
</html>
```

**弹出页面逻辑（popup.ts）：**

```typescript
let count = 0;

const countEl = document.getElementById('count')!;
const incrementBtn = document.getElementById('increment')!;
const decrementBtn = document.getElementById('decrement')!;

function updateCount() {
  countEl.textContent = count.toString();
}

incrementBtn.addEventListener('click', () => {
  count++;
  updateCount();
});

decrementBtn.addEventListener('click', () => {
  count--;
  updateCount();
});
```

### 5.3 模块化组织

**使用 ES Modules：**

```typescript
// src/store.ts
export const store = {
  state: {
    count: 0,
  },
  methods: {
    increment() {
      this.state.count++;
    },
    decrement() {
      this.state.count--;
    },
  },
};

// src/ui.ts
export function createCounter() {
  const container = document.createElement('div');
  container.innerHTML = `
    <p>Count: <span id="count">0</span></p>
    <button id="increment">+</button>
    <button id="decrement">-</button>
  `;
  return container;
}
```

**完整示例：**查看 [Vanilla 示例项目](../examples/vanilla/)

---

## 六、框架选择建议

### 6.1 推荐场景

| 场景 | 推荐框架 | 原因 |
|------|----------|------|
| 新手入门 | Svelte | 学习曲线平缓，编译时优化，性能优异 |
| 性能优先 | Solid | 细粒度响应式，性能最佳 |
| Vue 经验 | Vue | 生态成熟，渐进式框架，中文文档丰富 |
| React 经验 | React | 生态庞大，就业机会多 |
| 简单项目 | Vanilla | 无框架依赖，代码简洁 |

### 6.2 性能对比

| 指标 | Svelte | Solid | Vue | React | Vanilla |
|------|--------|-------|-----|-------|---------|
| 包大小 | 最小 | 小 | 中等 | 中等 | 最小 |
| 运行时 | 无 | 极小 | 中等 | 大 | 无 |
| 首次渲染 | 快 | 极快 | 快 | 中等 | 最快 |
| 更新性能 | 快 | 极快 | 快 | 中等 | 最快 |

### 6.3 学习曲线

| 框架 | 学习时间 | 概念复杂度 | 生态规模 |
|------|----------|------------|----------|
| Svelte | 1-2 周 | 低 | 中等 |
| Solid | 2-3 周 | 中等 | 中等 |
| Vue | 1-2 周 | 低 | 大 |
| React | 2-4 周 | 高 | 极大 |
| Vanilla | 1 周 | 低 | 无 |

---

## 七、通用最佳实践

### 7.1 组件设计

**单一职责原则：**

```typescript
// ✅ 好的设计
export function Button({ onClick, children }: ButtonProps) {
  return <button onClick={onClick}>{children}</button>;
}

// ❌ 不好的设计
export function Button({ onClick, children, user, api }: ComplexProps) {
  // 负责太多逻辑
}
```

### 7.2 状态管理

**小项目：**

- Svelte：使用 `writable` store
- Solid：使用 `createStore`
- Vue：使用 `ref` / `reactive`
- React：使用 `useState`

**中大型项目：**

- Svelte：使用 `svelte/store`
- Solid：使用 `solid-js/store`
- Vue：使用 Pinia
- React：使用 Zustand 或 Redux Toolkit

### 7.3 代码复用

**组合式函数 / Hooks：**

```typescript
// Svelte
export function useCounter(initial = 0) {
  const count = writable(initial);
  return {
    count,
    increment: () => count.update(n => n + 1),
    decrement: () => count.update(n => n - 1),
  };
}

// Solid
export function useCounter(initial = 0) {
  const [count, setCount] = createSignal(initial);
  return {
    count,
    increment: () => setCount(c => c + 1),
    decrement: () => setCount(c => c - 1),
  };
}

// Vue
export function useCounter(initial = 0) {
  const count = ref(initial);
  return {
    count,
    increment: () => count.value++,
    decrement: () => count.value--,
  };
}

// React
export function useCounter(initial = 0) {
  const [count, setCount] = useState(initial);
  return {
    count,
    increment: () => setCount(c => c + 1),
    decrement: () => setCount(c => c - 1),
  };
}
```

### 7.4 类型安全

**TypeScript 配置：**

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitAny": true,
    "noImplicitReturns": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

---

## 八、常见问题

### Q1: 如何切换框架？

**方法一：手动迁移**

1. 备份现有项目
2. 删除 `node_modules` 和 `package-lock.json`
3. 卸载旧框架依赖，安装新框架依赖
4. 更新配置文件
5. 逐个迁移组件

**方法二：创建新项目**

```bash
# 创建新项目
bunx wxt@latest init

# 选择新框架

# 复制业务逻辑（不包含框架特定代码）
cp -r old-project/src/new-project/src/
```

### Q2: 框架会影响性能吗？

所有框架都会产生一定的性能开销：

- **Svelte**：编译时优化，运行时开销最小
- **Solid**：细粒度响应式，性能最佳
- **Vue / React**：虚拟 DOM，有一定的运行时开销
- **Vanilla**：无框架，性能最佳

对于浏览器扩展，建议选择 Svelte 或 Solid 以获得最佳性能。

### Q3: 可以混用多个框架吗？

**技术上可以，但不推荐：**

- 增加包大小
- 增加构建时间
- 代码维护困难
- 可能产生兼容性问题

**正确做法：**在扩展中统一使用一个框架，在不同入口点之间共享代码。

### Q4: 如何处理跨框架代码复用？

使用 TypeScript 接口定义公共 API：

```typescript
// src/types.ts
export interface CounterStore {
  count: number;
  increment(): void;
  decrement(): void;
}

// 每个框架实现自己的 store，但遵循相同的接口
```

---

## 九、下一步

- [部署指南](./deployment.md)：学习如何构建和发布扩展
- [命令参考](../cli/commands.md)：掌握开发命令
- [构建阶段](../lifecycle/phases.md)：了解构建流程
- [示例代码](../examples/)：查看完整项目示例
- [入口点 API](../api/entrypoints.md)：学习核心 API
