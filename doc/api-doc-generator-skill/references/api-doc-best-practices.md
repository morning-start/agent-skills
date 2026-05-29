# API 文档最佳实践

## 目录

- [概述](#概述)
- [文档结构](#文档结构)
- [内容规范](#内容规范)
- [格式规范](#格式规范)
- [示例代码](#示例代码)
- [自动化工具](#自动化工具)
- [维护与更新](#维护与更新)
- [常见问题](#常见问题)

## 概述

本文档汇总了各框架的 API 文档最佳实践，提供文档组织建议和行业标准格式示例，帮助开发者创建高质量、易维护的 API 文档。

## 文档结构

### 1. 标准文档结构

一个完整的 API 文档应包含以下章节：

#### 1.1 概述（Overview）

- API 的用途和目标
- 支持的使用场景
- 前提条件（如注册账号、获取 API Key 等）
- 支持的协议（如 REST、GraphQL、gRPC 等）
- 快速开始指南

#### 1.2 认证方式（Authentication）

- 使用的认证机制（如 API Key、OAuth 2.0、JWT、Basic Auth 等）
- 如何获取凭证
- 请求头或参数中如何传递认证信息
- 示例（带认证的请求）

#### 1.3 基础信息（Base Info）

- API 的根路径（如 https://api.example.com/v1）
- 各个资源的端点（Endpoints）列表
- 请求与响应格式说明

#### 1.4 端点详情（Endpoints）

对每个 API 端点提供：

- 路径（如 /users/{id}）
- 方法（GET/POST 等）
- 描述（功能说明）
- 路径参数、查询参数、请求体参数
- 示例请求和响应
- 错误码及含义

#### 1.5 错误处理（Error Handling）

- 统一的错误响应格式
- 错误代码与人类可读信息
- 常见错误场景及解决建议

#### 1.6 速率限制（Rate Limiting）

- 每分钟/小时允许的请求数
- 超限后的响应
- 如何查看当前使用情况

#### 1.7 变更日志（Changelog）

- 版本更新记录
- 新增、修改、废弃的接口说明

#### 1.8 支持与反馈（Support）

- 联系方式
- 报告 Bug 或提需求的渠道

### 2. 文件组织规范

```
api/
├── overview.md
├── authentication.md
├── base-info.md
├── endpoints/
│   ├── users.md
│   ├── products.md
│   └── ...
├── error-handling.md
├── rate-limiting.md
├── changelog.md
└── support.md
```

## 内容规范

### 1. 端点文档格式

每个 API 端点应包含以下信息：

#### 1.1 基本信息

- **方法**：GET/POST/PUT/DELETE/PATCH
- **路径**：`/users/{id}`
- **描述**：获取指定用户的信息
- **功能**：根据用户 ID 返回用户详细信息

#### 1.2 请求参数

##### 路径参数

| 参数名 | 类型   | 必填 | 说明    |
| ------ | ------ | ---- | ------- |
| id     | string | 是   | 用户 ID |

##### 查询参数

| 参数名 | 类型   | 必填 | 默认值 | 说明                   |
| ------ | ------ | ---- | ------ | ---------------------- |
| fields | string | 否   | 无     | 指定返回字段，逗号分隔 |

##### 请求体参数

| 参数名 | 类型   | 必填 | 默认值 | 说明     |
| ------ | ------ | ---- | ------ | -------- |
| name   | string | 是   | -      | 用户名   |
| email  | string | 是   | -      | 邮箱地址 |

#### 1.3 请求示例

##### cURL

```bash
curl -X GET https://api.example.com/v1/users/123 \
  -H "Authorization: Bearer YOUR_API_KEY"
```

##### JavaScript (Fetch)

```javascript
fetch("https://api.example.com/v1/users/123", {
  method: "GET",
  headers: {
    Authorization: "Bearer YOUR_API_KEY",
  },
})
  .then((response) => response.json())
  .then((data) => console.log(data));
```

##### Python (Requests)

```python
import requests

url = 'https://api.example.com/v1/users/123'
headers = {
    'Authorization': 'Bearer YOUR_API_KEY'
}
response = requests.get(url, headers=headers)
result = response.json()
print(result)
```

#### 1.4 响应格式

##### 成功响应

**状态码**：200 OK

```json
{
  "id": "123",
  "name": "John Doe",
  "email": "john@example.com"
}
```

##### 错误响应

**状态码**：404 Not Found

```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "用户不存在"
  }
}
```

#### 1.5 状态码说明

| 状态码 | 说明           |
| ------ | -------------- |
| 200    | 请求成功       |
| 201    | 创建成功       |
| 400    | 请求参数错误   |
| 401    | 未授权         |
| 403    | 禁止访问       |
| 404    | 资源不存在     |
| 500    | 服务器内部错误 |

### 2. 错误码格式

| 错误码 | 说明         | 解决方法           |
| ------ | ------------ | ------------------ |
| 400    | 请求参数错误 | 检查请求参数格式   |
| 401    | 未授权       | 检查认证信息       |
| 404    | 资源不存在   | 确认资源ID是否正确 |
| 500    | 服务器错误   | 稍后重试或联系支持 |

## 格式规范

### 1. 命名规范

#### 1.1 URL 路径

- 使用小写字母
- 使用连字符（-）分隔单词
- 使用复数形式表示资源集合
- 使用单数形式表示单个资源

示例：

- ✅ `/users`
- ✅ `/users/{id}`
- ✅ `/user-profiles`
- ❌ `/Users`
- ❌ `/user_profiles`
- ❌ `/user`

#### 1.2 参数名

- 使用小写字母
- 使用下划线（\_）分隔单词（Python 风格）
- 或使用驼峰命名法（JavaScript 风格）

示例：

- ✅ `user_id`
- ✅ `userId`
- ❌ `UserID`
- ❌ `user-id`

#### 1.3 错误码

- 使用大写字母
- 使用下划线（\_）分隔单词
- 使用描述性的名称

示例：

- ✅ `USER_NOT_FOUND`
- ✅ `INVALID_PARAMETER`
- ❌ `user_not_found`
- ❌ `UserNotFound`

### 2. 类型说明

#### 2.1 基本类型

- `string`：字符串
- `number` / `integer`：数字
- `boolean`：布尔值
- `array`：数组
- `object`：对象

#### 2.2 复杂类型

- 使用嵌套结构描述复杂对象
- 使用数组类型 `array<string>` 或 `string[]`
- 使用枚举类型 `enum('value1', 'value2')`

示例：

```json
{
  "name": "string",
  "age": "integer",
  "isActive": "boolean",
  "tags": "array<string>",
  "profile": {
    "bio": "string",
    "avatar": "string"
  }
}
```

### 3. 必填/可选说明

- **必填**：使用"是"或"Required"标记
- **可选**：使用"否"或"Optional"标记
- **默认值**：提供默认值（如果有）

示例：
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| name | string | 是 | - | 用户名 |
| age | integer | 否 | 0 | 年龄 |

## 示例代码

### 1. 完整的端点文档示例

```markdown
# 获取用户信息

## 基本信息

- **方法**：GET
- **路径**：`/users/{id}`
- **描述**：获取指定用户的信息
- **功能**：根据用户 ID 返回用户详细信息

## 请求

### 请求头
```

Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

````

### 路径参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | string | 是 | 用户 ID |

### 查询参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| fields | string | 否 | 无 | 指定返回字段，逗号分隔 |

### 请求体

无

## 请求示例

### cURL

```bash
curl -X GET https://api.example.com/v1/users/123 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY"
````

### JavaScript (Fetch)

```javascript
fetch("https://api.example.com/v1/users/123", {
  method: "GET",
  headers: {
    "Content-Type": "application/json",
    Authorization: "Bearer YOUR_API_KEY",
  },
})
  .then((response) => response.json())
  .then((data) => console.log(data));
```

### Python (Requests)

```python
import requests

url = 'https://api.example.com/v1/users/123'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY'
}
response = requests.get(url, headers=headers)
result = response.json()
print(result)
```

## 响应

### 成功响应

**状态码**：200 OK

```json
{
  "id": "123",
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "isActive": true
}
```

### 错误响应

**状态码**：404 Not Found

```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "用户不存在"
  }
}
```

## 响应参数说明

| 参数名   | 类型    | 说明     |
| -------- | ------- | -------- |
| id       | string  | 用户 ID  |
| name     | string  | 用户名   |
| email    | string  | 邮箱地址 |
| age      | integer | 年龄     |
| isActive | boolean | 是否激活 |

## 状态码说明

| 状态码 | 说明           |
| ------ | -------------- |
| 200    | 请求成功       |
| 401    | 未授权         |
| 404    | 资源不存在     |
| 500    | 服务器内部错误 |

## 注意事项

1. 用户 ID 必须是有效的 UUID 格式
2. 如果用户不存在，返回 404 错误
3. 使用 `fields` 参数可以指定返回的字段，多个字段用逗号分隔

## 相关端点

- [创建用户](./create-user.md)
- [更新用户](./update-user.md)
- [删除用户](./delete-user.md)

````

## 自动化工具

### 1. 文档生成工具

#### 1.1 Swagger/OpenAPI
- **用途**：RESTful API 文档生成
- **支持框架**：FastAPI、Express、NestJS、Spring Boot、Gin、Echo
- **特点**：
  - 自动生成交互式文档
  - 支持多种输出格式（JSON、YAML）
  - 提供客户端 SDK 生成

#### 1.2 SpringDoc
- **用途**：Spring Boot API 文档生成
- **支持框架**：Spring Boot
- **特点**：
  - 集成 Swagger UI
  - 自动从注解生成文档
  - 支持 OpenAPI 3.0

#### 1.3 drf-spectacular
- **用途**：Django REST Framework 文档生成
- **支持框架**：Django REST Framework
- **特点**：
  - 自动生成 OpenAPI schema
  - 支持自定义 schema
  - 提供丰富的配置选项

#### 1.4 swaggo
- **用途**：Go API 文档生成
- **支持框架**：Gin、Echo
- **特点**：
  - 从注释生成文档
  - 支持多种输出格式
  - 集成 Swagger UI

#### 1.5 FastAPI 自动文档
- **用途**：FastAPI API 文档生成
- **支持框架**：FastAPI
- **特点**：
  - 自动生成文档
  - 支持 Swagger UI 和 ReDoc
  - 从类型注解生成文档

### 2. 文档托管工具

#### 2.1 Storybook
- **用途**：组件文档和可视化
- **支持框架**：React、Vue、Angular、Svelte
- **特点**：
  - 交互式组件预览
  - 自动生成文档
  - 支持多种插件

#### 2.2 VuePress
- **用途**：Vue 项目文档
- **支持框架**：Vue
- **特点**：
  - 基于 Vue 构建
  - 支持 Markdown
  - 提供默认主题

#### 2.3 Docusaurus
- **用途**：通用项目文档
- **支持框架**：React
- **特点**：
  - 基于 React 构建
  - 支持 Markdown
  - 提供默认主题

### 3. 文档质量检查工具

#### 3.1 spectral
- **用途**：OpenAPI 规范检查
- **特点**：
  - 检查 API 规范是否符合标准
  - 提供自定义规则
  - 支持多种输出格式

#### 3.2 redocly
- **用途**：OpenAPI 文档检查
- **特点**：
  - 检查文档质量
  - 提供文档预览
  - 支持多种输出格式

## 维护与更新

### 1. 文档更新流程

#### 1.1 代码变更时
1. 更新代码实现
2. 更新 API 文档
3. 运行文档生成工具
4. 审查生成的文档
5. 提交代码和文档

#### 1.2 定期审查
1. 每月审查一次文档
2. 检查文档是否与代码同步
3. 更新过时的示例
4. 添加新的端点文档
5. 标记废弃的端点

### 2. 版本管理

#### 2.1 版本号规范
遵循语义化版本规范（SemVer）：
- `MAJOR.MINOR.PATCH`
- MAJOR：不兼容的 API 变更
- MINOR：向下兼容的功能新增
- PATCH：向下兼容的问题修复

#### 2.2 版本策略
- 使用 URL 路径版本控制（如 `/api/v1/`）
- 保持向后兼容性
- 提供版本迁移指南
- 标记废弃的 API

### 3. 变更日志

#### 3.1 变更日志格式
```markdown
## [1.1.0] - 2025-03-06

### Added
- 新增用户搜索端点
- 支持批量创建用户

### Changed
- 更新用户端点响应格式
- 优化性能

### Deprecated
- 废弃旧的认证方式

### Removed
- 移除旧的认证方式

### Fixed
- 修复用户列表分页问题
````

## 常见问题

### 1. 如何处理可选参数？

#### 方法 1：使用默认值

```python
def get_users(page: int = 1, limit: int = 10):
    pass
```

#### 方法 2：使用 Optional 类型

```python
from typing import Optional

def get_users(page: Optional[int] = None, limit: Optional[int] = None):
    if page is None:
        page = 1
    if limit is None:
        limit = 10
```

### 2. 如何处理分页？

#### 标准分页格式

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "totalPages": 10
  }
}
```

#### 查询参数

| 参数名 | 类型    | 必填 | 默认值 | 说明     |
| ------ | ------- | ---- | ------ | -------- |
| page   | integer | 否   | 1      | 页码     |
| limit  | integer | 否   | 10     | 每页数量 |

### 3. 如何处理错误？

#### 标准错误格式

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述",
    "details": {}
  }
}
```

#### 常见错误码

| 错误码           | HTTP 状态码 | 说明             |
| ---------------- | ----------- | ---------------- |
| VALIDATION_ERROR | 400         | 请求参数验证失败 |
| UNAUTHORIZED     | 401         | 未授权           |
| FORBIDDEN        | 403         | 禁止访问         |
| NOT_FOUND        | 404         | 资源不存在       |
| INTERNAL_ERROR   | 500         | 服务器内部错误   |

### 4. 如何处理认证？

#### API Key 认证

```bash
curl -X GET https://api.example.com/v1/users \
  -H "X-API-Key: YOUR_API_KEY"
```

#### Bearer Token 认证

```bash
curl -X GET https://api.example.com/v1/users \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 5. 如何处理文件上传？

#### Multipart/Form-Data

```bash
curl -X POST https://api.example.com/v1/upload \
  -F "file=@/path/to/file.jpg"
```

#### Base64 编码

```json
{
  "file": "base64_encoded_string",
  "filename": "file.jpg"
}
```

### 6. 如何处理批量操作？

#### 批量创建

```json
{
  "users": [
    { "name": "User 1", "email": "user1@example.com" },
    { "name": "User 2", "email": "user2@example.com" }
  ]
}
```

#### 批量删除

```bash
curl -X DELETE https://api.example.com/v1/users?ids=1,2,3
```

### 7. 如何处理嵌套资源？

#### 标准格式

```
/users/{userId}/posts/{postId}
```

#### 示例

```bash
curl -X GET https://api.example.com/v1/users/123/posts/456
```

### 8. 如何处理过滤和排序？

#### 过滤

```bash
curl -X GET "https://api.example.com/v1/users?status=active&age=30"
```

#### 排序

```bash
curl -X GET "https://api.example.com/v1/users?sort=name&order=asc"
```

#### 查询参数

| 参数名 | 类型   | 说明                 |
| ------ | ------ | -------------------- |
| filter | string | 过滤条件             |
| sort   | string | 排序字段             |
| order  | string | 排序方向（asc/desc） |

### 9. 如何处理版本控制？

#### URL 路径版本控制

```
/api/v1/users
/api/v2/users
```

#### 请求头版本控制

```bash
curl -X GET https://api.example.com/v1/users \
  -H "API-Version: 1"
```

### 10. 如何处理速率限制？

#### 响应头

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1617235200
```

#### 超限响应

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "请求过于频繁，请稍后重试"
  }
}
```

## 总结

创建高质量的 API 文档需要遵循以下原则：

1. **完整性**：包含所有必要的信息
2. **准确性**：确保文档与代码同步
3. **清晰性**：使用简单明了的语言
4. **一致性**：保持格式和风格一致
5. **可维护性**：定期更新和审查文档
6. **自动化**：使用工具自动生成文档
7. **用户友好**：提供丰富的示例和说明

通过遵循这些最佳实践，您可以创建出专业、易用、易维护的 API 文档。
