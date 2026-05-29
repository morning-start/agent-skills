---
name: svelte-api-reference
description: Svelte API 参考技能，掌握 svelte/* 模块的完整 API，包括 store、transition、animate、easing 等
---

# Svelte API Reference

## 任务目标
- 本 Skill 用于：查阅 Svelte API 文档和使用内置模块
- 能力包含：svelte/store、svelte/transition、svelte/animate 等模块
- 触发条件：需要使用特定 API 功能时

## svelte/store 模块

### writable
```javascript
import { writable } from 'svelte/store';

const count = writable(0);

count.subscribe(value => console.log(value));
count.set(1);
count.update(n => n + 1);
```

### readable
```javascript
import { readable } from 'svelte/store';

const time = readable(new Date(), (set) => {
  const interval = setInterval(() => set(new Date()), 1000);
  return () => clearInterval(interval);
});
```

### derived
```javascript
import { derived } from 'svelte/store';

const doubled = derived(count, $count => $count * 2);

const summed = derived([a, b], ([$a, $b]) => $a + $b);
```

### readonly
```javascript
import { readonly, writable } from 'svelte/store';

const writableStore = writable(1);
const readableStore = readonly(writableStore);
```

### get
```javascript
import { get } from 'svelte/store';

const value = get(store);
```

### toStore / fromStore
```javascript
import { toStore, fromStore } from 'svelte/store';

const $state = writable('hello');
const store = fromStore($state);
const newStore = toStore(() => getValue(), (v) => setValue(v));
```

## svelte/transition 模块

### fade
```javascript
import { fade } from 'svelte/transition';

<div transition:fade={{ duration: 300 }}>content</div>
```

### fly
```javascript
import { fly } from 'svelte/transition';

<div transition:fly={{ x: 200, duration: 400 }}>content</div>
```

### slide
```javascript
import { slide } from 'svelte/transition';

<div transition:slide={{ duration: 300 }}>content</div>
```

### scale
```javascript
import { scale } from 'svelte/transition';

<div transition:scale={{ start: 0.5, duration: 300 }}>content</div>
```

### draw
```javascript
import { draw } from 'svelte/transition';

<svg transition:draw={{ duration: 1000 }}>
  <path d="M0 0 L100 100" />
</svg>
```

### blur
```javascript
import { blur } from 'svelte/transition';

<div transition:blur={{ amount: 10 }}>content</div>
```

### fly + fade 组合
```javascript
import { fly, fade } from 'svelte/transition';

<div transition:fly|global={{ y: 200 }} fade>
  content
</div>
```

## svelte/animate 模块

### flip
```javascript
import { flip } from 'svelte/animate';

{#each list as item (item.id)}
  <div animate:flip={{ delay: 0, duration: 300 }}>
    {item.name}
  </div>
{/each}
```

## svelte/easing 模块

### 内置缓动函数
```javascript
import { cubicOut, elasticOut, linear } from 'svelte/easing';

<div transition:fly={{ y: 200, easing: cubicOut }}>
  content
</div>
```

常用缓动函数：
- `linear` - 线性
- `cubicIn`/`cubicOut`/`cubicInOut` - 立方
- `elasticOut`/`elasticIn`/`elasticInOut` - 弹性
- `bounceOut`/`bounceIn`/`bounceInOut` - 弹跳
- `backOut`/`backIn`/`backInOut` - 回退

## svelte/events 模块

### on 事件处理
```javascript
import { on } from 'svelte/events';

const handler = on(element, 'click', (event) => {
  console.log('clicked');
});

// 清理
handler.destroy();
```

## svelte/motion 模块

### tweened
```javascript
import { tweened } from 'svelte/motion';

const size = tweened(0, { duration: 300, easing: cubicOut });
size.set(100);
```

### spring
```javascript
import { spring } from 'svelte/motion';

const pos = spring({ x: 0, y: 0 }, { stiffness: 0.1, damping: 0.25 });
pos.set({ x: 100, y: 100 });
```

## svelte/reactivity 模块

### Source
```javascript
import { source } from 'svelte/reactivity';

const count = source(0);
count.set(1);
count.update(n => n + 1);
console.log(count.get());
```

### Derived
```javascript
import { derived } from 'svelte/reactivity';

const doubled = derived(count, $c => $c * 2);
```

## svelte/compiler 模块

### compile
```javascript
import { compile } from 'svelte/compiler';

const result = compile(sourceCode, {
  filename: 'App.svelte',
  generate: 'dom'
});
```

## svelte/server 模块

### render
```javascript
import { render } from 'svelte/server';

const { html, head } = render(App, {
  props: { data: 'value' }
});
```

## 错误与警告代码

### 编译器错误
```javascript
// 错误代码示例
// x-eof-unexpected - 意外的文件结束
// css-expected-close-tag - CSS 缺少关闭标签
```

### 运行时错误
```javascript
// ownership_invalid_mutation - 修改非拥有的状态
// state_unsafe_mutation - 不安全的状态修改
```

## 资源索引
- svelte：https://svelte.dev/docs/svelte/svelte
- svelte/store：https://svelte.dev/docs/svelte/svelte-store
- svelte/transition：https://svelte.dev/docs/svelte/svelte-transition
- svelte/animate：https://svelte.dev/docs/svelte/svelte-animate
- svelte/easing：https://svelte.dev/docs/svelte/svelte-easing
- svelte/events：https://svelte.dev/docs/svelte/svelte-events
- svelte/motion：https://svelte.dev/docs/svelte/svelte-motion
- svelte/reactivity：https://svelte.dev/docs/svelte/svelte-reactivity
- svelte/server：https://svelte.dev/docs/svelte/svelte-server
- 编译器错误：https://svelte.dev/docs/svelte/compiler-errors
- 运行时错误：https://svelte.dev/docs/svelte/runtime-errors

## 注意事项
- store 的 $ 前缀在组件中自动订阅和取消订阅
- transition 函数返回的对象可以包含 css 或 tick 函数
- 使用 untrack 在 effect 中避免依赖追踪
