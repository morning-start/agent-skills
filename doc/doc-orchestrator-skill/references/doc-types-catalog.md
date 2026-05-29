# 文档类型目录

本文档定义 doc-orchestrator 支持的所有文档类型及其分类。

## 文档分类体系

### 需求类（requirement）

| 子类型 | ID 前缀 | 说明 |
|--------|---------|------|
| srs | REQ- | 软件需求规格说明，技术视角 |
| prd | REQ- | 产品需求文档，业务视角 |
| functional | REQ- | 功能需求说明 |
| non-functional | REQ- | 非功能需求说明 |

### 架构类（architecture）

| 子类型 | ID 前缀 | 说明 |
|--------|---------|------|
| sad | ARCH- | 系统架构设计文档 |
| tdd | ARCH- | 技术方案设计文档 |
| platform-web | ARCH- | Web 平台架构 |
| platform-mobile | ARCH- | 移动平台架构 |
| platform-desktop | ARCH- | 桌面平台架构 |
| platform-game | ARCH- | 游戏平台架构 |

### 接口数据类（api / data）

| 类型 | 子类型 | ID 前缀 | 说明 |
|------|--------|---------|------|
| api | rest | API- | RESTful API 文档 |
| api | graphql | API- | GraphQL API 文档 |
| api | grpc | API- | gRPC API 文档 |
| api | websocket | API- | WebSocket API 文档 |
| data | database | DATA- | 数据库设计文档 |
| data | dictionary | DATA- | 数据字典 |
| data | protocol | PROTO- | 通信协议文档 |

### 质量运维类（quality）

| 子类型 | ID 前缀 | 说明 |
|--------|---------|------|
| test | TEST- | 测试策略与计划 |
| ops | OPS- | 部署与运维手册 |
| security | SEC- | 安全合规文档 |

### 基础类（basic）

| 子类型 | ID 前缀 | 说明 |
|--------|---------|------|
| readme | README | 项目说明文档 |
| changelog | CHANGELOG | 变更日志 |
| contributing | CONTRIBUTING | 贡献指南 |

## 文档追溯规则

```
REQ → ARCH → API/DATA → TEST
        ↓
       OPS/SEC
```

- 需求文档是源头，不依赖其他文档
- 架构文档依赖需求文档
- API 和数据文档依赖架构文档
- 质量运维文档依赖需求和架构文档

## 项目规模裁剪

### 小项目（<10 功能）

必需：README + REQ(srs) + ARCH(sad) + API

### 中项目（10-30 功能）

必需：小项目全部 + PRD + DATA + TEST + CHANGELOG

可选：OPS + SEC

### 大项目（>30 功能）

必需：中项目全部 + TDD + 平台专项架构 + OPS + SEC

可选：functional-doc + non-functional-doc
