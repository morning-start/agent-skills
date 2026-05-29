---
name: project-wiki
version: 8.0.0
description: 面向开发人员的项目文档助手，提供模板化文档生成、标准化文档流程和实用知识库查询
tags: [project-wiki, documentation, templates, generator, knowledge-base]
---

# ProjectWiki - 面向开发人员的项目文档助手

## 任务目标

ProjectWiki 是面向开发人员、技术负责人和项目经理的文档助手，帮助快速创建和维护高质量项目文档。

**核心价值**:
- 🚀 **快速生成**: 3 分钟内生成 README、ARCHITECTURE 等标准文档
- 📋 **模板丰富**: 20+ 标准模板，覆盖基础文档、架构设计、需求文档、工作流程
- 🔧 **工具完善**: 交互式生成器 + 配置文件，提升效率
- 📚 **知识实用**: 技术框架、设计模式、最佳实践速查
- ✅ **质量保证**: 文档一致性检查 + 标准化工作流程，确保质量

---

## 快速上手（3 分钟）

### 步骤 1：准备配置文件

```bash
cat > config.yaml << EOF
project_name: "My Project"
username: "octocat"
version: "1.0.0"
description: "项目描述"
EOF
```

### 步骤 2：生成 README 文档

```bash
uv run python scripts/generate_doc.py \
  --template basic/README.md \
  --output README.md \
  --config config.yaml
```

### 步骤 3：生成架构文档

```bash
uv run python scripts/generate_doc.py \
  --template architecture/ARCHITECTURE.md \
  --output ARCHITECTURE.md \
  --config config.yaml
```

**完成!** 现在你有了两个标准文档。

---

## 核心能力

### 1. 模板 + 脚本生成 ⭐⭐⭐⭐⭐

**触发场景**: 新项目启动、需要快速生成标准文档

**输入**: 项目名称、作者等基本信息（可通过配置文件提供）

**输出**: 标准格式的 Markdown 文档

**支持模板**:
- **基础文档**: README.md, CHANGELOG.md, CONTRIBUTING.md, LICENSE.md
- **架构文档**: ARCHITECTURE.md, api-template.md, design-doc-template.md
- **需求文档**: functional-doc-template.md, requirement-doc-template.md, rtm-template.md
- **规划文档**: ROADMAP.md, version-entry-template.md

**示例**:
```bash
# 使用配置文件
uv run python scripts/generate_doc.py \
  --template architecture/ARCHITECTURE.md \
  --output ARCHITECTURE.md \
  --config config.yaml
```

### 2. 文档流程管理 ⭐⭐⭐⭐

**触发场景**: 文档生命周期管理、版本发布、需求变更

**核心功能**:
- **文档生成**: 从模板生成标准文档
- **一致性检查**: 版本发布前检查文档一致性
- **变更同步**: 需求变更后同步更新相关文档
- **健康检查**: 定期评估文档质量和完整性

**检查项**: 术语命名、内容逻辑、格式结构、数据参数、图表文字、角色权限、时间进度

**示例**:
```bash
# 版本发布前检查版本号一致性
grep "version:" SKILL.md
grep "## \[" CHANGELOG.md
cat templates/checklists/document-review-checklist.md
```

### 3. 知识库查询 ⭐⭐⭐

**触发场景**: 技术选型、架构设计、需要最佳实践参考

**知识库内容**:
- **技术框架**: frameworks.md - React, Vue, Angular, Spring Boot 等
- **设计模式**: patterns.md - 23 种设计模式速查
- **设计原则**: principles.md - SOLID, DRY, KISS 等原则
- **一致性规则**: consistency-rules.md - 文档一致性规范

**示例**:
```bash
# 查询 React 框架信息
cat references/knowledge/frameworks.md | grep -A 10 "React"
```

---

## 使用示例

### 场景 1: 新项目启动

```bash
cat > config.yaml << EOF
project_name: "Awesome Project"
username: "your-username"
version: "1.0.0"
description: "一个很棒的项目"
EOF

# 批量生成文档
uv run python scripts/generate_doc.py -t basic/README.md -o README.md -c config.yaml
uv run python scripts/generate_doc.py -t basic/CHANGELOG.md -o CHANGELOG.md -c config.yaml
uv run python scripts/generate_doc.py -t architecture/ARCHITECTURE.md -o ARCHITECTURE.md -c config.yaml
```

**检验结果**: ✅ 3 个标准文档已生成

### 场景 2: 生成 API 文档

```bash
uv run python scripts/generate_doc.py \
  --template architecture/api-template.md \
  --output wiki/api.md \
  --config config.yaml
```

**填写变量**: api_name (必填), endpoint (必填), method (必填)

**检验结果**: ✅ API 文档已生成

### 场景 3: 版本发布前检查

```bash
# 检查版本号
grep "version:" SKILL.md
grep "## \[" CHANGELOG.md
git tag -l

# 使用检查清单
cat templates/checklists/document-review-checklist.md
```

**检验结果**: ✅ 所有检查项通过

### 场景 4: 技术选型查询

```bash
# 查询框架和模式
cat references/knowledge/frameworks.md
cat references/knowledge/patterns.md
cat references/knowledge/principles.md
```

**检验结果**: ✅ 获取所需信息

### 场景 5: 批量生成脚本

```bash
#!/bin/bash
CONFIG="config.yaml"
GENERATOR="scripts/generate_doc.py"

uv run python $GENERATOR -t basic/README.md -o README.md -c $CONFIG
uv run python $GENERATOR -t basic/CHANGELOG.md -o CHANGELOG.md -c $CONFIG
uv run python $GENERATOR -t architecture/ARCHITECTURE.md -o ARCHITECTURE.md -c $CONFIG

echo "✅ 所有文档已生成"
```

### 场景 6: 使用标准化工作流程

```bash
# 1. 使用任务执行模板
cat templates/checklists/task-execution-template.md

# 2. 按照 WORKFLOW.md 执行任务
cat WORKFLOW.md

# 3. 执行质量检查
markdownlint *.md
markdown-link-check README.md

# 4. 组织评审
cat templates/checklists/document-review-checklist.md

# 5. 生成验收报告
cat templates/checklists/acceptance-report-template.md
```

**检验结果**: ✅ 任务执行规范、质量可控

---

## 工作流程

**3 步快速流程**:

```
1. 选择模板 → 2. 填写变量 → 3. 生成文档
```

**详细流程**:
1. **选择模板**: 根据项目类型和文档需求选择合适模板
2. **准备配置**: 创建配置文件或交互式填写变量
3. **生成文档**: 运行生成器，生成标准文档
4. **检查验证**: 运行一致性检查，确保文档质量

---

## 参考文档

### 高频使用

| 文档 | 用途 | 路径 |
|------|------|------|
| 快速开始 | 3 分钟上手 | [QUICKSTART.md](QUICKSTART.md) |
| 使用指南 | 详细说明 | [scripts/README.md](scripts/README.md) |
| 模板索引 | 查看所有模板 | [templates/](templates/) |

### 中频使用

| 文档 | 用途 | 路径 |
|------|------|------|
| 基础文档指南 | 编写 README 等 | [guides/basic-docs-checklist.md](references/guides/basic-docs-checklist.md) |
| 架构文档指南 | 编写 ARCHITECTURE | [guides/architecture-doc-guide.md](references/guides/architecture-doc-guide.md) |
| 文档管理指南 | 建立管理流程 | [guides/document-management-guide.md](references/guides/document-management-guide.md) |

### 知识库

| 文档 | 用途 | 路径 |
|------|------|------|
| 技术框架 | 框架速查 | [knowledge/frameworks.md](references/knowledge/frameworks.md) |
| 设计模式 | 模式速查 | [knowledge/patterns.md](references/knowledge/patterns.md) |
| 设计原则 | 原则速查 | [knowledge/principles.md](references/knowledge/principles.md) |
| 一致性规则 | 检查规范 | [knowledge/consistency-rules.md](references/knowledge/consistency-rules.md) |

---

## 常见问题（FAQ）

### Q1: 找不到模板？

**A**: 使用 `--list` 命令查看所有可用模板：

```bash
uv run python scripts/generate_doc.py --list
```

### Q2: 配置文件不生效？

**A**: 检查：
1. 配置文件格式是否正确（YAML/JSON）
2. 变量名是否与模板中的一致
3. 使用 `--config` 参数指定正确路径

### Q3: 变量未替换？

**A**: 确保变量格式正确：`{{variable_name}}`（注意双大括号）

### Q4: 如何批量生成文档？

**A**: 创建批量生成脚本（见场景 5），或使用配置文件依次生成。

### Q5: 如何更新已生成的文档？

**A**: 直接编辑生成的文件，或重新运行生成器（会提示覆盖）。

### Q6: 支持哪些配置文件格式？

**A**: 支持 YAML 和 JSON 格式，示例见 [config.example.yaml](scripts/config.example.yaml)。

---

## 注意事项

- **使用生成器**: 优先使用 `generate_doc.py` 快速生成
- **标准化优先**: 使用统一的变量格式 `{{variable_name}}`
- **渐进式完善**: 从核心文档开始，逐步完善
- **保持一致性**: 确保术语、版本、配置在各文档间一致
- **及时更新**: 代码变更时同步更新文档
- **定期验证**: 版本发布前进行一致性检查

---

## 命令速查

```bash
# 列出模板
uv run python scripts/generate_doc.py --list

# 生成单个文档
uv run python scripts/generate_doc.py -t basic/README.md -o README.md

# 使用配置文件
uv run python scripts/generate_doc.py -t basic/README.md -o README.md -c config.yaml

# 标准化模板变量
uv run python scripts/normalize_templates.py --templates-dir templates
```

## 模板速查

| 分类 | 模板 | 用途 |
|------|------|------|
| **基础** | basic/README.md | 项目说明 |
| **基础** | basic/CHANGELOG.md | 变更日志 |
| **架构** | architecture/ARCHITECTURE.md | 系统架构 |
| **架构** | architecture/api-template.md | API 文档 |
| **需求** | requirements/functional-doc-template.md | 功能需求 |
| **规划** | roadmap/ROADMAP.md | 项目路线图 |

## 变量格式

- `{{variable_name}}` - 普通变量
- `{{*variable_name}}` - 必填变量
- `{{?variable_name}}` - 可选变量

---

**最后更新**: 2026-03-13  
**版本**: v8.0.0  
**状态**: ✅ 可用
