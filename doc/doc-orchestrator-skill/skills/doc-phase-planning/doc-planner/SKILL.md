---
name: doc-planner
version: 0.1.0
description: 根据项目类型和规模规划需要生成的文档清单
---

# Doc Planner

## 职责

- 根据项目类型确定需要的文档类别
- 根据项目规模调整文档粒度
- 建立文档间的依赖关系
- 输出文档清单列表

## 输入

- `project-profile.yaml`

## 输出

```yaml
doc_list:
  - id: REQ-001
    type: requirement
    subtype: srs
    priority: must
  - id: REQ-002
    type: requirement
    subtype: prd
    priority: must
  - id: ARCH-001
    type: architecture
    subtype: sad
    priority: must
  - id: API-001
    type: api
    priority: must
```

## 文档规划规则

### 按项目类型

| 项目类型 | 必需文档 | 可选文档 |
|----------|---------|---------|
| frontend | SRS、PRD、组件文档 | 测试策略 |
| backend | SRS、PRD、架构、API | 部署运维 |
| fullstack | SRS、PRD、架构、API、数据 | 测试策略、部署运维 |
| mobile | SRS、PRD、架构、API | 安全合规 |
| desktop | SRS、PRD、架构 | 测试策略 |
| game | SRS、架构、协议 | 安全合规、性能测试 |
| cli | SRS、API（CLI命令） | - |

### 按项目规模

| 规模 | 文档策略 |
|------|---------|
| small | 仅必需文档，内容精简 |
| medium | 必需文档 + 可选文档 |
| large | 全部文档，按模块拆分 |

## 注意事项

- 依赖关系必须形成 DAG，不能有循环
- 优先级 must 的文档必须在 first tier 生成
- 用户可手动增删文档
