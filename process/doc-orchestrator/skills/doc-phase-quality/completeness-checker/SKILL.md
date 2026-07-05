---
name: completeness-checker
version: 0.1.1
description: Use when the user needs to check whether a document has all required sections, examples, and supporting material.
tags: [completeness, sections, examples, documentation]
---

# Completeness Checker

## 职责

- 检查文档是否包含所有必需章节
- 检查示例是否完整（请求/响应、配置示例等）
- 检查是否缺少关键信息
- 输出缺失清单

## 输入

- 文档集
- 各文档类型的必需章节定义

## 输出

```yaml
completeness_result:
  score: 0.85
  missing_sections:
    - doc: "API-001"
      section: "错误码"
      severity: error
      description: "API文档必须包含错误码说明"
    - doc: "TEST-001"
      section: "多端兼容测试矩阵"
      severity: warning
      description: "建议包含多端兼容性测试说明"
  missing_examples:
    - doc: "API-001"
      endpoint: "POST /api/v1/users"
      detail: "缺少响应示例"
```

## 必需章节定义

### 需求文档（SRS/PRD）

| 章节 | 必需 | 可选 |
|------|------|------|
| 引言/概述 | ✅ | |
| 系统概述 | ✅ | |
| 功能需求 | ✅ | |
| 非功能需求 | ✅ | |
| 接口需求 | | ✅ |
| 数据需求 | | ✅ |
| 约束与假设 | ✅ | |

### 架构文档（SAD/TDD）

| 章节 | 必需 | 可选 |
|------|------|------|
| 架构概述 | ✅ | |
| 系统上下文 | ✅ | |
| 架构视图 | ✅ | |
| 技术选型 | ✅ | |
| 模块设计 | ✅ | |
| 数据架构 | ✅ | |
| 安全架构 | ✅ | |
| 性能策略 | | ✅ |
| 容错与可用性 | | ✅ |

### API 文档

| 章节 | 必需 | 可选 |
|------|------|------|
| 概述 | ✅ | |
| 基础信息 | ✅ | |
| 认证与授权 | ✅ | |
| 通用规范 | ✅ | |
| 错误码 | ✅ | |
| 接口详情 | ✅ | |
| 多端差异 | | ✅ |

## 注意事项

- 必需章节缺失为 error，必须补充
- 可选章节缺失为 warning，建议补充
- 小项目可适当降低完整性要求
- 示例必须可运行/可理解
