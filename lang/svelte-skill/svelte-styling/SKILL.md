---
name: svelte-styling
description: Svelte 样式技能，掌握作用域样式、全局样式、CSS 自定义属性和嵌套样式，实现组件样式隔离与复用
---

# Svelte Styling

## 任务目标
- 本 Skill 用于：编写和管理 Svelte 组件的样式
- 能力包含：作用域样式、全局样式、CSS 自定义属性、嵌套样式
- 触发条件：需要为组件添加样式或处理样式冲突时

## 操作步骤

### 作用域样式
```svelte
<style>
  p {
    color: burlywood;
  }
</style>

<!-- 仅影响当前组件的 <p> -->
<p>只在当前组件生效</p>
```

### 全局样式
```svelte
<style>
  :global(body) {
    margin: 0;
  }

  :global(.shared-class) {
    font-size: 14px;
  }

  .local-class :global(.child) {
    color: red;
  }
</style>
```

### CSS 自定义属性（Props）
```svelte
<!-- 父组件 -->
<Component --color="red" --size="12px" />

<!-- 子组件 -->
<div style="color: var(--color); font-size: var(--size)">
  内容
</div>
```

### 嵌套 <style> 元素
```svelte
<div class="outer">
  <div class="inner">
    <p>嵌套样式测试</p>
  </div>
</div>

<style>
  .outer {
    .inner {
      p {
        color: blue;
      }
    }
  }
</style>
```

### 使用 JS 变量控制样式
```svelte
<script>
  let { theme = 'light' } = $props();
</script>

<div style:--bg={theme === 'dark' ? '#000' : '#fff'}>
  背景色随主题变化
</div>

<style>
  div {
    background: var(--bg);
  }
</style>
```

### 样式组合
```svelte
<style>
  .base {
    padding: 10px;
  }

  .variant {
    background: blue;
    color: white;
  }
</style>

<div class="base variant">组合样式</div>
```

## 资源索引
- 作用域样式：https://svelte.dev/docs/svelte/scoped-styles
- 全局样式：https://svelte.dev/docs/svelte/global-styles
- 自定义属性：https://svelte.dev/docs/svelte/custom-properties
- 嵌套样式：https://svelte.dev/docs/svelte/nested-style-elements

## 注意事项
- Svelte 5 作用域样式使用 `:where(.svelte-xyz)` 避免优先级问题
- 全局样式应谨慎使用，可能影响其他组件
- CSS 自定义属性是向子组件传递样式的推荐方式
