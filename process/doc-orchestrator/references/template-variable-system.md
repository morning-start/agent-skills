# 模板变量系统

本文档定义模板变量命名规范、类型和使用规则，确保模板变量的一致性和可维护性。

## 变量命名规范

### 命名规则

- 使用 snake_case：`project_name`, `tech_stack`
- 小写字母 + 下划线分隔
- 变量名应语义清晰，避免缩写

### 变量类型

| 类型 | 标记 | 说明 | 示例 |
|------|------|------|------|
| 必填 | `{{*var}}` | 必须有值，否则报错 | `{{*project_name}}` |
| 可选 | `{{?var}}` | 可为空，默认空字符串 | `{{?description}}` |
| 普通 | `{{var}}` | 应有值，缺失时警告 | `{{version}}` |

## 变量分类

### 项目级变量（所有文档通用）

| 变量 | 类型 | 说明 | 来源 |
|------|------|------|------|
| `project_name` | 必填 | 项目名称 | 用户输入 |
| `project_type` | 必填 | 项目类型 | project-analyzer |
| `version` | 必填 | 项目版本 | 用户输入/默认 1.0.0 |
| `author` | 可选 | 作者 | 用户输入 |
| `created_date` | 必填 | 创建日期 | 自动生成 |
| `tech_stack` | 必填 | 技术栈列表 | project-analyzer |
| `platforms` | 必填 | 目标平台 | project-analyzer |
| `description` | 可选 | 项目描述 | 用户输入 |

### 业务变量（需求文档专用）

| 变量 | 类型 | 说明 | 来源 |
|------|------|------|------|
| `target_users` | 必填 | 目标用户 | requirement-parser |
| `core_features` | 必填 | 核心功能列表 | requirement-parser |
| `user_personas` | 必填 | 用户画像 | requirement-parser |
| `user_journeys` | 可选 | 用户旅程 | requirement-parser |
| `business_goals` | 必填 | 业务目标 | requirement-parser |
| `success_metrics` | 可选 | 成功指标 | requirement-parser |

### 架构变量（架构文档专用）

| 变量 | 类型 | 说明 | 来源 |
|------|------|------|------|
| `architecture_pattern` | 必填 | 架构模式 | architecture-producer |
| `modules` | 必填 | 模块列表 | architecture-producer |
| `external_dependencies` | 必填 | 外部依赖 | architecture-producer |
| `deployment_strategy` | 必填 | 部署策略 | architecture-producer |
| `scalability_plan` | 可选 | 扩展计划 | architecture-producer |
| `security_measures` | 必填 | 安全措施 | architecture-producer |

### API 变量（API 文档专用）

| 变量 | 类型 | 说明 | 来源 |
|------|------|------|------|
| `base_url` | 必填 | API 基础 URL | api-producer |
| `auth_method` | 必填 | 认证方式 | api-producer |
| `api_version` | 必填 | API 版本 | api-producer |
| `endpoints` | 必填 | 接口列表 | api-producer |
| `error_codes` | 必填 | 错误码列表 | api-producer |
| `rate_limit` | 可选 | 速率限制 | api-producer |

### 数据变量（数据文档专用）

| 变量 | 类型 | 说明 | 来源 |
|------|------|------|------|
| `db_type` | 必填 | 数据库类型 | data-producer |
| `db_version` | 必填 | 数据库版本 | data-producer |
| `tables` | 必填 | 表列表 | data-producer |
| `indexes` | 必填 | 索引列表 | data-producer |
| `backup_strategy` | 可选 | 备份策略 | data-producer |

## 模板变量使用示例

```markdown
# {{*project_name}} - 软件需求规格说明书

## 版本信息

| 项目 | 内容 |
|------|------|
| 版本 | {{version}} |
| 日期 | {{created_date}} |
| 作者 | {{?author}} |

## 项目概述

{{*project_name}} 是一个 {{project_type}} 项目，使用以下技术栈：

{{#tech_stack}}
- {{.}}
{{/tech_stack}}

## 功能需求

{{#core_features}}
### {{name}}
{{description}}
{{/core_features}}
```

## 变量解析流程

1. template-selector 读取模板
2. 提取所有变量（必填/可选/普通）
3. 从 project-profile.yaml 和 requirement-parser 填充变量
4. 检查必填变量是否有值
5. 生成填充后的模板

## 注意事项

- 必填变量必须在生成前填充
- 可选变量为空时显示默认值（空字符串或 N/A）
- 普通变量缺失时记录 warning
- 变量名在模板中必须唯一
- 循环变量使用 `{{#var}}...{{/var}}` 语法
