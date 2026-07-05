---
name: template-selector
version: 0.1.1
description: Use when the user needs to choose the right documentation template for a document type or project context.
tags: [template-selection, planning, documentation]
---

# Template Selector

## 职责

- 根据文档类型从模板库选择对应模板
- 根据项目类型选择平台特定的模板变体
- 初始化模板变量
- 输出模板路径和变量映射

## 输入

- 文档清单（来自 doc-planner）
- 项目 profile（project-profile.yaml）

## 输出

```yaml
template_mappings:
  REQ-001:
    path: templates/requirements/srs.md
    variables:
      project_name: "..."
      version: "1.0.0"
      platforms: ["web"]
  REQ-002:
    path: templates/requirements/prd.md
    variables:
      project_name: "..."
      user_personas: [...]
```

## 选择规则

| 文档类型 | 默认模板 | 平台变体 |
|----------|---------|---------|
| requirement/srs | templates/requirements/srs.md | game → templates/requirements/srs-game.md |
| requirement/prd | templates/requirements/prd.md | mobile → templates/requirements/prd-mobile.md |
| architecture/sad | templates/architecture/sad.md | web/mobile/desktop/game |
| api | templates/api/endpoint.md | rest/graphql/grpc |
| data/database | templates/data/database.md | mysql/postgresql/mongodb |
| quality/test | templates/quality/test-strategy.md | frontend/backend/mobile |

## 变量初始化规则

1. 从 project-profile.yaml 提取公共变量
2. 从 requirement-parser 提取业务变量
3. 未定义的变量标记为 `{{?variable_name}}`（可选）待后续补充

## 注意事项

- 模板不存在时，使用最接近的模板并标注 warning
- 变量名必须与模板中的占位符完全匹配
- 支持模板继承和覆盖
