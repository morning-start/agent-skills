---
name: api-producer
version: 0.1.0
description: 生成 API 接口文档，支持 RESTful/GraphQL/gRPC 多种协议
---

# API Producer

## 职责

- 根据模板生成 API 接口文档
- 支持 RESTful/GraphQL/gRPC/WebSocket 多种协议
- 生成多端差异说明（Web/移动端/小程序）
- 生成 OpenAPI/Swagger 兼容格式

## 输入

- 模板路径（templates/api/）
- 架构文档
- 需求文档

## 输出

- API 接口文档（Markdown）
- OpenAPI 3.0 规范文件（YAML，可选）

## API 文档结构

```markdown
---
doc:
  id: "API-001"
  type: "api"
  version: "1.0.0"
  status: "draft"
  traceability:
    depends_on: ["ARCH-001"]
    feeds_into: ["TEST-001"]
---

# API 接口文档

## 1. 概述
- API 基础信息、版本、认证方式

## 2. 基础信息
- Base URL、协议、数据格式、版本策略

## 3. 认证与授权
- 认证方式（JWT/OAuth2/API Key）
- 权限说明

## 4. 通用规范
- 请求格式、响应格式、分页、排序、过滤

## 5. 错误码
- 错误码列表、含义、处理建议

## 6. 接口详情
### 6.1 用户模块
#### POST /api/v1/users
- 请求参数（Path/Query/Body/Headers）
- 响应结构（成功/失败）
- 示例（请求/响应）

## 7. 多端差异
- Web 端完整字段
- 移动端精简字段

## 8. 变更日志
- 版本变更记录
```

## 协议支持

| 协议 | 文档特点 |
|------|---------|
| RESTful | HTTP 方法、URL、状态码 |
| GraphQL | Query/Mutation、Schema |
| gRPC | Service、Message、.proto |
| WebSocket | 连接、消息格式、心跳 |

## 多端差异规则

| 终端 | 字段策略 |
|------|---------|
| Web | 完整字段、分页、权限标记 |
| Mobile | 精简字段、减少嵌套、压缩 |
| Mini Program | 兼容旧版、避免新特性 |

## 注意事项

- 每个接口必须包含请求/响应示例
- 错误码必须完整列出
- 多端差异必须明确标注
- 追溯关系 depends_on 指向架构文档，feeds_into 指向测试文档
