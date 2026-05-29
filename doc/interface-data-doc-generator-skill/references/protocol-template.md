# 协议与通信规范模板

## 协议概述
- **协议类型**：WebSocket / Protobuf / FlatBuffers
- **协议版本**：v1.0.0
- **应用场景**：实时通信 / 游戏交互 / 数据传输

---

## 1. WebSocket 协议规范

### 1.1 连接建立

#### 1.1.1 连接 URL
```
wss://api.example.com/ws?token={token}&device=web
```

#### 1.1.2 连接参数
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| token | String | 是 | 用户鉴权 Token | eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... |
| device | String | 否 | 设备类型（web/mobile/miniapp） | web |
| version | String | 是 | 协议版本 | 1.0.0 |

#### 1.1.3 握手流程
1. 客户端发起 WebSocket 连接请求
2. 服务端验证 Token 有效性
3. 验证通过后建立连接，返回握手成功消息

---

### 1.2 消息帧结构

#### 1.2.1 消息格式
```json
{
  "msgId": 1001,
  "cmd": 1001,
  "seq": 1,
  "timestamp": 1699999999,
  "body": {}
}
```

#### 1.2.2 消息头字段
| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| msgId | Integer | 是 | 消息唯一 ID |
| cmd | Integer | 是 | 指令码（见业务指令集） |
| seq | Integer | 是 | 消息序列号（用于消息去重和重排） |
| timestamp | Long | 是 | 时间戳（秒） |
| body | Object | 是 | 消息体（具体内容见各指令） |

---

### 1.3 心跳机制

#### 1.3.1 心心跳说明
- **心跳周期**：30 秒
- **超时断连**：90 秒无响应自动断开连接
- **心跳指令**：`CMD_PING = 1`, `CMD_PONG = 2`

#### 1.3.2 心跳流程
```
客户端 → 服务端: CMD_PING
服务端 → 客户端: CMD_PONG
```

**CMD_PING 示例**：
```json
{
  "msgId": 1,
  "cmd": 1,
  "seq": 1,
  "timestamp": 1699999999,
  "body": {}
}
```

**CMD_PONG 示例**：
```json
{
  "msgId": 2,
  "cmd": 2,
  "seq": 1,
  "timestamp": 1699999999,
  "body": {}
}
```

---

### 1.4 业务指令集

#### 1.4.1 基础指令
| 指令码 | 指令名称 | 说明 |
|--------|----------|------|
| 1 | CMD_PING | 心跳请求 |
| 2 | CMD_PONG | 心跳响应 |
| 1001 | CMD_LOGIN | 登录认证 |
| 1002 | CMD_LOGIN_RESP | 登录响应 |
| 1003 | CMD_LOGOUT | 登出 |

#### 1.4.2 业务指令（示例）
| 指令码 | 指令名称 | 说明 | 触发条件 |
|--------|----------|------|----------|
| 2001 | CMD_SEND_MESSAGE | 发送消息 | 用户发送聊天消息 |
| 2002 | CMD_RECV_MESSAGE | 接收消息 | 服务端推送消息 |
| 2003 | CMD_READ_MESSAGE | 消息已读 | 用户标记消息已读 |

#### 1.4.3 指令示例

**CMD_SEND_MESSAGE（发送消息）**：
```json
{
  "msgId": 1001,
  "cmd": 2001,
  "seq": 1,
  "timestamp": 1699999999,
  "body": {
    "roomId": 1001,
    "content": "Hello World",
    "contentType": "text"
  }
}
```

**CMD_RECV_MESSAGE（接收消息）**：
```json
{
  "msgId": 1002,
  "cmd": 2002,
  "seq": 2,
  "timestamp": 1699999999,
  "body": {
    "roomId": 1001,
    "senderId": 1001,
    "senderName": "张三",
    "content": "Hello World",
    "contentType": "text",
    "sendTime": 1699999999
  }
}
```

---

### 1.5 错误处理

#### 1.5.1 错误消息格式
```json
{
  "msgId": 1003,
  "cmd": 9999,
  "seq": 3,
  "timestamp": 1699999999,
  "body": {
    "code": 4001,
    "message": "Token 已过期",
    "details": {}
  }
}
```

#### 1.5.2 错误码说明
| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| 4001 | Token 无效或过期 | 重新登录获取新 Token |
| 4002 | 频率限制 | 降低发送频率 |
| 4003 | 非法指令 | 检查指令码是否正确 |
| 4004 | 连接超时 | 重新建立连接 |
| 5000 | 服务器内部错误 | 稍后重试 |

#### 1.5.3 异常处理策略
- Token 失效：关闭连接，提示用户重新登录
- 频率限制：延迟发送或丢弃消息
- 连接断开：自动重连（最多 3 次）

---

## 2. Protobuf 协议规范

### 2.1 IDL 定义文件（.proto）

#### 2.1.1 文件结构
```protobuf
syntax = "proto3";

package com.example.protocol;

// 导入其他消息定义
import "common.proto";

// 消息定义
message UserMessage {
  int32 user_id = 1;
  string username = 2;
  string email = 3;
}

// 枚举定义
enum UserStatus {
  UNKNOWN = 0;
  ACTIVE = 1;
  INACTIVE = 2;
}

// 请求消息
message LoginRequest {
  string username = 1;
  string password = 2;
}

// 响应消息
message LoginResponse {
  bool success = 1;
  string token = 2;
  string message = 3;
}
```

#### 2.1.2 字段编号规则
- 字段编号从 1 开始，不可重复
- 1-15：单字节编码（常用字段）
- 16-2047：双字节编码
- 19000-1999：保留字段（禁止使用）

---

### 2.2 序列化/反序列化规则

#### 2.2.1 序列化特性
- **编码方式**：Varint 编码（变长整数）
- **默认值**：未设置的字段使用默认值
  - 数值类型：0
  - 布尔类型：false
  - 字符串：空字符串 ""
  - 枚举：第一个枚举值

#### 2.2.2 向前/向后兼容
- **添加字段**：向前兼容（旧版本忽略新字段）
- **删除字段**：向后兼容（保留字段编号，改为 reserved）
- **修改字段类型**：不兼容（需升级版本）

**示例**：
```protobuf
message UserMessage {
  int32 user_id = 1;
  string username = 2;
  string email = 3;  // 可删除，改为 reserved 3;

  // 新增字段
  string phone = 4;  // 向前兼容
}
```

---

### 2.3 多语言支持

#### 2.3.1 代码生成
使用 `protoc` 编译器生成多语言代码：

```bash
# 生成 Java 代码
protoc --java_out=./java/ user.proto

# 生成 Python 代码
protoc --python_out=./python/ user.proto

# 生成 Go 代码
protoc --go_out=./go/ user.proto

# 生成 C++ 代码
protoc --cpp_out=./cpp/ user.proto
```

#### 2.3.2 使用示例

**Java 示例**：
```java
// 创建消息
UserMessage user = UserMessage.newBuilder()
    .setUserId(1001)
    .setUsername("张三")
    .setEmail("test@example.com")
    .build();

// 序列化
byte[] data = user.toByteArray();

// 反序列化
UserMessage parsedUser = UserMessage.parseFrom(data);
```

**Python 示例**：
```python
# 创建消息
user = UserMessage()
user.user_id = 1001
user.username = "张三"
user.email = "test@example.com"

# 序列化
data = user.SerializeToString()

# 反序列化
parsed_user = UserMessage()
parsed_user.ParseFromString(data)
```

---

### 2.4 性能对比

| 特性 | Protobuf | FlatBuffers | JSON |
|------|----------|-------------|------|
| 编码大小 | 小 | 最小 | 大 |
| 解析速度 | 快 | 最快（零拷贝） | 慢 |
| 兼容性 | 好 | 好 | 最好 |
| 易用性 | 中 | 中 | 最易 |

---

## 3. 注意事项

1. WebSocket 连接需定期发送心跳，避免超时断连
2. 消息序列号（seq）用于消息去重和重排，必须保证唯一性
3. Protobuf 字段编号不可重复，删除字段需改为 reserved
4. 错误消息需包含明确的错误码和错误说明
5. 频率限制：单个连接每秒最多发送 10 条消息
6. 连接超时：90 秒无响应自动断开
7. 重连策略：指数退避（1s, 2s, 4s, 8s），最多重连 3 次
