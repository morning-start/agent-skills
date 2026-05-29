# 知识库模板

本目录包含技术知识库文档模板。

## 模板列表

| 模板 | 用途 | 变量说明 |
|------|------|----------|
| [knowledge-template.md](./knowledge-template.md) | 技术知识库模板 | `{{tech_name}}`, `{{description}}`, `{{version}}` 等 |
| [consistency-checklist-template.md](./consistency-checklist-template.md) | 一致性检查清单 | `{{check_date}}`, `{{checker}}`, `{{items}}` 等 |

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
python scripts/generate-doc.py --template knowledge/knowledge-template.md --output ../my-project/knowledge/tech-name.md
```

### 方式二：手动填写

1. 复制模板文件到项目目录
2. 搜索所有 `{{variable_name}}` 格式的变量
3. 替换为实际内容
4. 保存文件

## 变量说明

### knowledge-template.md 变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `{{*tech_name}}` | 是 | - | 技术栈名称 |
| `{{*description}}` | 是 | - | 技术描述 |
| `{{version}}` | 否 | - | 版本号 |
| `{{official_website}}` | 否 | - | 官方网站 URL |

### consistency-checklist-template.md 变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `{{*check_date}}` | 是 | - | 检查日期 (YYYY-MM-DD) |
| `{{*checker}}` | 是 | - | 检查人姓名 |
| `{{items}}` | 否 | - | 检查项列表 |

---

**最后更新**: 2026-03-06
