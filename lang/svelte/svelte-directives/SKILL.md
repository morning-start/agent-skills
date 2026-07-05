---
name: svelte-directives
description: Svelte 指令技能，掌握 bind、use、transition、animate 等指令，实现 DOM 交互、动画和双向绑定
---

# Svelte Directives

## 任务目标
- 本 Skill 用于：使用 Svelte 指令实现 DOM 交互和数据绑定
- 能力包含：bind 绑定、use 动作、transition 过渡、animate 动画
- 触发条件：需要双向绑定、DOM 操作或动画效果时

## 操作步骤

### bind: 双向绑定

#### 值的绑定
```svelte
<input bind:value={message} />
<textarea bind:value></textarea>
```

#### 复选框与单选
```svelte
<input type="checkbox" bind:checked={agree} />
<input type="radio" bind:group={selection} value="a" />
```

#### select 绑定
```svelte
<select bind:value={selected}>
  <option value="a">A</option>
  <option value="b">B</option>
</select>

<select multiple bind:value={items}>
  <option>A</option>
  <option>B</option>
</select>
```

#### 数值输入
```svelte
<input type="number" bind:value={num} min="0" max="100" />
<input type="range" bind:value range />
```

#### 文件输入
```svelte
<input type="file" bind:files />
```

#### 组件 props 绑定
```svelte
<Keypad bind:value={pin} />

<!-- 组件需要使用 $bindable -->
<script>
  let { value = $bindable() } = $props();
</script>
```

#### 尺寸绑定
```svelte
<div bind:offsetWidth={w} bind:offsetHeight={h}>
  <Chart {width}={w} height={h} />
</div>
```

#### bind:this 获取 DOM 引用
```svelte
<canvas bind:this={canvas}></canvas>

<script>
  let canvas;
  $effect(() => {
    const ctx = canvas.getContext('2d');
  });
</script>
```

### use: 动作
```svelte
<script>
  import { tooltip } from './actions';
</script>

<button use:tooltip={'提示文本'}>hover</button>
```

### transition: 过渡

#### 内置过渡
```svelte
<script>
  import { fade, fly, slide } from 'svelte/transition';
</script>

{#if visible}
  <div transition:fade>淡入淡出</div>
  <div transition:fly={{ y: 200 }}>飞入</div>
  <div transition:slide>滑动</div>
{/if}
```

#### 全局过渡
```svelte
<p transition:fade|global>父级变化也会触发</p>
```

#### 自定义过渡
```svelte
<script>
  function whoosh(node, params) {
    return {
      duration: 400,
      css: (t) => `transform: scale(${t})`
    };
  }
</script>

<div in:whoosh>whooshes in</div>
```

### in: 和 out: 单向过渡
```svelte
<div in:fade out:fly>内容</div>
```

### animate: 动画
```svelte
<script>
  import { flip } from 'svelte/animate';
</script>

{#each list as item (item.id)}
  <div animate:flip>{item.name}</div>
{/each}
```

### style: 样式指令
```svelte
<div style:color="red" style:font-size="14px">样式</div>
<div style:color style:width="100px">缩写形式</div>
```

### class: 类指令
```svelte
<div class:active={isActive} class:disabled={isDisabled}>
  内容
</div>

<!-- 对象形式 (Svelte 5.16+) -->
<div class={{ active: true, dark: false }}>内容</div>

<!-- 数组形式 -->
<div class={['one', condition && 'two']}>内容</div>
```

### await 块指令
```svelte
{#await promise}
  <p>loading...</p>
{:then value}
  <p>{value}</p>
{/await}
```

## 资源索引
- bind：https://svelte.dev/docs/svelte/bind
- use：https://svelte.dev/docs/svelte/use
- transition：https://svelte.dev/docs/svelte/transition
- in/out：https://svelte.dev/docs/svelte/in-and-out
- animate：https://svelte.dev/docs/svelte/animate
- style：https://svelte.dev/docs/svelte/style
- class：https://svelte.dev/docs/svelte/class
- await：https://svelte.dev/docs/svelte/await-expressions

## 注意事项
- bind:group 用于单选和复选框组
- 过渡函数返回的 css 函数会被 Svelte 转换为 keyframes
- 优先使用 class 属性而非 class: 指令（更简洁）
- bind:this 在 mounted 后才有效
