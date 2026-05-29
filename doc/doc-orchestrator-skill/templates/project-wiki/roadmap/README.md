# 规划文档模板

本目录包含项目规划和路线图模板。

## 模板列表

| 模板 | 用途 | 变量说明 |
|------|------|----------|
| [ROADMAP.md](./ROADMAP.md) | 项目路线图 | `{{project_name}}`, `{{milestones}}`, `{{timeline}}` 等 |
| [version-entry-template.md](./version-entry-template.md) | 版本发布说明模板 | `{{version}}`, `{{release_date}}`, `{{changes}}` 等 |

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
python scripts/generate-doc.py --template roadmap/ROADMAP.md --output ../my-project/ROADMAP.md
```

### 方式二：手动填写

1. 复制模板文件到项目目录
2. 搜索所有 `{{variable_name}}` 格式的变量
3. 替换为实际内容
4. 保存文件

## 变量说明

### ROADMAP.md 变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `{{*project_name}}` | 是 | - | 项目名称 |
| `{{*milestones}}` | 是 | - | 里程碑列表 |
| `{{timeline}}` | 否 | - | 时间线规划 |

### version-entry-template.md 变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `{{*version}}` | 是 | - | 版本号 |
| `{{*release_date}}` | 是 | - | 发布日期 (YYYY-MM-DD) |
| `{{*changes}}` | 是 | - | 变更内容列表 |

---

**最后更新**: 2026-03-06
