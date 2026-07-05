---
name: svelte-legacy
description: Svelte 4 遗留语法技能，掌握旧版 API 包括 export let、$: 反应式语句、slot、createEventDispatcher 等，确保向后兼容
---

# Svelte Legacy (Svelte 4 语法)

## 任务目标
- 本 Skill 用于：理解和维护使用 Svelte 4 语法的遗留代码
- 能力包含：旧版 props、反应式声明、slot、事件派发等
- 触发条件：需要维护 Svelte 4 项目或迁移旧代码时

## 操作步骤

### export let - 属性导出
```svelte
<!-- Svelte 4 -->
<script>
  export let name = 'default';
  export let count;
</script>

<p>{name}: {count}</p>
```

### $: 反应式声明
```svelte
<!-- Svelte 4 -->
<script>
  let count = 0;
  $: doubled = count * 2;
  $: console.log('count changed', count);
</script>
```

### $$props - 所有属性
```svelte
<!-- Svelte 4 -->
<script>
  export let name;
  let { ...rest } = $$props;
</script>

<div {...rest}>{name}</div>
```

### $$restProps - 剩余属性
```svelte
<!-- Svelte 4 -->
<script>
  export let name;
  let { class: className, ...rest } = $$restProps;
</script>

<div class={className} {...rest}>{name}</div>
```

### on: 事件指令
```svelte
<!-- Svelte 4 -->
<button on:click={handleClick}>点击</button>
<button on:click|once|preventDefault={handleClick}>点击</button>
```

### 事件修饰符
```svelte
<button on:click|stopPropagation|preventDefault={handler}>
  点击
</button>
```

### createEventDispatcher - 事件派发
```svelte
<!-- Svelte 4 -->
<script>
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  function send() {
    dispatch('message', { text: 'hello' });
  }
</script>
```

```svelte
<!-- 监听事件 -->
<Child on:message={handleMessage} />
```

### slot - 插槽

#### 默认插槽
```svelte
<!-- Child.svelte -->
<slot />

<!-- Parent.svelte -->
<Child>
  <p>插槽内容</p>
</Child>
```

#### 命名插槽
```svelte
<!-- Child.svelte -->
<slot name="header" />
<slot name="footer" />

<!-- Parent.svelte -->
<Child>
  <p slot="header">头部</p>
  <p slot="footer">底部</p>
</Child>
```

#### 插槽属性
```svelte
<!-- Child.svelte -->
<slot value={currentValue} />

<!-- Parent.svelte -->
<Child let:value>
  <p>{value}</p>
</Child>
```

### $$slots - 插槽访问
```svelte
<script>
  export let name;
</script>

{#if $$slots.default}
  <div>
    <slot />
  </div>
{/if}

{#if $$slots.header}
  <slot name="header" />
{/if}
```

### svelte:component - 动态组件
```svelte
<!-- Svelte 4 -->
<script>
  import A from './A.svelte';
  import B from './B.svelte';

  let Current = A;
</script>

<svelte:component this={Current} />
```

### svelte:self - 递归组件
```svelte
<!-- Svelte 4 -->
<script>
  import Self from './Self.svelte';
</script>

{#if count > 0}
  <Self />
{/if}
```

### svelte:fragment - 片段占位
```svelte
<!-- Child.svelte -->
<svelte:fragment slot="items">
  <div>item</div>
</svelte:fragment>
```

### beforeUpdate / afterUpdate
```svelte
<script>
  import { beforeUpdate, afterUpdate } from 'svelte';

  let message = '';

  beforeUpdate(() => {
    message = '更新前';
  });

  afterUpdate(() => {
    message = '更新后';
  });
</script>
```

### onMount / onDestroy
```svelte
<script>
  import { onMount, onDestroy } from 'svelte';

  onMount(() => {
    console.log('mounted');
    return () => console.log('unmounted');
  });

  onDestroy(() => {
    console.log('destroyed');
  });
</script>
```

### run 函数 (迁移辅助)
```svelte
<!-- 迁移脚本生成的代码 -->
<script>
  import { run } from 'svelte/legacy';

  run(() => {
    // 原 $: 语句内容
  });
</script>
```

## 生命周期对比

| Svelte 4 | Svelte 5 |
|----------|----------|
| `export let` | `let { } = $props()` |
| `$:` | `$derived` / `$effect` |
| `on:event` | `onevent` |
| `createEventDispatcher` | callback props |
| `<slot>` | `{#snippet}` / `{@render}` |
| `beforeUpdate` | `$effect.pre` |
| `afterUpdate` | `$effect` |
| `$$restProps` | `...rest` |
| `<svelte:component>` | 直接组件变量 |

## 资源索引
- Legacy Overview：https://svelte.dev/docs/svelte/legacy-overview
- Reactive let：https://svelte.dev/docs/svelte/legacy-let
- Reactive $:：https://svelte.dev/docs/svelte/legacy-reactive-assignments
- export let：https://svelte.dev/docs/svelte/legacy-export-let
- $$props：https://svelte.dev/docs/svelte/legacy-$$props-and-$$restProps
- on: 指令：https://svelte/docs/svelte/legacy-on
- slot：https://svelte.dev/docs/svelte/legacy-slots
- $$slots：https://svelte.dev/docs/svelte/legacy-$$slots
- svelte:component：https://svelte.dev/docs/svelte/legacy-svelte-component
- svelte:self：https://svelte.dev/docs/svelte/legacy-svelte-self
- svelte:fragment：https://svelte.dev/docs/svelte/legacy-svelte-fragment
- Component API：https://svelte.dev/docs/svelte/legacy-component-api

## 注意事项
- Svelte 5 支持混用新旧语法
- 新项目应优先使用 runes
- 迁移脚本可自动处理大部分转换
- createEventDispatcher 需要手动迁移
