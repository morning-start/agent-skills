---
name: doc-phase-production
version: 0.1.1
description: Use when the user needs document generation, diagram generation, or a production step for a planned document set.
tags: [production, document-generation, diagramming, documentation]
---

# Production Phase Coordinator

## 职责

- 按 doc-plan 执行文档生成
- 管理文档间的追溯关系
- 智能生成图示（TXT/Mermaid）
- 输出完整文档集

## 子技能

| 执行者 | 职责 | 路径 |
|--------|------|------|
| requirements-producer | 需求文档生成 | [查看](requirements-producer/SKILL.md) |
| architecture-producer | 架构文档生成 | [查看](architecture-producer/SKILL.md) |
| api-producer | API 文档生成 | [查看](api-producer/SKILL.md) |
| data-producer | 数据文档生成 | [查看](data-producer/SKILL.md) |
| quality-producer | 质量运维文档生成 | [查看](quality-producer/SKILL.md) |
| diagram-producer | 智能绘图 | [查看](diagram-producer/SKILL.md) |

## 输入

- `doc-plan.yaml`（来自 planning 阶段）
- `project-profile.yaml`
- 模板文件（来自 templates/）

## 输出

- 完整的文档集（Markdown 格式）
- 每份文档包含 YAML front matter（双轨格式）
- 文档间建立追溯关系

## 工作流程

1. 按执行计划逐 phase 生成文档
2. 每个执行者读取对应模板和项目信息
3. 生成文档内容，填充变量
4. 添加 YAML front matter
5. 建立追溯关系（depends_on, feeds_into）
6. 调用 diagram-producer 生成图示
7. 输出到目标目录

## 双轨格式要求

所有生成的文档必须包含 YAML front matter：

```yaml
---
doc:
  id: "REQ-001"
  type: "requirement"
  version: "1.0.0"
  status: "draft"
  created: "2026-05-02"
  traceability:
    depends_on: []
    feeds_into: ["ARCH-001"]
---
```

## 注意事项

- 文档生成顺序必须遵循依赖关系
- 追溯关系必须双向对应（A feeds_into B 则 B depends_on A）
- 图示默认智能选择，不需要用户指定
- 生成失败时标注错误并继续后续文档
- 所有文档使用统一的术语和命名
