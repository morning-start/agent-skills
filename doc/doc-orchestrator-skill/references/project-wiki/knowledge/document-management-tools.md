# 文档管理工具链

## 概述

本文档汇总了文档管理各环节的推荐工具，帮助团队选择合适的工具建立文档管理流程。

---

## 工具分类

### 1. 文档编写工具

| 工具 | 类型 | 特点 | 适用场景 |
|------|------|------|---------|
| **VS Code** | 编辑器 | 免费、插件丰富、Git 集成 | 技术文档、代码注释 |
| **Typora** | 编辑器 | 实时预览、简洁 | 快速编写 Markdown |
| **Obsidian** | 笔记 | 双向链接、知识图谱 | 个人知识库、笔记 |
| **Notion** | 笔记 | 数据库、协作 | 团队知识库 |

**推荐**：技术文档首选 VS Code，个人笔记推荐 Obsidian。

---

### 2. 协作与知识库平台

| 工具 | 部署方式 | 特点 | 适用场景 |
|------|---------|------|---------|
| **Confluence** | 云端/本地 | 功能强大、企业级 | 大型企业、正式文档 |
| **Notion** | 云端 | 灵活、数据库 | 中小团队、知识库 |
| **Wiki.js** | 自托管 | 开源、Git 集成 | 技术团队、开源项目 |
| **DokuWiki** | 自托管 | 轻量、无需数据库 | 小型团队、简单文档 |
| **GitBook** | 云端 | 美观、版本管理 | 产品文档、API 文档 |

**推荐**：企业团队用 Confluence，技术团队用 Wiki.js，产品文档用 GitBook。

---

### 3. API 文档工具

| 工具 | 输入格式 | 特点 | 适用场景 |
|------|---------|------|---------|
| **Swagger UI** | OpenAPI YAML/JSON | 交互式、自动生成 | REST API 文档 |
| **Redoc** | OpenAPI YAML/JSON | 美观、响应式 | 对外 API 文档 |
| **Postman** | Collection JSON | 可测试、分享 | API 调试、团队共享 |
| **Stoplight** | OpenAPI | 可视化编辑、协作 | API 设计、文档 |

**推荐**：REST API 用 Swagger UI，对外文档用 Redoc，调试用 Postman。

---

### 4. 静态文档站点生成器

| 工具 | 技术栈 | 特点 | 适用场景 |
|------|-------|------|---------|
| **MkDocs** | Python | 简单、快速 | Python 项目文档 |
| **Docusaurus** | React | 功能强大、多版本 | 开源项目、产品文档 |
| **VitePress** | Vue | 快速、简洁 | Vue 生态项目 |
| **Docsify** | Vue | 轻量、无需构建 | 简单文档站点 |
| **VuePress** | Vue | 成熟、插件多 | 技术文档 |

**推荐**：React 项目用 Docusaurus，Vue 项目用 VitePress，简单文档用 Docsify。

---

### 5. 图表绘制工具

| 工具 | 类型 | 特点 | 适用场景 |
|------|------|------|---------|
| **Mermaid** | 代码化 | 可版本控制、集成 Markdown | 流程图、时序图、架构图 |
| **Draw.io** | 图形化 | 免费、功能全、Confluence 集成 | 复杂图表、ER 图 |
| **Excalidraw** | 手绘风 | 简洁、协作 | 草图、示意图 |
| **Lucidchart** | 专业 | 功能强大、协作 | 企业级图表 |
| **PlantUML** | 代码化 | UML 专用 | 软件设计图 |

**推荐**：技术文档用 Mermaid，复杂图表用 Draw.io，草图用 Excalidraw。

---

### 6. 版本与权限管理

| 工具 | 特点 | 适用场景 |
|------|------|---------|
| **Git + GitHub** | 版本控制、PR 评审、Pages 部署 | 开源项目、技术团队 |
| **Git + GitLab** | 版本控制、CI/CD、内置 Wiki | 企业团队、私有项目 |
| **GitHub Pages** | 免费部署、自定义域名 | 文档站点部署 |
| **Netlify** | 自动部署、预览 | 文档站点部署 |
| **Vercel** | 快速部署、自动 HTTPS | 文档站点部署 |

**推荐**：技术团队用 Git+GitHub/GitLab，文档站点用 GitHub Pages 或 Netlify。

---

### 7. 自动化检查工具

| 工具 | 功能 | 适用场景 |
|------|------|---------|
| **Vale** | 语言风格检查、术语一致性 | 英文文档、风格统一 |
| **markdown-link-check** | 链接有效性检查 | 所有 Markdown 文档 |
| **markdownlint** | Markdown 格式检查 | 所有 Markdown 文档 |
| **Prettier** | 代码格式化 | Markdown 格式化 |
| **custom CI scripts** | 自定义检查脚本 | 特定需求检查 |

**推荐**：必备 markdownlint 和 markdown-link-check，英文文档加用 Vale。

---

## 工具选择建议

### 小团队（<10 人）

**推荐组合**：
- 文档编写：VS Code + Markdown
- 知识库：Notion 或 Wiki.js
- API 文档：Swagger UI
- 文档站点：VitePress + GitHub Pages
- 图表：Mermaid + Excalidraw
- 版本管理：Git + GitHub
- 自动化检查：markdownlint + markdown-link-check

### 中团队（10-50 人）

**推荐组合**：
- 文档编写：VS Code + Typora
- 知识库：Confluence 或 GitBook
- API 文档：Swagger UI + Redoc
- 文档站点：Docusaurus + Netlify
- 图表：Mermaid + Draw.io
- 版本管理：Git + GitLab
- 自动化检查：Vale + CI 集成

### 大团队（>50 人）

**推荐组合**：
- 文档编写：VS Code + 企业版编辑器
- 知识库：Confluence（企业版）
- API 文档：Stoplight + Swagger UI
- 文档站点：Docusaurus（多版本）
- 图表：Draw.io（企业版）+ Mermaid
- 版本管理：Git + 企业 GitLab
- 自动化检查：完整 CI/CD 集成

---

## 工具集成示例

### CI 自动部署文档

```yaml
# .github/workflows/docs-deploy.yml
name: Deploy Documentation

on:
  push:
    branches: [main]
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build docs
        run: npm run docs:build
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./wiki/dist
```

### 自动化检查

```yaml
# .github/workflows/doc-check.yml
name: Document Check

on:
  pull_request:
    paths:
      - '**/*.md'

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Check links
        run: |
          npm install -g markdown-link-check
          find . -name "*.md" -exec markdown-link-check {} \;
      
      - name: Check format
        run: |
          npm install -g markdownlint-cli
          markdownlint **/*.md
```

---

## 参考资料

- [文档管理流程指南](document-management-guide.md)
- [健康度检查指南](document-health-check-guide.md)
