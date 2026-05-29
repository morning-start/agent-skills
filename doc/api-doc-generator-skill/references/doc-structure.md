# API 文档结构规范

## 目录
- [概述](#概述)
- [标准章节结构](#标准章节结构)
- [文件组织规范](#文件组织规范)
- [内容格式规范](#内容格式规范)
- [示例](#示例)

## 概述

本文档定义了 API 文档的标准结构和格式规范，确保生成的文档符合高质量 API 文档的要求。

## 标准章节结构

### 1. 概述（overview.md）
- API 的用途和目标
- 支持的使用场景
- 前提条件（如注册账号、获取 API Key 等）
- 支持的协议（如 REST、GraphQL、gRPC 等）

### 2. 认证方式（authentication.md）
- 使用的认证机制（如 API Key、OAuth 2.0、JWT、Basic Auth 等）
- 如何获取凭证
- 请求头或参数中如何传递认证信息
- 示例（带认证的请求）

### 3. 基础信息（base-info.md）
- API 的根路径（如 https://api.example.com/v1）
- 各个资源的端点（Endpoints）列表
- 请求与响应格式说明

### 4. 端点详情（endpoints/）
对每个 API 端点提供：
- 路径（如 /users/{id}）
- 方法（GET/POST 等）
- 描述（功能说明）
- 路径参数、查询参数、请求体参数
- 示例请求和响应
- 错误码及含义

### 5. 错误处理（error-handling.md）
- 统一的错误响应格式
- 错误代码与人类可读信息
- 常见错误场景及解决建议

### 6. 速率限制（rate-limiting.md）
- 每分钟/小时允许的请求数
- 超限后的响应
- 如何查看当前使用情况

### 7. 变更日志（changelog.md）
- 版本更新记录
- 新增、修改、废弃的接口说明

### 8. 支持与反馈（support.md）
- 联系方式
- 报告 Bug 或提需求的渠道

## 文件组织规范

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

## 内容格式规范

### 端点文档格式

```markdown
## 端点名称

### 请求
- **方法**: GET
- **路径**: `/users/{id}`
- **描述**: 获取指定用户的信息

### 路径参数
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | string | 是 | 用户ID |

### 查询参数
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| fields | string | 否 | 无 | 指定返回字段，逗号分隔 |

### 请求体
无

### 请求示例
```bash
curl -X GET https://api.example.com/v1/users/123
```

### 响应
```json
{
  "id": "123",
  "name": "John Doe",
  "email": "john@example.com"
}
```

### 错误响应
```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "用户不存在"
  }
}
```
```

### 错误码格式
| 错误码 | 说明 | 解决方法 |
|--------|------|----------|
| 400 | 请求参数错误 | 检查请求参数格式 |
| 401 | 未授权 | 检查认证信息 |
| 404 | 资源不存在 | 确认资源ID是否正确 |
| 500 | 服务器错误 | 稍后重试或联系支持 |

## 示例

### 完整的端点文档示例

参见 `assets/templates/endpoint-template.md`

### 模块文档示例

参见 `assets/templates/module-template.md`
