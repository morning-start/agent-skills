# Web 框架路由识别模式

## 目录

- [后端框架](#后端框架)
  - [Flask](#flask)
  - [FastAPI](#fastapi)
  - [Express](#express)
  - [Django](#django)
  - [NestJS](#nestjs)
  - [Spring Boot](#spring-boot)
  - [Gin](#gin)
  - [Echo](#echo)
- [前端框架](#前端框架)
  - [React](#react)
  - [Vue](#vue)
  - [Angular](#angular)
  - [Svelte](#svelte)
  - [Next.js](#nextjs)
  - [Nuxt.js](#nuxtjs)
- [通用识别策略](#通用识别策略)
- [限制与建议](#限制与建议)

## 后端框架

### Flask

#### 路由定义模式

```python
@app.route('/users', methods=['GET', 'POST'])
def users():
    pass

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    pass

# 使用蓝图
@bp.route('/products', methods=['GET'])
def products():
    pass
```

#### 识别规则

- 装饰器：`@app.route` 或 `@bp.route`
- 第一个参数：路由路径
- methods参数：HTTP方法（可选，默认GET）
- 路径参数格式：`<param_name>` 或 `<type:param_name>`

#### 参数提取

- 路径参数：从路由装饰器的路径中提取 `<param_name>`
- 查询参数：查找 `request.args.get()` 调用
- 请求体参数：查找 `request.json.get()` 或 `request.form.get()` 调用

### FastAPI

#### 路由定义模式

```python
@app.get('/users')
async def get_users(skip: int = 0, limit: int = 100):
    pass

@app.post('/users')
async def create_user(user: UserCreate):
    pass

@app.get('/users/{user_id}')
async def get_user(user_id: int):
    pass
```

#### 识别规则

- 装饰器：`@app.get`, `@app.post`, `@app.put`, `@app.delete`, `@app.patch`
- 装饰器名称直接表示HTTP方法
- 第一个参数：路由路径
- 函数签名中的参数：自动识别为查询参数或路径参数

#### 参数提取

- 路径参数：路径中的 `{param_name}`
- 查询参数：函数签名中非路径参数且有默认值
- 请求体参数：函数签名中的Pydantic模型参数
- 类型注解：从类型注解中提取参数类型

### Express

#### 路由定义模式

```javascript
// 应用级别
app.get("/users", (req, res) => {
  // ...
});

app.post("/users", (req, res) => {
  // ...
});

// 路由器级别
router.get("/products", (req, res) => {
  // ...
});

// 路径参数
app.get("/users/:id", (req, res) => {
  // ...
});
```

#### 识别规则

- 方法调用：`app.get`, `app.post`, `app.put`, `app.delete`, `app.patch`
- 或：`router.get`, `router.post` 等
- 第一个参数：路由路径
- 第二个参数：回调函数

#### 参数提取

- 路径参数：路径中的 `:param_name` 格式
- 查询参数：`req.query` 属性
- 请求体参数：`req.body` 属性

### Django

#### 路由定义模式

```python
# 函数视图
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list, name='user-list'),
    path('users/<int:user_id>/', views.user_detail, name='user-detail'),
]

# 类视图
from django.urls import path
from .views import UserListView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
]

# Django REST Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def user_list(request):
    if request.method == 'GET':
        # ...
    elif request.method == 'POST':
        # ...

# ViewSet
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# 路由注册
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'users', UserViewSet)
urlpatterns = router.urls
```

#### 识别规则

- URL配置：`path()`, `re_path()`, `url()`
- DRF装饰器：`@api_view`, `@permission_classes`
- ViewSet：继承自 `viewsets.ModelViewSet` 或其他ViewSet基类
- 路由注册：`router.register()`

#### 参数提取

- 路径参数：URL模式中的 `<param_name>` 或 `<type:param_name>`
- 查询参数：`request.GET` 或 `request.query_params`
- 请求体参数：`request.data` 或 `request.POST`
- 类型注解：从序列化器（Serializer）中提取

### NestJS

#### 路由定义模式

```typescript
import {
  Controller,
  Get,
  Post,
  Put,
  Delete,
  Body,
  Param,
} from "@nestjs/common";

@Controller("users")
export class UsersController {
  @Get()
  findAll() {
    // ...
  }

  @Get(":id")
  findOne(@Param("id") id: string) {
    // ...
  }

  @Post()
  create(@Body() createUserDto: CreateUserDto) {
    // ...
  }

  @Put(":id")
  update(@Param("id") id: string, @Body() updateUserDto: UpdateUserDto) {
    // ...
  }

  @Delete(":id")
  remove(@Param("id") id: string) {
    // ...
  }
}
```

#### 识别规则

- 装饰器：`@Controller`, `@Get`, `@Post`, `@Put`, `@Delete`, `@Patch`
- 类装饰器：`@Controller` 指定基础路径
- 方法装饰器：`@Get`, `@Post` 等指定具体路由和HTTP方法
- 参数装饰器：`@Param`, `@Body`, `@Query`, `@Headers`

#### 参数提取

- 路径参数：`@Param('param_name')` 装饰器
- 查询参数：`@Query('param_name')` 装饰器
- 请求体参数：`@Body()` 装饰器，配合DTO类
- 类型注解：从DTO类的TypeScript类型中提取

### Spring Boot

#### 路由定义模式

```java
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping
    public List<User> getAllUsers() {
        // ...
    }

    @GetMapping("/{id}")
    public User getUserById(@PathVariable Long id) {
        // ...
    }

    @PostMapping
    public User createUser(@RequestBody User user) {
        // ...
    }

    @PutMapping("/{id}")
    public User updateUser(@PathVariable Long id, @RequestBody User user) {
        // ...
    }

    @DeleteMapping("/{id}")
    public void deleteUser(@PathVariable Long id) {
        // ...
    }
}
```

#### 识别规则

- 类注解：`@RestController`, `@Controller`
- 路径注解：`@RequestMapping`, `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`, `@PatchMapping`
- 参数注解：`@PathVariable`, `@RequestBody`, `@RequestParam`, `@RequestHeader`

#### 参数提取

- 路径参数：`@PathVariable` 注解
- 查询参数：`@RequestParam` 注解
- 请求体参数：`@RequestBody` 注解
- 类型注解：从Java类型中提取

### Gin

#### 路由定义模式

```go
package main

import (
    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.Default()

    // 简单路由
    r.GET("/users", getUsers)
    r.POST("/users", createUser)
    r.PUT("/users/:id", updateUser)
    r.DELETE("/users/:id", deleteUser)

    // 路由组
    v1 := r.Group("/api/v1")
    {
        v1.GET("/users", getUsers)
        v1.POST("/users", createUser)
    }

    r.Run(":8080")
}

func getUsers(c *gin.Context) {
    // ...
}

func createUser(c *gin.Context) {
    // ...
}

func updateUser(c *gin.Context) {
    id := c.Param("id")
    // ...
}

func deleteUser(c *gin.Context) {
    id := c.Param("id")
    // ...
}
```

#### 识别规则

- 方法调用：`r.GET`, `r.POST`, `r.PUT`, `r.DELETE`, `r.PATCH`
- 路由组：`r.Group()` 创建路由组
- 第一个参数：路由路径
- 第二个参数：处理函数

#### 参数提取

- 路径参数：`c.Param("param_name")` 方法
- 查询参数：`c.Query("param_name")` 或 `c.DefaultQuery()` 方法
- 请求体参数：`c.BindJSON()` 或 `c.ShouldBindJSON()` 方法
- 类型注解：从Go结构体中提取

### Echo

#### 路由定义模式

```go
package main

import (
    "github.com/labstack/echo/v4"
)

func main() {
    e := echo.New()

    // 简单路由
    e.GET("/users", getUsers)
    e.POST("/users", createUser)
    e.PUT("/users/:id", updateUser)
    e.DELETE("/users/:id", deleteUser)

    // 路由组
    v1 := e.Group("/api/v1")
    v1.GET("/users", getUsers)
    v1.POST("/users", createUser)

    e.Start(":8080")
}

func getUsers(c echo.Context) error {
    // ...
}

func createUser(c echo.Context) error {
    // ...
}

func updateUser(c echo.Context) error {
    id := c.Param("id")
    // ...
}

func deleteUser(c echo.Context) error {
    id := c.Param("id")
    // ...
}
```

#### 识别规则

- 方法调用：`e.GET`, `e.POST`, `e.PUT`, `e.DELETE`, `e.PATCH`
- 路由组：`e.Group()` 创建路由组
- 第一个参数：路由路径
- 第二个参数：处理函数

#### 参数提取

- 路径参数：`c.Param("param_name")` 方法
- 查询参数：`c.QueryParam("param_name")` 或 `c.QueryParams()` 方法
- 请求体参数：`c.Bind()` 方法
- 类型注解：从Go结构体中提取

## 前端框架

### React

#### 组件定义模式

```jsx
// 函数组件
function MyComponent({ prop1, prop2 }) {
  return <div>{prop1}</div>;
}

// 使用 Hooks
function MyComponent({ prop1 }) {
  const [state, setState] = useState(null);
  const handleClick = () => {
    // ...
  };
  return <div onClick={handleClick}>{prop1}</div>;
}

// 类组件
class MyComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = { value: '' };
  }

  handleClick() {
    // ...
  }

  render() {
    return <div onClick={() => this.handleClick()}>{this.props.prop1}</div>;
  }
}

// TypeScript 组件
interface MyComponentProps {
  prop1: string;
  prop2?: number;
}

function MyComponent({ prop1, prop2 }: MyComponentProps) {
  return <div>{prop1}</div>;
}
```

#### 识别规则

- 函数组件：以大写字母开头的函数
- 类组件：继承自 `React.Component` 或 `React.PureComponent` 的类
- Hooks：`useState`, `useEffect`, `useContext`, `useRef`, `useCallback`, `useMemo` 等
- Props：函数参数或 `this.props`
- Events：以 `on` 开头的属性（如 `onClick`, `onChange`）

#### 参数提取

- Props：函数参数或类组件的 `this.props`
- State：`useState` 返回值或类组件的 `this.state`
- Events：以 `on` 开头的属性
- 类型注解：从 TypeScript 接口或类型中提取

### Vue

#### 组件定义模式

```vue
<!-- Options API -->
<template>
  <div>{{ message }}</div>
</template>

<script>
export default {
  name: "MyComponent",
  props: {
    prop1: String,
    prop2: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      message: "Hello",
    };
  },
  methods: {
    handleClick() {
      // ...
    },
  },
  computed: {
    computedValue() {
      return this.message.toUpperCase();
    },
  },
  watch: {
    message(newVal, oldVal) {
      // ...
    },
  },
};
</script>

<!-- Composition API -->
<template>
  <div>{{ message }}</div>
</template>

<script setup>
import { ref, computed, watch } from "vue";

const props = defineProps({
  prop1: String,
  prop2: {
    type: Number,
    default: 0,
  },
});

const emit = defineEmits(["update", "change"]);

const message = ref("Hello");

const computedValue = computed(() => message.value.toUpperCase());

watch(message, (newVal, oldVal) => {
  // ...
});

function handleClick() {
  emit("update", newValue);
}
</script>

<!-- TypeScript 组件 -->
<template>
  <div>{{ message }}</div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";

interface Props {
  prop1: string;
  prop2?: number;
}

const props = withDefaults(defineProps<Props>(), {
  prop2: 0,
});

const emit = defineEmits<{
  update: [value: string];
  change: [value: number];
}>();
</script>
```

#### 识别规则

- Options API：`export default { name, props, data, methods, computed, watch }`
- Composition API：`<script setup>` 和 `defineProps`, `defineEmits`
- Props：`props` 对象或 `defineProps` 函数
- Events：`$emit` 方法或 `defineEmits` 函数
- Slots：`<slot>` 元素
- 类型注解：从 TypeScript 接口或类型中提取

#### 参数提取

- Props：`props` 对象或 `defineProps` 的参数
- Events：`$emit` 调用或 `defineEmits` 的参数
- Slots：`<slot>` 元素
- 类型注解：从 TypeScript 接口或类型中提取

### Angular

#### 组件定义模式

```typescript
import { Component, Input, Output, EventEmitter } from "@angular/core";

@Component({
  selector: "app-my-component",
  template: ` <div>{{ message }}</div> `,
  styles: [
    `
      div {
        color: blue;
      }
    `,
  ],
})
export class MyComponent {
  @Input() prop1: string;
  @Input() prop2: number = 0;

  @Output() update = new EventEmitter<string>();
  @Output() change = new EventEmitter<number>();

  message: string = "Hello";

  handleClick() {
    this.update.emit("new value");
    this.change.emit(123);
  }
}

// 使用 OnPush 变更检测策略
@Component({
  selector: "app-my-component",
  template: `<div>{{ message }}</div>`,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MyComponent {
  @Input() prop1: string;
  message: string = "Hello";
}
```

#### 识别规则

- 装饰器：`@Component`, `@Input`, `@Output`, `@ViewChild`, `@ContentChild`
- 输入属性：`@Input` 装饰器
- 输出属性：`@Output` 装饰器，配合 `EventEmitter`
- 生命周期钩子：`ngOnInit`, `ngOnChanges`, `ngDoCheck`, `ngAfterContentInit`, `ngAfterViewInit`, `ngOnDestroy`
- 类型注解：从 TypeScript 类型中提取

#### 参数提取

- Inputs：`@Input` 装饰器标记的属性
- Outputs：`@Output` 装饰器标记的属性
- Events：`EventEmitter` 的泛型类型
- 类型注解：从 TypeScript 类型中提取

### Svelte

#### 组件定义模式

```svelte
<!-- 基本组件 -->
<script>
  export let prop1;
  export let prop2 = 0;

  let message = 'Hello';

  function handleClick() {
    message = 'New message';
  }
</script>

<div on:click={handleClick}>
  {message}
</div>

<!-- TypeScript 组件 -->
<script lang="ts">
  export let prop1: string;
  export let prop2: number = 0;

  let message: string = 'Hello';

  function handleClick(): void {
    message = 'New message';
  }
</script>

<!-- 事件派发 -->
<script>
  import { createEventDispatcher } from 'svelte';

  export let prop1: string;

  const dispatch = createEventDispatcher();

  function handleClick() {
    dispatch('update', { value: 'new value' });
  }
</script>

<button on:click={handleClick}>
  Click me
</button>

<!-- Slots -->
<div class="container">
  <slot name="header"></slot>
  <slot></slot>
  <slot name="footer"></slot>
</div>
```

#### 识别规则

- Props：`export let` 声明的变量
- Events：`createEventDispatcher()` 创建的派发器
- Slots：`<slot>` 元素
- Reactivity：`$:` 前缀的响应式语句
- Stores：`import { writable, readable, derived } from 'svelte/store'`
- 类型注解：从 TypeScript 类型中提取

#### 参数提取

- Props：`export let` 声明的变量
- Events：`dispatch` 调用
- Slots：`<slot>` 元素
- 类型注解：从 TypeScript 类型中提取

### Next.js

#### API 路由模式

```typescript
// Pages Router (pages/api/)
// pages/api/users.ts
import type { NextApiRequest, NextApiResponse } from "next";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === "GET") {
    // ...
  } else if (req.method === "POST") {
    // ...
  }
}

// 动态路由
// pages/api/users/[id].ts
export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const { id } = req.query;
  // ...
}

// App Router (app/api/)
// app/api/users/route.ts
import { NextResponse } from "next/server";

export async function GET(request: Request) {
  // ...
}

export async function POST(request: Request) {
  const body = await request.json();
  // ...
}

// 动态路由
// app/api/users/[id]/route.ts
export async function GET(
  request: Request,
  { params }: { params: { id: string } },
) {
  const { id } = params;
  // ...
}
```

#### 识别规则

- Pages Router：`pages/api/` 目录下的文件
- App Router：`app/api/` 目录下的 `route.ts` 文件
- 动态路由：方括号 `[param]` 包裹的文件名或目录名
- HTTP方法：导出名为 `GET`, `POST`, `PUT`, `DELETE`, `PATCH` 的函数

#### 参数提取

- 路径参数：`req.query` (Pages Router) 或 `params` (App Router)
- 查询参数：`req.query` (Pages Router) 或 `request.url` (App Router)
- 请求体参数：`req.body` (Pages Router) 或 `request.json()` (App Router)
- 类型注解：从 TypeScript 类型中提取

### Nuxt.js

#### API 路由模式

```typescript
// Nuxt 3 (server/api/)
// server/api/users.get.ts
export default defineEventHandler((event) => {
  // GET 请求
});

// server/api/users.post.ts
export default defineEventHandler((event) => {
  // POST 请求
});

// 动态路由
// server/api/users/[id].get.ts
export default defineEventHandler((event) => {
  const id = getRouterParam(event, "id");
  // ...
});

// 统一处理多种方法
// server/api/users.ts
export default defineEventHandler(async (event) => {
  const method = getMethod(event);

  if (method === "GET") {
    // ...
  } else if (method === "POST") {
    const body = await readBody(event);
    // ...
  }
});
```

#### 识别规则

- API路由：`server/api/` 目录下的文件
- 方法特定路由：`.get.ts`, `.post.ts`, `.put.ts`, `.delete.ts`, `.patch.ts` 后缀
- 动态路由：方括号 `[param]` 包裹的文件名
- 事件处理器：`defineEventHandler` 函数

#### 参数提取

- 路径参数：`getRouterParam(event, 'paramName')`
- 查询参数：`getQuery(event)` 或 `getRouterParam(event, 'query')`
- 请求体参数：`readBody(event)`
- 类型注解：从 TypeScript 类型中提取

## 通用识别策略

### 1. 框架检测

#### 后端框架检测优先级

1. 检测 `from fastapi import` 或 `FastAPI(` → FastAPI
2. 检测 `from flask import` 或 `Flask(` → Flask
3. 检测 `from django.urls import` 或 `from rest_framework import` → Django
4. 检测 `@Controller` 或 `@RestController` → Spring Boot
5. 检测 `@nestjs/common` → NestJS
6. 检测 `github.com/gin-gonic/gin` → Gin
7. 检测 `github.com/labstack/echo/v4` → Echo
8. 检测 `require('express')` 或 `express()` → Express

#### 前端框架检测优先级

1. 检测 `import React` 或 `from 'react'` → React
2. 检测 `<template>` 标签或 `defineProps` → Vue
3. 检测 `@Component` 或 `@angular/core` → Angular
4. 检测 `<script>` 标签且没有 `lang="ts"` → Svelte
5. 检测 `next/server` 或 `pages/api/` → Next.js
6. 检测 `defineEventHandler` 或 `server/api/` → Nuxt.js

### 2. 路由提取

- 使用正则表达式匹配路由定义模式
- 提取路径、方法、函数名
- 记录文件名和行号

### 3. 参数提取

- 根据框架特点提取不同类型的参数
- 优先利用类型注解（TypeScript、FastAPI、NestJS）
- 解析代码中的请求对象调用

### 4. 文档提取

- Python：提取函数的docstring（三引号字符串）
- JavaScript/TypeScript：提取JSDoc注释
- Go：提取函数注释
- Java：提取Javadoc注释

## 限制与建议

### 当前限制

1. 仅识别静态路由，无法完全解析动态路由生成器
2. 参数提取基于简单模式匹配，可能遗漏复杂用法
3. 响应结构无法自动提取，需要手动补充
4. 对于复杂的装饰器链和中间件，识别可能不准确

### 使用建议

1. 在代码中添加清晰的docstring和注释
2. 使用类型注解（TypeScript、FastAPI、NestJS）
3. 对于复杂路由，手动补充文档信息
4. 生成文档后人工审核和补充
5. 使用标准的命名约定和代码结构
6. 为API端点添加描述性的注释和文档字符串
