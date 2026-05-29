# 模板文档生成器

基于模板 + 脚本快速生成标准文档的工具集。

## 功能特性

- ✅ **模板分类管理**：按文档类型分层组织（basic/architecture/requirements/knowledge/roadmap/checklists）
- ✅ **统一变量命名**：所有模板使用统一的 `{{variable_name}}` 格式
- ✅ **交互式生成**：命令行交互式引导填写变量
- ✅ **配置文件支持**：支持 YAML/JSON 配置文件预定义变量
- ✅ **变量标准化**：自动识别并替换不同格式的变量（76 个变量已统一）

## 快速开始

### 1. 列出所有可用模板

```bash
cd project-wiki
uv run python scripts/generate_doc.py --list
```

### 2. 生成单个文档

```bash
# 生成 README.md
uv run python scripts/generate_doc.py \
  --template basic/README.md \
  --output ../my-project/README.md

# 生成架构文档
uv run python scripts/generate_doc.py \
  --template architecture/ARCHITECTURE.md \
  --output ../my-project/ARCHITECTURE.md
```

### 3. 使用配置文件

```bash
# 复制示例配置
cp scripts/config.example.yaml scripts/config.yaml

# 编辑配置文件
# vim scripts/config.yaml

# 使用配置生成文档
uv run python scripts/generate_doc.py \
  --template basic/README.md \
  --output ../my-project/README.md \
  --config scripts/config.yaml
```

## 目录结构

```
templates/
├── basic/              # 基础文档模板
│   ├── README.md       # 项目说明
│   ├── CHANGELOG.md    # 变更日志
│   ├── CONTRIBUTING.md # 贡献指南
│   ├── CODE_OF_CONDUCT.md  # 行为准则
│   ├── LICENSE.md      # 许可证
│   └── changelog-template.md
├── architecture/       # 架构设计模板
│   ├── ARCHITECTURE.md
│   ├── design-doc-template.md
│   ├── api-template.md
│   └── architecture-doc-template.md
├── requirements/       # 需求文档模板
│   ├── functional-doc-template.md
│   ├── requirement-doc-template.md
│   └── rtm-template.md
├── knowledge/          # 知识库模板
│   ├── knowledge-template.md
│   └── consistency-checklist-template.md
├── roadmap/            # 规划文档模板
│   ├── ROADMAP.md
│   └── version-entry-template.md
└── checklists/         # 检查清单模板
    ├── document-review-checklist.md
    └── lightweight-doc-management-process.md

scripts/
├── generate_doc.py          # 文档生成器主脚本
├── normalize_templates.py   # 模板变量标准化工具
├── config.example.yaml      # 配置文件示例
└── README.md                # 使用指南
```

## 模板变量规范

### 变量格式

- `{{variable_name}}` - 普通变量
- `{{*variable_name}}` - 必填变量（星号标记）
- `{{?variable_name}}` - 可选变量（问号标记）

### 常见变量

| 变量名 | 必填 | 说明 | 示例 |
|--------|------|------|------|
| `{{*project_name}}` | 是 | 项目名称 | My Project |
| `{{*username}}` | 是 | GitHub 用户名 | octocat |
| `{{version}}` | 否 | 版本号 | 1.0.0 |
| `{{description}}` | 否 | 项目描述 | 一个很棒的项目 |
| `{{contact_email}}` | 否 | 联系邮箱 | contact@example.com |

## 使用示例

### 示例 1：新项目初始化

```bash
# 1. 创建项目
mkdir my-project && cd my-project

# 2. 创建配置文件
cat > config.yaml << EOF
project_name: "My Project"
username: "octocat"
version: "1.0.0"
description: "项目描述"
EOF

# 3. 生成文档
uv run python ../project-wiki/scripts/generate_doc.py \
  --template basic/README.md \
  --output README.md \
  --config config.yaml

uv run python ../project-wiki/scripts/generate_doc.py \
  --template basic/CONTRIBUTING.md \
  --output CONTRIBUTING.md \
  --config config.yaml
```

### 示例 2：标准化现有模板

```bash
# 检查并标准化模板变量
uv run python scripts/normalize_templates.py \
  --templates-dir templates \
  --output-report variable_report.md
```

## 工具说明

### generate_doc.py - 文档生成器

主要功能：
- 列出所有可用模板
- 交互式填写变量
- 支持配置文件
- 自动生成文档

命令行参数：
```
-l, --list              列出所有模板
-t, --template          模板路径
-o, --output            输出文件路径
-c, --config            配置文件路径
--overwrite             覆盖已存在文件
```

### normalize_templates.py - 变量标准化工具

主要功能：
- 扫描所有模板文件
- 识别不同格式的变量
- 统一替换为标准格式
- 生成变量映射报告

命令行参数：
```
--templates-dir         模板目录
--dry-run              仅预览不修改
--output-report        输出报告文件
```

## 配置文件示例

```yaml
# config.yaml
project_name: "我的项目"
username: "your-username"
description: "项目描述"
version: "1.0.0"
contact_email: "contact@example.com"
author: "作者姓名"
license_type: "MIT"
year: "2024"
```

## 成果统计

- ✅ **模板目录重构**：6 个分类目录，18 个模板文件
- ✅ **变量统一**：76 个变量已标准化
- ✅ **索引文档**：每个目录都有 README 索引和变量说明
- ✅ **生成工具**：交互式 CLI 工具，支持配置化
- ✅ **使用文档**：完整的使用指南和示例

## 下一步计划

- [ ] 实现批量生成模式（一键生成项目文档集）
- [ ] 为每个模板添加更详细的变量说明注释块
- [ ] 支持环境变量引用
- [ ] 添加更多模板示例
- [ ] 支持自定义模板扩展

## 技术栈

- **Python 3.11+**: 脚本语言
- **uv**: 依赖管理
- **PyYAML**: YAML 配置文件支持（可选）

## 相关文档

- [脚本使用指南](scripts/README.md)
- [模板目录索引](templates/)
- [变量统一报告](variable_report.md)

---

**最后更新**: 2026-03-06
