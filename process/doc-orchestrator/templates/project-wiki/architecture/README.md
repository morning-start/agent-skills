# 架构设计模板

本目录包含系统架构和设计文档模板。

## 模板列表

| 模板 | 用途 | 变量说明 |
|------|------|----------|
| [ARCHITECTURE.md](./ARCHITECTURE.md) | 系统架构设计 | `{{project_name}}`, `{{tech_stack}}`, `{{architecture_diagram}}` 等 |
| [design-doc-template.md](./design-doc-template.md) | 详细设计文档 | `{{design_title}}`, `{{author}}`, `{{version}}` 等 |
| [api-template.md](./api-template.md) | API 接口文档 | `{{api_name}}`, `{{endpoint}}`, `{{method}}` 等 |
| [architecture-doc-template.md](./architecture-doc-template.md) | 架构文档模板 | `{{system_name}}`, `{{components}}`, `{{relationships}}` 等 |

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
python scripts/generate-doc.py --template architecture/ARCHITECTURE.md --output ../my-project/ARCHITECTURE.md
```

### 方式二：手动填写

1. 复制模板文件到项目目录
2. 搜索所有 `{{variable_name}}` 格式的变量
3. 替换为实际内容
4. 保存文件

## 变量说明

### ARCHITECTURE.md 变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `{{*project_name}}` | 是 | - | 项目名称 |
| `{{*tech_stack}}` | 是 | - | 技术栈列表 |
| `{{architecture_diagram}}` | 否 | - | 架构图 (Mermaid 格式) |

### design-doc-template.md 变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `{{*design_title}}` | 是 | - | 设计文档标题 |
| `{{*author}}` | 是 | - | 作者姓名 |
| `{{version}}` | 否 | v1.0 | 版本号 |
| `{{create_date}}` | 否 | - | 创建日期 (YYYY-MM-DD) |

### api-template.md 变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `{{*api_name}}` | 是 | - | API 名称 |
| `{{*endpoint}}` | 是 | - | API 路径 |
| `{{*method}}` | 是 | - | HTTP 方法 (GET/POST/PUT/DELETE) |
| `{{?version}}` | 否 | v1 | API 版本 |

---

**最后更新**: 2026-03-06
