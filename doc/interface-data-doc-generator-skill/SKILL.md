---
name: interface-data-doc-generator
version: 1.0.1
description: "⚠️ DEPRECATED: 此技能已废弃，请使用 doc-orchestrator 代替。接口与数据文档生成器，自动生成API文档、数据库设计文档和通信协议规范"
tags: [api-doc, database-doc, protocol, documentation, generator, validation, deprecated]
deprecated: true
deprecation_notice: "此技能已废弃，请使用 doc-orchestrator 代替。新技能提供五阶段文档生命周期管理、双轨格式协议、智能绘图、质量门禁。"
deprecation_date: "2026-05-02"
replacement: "doc-orchestrator"
---

> ⚠️ **此技能已废弃**
> 
> 请使用 [doc-orchestrator](../doc-orchestrator/SKILL.md) 代替。

# InterfaceDataDocGenerator - 接口与数据文档生成器

## 任务目标

InterfaceDataDocGenerator 是一个智能接口与数据文档生成器，帮助你快速生成专业的 API 接口文档、数据库设计文档和通信协议规范。

**核心价值**:
- 🚀 **快速生成**: 根据架构文档自动生成完整的技术文档
- 📋 **模板丰富**: 支持多种文档类型（API/数据库/协议）
- 🔧 **工具完善**: 提供格式验证脚本确保文档质量
- 📚 **技术全面**: 支持多种编程语言和架构框架
- ✅ **质量保证**: 完整性校验和规范性分析

---

## 快速上手（5 分钟）

### 1. 生成 API 接口文档

```bash
# 智能体分析接口需求并生成文档
# 参考 references/api-doc-template.md 模板
# 生成 OpenAPI 3.0 格式或 Postman Collection 格式
```

### 2. 生成数据库设计文档

```bash
# 智能体分析数据模型并生成文档
# 参考 references/db-doc-template.md 模板
# 包含表结构、数据字典、索引策略
```

### 3. 验证文档格式

```bash
# 验证 OpenAPI 格式
python scripts/validate_openapi.py openapi.yaml

# 验证 Protobuf 格式
python scripts/validate_protobuf.proto schema.proto

# 验证 SQL DDL 语法
python scripts/validate_sql.py schema.sql
```

**完成!** 现在你有了标准格式的接口文档、数据库文档和通信协议文档。

---

## 核心能力

### 1. 文档自动生成 ⭐⭐⭐⭐⭐

**触发场景**: 新项目启动、需要快速生成技术文档时

**输入**: 架构文档、需求描述或接口列表

**输出**: 标准格式的 Markdown 文档

**支持文档类型**:
- API 接口文档（OpenAPI 3.0、Postman Collection）
- 数据库设计文档（表结构、数据字典、索引）
- 通信协议文档（WebSocket、Protobuf、FlatBuffers）

### 2. 现有文档分析与优化 ⭐⭐⭐⭐⭐

**触发场景**: 需要审查和优化现有技术文档时

**分析维度**:
- 完整性检查（是否包含所有必需章节）
- 规范性检查（命名规范、字段类型、约束定义）
- 格式验证（OpenAPI、Protobuf、SQL 语法）
- 优化建议（数据结构设计、索引优化）

### 3. 多语言多架构支持 ⭐⭐⭐⭐

**触发场景**: 需要为不同技术栈生成文档时

**支持语言/框架**:
- 后端: Java/SpringBoot、Go/Gin、Python/Django/Flask/FastAPI、Node.js/Express/NestJS
- 前端: React、Vue、Angular、Svelte、Next.js、Nuxt.js
- 数据库: MySQL、PostgreSQL、Oracle、MongoDB
- 协议: RESTful、GraphQL、WebSocket、gRPC

### 4. 多端差异管理 ⭐⭐⭐⭐

**触发场景**: 需要为不同终端生成差异化文档时

**支持终端**:
- Web 端（完整字段、分页信息、权限标记）
- 移动端（精简字段、减少嵌套、压缩数据）
- 小程序（兼容性考虑、避免使用最新特性）

### 5. 需求变更分析 ⭐⭐⭐

**触发场景**: 需求变更后分析影响范围时

**分析内容**:
- 对比变更前后的文档差异
- 识别受影响的接口/表/协议
- 提供兼容性建议
- 评估影响范围（技术/开发/测试/用户体验）

### 6. 完整性校验 ⭐⭐⭐⭐

**触发场景**: 文档生成后确保质量时

**检查项**:
- API 文档：请求参数、响应结构、错误码、鉴权说明
- 数据库文档：表结构、数据字典、索引策略
- 协议文档：连接建立、消息格式、错误处理

---

## 使用示例

### 场景 1: 生成 RESTful API 文档（推荐）

适用于前后端项目需要 API 接口文档。

**执行流程**:
1. 智能体分析用户提供的接口列表和业务逻辑
2. 参考 `references/api-doc-template.md` 生成完整文档
3. 调用 `scripts/validate_openapi.py` 验证 YAML 格式

**关键要点**:
- 包含 GET/POST/PUT/DELETE 等方法
- 定义请求参数（Path/Query/Body/Headers）
- 提供成功/失败响应示例
- 说明 JWT 鉴权方式

**检验结果**: ✅ API 文档已生成并验证

### 场景 2: 优化现有数据库文档

适用于分析现有数据库设计文档，提供优化建议。

**执行流程**:
1. 智能体读取用户提供的数据库设计文档
2. 调用 `scripts/validate_sql.py` 验证 DDL 语法
3. 分析索引策略、字段类型、约束定义
4. 提供优化建议（如添加联合索引、优化字段长度）

**关键要点**:
- 检查主键、外键、唯一约束是否完整
- 分析索引是否覆盖常用查询场景
- 验证字段类型是否合理（如 VARCHAR 长度）
- 提供数据字典的完整性建议

**检验结果**: ✅ 数据库文档已优化

### 场景 3: 定义游戏实时通信协议

适用于多人在线游戏设计 WebSocket + Protobuf 通信协议。

**执行流程**:
1. 智能体与用户澄清游戏类型和通信需求
2. 参考 `references/protocol-template.md` 和 `references/protobuf-guide.md`
3. 生成 .proto 定义文件和 WebSocket 消息格式
4. 调用 `scripts/validate_protobuf.py` 验证语法

**关键要点**:
- 定义消息 ID 和指令码（如 CMD_LOGIN, CMD_MOVE）
- 说明心跳机制和超时断连策略
- 提供错误处理和频率限制规则
- 包含完整的请求/响应示例

**检验结果**: ✅ 通信协议已定义并验证

### 场景 4: 处理多端差异

适用于需要为 Web、移动端、小程序生成差异化文档。

**执行流程**:
1. 识别多端需求（Web、移动端、小程序）
2. 为不同终端定义不同的响应字段
3. 标注字段差异说明
4. 提供不同终端的接口版本号

**关键要点**:
- Web 端：返回完整字段、分页信息、权限标记
- 移动端：精简字段、减少嵌套层级、压缩数据量
- 小程序：兼容性考虑（如避免使用最新特性）

**检验结果**: ✅ 多端差异化文档已生成

---

## 工作流程

### 简化版流程

```
1. 需求分析 → 2. 文档生成 → 3. 格式验证 → 4. 完整性校验
```

### 详细版流程

#### 第一步：查阅信息

1. **需求分析与澄清**
   - 询问目标语言/架构（如 Java/SpringBoot、Go/Gin、Python/Django 等）
   - 确认需要生成的文档类型（API/数据库/协议，或全部）
   - 明确多端需求（Web、移动端、小程序等）
   - 如果提供的是架构文档或需求文档，读取并提取关键信息

2. **信息补充与搜索**（如遇陌生架构）
   - 使用搜索工具查找目标语言/架构的最佳实践和规范
   - 获取特定框架的接口定义标准（如 SpringBoot 的 RESTful 规范）
   - 了解目标数据库的特性（MySQL/PostgreSQL/Oracle 等）

#### 第二步：执行操作

1. **文档生成**
   - **API 接口文档**：
     - 参考 `references/api-doc-template.md` 的模板结构
     - 生成 OpenAPI 3.0 格式或 Postman Collection 格式
     - 包含：基础信息、请求参数、响应结构、错误码、鉴权方式、多端差异
     - 使用 `scripts/validate_openapi.py` 验证格式正确性
   - **数据库设计文档**：
     - 参考 `references/db-doc-template.md` 的模板结构
     - 生成表结构清单、数据字典、索引策略、关系图
     - 使用 `scripts/validate_sql.py` 验证 DDL 语法正确性
   - **协议与通信规范**：
     - 参考 `references/protocol-template.md` 的模板结构
     - 根据场景选择 WebSocket 或二进制协议（Protobuf/FlatBuffers）
     - 生成 IDL 定义文件、消息帧结构、业务指令集
     - 使用 `scripts/validate_protobuf.py` 验证 .proto 文件语法

2. **完整性校验**
   - 检查文档是否包含所有必需章节
   - 确认示例数据的完整性
   - 验证格式规范的一致性

#### 第三步：检查验收

1. **格式验证**
   - 使用 `scripts/validate_openapi.py` 验证 OpenAPI 格式
   - 使用 `scripts/validate_protobuf.py` 验证 Protobuf 格式
   - 使用 `scripts/validate_sql.py` 验证 SQL 语法

2. **完整性检查**
   - API 文档：请求参数、响应结构、错误码、鉴权说明
   - 数据库文档：表结构、数据字典、索引策略
   - 协议文档：连接建立、消息格式、错误处理

3. **规范性分析**
   - 检查命名规范、字段类型、约束定义是否符合最佳实践
   - 提供优化建议

---

## 资源索引

### 格式验证脚本

| 脚本 | 用途 |
|------|------|
| `scripts/validate_openapi.py` | 验证 OpenAPI 3.0/YAML 格式 |
| `scripts/validate_protobuf.py` | 验证 Protobuf .proto 文件语法 |
| `scripts/validate_sql.py` | 验证 SQL DDL 语法正确性 |

### 文档模板

| 模板 | 用途 |
|------|------|
| `references/api-doc-template.md` | 生成 API 接口文档时参考 |
| `references/db-doc-template.md` | 生成数据库设计文档时参考 |
| `references/protocol-template.md` | 生成协议与通信规范时参考 |

### 技术参考

| 文档 | 用途 |
|------|------|
| `references/openapi-cheatsheet.md` | 编写 OpenAPI 规范时查阅 |
| `references/protobuf-guide.md` | 使用 Protobuf 协议时查阅 |
| `references/websocket-guide.md` | 定义 WebSocket 协议时查阅 |

---

## 命令速查

```bash
# 验证 OpenAPI 格式
python scripts/validate_openapi.py openapi.yaml

# 验证 Protobuf 格式
python scripts/validate_protobuf.py schema.proto

# 验证 SQL DDL 语法
python scripts/validate_sql.py schema.sql
```

---

## 常见问题（FAQ）

### Q1: 如何确定使用哪种文档模板？

**A**: 根据需求选择：
- 需要定义 API 接口 → 使用 `references/api-doc-template.md`
- 需要设计数据库表结构 → 使用 `references/db-doc-template.md`
- 需要定义通信协议 → 使用 `references/protocol-template.md`

### Q2: 验证脚本失败怎么办？

**A**: 检查以下几点：
1. 文件路径是否正确
2. 文件格式是否符合规范（YAML/JSON/SQL）
3. 依赖包是否已安装（pyyaml、jsonschema、protobuf）

### Q3: 如何处理多端差异？

**A**: 在文档中明确标注：
- 为不同终端定义不同的响应字段
- 标注字段差异说明
- 提供不同终端的接口版本号

### Q4: 需求变更后如何更新文档？

**A**: 使用需求变更分析功能：
1. 对比变更前后的文档差异
2. 分析影响范围（哪些接口/表/协议受影响）
3. 提供兼容性建议

---

## 注意事项

- **格式验证优先**: 仅在需要格式验证时调用脚本，文档生成主要由智能体完成
- **知识补全**: 当遇到不熟悉的技术栈时，使用搜索工具补充信息
- **完整性保证**: 确保文档包含完整的示例和错误码说明
- **多端差异**: 多端差异需明确标注，避免混淆
- **变更分析**: 需求变更时，分析影响范围并提供兼容性建议
- **最佳实践**: 遵循目标语言/架构的最佳实践和规范
- **命名规范**: 确保命名规范、字段类型、约束定义符合标准

---

## 前置准备

### 依赖说明

scripts 脚本所需的依赖包及版本：

```
pyyaml>=6.0
jsonschema>=4.17.0
protobuf>=4.21.0
```

---

**最后更新**: 2026-03-06  
**版本**: v1.0.0  
**状态**: ✅ 可用
