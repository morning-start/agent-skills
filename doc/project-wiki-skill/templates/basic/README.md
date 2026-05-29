# 基础文档模板

本目录包含项目基础文档模板。

## 模板列表

| 模板 | 用途 | 变量说明 |
|------|------|----------|
| [README.md](./README.md) | 项目说明文档 | `{{project_name}}`, `{{username}}`, `{{version}}` 等 |
| [CHANGELOG.md](./CHANGELOG.md) | 变更日志 | `{{version}}`, `{{date}}`, `{{changes}}` 等 |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | 贡献指南 | `{{project_name}}`, `{{contact_email}}` 等 |
| [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) | 行为准则 | `{{project_name}}`, `{{contact_email}}` 等 |
| [LICENSE.md](./LICENSE.md) | 许可证 | `{{year}}`, `{{author}}`, `{{license_type}}` 等 |
| [changelog-template.md](./changelog-template.md) | 变更日志条目模板 | `{{version}}`, `{{date}}`, `{{changes}}` 等 |

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
python scripts/generate-doc.py --template basic/README.md --output ../my-project/README.md
```

### 方式二：手动填写

1. 复制模板文件到项目目录
2. 搜索所有 `{{variable_name}}` 格式的变量
3. 替换为实际内容
4. 保存文件

## 变量说明

### README.md 变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `{{*project_name}}` | 是 | - | 项目名称 |
| `{{*username}}` | 是 | - | GitHub 用户名/组织名 |
| `{{version}}` | 否 | 1.0.0 | 项目版本 |
| `{{description}}` | 否 | - | 项目描述 |

### CHANGELOG.md 变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `{{*version}}` | 是 | - | 版本号 |
| `{{*date}}` | 是 | - | 发布日期 (YYYY-MM-DD) |
| `{{*changes}}` | 是 | - | 变更内容列表 |

---

**最后更新**: 2026-03-06
