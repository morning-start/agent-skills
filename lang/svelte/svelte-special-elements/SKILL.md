---
name: svelte-special-elements
description: Svelte 特殊元素技能，掌握 svelte:window、svelte:document、svelte:element 等内置元素，实现全局事件和动态元素处理
---

# Svelte Special Elements

## 任务目标
- 本 Skill 用于：使用 Svelte 内置的特殊元素
- 能力包含：窗口/文档事件、动态元素、元素选项、片段等
- 触发条件：需要监听全局事件或动态渲染元素时

## 操作步骤

### svelte:element 动态元素
```svelte
<script>
  let tag = $state('div');
</script>

<svelte:element this={tag}>
  动态标签内容
</svelte:element>

<!-- 带命名空间 -->
<svelte:element this={tag} xmlns="http://www.w3.org/2000/svg">
  SVG 内容
</svelte:element>
```

### svelte:window 全局窗口事件
```svelte
<svelte:window onkeydown={handleKey} onresize={handleResize} />
<svelte:window bind:innerWidth bind:innerHeight />
<svelte:window bind:scrollY />
```

### svelte:document 文档事件
```svelte
<svelte:document onvisibilitychange={handleVisibility} />
<svelte:document onselectionchange={handleSelection} />
```

### svelte:body  body 事件
```svelte
<svelte:body onmouseenter={handleMouseEnter} onmouseleave={handleMouseLeave} />
```

### svelte:head 文档头部
```svelte
<svelte:head>
  <title>页面标题</title>
  <meta name="description" content="描述" />
  <link rel="canonical" href="https://example.com" />
</svelte:head>
```

### svelte:boundary 错误边界
```svelte
<svelte:boundary onerror={handleError}>
  <ComponentThatMightFail />

  {#snippet failed()}
    <p>加载失败</p>
  {/snippet}
</svelte:boundary>
```

### svelte:options 编译器选项
```svelte
<svelte:options customElement="my-element" />
<svelte:options runes={true} />
<svelte:options immutable={true} />
<svelte:options accessors={true} />
<svelte:options namespace="svg" />
<svelte:options preserveWhitespace={true} />
```

### svelte:fragment 片段占位
```svelte
<!-- Child.svelte -->
<svelte:fragment slot="header">
  <h1>标题</h1>
</svelte:fragment>

<!-- Parent.svelte -->
<Child>
  <svelte:fragment slot="header">
    <h1>重写的标题</h1>
  </svelte:fragment>
</Child>
```

## 资源索引
- svelte:boundary：https://svelte.dev/docs/svelte/svelte-boundary
- svelte:window：https://svelte.dev/docs/svelte/svelte-window
- svelte:document：https://svelte.dev/docs/svelte/svelte-document
- svelte:body：https://svelte.dev/docs/svelte/svelte-body
- svelte:head：https://svelte.dev/docs/svelte/svelte-head
- svelte:element：https://svelte.dev/docs/svelte/svelte-element
- svelte:options：https://svelte.dev/docs/svelte/svelte-options

## 注意事项
- svelte:element 的 `this` 值必须是有效的 DOM 标签名
- svelte:window/document/body 只能出现在组件顶层
- customElement 用于创建 Web Components
