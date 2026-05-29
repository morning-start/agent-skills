# WebSocket 协议指南

## 概览
WebSocket 是一种在单个 TCP 连接上进行全双工通信的协议。相比 HTTP 的请求-响应模式，WebSocket 支持服务器主动向客户端推送消息，适用于实时性要求高的场景（如聊天、游戏、实时通知）。

---

## 连接建立

### 握手过程
WebSocket 连接建立基于 HTTP 升级机制：

1. 客户端发起 HTTP 请求（Upgrade 头）
2. 服务端响应 101 Switching Protocols
3. 连接升级为 WebSocket 协议

### 客户端请求示例
```http
GET /ws HTTP/1.1
Host: api.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

### 服务端响应示例
```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

---

## 消息帧结构

### 帧格式
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-------+-+-------------+-------------------------------+
|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
|I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
|N|V|V|V|       |S|             |   (if payload len==126/127)   |
| |1|2|3|       |K|             |                               |
+-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
|     Extended payload length continued, if payload len == 127  |
+ - - - - - - - - - - - - - - - +-------------------------------+
|                               |Masking-key, if MASK set to 1  |
+-------------------------------+-------------------------------+
| Masking-key (continued)       |           Payload Data         |
+-------------------------------- - - - - - - - - - - - - - - - +
:                     Payload Data continued ...                :
+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
|                     Payload Data continued ...                |
+---------------------------------------------------------------+
```

### Opcode 说明
| Opcode | 值 | 说明 |
|--------|-----|------|
| %x0 | 0 | 连续帧 |
| %x1 | 1 | 文本帧（UTF-8） |
| %x2 | 2 | 二进制帧 |
| %x8 | 8 | 连接关闭 |
| %x9 | 9 | Ping |
| %xA | 10 | Pong |

---

## 心跳机制

### 心跳目的
- 检测连接是否存活
- 防止连接超时断开
- 同步网络延迟

### 心跳实现
```javascript
// 客户端发送心跳
const sendPing = () => {
  ws.send(JSON.stringify({ cmd: 'ping' }));
  setTimeout(sendPing, 30000);  // 每 30 秒发送一次
};

// 服务端响应
ws.on('message', (message) => {
  const data = JSON.parse(message);
  if (data.cmd === 'pong') {
    console.log('收到心跳响应');
  }
});
```

### 超时断连
```javascript
let lastPongTime = Date.now();

ws.on('message', (message) => {
  const data = JSON.parse(message);
  if (data.cmd === 'pong') {
    lastPongTime = Date.now();
  }
});

// 检查超时
setInterval(() => {
  if (Date.now() - lastPongTime > 90000) {  // 90 秒无响应
    ws.close();
  }
}, 10000);
```

---

## 消息格式设计

### 标准消息格式
```json
{
  "msgId": 1001,
  "cmd": 1001,
  "seq": 1,
  "timestamp": 1699999999,
  "body": {}
}
```

### 字段说明
| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| msgId | Integer | 是 | 消息唯一 ID |
| cmd | Integer | 是 | 指令码（见业务指令集） |
| seq | Integer | 是 | 消息序列号（用于去重） |
| timestamp | Long | 是 | 时间戳（秒） |
| body | Object | 是 | 消息体 |

---

## 业务指令集

### 基础指令
| 指令码 | 指令名称 | 说明 | 方向 |
|--------|----------|------|------|
| 1 | CMD_PING | 心跳请求 | 客户端→服务端 |
| 2 | CMD_PONG | 心跳响应 | 服务端→客户端 |
| 1001 | CMD_LOGIN | 登录 | 客户端→服务端 |
| 1002 | CMD_LOGIN_RESP | 登录响应 | 服务端→客户端 |
| 1003 | CMD_LOGOUT | 登出 | 客户端→服务端 |

### 业务指令示例
| 指令码 | 指令名称 | 说明 | 方向 |
|--------|----------|------|------|
| 2001 | CMD_SEND_MESSAGE | 发送消息 | 客户端→服务端 |
| 2002 | CMD_RECV_MESSAGE | 接收消息 | 服务端→客户端 |
| 2003 | CMD_READ_MESSAGE | 消息已读 | 客户端→服务端 |

---

## 错误处理

### 关闭码（Close Code）
| 关闭码 | 说明 |
|--------|------|
| 1000 | 正常关闭 |
| 1001 | 端点离开（如关闭浏览器） |
| 1002 | 协议错误 |
| 1003 | 不支持的数据类型 |
| 1007 | 数据类型不一致 |
| 1008 | 违反策略 |
| 1009 | 消息过大 |
| 1010 | 缺少扩展 |
| 1011 | 内部错误 |
| 1015 | TLS 握手失败 |

### 错误消息格式
```json
{
  "code": 4001,
  "message": "Token 已过期",
  "details": {}
}
```

### 错误处理策略
```javascript
ws.on('close', (code, reason) => {
  console.log(`连接关闭，关闭码：${code}`);
  if (code === 1000) {
    console.log('正常关闭');
  } else if (code === 1001) {
    console.log('客户端离开');
  } else {
    console.log('异常关闭，尝试重连...');
    reconnect();
  }
});
```

---

## 重连机制

### 重连策略
- **指数退避**：1s, 2s, 4s, 8s, ...（最多重试 3 次）
- **最大重试次数**：3 次
- **重连条件**：连接异常关闭、网络错误

### 重连实现
```javascript
let reconnectAttempts = 0;
const maxReconnectAttempts = 3;

const reconnect = () => {
  if (reconnectAttempts >= maxReconnectAttempts) {
    console.log('重连失败，达到最大重试次数');
    return;
  }

  const delay = Math.pow(2, reconnectAttempts) * 1000;  // 指数退避
  setTimeout(() => {
    reconnectAttempts++;
    console.log(`尝试重连（${reconnectAttempts}/${maxReconnectAttempts}）...`);
    connect();
  }, delay);
};
```

---

## 安全性

### 认证机制
```javascript
// 连接时携带 Token
const ws = new WebSocket(`wss://api.example.com/ws?token=${token}`);

// 连接建立后发送认证消息
ws.onopen = () => {
  ws.send(JSON.stringify({
    cmd: 'CMD_LOGIN',
    token: token
  }));
};
```

### 数据加密
- 使用 WSS（WebSocket over TLS）加密传输
- 敏感数据（如密码）在应用层加密

### 频率限制
- 单个连接每秒最多发送 10 条消息
- 超过限制时延迟发送或丢弃消息

---

## 性能优化

### 消息压缩
```javascript
// 使用 Compression Extension
const ws = new WebSocket('wss://api.example.com/ws', [], {
  perMessageDeflate: {
    serverNoContextTakeover: true,
    clientNoContextTakeover: true
  }
});
```

### 消息合并
```javascript
// 合并多条小消息
const messageQueue = [];

const sendMessage = (data) => {
  messageQueue.push(data);

  // 每 100ms 批量发送一次
  setTimeout(() => {
    if (messageQueue.length > 0) {
      ws.send(JSON.stringify({ messages: messageQueue }));
      messageQueue.length = 0;
    }
  }, 100);
};
```

### 心跳优化
- 根据网络状况动态调整心跳间隔
- 网络延迟高时增加心跳频率

---

## 最佳实践

1. **心跳机制**：定期发送心跳，检测连接存活
2. **消息去重**：使用消息序列号（seq）去重
3. **错误处理**：捕获所有异常，提供友好的错误提示
4. **重连策略**：使用指数退避，避免频繁重连
5. **安全性**：使用 WSS 加密传输，携带 Token 认证
6. **性能优化**：使用压缩、批量发送、消息合并
7. **日志记录**：记录连接、消息、错误等关键事件
8. **监控告警**：监控连接数、消息量、延迟等指标

---

## 常见问题

### Q: 如何处理网络断开？
A: 监听 `close` 和 `error` 事件，自动重连：
```javascript
ws.on('close', () => {
  reconnect();
});

ws.onerror = (error) => {
  console.error('WebSocket 错误:', error);
  reconnect();
};
```

### Q: 如何避免消息丢失？
A: 使用消息确认机制（ACK）：
```javascript
const sendWithAck = (message, callback) => {
  const msgId = generateMsgId();
  ws.send(JSON.stringify({ ...message, msgId }));

  const ackTimeout = setTimeout(() => {
    callback('消息发送超时');
  }, 5000);

  // 监听 ACK
  ws.on('message', (data) => {
    const msg = JSON.parse(data);
    if (msg.msgId === msgId) {
      clearTimeout(ackTimeout);
      callback(null, msg);
    }
  });
};
```

### Q: 如何处理消息顺序？
A: 使用消息序列号（seq）排序：
```javascript
const msgBuffer = {};

ws.on('message', (data) => {
  const msg = JSON.parse(data);
  msgBuffer[msg.seq] = msg;

  // 按序列号排序后处理
  const sortedMsgs = Object.values(msgBuffer)
    .sort((a, b) => a.seq - b.seq);

  sortedMsgs.forEach(processMessage);
});
```
