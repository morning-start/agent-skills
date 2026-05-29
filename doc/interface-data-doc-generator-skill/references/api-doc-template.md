# API 接口文档模板

## 文档概述
- **项目名称**：[项目名称]
- **API 版本**：v1.0.0
- **基础 URL**：`https://api.example.com/v1`
- **文档格式**：OpenAPI 3.0 / Postman Collection

---

## 1. 基础信息

### 1.1 通用说明
- **编码格式**：UTF-8
- **内容类型**：application/json
- **字符集**：utf-8
- **时区**：UTC+8

### 1.2 鉴权方式
| 类型 | 说明 |
|------|------|
| **鉴权类型** | JWT Token / API Key / OAuth2.0 |
| **Header 名称** | Authorization |
| **格式** | `Bearer {token}` 或 `Api-Key {key}` |
| **获取方式** | 登录接口返回 / 管理后台申请 |

### 1.3 响应格式规范
所有接口响应统一格式：

```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": 1699999999
}
```

### 1.4 错误码说明
| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| 200 | 成功 | - |
| 400 | 请求参数错误 | 检查请求参数格式 |
| 401 | 未授权 | 检查 Token 是否有效 |
| 403 | 禁止访问 | 检查权限 |
| 404 | 资源不存在 | 检查请求路径 |
| 429 | 请求过于频繁 | 降低请求频率 |
| 500 | 服务器内部错误 | 联系技术支持 |

---

## 2. 接口列表

### 2.1 用户模块

#### 2.1.1 用户注册
- **接口名称**：用户注册
- **接口路径**：`/api/v1/users/register`
- **请求方法**：POST
- **功能说明**：新用户注册账号

**请求参数**：
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| username | String | 是 | 用户名（3-20字符） | zhangsan |
| password | String | 是 | 密码（6-20字符） | 123456 |
| email | String | 是 | 邮箱地址 | test@example.com |
| phone | String | 否 | 手机号 | 13800138000 |

**请求示例**：
```json
{
  "username": "zhangsan",
  "password": "123456",
  "email": "test@example.com"
}
```

**成功响应**：
```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "userId": 1001,
    "username": "zhangsan",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "timestamp": 1699999999
}
```

**错误响应**：
```json
{
  "code": 400,
  "message": "用户名已存在",
  "data": null,
  "timestamp": 1699999999
}
```

#### 2.1.2 用户登录
- **接口名称**：用户登录
- **接口路径**：`/api/v1/users/login`
- **请求方法**：POST
- **功能说明**：用户登录获取 Token

**请求参数**：
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| username | String | 是 | 用户名或邮箱 | zhangsan |
| password | String | 是 | 密码 | 123456 |

**请求示例**：
```json
{
  "username": "zhangsan",
  "password": "123456"
}
```

**成功响应**：
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "userId": 1001,
    "username": "zhangsan",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 7200
  },
  "timestamp": 1699999999
}
```

---

### 2.2 订单模块

#### 2.2.1 创建订单
- **接口名称**：创建订单
- **接口路径**：`/api/v1/orders`
- **请求方法**：POST
- **功能说明**：创建新订单

**请求参数**：
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| productId | Integer | 是 | 商品 ID | 1001 |
| quantity | Integer | 是 | 购买数量 | 2 |
| addressId | Integer | 是 | 收货地址 ID | 2001 |
| remark | String | 否 | 订单备注 | 尽快发货 |

**成功响应**：
```json
{
  "code": 200,
  "message": "订单创建成功",
  "data": {
    "orderId": "202401010001",
    "totalAmount": 199.00,
    "status": "pending_payment"
  },
  "timestamp": 1699999999
}
```

---

## 3. 多端差异说明

### 3.1 Web 端特性
- 返回完整字段信息
- 包含分页信息、权限标记
- 支持更多元数据（如操作日志、审计信息）

### 3.2 移动端特性
- 精简字段（省略冗余描述）
- 减少嵌套层级（避免深度嵌套）
- 压缩数据量（去除 null 字段）

### 3.3 小程序端特性
- 兼容性考虑（避免使用最新特性）
- 减少网络请求（合并多个接口）
- 优化加载速度（懒加载、分页）

**示例差异**：
同一个用户信息接口：
- **Web 端响应**：包含 `avatar`, `nickname`, `bio`, `createdAt`, `updatedAt`, `lastLoginTime`, `loginCount`
- **移动端响应**：仅包含 `avatar`, `nickname`, `bio`
- **小程序端响应**：仅包含 `avatar`, `nickname`

---

## 4. 注意事项

1. 所有接口均需要携带鉴权 Token（除登录、注册等公开接口）
2. 请求频率限制：每分钟最多 100 次请求
3. 时间戳格式：Unix 时间戳（秒）
4. 金额单位：元（保留两位小数）
5. 布尔值：使用 `true`/`false`（JSON 格式）

---

## 5. 调试工具

- **Swagger UI**：`https://api.example.com/swagger`
- **Postman Collection**：[下载链接]
- **Mock 服务**：`https://mock.example.com`
