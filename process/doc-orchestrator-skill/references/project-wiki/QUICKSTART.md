# 快速开始 - 3 分钟生成项目文档

本指南演示如何在 3 分钟内使用模板生成器为新项目生成标准文档。

## 3 步快速开始

### 步骤 1：准备配置文件（1 分钟）

```bash
# 进入项目目录
cd my-project

# 创建配置文件
cat > config.yaml << EOF
project_name: "My Project"
username: "your-username"
version: "1.0.0"
description: "项目描述"
contact_email: "contact@example.com"
EOF
```

### 步骤 2：生成 README 文档（1 分钟）

```bash
uv run python scripts/generate_doc.py \
  --template basic/README.md \
  --output README.md \
  --config config.yaml
```

### 步骤 3：生成架构文档（1 分钟）

```bash
uv run python scripts/generate_doc.py \
  --template architecture/ARCHITECTURE.md \
  --output ARCHITECTURE.md \
  --config config.yaml
```

**完成!** 现在你有了两个标准文档。

---

## 命令速查

```bash
# 列出所有模板
uv run python scripts/generate_doc.py --list

# 生成单个文档
uv run python scripts/generate_doc.py -t basic/README.md -o README.md

# 使用配置文件
uv run python scripts/generate_doc.py -t basic/README.md -o README.md -c config.yaml

# 覆盖已存在文件
uv run python scripts/generate_doc.py -t basic/README.md -o README.md -c config.yaml --overwrite

# 标准化模板变量
uv run python scripts/normalize_templates.py --templates-dir templates
```

## 变量格式速查

| 格式 | 说明 | 示例 |
|------|------|------|
| `{{variable_name}}` | 普通变量 | `{{project_name}}` |
| `{{*variable_name}}` | 必填变量 | `{{*username}}` |
| `{{?variable_name}}` | 可选变量 | `{{?description}}` |

## 模板分类速查

| 分类 | 常用模板 | 用途 |
|------|----------|------|
| **基础** | basic/README.md | 项目说明文档 |
| **基础** | basic/CHANGELOG.md | 变更日志 |
| **架构** | architecture/ARCHITECTURE.md | 系统架构设计 |
| **架构** | architecture/api-template.md | API 接口文档 |
| **需求** | requirements/functional-doc-template.md | 功能需求文档 |
| **规划** | roadmap/ROADMAP.md | 项目路线图 |

## 配置文件示例

```yaml
# config.yaml
project_name: "My Project"
username: "your-username"
version: "1.0.0"
description: "项目描述"
contact_email: "contact@example.com"
author: "作者姓名"
```

## 故障排查速查

| 问题 | 检查项 | 解决方案 |
|------|--------|----------|
| 找不到模板 | 模板路径 | 使用 `--list` 查看所有模板 |
| 配置文件不生效 | 文件格式 | 检查 YAML/JSON 格式 |
| 变量未替换 | 变量名匹配 | 确保变量名完全一致 |
| 命令执行失败 | Python 环境 | 使用 `uv run python` |

---

## 下一步

生成基础文档后，你可以：

```bash
# 生成更多文档
uv run python scripts/generate_doc.py -t basic/CHANGELOG.md -o CHANGELOG.md -c config.yaml
uv run python scripts/generate_doc.py -t basic/CONTRIBUTING.md -o CONTRIBUTING.md -c config.yaml
uv run python scripts/generate_doc.py -t basic/LICENSE.md -o LICENSE.md -c config.yaml

# 生成架构相关文档
uv run python scripts/generate_doc.py -t architecture/api-template.md -o wiki/api.md -c config.yaml

# 生成规划文档
uv run python scripts/generate_doc.py -t roadmap/ROADMAP.md -o ROADMAP.md -c config.yaml
```

## 高级技巧

### 技巧 1：批量生成脚本

创建 `generate-docs.sh`:

```bash
#!/bin/bash
CONFIG="config.yaml"
GENERATOR="scripts/generate_doc.py"

echo "📦 生成项目文档..."

uv run python $GENERATOR -t basic/README.md -o README.md -c $CONFIG
uv run python $GENERATOR -t basic/CHANGELOG.md -o CHANGELOG.md -c $CONFIG
uv run python $GENERATOR -t architecture/ARCHITECTURE.md -o ARCHITECTURE.md -c $CONFIG

echo "✅ 文档生成完成！"
```

使用：

```bash
chmod +x generate-docs.sh
./generate-docs.sh
```

### 技巧 2：复用配置

将配置文件放在工作区根目录，所有项目共享：

```bash
# 工作区配置
~/workspace/doc-config.yaml

# 在各项目中引用
uv run python scripts/generate_doc.py \
  --template basic/README.md \
  --output README.md \
  --config ~/workspace/doc-config.yaml
```

### 技巧 3：不使用配置文件

直接交互式填写：

```bash
uv run python scripts/generate_doc.py \
  --template basic/README.md \
  --output README.md
```

脚本会逐个提示你填写变量。

## 常见问题

### Q: 找不到模板？

**A**: 确保路径正确，使用 `--list` 查看所有可用模板。

### Q: 配置文件不生效？

**A**: 检查 YAML 格式，确保变量名与模板中的一致。

### Q: 想修改生成的文档？

**A**: 直接编辑生成的文件即可，配置文件可以重复使用。

## 参考文档

- [完整使用指南](scripts/README.md)
- [模板生成器总览](TEMPLATE_GENERATOR.md)
- [配置文件示例](scripts/config.example.yaml)

---

**提示**: 更多使用场景请参考 [SKILL.md](SKILL.md)。
