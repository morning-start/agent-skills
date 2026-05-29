# 前端框架 API 文档参考

## 目录

- [概述](#概述)
- [React](#react)
- [Vue](#vue)
- [Angular](#angular)
- [Svelte](#svelte)
- [Next.js](#nextjs)
- [Nuxt.js](#nuxtjs)
- [通用最佳实践](#通用最佳实践)

## 概述

本文档提供了主流前端框架的 API 文档组织方式和组件识别的最佳实践，帮助开发者更好地理解和使用前端框架的 API 文档。

## React

### 官方文档结构

React 的官方文档（react.dev）采用以下组织结构：

- **Getting Started** - 快速入门和基础概念
- **Learn** - 深入学习 React 核心概念
- **Reference** - API 参考，包含所有 React API
- **Reference > Hooks** - 所有 Hooks 的详细文档
- **Reference > Components** - 组件 API 参考

### 组件文档组织方式

#### 1. 组件概述

```markdown
# ComponentName

用于描述组件的主要用途和功能。
```

#### 2. Props 文档

```markdown
## Props

| Prop  | Type   | Default | Required | Description       |
| ----- | ------ | ------- | -------- | ----------------- |
| prop1 | string | -       | Yes      | 描述 prop1 的用途 |
| prop2 | number | 0       | No       | 描述 prop2 的用途 |
```

#### 3. 使用示例

````markdown
## Usage

```jsx
import { ComponentName } from "./ComponentName";

function App() {
  return <ComponentName prop1="value" />;
}
```
````

````

#### 4. TypeScript 类型定义
```typescript
interface ComponentNameProps {
  prop1: string;
  prop2?: number;
  prop3?: {
    nested: string;
  };
}
````

### 组件识别最佳实践

#### 1. 函数组件识别

- 以大写字母开头的函数
- 返回 JSX 元素
- 使用 `export` 或 `export default` 导出

#### 2. 类组件识别

- 继承自 `React.Component` 或 `React.PureComponent`
- 实现 `render()` 方法
- 使用 `@Component` 装饰器（如果使用 TypeScript）

#### 3. Hooks 识别

- 以 `use` 开头的函数
- 在函数组件内部调用
- 遵循 Hooks 规则

#### 4. Props 提取

- 函数组件：从函数参数中提取
- 类组件：从 `this.props` 中提取
- TypeScript：从接口或类型定义中提取

#### 5. Events 提取

- 查找以 `on` 开头的属性（如 `onClick`, `onChange`）
- 从事件处理器函数签名中提取事件类型

### 文档生成建议

1. **使用 JSDoc 注释**

```jsx
/**
 * Button 组件用于触发操作
 * @param {Object} props - 组件属性
 * @param {string} props.label - 按钮文本
 * @param {() => void} props.onClick - 点击事件处理器
 * @param {boolean} props.disabled - 是否禁用
 */
function Button({ label, onClick, disabled }) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  );
}
```

2. **使用 TypeScript 类型定义**

```typescript
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
  variant?: 'primary' | 'secondary';
}

function Button({ label, onClick, disabled, variant = 'primary' }: ButtonProps) {
  return <button onClick={onClick} disabled={disabled}>{label}</button>;
}
```

3. **提供完整的使用示例**

```jsx
import { Button } from "./Button";

function Example() {
  return (
    <div>
      <Button label="Click me" onClick={() => alert("Clicked!")} />
      <Button label="Disabled" disabled onClick={() => {}} />
    </div>
  );
}
```

## Vue

### 官方文档结构

Vue 的官方文档（vuejs.org）采用以下组织结构：

- **Essentials** - 基础概念和核心功能
- **Components In-Depth** - 深入了解组件
- **Reactivity In-Depth** - 深入了解响应式系统
- **Built-in Components** - 内置组件
- **Built-in Directives** - 内置指令
- **API Reference** - API 参考

### 组件文档组织方式

#### 1. 组件概述

```markdown
# ComponentName

用于描述组件的主要用途和功能。
```

#### 2. Props 文档

```markdown
## Props

| Prop  | Type   | Default | Required | Description       |
| ----- | ------ | ------- | -------- | ----------------- |
| prop1 | String | -       | Yes      | 描述 prop1 的用途 |
| prop2 | Number | 0       | No       | 描述 prop2 的用途 |
```

#### 3. Events 文档

```markdown
## Events

| Event  | Payload             | Description    |
| ------ | ------------------- | -------------- |
| update | value               | 当值更新时触发 |
| change | { value, oldValue } | 当值改变时触发 |
```

#### 4. Slots 文档

```markdown
## Slots

| Slot    | Description  |
| ------- | ------------ |
| default | 默认插槽内容 |
| header  | 头部插槽内容 |
| footer  | 底部插槽内容 |
```

#### 5. 使用示例

```vue
<template>
  <ComponentName prop1="value" @update="handleUpdate">
    <template #header>Header Content</template>
    Default Content
    <template #footer>Footer Content</template>
  </ComponentName>
</template>
```

### 组件识别最佳实践

#### 1. Options API 组件识别

- `export default` 对象包含 `name`, `props`, `data`, `methods`, `computed`, `watch`
- 使用 `<template>` 标签定义模板

#### 2. Composition API 组件识别

- 使用 `<script setup>` 语法
- 使用 `defineProps` 和 `defineEmits`
- 使用 `ref`, `computed`, `watch` 等组合式函数

#### 3. Props 提取

- Options API：从 `props` 对象中提取
- Composition API：从 `defineProps` 调用中提取
- TypeScript：从接口或类型定义中提取

#### 4. Events 提取

- Options API：从 `this.$emit` 调用中提取
- Composition API：从 `defineEmits` 调用中提取
- TypeScript：从 `defineEmits` 的类型参数中提取

#### 5. Slots 提取

- 从模板中的 `<slot>` 元素提取
- 记录具名插槽（`<slot name="header">`）

### 文档生成建议

1. **使用 JSDoc 注释**

```vue
<script>
/**
 * Button 组件用于触发操作
 */
export default {
  name: "Button",
  props: {
    label: {
      type: String,
      required: true,
      description: "按钮文本",
    },
    disabled: {
      type: Boolean,
      default: false,
      description: "是否禁用",
    },
  },
  emits: ["click"],
  methods: {
    handleClick() {
      if (!this.disabled) {
        this.$emit("click");
      }
    },
  },
};
</script>
```

2. **使用 TypeScript 类型定义**

```vue
<script setup lang="ts">
interface ButtonProps {
  label: string;
  disabled?: boolean;
  variant?: "primary" | "secondary";
}

const props = withDefaults(defineProps<ButtonProps>(), {
  disabled: false,
  variant: "primary",
});

const emit = defineEmits<{
  click: [];
}>();
</script>
```

3. **提供完整的使用示例**

```vue
<template>
  <div>
    <Button label="Click me" @click="handleClick" />
    <Button label="Disabled" disabled @click="handleClick" />
  </div>
</template>

<script setup>
import { Button } from "./Button";

function handleClick() {
  alert("Clicked!");
}
</script>
```

## Angular

### 官方文档结构

Angular 的官方文档（angular.io）采用以下组织结构：

- **Tutorial** - 教程
- **Introduction** - 介绍和概念
- **Components & Templates** - 组件和模板
- **Forms** - 表单
- **Dependency Injection** - 依赖注入
- **API** - API 参考

### 组件文档组织方式

#### 1. 组件概述

```markdown
# ComponentName

用于描述组件的主要用途和功能。
```

#### 2. Inputs 文档

```markdown
## Inputs

| Input  | Type   | Default | Required | Description        |
| ------ | ------ | ------- | -------- | ------------------ |
| input1 | string | -       | Yes      | 描述 input1 的用途 |
| input2 | number | 0       | No       | 描述 input2 的用途 |
```

#### 3. Outputs 文档

```markdown
## Outputs

| Output | Payload             | Description    |
| ------ | ------------------- | -------------- |
| update | value               | 当值更新时触发 |
| change | { value, oldValue } | 当值改变时触发 |
```

#### 4. 使用示例

```typescript
import { Component } from "@angular/core";

@Component({
  selector: "app-example",
  template: `
    <app-component-name [input1]="value" (update)="handleUpdate($event)">
    </app-component-name>
  `,
})
export class ExampleComponent {
  value = "example";

  handleUpdate(newValue: string) {
    console.log(newValue);
  }
}
```

### 组件识别最佳实践

#### 1. 组件识别

- 使用 `@Component` 装饰器标记类
- 包含 `selector`, `template`, `styles` 等元数据

#### 2. Inputs 提取

- 从 `@Input()` 装饰器标记的属性中提取
- TypeScript：从属性类型中提取

#### 3. Outputs 提取

- 从 `@Output()` 装饰器标记的属性中提取
- 从 `EventEmitter` 的泛型类型中提取事件负载类型

#### 4. 生命周期钩子识别

- `ngOnInit`, `ngOnChanges`, `ngDoCheck`, `ngAfterContentInit`, `ngAfterViewInit`, `ngOnDestroy`

### 文档生成建议

1. **使用 JSDoc 注释**

```typescript
import { Component, Input, Output, EventEmitter } from "@angular/core";

/**
 * Button 组件用于触发操作
 */
@Component({
  selector: "app-button",
  template: `<button (click)="handleClick()">{{ label }}</button>`,
})
export class ButtonComponent {
  /**
   * 按钮文本
   */
  @Input() label: string;

  /**
   * 是否禁用
   */
  @Input() disabled = false;

  /**
   * 点击事件
   */
  @Output() click = new EventEmitter<void>();

  handleClick() {
    if (!this.disabled) {
      this.click.emit();
    }
  }
}
```

2. **使用 TypeScript 类型定义**

```typescript
import { Component, Input, Output, EventEmitter } from "@angular/core";

interface ButtonProps {
  label: string;
  disabled?: boolean;
  variant?: "primary" | "secondary";
}

@Component({
  selector: "app-button",
  template: `<button (click)="handleClick()">{{ label }}</button>`,
})
export class ButtonComponent implements ButtonProps {
  @Input() label!: string;
  @Input() disabled = false;
  @Input() variant: "primary" | "secondary" = "primary";
  @Output() click = new EventEmitter<void>();
}
```

3. **提供完整的使用示例**

```typescript
import { Component } from "@angular/core";
import { ButtonComponent } from "./button.component";

@Component({
  selector: "app-example",
  template: `
    <app-button label="Click me" (click)="handleClick()" />
    <app-button label="Disabled" [disabled]="true" (click)="handleClick()" />
  `,
})
export class ExampleComponent {
  handleClick() {
    alert("Clicked!");
  }
}
```

## Svelte

### 官方文档结构

Svelte 的官方文档（svelte.dev）采用以下组织结构：

- **Introduction** - 介绍
- **Basic Syntax** - 基础语法
- **Reactivity** - 响应式
- **Lifecycle** - 生命周期
- **Slots** - 插槽
- **Special elements** - 特殊元素
- **Component API** - 组件 API

### 组件文档组织方式

#### 1. 组件概述

```markdown
# ComponentName

用于描述组件的主要用途和功能。
```

#### 2. Props 文档

```markdown
## Props

| Prop  | Type   | Default | Required | Description       |
| ----- | ------ | ------- | -------- | ----------------- |
| prop1 | string | -       | Yes      | 描述 prop1 的用途 |
| prop2 | number | 0       | No       | 描述 prop2 的用途 |
```

#### 3. Events 文档

```markdown
## Events

| Event  | Payload             | Description    |
| ------ | ------------------- | -------------- |
| update | value               | 当值更新时触发 |
| change | { value, oldValue } | 当值改变时触发 |
```

#### 4. Slots 文档

```markdown
## Slots

| Slot    | Description  |
| ------- | ------------ |
| default | 默认插槽内容 |
| header  | 头部插槽内容 |
| footer  | 底部插槽内容 |
```

#### 5. 使用示例

```svelte
<script>
  import ComponentName from './ComponentName.svelte';
</script>

<ComponentName prop1="value" on:update={handleUpdate}>
  <svelte:fragment slot="header">Header Content</svelte:fragment>
  Default Content
  <svelte:fragment slot="footer">Footer Content</svelte:fragment>
</ComponentName>
```

### 组件识别最佳实践

#### 1. 组件识别

- `.svelte` 文件扩展名
- 包含 `<script>` 和 `<template>` 标签

#### 2. Props 提取

- 从 `export let` 声明的变量中提取
- TypeScript：从类型注解中提取

#### 3. Events 提取

- 从 `dispatch` 调用中提取
- 从事件名称和负载中提取

#### 4. Slots 提取

- 从 `<slot>` 元素提取
- 记录具名插槽（`<slot name="header">`）

### 文档生成建议

1. **使用 JSDoc 注释**

```svelte
<script>
  import { createEventDispatcher } from 'svelte';

  /**
   * Button 组件用于触发操作
   */
  export let label;
  export let disabled = false;

  const dispatch = createEventDispatcher();

  function handleClick() {
    if (!disabled) {
      dispatch('click');
    }
  }
</script>

<button on:click={handleClick} disabled={disabled}>
  {label}
</button>
```

2. **使用 TypeScript 类型定义**

```svelte
<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  interface ButtonProps {
    label: string;
    disabled?: boolean;
    variant?: 'primary' | 'secondary';
  }

  export let label: string;
  export let disabled = false;
  export let variant: 'primary' | 'secondary' = 'primary';

  const dispatch = createEventDispatcher<{
    click: void;
  }>();

  function handleClick() {
    if (!disabled) {
      dispatch('click');
    }
  }
</script>

<button on:click={handleClick} disabled={disabled}>
  {label}
</button>
```

3. **提供完整的使用示例**

```svelte
<script>
  import Button from './Button.svelte';

  function handleClick() {
    alert('Clicked!');
  }
</script>

<Button label="Click me" on:click={handleClick} />
<Button label="Disabled" disabled on:click={handleClick} />
```

## Next.js

### 官方文档结构

Next.js 的官方文档（nextjs.org）采用以下组织结构：

- **Getting Started** - 快速入门
- **Pages** - 页面路由
- **Routing** - 路由
- **Rendering** - 渲染
- **Data Fetching** - 数据获取
- **API Routes** - API 路由
- **Building Your Application** - 构建应用

### API 路由文档组织方式

#### 1. 端点概述

```markdown
# Endpoint Name

用于描述 API 端点的主要用途和功能。
```

#### 2. 请求参数

```markdown
## Request Parameters

### Query Parameters

| Parameter | Type   | Required | Default | Description        |
| --------- | ------ | -------- | ------- | ------------------ |
| param1    | string | Yes      | -       | 描述 param1 的用途 |
| param2    | number | No       | 0       | 描述 param2 的用途 |

### Body Parameters

| Parameter | Type   | Required | Default | Description        |
| --------- | ------ | -------- | ------- | ------------------ |
| field1    | string | Yes      | -       | 描述 field1 的用途 |
| field2    | number | No       | 0       | 描述 field2 的用途 |
```

#### 3. 响应格式

````markdown
## Response Format

### Success Response

```json
{
  "data": {},
  "status": "success"
}
```
````

### Error Response

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Error message"
  }
}
```

````

### API 路由识别最佳实践

#### 1. Pages Router 识别
- `pages/api/` 目录下的文件
- 导出默认处理函数
- 使用 `NextApiRequest` 和 `NextApiResponse` 类型

#### 2. App Router 识别
- `app/api/` 目录下的 `route.ts` 文件
- 导出名为 `GET`, `POST`, `PUT`, `DELETE`, `PATCH` 的函数
- 使用 `Request` 和 `Response` 类型

#### 3. 动态路由识别
- 方括号 `[param]` 包裹的文件名或目录名

### 文档生成建议

1. **使用 TypeScript 类型定义**
```typescript
// pages/api/users.ts
import type { NextApiRequest, NextApiResponse } from 'next';

interface User {
  id: string;
  name: string;
  email: string;
}

interface ApiResponse<T> {
  data: T;
  status: 'success' | 'error';
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ApiResponse<User[]>>
) {
  if (req.method === 'GET') {
    const users = await getUsers();
    res.status(200).json({ data: users, status: 'success' });
  }
}
````

2. **提供完整的使用示例**

```typescript
// app/api/users/route.ts
import { NextResponse } from "next/server";

export async function GET(request: Request) {
  const users = await getUsers();
  return NextResponse.json({ data: users, status: "success" });
}

export async function POST(request: Request) {
  const body = await request.json();
  const user = await createUser(body);
  return NextResponse.json({ data: user, status: "success" }, { status: 201 });
}
```

## Nuxt.js

### 官方文档结构

Nuxt.js 的官方文档（nuxt.com）采用以下组织结构：

- **Getting Started** - 快速入门
- **Concepts** - 概念
- **Directory Structure** - 目录结构
- **Routing** - 路由
- **Data Fetching** - 数据获取
- **Server Routes** - 服务器路由
- **Components** - 组件

### API 路由文档组织方式

#### 1. 端点概述

```markdown
# Endpoint Name

用于描述 API 端点的主要用途和功能。
```

#### 2. 请求参数

```markdown
## Request Parameters

### Query Parameters

| Parameter | Type   | Required | Default | Description        |
| --------- | ------ | -------- | ------- | ------------------ |
| param1    | string | Yes      | -       | 描述 param1 的用途 |
| param2    | number | No       | 0       | 描述 param2 的用途 |

### Body Parameters

| Parameter | Type   | Required | Default | Description        |
| --------- | ------ | -------- | ------- | ------------------ |
| field1    | string | Yes      | -       | 描述 field1 的用途 |
| field2    | number | No       | 0       | 描述 field2 的用途 |
```

#### 3. 响应格式

````markdown
## Response Format

### Success Response

```json
{
  "data": {},
  "status": "success"
}
```
````

### Error Response

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Error message"
  }
}
```

````

### API 路由识别最佳实践

#### 1. API 路由识别
- `server/api/` 目录下的文件
- 使用 `defineEventHandler` 函数
- 方法特定路由：`.get.ts`, `.post.ts`, `.put.ts`, `.delete.ts`, `.patch.ts` 后缀

#### 2. 动态路由识别
- 方括号 `[param]` 包裹的文件名

### 文档生成建议

1. **使用 TypeScript 类型定义**
```typescript
// server/api/users.get.ts
import type { H3Event } from 'h3';

interface User {
  id: string;
  name: string;
  email: string;
}

interface ApiResponse<T> {
  data: T;
  status: 'success' | 'error';
}

export default defineEventHandler(async (event: H3Event) => {
  const users = await getUsers();
  return { data: users, status: 'success' };
});
````

2. **提供完整的使用示例**

```typescript
// server/api/users.ts
export default defineEventHandler(async (event) => {
  const method = getMethod(event);

  if (method === "GET") {
    const users = await getUsers();
    return { data: users, status: "success" };
  } else if (method === "POST") {
    const body = await readBody(event);
    const user = await createUser(body);
    return { data: user, status: "success" };
  }
});
```

## 通用最佳实践

### 1. 文档结构

#### 组件文档应包含：

- 组件概述
- Props/Inputs 文档
- Events/Outputs 文档
- Slots 文档（如果适用）
- 使用示例
- TypeScript 类型定义

#### API 文档应包含：

- 端点概述
- 请求参数（路径、查询、请求体）
- 响应格式
- 错误处理
- 使用示例

### 2. 类型注解

- 始终使用 TypeScript 类型注解
- 为组件 Props 定义接口
- 为 API 请求和响应定义类型
- 使用泛型提高类型安全性

### 3. 注释规范

- 使用 JSDoc 或框架特定的注释格式
- 为公共 API 提供描述性注释
- 说明参数的类型、默认值和用途
- 提供使用示例

### 4. 示例代码

- 提供完整、可运行的示例
- 展示常见使用场景
- 包含错误处理
- 说明最佳实践

### 5. 文档生成工具

- **Storybook**: 用于组件文档和可视化
- **TypeDoc**: 用于 TypeScript API 文档
- **JSDoc**: 用于 JavaScript API 文档
- **VuePress**: 用于 Vue 项目文档
- **Docusaurus**: 用于通用项目文档

### 6. 自动化文档生成

- 从代码注释自动生成文档
- 使用 CI/CD 自动更新文档
- 保持文档与代码同步
- 定期审查和更新文档
