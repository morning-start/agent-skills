---
name: doc-phase-planning
version: 0.1.1
description: Use when the user needs document planning, template selection, or execution order design after project analysis.
tags: [planning, document-plan, template-selection, documentation]
---

# Planning Phase Coordinator

## 职责

- 根据项目 profile 规划需要生成的文档清单
- 为每种文档类型选择合适的模板
- 生成文档生成执行计划
- 输出标准化的 `doc-plan.yaml`

## 子技能

| 执行者 | 职责 | 路径 |
|--------|------|------|
| doc-planner | 文档清单规划 | [查看](doc-planner/SKILL.md) |
| template-selector | 模板选择 | [查看](template-selector/SKILL.md) |
| schedule-builder | 执行计划生成 | [查看](schedule-builder/SKILL.md) |

## 输入

- `project-profile.yaml`（来自 analysis 阶段）

## 输出

```yaml
doc-plan:
  project_type: fullstack
  scale: medium
  doc_list:
    - id: REQ-001
      type: requirement
      subtype: srs
      template: templates/requirements/srs.md
      priority: must
      depends_on: []
    - id: REQ-002
      type: requirement
      subtype: prd
      template: templates/requirements/prd.md
      priority: must
      depends_on: []
    - id: ARCH-001
      type: architecture
      subtype: sad
      template: templates/architecture/sad.md
      priority: must
      depends_on: [REQ-001]
    - id: API-001
      type: api
      template: templates/api/endpoint.md
      priority: must
      depends_on: [ARCH-001]
  execution_order:
    - [REQ-001, REQ-002]
    - [ARCH-001]
    - [API-001]
```

## 工作流程

1. 读取 project-profile.yaml
2. 调用 doc-planner 根据项目类型和规模规划文档清单
3. 调用 template-selector 为每个文档选择模板
4. 调用 schedule-builder 生成依赖关系和执行顺序
5. 输出 doc-plan.yaml

## 注意事项

- 小项目自动裁剪非必要文档（如测试策略可简化为检查清单）
- 大项目增加文档粒度（如 API 按模块拆分）
- 依赖关系必须正确反映文档间的追溯需求
- 用户可自定义裁剪文档清单
