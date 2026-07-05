# 轻量级文档管理流程

## 概述

本文档提供适用于中小团队的轻量级文档管理流程，快速落地，无需复杂流程。

**适用团队**：10 人以下，敏捷开发，快速迭代

---

## 核心原则

1. **最小可行文档**：只写必要的文档
2. **文档即代码**：与代码一起提交、评审、部署
3. **自动化优先**：能自动检查的绝不手动
4. **渐进式完善**：从最小集开始，逐步完善

---

## 流程步骤

### 1. 项目初始化

**目标**：5 分钟内完成文档框架搭建。

**步骤**：
```bash
# 1. 创建 wiki/ 目录
mkdir wiki

# 2. 创建基础文档
cd docs
touch README.md
touch TEMPLATE.md

# 3. 创建文档清单
cat > DOCS_LIST.md << EOF
# 项目文档清单

## 必备文档
- [ ] README.md - 项目说明
- [ ] ARCHITECTURE.md - 架构设计
- [ ] API.md - API 文档

## 选作文档
- [ ] USER_GUIDE.md - 用户指南
- [ ] DEPLOYMENT.md - 部署手册
EOF
```

**输出**：
- wiki/ 目录
- README.md（项目文档入口）
- TEMPLATE.md（文档模板）
- DOCS_LIST.md（文档清单）

---

### 2. Feature PR 流程

**目标**：每个功能 PR 都包含文档更新。

**流程**：
```markdown
# PR 模板

## 变更描述
- 功能说明
- 技术实现

## 文档更新
- [ ] README.md 已更新
- [ ] API 文档已更新
- [ ] 架构文档已更新
- [ ] 无需文档更新（请说明原因）

## 自查
- [ ] 文档中的代码示例已验证
- [ ] 链接有效
- [ ] 术语一致
```

**CI 检查**：
```yaml
# .github/workflows/doc-check.yml
name: PR Document Check

on:
  pull_request:
    paths:
      - '**/*.md'

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Check if docs updated
        run: |
          # 检查代码变更是否包含文档更新
          # 如果变更代码但无文档更新，发出警告
```

---

### 3. 主干合并前检查

**目标**：自动检查文档质量。

**CI 检查项**：
```yaml
# .github/workflows/doc-validation.yml
name: Document Validation

on:
  pull_request:
    branches: [main]
    paths:
      - 'wiki/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Check links
        run: |
          npm install -g markdown-link-check
          find docs -name "*.md" -exec markdown-link-check {} \;
      
      - name: Check format
        run: |
          npm install -g markdownlint-cli
          markdownlint wiki/
      
      - name: Check placeholders
        run: |
          if grep -r "{{" wiki/ || grep -r "\[TODO\]" wiki/; then
            echo "Found unreplaced placeholders"
            exit 1
          fi
```

---

### 4. 版本发布流程

**目标**：自动部署文档站点。

**流程**：
```yaml
# .github/workflows/docs-deploy.yml
name: Deploy Documentation

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build docs
        run: |
          npm ci
          npm run docs:build
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./wiki/dist
          tag_name: docs-v${{ github.ref_name }}
```

**输出**：
- 自动部署文档站点
- 创建版本文档标签（docs-v1.0.0）
- 在 Release 中附上文档链接

---

### 5. 月度健康度 Review

**目标**：10 分钟快速 review 文档健康度。

**流程**：
```markdown
# 月度站会议程（10 分钟）

## 文档健康度（5 分钟）
- 运行健康度检查脚本
- 查看检查结果
- 分配修复任务

## 文档更新（3 分钟）
- 本月新增文档
- 本月更新文档
- 需要更新的文档

## 改进建议（2 分钟）
- 收集团队反馈
- 讨论改进建议
```

**健康度检查脚本**：
```bash
#!/bin/bash
# wiki/health-check.sh

echo "=== 文档健康度检查 ==="
echo ""

# 统计
total=$(find . -name "*.md" | wc -l)
fresh=$(find . -name "*.md" -mtime -30 | wc -l)
stale=$(find . -name "*.md" -mtime +90 | wc -l)

echo "总文档数：$total"
echo "新鲜文档（<30 天）：$fresh"
echo "可能过期（>90 天）：$stale"
echo ""

# 检查链接
echo "检查链接..."
find . -name "*.md" -exec markdown-link-check {} \; 2>&1 | grep -v "^$"

# 检查格式
echo "检查格式..."
markdownlint **/*.md 2>&1 | head -20
```

---

## 工具推荐（最小集）

**必备工具**：
- VS Code + Markdown 插件
- Git + GitHub
- markdownlint（格式检查）
- markdown-link-check（链接检查）

**可选工具**：
- VitePress（文档站点）
- Mermaid（图表）
- Swagger UI（API 文档）

---

## 文档模板

### 最小文档模板

```markdown
# {{文档标题}}

## 概述
{{简要描述文档目的}}

## 内容
{{主要内容}}

## 示例
{{代码示例或使用示例}}

## 参考资料
- {{相关链接}}

---
**维护责任人**：{{姓名}}
**最后更新**：{{日期}}
**版本**：{{版本号}}
```

---

## 成功指标

**文档健康度指标**：
- 新鲜文档比例 > 80%
- 链接有效率 = 100%
- 格式规范率 > 95%
- 月度更新率 > 50%

**团队满意度指标**：
- 新人上手时间缩短
- 文档查询时间 < 5 分钟
- 团队文档满意度 > 4/5

---

## 渐进式完善

**第一阶段（1-2 周）**：
- 创建 wiki/ 目录
- 编写 README.md
- 建立 PR 文档检查

**第二阶段（2-4 周）**：
- 编写核心文档（架构、API）
- 部署文档站点
- 实施健康度检查

**第三阶段（4-8 周）**：
- 完善文档模板
- 自动化文档检查
- 建立文档评审机制

**持续改进**：
- 收集团队反馈
- 优化文档流程
- 提升文档质量

---

## 参考资料

- [文档管理流程指南](document-management-guide.md)
- [评审 checklist 模板](../templates/document-review-checklist.md)
- [健康度检查指南](document-health-check-guide.md)
