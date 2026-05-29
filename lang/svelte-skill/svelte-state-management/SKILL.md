---
name: svelte-state-management
description: Svelte 状态管理技能，掌握 Stores 和 Context API，实现跨组件状态共享和依赖注入
---

# Svelte State Management

## 任务目标
- 本 Skill 用于：管理跨组件共享状态
- 能力包含：Store 创建与使用、Context 上下文、响应式状态导出
- 触发条件：需要在多个组件间共享状态时

## 操作步骤

### 使用 Stores

#### 创建 Writable Store
```javascript
import { writable } from 'svelte/store';

export const count = writable(0);

count.subscribe(value => console.log(value));
count.set(1);
count.update(n => n + 1);
```

#### 创建 Readable Store
```javascript
import { readable } from 'svelte/store';

const time = readable(new Date(), (set) => {
  const interval = setInterval(() => set(new Date()), 1000);
  return () => clearInterval(interval);
});
```

#### 创建 Derived Store
```javascript
import { derived } from 'svelte/store';

const doubled = derived(count, $count => $count * 2);

const summed = derived([a, b], ([$a, $b]) => $a + $b);
```

#### 在组件中使用
```svelte
<script>
  import { count } from './stores';
</script>

<p>计数: {$count}</p>
<button onclick={() => $count++}>+1</button>
```

### 使用 Context

#### 创建 Context
```javascript
// context.js
import { createContext } from 'svelte';

export const [getUserContext, setUserContext] = createContext();
```

#### 设置 Context
```svelte
<!-- Parent.svelte -->
<script>
  import { setUserContext } from './context';
  setUserContext({ name: 'Alice' });
</script>
```

#### 获取 Context
```svelte
<!-- Child.svelte -->
<script>
  import { getUserContext } from './context';
  const user = getUserContext();
</script>

<p>你好, {user.name}</p>
```

### 使用 setContext/getContext
```svelte
<script>
  import { setContext, getContext } from 'svelte';

  setContext('theme', 'dark');
  const theme = getContext('theme');
</script>
```

### 响应式状态对象
```javascript
// state.svelte.js
export const userState = $state({
  name: 'John',
  age: 30
});
```

```svelte
<script>
  import { userState } from './state.svelte.js';
</script>

<p>{userState.name}</p>
<button onclick={() => userState.age++}>长大</button>
```

## 资源索引
- Stores：https://svelte.dev/docs/svelte/stores
- Context：https://svelte.dev/docs/svelte/context

## 注意事项
- $ 前缀的 store 变量会在组件初始化时自动订阅
- Context 在组件树中是键值对存储
- createContext 提供更好的类型安全
- 避免在 SSR 时使用全局模块状态，使用 Context
