---
name: tutorial-writer-publish
version: v7.0.0
author: skill-factory
description: >
  Use when deploying tutorial websites to GitHub Pages, configuring CI/CD workflows,
  setting up GitHub Actions, managing deployment configurations, or troubleshooting
  static site deployment issues for Astro + Starlight sites built with Content-First v2 architecture.
  Triggers on "部署到 GitHub", "GitHub Pages", "Actions 工作流", "CI-CD", "网站发布",
  "自动部署", "PDF 生成", "多形态发布".
  Covers GitHub Actions integration, base path configuration, custom domains,
  SSL/TLS, production monitoring, and multi-format publishing (PDF/EPUB) for Astro + Starlight sites.
  This is a low-frequency skill typically called after build phase completion (build v2.0.0+ required).
tags: [tutorial, publishing, astro, starlight, github-pages, web, deployment, ci-cd, content-first, multi-format]
dependency:
  parent: tutorial-writer
  structure: "Type 1 (重+厚): 单文件 + references"
  pattern: "Self-contained"
meta:
  complexity: intermediate
  standalone: true
  can_invoke_directly: true
  astro_version: "6.3"
  call_frequency: "low"  # 低频调用：预计每项目 2-3 次
  architecture_version: "content-first-v2"  # 内容优先架构 v2（与 build v2.0.0 对齐）
---

# Tutorial Writer — 🚀 网页发布（GitHub Pages + 多形态）v7.0

> **父技能**: [tutorial-writer](../SKILL.md)
> **独立可用**: ✅ 可通过 `/publish` 直接触发（L1 直达）
> **架构**: 自含型单文件技能 — 包含完整的 GitHub Pages 发布指南 + 多形态发布支持
> **使用频率**: 🟢 **低频** — 通常在构建完成后调用（每项目 2-3 次）
> **架构版本**: **Content-First v2**（要求 build v2.0.0+）

---

## 🎯 职责范围

| ✅ 负责 | ❌ 不负责 |
|---------|----------|
| GitHub Pages 专用配置和部署 | Astro 项目构建 → `/build` |
| GitHub Actions 工作流设置 | Starlight 主题配置 → `/build` |
| base 路径 / trailingSlash 配置 | Content Collections → `/build` |
| 自定义域名 / DNS / SSL | 组件开发 → `/build` |
| CI/CD 流水线和自动化 | 性能优化（构建时）→ `/build` |
| 部署监控、回滚、通知 | 本地开发环境 → `/build` |

**设计理念**: 本技能是 Tutorial Writer 流程中的**低频操作**，但内容完整详尽。Agent 在需要部署时一次性获取所有所需信息。

---

## 前置条件

在开始配置前，确认以下构建阶段交付物已就绪：

### ✅ 架构一致性检查（Content-First v2）

- [ ] 项目采用**内容优先架构**（`content/` 在根目录，非 `src/content/`）
- [ ] `content/chapters/` 目录存在且包含 Markdown 文件
- [ ] 文件命名符合规范：英文 slug（如 `01-rag-overview.md`）+ 中文标题（Frontmatter）
- [ ] `content/config.ts` 已配置 Content Collections schema

### ✅ 构建产物验证

- [ ] 已完成 `/build` 阶段（Astro 项目构建完成，使用 content-first 架构 v2.0.0）
- [ ] `npm run build` 成功，无错误输出
- [ ] `dist/` 目录结构正确（包含 `_astro/`、HTML 文件）
- [ ] 本地 `npm run preview` 页面显示正常
- [ ] 浏览器控制台无 404 错误（CSS/JS/图片）
- [ ] 响应式布局验证通过（375px / 768px / 1280px）

⚠️ **架构版本要求**: 本技能基于 **content-first-v2** 架构设计，与 `build v2.0.0` 完全对齐。如果项目仍使用旧版 `src/content/docs/` 结构，请先执行 `/build` 进行架构升级。

⚠️ 如果上述条件未满足，请先执行 `/build` 完成网站构建。

---

## 🚀 快速发布：4 步部署到 GitHub Pages

### Step 1: 关键部署配置

**astro.config.mjs**（必须正确设置的 3 个关键项 — **Content-First v2 架构版**）：

```javascript
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  // ⭐ 关键 1：完整站点 URL（影响 SEO、sitemap、OG 图片路径）
  site: 'https://username.github.io',

  // ⭐ 关键 2：项目路径前缀（GitHub Pages 项目站点必填！）
  // 用户站点（username.github.io）可不填或设为 '/'
  base: '/repo-name/',

  // ⭐ 关键 3：避免 GitHub Pages 404 问题
  trailingSlash: 'always',    // 输出 /about/index.html 而非 /about.html

  integrations: [
    starlight({
      title: '教程标题',
      description: '教程描述',

      social: {
        github: 'https://github.com/username/repo',
      },

      sidebar: [
        { label: '首页', slug: 'index' },
        {
          label: '章节',
          autogenerate: { directory: 'chapters' },  // ⭐ 指向 content/chapters/（Content-First 架构）
        },
      ],

      editLink: {
        baseUrl: 'https://github.com/username/repo/edit/main/',
      },
      lastUpdated: true,
      pagination: true,
      search: { mode: 'auto' },
    }),
  ],
});
```

**关键配置项说明**（Content-First v2 架构）：

| 配置项 | 值 | 说明 |
|--------|-----|------|
| `site` | 完整 URL | 影响 SEO、sitemap、OG 图片路径 |
| `base` | `'/repo-name/'` | GitHub Pages 项目站点必填 |
| `trailingSlash` | `'always'` | 避免 GitHub Pages 404 |
| `autogenerate.directory` | `'chapters'` | **指向 `content/chapters/` 目录**（非 `src/content/docs/`） |

**两种场景的配置差异**：

| 场景 | `site` 值 | `base` 值 | 最终 URL 示例 |
|------|----------|----------|--------------|
| **用户/组织站点** | `https://username.github.io` | 不填或 `'/'` | `https://username.github.io/` |
| **项目站点**（推荐） | `https://username.github.io` | `'/repo-name'` | `https://username.github.io/repo/` |

⚠️ **常见错误**：忘记设置 `base` 导致所有静态资源（CSS/JS/图片）404！

### Step 2: 创建 GitHub Actions 工作流

**文件位置**: `.github/workflows/deploy.yml`

#### 方案 A：官方 withastro/action（推荐，最简）

```yaml
name: Deploy to GitHub Pages

on:
  # 推送到 main 分支时自动触发
  push:
    branches: ['main']
  # 支持手动触发（可选）
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deploy.outputs.page_url }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Build site
        run: npm run build

      - name: Deploy to GitHub Pages
        id: deploy
        uses: withastro/action@v3
        # withastro/action 自动处理：
        # ✅ 构建产物上传
        # ✅ GitHub Pages 部署
        # ✅ 部署 URL 输出
```

#### 方案 B：标准 Actions 工作流（更可控）

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: ['main']
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  # Job 1: 构建
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build
        env:
          NODE_OPTIONS: --max-old-space-size=4096  # 大型项目防 OOM

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist

  # Job 2: 部署（依赖构建完成）
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**方案对比**：

| 维度 | 方案 A (withastro/action) | 方案 B (标准工作流) |
|------|--------------------------|-------------------|
| 配置复杂度 | ⭐ 简单（~30 行） | ⭐⭐ 中等（~60 行） |
| 可控性 | 中等 | 高（可自定义每一步） |
| 适用场景 | 标准教程站点 | 需要额外构建步骤的大型项目 |
| 官方推荐 | ✅ 是 | ✅ 也是标准做法 |

### Step 3: 配置 GitHub 仓库 Settings

1. 进入目标仓库 → **Settings**（设置）
2. 左侧菜单找到 **Pages**（页面）
3. **Source**（源）选择 **GitHub Actions**
   - ⚠️ 不要选择 "Deploy from a branch"（旧方式，不推荐）
4. 等待首次 Actions 运行完成（约 2-5 分钟）
5. 访问显示的 URL 验证部署成功：
   ```
   https://username.github.io/repo-name/
   ```

### Step 4: 部署后验证

**必查项目**：

- [ ] 首页可正常打开，样式加载正确
- [ ] 所有导航链接可点击，无 404
- [ ] 图片、CSS、JS 文件路径正确（浏览器控制台无红色错误）
- [ ] 搜索功能可用（Pagefind 索引正常）
- [ ] 暗色模式切换正常
- [ ] 移动端响应式布局正常
- [ ] Lighthouse 评分 ≥ 90（Performance + Accessibility）

**快速验证命令**（本地模拟 GitHub Pages 环境 — Content-First v2 架构）：

```bash
# ✅ 检查 content-first 架构目录结构
ls content/chapters/                    # 应该看到 *.md 文件
cat content/config.ts                   # 应该有 Content Collections 定义

# 模拟 base 路径环境
GH_PAGES_BASE=/repo-name npm run build

# 使用 serve 模拟静态服务器
npx serve dist -l 3000

# 访问测试地址
# http://localhost:3000/repo-name/
```

> 💡 **Content-First 架构验证要点**: 确认构建产物 `dist/` 中的链接都正确指向 `/repo-name/chapters/xxx` 而非 `/repo-name/docs/xxx`

---

## 🔧 详细配置指南

### base 路径深度解析

**为什么必须设置 base？**

GitHub Pages 项目站点的 URL 结构：
```
https://username.github.io/<repository-name>/
```

Astro 默认假设网站位于根路径 `/`，但实际在 `/<repo>/` 下。导致：
- ❌ CSS/JS 请求 `/_astro/style.css` → 实际应为 `/<repo>/_astro/style.css`
- ❌ 图片请求 `/images/bg.png` → 404
- ❌ 导航链接跳转到错误地址

**base 的作用**：为所有相对路径添加前缀。

**动态 base 配置**（本地开发 + 生产环境兼容）：

```javascript
// astro.config.mjs
export default defineConfig({
  base: process.env.GH_PAGES_BASE || '/',
  // 开发环境：base = '/'（默认）
  // 生产环境：GH_PAGES_BASE='/repo-name/' npm run build
});
```

**package.json 脚本**：

```json
{
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "build:gh": "GH_PAGES_BASE=/repo-name astro build",
    "preview": "astro preview"
  }
}
```

### trailingSlash 必须设置为 'always'

**原因**：GitHub Pages 的行为机制

| 请求路径 | GitHub Pages 查找 | Astro 默认输出 | 结果 |
|---------|------------------|---------------|------|
| `/about` | `/about/index.html` | `/about.html` | **404 ❌** |
| `/about/` | `/about/index.html` | `/about/index.html` | **200 ✅** |

**配置方法**：

```javascript
trailingSlash: 'always',  // ✅ 正确
// trailingSlash: 'ignore',  // ❌ 错误：导致 GitHub Pages 404
```

### outDir 配置选项

**选项 A: 使用默认 `dist/` 目录（推荐）**

```javascript
// 不设置 outDir（默认值即可）
// GitHub Actions 使用 actions/upload-pages-artifact 上传 dist/
```

优点：
- ✅ 符合 Astro 惯例
- ✅ 官方 Action 最佳支持
- ✅ 无需 `.nojekyll` 文件

**选项 B: 输出到 `docs/` 目录（传统方式）**

```javascript
outDir: './docs',
```

适用场景：
- 不使用 GitHub Actions（手动部署）
- 在 Settings 中选择 "Deploy from branch" → `gh-pages` 分支或 `/docs` 文件夹

⚠️ **必须在 `docs/` 目录中创建 `.nojekyll` 文件**：

```bash
# 方式一：构建后自动创建
echo "" > docs/.nojekyll

# 方式二：在 public/ 中放置（每次构建自动复制）
echo "" > public/.nojekyll
```

原因：GitHub Pages 默认使用 Jekyll 处理，会忽略以 `_` 开头的目录（如 `_astro/`），导致所有 JS/CSS 丢失！

---

## 🌐 自定义域名配置

### 方法一：通过 GitHub Settings（推荐）

1. **Settings** → **Pages** → **Custom domain**
2. 输入域名（如 `www.example.com` 或 `example.com`）
3. 等待 GitHub 自动创建 DNS 记录提示
4. 到域名注册商处添加 DNS 记录：

**Apex 域名配置**（example.com）：

| 类型 | 名称 | 值 | TTL |
|------|------|-----|-----|
| A | @ | `185.199.108.153` | 3600 |
| A | @ | `185.199.109.153` | 3600 |
| A | @ | `185.199.110.153` | 3600 |
| A | @ | `185.199.111.153` | 3600 |
| CNAME | www | `username.github.io` | 3600 |

**子域名配置**（www.example.com / blog.example.com）：

| 类型 | 名称 | 值 | TTL |
|------|------|-----|-----|
| CNAME | www/blog | `username.github.io` | 3600 |

5. 等待 DNS 生效（通常几分钟，最长 48 小时）
6. 启用 **Enforce HTTPS**（强制 HTTPS，提高安全性）

### 方法二：CNAME 文件

在 `public/CNAME` 中添加：

```
www.example.com
```

或 Apex 域名：

```
example.com
```

### 更新 astro.config.mjs

```javascript
site: 'https://www.example.com',  // 更新为自定义域名
base: '/',                        // 自定义域名通常不需要 base（根路径）
trailingSlash: 'always',
```

### SSL/TLS 证书

✅ **GitHub Pages 自动提供 Let's Encrypt 证书**：
- 免费、自动续期
- 支持 HTTP/2
- 在 Settings → Pages → Enforce HTTPS 启用强制跳转

---

## 🔄 CI/CD 进阶配置

### 多环境部署（Staging / Production）

**分支策略**：

```
main          → Production 部署（正式站点）
staging       → Staging 部署（预发布测试）
develop       → 开发环境（开发者日常验证）
```

**`.github/workflows/deploy-staging.yml`**：

```yaml
name: Deploy to Staging

on:
  push:
    branches: ['staging']

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages-staging  # 单独的环境名称
      url: ${{ steps.deploy.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: npm
      - run: npm ci
      - run: npm run build
      - uses: withastro/action@v3
```

⚠️ **注意**：GitHub 免费版仅支持 **1 个 GitHub Pages 环境**。Staging 和 Production 共享同一个 URL。如需完全隔离的环境，考虑使用 Cloudflare Pages 或 Vercel（免费支持多环境）。

### 部署通知（Slack / Discord / Email）

在 `deploy.yml` 末尾添加通知步骤：

```yaml
      - name: Notify Success
        if: success()
        run: |
          curl -X POST -H 'Content-type: application/json' \
          --data '{
            "text": "✅ 教程站点部署成功!\n仓库: ${{ github.repository }}\n提交: ${{ github.sha }}\n作者: ${{ github.actor }}\nURL: ${{ steps.deploy.outputs.page_url }}"
          }' \
          ${{ secrets.SLACK_WEBHOOK_URL }}

      - name: Notify Failure
        if: failure()
        run: |
          curl -X POST -H 'Content-type: application/json' \
          --data '{
            "text": "❌ 部署失败!\n仓库: ${{ github.repository }}\n查看: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
          }' \
          ${{ secrets.SLACK_WEBHOOK_URL }}
```

### 自动回滚机制（高级）

基于健康检查的自动回滚（在 deploy job 后添加）：

```yaml
  health-check:
    runs-on: ubuntu-latest
    needs: [build-and-deploy]  # 依赖部署完成
    if: always()               # 即使部署成功也执行检查
    steps:
      - name: Wait for Deployment
        run: sleep 30  # 等待 CDN 生效

      - name: Health Check
        id: health
        run: |
          STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
            "${{ needs.build-and-deploy.outputs.page_url }}")

          if [ "$STATUS" != "200" ]; then
            echo "❌ Health check failed! Status: $STATUS"
            echo "rollback_needed=true" >> $GITHUB_OUTPUT
            exit 1
          fi
          echo "✅ Site healthy"
          echo "rollback_needed=false" >> $GITHUB_OUTPUT

      - name: Create Rollback Issue
        if: failure()
        run: |
          gh issue create \
            --title "🚨 部署失败 - 需要回滚" \
            --body "部署未通过健康检查。\n\n**操作建议**:\n1. \`git revert HEAD\`\n2. 推送到 main 触发重新部署\n3. 或手动回滚到上一个稳定版本" \
            --repo ${{ github.repository }}
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 📚 多形态发布支持（Content-First 架构优势）

> **架构优势**: Content-First v2 架构的 `content/chapters/` 作为**纯 Markdown 源**，天然支持多渠道发布，无需维护多份内容。

### 发布形态总览

```
content/chapters/*.md
       │
       ├──→ Astro 构建 → 交互式网站（GitHub Pages）✅ 主力
       ├──→ Pandoc      → PDF / EPUB / Word 🆕 可选
       ├──→ mdbook      → 备用静态站 🆕 可选
       └──→ Notion API  → 协作平台同步 🆕 可选
```

### 🆕 方案 1: PDF 自动生成（Pandoc + CI/CD）

**适用场景**: 需要提供离线阅读版本、打印版教程、或存档用途

#### 前置准备

```bash
# 安装 Pandoc（CI 环境通常会预装）
# Windows: choco install pandoc
# Mac: brew install pandoc
# Ubuntu: sudo apt-get install pandoc

# 安装 LaTeX 引擎（PDF 生成必需）
# Windows: 安装 MiKTeX 或 TeX Live
# Mac: brew install --cask mactex
```

#### PDF 生成脚本

创建 `scripts/generate-pdf.sh`：

```bash
#!/bin/bash
set -e

echo "📄 开始生成 PDF..."

# 从 content/chapters/ 读取所有 Markdown（按文件名排序）
pandoc content/chapters/*.md \
  --from markdown \
  --to pdf \
  --output dist/tutorial.pdf \
  --pdf-engine=xelatex \
  --metadata title="教程完整版" \
  --metadata author="作者名称" \
  --toc \                          # 自动生成目录
  --toc-depth=3 \                  # 目录深度 3 级
  --highlight-style=tango \        # 代码高亮主题
  --resource-path=. \              # 资源路径
  -V geometry:a4paper \            # A4 纸张
  -V geometry:margin=2.5cm \       # 页边距 2.5cm
  -V mainfont="Noto Sans CJC SC" \ # 中文字体（需系统安装）
  -V monofont="Noto Sans Mono CJC SC"

echo "✅ PDF 生成完成: dist/tutorial.pdf"
```

#### package.json 脚本配置

```json
{
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "build:pdf": "./scripts/generate-pdf.sh",
    "build:all": "npm run build && npm run build:pdf",
    "preview": "astro preview"
  }
}
```

#### GitHub Actions 集成（自动生成 + 发布 PDF）

在 `.github/workflows/deploy.yml` 的 build job 中添加 PDF 生成步骤：

```yaml
      - name: Generate PDF (Optional)
        if: success()
        run: |
          echo "📄 Installing Pandoc..."
          sudo apt-get update && sudo apt-get install -y pandoc texlive-xetex texlive-fonts-recommended

          echo "📄 Generating PDF from content/chapters/..."
          chmod +x scripts/generate-pdf.sh
          npm run build:pdf

          echo "✅ PDF generated successfully"
          ls -lh dist/tutorial.pdf

      - name: Upload PDF Artifact (Optional)
        if: success()
        uses: actions/upload-artifact@v4
        with:
          name: tutorial-pdf
          path: dist/tutorial.pdf
          retention-days: 30  # 保留 30 天
```

**下载 PDF**: 在 GitHub Actions 运行页面底部的 **Artifacts** 区域下载生成的 PDF 文件。

### 🆕 方案 2: EPUB 电子书生成

修改脚本支持 EPUB 输出：

```bash
# 生成 EPUB（适合电子阅读器）
pandoc content/chapters/*.md \
  --from markdown \
  --to epub \
  --output dist/tutorial.epub \
  --metadata title="教程电子书版" \
  --toc \
  --toc-depth=3 \
  --epub-cover-image=cover.png \  # 封面图片（可选）
  --css=styles/epub.css           # 自定义样式（可选）
```

### 🆕 方案 3: GitHub Releases 自动发布（PDF + Source）

在部署成功后自动创建 Release 并上传 PDF：

```yaml
      - name: Create GitHub Release (Optional)
        if: success() && github.ref == 'refs/heads/main'
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          VERSION="v$(date +'%Y.%m.%d')"
          
          gh release create "$VERSION" \
            --title "教程发布 $VERSION" \
            --notes "## 📦 发布内容

          ### 🌐 在线版本
          - GitHub Pages: https://username.github.io/repo/

          ### 📄 离线版本
          - **tutorial.pdf**: 完整离线 PDF 版本
          - **tutorial.epub**: 电子书格式（适配 Kindle/iBooks）

          ---
          *由 Content-First 架构自动生成*" \
            dist/tutorial.pdf \
            dist/tutorial.epub
```

### 多形态发布对比

| 形态 | 工具 | 适用场景 | 维护成本 | CI/CD 支持 |
|------|------|---------|----------|-----------|
| **交互网站** | Astro + Starlight | 在线浏览、搜索、响应式 | 低（主力）| ✅ 自动部署 |
| **PDF** | Pandoc + XeLaTeX | 离线阅读、打印、存档 | 中（需 LaTeX）| ✅ 可选 |
| **EPUB** | Pandoc | Kindle、iBooks 等阅读器 | 低 | ✅ 可选 |
| **Word** | Pandoc | 编辑、审阅、协作 | 低 | ✅ 可选 |

> 💡 **推荐策略**: 以 **GitHub Pages 网站**为主力发布渠道，**PDF** 作为可选项按需生成。Content-First 架构确保所有格式从同一内容源生成，无需手动同步。

---

## 🐛 常见问题排查手册

### 问题 1: 静态资源全部 404

**症状**：
- 页面 HTML 加载成功，但样式丢失、图片不显示
- 控制台报错：`GET https://username.github.io/_astro/style.css 404`

**原因**：未设置 `base` 或 `base` 值错误

**解决方案**：
```javascript
// astro.config.mjs
base: '/your-repo-name/',  // 必须与仓库名完全一致
```

**验证方法**：
```bash
# 检查生成的 HTML 中的资源路径
cat dist/index.html | grep '_astro'
# 应该看到：/_astro/style.abc123.css
# 如果是 /your-repo-name/_astro/style.abc123.css 则正确
```

### 问题 2: 点击导航链接后 404

**症状**：
- 首页正常，点击侧边栏或内部链接后 404
- 直接刷新页面也 404

**原因**：未设置 `trailingSlash: 'always'`

**解决方案**：
```javascript
trailingSlash: 'always',
```

### 问题 3: `_astro/` 目录被忽略（所有 JS/CSS 缺失）

**症状**：
- 构建成功，但网站完全无样式、无交互功能
- 浏览器 Network 面板显示所有 `/_astro/*` 请求 404

**原因**：GitHub Pages 使用 Jekyll 处理，忽略了 `_` 开头的目录

**解决方案**（按优先级）：

1. **使用 GitHub Actions**（推荐）：自动绕过 Jekyll
2. **添加 `.nojekyll` 文件**：
   ```bash
   touch public/.nojekyll  # 或 touch docs/.nojekyll
   ```

### 问题 4: 构建内存不足（OOM）

**症状**：
- GitHub Actions 报错：`FATAL ERROR: Ineffective mark-compacts near heap limit`
- 大型教程站点（100+ 章）容易触发

**解决方案**：
```yaml
# deploy.yml 的 build step 中添加环境变量
- name: Build
  run: npm run build
  env:
    NODE_OPTIONS: --max-old-space-size=4096  # 增加到 4GB
```

**长期优化**：
- 减少单次构建的内容量（分批构建）
- 启用 Astro 6.0+ 实验性 Queued Rendering（渲染速度提升 2x）
- 清理未使用的依赖和插件

### 问题 5: 部署缓慢（>10 分钟）

**优化策略**：

1. ✅ **启用依赖缓存**（已在模板中配置）
2. ✅ **减少 Content Collections 数量**：如有数百篇内容，考虑分批
3. ✅ **启用实验性 Queued Rendering**（Astro 6.0+）：
   ```javascript
   experimental: {
     queuedRendering: { enabled: true },
   },
   ```
4. ✅ **优化图片**：使用 WebP 格式，减少图片数量和尺寸
5. ✅ **精简插件**：移除不必要的 Starlight 插件

---

## 📋 完整部署检查清单

### 部署前（构建阶段交付物验证）

- [ ] `npm run build` 无错误（exit 0）
- [ ] `astro.config.mjs` 中 `site` 和 `base` 正确设置
- [ ] `trailingSlash: 'always'` 已配置
- [ ] 本地 `npm run preview` 显示正常
- [ ] 浏览器控制台无 404/500 错误
- [ ] 所有图片、CSS、JS 资源加载成功
- [ ] 内部链接均可点击且不 404
- [ ] 响应式布局验证通过（375px / 768px / 1280px）
- [ ] 暗色模式切换正常
- [ ] 搜索功能可用
- [ ] Lighthouse Performance ≥ 90, Accessibility ≥ 90

### 配置验证

- [ ] `.github/workflows/deploy.yml` 存在且语法正确
- [ ] Actions 权限配置正确（contents: read, pages: write, id-token: write）
- [ ] Node.js 版本 ≥ 18（推荐 20）
- [ ] 如使用自定义域名，DNS 记录已配置

### 部署后（生产环境验证）

- [ ] GitHub Actions 工作流运行成功（绿色 ✓）
- [ ] 访问 GitHub Pages URL 可正常打开
- [ ] 首页样式、布局、图片显示正确
- [ ] 导航菜单可点击，所有章节可达
- [ ] 页面内搜索可用
- [ ] 移动端显示正常
- [ ] 无敏感信息泄露（API Key、密码等）
- [ ] 自定义域名 HTTPS 正常（如已配置）
- [ ] Lighthouse 评分达标（在线版）

---

## 📊 监控与维护

### Uptime 监控（免费方案）

| 服务 | 特点 | 价格 |
|------|------|------|
| **UptimeRobot** | 每 5 分钟检查，邮件/Slack 通知 | 免费 |
| **Better Uptime** | 包含状态页面，电话/SMS 告警 | 免费基础版 |
| **GitHub Status** | 有限监控（仅查看部署历史） | 免费 |

**UptimeRobot 配置示例**：
- 监控 URL: `https://username.github.io/repo/`
- 检查频率: 5 分钟
- 关键词检测: `<title>` 标签中的站点名称
- 通知: Slack Webhook / Email

### Core Web Vitals 监控（可选）

在布局组件中添加：

```astro
---
// src/layouts/BaseLayout.astro（如果自定义布局）
---

<script>
  import { onCLS, onFID, onINP, onLCP } from 'web-vitals';

  function sendToAnalytics(metric) {
    const body = JSON.stringify(metric);
    navigator.sendBeacon('/api/vitals', body);
  }

  onCLS(sendToAnalytics);
  onFID(sendToAnalytics);
  onINP(sendToAnalytics);
  onLCP(sendToAnalytics);
</script>
```

---

## 🔗 与构建阶段的衔接（Content-First v2 对齐）

### 版本兼容性矩阵

| publish 版本 | 兼容 build 版本 | 架构版本 | 状态 |
|-------------|----------------|---------|------|
| **v7.0.0** | **v2.0.0+** | **content-first-v2** | ✅ **当前推荐** |
| v6.1.0 | v1.0.0 - v1.x.x | 传统架构 | ⚠️ 已弃用 |

> ⚠️ **重要**: 本版本 (**v7.0.0**) 要求 **build v2.0.0+** (Content-First v2 架构)。如果使用旧版 build (v1.x)，请先升级 build 或使用 publish v6.1.0。

### 完整工作流（Content-First v2 架构）

```
┌─────────────────────────────────────────────────────────────────┐
│                    Content-First v2 完整流程                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────┐      ┌──────────────────────┐        │
│  │   🏗️ Build v2.0.0    │      │   🚀 Publish v7.0.0  │        │
│  │   (高频: 10-20次/项目)│ ───→ │   (低频: 2-3次/项目) │        │
│  └──────────────────────┘      └──────────────────────┘        │
│                                                                 │
│  ① npm create astro@latest          ① 配置 base/site/trailingSlash │
│     --template starlight            ② 创建 .github/workflows/    │
│ ② 重构为 content/ 结构              ③ 配置 GitHub Settings       │
│     └── content/chapters/           ④ 首次部署 & 验证             │
│     └── src/components/             ⑤ 可选: 多形态发布            │
│ ③ 编写内容 (Markdown)                  ├── PDF (Pandoc)          │
│     └── 英文 slug 文件名                 ├── EPUB                │
│     └── 中文标题 (Frontmatter)           └── GitHub Releases     │
│ ④ 开发组件 (按功能分组)             ⑥ 可选: 自定义域名            │
│     └── interactive/                ⑦ 可选: 监控和通知            │
│     └── charts/                     ⑧ 生产环境持续维护            │
│     └── code/                           ├── Uptime 监控         │
│ ⑤ 配置 Content Collections             └── 自动回滚             │
│ ⑥ 内容增强管道 (可选)                                           │
│     ├── Mermaid 预渲染                    ↓                      │
│     └── 组件插槽注入                完成！✅                       │
│ ⑦ npm run build                                                  │
│ ⑧ npm run preview                                                │
│ ⑨ 通过所有质量门禁                                                │
│         ↓                                                        │
│    触发: /publish                                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 构建阶段交付物清单（Content-First v2）

publish 期望从 build 接收以下交付物：

| # | 交付物 | 路径 | 验证方式 | 必需 |
|---|--------|------|---------|------|
| 1 | **内容目录** | `content/chapters/*.md` | `ls content/chapters/` | ✅ 是 |
| 2 | **配置文件** | `content/config.ts` | 存在且含 schema 定义 | ✅ 是 |
| 3 | **构建产物** | `dist/` 目录 | `npm run build` 成功 | ✅ 是 |
| 4 | **HTML 文件** | `dist/**/*.html` | 包含正确 base 路径 | ✅ 是 |
| 5 | **静态资源** | `dist/_astro/*` | CSS/JS/字体文件完整 | ✅ 是 |
| 6 | **PDF（可选）** | `dist/tutorial.pdf` | `npm run build:pdf` 成功 | 🔵 可选 |
| 7 | **EPUB（可选）** | `dist/tutorial.epub` | Pandoc 生成成功 | 🔵 可选 |

### 触发条件

当以下条件**全部满足**时，调用本技能进入部署流程：

```bash
# ✅ 架构检查通过
test -d content/chapters && echo "Content-First v2 架构确认"

# ✅ 构建成功
npm run build && echo "Exit code: $?"

# ✅ 本地预览正常
npm run preview &
# 浏览器访问 http://localhost:4321 确认无误

# 准备就绪，调用发布技能
→ /publish               # 进入 GitHub Pages + 多形态发布流程
```

### 常见衔接问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| publish 找不到内容 | 使用旧版 `src/content/docs/` | 升级到 build v2.0.0，迁移到 `content/chapters/` |
| PDF 生成失败 | 未安装 Pandoc/LaTeX | CI 脚本中添加安装步骤，或跳过 PDF 生成 |
| URL 路径 404 | `base` 配置与仓库名不匹配 | 确保 `base: '/repo-name/'` 与 GitHub 仓库名一致 |
| 中文文件名乱码 | 未使用英文 slug | 遵循 build v2.0.0 命名规范：`01-slug.md` |

---

## 📂 本技能结构

```
skills/tutorial-writer-publish/
├── SKILL.md                              ← 本文件（自含型 ~500行）
└── references/
    ├── web-publishing.md                 ← Starlight 构建参考（遗留）
    ├── decision-record-rules.md          ← 决策细则
    └── github-pages-guide.md             ← 高级部署场景详解
```

---

## 📚 参考文档索引

| 文档 | 内容 | 何时读取 |
|------|------|---------|
| [web-publishing.md](references/web-publishing.md) | Starlight 完整配置参考 + 插件生态 | 需要 Starlight 构建细节时 |
| [github-pages-guide.md](references/github-pages-guide.md) | 多环境部署、回滚策略、安全加固、迁移指南 | 需要进阶部署场景时 |

> 💡 **加载时机**: 仅在需要额外细节时读取，本文件已覆盖主要部署流程

---

## 🔗 相关资源

| 资源 | 路径/链接 | 用途 |
|------|----------|------|
| 父技能 | [../SKILL.md](../SKILL.md) | Tutorial Writer 主路由器 |
| 构建子技能 | [../skills/tutorial-writer-build/SKILL.md](../skills/tutorial-writer-build/SKILL.md) | Astro 构建流程 |
| Astro 官方部署文档 | https://docs.astro.build/guides/deploy/github/ | 官方权威指南 |
| withastro/action | https://github.com/withastro/action | 官方 Action 仓库 |
| GitHub Pages 文档 | https://docs.github.com/en/pages | GitHub Pages 完整文档 |

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| **v7.0.0** | 2026-05-31 | **🎯 Content-First v2 对齐升级**: 全面对齐 build v2.0.0 架构；新增 `architecture_version: "content-first-v2"` 元数据；前置条件增加架构一致性检查（content/chapters/ 目录、英文 slug 命名规范）；astro.config.mjs 示例更新为完整 Content-First 版本（含 sidebar autogenerate 配置）；验证命令增加架构目录检查；**新增多形态发布支持章节**（PDF/EPUB/Word 生成 + Pandoc + CI/CD 集成 + GitHub Releases 自动发布）；衔接说明全面重写（版本兼容性矩阵、完整工作流图、交付物清单、常见问题表）；description 更新（新增 content-first/multi-format 触发词）；标题更新为"GitHub Pages + 多形态" |
| **v6.1.0** | 2026-05-30 | **🎯 扁平化重构**: 从 1-Sub Router 升级为**自含型单文件技能**；移除 skills/website-deploy/ 子目录；将完整部署指南（~450行）合并到主 SKILL.md；结构简化为 Type 1（单文件 + references）；保留所有功能和内容 |
| **v6.0.0** | 2026-05-30 | 1-Sub Router（publish → website-deploy）（前版本） |
