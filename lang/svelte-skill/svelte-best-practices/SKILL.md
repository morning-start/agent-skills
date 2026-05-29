---
name: svelte-best-practices
description: Svelte 最佳实践技能，掌握测试、TypeScript 集成、迁移指南和常见问题解答，编写高质量 Svelte 应用
---

# Svelte Best Practices

## 任务目标
- 本 Skill 用于：遵循 Svelte 最佳实践，编写高质量代码
- 能力包含：测试策略、TypeScript 集成、版本迁移、FAQ
- 触发条件：需要编写测试、配置 TypeScript 或迁移 Svelte 版本时

## 操作步骤

### $state 最佳实践
```svelte
<script>
  // 仅对需要响应式的变量使用 $state
  let count = $state(0);

  // 大对象使用 $state.raw 优化性能
  let apiData = $state.raw({});
</script>
```

### $derived 优于 $effect
```svelte
<script>
  // 推荐：使用派生
  let doubled = $derived(count * 2);

  // 避免：使用效果同步状态
  let doubled;
  $effect(() => {
    doubled = count * 2;
  });
</script>
```

### 事件处理
```svelte
<!-- 推荐：使用事件属性 -->
<button onclick={handleClick}>点击</button>

<!-- 避免：使用旧的 on: 指令 -->
<button on:click={handleClick}>点击</button>
```

### Props 处理
```svelte
<script>
  // 推荐：基于 props 的派生值
  let { type } = $props();
  let color = $derived(type === 'danger' ? 'red' : 'green');
</script>

<!-- 避免：非响应式赋值 -->
<script>
  let { type } = $props();
  let color = type === 'danger' ? 'red' : 'green';
</script>
```

### 调试工具
```svelte
<script>
  let count = $state(0);

  // 追踪依赖
  $effect(() => {
    $inspect.trace();
    doSomeWork();
  });
</script>
```

### 测试配置 (Vitest)
```javascript
// vite.config.js
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'jsdom'
  },
  resolve: process.env.VITEST ? {
    conditions: ['browser']
  } : undefined
});
```

### 组件测试
```javascript
import { mount, unmount, flushSync } from 'svelte';
import { expect, test } from 'vitest';
import Component from './Component.svelte';

test('Component', () => {
  const target = document.body;
  const component = mount(Component, { target, props: { initial: 0 } });

  expect(document.body.innerHTML).toBe('<button>0</button>');

  document.body.querySelector('button').click();
  flushSync();

  expect(document.body.innerHTML).toBe('<button>1</button>');

  unmount(component);
});
```

### TypeScript 配置
```javascript
// svelte.config.js
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

export default {
  preprocess: vitePreprocess({ script: true })
};
```

### TypeScript Props
```svelte
<script lang="ts">
  import type { Snippet } from 'svelte';

  interface Props {
    required: number;
    optional?: boolean;
    children: Snippet;
  }

  let { required, optional = false, children }: Props = $props();
</script>
```

### 泛型组件
```svelte
<script lang="ts" generics="T extends { text: string }">
  interface Props {
    items: T[];
    select(item: T): void;
  }

  let { items, select }: Props = $props();
</script>
```

## Svelte 4 到 Svelte 5 迁移要点

### let → $state
```svelte
<!-- Svelte 4 -->
<script>
  let count = 0;
</script>

<!-- Svelte 5 -->
<script>
  let count = $state(0);
</script>
```

### $: → $derived/$effect
```svelte
<!-- Svelte 4 -->
<script>
  $: doubled = count * 2;
</script>

<!-- Svelte 5 -->
<script>
  let doubled = $derived(count * 2);
</script>
```

### export let → $props
```svelte
<!-- Svelte 4 -->
<script>
  export let name;
</script>

<!-- Svelte 5 -->
<script>
  let { name } = $props();
</script>
```

### on:click → onclick
```svelte
<!-- Svelte 4 -->
<button on:click={handleClick}>点击</button>

<!-- Svelte 5 -->
<button onclick={handleClick}>点击</button>
```

### slot → snippet
```svelte
<!-- Svelte 4 -->
<slot />

<!-- Svelte 5 -->
<script>
  let { children } = $props();
</script>
{@render children?.()}
```

### createEventDispatcher → callback props
```svelte
<!-- Svelte 4 -->
<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();
  dispatch('change', value);
</script>

<!-- Svelte 5 -->
<script>
  let { onchange } = $props();
  onchange?.(value);
</script>
```

## 资源索引
- 最佳实践：https://svelte.dev/docs/svelte/best-practices
- 测试：https://svelte.dev/docs/svelte/testing
- TypeScript：https://svelte.dev/docs/svelte/typescript
- V5 迁移指南：https://svelte.dev/docs/svelte/v5-migration-guide
- V4 迁移指南：https://svelte.dev/docs/svelte/v4-migration-guide
- FAQ：https://svelte.dev/docs/svelte/faq

## 注意事项
- 优先使用 runes（$state, $derived, $effect）而非旧语法
- 避免在 $effect 中更新状态
- 使用 keyed each 块提高列表渲染性能
- 使用 Context 而非全局模块状态防止 SSR 数据泄露
