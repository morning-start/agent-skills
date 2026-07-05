---
name: svelte-control-flow
description: Svelte 控制流技能，掌握条件渲染、列表渲染、异步处理和代码片段，实现复杂的组件逻辑流程
---

# Svelte Control Flow

## 任务目标
- 本 Skill 用于：实现条件、循环、异步等控制流逻辑
- 能力包含：if/each/await/key/snippet 块及 render 标签
- 触发条件：需要条件渲染、列表渲染或处理异步数据时

## 操作步骤

### {#if} 条件块
```svelte
{#if answer === 42}
  <p>正确!</p>
{:else if count > 10}
  <p>太大了</p>
{:else}
  <p>太小了</p>
{/if}
```

### {#each} 循环块
```svelte
<!-- 基本用法 -->
{#each items as item}
  <li>{item.name}</li>
{/each}

<!-- 带索引 -->
{#each items as item, i}
  <li>{i + 1}: {item.name}</li>
{/each}

<!-- 带 key 的循环 -->
{#each items as item (item.id)}
  <li>{item.name}</li>
{/each}

<!-- 解构和剩余模式 -->
{#each objects as { id, ...rest }}
  <li><span>{id}</span><Component {...rest} /></li>
{/each}

<!-- 空数据占位 -->
{#each items as item}
  <p>{item}</p>
{:else}
  <p>没有数据</p>
{/each}
```

### {#await} 异步块
```svelte
<!-- 完整形式 -->
{#await promise}
  <p>加载中...</p>
{:then value}
  <p>结果: {value}</p>
{:catch error}
  <p>错误: {error.message}</p>
{/await}

<!-- 简化形式 -->
{#await promise then value}
  <p>{value}</p>
{/await}

{#await promise catch error}
  <p>错误: {error.message}</p>
{/await}
```

### {#key} 键控块
```svelte
<!-- 当 key 变化时重新渲染内容 -->
{#key count}
  <div>{Math.random()}</div>
{/key}
```

### {#snippet} 代码片段
```svelte
{#snippet greeting(name)}
  <p>你好, {name}!</p>
{/snippet}

{@render greeting('Alice')}
{@render greeting('Bob')}
```

### 片段参数与解构
```svelte
{#snippet row(d)}
  <tr><td>{d.name}</td><td>{d.price}</td></tr>
{/snippet}
```

### 片段作用域
```svelte
{#snippet hello(name)}
  <p>你好 {name}!</p>
{/snippet}

{@render hello('world')}
```

### 向组件传递片段
```svelte
<!-- 作为属性传递 -->
<Table {header} {row} />

<!-- 隐式 children -->
<Button>点击我</Button>
```

### {@render} 渲染片段
```svelte
<script>
  let { children } = $props();
</script>

<button>{@render children?.()}</button>
```

## 资源索引
- if：https://svelte.dev/docs/svelte/if
- each：https://svelte.dev/docs/svelte/each
- await：https://svelte.dev/docs/svelte/await
- key：https://svelte.dev/docs/svelte/key
- snippet：https://svelte.dev/docs/svelte/snippet
- @render：https://svelte.dev/docs/svelte/@render
- await 表达式：https://svelte.dev/docs/svelte/await-expressions

## 注意事项
- 优先使用带 key 的 each 块以获得更好的性能
- snippet 可以引用外部变量，但不能引用模块级 `<script>` 外的变量
- `{@render children?.()}` 使用可选链处理未提供的情况
