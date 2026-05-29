---
name: svelte-template-basics
description: Svelte 模板基础技能，掌握标记语法、文本表达式、注释和特殊渲染标签，实现组件模板的编写
---

# Svelte Template Basics

## 任务目标
- 本 Skill 用于：编写 Svelte 组件的模板结构
- 能力包含：元素标签、属性绑定、文本插值、特殊渲染标签
- 触发条件：需要编写 Svelte 组件模板时

## 操作步骤

### 元素与组件标签
```svelte
<!-- 小写标签 = HTML 元素 -->
<div>

<!-- 大写标签 = Svelte 组件 -->
<Widget />

<!-- 点号表示法 -->
<my.customComponent />
```

### 属性绑定
```svelte
<!-- 表达式属性 -->
<button disabled={!clickable}>click</button>

<!-- 缩写形式 -->
<input {value} />
<!-- 等价于 -->
<input value={value} />

<!-- 展开属性 -->
<Widget {...props} />
```

### 事件处理
```svelte
<!-- 事件属性 -->
<button onclick={() => count++}>+1</button>

<!-- 事件委托 -->
<input beforeinput onbeforeinput={handleInput} />
```

### 文本表达式
```svelte
<p>{a} + {b} = {a + b}</p>

<!-- null/undefined 被省略 -->
<p>{value ?? 'default'}</p>
```

### {@html} 渲染 HTML
```svelte
<div>{@html htmlString}</div>
```

### {@const} 局部常量
```svelte
{#each items as item}
  {@const id = item.id + '-suffix'}
  <div {id}>{item.name}</div>
{/each}
```

### {@debug} 调试标签
```svelte
{@debug user}

<!-- 或指定变量 -->
{@debug user, count}
```

### {@attach} 附加动作
```svelte
<script>
  import { tooltip } from './actions';
</script>

<button {@attach tooltip={message}}>hover me</button>
```

### 组件注释
```svelte
<!-- 普通注释 -->

<!-- svelte-ignore a11y_autofocus -->
<input bind:value autofocus />
```

## 资源索引
- 基础标记：https://svelte.dev/docs/svelte/basic-markup
- @html：https://svelte.dev/docs/svelte/@html
- @attach：https://svelte.dev/docs/svelte/@attach
- @const：https://svelte.dev/docs/svelte/@const
- @debug：https://svelte.dev/docs/svelte/@debug

## 注意事项
- `{@html}` 内容不会被转义，注意 XSS 风险
- 事件属性以 `on` 开头，如 `onclick`、`oninput`
- `<script module>` 可导出代码供其他组件使用
