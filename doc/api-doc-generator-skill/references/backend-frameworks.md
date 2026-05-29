# 后端框架 API 文档参考

## 目录

- [概述](#概述)
- [Flask](#flask)
- [FastAPI](#fastapi)
- [Django](#django)
- [Express](#express)
- [NestJS](#nestjs)
- [Spring Boot](#spring-boot)
- [Gin](#gin)
- [Echo](#echo)
- [通用最佳实践](#通用最佳实践)

## 概述

本文档提供了主流后端框架的 API 文档组织方式和路由识别的最佳实践，帮助开发者更好地理解和使用后端框架的 API 文档。

## Flask

### 官方文档结构

Flask 的官方文档（flask.palletsprojects.com）采用以下组织结构：

- **Quickstart** - 快速入门
- **Tutorial** - 教程
- **API** - API 参考
- **Patterns** - 设计模式
- **Deploying** - 部署

### API 文档组织方式

#### 1. 端点概述

```markdown
# Endpoint Name

用于描述 API 端点的主要用途和功能。
```

#### 2. 请求参数

```markdown
## Request Parameters

### Path Parameters

| Parameter | Type   | Required | Description |
| --------- | ------ | -------- | ----------- |
| id        | string | Yes      | 用户 ID     |

### Query Parameters

| Parameter | Type    | Required | Default | Description |
| --------- | ------- | -------- | ------- | ----------- |
| page      | integer | No       | 1       | 页码        |
| limit     | integer | No       | 10      | 每页数量    |

### Body Parameters

| Parameter | Type   | Required | Default | Description |
| --------- | ------ | -------- | ------- | ----------- |
| name      | string | Yes      | -       | 用户名      |
| email     | string | Yes      | -       | 邮箱地址    |
```

#### 3. 响应格式

````markdown
## Response Format

### Success Response

```json
{
  "id": "123",
  "name": "John Doe",
  "email": "john@example.com"
}
```
````

### Error Response

```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "用户不存在"
  }
}
```

````

### 路由识别最佳实践

#### 1. 路由装饰器识别
- `@app.route` 或 `@bp.route` 装饰器
- 第一个参数：路由路径
- `methods` 参数：HTTP 方法

#### 2. 参数提取
- 路径参数：从路由装饰器的路径中提取 `<param_name>`
- 查询参数：查找 `request.args.get()` 调用
- 请求体参数：查找 `request.json.get()` 或 `request.form.get()` 调用

#### 3. 文档提取
- 从函数的 docstring（三引号字符串）中提取文档

### 文档生成建议

1. **使用 docstring 注释**
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/users', methods=['GET', 'POST'])
def users():
    """
    获取用户列表或创建新用户

    GET 请求：
    - page: 页码（默认 1）
    - limit: 每页数量（默认 10）

    POST 请求：
    - name: 用户名（必需）
    - email: 邮箱地址（必需）
    """
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        users = get_users(page, limit)
        return jsonify(users)
    elif request.method == 'POST':
        data = request.get_json()
        user = create_user(data)
        return jsonify(user), 201
````

2. **使用 Marshmallow 序列化**

```python
from flask import Flask, request, jsonify
from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    email = fields.Email(required=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users = get_users()
        return jsonify(users_schema.dump(users))
    elif request.method == 'POST':
        data = user_schema.load(request.get_json())
        user = create_user(data)
        return jsonify(user_schema.dump(user)), 201
```

## FastAPI

### 官方文档结构

FastAPI 的官方文档（fastapi.tiangolo.com）采用以下组织结构：

- **Tutorial** - 教程
- **Advanced User Guide** - 高级用户指南
- **API Reference** - API 参考
- **Project Generation** - 项目生成
- **Deployment** - 部署

### API 文档组织方式

#### 1. 端点概述

```markdown
# Endpoint Name

用于描述 API 端点的主要用途和功能。
```

#### 2. 请求参数

```markdown
## Request Parameters

### Path Parameters

| Parameter | Type    | Required | Description |
| --------- | ------- | -------- | ----------- |
| user_id   | integer | Yes      | 用户 ID     |

### Query Parameters

| Parameter | Type    | Required | Default | Description  |
| --------- | ------- | -------- | ------- | ------------ |
| skip      | integer | No       | 0       | 跳过的记录数 |
| limit     | integer | No       | 100     | 返回的记录数 |

### Body Parameters

| Parameter | Type   | Required | Default | Description |
| --------- | ------ | -------- | ------- | ----------- |
| name      | string | Yes      | -       | 用户名      |
| email     | string | Yes      | -       | 邮箱地址    |
```

#### 3. 响应格式

````markdown
## Response Format

### Success Response

```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com"
}
```
````

### Error Response

```json
{
  "detail": "User not found"
}
```

````

### 路由识别最佳实践

#### 1. 路由装饰器识别
- `@app.get`, `@app.post`, `@app.put`, `@app.delete`, `@app.patch` 装饰器
- 第一个参数：路由路径
- 函数签名中的参数：自动识别为查询参数或路径参数

#### 2. 参数提取
- 路径参数：路径中的 `{param_name}`
- 查询参数：函数签名中非路径参数且有默认值
- 请求体参数：函数签名中的 Pydantic 模型参数
- 类型注解：从类型注解中提取参数类型

#### 3. 文档提取
- 从函数的 docstring 中提取文档
- 从 Pydantic 模型的 Field 描述中提取文档

### 文档生成建议

1. **使用 Pydantic 模型**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class UserCreate(BaseModel):
    name: str = Field(..., description="用户名")
    email: str = Field(..., description="邮箱地址")

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    """
    创建新用户

    - **name**: 用户名
    - **email**: 邮箱地址
    """
    new_user = create_user_in_db(user)
    return new_user
````

2. **使用自动文档生成**

```python
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI()

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )
```

## Django

### 官方文档结构

Django 的官方文档（docs.djangoproject.com）采用以下组织结构：

- **Getting started** - 快速入门
- **The Model Layer** - 模型层
- **Views and URLconfs** - 视图和 URL 配置
- **Forms** - 表单
- **The Django REST Framework** - Django REST 框架

### API 文档组织方式

#### 1. 端点概述

```markdown
# Endpoint Name

用于描述 API 端点的主要用途和功能。
```

#### 2. 请求参数

```markdown
## Request Parameters

### Path Parameters

| Parameter | Type    | Required | Description |
| --------- | ------- | -------- | ----------- |
| id        | integer | Yes      | 用户 ID     |

### Query Parameters

| Parameter | Type    | Required | Default | Description |
| --------- | ------- | -------- | ------- | ----------- |
| page      | integer | No       | 1       | 页码        |
| page_size | integer | No       | 10      | 每页数量    |

### Body Parameters

| Parameter | Type   | Required | Default | Description |
| --------- | ------ | -------- | ------- | ----------- |
| name      | string | Yes      | -       | 用户名      |
| email     | string | Yes      | -       | 邮箱地址    |
```

#### 3. 响应格式

````markdown
## Response Format

### Success Response

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```
````

### Error Response

```json
{
  "detail": "Not found."
}
```

````

### 路由识别最佳实践

#### 1. URL 配置识别
- `path()`, `re_path()`, `url()` 函数
- 第一个参数：路由路径
- 第二个参数：视图函数或视图类

#### 2. 参数提取
- 路径参数：URL 模式中的 `<param_name>` 或 `<type:param_name>`
- 查询参数：`request.GET` 或 `request.query_params`
- 请求体参数：`request.data` 或 `request.POST`
- 类型注解：从序列化器（Serializer）中提取

#### 3. 文档提取
- 从视图函数的 docstring 中提取文档
- 从序列化器的 Field 描述中提取文档

### 文档生成建议

1. **使用 Django REST Framework**
```python
from rest_framework import serializers, viewsets
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserViewSet(viewsets.ModelViewSet):
    """
    API 端点，允许用户被查看或编辑。
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
````

2. **使用 drf-spectacular**

```python
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
    @extend_schema(
        summary="获取用户列表",
        description="返回所有用户的列表",
        parameters=[
            OpenApiParameter(
                name="page",
                type=int,
                description="页码",
                required=False,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
```

## Express

### 官方文档结构

Express 的官方文档（expressjs.com）采用以下组织结构：

- **Getting started** - 快速入门
- **Guide** - 指南
- **API reference** - API 参考
- **Advanced topics** - 高级主题
- **Resources** - 资源

### API 文档组织方式

#### 1. 端点概述

```markdown
# Endpoint Name

用于描述 API 端点的主要用途和功能。
```

#### 2. 请求参数

```markdown
## Request Parameters

### Path Parameters

| Parameter | Type   | Required | Description |
| --------- | ------ | -------- | ----------- |
| id        | string | Yes      | 用户 ID     |

### Query Parameters

| Parameter | Type   | Required | Default | Description |
| --------- | ------ | -------- | ------- | ----------- |
| page      | number | No       | 1       | 页码        |
| limit     | number | No       | 10      | 每页数量    |

### Body Parameters

| Parameter | Type   | Required | Default | Description |
| --------- | ------ | -------- | ------- | ----------- |
| name      | string | Yes      | -       | 用户名      |
| email     | string | Yes      | -       | 邮箱地址    |
```

#### 3. 响应格式

````markdown
## Response Format

### Success Response

```json
{
  "id": "123",
  "name": "John Doe",
  "email": "john@example.com"
}
```
````

### Error Response

```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "用户不存在"
  }
}
```

````

### 路由识别最佳实践

#### 1. 路由方法识别
- `app.get`, `app.post`, `app.put`, `app.delete`, `app.patch` 方法
- 或 `router.get`, `router.post` 等
- 第一个参数：路由路径
- 第二个参数：回调函数

#### 2. 参数提取
- 路径参数：路径中的 `:param_name` 格式
- 查询参数：`req.query` 属性
- 请求体参数：`req.body` 属性

#### 3. 文档提取
- 从路由定义前的注释（`//` 或 `/* */`）中提取文档

### 文档生成建议

1. **使用 JSDoc 注释**
```javascript
/**
 * @route GET /users
 * @summary 获取用户列表
 * @param {number} page.query - 页码
 * @param {number} limit.query - 每页数量
 * @returns {Array<User>} 200 - 用户列表
 */
app.get('/users', async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 10;
  const users = await getUsers(page, limit);
  res.json(users);
});

/**
 * @route POST /users
 * @summary 创建新用户
 * @param {UserCreate.model} body.body.required - 用户数据
 * @returns {User} 201 - 创建的用户
 */
app.post('/users', async (req, res) => {
  const user = await createUser(req.body);
  res.status(201).json(user);
});
````

2. **使用 Swagger**

```javascript
const swaggerUi = require("swagger-ui-express");
const swaggerDocument = require("./swagger.json");

app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerDocument));
```

## NestJS

### 官方文档结构

NestJS 的官方文档（docs.nestjs.com）采用以下组织结构：

- **Overview** - 概述
- **First Steps** - 第一步
- **Fundamentals** - 基础知识
- **Techniques** - 技术
- **OpenAPI (Swagger)** - OpenAPI (Swagger)

### API 文档组织方式

#### 1. 端点概述

```markdown
# Endpoint Name

用于描述 API 端点的主要用途和功能。
```

#### 2. 请求参数

```markdown
## Request Parameters

### Path Parameters

| Parameter | Type   | Required | Description |
| --------- | ------ | -------- | ----------- |
| id        | string | Yes      | 用户 ID     |

### Query Parameters

| Parameter | Type   | Required | Default | Description |
| --------- | ------ | -------- | ------- | ----------- |
| page      | number | No       | 1       | 页码        |
| limit     | number | No       | 10      | 每页数量    |

### Body Parameters

| Parameter | Type   | Required | Default | Description |
| --------- | ------ | -------- | ------- | ----------- |
| name      | string | Yes      | -       | 用户名      |
| email     | string | Yes      | -       | 邮箱地址    |
```

#### 3. 响应格式

````markdown
## Response Format

### Success Response

```json
{
  "id": "123",
  "name": "John Doe",
  "email": "john@example.com"
}
```
````

### Error Response

```json
{
  "statusCode": 404,
  "message": "User not found",
  "error": "Not Found"
}
```

````

### 路由识别最佳实践

#### 1. 装饰器识别
- `@Controller`, `@Get`, `@Post`, `@Put`, `@Delete`, `@Patch` 装饰器
- 类装饰器：`@Controller` 指定基础路径
- 方法装饰器：`@Get`, `@Post` 等指定具体路由和 HTTP 方法
- 参数装饰器：`@Param`, `@Body`, `@Query`, `@Headers`

#### 2. 参数提取
- 路径参数：`@Param('param_name')` 装饰器
- 查询参数：`@Query('param_name')` 装饰器
- 请求体参数：`@Body()` 装饰器，配合 DTO 类
- 类型注解：从 DTO 类的 TypeScript 类型中提取

#### 3. 文档提取
- 从装饰器的参数中提取文档
- 从 DTO 类的属性装饰器中提取文档

### 文档生成建议

1. **使用 DTO 类**
```typescript
import { IsString, IsEmail } from 'class-validator';

export class CreateUserDto {
  @ApiProperty({ description: '用户名' })
  @IsString()
  name: string;

  @ApiProperty({ description: '邮箱地址' })
  @IsEmail()
  email: string;
}

export class UserResponseDto {
  @ApiProperty({ description: '用户 ID' })
  id: string;

  @ApiProperty({ description: '用户名' })
  name: string;

  @ApiProperty({ description: '邮箱地址' })
  email: string;
}
````

2. **使用 Swagger 装饰器**

```typescript
import { ApiTags, ApiOperation, ApiParam, ApiQuery } from "@nestjs/swagger";

@Controller("users")
@ApiTags("users")
export class UsersController {
  @Get()
  @ApiOperation({ summary: "获取用户列表" })
  @ApiQuery({ name: "page", required: false, type: Number })
  @ApiQuery({ name: "limit", required: false, type: Number })
  findAll(@Query("page") page: number, @Query("limit") limit: number) {
    return this.usersService.findAll(page, limit);
  }

  @Get(":id")
  @ApiOperation({ summary: "获取用户详情" })
  @ApiParam({ name: "id", description: "用户 ID" })
  findOne(@Param("id") id: string) {
    return this.usersService.findOne(id);
  }
}
```

## Spring Boot

### 官方文档结构

Spring Boot 的官方文档（spring.io/projects/spring-boot）采用以下组织结构：

- **Getting Started** - 快速入门
- **Using Spring Boot** - 使用 Spring Boot
- **Spring Boot Features** - Spring Boot 特性
- **Production-Ready Features** - 生产就绪特性
- **Spring Boot Actuator** - Spring Boot Actuator

### API 文档组织方式

#### 1. 端点概述

```markdown
# Endpoint Name

用于描述 API 端点的主要用途和功能。
```

#### 2. 请求参数

```markdown
## Request Parameters

### Path Parameters

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| id        | Long | Yes      | 用户 ID     |

### Query Parameters

| Parameter | Type | Required | Default | Description |
| --------- | ---- | -------- | ------- | ----------- |
| page      | int  | No       | 1       | 页码        |
| size      | int  | No       | 10      | 每页数量    |

### Body Parameters

| Parameter | Type   | Required | Default | Description |
| --------- | ------ | -------- | ------- | ----------- |
| name      | String | Yes      | -       | 用户名      |
| email     | String | Yes      | -       | 邮箱地址    |
```

#### 3. 响应格式

````markdown
## Response Format

### Success Response

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```
````

### Error Response

```json
{
  "timestamp": "2025-03-06T12:00:00.000+00:00",
  "status": 404,
  "error": "Not Found",
  "message": "User not found",
  "path": "/api/users/1"
}
```

````

### 路由识别最佳实践

#### 1. 注解识别
- 类注解：`@RestController`, `@Controller`
- 路径注解：`@RequestMapping`, `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`, `@PatchMapping`
- 参数注解：`@PathVariable`, `@RequestBody`, `@RequestParam`, `@RequestHeader`

#### 2. 参数提取
- 路径参数：`@PathVariable` 注解
- 查询参数：`@RequestParam` 注解
- 请求体参数：`@RequestBody` 注解
- 类型注解：从 Java 类型中提取

#### 3. 文档提取
- 从注解的参数中提取文档
- 从 Javadoc 注释中提取文档

### 文档生成建议

1. **使用 SpringDoc OpenAPI**
```java
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;

@RestController
@RequestMapping("/api/users")
@Tag(name = "users", description = "用户管理 API")
public class UserController {

    @GetMapping
    @Operation(summary = "获取用户列表", description = "返回所有用户的列表")
    public List<User> getAllUsers(
            @Parameter(description = "页码") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "每页数量") @RequestParam(defaultValue = "10") int size) {
        return userService.findAll(page, size);
    }

    @GetMapping("/{id}")
    @Operation(summary = "获取用户详情", description = "根据 ID 获取用户信息")
    public User getUserById(
            @Parameter(description = "用户 ID") @PathVariable Long id) {
        return userService.findById(id);
    }
}
````

2. **使用 DTO 类**

```java
import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "创建用户请求")
public class CreateUserRequest {
    @Schema(description = "用户名", required = true)
    private String name;

    @Schema(description = "邮箱地址", required = true)
    private String email;

    // getters and setters
}
```

## Gin

### 官方文档结构

Gin 的官方文档（gin-gonic.com/docs）采用以下组织结构：

- **Introduction** - 介绍
- **Installation** - 安装
- **Quick Start** - 快速开始
- **API Examples** - API 示例
- **FAQ** - 常见问题

### API 文档组织方式

#### 1. 端点概述

```markdown
# Endpoint Name

用于描述 API 端点的主要用途和功能。
```

#### 2. 请求参数

```markdown
## Request Parameters

### Path Parameters

| Parameter | Type   | Required | Description |
| --------- | ------ | -------- | ----------- |
| id        | string | Yes      | 用户 ID     |

### Query Parameters

| Parameter | Type | Required | Default | Description |
| --------- | ---- | -------- | ------- | ----------- |
| page      | int  | No       | 1       | 页码        |
| limit     | int  | No       | 10      | 每页数量    |

### Body Parameters

| Parameter | Type   | Required | Default | Description |
| --------- | ------ | -------- | ------- | ----------- |
| name      | string | Yes      | -       | 用户名      |
| email     | string | Yes      | -       | 邮箱地址    |
```

#### 3. 响应格式

````markdown
## Response Format

### Success Response

```json
{
  "id": "123",
  "name": "John Doe",
  "email": "john@example.com"
}
```
````

### Error Response

```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "用户不存在"
  }
}
```

````

### 路由识别最佳实践

#### 1. 方法调用识别
- `r.GET`, `r.POST`, `r.PUT`, `r.DELETE`, `r.PATCH` 方法
- 路由组：`r.Group()` 创建路由组
- 第一个参数：路由路径
- 第二个参数：处理函数

#### 2. 参数提取
- 路径参数：`c.Param("param_name")` 方法
- 查询参数：`c.Query("param_name")` 或 `c.DefaultQuery()` 方法
- 请求体参数：`c.BindJSON()` 或 `c.ShouldBindJSON()` 方法
- 类型注解：从 Go 结构体中提取

#### 3. 文档提取
- 从函数注释中提取文档
- 从结构体标签中提取文档

### 文档生成建议

1. **使用结构体标签**
```go
package main

import (
    "github.com/gin-gonic/gin"
)

type User struct {
    ID    string `json:"id" example:"123"`
    Name  string `json:"name" binding:"required" example:"John Doe"`
    Email string `json:"email" binding:"required,email" example:"john@example.com"`
}

type CreateUserRequest struct {
    Name  string `json:"name" binding:"required" example:"John Doe"`
    Email string `json:"email" binding:"required,email" example:"john@example.com"`
}

func main() {
    r := gin.Default()

    r.GET("/users", getUsers)
    r.POST("/users", createUser)
    r.GET("/users/:id", getUser)

    r.Run(":8080")
}

func getUsers(c *gin.Context) {
    page := c.DefaultQuery("page", "1")
    limit := c.DefaultQuery("limit", "10")
    users := getUsersFromDB(page, limit)
    c.JSON(200, users)
}

func createUser(c *gin.Context) {
    var req CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(400, gin.H{"error": err.Error()})
        return
    }
    user := createUserInDB(req)
    c.JSON(201, user)
}

func getUser(c *gin.Context) {
    id := c.Param("id")
    user := getUserFromDB(id)
    if user == nil {
        c.JSON(404, gin.H{"error": "User not found"})
        return
    }
    c.JSON(200, user)
}
````

2. **使用 Swagger**

```go
import (
    "github.com/gin-gonic/gin"
    swagFiles "github.com/swaggo/files"
    ginSwagger "github.com/swaggo/gin-swagger"

    _ "your-project/docs"
)

func main() {
    r := gin.Default()

    r.GET("/swagger/*any", ginSwagger.WrapHandler(swagFiles.Handler))

    r.Run(":8080")
}
```

## Echo

### 官方文档结构

Echo 的官方文档（echo.labstack.com/docs）采用以下组织结构：

- **Guide** - 指南
- **Routing** - 路由
- **Middleware** - 中间件
- **Request** - 请求
- **Response** - 响应

### API 文档组织方式

#### 1. 端点概述

```markdown
# Endpoint Name

用于描述 API 端点的主要用途和功能。
```

#### 2. 请求参数

```markdown
## Request Parameters

### Path Parameters

| Parameter | Type   | Required | Description |
| --------- | ------ | -------- | ----------- |
| id        | string | Yes      | 用户 ID     |

### Query Parameters

| Parameter | Type | Required | Default | Description |
| --------- | ---- | -------- | ------- | ----------- |
| page      | int  | No       | 1       | 页码        |
| limit     | int  | No       | 10      | 每页数量    |

### Body Parameters

| Parameter | Type   | Required | Default | Description |
| --------- | ------ | -------- | ------- | ----------- |
| name      | string | Yes      | -       | 用户名      |
| email     | string | Yes      | -       | 邮箱地址    |
```

#### 3. 响应格式

````markdown
## Response Format

### Success Response

```json
{
  "id": "123",
  "name": "John Doe",
  "email": "john@example.com"
}
```
````

### Error Response

```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "用户不存在"
  }
}
```

````

### 路由识别最佳实践

#### 1. 方法调用识别
- `e.GET`, `e.POST`, `e.PUT`, `e.DELETE`, `e.PATCH` 方法
- 路由组：`e.Group()` 创建路由组
- 第一个参数：路由路径
- 第二个参数：处理函数

#### 2. 参数提取
- 路径参数：`c.Param("param_name")` 方法
- 查询参数：`c.QueryParam("param_name")` 或 `c.QueryParams()` 方法
- 请求体参数：`c.Bind()` 方法
- 类型注解：从 Go 结构体中提取

#### 3. 文档提取
- 从函数注释中提取文档
- 从结构体标签中提取文档

### 文档生成建议

1. **使用结构体标签**
```go
package main

import (
    "github.com/labstack/echo/v4"
)

type User struct {
    ID    string `json:"id" example:"123"`
    Name  string `json:"name" validate:"required" example:"John Doe"`
    Email string `json:"email" validate:"required,email" example:"john@example.com"`
}

type CreateUserRequest struct {
    Name  string `json:"name" validate:"required" example:"John Doe"`
    Email string `json:"email" validate:"required,email" example:"john@example.com"`
}

func main() {
    e := echo.New()

    e.GET("/users", getUsers)
    e.POST("/users", createUser)
    e.GET("/users/:id", getUser)

    e.Start(":8080")
}

func getUsers(c echo.Context) error {
    page := c.QueryParam("page")
    limit := c.QueryParam("limit")
    users := getUsersFromDB(page, limit)
    return c.JSON(200, users)
}

func createUser(c echo.Context) error {
    var req CreateUserRequest
    if err := c.Bind(&req); err != nil {
        return c.JSON(400, map[string]string{"error": err.Error()})
    }
    user := createUserInDB(req)
    return c.JSON(201, user)
}

func getUser(c echo.Context) error {
    id := c.Param("id")
    user := getUserFromDB(id)
    if user == nil {
        return c.JSON(404, map[string]string{"error": "User not found"})
    }
    return c.JSON(200, user)
}
````

2. **使用 Swagger**

```go
import (
    "github.com/labstack/echo/v4"
    echoSwagger "github.com/swaggo/echo-swagger"

    _ "your-project/docs"
)

func main() {
    e := echo.New()

    e.GET("/swagger/*", echoSwagger.WrapHandler)

    e.Start(":8080")
}
```

## 通用最佳实践

### 1. 文档结构

#### API 文档应包含：

- 端点概述
- 请求参数（路径、查询、请求体）
- 响应格式
- 错误处理
- 使用示例
- 认证方式

### 2. 类型注解

- 始终使用类型注解（TypeScript、Python 类型注解、Java 类型、Go 结构体）
- 为请求和响应定义类型
- 使用验证库（如 Pydantic、class-validator、Hibernate Validator）

### 3. 注释规范

- 使用框架特定的注释格式（JSDoc、docstring、Javadoc）
- 为公共 API 提供描述性注释
- 说明参数的类型、默认值和用途
- 提供使用示例

### 4. 示例代码

- 提供完整、可运行的示例
- 展示常见使用场景
- 包含错误处理
- 说明最佳实践

### 5. 文档生成工具

- **Swagger/OpenAPI**: 用于 RESTful API 文档
- **SpringDoc**: 用于 Spring Boot API 文档
- **drf-spectacular**: 用于 Django REST Framework 文档
- **swaggo**: 用于 Go Echo/Gin 文档
- **FastAPI 自动文档**: 用于 FastAPI 文档

### 6. 自动化文档生成

- 从代码注释自动生成文档
- 使用 CI/CD 自动更新文档
- 保持文档与代码同步
- 定期审查和更新文档

### 7. RESTful 设计原则

- 使用合适的 HTTP 方法（GET、POST、PUT、DELETE、PATCH）
- 使用语义化的 URL 路径
- 使用合适的 HTTP 状态码
- 提供一致的响应格式
- 支持分页、过滤、排序

### 8. 错误处理

- 提供清晰的错误消息
- 使用标准的错误代码
- 包含错误详情和建议
- 记录错误日志

### 9. 认证和授权

- 使用标准的认证方式（API Key、OAuth 2.0、JWT）
- 在文档中说明认证方式
- 提供认证示例
- 说明权限要求

### 10. 版本控制

- 使用 URL 路径版本控制（如 `/api/v1/`）
- 在文档中说明版本策略
- 提供版本迁移指南
- 保持向后兼容性
