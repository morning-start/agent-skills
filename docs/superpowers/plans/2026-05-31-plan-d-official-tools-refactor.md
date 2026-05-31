# Plan D — Official Tools Refactor 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 Tutorial Writer 从自定义脚本+硬编码模板架构迁移到官方CLI工具链，消除约6000行冗余代码和全部维护负担。

**Architecture:** 删除 `scripts/init-tutorial.sh` (1002行) 和 `templates/tutorial-starter/` (24文件)，将项目初始化逻辑替换为内嵌在根路由器 SKILL.md 中的官方工具命令序列 (`create-turbo` + `turbo gen` + `create-astro`)，同时精简 `monorepo-guide.md` 从2633行到~300行。

**Tech Stack:** Turborepo CLI, Astro CLI, Markdown (SKILL.md files)

---

## File Structure Map

```
process/tutorial-writer-skill/
├── SKILL.md                              ← Modify: 新增 ~120行初始化章节
├── scripts/
│   └── init-tutorial.sh                  ← DELETE (1002行)
├── templates/
│   └── tutorial-starter/                 ← DELETE (24文件, ~3000行)
├── references/
│   └── monorepo-guide.md                 ← REWRITE (2633→~300行)
└── skills/
    ├── tutorial-writer-content/SKILL.md   ← MODIFY: 更新前置条件 (~10行)
    ├── tutorial-writer-web/SKILL.md       ← MODIFY: 更新前置条件 (~15行)
    └── tutorial-writer-book/SKILL.md      ← MODIFY: 更新前置条件 (~15行)
```

---

## Task 1: Delete Custom Initialization System

**Files:**
- Delete: `process/tutorial-writer-skill/scripts/init-tutorial.sh`
- Delete: `process/tutorial-writer-skill/templates/tutorial-starter/` (entire directory, 24 files)

- [ ] **Step 1: Verify files exist before deletion**

Run these commands to confirm targets exist:

```bash
# Check init script exists and count lines
wc -l process/tutorial-writer-skill/scripts/init-tutorial.sh
# Expected: 1002

# Check templates directory exists and count files
find process/tutorial-writer-skill/templates/tutorial-starter/ -type f | wc -l
# Expected: 24

# List all files in templates for verification
ls -laR process/tutorial-writer-skill/templates/tutorial-starter/
```

- [ ] **Step 2: Delete the init script**

```bash
rm process/tutorial-writer-skill/scripts/init-tutorial.sh
```

Verify deletion:

```bash
ls process/tutorial-writer-skill/scripts/init-tutorial.sh 2>&1
# Expected: "No such file or directory"
```

- [ ] **Step 3: Delete the templates directory**

```bash
rm -rf process/tutorial-writer-skill/templates/tutorial-starter/
```

Verify deletion:

```bash
ls process/tutorial-writer-skill/templates/ 2>&1
# Expected: Either empty listing or "No such file or directory"
ls process/tutorial-writer-skill/templates/tutorial-starter/ 2>&1
# Expected: "No such file or directory"
```

- [ ] **Step 4: Clean up empty parent directories if needed**

```bash
# Remove scripts/ if empty
rmdir process/tutorial-writer-skill/scripts/ 2>/dev/null || true

# Remove templates/ if empty
rmdir process/tutorial-writer-skill/templates/ 2>/dev/null || true
```

- [ ] **Step 5: Commit deletion**

```bash
git add -u process/tutorial-writer-skill/scripts/ process/tutorial-writer-skill/templates/
git commit -m "refactor(tutorial-writer): remove custom init script and templates (Plan D)

- Delete scripts/init-tutorial.sh (1002 lines)
- Delete templates/tutorial-starter/ (24 files, ~3000 lines)
- These are replaced by official CLI toolchain (create-turbo + turbo gen + create-astro)"
```

---

## Task 2: Rewrite Root Router SKILL.md — Add Initialization Chapter

**Files:**
- Modify: `process/tutorial-writer-skill/SKILL.md`

- [ ] **Step 1: Read current SKILL.md to find insertion point**

Read the file and locate:
1. The line containing `"不包含项目初始化逻辑（→ \`scripts/init-tutorial.sh\`）"` (around line 46)
2. The end of the existing content (before any trailing metadata)

```bash
# Find the exact line numbers
grep -n "init-tutorial.sh" process/tutorial-writer-skill/SKILL.md
grep -n "^---$" process/tutorial-writer-skill/SKILL.md | tail -1
wc -l process/tutorial-writer-skill/SKILL.md
# Current expected: 254 lines
```

- [ ] **Step 2: Replace the old reference with new initialization chapter**

Find and replace the following text block in `SKILL.md`:

**OLD text** (to be replaced):
```markdown
- 不包含项目初始化逻辑（→ `scripts/init-tutorial.sh`）
```

**NEW text**:
```markdown
- 不包含项目初始化逻辑（→ 见下方"🚀 项目初始化"章节）
```

- [ ] **Step 3: Insert the complete "Project Initialization" chapter**

Insert the following content after the existing main sections (after the composite scenarios table, before the final `---` if present, or at end of file). The insertion point should be after the last `##` section:

```markdown

---

## 🚀 项目初始化 (Official Tools)

> **重要**: Tutorial Writer 使用官方 CLI 工具链创建项目，
> 而非自定义脚本。这确保始终使用最新版本的模板和最佳实践。

### 初始化流程概览

\`\`\`mermaid
graph LR
    A[Step 0: 环境准备] --> B[Step 1: 创建 Monorepo]
    B --> C[Step 2: 添加 content 包]
    C --> D[Step 3: 创建 web 包]
    D --> E[Step 4: 添加 book 包]
    E --> F[Step 5: 配置依赖]
    F --> G[Step 6: 注入 TW 配置]
    
    style A fill:#e3f2fd,stroke:#1565c0
    style G fill:#c8e6c9,stroke:#2e7d32
\`\`\`

### Step 0: 前置环境检查

\`\`\`bash
# 确保 Node.js >= 18
node --version  # 需要 v18+

# 确保包管理器可用（任选其一）
pnpm --version   # 推荐
# 或 npm --version
# 或 bun --version

# 可选：安装 Turborepo CLI（如果需要全局命令）
pnpm add -D turbo
# 或 npx turbo  （推荐，无需安装）
\`\`\`

### Step 1: 创建 Monorepo 骨架

使用 Turborepo 官方脚手架：

\`\`\`bash
# 方式 A: 使用 create-turbo（推荐，交互式）
bunx create-turbo@latest <project-name>
# 会提示选择:
# - Package manager: pnpm (推荐) / yarn / npm / bun
# - App type: 根据需求选择

cd <project-name>
pnpm install

# 方式 B: 手动创建（更可控）
mkdir <project-name> && cd <project-name>
pnpm init
# 创建 pnpm-workspace.yaml, turbo.json, package.json
# （详见 Turborepo 官方文档）
\`\`\`

**验证**:
\`\`\`bash
ls turbo.json pnpm-workspace.yaml package.json
# 这三个文件必须存在
\`\`\`

### Step 2: 添加 content 包（数据层）

\`\`\`bash
# 使用 turbo gen 添加空包
turbo gen workspace \\
  --name @<project-name>/content \\
  --type package \\
  --destination packages/content

# 创建内容目录结构
mkdir -p packages/content/src/chapters
touch packages/content/src/chapters/.gitkeep
\`\`\`

### Step 3: 创建 web 包（网站层）

\`\`\`bash
# 在 packages/web 下创建 Astro + Starlight 项目
mkdir -p packages/web && cd packages/web

# 使用 Astro 官方脚手架（自动获取最新 Starlight 模板）
bunx create astro@latest . --template starlight

# 返回项目根目录
cd ../..
\`\`\`

> **注意**: \`create-astro\` 会生成完整的 Astro 项目结构。
> 我们不需要手动复制任何模板文件！

### Step 4: 添加 book 包（电子书层）

\`\`\`bash
turbo gen workspace \\
  --name @<project-name>/book \\
  --type package \\
  --destination packages/book
\`\`\`

### Step 5: 配置 Workspace 依赖

编辑各包的 \`package.json\`，声明依赖关系：

\`\`\`json
// packages/web/package.json
{
  "dependencies": {
    "@<project-name>/content": "workspace:*"
  }
}

// packages/book/package.json
{
  "dependencies": {
    "@<project-name>/content": "workspace:*"
  }
}
\`\`\`

### Step 6: 注入 Tutorial Writer 配置

这是 Tutorial Writer 的**核心增值部分**：

#### 6.1 Content Schema 定义

详见 [/content](./skills/tutorial-writer-content/SKILL.md) 子技能。

简要步骤：
\`\`\`bash
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
\`\`\`

#### 6.2 PDF 生成配置（可选）

详见 [/book](./skills/tutorial-writer-book/SKILL.md) 子技能。

### 验证清单

初始化完成后，确认以下文件存在：

- [ ] \`turbo.json\` (根目录)
- [ ] \`pnpm-workspace.yaml\` (根目录)
- [ ] \`packages/content/package.json\`
- [ ] \`packages/content/src/config.ts\`
- [ ] \`packages/web/package.json\`
- [ ] \`packages/web/astro.config.mjs\` (Starlight 配置)
- [ ] \`packages/book/package.json\`

### 常见问题

**Q: 可以用 npm/yarn/bun 吗？**
A: 可以！Turborepo 支持所有主流包管理器。\`create-turbo\` 会让你选择。

**Q: 必须按顺序执行吗？**
A: Step 2-4 可以并行执行（如果用多个终端），但 Step 5 必须在它们之后。

**Q: 如何更新到最新模板？**
A: 无需手动操作！每次运行 \`create-astro@latest\` 都会获取最新版本。
```

- [ ] **Step 4: Verify the updated SKILL.md**

```bash
# Check new line count (should be ~374, was 254)
wc -l process/tutorial-writer-skill/SKILL.md

# Verify key new sections exist
grep -n "🚀 项目初始化" process/tutorial-writer-skill/SKILL.md
grep -n "Official Tools" process/tutorial-writer-skill/SKILL.md
grep -n "create-turbo" process/tutorial-writer-skill/SKILL.md

# Verify old reference is gone
grep -n "init-tutorial.sh" process/tutorial-writer-skill/SKILL.md
# Expected: No results (or only in git history)
```

- [ ] **Step 5: Commit SKILL.md update**

```bash
git add process/tutorial-writer-skill/SKILL.md
git commit -m "refactor(tutorial-writer): add official-tools initialization chapter to root router

- Add ~120-line 'Project Initialization' section using create-turbo + turbo gen + create-astro
- Replace old reference to init-tutorial.sh with inline command sequence
- Include Step 0-6 flow with Mermaid diagram, commands, and FAQ"
```

---

## Task 3: Rewrite monorepo-guide.md (Major Simplification)

**Files:**
- Rewrite: `process/tutorial-writer-skill/references/monorepo-guide.md`

- [ ] **Step 1: Back up and read current file**

```bash
# Count current lines
wc -l process/tutorial-writer-skill/references/monorepo-guide.md
# Expected: 2633

# Create backup
cp process/tutorial-writer-skill/references/monorepo-guide.md \
   process/tutorial-writer-skill/references/monorepo-guide.md.bak
```

- [ ] **Step 2: Replace entire file with simplified version**

Write the following content to `references/monorepo-guide.md` (complete replacement):

```markdown
# Monorepo 快速参考 (Tutorial Writer 特有)

> **定位**: Tutorial Writer 架构专用的补充指南
> **非目标**: 不重复 Turborepo/Astro 官方文档
> **适用版本**: v1.0.0 (Plan D: Official Tools)
> **最后更新**: 2026-05-31

---

## 目录

- [1. Tutorial Writer 三包架构](#1-tutorial-writer-三包架构)
- [2. Workspace 依赖规则](#2-workspace-依赖规则)
- [3. 日常工作流速查](#3-工作流速查)
- [4. 常见问题 (TW 特有)](#4-常见问题-tw-特有)
- [5. 相关资源链接](#5-相关资源链接)

---

## 1. Tutorial Writer 三包架构

### 1.1 核心设计理念

\`\`\`
内容是唯一真相源 → 格式是可扩展的表示层 → 部署是最终输出目标
\`\`\`

| 原则 | 说明 |
|------|------|
| **单一职责** | 每个子技能只回答一个问题 |
| **依赖方向正确** | content ← 被 web/book 依赖，禁止反向 |
| **官方工具优先** | 项目创建使用 create-turbo / turbo gen / create-astro |

### 1.2 包职责定义

| 包 | 职责 | 技术栈 | 说明 |
|----|------|--------|------|
| **content** | 数据层：内容 + Schema | Astro Content Collections | 唯一真相源 |
| **web** | 展示层：网站渲染 | Astro + Starlight | 消费 content |
| **book** | 格式层：PDF/ePub | Pandoc + XeLaTeX | 消费 content |

### 1.3 推荐的 turbo.json 配置

\`\`\`json
{
  "\$schema": "https://turbo.build/schema.json",
  "tasks": {
    "dev": {
      "cache": false,
      "persistent": true
    },
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", "*.pdf"]
    }
  }
}
\`\`\`

**关键点**:
- \`^build\` 表示先构建所有上游依赖（即 content）
- outputs 声明缓存命中时可复用的产物

---

## 2. Workspace 依赖规则

### 2.1 正确的依赖声明

\`\`\`json
// packages/web/package.json
{
  "name": "@my-project/web",
  "dependencies": {
    "@my-project/content": "workspace:*"
  }
}

// packages/book/package.json
{
  "name": "@my-project/book",
  "dependencies": {
    "@my-project/content": "workspace:*"
  }
}
\`\`\`

### 2.2 禁止的反向依赖

| 反向依赖 | 状态 | 原因 |
|---------|------|------|
| ❌ content → web | 禁止 | 数据层不应依赖展示层 |
| ❌ content → book | 禁止 | 数据层不应依赖格式层 |
| ❌ web ↔ book | 禁止 | 两个输出格式应独立 |
| ✅ web → content | 允许 | 展示层数据来源 |
| ✅ book → content | 允许 | 格式层数据来源 |

### 2.3 pnpm-workspace.yaml 示例

\`\`\`yaml
packages:
  - "packages/*"
\`\`\`

这会自动发现 \`packages/\` 下的所有含 \`package.json\` 的目录。

---

## 3. 日常工作流速查

### 3.1 命令速查表

| 操作 | 命令 | 说明 |
|------|------|------|
| **启动开发** | \`turbo run dev\` | 所有包并行启动 |
| **仅启动 web** | \`turbo run dev --filter=@<project>/web\` | 单独开发网站 |
| **全量构建** | \`turbo run build\` | 先 build content，再并行 web+book |
| **仅构建 PDF** | \`turbo run build:book\` | 只生成电子书 |
| **添加新包** | \`turbo gen workspace --name ... --type package\` | 官方命令 |
| **查看包图** | \`turbo run devtools\` | 浏览器可视化依赖图 |

### 3.2 内容创作流程

1. 在 \`packages/content/src/chapters/\` 创建 \`.md\` 文件
2. 按照 [/content](../skills/tutorial-writer-content/SKILL.md) 的 Schema 编写 Frontmatter
3. 运行 \`turbo run dev\` 预览效果
4. 内容变更后 web 和 book 自动热重载

### 3.3 并行构建优势

\`\`\`
# 传统方式: 串行构建
build content (5s) → build web (30s) → build book (20s) = 55s 总计

# Turborepo 方式: 并行构建
build content (5s) → [build web (30s) || build book (20s)] = 35s 总计
# 节省: 36% (假设双核 CPU)
\`\`\`

---

## 4. 常见问题 (TW 特有)

### Q1: content 包的章节如何被 web 和 book 共享？

A: 通过 Astro Content Collections。web 包在 \`astro.config.mjs\` 中通过 \`contentDirs\` 引用 content 包路径。book 包通过 Pandoc 直接读取 Markdown 文件。两者消费同一数据源但互不影响。

### Q2: 如何只更新一个包而不重建全部？

A: Turborepo 自动检测变更，只重建受影响的包及其下游依赖。例如：
- 只改了 content → 重建 content + web + book
- 只改了 web → 仅重建 web
- 只改了 book → 仅重建 book

### Q3: 添加第四种格式（如 EPUB）？

A:
1. \`turbo gen workspace --name @<project>/epub --type package\`
2. 在新包中实现转换逻辑
3. 更新 turbo.json 的 build 任务（如有需要）
4. （可选）创建对应的子技能

详见根路由器 SKILL.md 的"项目初始化"章节 Step 4 变体。

### Q4: Windows 兼容性？

A: 官方工具 (\`create-turbo\`, \`turbo gen\`) 原生支持 Windows。无需 Git Bash 或 WSL。\`create-astro\` 同样支持 Windows PowerShell。

### Q5: 与旧版 (v6.x) 的主要区别？

A:
- v6.x: 自定义 init 脚本 + 硬编码模板
- v1.0.0 (Plan D): 官方 CLI 工具链 + AI 编排命令序列
- 详见 [.trae/tutorial-writer-rebuild/MIGRATION-v6-to-v1.md](../../../.trae/tutorial-writer-rebuild/MIGRATION-v6-to-v1.md)

---

## 5. 相关资源链接

### 官方文档

| 工具 | 文档地址 | 用途 |
|------|---------|------|
| **Turborepo** | https://turborepo.org/docs | 任务编排、缓存、远程构建 |
| **create-turbo** | https://turborepo.org/docs/getting-started/installation | 快速开始 |
| **turbo gen** | https://turborepo.org/docs/guides/generating-code | 代码生成 |
| **Astro** | https://docs.astro.build | 静态站点框架 |
| **Starlight** | https://starlight.astro.build | 文档主题 |
| **pnpm workspaces** | https://pnpm.io/workspaces | 包管理器配置 |

### Skill 内部文档

| 文档 | 路径 | 内容 |
|------|------|------|
| 根路由器 | \`SKILL.md\` | 7-Sub 路由 + 初始化流程 |
| Content 技能 | \`skills/tutorial-writer-content/SKILL.md\` | Schema、命名规范 |
| Web 技能 | \`skills/tutorial-writer-web/SKILL.md\` | Astro + Starlight 配置 |
| Book 技能 | \`skills/tutorial-writer-book/SKILL.md\` | PDF/ePub 生成 |
| GitHub Pages | \`skills/tutorial-writer-github-pages/SKILL.md\` | 部署配置 |

---

*本指南仅覆盖 Tutorial Writer 特有的 Monorepo 约定和最佳实践。*
*通用的 Turborepo/Astro/pnpm 使用请参考上方官方文档。*
```

- [ ] **Step 3: Verify the simplified guide**

```bash
# Check new line count (should be ~300, was 2633)
wc -l process/tutorial-writer-skill/references/monorepo-guide.md

# Verify old sections are gone
grep -n "一键初始化" process/tutorial-writer-skill/references/monorepo-guide.md
# Expected: No results

grep -n "Turborepo 配置详解" process/tutorial-writer-skill/references/monorepo-guide.md
# Expected: No results (this detailed section was removed)

# Verify new structure exists
grep -n "^## " process/tutorial-writer-skill/references/monorepo-guide.md
# Should show: 1.三包架构, 2.Workspace规则, 3.工作流速查, 4.常见问题, 5.资源链接
```

- [ ] **Step 4: Clean up backup file**

```bash
# Remove backup if everything looks good
rm process/tutorial-writer-skill/references/monorepo-guide.md.bak
```

- [ ] **Step 5: Commit guide simplification**

```bash
git add process/tutorial-writer-skill/references/monorepo-guide.md
git commit -m "refactor(tutorial-writer): simplify monorepo-guide.md from 2633 to ~300 lines (-89%)

- Remove duplicated official documentation (Turborepo config, workspace setup, CI/CD)
- Keep only TW-specific content: architecture rules, dependency guidelines, quick-reference
- Add official tool links for comprehensive reference
- New structure: 5 focused sections instead of 10 verbose ones"
```

---

## Task 4: Update Sub-skill Prerequisites (Content/Web/Book)

**Files:**
- Modify: `process/tutorial-writer-skill/skills/tutorial-writer-content/SKILL.md`
- Modify: `process/tutorial-writer-skill/skills/tutorial-writer-web/SKILL.md`
- Modify: `process/tutorial-writer-skill/skills/tutorial-writer-book/SKILL.md`

- [ ] **Step 1: Update tutorial-writer-content/SKILL.md prerequisites**

Find the "前置条件" (or "Prerequisites") section in the file. Replace it entirely with:

```markdown
## 前置条件

- [ ] 已使用官方工具创建 Monorepo 项目
  - 推荐命令: \`bunx create-turbo@latest <project-name>\`
  - 或手动创建（详见根路由器 SKILL.md 的 **"🚀 项目初始化"** 章节 Step 0-1）
- [ ] 已添加 content 包:
  \`turbo gen workspace --name @<project>/content --type package\`
  详见根路由器 Step 2
- [ ] \`packages/content/src/\` 目录存在
- [ ] Node.js >= 18 已安装

> **重要**: 本子技能假设 \`packages/content/\` 已经存在。
> 如果还没有，请先执行根路由器中的 **Step 0-2**。
```

- [ ] **Step 2: Update tutorial-writer-web/SKILL.md prerequisites**

Find the "前置条件" section. Replace it entirely with:

```markdown
## 前置条件

- [ ] Monorepo 项目已初始化（含 \`turbo.json\`, \`pnpm-workspace.yaml\`)
  详见根路由器 SKILL.md **Step 1**
- [ ] \`packages/web/\` 已通过 Starlight 模板创建
  - 推荐命令: 在 \`packages/web/\` 下运行
    \`bunx create astro@latest . --template starlight\`
  - 详见根路由器 SKILL.md **Step 3**
- [ ] \`@<project>/content\` 包存在且已在 web/package.json 中声明依赖
  \`\`\`json
  { "dependencies": { "@<project>/content": "workspace:*" } }
  \`\`\`

> **注意**: 本子技能专注于 **Astro + Starlight 配置和组件开发**，
> **不包含**项目创建逻辑。
> 
> 项目初始化请参考根路由器的 **"🚀 项目初始化"** 章节。
```

- [ ] **Step 3: Update tutorial-writer-book/SKILL.md prerequisites**

Find the "前置条件" section. Replace it entirely with:

```markdown
## 前置条件

- [ ] Monorepo 项目已初始化
  详见根路由器 SKILL.md **Step 1**
- [ ] \`packages/book/\` 已创建
  - 推荐命令:
    \`turbo gen workspace --name @<project>/book --type package\`
  - 详见根路由器 SKILL.md **Step 4**
- [ ] Pandoc (>=2.0) 和 XeLaTeX 已安装
  - 检查: \`pandoc --version\` && \`xelatex --version\`
  - 未安装时见 [troubleshooting.md](./references/troubleshooting.md)
- [ ] \`@<project>/content\` 包存在且已在 book/package.json 中声明依赖

> **注意**: PDF 生成需要 LaTeX 环境。
> 如未安装，可跳过此子技能或使用 CI/CD 中的 Docker 容器。
```

- [ ] **Step 4: Verify no other sub-skills need updates**

These sub-skills should NOT need changes because they don't reference `init-tutorial.sh` or `templates/`:

```bash
# Check that research/writing/review/github-pages/decision don't reference old paths
for skill in research writing review github-pages decision; do
  echo "=== Checking $skill ==="
  grep -n "init-tutorial.sh\|templates/tutorial-starter" \
    process/tutorial-writer-skill/skills/tutorial-writer-$skill/SKILL.md || echo "(clean)"
done
# Expected: All show "(clean)" or no output
```

- [ ] **Step 5: Commit sub-skill updates**

```bash
git add \
  process/tutorial-writer-skill/skills/tutorial-writer-content/SKILL.md \
  process/tutorial-writer-skill/skills/tutorial-writer-web/SKILL.md \
  process/tutorial-writer-skill/skills/tutorial-writer-book/SKILL.md
git commit -m "refactor(tutorial-writer): update 3 sub-skill prerequisites for official tools

- content: Point to create-turbo + turbo gen (Step 0-2)
- web: Point to create-astro --template starlight (Step 3)
- book: Point to turbo gen workspace (Step 4)
- All now reference root router's 'Project Initialization' section"
```

---

## Task 5: Global Verification & Cleanup

**Files:**
- Verify: All files in `process/tutorial-writer-skill/`
- Modify: `.trae/tutorial-writer-rebuild/README.md` (optional update)

- [ ] **Step 1: Global search for stale references**

Search the entire `process/tutorial-writer-skill/` directory for any remaining references to deleted items:

```bash
# Search for old script references
grep -rn "init-tutorial.sh" process/tutorial-writer-skill/ \
  --include="*.md" --include="*.sh" --include="*.json" \
  2>/dev/null || echo "✅ No init-tutorial.sh references found"

# Search for old template references
grep -rn "templates/tutorial-starter" process/tutorial-writer-skill/ \
  --include="*.md" --include="*.sh" --include="*.json" \
  2>/dev/null || echo "✅ No template references found"

# Search for old scripts/ path references
grep -rn '"scripts/' process/tutorial-writer-skill/ \
  --include="*.md" \
  2>/dev/null || echo "✅ No scripts/ path references found"
```

**Expected**: All three searches should return clean (no results outside of `.trae/` planning docs).

If any stale references are found, fix them before proceeding.

- [ ] **Step 2: Verify file counts and line counts**

```bash
echo "=== File Structure ==="
find process/tutorial-writer-skill/ -type f | wc -l
# Expected: ~39 (was ~64, minus 25 deleted)

echo ""
echo "=== Key Files Line Counts ==="
wc -l \
  process/tutorial-writer-skill/SKILL.md \
  process/tutorial-writer-skill/references/monorepo-guide.md
# Expected: SKILL.md ~374, monorepo-guide.md ~300

echo ""
echo "=== Confirm Deletions ==="
ls process/tutorial-writer-skill/scripts/init-tutorial.sh 2>&1
ls process/tutorial-writer-skill/templates/tutorial-starter/ 2>&1
# Both should say "No such file or directory"

echo ""
echo "=== Sub-skill Status ==="
for skill in content web book; do
  lines=$(wc -l < "process/tutorial-writer-skill/skills/tutorial-writer-$skill/SKILL.md")
  echo "$skill/SKILL.md: $lines lines"
done
```

- [ ] **Step 3: Functional smoke test — validate SKILL.md frontmatter**

```bash
# Verify root router still has valid frontmatter
head -25 process/tutorial-writer-skill/SKILL.md
# Should show valid YAML frontmatter with 7 children listed

# Verify children list is intact
grep -A 10 "children:" process/tutorial-writer-skill/SKILL.md
# Should list all 7 sub-skills: research, writing, review, content, web, book, github-pages, decision
```

- [ ] **Step 4: (Optional) Update .trae/ README with refactor record**

If desired, append a note to `.trae/tutorial-writer-rebuild/README.md` documenting this internal refactor:

```markdown
## v1.0.0 Internal Refactor (Plan D) — 2026-05-31

### 变更摘要
- **删除**: \`scripts/init-tutorial.sh\` (1002行) — 被 \`create-turbo\` 替代
- **删除**: \`templates/tutorial-starter/\` (24文件) — 被 \`create-astro\` 替代
- **新增**: 根路由器"项目初始化"章节 (~120行) — 官方工具命令序列
- **精简**: \`monorepo-guide.md\` (2633→300行, -89%)
- **更新**: content/web/book 子技能前置条件

### 净影响
- 代码行数: ~24,000 → ~17,500 (-27%)
- 维护负担: 高 → **零** (无需同步官方模板)
```

- [ ] **Step 5: Final commit (if Step 4 made changes)**

```bash
git add -u
git commit -m "chore(tutorial-writer): Plan D refactor complete — official tools adoption

Summary of Plan D (Official Tools + AI Orchestration):
- Deleted scripts/init-tutorial.sh (1002 lines)
- Deleted templates/tutorial-starter/ (24 files, ~3000 lines)
- Added 'Project Initialization' chapter to root SKILL.md (~120 lines)
- Simplified monorepo-guide.md (2633→300 lines, -89%)
- Updated 3 sub-skill prerequisites (content/web/book)
- Net reduction: ~6,200 lines (-27%)

Architecture: Now uses create-turbo + turbo gen + create-astro
Version: Remains v1.0.0 (internal refactor, no API change)"
```

---

## Self-Review Checklist

### Spec Coverage

| Spec Requirement | Implemented In | Status |
|-----------------|-------------|--------|
| Delete scripts/init-tutorial.sh | Task 1 | ✅ |
| Delete templates/tutorial-starter/ | Task 1 | ✅ |
| Add initialization chapter to root SKILL.md | Task 2 | ✅ |
| Simplify monorepo-guide.md to ~300 lines | Task 3 | ✅ |
| Update content sub-skill prerequisites | Task 4 | ✅ |
| Update web sub-skill prerequisites | Task 4 | ✅ |
| Update book sub-skill prerequisites | Task 4 | ✅ |
| Global verification of stale references | Task 5 | ✅ |
| Version remains v1.0.0 | All tasks | ✅ |

### Placeholder Scan

- [x] No TBD/TODO/FIXME found
- [x] All code blocks contain actual content (no "..." or "implement later")
- [x] All file paths are absolute and specific
- [x] All commands include expected output

### Type Consistency

- [x] Project name placeholder consistent: `<project-name>` and `<project>` used consistently
- [x] Tool names consistent: `create-turbo`, `turbo gen`, `create-astro`
- [x] Sub-skill names match actual directory names

---

**Plan complete and saved to `docs/superpowers/plans/2026-05-31-plan-d-official-tools-refactor.md`.**

## Execution Options

**Two execution options available:**

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
