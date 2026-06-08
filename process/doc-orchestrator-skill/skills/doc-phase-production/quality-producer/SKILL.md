---
name: quality-producer
version: 0.1.1
description: Use when the user needs quality, testing, deployment, operations, or security documentation.
tags: [quality, testing, operations, security, documentation]
---

# Quality Producer

## 职责

- 生成测试策略与计划文档
- 生成部署与运维手册
- 生成安全合规文档
- 为文档添加追溯关系

## 输入

- 模板路径（templates/quality/）
- 项目 profile
- 架构文档

## 输出

- 测试策略文档
- 部署运维手册
- 安全合规文档

## 测试策略文档结构

```markdown
---
doc:
  id: "TEST-001"
  type: "quality"
  subtype: "test"
  version: "1.0.0"
  status: "draft"
  traceability:
    depends_on: ["REQ-001", "ARCH-001"]
    feeds_into: []
---

# 测试策略与计划

## 1. 测试概述
- 目标、范围、策略

## 2. 测试类型
- 单元测试、集成测试、E2E 测试、性能测试、安全测试

## 3. 测试覆盖率目标
- 各测试类型覆盖率目标

## 4. 测试环境
- 开发环境、测试环境、预发环境

## 5. 测试工具链
- 工具选型、配置

## 6. 多端兼容测试矩阵
- Web/移动端/桌面端兼容性

## 7. 测试进度与里程碑
- 阶段划分、交付物

## 8. 风险与应对
- 识别风险、应对策略
```

## 部署运维手册结构

```markdown
---
doc:
  id: "OPS-001"
  type: "quality"
  subtype: "ops"
  version: "1.0.0"
  status: "draft"
---

# 部署与运维手册

## 1. 系统架构
- 部署架构图、组件说明

## 2. 环境配置
- 开发/测试/生产环境差异

## 3. 部署流程
- CI/CD 配置、部署步骤、验证

## 4. 容器化配置
- Dockerfile、docker-compose、K8s

## 5. 监控告警
- 指标、告警规则、仪表盘

## 6. 日志管理
- 日志收集、存储、分析

## 7. 故障恢复
- 常见问题、排查流程、回滚

## 8. 扩缩容策略
- 自动扩缩容配置
```

## 安全合规文档结构

```markdown
---
doc:
  id: "SEC-001"
  type: "quality"
  subtype: "security"
  version: "1.0.0"
  status: "draft"
---

# 安全合规文档

## 1. 隐私合规
- GDPR/CCPA/网络安全法等

## 2. 数据安全
- 加密、脱敏、备份策略

## 3. 访问控制
- 认证、授权、审计

## 4. 第三方合规
- SDK 清单、合规性说明

## 5. 应急响应
- 安全事件处理流程
```

## 注意事项

- 测试策略必须与需求覆盖率对应
- 部署运维必须包含完整的故障恢复流程
- 安全合规必须识别目标市场法规
- 追溯关系 depends_on 指向需求和架构文档
