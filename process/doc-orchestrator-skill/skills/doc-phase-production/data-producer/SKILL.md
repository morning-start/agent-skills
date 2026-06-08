---
name: data-producer
version: 0.1.1
description: Use when the user needs database design, data dictionary, or communication protocol documentation.
tags: [data-modeling, database-design, protocol, documentation]
---

# Data Producer

## 职责

- 生成数据库设计文档
- 生成数据字典
- 生成通信协议文档（WebSocket/gRPC/Protobuf）
- 生成数据流图

## 输入

- 模板路径（templates/data/）
- 架构文档
- 需求文档

## 输出

- 数据库设计文档
- 数据字典
- 协议文档（如适用）

## 数据库设计文档结构

```markdown
---
doc:
  id: "DATA-001"
  type: "data"
  subtype: "database"
  version: "1.0.0"
  status: "draft"
  traceability:
    depends_on: ["ARCH-001"]
    feeds_into: ["API-001", "TEST-001"]
---

# 数据库设计文档

## 1. 概述
- 数据库类型、版本、设计原则

## 2. ER 图
- 实体关系图

## 3. 表结构
### 3.1 users 表
- 字段定义（名称、类型、约束、说明）
- 索引定义
- 外键关系

## 4. 数据字典
- 枚举值定义
- 状态码说明

## 5. 索引策略
- 主键、唯一索引、联合索引
- 查询优化建议

## 6. 迁移策略
- 版本管理、回滚方案

## 7. 安全策略
- 数据加密、脱敏、备份
```

## 通信协议文档结构

```markdown
---
doc:
  id: "PROTO-001"
  type: "data"
  subtype: "protocol"
  version: "1.0.0"
  status: "draft"
---

# 通信协议文档

## 1. 协议概述
- 协议类型、版本、适用场景

## 2. 连接管理
- 连接建立、心跳机制、超时断连

## 3. 消息格式
- 帧结构、编码方式

## 4. 指令集
- 指令码、请求/响应格式

## 5. 错误处理
- 错误码、重试策略
```

## 注意事项

- 表结构必须包含完整字段定义和约束
- 索引策略必须说明设计理由
- 协议文档必须包含完整示例
- 追溯关系 depends_on 指向架构文档
