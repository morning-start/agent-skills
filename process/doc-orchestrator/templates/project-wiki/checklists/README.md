# 检查清单模板

本目录包含文档评审和检查清单模板。

## 模板列表

| 模板 | 用途 | 变量说明 |
|------|------|----------|
| [document-review-checklist.md](./document-review-checklist.md) | 文档评审清单 | `{{document_name}}`, `{{reviewer}}`, `{{review_date}}` 等 |
| [task-execution-template.md](./task-execution-template.md) | 任务执行模板 | `{{task_id}}`, `{{task_name}}`, `{{owner}}` 等 |
| [acceptance-report-template.md](./acceptance-report-template.md) | 任务验收报告 | `{{task_id}}`, `{{acceptance_date}}`, `{{reviewers}}` 等 |
| [lightweight-doc-management-process.md](./lightweight-doc-management-process.md) | 轻量级文档管理流程 | `{{team_name}}`, `{{process_steps}}`, `{{roles}}` 等 |

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
python scripts/generate-doc.py --template checklists/document-review-checklist.md --output ../my-project/checklists/review-checklist.md
```

### 方式二：手动填写

1. 复制模板文件到项目目录
2. 搜索所有 `{{variable_name}}` 格式的变量
3. 替换为实际内容
4. 保存文件

## 变量说明

### document-review-checklist.md 变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `{{*document_name}}` | 是 | - | 文档名称 |
| `{{*reviewer}}` | 是 | - | 评审人姓名 |
| `{{review_date}}` | 否 | - | 评审日期 (YYYY-MM-DD) |
| `{{check_items}}` | 否 | - | 检查项列表 |

### lightweight-doc-management-process.md 变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `{{*team_name}}` | 是 | - | 团队名称 |
| `{{process_steps}}` | 否 | - | 流程步骤列表 |
| `{{roles}}` | 否 | - | 角色职责列表 |

---

**最后更新**: 2026-03-06
