---
name: architecture-producer
version: 0.1.0
description: 生成架构类文档（SAD、TDD、平台专项架构）
---

# Architecture Producer

## 职责

- 根据模板生成 SAD（系统架构设计）
- 根据模板生成 TDD（技术方案设计）
- 生成平台专项架构文档（Web/移动/桌面/游戏）
- 为文档添加追溯关系

## 输入

- 模板路径（templates/architecture/）
- 项目 profile
- 需求文档（SRS/PRD）

## 输出

- SAD 文档
- TDD 文档
- 平台架构文档

## SAD 文档结构

```markdown
---
doc:
  id: "ARCH-001"
  type: "architecture"
  subtype: "sad"
  version: "1.0.0"
  status: "draft"
  traceability:
    depends_on: ["REQ-001"]
    feeds_into: ["API-001", "DATA-001"]
---

# 系统架构设计文档

## 1. 架构概述
- 设计目标、约束、假设

## 2. 系统上下文
- 系统边界、外部依赖、用户角色

## 3. 架构视图
- 逻辑视图（模块划分）
- 物理视图（部署架构）
- 开发视图（技术栈）
- 进程视图（运行时交互）

## 4. 技术选型
- 语言、框架、中间件、数据库
- 选型理由和对比

## 5. 模块设计
- 模块职责、接口、依赖

## 6. 数据架构
- 数据模型、存储策略、缓存策略

## 7. 安全架构
- 认证、授权、加密、审计

## 8. 性能策略
- 缓存、负载均衡、异步处理

## 9. 容错与可用性
- 降级策略、熔断、重试、限流

## 10. 附录
- 架构图、术语表
```

## TDD 文档结构

```markdown
---
doc:
  id: "ARCH-002"
  type: "architecture"
  subtype: "tdd"
  version: "1.0.0"
  status: "draft"
  traceability:
    depends_on: ["ARCH-001"]
    feeds_into: ["API-001"]
---

# 技术方案设计文档

## 1. 模块概述
- 职责、范围、边界

## 2. 详细设计
- 类图、序列图、状态图

## 3. 接口契约
- API 定义、消息格式

## 4. 数据模型
- 表结构、字段定义

## 5. 关键算法
- 伪代码、流程图

## 6. 异常处理
- 错误码、重试策略

## 7. 测试策略
- 测试重点、Mock 方案
```

## 平台专项

| 平台 | 专项内容 |
|------|---------|
| Web | 响应式策略、BFF 层、CDN 策略 |
| Mobile | 离线策略、推送服务、权限管理 |
| Desktop | 进程隔离、系统 API、更新策略 |
| Game | 渲染管线、网络同步、资源管理 |

## 注意事项

- 架构设计必须与需求一致
- 技术选型必须有理由
- 必须包含架构图（调用 diagram-producer）
- 追溯关系 depends_on 指向需求文档，feeds_into 指向 API/数据文档
