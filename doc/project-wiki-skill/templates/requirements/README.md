# 需求文档模板

本目录包含需求分析和功能文档模板。

## 模板列表

| 模板 | 用途 | 变量说明 |
|------|------|----------|
| [functional-doc-template.md](./functional-doc-template.md) | 功能需求文档 | `{{function_name}}`, `{{description}}`, `{{priority}}` 等 |
| [requirement-doc-template.md](./requirement-doc-template.md) | 详细需求文档 | `{{requirement_title}}`, `{{business_need}}`, `{{constraints}}` 等 |
| [rtm-template.md](./rtm-template.md) | 需求追踪矩阵 | `{{requirement_id}}`, `{{design_section}}`, `{{test_case}}` 等 |

## 变量命名规范

- 必填变量：`{{*variable_name}}` (星号前缀)
- 可选变量：`{{?variable_name}}` (问号前缀)
- 普通变量：`{{variable_name}}`

## 使用方式

### 方式一：使用生成脚本（推荐）

```bash
# 进入 project-wiki 目录
cd project-wiki

# 运行生成脚本
python scripts/generate-doc.py --template requirements/functional-doc-template.md --output ../my-project/requirements/function-name.md
```

### 方式二：手动填写

1. 复制模板文件到项目目录
2. 搜索所有 `{{variable_name}}` 格式的变量
3. 替换为实际内容
4. 保存文件

## 变量说明

### functional-doc-template.md 变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `{{*function_name}}` | 是 | - | 功能名称 |
| `{{*description}}` | 是 | - | 功能描述 |
| `{{priority}}` | 否 | P1 | 优先级 (P0/P1/P2/P3) |
| `{{target_users}}` | 否 | - | 目标用户群体 |

### requirement-doc-template.md 变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `{{*requirement_title}}` | 是 | - | 需求标题 |
| `{{*business_need}}` | 是 | - | 业务需求描述 |
| `{{constraints}}` | 否 | - | 约束条件列表 |

### rtm-template.md 变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `{{*requirement_id}}` | 是 | - | 需求 ID (如 REQ-001) |
| `{{*design_section}}` | 是 | - | 对应设计文档章节 |
| `{{test_case}}` | 否 | - | 对应测试用例 |

---

**最后更新**: 2026-03-06
