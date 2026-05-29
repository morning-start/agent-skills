# OpenAPI 3.0 快速参考

## 基本结构

```yaml
openapi: 3.0.3
info:
  title: API 文档
  version: 1.0.0
  description: API 接口文档
servers:
  - url: https://api.example.com/v1
    description: 生产环境
paths:
  /users:
    get:
      summary: 获取用户列表
      responses:
        '200':
          description: 成功
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

---

## 常用数据类型

| 类型 | 说明 | 示例 |
|------|------|------|
| string | 字符串 | "hello" |
| integer | 整数 | 123 |
| number | 浮点数 | 123.45 |
| boolean | 布尔值 | true/false |
| array | 数组 | [1, 2, 3] |
| object | 对象 | {"key": "value"} |

---

## 参数定义

### Query 参数
```yaml
parameters:
  - name: page
    in: query
    required: false
    schema:
      type: integer
      default: 1
      minimum: 1
```

### Path 参数
```yaml
parameters:
  - name: userId
    in: path
    required: true
    schema:
      type: integer
```

### Header 参数
```yaml
parameters:
  - name: Authorization
    in: header
    required: true
    schema:
      type: string
    example: "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Body 参数
```yaml
requestBody:
  required: true
  content:
    application/json:
      schema:
        type: object
        properties:
          username:
            type: string
          password:
            type: string
        required:
          - username
          - password
```

---

## 响应定义

### 成功响应
```yaml
responses:
  '200':
    description: 成功
    content:
      application/json:
        schema:
          type: object
          properties:
            code:
              type: integer
            message:
              type: string
            data:
              type: object
```

### 错误响应
```yaml
responses:
  '400':
    description: 请求参数错误
    content:
      application/json:
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 400
            message:
              type: string
              example: "请求参数错误"
            data:
              type: object
              nullable: true
```

---

## Schema 复用

### 定义组件
```yaml
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        username:
          type: string
        email:
          type: string
          format: email
```

### 引用组件
```yaml
schema:
  $ref: '#/components/schemas/User'
```

---

## 鉴权方式

### JWT Bearer Token
```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

### API Key
```yaml
components:
  securitySchemes:
    apiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key

security:
  - apiKeyAuth: []
```

---

## 数组和枚举

### 数组
```yaml
type: array
items:
  type: string
minItems: 1
maxItems: 100
```

### 枚举
```yaml
type: string
enum:
  - PENDING
  - APPROVED
  - REJECTED
```

---

## 常用关键字

| 关键字 | 说明 |
|--------|------|
| `type` | 数据类型 |
| `format` | 数据格式（如 email、date-time） |
| `description` | 字段描述 |
| `example` | 示例值 |
| `default` | 默认值 |
| `required` | 必填字段 |
| `nullable` | 是否可为 null |
| `minimum` / `maximum` | 最小值 / 最大值 |
| `minLength` / `maxLength` | 最小长度 / 最大长度 |
| `pattern` | 正则表达式（字符串格式） |
| `oneOf` / `anyOf` / `allOf` | 组合类型 |

---

## 完整示例

```yaml
openapi: 3.0.3
info:
  title: 用户管理 API
  version: 1.0.0
  description: 用户管理接口文档

servers:
  - url: https://api.example.com/v1
    description: 生产环境
  - url: https://dev-api.example.com/v1
    description: 开发环境

paths:
  /users:
    get:
      summary: 获取用户列表
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
            minimum: 1
        - name: size
          in: query
          schema:
            type: integer
            default: 10
            minimum: 1
            maximum: 100
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  message:
                    type: string
                  data:
                    type: object
                    properties:
                      users:
                        type: array
                        items:
                          $ref: '#/components/schemas/User'
                      total:
                        type: integer

    post:
      summary: 创建用户
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                  minLength: 3
                  maxLength: 20
                password:
                  type: string
                  minLength: 6
                  maxLength: 20
                email:
                  type: string
                  format: email
              required:
                - username
                - password
                - email
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  message:
                    type: string
                  data:
                    $ref: '#/components/schemas/User'

  /users/{userId}:
    get:
      summary: 获取用户详情
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    $ref: '#/components/schemas/User'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
          description: 用户 ID
        username:
          type: string
          description: 用户名
        email:
          type: string
          format: email
          description: 邮箱
        createdAt:
          type: string
          format: date-time
          description: 创建时间

security:
  - bearerAuth: []
```
