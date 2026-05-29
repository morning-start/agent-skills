# 双轨格式协议

本文档定义文档的双轨格式规范，同时满足 Agent 可解析和人类可读的需求。

## 格式架构

```
┌─────────────────────────────────────────────┐
│              YAML Front Matter              │  ← Agent 可解析
│  结构化元数据：ID、类型、版本、追溯链、质量分 │
├─────────────────────────────────────────────┤
│                                             │
│              Markdown Body                   │  ← 人类可读
│  自然语言正文：章节、图表、代码示例           │
│                                             │
└─────────────────────────────────────────────┘
```

## YAML Front Matter 规范

### 必填字段

```yaml
---
doc:
  id: "REQ-001"                    # 文档唯一标识
  type: "requirement"              # 文档大类
  subtype: "srs"                   # 文档子类型（可选）
  version: "1.0.0"                 # 语义化版本号
  status: "draft"                  # 文档状态
  created: "2026-05-02"           # 创建日期
---
```

### 可选字段

```yaml
---
doc:
  id: "REQ-001"
  type: "requirement"
  version: "1.0.0"
  status: "draft"
  
  title: "软件需求规格说明书"       # 文档标题（可选，默认从正文提取）
  author: "doc-orchestrator"       # 作者
  updated: "2026-05-02"           # 最后更新日期
  
  traceability:                    # 追溯关系
    depends_on: ["REQ-001"]        # 依赖的文档 ID
    feeds_into: ["ARCH-001"]       # 被依赖的文档 ID
  
  metadata:                        # 元数据
    project_name: "电商平台"
    project_type: "fullstack"
    tech_stack: ["react", "node", "postgres"]
    platforms: ["web", "mobile"]
  
  quality:                         # 质量指标（由 quality 阶段填充）
    completeness: 0.85
    consistency_score: 0.92
    overall_score: 0.87
    last_validated: "2026-05-02"
  
  tags: ["auth", "user"]           # 标签
---
```

### 字段定义

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | ✅ | 格式：`{PREFIX}-{NNN}` |
| type | string | ✅ | 见文档类型目录 |
| subtype | string | | 细分类型 |
| version | string | ✅ | 语义化版本 `MAJOR.MINOR.PATCH` |
| status | string | ✅ | draft/review/approved/deprecated |
| created | string | ✅ | ISO 8601 日期 |
| updated | string | | 最后更新日期 |
| title | string | | 文档标题 |
| author | string | | 文档作者 |
| traceability | object | | 追溯关系 |
| metadata | object | | 项目元数据 |
| quality | object | | 质量指标 |
| tags | string[] | | 分类标签 |

## Markdown Body 规范

### 标题层级

```markdown
# 一级标题（文档标题，仅一个）
## 二级标题（主要章节）
### 三级标题（子章节）
#### 四级标题（详细内容）
```

- 必须从 `#` 开始，仅一个
- 不能跳级（如从 `##` 直接到 `####`）
- 标题命名：中文为主，英文可选

### 代码块

````markdown
```yaml
# 必须标注语言
key: value
```
````

- 必须标注语言标签
- 支持：yaml, json, javascript, python, bash, sql, mermaid
- 复杂代码可添加行号注释

### 表格

```markdown
| 列 1 | 列 2 | 列 3 |
|------|------|------|
| 数据 1 | 数据 2 | 数据 3 |
```

- 表头必须有分隔线
- 列对齐可选
- 复杂表格可改用列表

### 图示

- TXT 字符图：直接放在代码块中
- Mermaid 图：使用 ````mermaid` 代码块

## Agent 操作能力

### 文档检索

```yaml
# 按类型检索
filter:
  type: "api"
  
# 按追溯检索
filter:
  feeds_into: "ARCH-001"
  
# 按质量检索
filter:
  quality.overall_score: "< 0.80"
```

### 变更分析

```yaml
# 追溯变更影响
change:
  affected_id: "REQ-001"
  trace:
    - "ARCH-001"
    - "API-001"
    - "TEST-001"
```

### 批量更新

```yaml
# 批量更新版本号
update:
  version: "1.1.0"
  filter:
    type: "*"
```

## 格式验证规则

1. YAML front matter 必须以 `---` 开始和结束
2. 必填字段不能为空
3. id 必须符合命名规范
4. version 必须符合语义化版本规范
5. status 必须是枚举值之一
6. traceability 中的 ID 必须在文档集中存在

## 注意事项

- Agent 格式不可删除，必须保留在文档头部
- 人类格式可自由编辑正文内容
- 变更正文时同步更新 YAML front matter 的 updated 字段
- 质量分数由 quality 阶段自动填充，不应手动修改
