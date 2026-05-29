# 文档生成器使用指南

快速使用模板 + 脚本生成标准文档。

## 安装依赖

```bash
# 进入 project-wiki 目录
cd project-wiki

# 安装依赖 (可选，如需 YAML 支持)
uv add pyyaml
```

## 快速开始

### 1. 列出所有可用模板

```bash
uv run python scripts/generate_doc.py --list
```

输出示例:
```
可用模板列表:

architecture/
  - ARCHITECTURE.md
  - api-template.md
  - architecture-doc-template.md
  - design-doc-template.md

basic/
  - CHANGELOG.md
  - CODE_OF_CONDUCT.md
  - CONTRIBUTING.md
  - LICENSE.md
  - README.md
  - changelog-template.md

...
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

脚本会交互式引导你填写变量。

### 3. 使用配置文件（推荐）

创建配置文件 `config.yaml`:

```yaml
project_name: "我的项目"
username: "your-username"
description: "项目描述"
version: "1.0.0"
contact_email: "contact@example.com"
author: "作者姓名"
```

使用配置文件生成:

```bash
uv run python scripts/generate_doc.py \
  --template basic/README.md \
  --output ../my-project/README.md \
  --config config.yaml
```

配置文件中的值会自动填充，只需填写差异化的内容。

### 4. 批量生成（开发中）

```bash
# 一键生成项目文档集
uv run python scripts/generate_doc.py \
  --project my-project \
  --output-dir ../my-project/docs
```

## 模板变量说明

### 变量格式

- `{{variable_name}}` - 普通变量
- `{{*variable_name}}` - 必填变量（星号标记）
- `{{?variable_name}}` - 可选变量（问号标记）

### 常见变量

#### 基础文档变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `{{*project_name}}` | 项目名称 | My Project |
| `{{*username}}` | GitHub 用户名 | octocat |
| `{{version}}` | 版本号 | 1.0.0 |
| `{{description}}` | 项目描述 | 一个很棒的项目 |
| `{{contact_email}}` | 联系邮箱 | contact@example.com |

#### 架构文档变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `{{*tech_stack}}` | 技术栈 | React, TypeScript |
| `{{architecture_diagram}}` | 架构图 | Mermaid 图表代码 |

#### API 文档变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `{{*api_name}}` | API 名称 | User API |
| `{{*endpoint}}` | 端点路径 | /api/users |
| `{{*method}}` | HTTP 方法 | POST |

## 配置文件格式

支持 YAML 和 JSON 两种格式。

### YAML 示例 (config.yaml)

```yaml
project_name: "我的项目"
username: "octocat"
version: "1.0.0"
features:
  - "功能 1"
  - "功能 2"
```

### JSON 示例 (config.json)

```json
{
  "project_name": "我的项目",
  "username": "octocat",
  "version": "1.0.0",
  "features": ["功能 1", "功能 2"]
}
```

## 命令行参数

```
usage: generate_doc.py [-h] [--list] [--template TEMPLATE] [--output OUTPUT]
                       [--config CONFIG] [--project PROJECT]
                       [--output-dir OUTPUT_DIR] [--overwrite]
                       [--templates-dir TEMPLATES_DIR]

选项:
  -h, --help            显示帮助信息
  --list, -l            列出所有可用模板
  --template, -t        模板路径 (如：basic/README.md)
  --output, -o          输出文件路径
  --config, -c          配置文件路径 (YAML/JSON)
  --project, -p         项目名称 (批量生成模式)
  --output-dir, -d      输出目录 (默认当前目录)
  --overwrite           覆盖已存在的文件
  --templates-dir       模板目录路径 (默认：project-wiki/templates)
```

## 最佳实践

### 1. 为团队创建标准配置

在团队仓库中维护标准配置文件：

```bash
# 团队标准配置
templates/config-team.yaml
```

新成员只需复制配置并修改少量参数。

### 2. 使用环境变量

敏感信息使用环境变量：

```bash
# .env 文件
GITHUB_USERNAME=octocat
CONTACT_EMAIL=contact@example.com
```

在配置文件中引用：

```yaml
username: ${GITHUB_USERNAME}
contact_email: ${CONTACT_EMAIL}
```

### 3. 版本化管理配置

不同版本使用不同配置：

```bash
config-v1.0.yaml
config-v2.0.yaml
```

### 4. 组合使用多个配置

```bash
# 基础配置 + 项目特定配置
uv run python scripts/generate_doc.py \
  --template basic/README.md \
  --output README.md \
  --config config-base.yaml
```

## 示例工作流

### 新项目初始化

```bash
# 1. 创建项目目录
mkdir my-new-project
cd my-new-project

# 2. 创建配置文件
cat > config.yaml << EOF
project_name: "My New Project"
username: "octocat"
version: "1.0.0"
EOF

# 3. 生成基础文档
uv run python ../project-wiki/scripts/generate_doc.py \
  --template basic/README.md \
  --output README.md \
  --config config.yaml

uv run python ../project-wiki/scripts/generate_doc.py \
  --template basic/CONTRIBUTING.md \
  --output CONTRIBUTING.md \
  --config config.yaml

uv run python ../project-wiki/scripts/generate_doc.py \
  --template basic/LICENSE.md \
  --output LICENSE.md \
  --config config.yaml

# 4. 生成架构文档
uv run python ../project-wiki/scripts/generate_doc.py \
  --template architecture/ARCHITECTURE.md \
  --output ARCHITECTURE.md \
  --config config.yaml
```

### 版本发布

```bash
# 1. 更新配置中的版本号
# 编辑 config.yaml，修改 version: "2.0.0"

# 2. 生成变更日志条目
uv run python ../project-wiki/scripts/generate_doc.py \
  --template basic/changelog-template.md \
  --output CHANGELOG-v2.0.md \
  --config config.yaml
```

## 故障排除

### 问题 1: 找不到模板

**解决**: 使用 `--list` 查看可用模板，确保路径正确。

### 问题 2: 变量未替换

**解决**: 检查变量名是否匹配，必填变量必须填写。

### 问题 3: 配置文件加载失败

**解决**: 检查 YAML/JSON 格式是否正确，确保安装了 `pyyaml`。

## 高级用法

### 自定义模板

将自定义模板放在 `templates/custom/` 目录：

```bash
mkdir -p templates/custom
cp my-template.md templates/custom/
```

使用自定义模板:

```bash
uv run python scripts/generate_doc.py \
  --template custom/my-template.md \
  --output output.md
```

### 批量处理脚本

创建批量生成脚本 `generate-all.sh`:

```bash
#!/bin/bash

CONFIG="config.yaml"
OUTPUT_DIR="../my-project"
TEMPLATES_DIR="project-wiki/templates"

# 生成基础文档
python scripts/generate_doc.py \
  --template basic/README.md \
  --output $OUTPUT_DIR/README.md \
  --config $CONFIG \
  --templates-dir $TEMPLATES_DIR

python scripts/generate_doc.py \
  --template basic/CHANGELOG.md \
  --output $OUTPUT_DIR/CHANGELOG.md \
  --config $CONFIG \
  --templates-dir $TEMPLATES_DIR

echo "✓ 所有文档已生成"
```

## 贡献模板

欢迎贡献新的模板！请遵循以下规范：

1. 将模板放在合适的分类目录下
2. 使用统一的变量格式 `{{variable_name}}`
3. 在目录 README 中添加变量说明
4. 提供示例配置文件

---

**最后更新**: 2026-03-06
