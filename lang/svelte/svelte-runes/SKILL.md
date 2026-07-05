---
name: svelte-runes
description: Svelte 5 Runes 系统技能，掌握 $state、$derived、$effect、$props 等响应式原语，实现组件状态管理和副作用处理
---

# Svelte Runes

## 任务目标
- 本 Skill 用于：使用 Runes 系统管理 Svelte 组件的状态和副作用
- 能力包含：响应式状态、派生计算、副作用执行、属性声明
- 触发条件：需要创建响应式状态、同步计算值或处理副作用时

## 操作步骤

### $state - 响应式状态
```svelte
<script>
  let count = $state(0);
  let user = $state({ name: 'John', age: 30 });
</script>

<button onclick={() => count++}>{count}</button>
```

### $state.raw - 浅层响应式
```svelte
<script>
  let data = $state.raw({ items: [] });
  // data.items.push() 不会触发更新
  data = { items: [1,2,3] }; // 需要整体替换
</script>
```

### $derived - 派生状态
```svelte
<script>
  let count = $state(0);
  let doubled = $derived(count * 2);
</script>

<p>{count} x 2 = {doubled}</p>
```

### $derived.by - 复杂派生
```svelte
<script>
  let numbers = $state([1, 2, 3]);
  let total = $derived.by(() => {
    return numbers.reduce((sum, n) => sum + n, 0);
  });
</script>
```

### $effect - 副作用
```svelte
<script>
  let canvas;
  let color = $state('#ff3e00');

  $effect(() => {
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = color;
    ctx.fillRect(0, 0, 100, 100);
  });
</script>

<canvas bind:this={canvas}></canvas>
```

### $effect 返回清理函数
```svelte
<script>
  let milliseconds = $state(1000);
  let count = $state(0);

  $effect(() => {
    const interval = setInterval(() => count++, milliseconds);
    return () => clearInterval(interval);
  });
</script>
```

### $props - 组件属性
```svelte
<script>
  let { name, age = 18 } = $props();
</script>

<p>{name}, {age}</p>
```

### $bindable - 可绑定属性
```svelte
<script>
  let { value = $bindable() } = $props();
</script>

<input bind:value />
```

### $inspect - 调试响应式
```svelte
<script>
  let count = $state(0);
  $inspect(count).with((type, val) => {
    if (type === 'update') console.log('changed to', val);
  });
</script>
```

## 资源索引
- $state：https://svelte.dev/docs/svelte/$state
- $derived：https://svelte.dev/docs/svelte/$derived
- $effect：https://svelte.dev/docs/svelte/$effect
- $props：https://svelte.dev/docs/svelte/$props
- $bindable：https://svelte.dev/docs/svelte/$bindable
- $inspect：https://svelte.dev/docs/svelte/$inspect
- $host：https://svelte.dev/docs/svelte/$host

## 注意事项
- $derived 表达式不应有副作用
- $effect 仅在浏览器运行，不参与 SSR
- 避免在 $effect 中更新状态，优先使用 $derived
- $state 深层代理数组和普通对象，类实例不会被代理
