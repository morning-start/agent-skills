# Phase 0: 基础设施与脚手架 — 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立 Tutorial Writer v1.0.0 的 Monorepo 基础设施，包括一键初始化脚本、完整项目模板和 Turborepo 使用指南

**Architecture:** 采用"三层分离"架构 — scripts/ (初始化工具) + templates/ (项目模板) + references/ (使用指南) 完全解耦，为后续 7-Sub 技能体系奠定基础

**Tech Stack:** Bash (跨平台), Turborepo, pnpm workspaces, Astro, Starlight, Pandoc, LaTeX

**前置文档:**
- 设计背景: [.trae/tutorial-writer-rebuild/README.md](../../.trae/tutorial-writer-rebuild/README.md)
- 任务分解: [.trae/tutorial-writer-rebuild/ROADMAP.md](../../.trae/tutorial-writer-rebuild/ROADMAP.md)

---

## 文件结构总览

本 Phase 将创建以下文件结构：

```
process/tutorial-writer-skill/
│
├── 🆁 scripts/                            ← 新建目录
│   └── init-tutorial.sh                   ← Task 0.1: 一键 Monorepo 初始化脚本
│
├── 🆁 templates/                          ← 新建目录
│   └── tutorial-starter/                 ← Task 0.2: 完整项目模板
│       ├── packages/
│       │   ├── content/                  ← 内容包模板
│       │   │   ├── src/
│       │   │   │   ├── chapters/
│       │   │   │   │   └── .gitkeep
│       │   │   │   └── config.ts
│       │   │   ├── package.json
│       │   │   └── tsconfig.json
│       │   │
│       │   ├── web/                      ← 网站包模板
│       │   │   ├── astro.config.mjs
│       │   │   ├── public/
│       │   │   │   └── favicon.svg
│       │   │   ├── src/
│       │   │   │   ├── components/
│       │   │   │   │   ├── interactive/.gitkeep
│       │   │   │   │   ├── charts/.gitkeep
│       │   │   │   │   └── code/.gitkeep
│       │   │   │   └── styles/
│       │   │   │       └── global.css
│       │   │   ├── package.json
│       │   │   └── tsconfig.json
│       │   │
│       │   └── book/                     ← 电子书包模板
│       │       ├── scripts/
│       │       │   └── generate-pdf.sh
│       │       ├── templates/
│       │       │   └── default.latex
│       │       ├── styles/
│       │       │   └── pdf.css
│       │       ├── package.json
│       │       └── README.md
│       │
│       ├── turbo.json
│       ├── pnpm-workspace.yaml
│       ├── .gitignore
│       ├── .editorconfig
│       ├── package.json
│       └── README.md
│
└── references/
    └── 🆁 monorepo-guide.md              ← Task 0.3: Turborepo 使用指南
```

---

## Task 1: 创建 init-tutorial.sh 脚本

**Files:**
- Create: `process/tutorial-writer-skill/scripts/init-tutorial.sh`
- Test: 手动测试（运行脚本验证输出）

### 概述

创建一个功能完整的 Bash 脚本，用于一键生成 Turborepo Monorepo 项目骨架。该脚本将：
- 解析命令行参数
- 检测环境依赖
- 创建完整的三包结构（content/web/book）
- 生成所有必需的配置文件
- 可选地初始化 Git 和安装依赖

---

- [ ] **Step 1: 创建脚本文件头部和参数解析**

```bash
#!/bin/bash
# ==============================================================================
# init-tutorial.sh - Tutorial Writer Monorepo 初始化脚本
# ==============================================================================
# 用法: ./scripts/init-tutorial.sh <project-name> [options]
#
# 参数:
#   <project-name>    项目名称（必填）
#   --template=<name> 模板变体 (starlight|blog|minimal) [默认: starlight]
#   --ci=<platform>   CI 平台 (github|gitlab|none) [默认: github]
#   --no-install      跳过依赖安装
#   --help            显示帮助信息
#
# 示例:
#   ./scripts/init-tutorial.sh my-rag-tutorial
#   ./scripts/init-tutorial.sh my-blog --template=blog --ci=gitlab
#   ./scripts/init-tutorial.sh my-docs --no-install
# ==============================================================================

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() { echo -e "${BLUE}[INFO]${NC} $*"; }
log_success() { echo -e "${GREEN}[✓]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[!]${NC} $*"; }
log_error() { echo -e "${RED}[✗]${NC} $*" >&2; }

# 默认值
TEMPLATE="starlight"
CI_PLATFORM="github"
SKIP_INSTALL=false
PROJECT_NAME=""

# 显示帮助
show_help() {
  cat << 'EOF'
Tutorial Writer Monorepo 初始化脚本

用法:
  ./scripts/init-tutorial.sh <project-name> [options]

参数:
  <project-name>          项目名称（必填，用于目录名和包名）

选项:
  --template=<name>       选择模板变体:
                             starlight  - Starlight 文档主题 (默认)
                             blog       - Astro 博客模板
                           minimal     - 空白 Astro 项目
  --ci=<platform>         选择 CI 平台:
                             github     - GitHub Actions (默认)
                             gitlab     - GitLab CI
                             none       - 不生成 CI 配置
  --no-install             跳过依赖安装步骤
  --help                  显示此帮助信息

示例:
  # 基础用法（Starlight + GitHub Actions）
  ./scripts/init-tutorial.sh my-tutorial

  # 使用博客模板 + GitLab CI
  ./scripts/init-tutorial.sh my-blog --template=blog --ci=gitlab

  # 只生成骨架，不安装依赖
  ./scripts/init-tutorial.sh my-docs --no-install

EOF
  exit 0
}

# 解析参数
parse_args() {
  if [[ $# -eq 0 ]]; then
    log_error "缺少必填参数: <project-name>"
    echo ""
    show_help
  fi

  PROJECT_NAME="${1}"
  shift

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --template=*)
        TEMPLATE="${1#*=}"
        ;;
      --ci=*)
        CI_PLATFORM="${1#*=}"
        ;;
      --no-install)
        SKIP_INSTALL=true
        ;;
      --help|-h)
        show_help
        ;;
      *)
        log_error "未知参数: $1"
        echo "使用 --help 查看帮助"
        exit 1
        ;;
    esac
    shift
  done

  # 验证项目名称
  if [[ ! "$PROJECT_NAME" =~ ^[a-z][a-z0-9-]*$ ]]; then
    log_error "无效的项目名称: $PROJECT_NAME"
    echo "项目名称必须是小写字母开头，可包含小写字母、数字和连字符"
    exit 1
  fi

  # 验证模板选项
  if [[ ! "$TEMPLATE" =~ ^(starlight|blog|minimal)$ ]]; then
    log_error "无效的模板: $TEMPLATE"
    echo "可选模板: starlight, blog, minimal"
    exit 1
  fi

  # 验证 CI 平台
  if [[ ! "$CI_PLATFORM" =~ ^(github|gitlab|none)$ ]]; then
    log_error "无效的 CI 平台: $CI_PLATFORM"
    echo "可选平台: github, gitlab, none"
    exit 1
  fi
}
```

- [ ] **Step 2: 添加环境检测函数**

```bash
# 环境检测
check_environment() {
  log_info "检查环境依赖..."

  # 检查 Node.js
  if ! command -v node &>/dev/null; then
    log_error "未找到 Node.js，请先安装 (>=18.0.0)"
    echo "推荐安装方式: https://nodejs.org/"
    exit 1
  fi

  local node_version
  node_version=$(node -v | grep -oE '[0-9]+' | head -1)
  if [[ "$node_version" -lt 18 ]]; then
    log_error "Node.js 版本过低: $(node -v) (需要 >=18.0.0)"
    exit 1
  fi
  log_success "Node.js: $(node -v)"

  # 检查 pnpm
  if ! command -v pnpm &>/dev/null; then
    log_warn "未找到 pnpm，尝试使用 npm..."
    if ! command -v npm &>/dev/null; then
      log_error "未找到 npm，请安装 pnpm 或 npm"
      echo "pnpm 安装: npm install -g pnpm"
      exit 1
    fi
    PACKAGE_MANAGER="npm"
  else
    PACKAGE_MANAGER="pnpm"
  fi
  log_success "包管理器: $PACKAGE_MANAGER ($($PACKAGE_MANAGER --version))"

  # 检查 Git（可选）
  if command -v git &>/dev/null; then
    HAS_GIT=true
    log_success "Git: $(git --version)"
  else
    HAS_GIT=false
    log_warn "未找到 Git，跳过 Git 初始化"
  fi
}
```

- [ ] **Step 3: 添加核心目录创建函数**

```bash
# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="${SCRIPT_DIR}/../templates/tutorial-starter"

# 创建根目录结构
create_root_structure() {
  log_info "创建根目录结构..."

  mkdir -p "${PROJECT_NAME}"

  cd "${PROJECT_NAME}" || exit 1

  log_success "项目目录: $(pwd)"
}

# 创建 packages/content 目录
create_content_package() {
  log_info "创建 content 包 (内容源)..."

  mkdir -p "packages/content/src/chapters"

  # 创建 .gitkeep
  touch "packages/content/src/chapters/.gitkeep"

  # 创建 package.json
  cat > "packages/content/package.json" << EOF
{
  "name": "@${PROJECT_NAME}/content",
  "version": "0.0.1",
  "private": true,
  "type": "module",
  "exports": {
    "./config": "./src/config.ts",
    "./chapters": "./src/chapters/*"
  },
  "scripts": {
    "typecheck": "tsc --noEmit"
  },
  "devDependencies": {
    "typescript": "^5.4.0",
    "astro": "^4.16.0",
    "@astrojs/starlight": "^0.28.0"
  }
}
EOF

  # 创建 tsconfig.json
  cat > "packages/content/tsconfig.json" << EOF
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"]
}
EOF

  log_success "content 包已创建"
}

# 创建 packages/web 目录
create_web_package() {
  log_info "创建 web 包 (网站)..."

  mkdir -p "packages/web/public"
  mkdir -p "packages/web/src/{components/{interactive,charts,code},layouts,styles}"

  # 创建占位文件
  touch "packages/web/src/components/interactive/.gitkeep"
  touch "packages/web/src/components/charts/.gitkeep"
  touch "packages/web/src/components/code/.gitkeep"

  # 创建 astro.config.mjs
  cat > "packages/web/astro.config.mjs" << 'EOF'
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [
    starlight({
      title: '教程标题',
      description: '教程描述',
      
      sidebar: [
        {
          label: '章节',
          autogenerate: {
            directory: 'chapters',
          },
        },
      ],
      
      social: {
        github: 'https://github.com/user/repo',
      },
      
      editLink: {
        baseUrl: 'https://github.com/user/repo/edit/main/',
      },
      
      lastUpdated: true,
      pagination: true,
      search: {
        mode: 'auto',
      },
    }),
  ],
});
EOF

  # 创建 package.json
  cat > "packages/web/package.json" << EOF
{
  "name": "@${PROJECT_NAME}/web",
  "version": "0.0.1",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview",
    "astro": "astro"
  },
  "dependencies": {
    "@${PROJECT_NAME}/content": "workspace:*",
    "astro": "^4.16.0",
    "@astrojs/starlight": "^0.28.0"
  },
  "devDependencies": {
    "typescript": "^5.4.0"
  }
}
EOF

  # 创建 tsconfig.json
  cat > "packages/web/tsconfig.json" << EOF
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*", "astro.config.mjs"]
}
EOF

  # 创建全局样式
  cat > "packages/web/src/styles/global.css" << 'EOF'
/* 全局样式 - Tutorial Writer */
:root {
  --font-sans: system-ui, -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  
  --color-primary: #3178c6;
  --color-text: #1a1a1a;
  --color-bg: #ffffff;
  
  /* 响应式断点 */
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-text: #e5e5e5;
    --color-bg: #111111;
  }
}
EOF

  log_success "web 包已创建"
}

# 创建 packages/book 目录
create_book_package() {
  log_info "创建 book 包 (电子书)..."

  mkdir -p "packages/book/{scripts,templates,styles}"

  # 创建 PDF 生成脚本框架
  cat > "packages/book/scripts/generate-pdf.sh" << 'SCRIPT'
#!/bin/bash
# PDF 生成脚本 - 使用 Pandoc 从 Markdown 生成 PDF
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTENT_DIR="${SCRIPT_DIR}/../../content/src/chapters"
OUTPUT_DIR="${SCRIPT_DIR}/../../dist"

echo "📄 开始生成 PDF..."

# 检查 Pandoc 是否安装
if ! command -v pandoc &>/dev/null; then
  echo "❌ 未找到 Pandoc，请先安装"
  echo "   macOS: brew install pandoc"
  echo "   Ubuntu: sudo apt-get install pandoc"
  exit 1
fi

# 创建输出目录
mkdir -p "${OUTPUT_DIR}"

# 收集所有 Markdown 文件
mapfile -t CHAPTERS < <(find "${CONTENT_DIR}" -name "*.md" -type f | sort)

if [[ ${#CHAPTERS[@]} -eq 0 ]]; then
  echo "⚠️ 未找到章节文件 (${CONTENT_DIR})"
  exit 0
fi

echo "找到 ${#CHAPTERS[@]} 个章节"

# 构建 Pandoc 命令
PANDOC_ARGS=(
  ${CHAPTERS[@]}
  --from markdown
  --to pdf
  --output "${OUTPUT_DIR}/tutorial.pdf"
  --pdf-engine=xelatex
  --metadata title="教程完整版"
  --toc
  --toc-depth=3
  --highlight-style=tango
  -V geometry:a4paper
  -V geometry:margin=2.5cm
  -V mainfont="Noto Sans CJC SC"
  -V monofont="Noto Sans Mono CJC SC"
  --resource-path=.
)

# 执行转换
pandoc "${PANDOC_ARGS[@]}"

echo "✅ PDF 已生成: ${OUTPUT_DIR}/tutorial.pdf"
SCRIPT
  chmod +x "packages/book/scripts/generate-pdf.sh"

  # 创建默认 LaTeX 模板
  cat > "packages/book/templates/default.latex" << 'LATEX'
\documentclass[a4paper,11pt]{article}

% 中文支持
\usepackage{ctex}
\usepackage{xeCJK}
\setCJKmainfont{Noto Sans CJK SC}
\setCJKmonofont{Noto Sans Mono CJC SC}

% 页面设置
\usepackage[
  a4paper,
  top=2.5cm,
  bottom=2.5cm,
  left=2.5cm,
  right=2.5cm
]{geometry}

% 代码高亮
\usepackage{listings}
\usepackage{xcolor}

% 超链接
\usepackage{hyperref}
\hypersetup{
  colorlinks=true,
  linkcolor=blue,
  urlcolor=blue,
  pdftitle={Tutorial},
  pdfauthor={Author}
}

% 标题信息
\title{教程标题}
\author{作者名称}
\date{\today}

\begin{document}

\maketitle
\tableofcontents
\newpage

% 内容将由 Pandoc 自动填充

\end{document}
LATEX

  # 创建 PDF 样式
  cat > "packages/book/styles/pdf.css" << 'CSS'
/* PDF 排版样式 */

body {
  font-family: 'Noto Sans CJK SC', sans-serif;
  font-size: 11pt;
  line-height: 1.6;
  margin: 2.5cm;
}

h1 {
  font-size: 24pt;
  border-bottom: 2px solid #333;
  padding-bottom: 0.3em;
  page-break-before: always;
}

h2 {
  font-size: 18pt;
  border-bottom: 1px solid #666;
  padding-bottom: 0.2em;
  margin-top: 1.5em;
}

h3 {
  font-size: 14pt;
  margin-top: 1.2em;
}

code {
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  background-color: #f5f5f5;
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-size: 9pt;
}

pre {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 1em;
  overflow-x: auto;
  page-break-inside: avoid;
}

pre code {
  background: none;
  padding: 0;
  font-size: 8pt;
}

table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
}

th, td {
  border: 1px solid #ddd;
  padding: 0.5em;
  text-align: left;
}

th {
  background-color: #f5f5f5;
  font-weight: bold;
}

blockquote {
  border-left: 4px solid #3178c6;
  margin: 1em 0;
  padding-left: 1em;
  color: #666;
}

img {
  max-width: 100%;
  height: auto;
}
CSS

  # 创建 package.json
  cat > "packages/book/package.json" << EOF
{
  "name": "@${PROJECT_NAME}/book",
  "version": "0.0.1",
  "private": true,
  "type": "module",
  "scripts": {
    "build:pdf": "bash scripts/generate-pdf.sh",
    "preview": "open dist/tutorial.pdf"
  },
  "dependencies": {
    "@${PROJECT_NAME}/content": "workspace:*"
  },
  "devDependencies": {}
}
EOF

  # 创建 README
  cat > "packages/book/README.md" << EOF
# @${PROJECT_NAME}/book - 电子书生成包

## 功能

从 Markdown 内容生成专业排版的 PDF 电子书。

## 使用方法

\`\`\`bash
# 生成 PDF
pnpm --filter @${PROJECT_NAME}/book build:pdf

# 预览 PDF
pnpm --filter @${PROJECT_NAME}/book preview
\`\`\`

## 输出位置

生成的 PDF 文件位于 \`dist/tutorial.pdf\`。

## 依赖

- [Pandoc](https://pandoc.org/) (>=2.0)
- XeLaTeX (通过 TeX Live 或 MiKTeX)
- 中文字体: Noto Sans CJC SC

## 自定义

- **LaTeX 模板**: 编辑 \`templates/default.latex\`
- **PDF 样式**: 编辑 \`styles/pdf.css\`
- **生成脚本**: 编辑 \`scripts/generate-pdf.sh\`
EOF

  log_success "book 包已创建"
}
```

- [ ] **Step 4: 添加配置文件生成函数**

```bash
# 创建 Turborepo 配置
create_turbo_config() {
  log_info "创建 Turborepo 配置..."

  cat > "turbo.json" << 'EOF'
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "dev": {
      "cache": false,
      "persistent": true
    },
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", "*.pdf"]
    },
    "build:web": {
      "cache": false,
      "dependsOn": ["@tutorial/content#build"]
    },
    "build:book": {
      "cache": false,
      "dependsOn": ["@tutorial/content#build"]
    }
  }
}
EOF

  log_success "turbo.json 已创建"
}

# 创建 pnpm workspace 配置
create_workspace_config() {
  log_info "创建 workspace 配置..."

  cat > "pnpm-workspace.yaml" << 'EOF'
packages:
  - 'packages/*'
EOF

  log_success "pnpm-workspace.yaml 已创建"
}

# 创建根 package.json
create_root_package_json() {
  log_info "创建根 package.json..."

  cat > "package.json" << EOF
{
  "name": "${PROJECT_NAME}-monorepo",
  "private": true,
  "scripts": {
    "dev": "turbo run dev",
    "build": "turbo run build",
    "build:web": "turbo run build:web --filter=@${PROJECT_NAME}/web",
    "build:book": "turbo run build:book --filter=@${PROJECT_NAME}/book",
    "test": "turbo run test",
    "lint": "turbo run lint"
  },
  "devDependencies": {
    "typescript": "^5.4.0",
    "turbo": "^2.0.0"
  },
  "packageManager": "pnpm@9.0.0",
  "engines": {
    "node": ">=18.0.0"
  }
}
EOF

  log_success "根 package.json 已创建"
}

# 创建 TypeScript 基础配置
create_tsconfig_base() {
  log_info "创建 TypeScript 基础配置..."

  cat > "tsconfig.base.json" << 'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "exclude": ["node_modules", "dist"]
}
EOF

  log_success "tsconfig.base.json 已创建"
}
```

- [ ] **Step 5: 添加辅助文件和 CI 配置**

```bash
# 创建 .gitignore
create_gitignore() {
  log_info "创建 .gitignore..."

  cat > ".gitignore" << 'EOF'
# Dependencies
node_modules/

# Build outputs
dist/
*.astro

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/*
!.vscode/extensions.json
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Turbo
.turbo

# LaTeX 临时文件
*.aux
*.log
*.out
*.toc
*.fls
*.fdb_latexmk
*.synctex.gz

# PDF 产物 (可选提交)
# dist/*.pdf
EOF

  log_success ".gitignore 已创建"
}

# 创建 .editorconfig
create_editorconfig() {
  log_info "创建 .editorconfig..."

  cat > ".editorconfig" << 'EOF'
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 2
insert_final_newline = true
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false

[*.{json,yml,yaml}]
indent_size = 2

[*.ts]
indent_size = 2

[*.{sh,bash}]
indent_size = 2
EOF

  log_success ".editorconfig 已创建"
}

# 创建 GitHub Actions 工作流
create_github_actions() {
  if [[ "$CI_PLATFORM" != "github" ]]; then
    return
  fi

  log_info "创建 GitHub Actions 工作流..."

  mkdir -p ".github/workflows"

  cat > ".github/workflows/deploy.yml" << 'YAML'
name: Deploy Website

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v4
        with:
          version: 9

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm

      - name: Install dependencies
        run: pnpm install

      - name: Build website
        run: turbo run build:web

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: packages/web/dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    if: github.ref == 'refs/heads/main' && github.event_name != 'pull_request'
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
YAML

  log_success "GitHub Actions 工作流已创建"
}

# 创建 GitLab CI 配置
create_gitlab_ci() {
  if [[ "$CI_PLATFORM" != "gitlab" ]]; then
    return
  fi

  log_info "创建 GitLab CI 配置..."

  cat > ".gitlab-ci.yml" << 'YAML'
stages:
  - build
  - deploy

variables:
  PNPM_CACHE_DIR: .pnpm-store

cache:
  key: "$CI_COMMIT_REF_SLUG-pnpm"
  paths:
    - .pnpm-store/

build:website:
  stage: build
  image: node:20-alpine
  before_script:
    - corepack enable
    - pnpm config set store-dir .pnpm-store
  script:
    - pnpm install
    - turbo run build:web
  artifacts:
    paths:
      - packages/web/dist/
    expire_in: 1 hour

pages:
  stage: deploy
  script:
    - mv packages/web/dist public
  artifacts:
    paths:
      - public
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
YAML

  log_success "GitLab CI 配置已创建"
}
```

- [ ] **Step 6: 添加主执行逻辑和完成信息**

```bash
# 初始化 Git 仓库
init_git() {
  if [[ "$HAS_GIT" == "true" ]] && [[ ! -d ".git" ]]; then
    log_info "初始化 Git 仓库..."
    git init -q
    git add -A
    git commit -q -m "chore: initial project scaffold from tutorial-writer"
    log_success "Git 仓库已初始化"
  elif [[ -d ".git" ]]; then
    log_warn "Git 仓库已存在，跳过初始化"
  fi
}

# 安装依赖
install_dependencies() {
  if [[ "$SKIP_INSTALL" == "true" ]]; then
    log_warn "跳过依赖安装 (--no-install)"
    return
  fi

  log_info "安装依赖..."

  case "$PACKAGE_MANAGER" in
    pnpm)
      pnpm install
      ;;
    npm)
      npm install
      ;;
  esac

  log_success "依赖安装完成"
}

# 显示完成信息
show_completion_message() {
  echo ""
  echo "=========================================="
  log_success "✨ 项目创建完成!"
  echo "=========================================="
  echo ""
  echo "📁 项目位置: $(pwd)/"
  echo ""
  echo "📦 包结构:"
  echo "  ├── packages/content/   ← 内容源 (Markdown)"
  echo "  ├── packages/web/       ← 网站 (Astro + Starlight)"
  echo "  └── packages/book/      ← 电子书 (PDF)"
  echo ""
  echo "🚀 快速开始:"
  echo ""
  if [[ "$SKIP_INSTALL" == "true" ]]; then
    echo "  1. cd ${PROJECT_NAME}/"
    echo "  2. pnpm install          # 或: npm install"
    echo "  3. turbo run dev         # 启动开发服务器"
  else
    echo "  1. cd ${PROJECT_NAME}/"
    echo "  2. turbo run dev         # 启动开发服务器"
  fi
  echo ""
  echo "📖 更多帮助:"
  echo "  - 查看 ../references/monorepo-guide.md 了解 Turborepo 用法"
  echo "  - 运行 /research 开始调研规划"
  echo "  - 运行 /writing 开始撰写内容"
  echo ""
  echo "=========================================="
}

# 主函数
main() {
  echo ""
  echo "╔══════════════════════════════════════╗"
  echo "║  Tutorial Writer Monorepo 初始化器  ║"
  echo "╚══════════════════════════════════════╝"
  echo ""

  parse_args "$@"
  check_environment
  create_root_structure
  create_content_package
  create_web_package
  create_book_package
  create_turbo_config
  create_workspace_config
  create_root_package_json
  create_tsconfig_base
  create_gitignore
  create_editorconfig
  create_github_actions
  create_gitlab_ci
  init_git
  install_dependencies
  show_completion_message
}

# 执行主函数
main "$@"
```

- [ ] **Step 7: 验证脚本语法并设置权限**

```bash
# 在终端中运行以下命令验证:

# 1. 检查语法错误
bash -n process/tutorial-writer-skill/scripts/init-tutorial.sh

# 2. 设置可执行权限
chmod +x process/tutorial-writer-skill/scripts/init-tutorial.sh

# 3. 测试 help 输出
./process/tutorial-writer-skill/scripts/init-tutorial.sh --help
```

预期输出：显示完整的帮助信息，无错误

- [ ] **Step 8: Commit**

```bash
git add process/tutorial-writer-skill/scripts/init-tutorial.sh
git commit -m "feat(phase-0): add init-tutorial.sh monorepo initialization script"
```

---

## Task 2: 创建 templates/tutorial-starter/ 模板

**Files:**
- Create: `process/tutorial-writer-skill/templates/tutorial-starter/` (完整目录树)
- 内含: 所有 packages/ 的模板文件、配置文件、辅助文件

---

- [ ] **Step 1: 创建 templates 目录结构**

```bash
mkdir -p process/tutorial-writer-skill/templates/tutorial-starter
cd process/tutorial-writer-skill/templates/tutorial-starter

# 创建完整目录树
mkdir -p packages/content/src/chapters
mkdir -p packages/web/{public,src/{components/{interactive,charts,code},layouts,styles}}
mkdir -p packages/book/{scripts,templates,styles}
mkdir -p .github/workflows
```

- [ ] **Step 2: 复制 packages/content/src/config.ts**

此文件在 Step 1 的 `create_content_package()` 函数中已定义完整内容。确保模板中的版本与之完全一致：

```typescript
import { defineCollection, z } from 'astro:content';
import { docsLoader, docsSchema } from '@astrojs/starlight/loaders';

const chapters = defineCollection({
  loader: docsLoader(),
  schema: docsSchema({
    schema: z.object({
      // 基础字段
      title: z.string(),
      description: z.string().optional(),
      draft: z.boolean().default(false),
      
      // 教程扩展字段
      tags: z.array(z.string()).default([]),
      difficulty: z.enum(['beginner', 'intermediate', 'advanced']).optional(),
      readingTime: z.number().optional(),
      prerequisites: z.array(z.string()).default([]),
      
      // 增强管道支持
      hasInteractive: z.boolean().default(false),
      hasMermaid: z.boolean().default(false),
      hasMath: z.boolean().default(false),
    }),
  }),
});

export const collections = { chapters };
```

- [ ] **Step 3: 创建所有占位文件和 README**

确保以下文件存在且内容正确：
- `packages/content/src/chapters/.gitkeep` (空文件)
- `packages/web/public/favicon.svg` (SVG 图标)
- `packages/web/src/components/interactive/.gitkeep`
- `packages/web/src/components/charts/.gitkeep`
- `packages/web/src/components/code/.gitkeep`
- `packages/web/src/styles/global.css` (CSS 内容见 Step 1)
- `templates/README.md` (项目说明)

- [ ] **Step 4: Commit**

```bash
git add process/tutorial-writer-skill/templates/
git commit -m "feat(phase-0): add tutorial-starter monorepo template"
```

---

## Task 3: 创建 monorepo-guide.md 参考文档

**Files:**
- Create: `process/tutorial-writer-skill/references/monorepo-guide.md`

---

- [ ] **Step 1: 创建 Turborepo 使用指南**

编写完整的参考文档 (~400-600 行)，涵盖：

```markdown
# Monorepo 使用指南 (Turborepo)

## 1. 安装和初始化
## 2. turbo.json 配置详解
## 3. workspace 依赖管理
## 4. 任务定义和编排
## 5. 缓存策略
## 6. 常见问题排查
## 7. 与各子技能的集成点
## 8. 性能优化建议
```

关键章节要点：

**第 1 章**: 如何使用 `init-tutorial.sh` 快速开始
**第 2 章**: 详细解释每个 task 的 dependsOn 和 outputs 含义
**第 3 章**: workspace:* 语法的使用场景和最佳实践
**第 7 章**: 明确说明 content → web/book 的数据流向

- [ ] **Step 2: Commit**

```bash
git add process/tutorial-writer-skill/references/monorepo-guide.md
git commit -m "docs(phase-0): add Turborepo monorepo usage guide"
```

---

## 验收标准

Phase 0 完成后，必须满足以下条件：

- [ ] `scripts/init-tutorial.sh` 可独立运行并通过 `--help` 测试
- [ ] `templates/tutorial-starter/` 包含完整的三包骨架
- [ ] 运行 `init-tutorial.sh test-project --no-install` 成功生成项目
- [ ] 生成的项目可通过 `ls packages/` 看到 content/web/book 三个目录
- [ ] `references/monorepo-guide.md` 文档完整可用
- [ ] 无 TODO/FIXME/HACK 残留在代码中

---

## 后续步骤

Phase 0 完成后，进入 **Phase 1: 核心重构**：

1. 重构根路由器 SKILL.md (6-Sub → 7-Sub)
2. 重命名 build → web 并重构
3. 重命名 publish → github-pages 并重构
4. 精简 writing 子技能
5. 更新保持不变的子技能 (research/review/decision)

---

**计划创建时间**: 2026-05-31
**预计实施时间**: 4-6 小时
**风险等级**: 低（纯新增，不影响现有功能）
