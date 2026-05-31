---
name: tutorial-writer
version: "v1.0.0"
author: skill-factory
description: Use when creating, writing, reviewing, building, publishing technical tutorial content via GitHub Pages with Monorepo architecture (Turborepo), or managing decisions across the full tutorial lifecycle including PDF/ebook generation and content schema management
tags: [tutorial, writing, technical-documentation, router, research, review, web, book, github-pages, decision-record, astro, starlight, monorepo, turborepo, content-management, pdf, epub]
dependency:
  parent: none
  children:
    - tutorial-writer-research
    - tutorial-writer-writing
    - tutorial-writer-review
    - tutorial-writer-content
    - tutorial-writer-web
    - tutorial-writer-book
    - tutorial-writer-github-pages
    - tutorial-writer-decision
meta:
  architecture_version: "monorepo-v1"
  sub_skills_count: 8
  web_version_requirement: ">=v1.0.0"
  book_version_requirement: ">=v1.0.0"
  github_pages_version_requirement: ">=v1.0.0"
---

# Tutorial Writer v1.0.0 — 8-Sub Router (Monorepo Edition)

> **定位**: 轻量路由枢纽 — 将教程创作请求分发到 8 个独立子技能
> **架构**: 8-Entry Router (root → skills/ = Layer 0 → Layer 1)
> **工具链**: Turborepo | **方案**: 方案 C (8-Sub Hybrid + Independent Init)
> **架构版本**: **Monorepo-v1**（内容-格式解耦 + 三层分离）

## 目标

将教程创作的完整生命周期（调研规划 → 撰写执行 → 内容管理 → 质量校验 → 网站构建 → 电子书生成 → 部署发布 → 决策贯穿）通过统一入口分发，每个阶段有独立的技能文件和细则。

**能做什么**:
- 智能路由用户请求到 8 个自含型子技能
- 提供全局速查（铁律/分类）
- 展示子技能概览和相互依赖关系
- 引导项目初始化流程

**不能做什么**:
- 不包含具体操作步骤（各子技能负责）
- 不执行校验或构建或发布（→ `/review` `/web` `/book` `/github-pages`）
- 不包含项目初始化逻辑（→ 见下方"🚀 项目初始化"章节）

---

## 🏗️ Monorepo 架构概览

> **设计来源**: [README.md](.trae/tutorial-writer-rebuild/README.md) 第 4、5 章
> **核心哲学**: **内容是唯一真相源，格式是可扩展的表示层**

### 架构核心理念

```
Layer 1: 路由层 (SKILL.md)          → 纯请求分发
Layer 2: 技能层 (skills/*)           → 每个技能只关注核心职责
Layer 3: 工具层 (scripts+templates)  → 初始化、模板、共享工具

apps/                            ← 应用层
├── web/ (表示层 A)         ← 网站 (Astro + Starlight, 依赖 content)
packages/                        ← 库层
├── content/ (数据层)             ← 唯一真相源
└── book/    (表示层 B)          ← 电子书 (Pandoc + PDF, 依赖 content)

依赖关系: content ← web, content ← book (禁止反向)
```

### 三大设计原则

| 原则 | 说明 |
|------|------|
| **单一职责** | 每个子技能只回答一个问题 |
| **依赖方向正确** | content ← 被 tutorial/book 依赖，禁止反向 |
| **初始化解耦** | init 脚本负责创建项目骨架，子技能假设包已存在 |

### 版本兼容性要求

| 子技能 | 最低版本 | 架构支持 |
|--------|---------|---------|
| **web** (apps/web) | **v1.0.0+** | ✅ Monorepo (移除初始化逻辑) |
| **book** (packages/book) | **v1.0.0+** | ✅ 全新电子书生成 |
| **github-pages** | **v1.0.0+** | ✅ 仅部署 (移除 PDF/EPUB) |

> **本路由器要求 web (apps/web) ≥ v1.0.0、book ≥ v1.0.0、github-pages ≥ v1.0.0**。旧版子技能使用传统架构，与本版本不兼容。

---

## 🎯 核心原则（速查）

```
┌──────────────────────────────────────────────┐
│                三大铁律                        │
├──────────────────────────────────────────────┤
│ ① 层级 ≤3 层 (references/assets 不算)         │
│ ② NO SKILL WITHOUT USE CASE IN AGENTS         │
│ ③ description 只写触发条件 (CSO)              │
└──────────────────────────────────────────────┘
```

**CSO 规则**: description 含 "Use when..."，max 1024 字符

详情见 [references/design-principles.md](references/design-principles.md)。

---

## 🧭 8-Sub 路由表

```
用户说...                                        → 调用
─────────────────────────────────              ─────────────────────────────────────
"搜索/调研/规划/找资料/设计章节结构"            → 📚 /research       (调研与规划)
"写/撰写/创作/编写章节"                        → ✍️ /writing        (撰写执行)
"检查/校对/质量/门禁/评分"                     → ✅ /review         (质量校验)
"内容结构/schema/命名规范/Frontmatter/目录组织" → 📝 /content        (内容管理) 🆕
"构建网站/Astro/Starlight/组件/配置"           → 🌐 /web            (网站构建) ⭐ 高频
"PDF/电子书/Pandoc/排版/EPUB/LaTeX"           -> 📖 /book           (电子书生成) 🆕
"部署/GitHub Pages/Actions/CI-CD/域名"         → 🚀 /github-pages   (Pages 部署) 🟢 低频
"配置/决策/改决策/看看决策/冲突"               → 📐 /decision      (决策系统)
```

### 复合场景

| 用户意图 | 执行顺序 |
|---------|---------|
| 完整创作一个教程（网站+电子书） | research → writing → content → review → web + book → github-pages |
| 完整创作一个教程（仅网站） | research → writing → content → review → web → github-pages |
| 生成电子书 PDF | research → writing → content → book |
| 优化已有章节 | review → writing → content → review → web → github-pages |
| 创建新教程项目 | decision → 运行 init 脚本 → research → writing → content → review → web → github-pages |
| 仅修改配置 | decision |
| 仅构建/重构网站 | web（可独立反复调用）|
| 仅重新部署 | github-pages（可独立调用）|
| 仅生成电子书 | book（可独立调用）|

### 歧义处理

不确定用户意图时提供选项：

> "您是想：a) 📚 调研规划 b) ✍️ 撰写/修改内容 c) 📝 内容结构管理 d) ✅ 质量检查 e) 🌐 构建网站 f) 📖 生成电子书 g) 🚀 部署发布 h) 📐 管理决策？"

---

## 📂 子技能一览

| # | 子技能 | 版本 | 变更类型 | 职责 | 触发词 | 关键特性 | 频率 |
|---|--------|------|---------|------|--------|---------|------|
| ① | [research](skills/tutorial-writer-research/SKILL.md) | v1.0.0 | ✅ 保持 | 调研规划 | 搜索/规划/设计结构 | 搜索方法论+长度规划+标准概览 | 低 |
| ② | [writing](skills/tutorial-writer-writing/SKILL.md) | v1.0.0 | ⚠️ 精简 | 撰写执行 | 写/撰写/完成章节 | 写作流程+素材管理+规范R1-R6（已移除内容管理部分） | 中 |
| ③ | [review](skills/tutorial-writer-review/SKILL.md) | v1.0.0 | ✅ 保持 | 质量校验 | 检查/校对/门禁 | 14项质量门禁+评分卡 | 中 |
| ④ | [content](skills/tutorial-writer-content/SKILL.md) | v1.0.0 | 🆕 新增 | **内容管理** | **内容结构/schema/命名规范** | **文件组织+Frontmatter schema+Content Collections+增强管道** | 中 |
| ⑤ | [web](skills/tutorial-writer-web/SKILL.md) | v1.0.0 | ✏️ 重命名 | **网站构建** | **构建/Astro/Starlight/组件/配置** | **Astro+Starlight配置+组件开发+构建优化（已移除初始化）** | 🔴 高 |
| ⑥ | [book](skills/tutorial-writer-book/SKILL.md) | v1.0.0 | 🆕 新增 | **电子书生成** | **PDF/电子书/Pandoc/排版/EPUB** | **PDF/EPUB生成+Pandoc配置+LaTeX模板+电子书样式** | 🟡 中 |
| ⑦ | [github-pages](skills/tutorial-writer-github-pages/SKILL.md) | v1.0.0 | ✏️ 重命名 | **Pages 部署** | **部署/GitHub Pages/Actions/CI-CD** | **GitHub Actions+Pages部署+域名/DNS/SSL+监控（已移除PDF/EPUB）** | 🟢 低 |
| ⑧ | [decision](skills/tutorial-writer-decision/SKILL.md) | v1.0.0 | ✅ 保持 | 决策贯穿 | 配置/决策 | 决策方法论+阶段映射+冲突解决 | 贯穿 |

> 8 个子技能完全自含：独立 SKILL.md + references/ + 阶段性决策细则
>
> **频率说明**: web 为高频子技能（预计每项目 10-20 次调用），github-pages 为低频（2-3 次），book 为中频（3-5 次）
>
> **变更说明**:
> - **✅ 保持**: 职责不变，仅更新版本号和引用
> - **⚠️ 精简**: 移除了内容管理相关部分（→ content 子技能）
> - **🆕 新增**: 全新子技能，填补职责空白
> - **✏️ 重命名**: 目录重命名 + 职责聚焦（如 publish → github-pages 仅保留部署）

---

## 📂 项目结构

```
tutorial-writer/
├── SKILL.md                              ← 本文件 (8-Sub 路由器)
├── references/                           ← 全局共享参考
│   ├── design-principles.md              ← 铁律+分类+架构说明
│   ├── cross-chapter-rules.md            ← R7-R10 跨章一致性规则
│   ├── phase-mapping.md                  ← 阶段→决策项映射
│   └── monorepo-guide.md                 ← 🆕 Turborepo 使用指南
├── assets/                               ← 全局共享模板
│   ├── decision-record-schema.json
│   └── decision-record-template.json
└── skills/                               ← Layer 1: 8个独立子技能
    ├── ① tutorial-writer-research/       ← 📚 调研规划 (保持)
    ├── ② tutorial-writer-writing/        ← ✍️ 撰写执行 (精简)
    ├── ③ tutorial-writer-review/         ← ✅ 质量校验 (保持)
    ├── 🆕 ④ tutorial-writer-content/     ← 📝 内容管理 (新增)
    ├── ✏️ ⑤ tutorial-writer-web/         ← 🌐 网站构建 (原 build)
    ├── 🆕 ⑥ tutorial-writer-book/        ← 📖 电子书生成 (新增)
    ├── ✏️ ⑦ tutorial-writer-github-pages/← 🚀 Pages 部署 (原 publish)
    └── ⑧ tutorial-writer-decision/       ← 📐 决策贯穿 (保持)
```

---

## 🚀 项目初始化

> **重要**: 项目初始化已迁移至官方 CLI 工具链，详见下方"🚀 项目初始化 (Official Tools)"章节。

---

## ⚠️ 注意事项

- **子技能优先**: 根文件仅做路由，详细逻辑在各子技能中
- **每个子技能可独立使用**: 有自己的 description，Agent 可直接触发
- **全局 references/ 仅放跨子技能公共内容**: 设计原则/跨章规则/阶段映射/Monorepo 指南
- **职能归属明确**: 搜索规划在 research，撰写在写作，内容管理在 content，校验在 review，网站构建在 web，电子书在 book，部署在 github-pages，决策在 decision
- **决策贯穿所有阶段**: 每个子技能内有独立的 `decision-record-rules.md` 定义本阶段决策细则
- **🆕 Monorepo 架构约束**:
  - **必须通过 init 脚本初始化项目**: 不要在子技能中手动创建 Monorepo 结构
  - **版本要求**: web ≥ v1.0.0, book ≥ v1.0.0, github-pages ≥ v1.0.0
  - **依赖方向**: content 包被 web 和 book 依赖，禁止反向依赖
  - **内容唯一源**: 所有 Markdown 内容放在 `packages/content/src/chapters/`
  - **初始化顺序**: 先按照"🚀 项目初始化 (Official Tools)"章节初始化项目，再使用各子技能
  - **如需使用旧版架构**: 请降级到 tutorial-writer v6.1.0

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| **v1.0.0** | 2026-05-31 | **🔄 Monorepo 架构重大重构 (6→8 Sub)**: 版本重置为 v1.0.0；子技能从 6 个扩展至 8 个（新增 content、book；build→web，publish→github-pages 重命名）；新增 `meta.architecture_version: "monorepo-v1"` 和 `meta.sub_skills_count: 8` 元数据；路由表从 6 行扩展至 8 行（新增 content/book 触发路径）；子技能一览表新增「版本号」和「变更类型」两列；复合场景更新（新增电子书生成、并行构建等场景）；新增「🚀 项目初始化 (Official Tools)」章节（使用官方 CLI 工具链）；注意事项全面更新为 Monorepo 架构约束；description 和 tags 更新（新增 monorepo/turborepo/pdf/epub/content-management） |
| **v6.1.0** | 2026-05-31 | Content-First v2 架构对齐（前版本，已终止维护） |
| **v6.0.0** | 2026-05-30 | 6-Sub Router 重构（前版本，已终止维护） |
| **v4.1.0** | 2026-05-30 | 模块化配置 + 插件生态（前版本） |
| **v4.0.0** | 2026-05-30 | Astro + Starlight 发布方案（前版本） |
| **v3.2.0** | 2026-05-29 | Tag 驱动发布 + skill-factory 接管（前版本） |
| **v3.1.0** | 2026-05-29 | Web 富交互增强（前版本） |
| **v3.0.0** | 2026-05-29 | 5-Sub Router 重构（前版本） |

---

**最后更新**: 2026-05-31 | **维护者**: skill-factory + user collaboration

---

## 🚀 项目初始化 (Official Tools)

> **重要**: Tutorial Writer 使用官方 CLI 工具链创建项目，
> 而非自定义脚本。这确保始终使用最新版本的模板和最佳实践。

### 初始化流程概览

```mermaid
graph LR
    A[Step 0: 环境准备] --> B[Step 1: 创建 Monorepo]
    B --> C[Step 2: 添加 content 包]
    C --> D[Step 3: 创建 web 包]
    D --> E[Step 4: 添加 book 包]
    E --> F[Step 5: 配置依赖]
    F --> G[Step 6: 注入 TW 配置]
    
    style A fill:#e3f2fd,stroke:#1565c0
    style G fill:#c8e6c9,stroke:#2e7d32
```

### Step 0: 前置环境检查

```bash
# 确保 Node.js >= 18
node --version  # 需要 v18+

# 确保包管理器可用（任选其一）
bun --version    # 推荐（教程项目使用 bun）
# 或 pnpm --version
# 或 npm --version

# 可选：安装 Turborepo CLI（如果需要全局命令）
bun add -D turbo
# 或 npx turbo  （推荐，无需安装）
```

### Step 1: 创建 Monorepo 骨架

使用 Turborepo 官方脚手架：

```bash
# 方式 A: 使用 create-turbo（推荐，交互式）
bunx create-turbo@latest <project-name>
# 会提示选择:
# - Package manager: bun (推荐) / pnpm / yarn / npm
# - App type: 根据需求选择

cd <project-name>
bun install

# 方式 B: 手动创建（更可控）
mkdir <project-name> && cd <project-name>
bun init
# 在 package.json 中添加 workspaces: ["apps/*", "packages/*"]
# 创建 turbo.json（详见 Turborepo 官方文档）
```

**验证**:
```bash
ls turbo.json package.json
# 然后检查 package.json 包含 workspaces 配置
```

### Step 2: 添加 content 包（数据层）

```bash
# 使用 turbo gen 添加空包
turbo gen workspace \
  --name @repo/content \
  --type package \
  --destination packages/content

# 创建内容目录结构
mkdir -p packages/content/src/chapters
touch packages/content/src/chapters/.gitkeep
```

### Step 3: 创建 web 应用（网站层）

```bash
# 在 apps/web 下创建 Astro + Starlight 项目
mkdir -p apps/web && cd apps/web

# 使用 Astro 官方脚手架（自动获取最新 Starlight 模板）
bunx create astro@latest . --template starlight

# 返回项目根目录
cd ../..
```

> **注意**: `create-astro` 会生成完整的 Astro 项目结构。
> 我们不需要手动复制任何模板文件！
>
> **Turbo 约定**: 可运行的应用放在 `apps/` 目录，共享库放在 `packages/` 目录。`apps/web` 是新增的教程站点，与 `create-turbo` 默认生成的 `apps/web`、`apps/docs` 并列。

### Step 4: 添加 book 包（电子书层）

```bash
turbo gen workspace \
  --name @repo/book \
  --type package \
  --destination packages/book
```

### Step 5: 配置 Workspace 依赖

编辑各包的 `package.json`，声明依赖关系：

```json
// apps/web/package.json
{
  "dependencies": {
    "@repo/content": "workspace:*"
  }
}

// packages/book/package.json
{
  "dependencies": {
    "@repo/content": "workspace:*"
  }
}
```

### Step 6: 注入 Tutorial Writer 配置

这是 Tutorial Writer 的**核心增值部分**：

#### 6.1 Content Schema 定义

详见 [/content](./skills/tutorial-writer-content/SKILL.md) 子技能。

简要步骤：
```bash
# 创建 Content Collections 配置
cat > packages/content/src/config.ts << 'EOF'
import { defineCollection, z } from 'astro:content';
import { docsLoader, docsSchema } from '@astrojs/starlight/loaders';

const chapters = defineCollection({
  loader: docsLoader(),
  schema: docsSchema({
    schema: z.object({
      title: z.string(),
      description: z.string().optional(),
      draft: z.boolean().default(false),
      tags: z.array(z.string()).default([]),
      difficulty: z.enum(['beginner', 'intermediate', 'advanced']).optional(),
      readingTime: z.number().optional(),
      prerequisites: z.array(z.string()).default([]),
      hasInteractive: z.boolean().default(false),
      hasMermaid: z.boolean().default(false),
      hasMath: z.boolean().default(false),
    }),
  }),
});

export const collections = { chapters };
EOF
```

#### 6.2 PDF 生成配置（可选）

详见 [/book](./skills/tutorial-writer-book/SKILL.md) 子技能。

### 验证清单

初始化完成后，确认以下文件存在：

- [ ] `turbo.json` (根目录)
- [ ] `package.json` 包含 `workspaces: ["apps/*", "packages/*"]`
- [ ] `packages/content/package.json`
- [ ] `packages/content/src/config.ts`
- [ ] `apps/web/package.json`
- [ ] `apps/web/astro.config.mjs` (Starlight 配置)
- [ ] `packages/book/package.json`

### 常见问题

**Q: 可以用 pnpm/npm/yarn 吗？**
A: 可以！Turborepo 支持所有主流包管理器。本教程示例使用 `bun` 和 npm workspaces（`"workspaces"` 字段配置在 `package.json` 中）。

**Q: 必须按顺序执行吗？**
A: Step 2-4 可以并行执行（如果用多个终端），但 Step 5 必须在它们之后。

**Q: 如何更新到最新模板？**
A: 无需手动操作！每次运行 `create-astro@latest` 都会获取最新版本。
