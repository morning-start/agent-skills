---
name: svelte-lifecycle
description: Svelte 生命周期技能，掌握组件挂载、销毁、tick 等钩子，实现组件生命周期管理和 DOM 操作
---

# Svelte Lifecycle

## 任务目标
- 本 Skill 用于：管理 Svelte 组件的生命周期
- 能力包含：挂载/销毁钩子、tick、命令式组件 API
- 触发条件：需要在组件生命周期特定阶段执行代码时

## 操作步骤

### onMount - 挂载钩子
```svelte
<script>
  import { onMount } from 'svelte';

  onMount(() => {
    console.log('组件已挂载');
    return () => console.log('组件将销毁');
  });
</script>
```

### onDestroy - 销毁钩子
```svelte
<script>
  import { onDestroy } from 'svelte';

  onDestroy(() => {
    console.log('组件正在销毁');
  });
</script>
```

### tick - DOM 更新同步
```svelte
<script>
  import { tick } from 'svelte';

  async function updateAndLog() {
    count = 10;
    await tick();
    console.log('DOM 已更新');
  }
</script>
```

### $effect.pre - 预更新效果
```svelte
<script>
  import { tick } from 'svelte';

  let messages = $state([]);
  let div;

  $effect.pre(() => {
    if (!div) return;
    messages.length; // 依赖追踪
    if (div.offsetHeight + div.scrollTop > div.scrollHeight - 50) {
      tick().then(() => div.scrollTo(0, div.scrollHeight));
    }
  });
</script>

<div bind:this={div}>
  {#each messages as msg}
    <p>{msg}</p>
  {/each}
</div>
```

### $effect.root - 根效果
```svelte
<script>
  import { flushSync } from 'svelte';

  const cleanup = $effect.root(() => {
    let count = $state(0);

    $effect(() => {
      console.log('count:', count);
    });

    return () => console.log('root cleanup');
  });

  cleanup();
</script>
```

### 命令式组件挂载
```javascript
import { mount } from 'svelte';
import App from './App.svelte';

const app = mount(App, {
  target: document.getElementById('app'),
  props: { name: 'World' }
});
```

### 命令式组件卸载
```javascript
import { mount, unmount } from 'svelte';

const app = mount(App, { target: document.body });
unmount(app);
```

### SSR 渲染
```javascript
import { render } from 'svelte/server';
import App from './App.svelte';

const { html, head } = render(App, {
  props: { name: 'World' }
});
```

### Hydratable 数据
```svelte
<script>
  let { data } = $props();
</script>

<!-- 数据在服务端序列化和客户端水合 -->
<p>{data.content}</p>
```

## 资源索引
- 生命周期钩子：https://svelte.dev/docs/svelte/lifecycle-hooks
- 命令式组件 API：https://svelte.dev/docs/svelte/imperative-component-api
- Hydratable：https://svelte.dev/docs/svelte/hydratable

## 注意事项
- onMount 不在服务端执行
- onDestroy 在服务端也可以执行
- $effect 在 DOM 更新后执行，$effect.pre 在更新前
- $effect.root 用于在组件外创建响应式作用域
