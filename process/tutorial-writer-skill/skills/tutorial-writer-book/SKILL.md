---
name: tutorial-writer-book
version: "1.0.0"
author: skill-factory
description: >
  Use when generating PDF or EPUB ebooks from Markdown content,
  configuring Pandoc conversion pipelines, creating LaTeX templates,
  or designing ebook typography and layout for Turborepo monorepo tutorial projects.
  Triggers on "PDF", "电子书", "Pandoc", "LaTeX", "ebook",
  "typography", "publishing", "offline reading".
tags: [pdf, epub, pandoc, latex, ebook, typography, publishing, offline, monorepo, format-output]
dependency:
  parent: tutorial-writer
  structure: "Type 3 (厚+references): 单文件 + 详细 references"
  pattern: "Format Producer"
meta:
  complexity: advanced
  standalone: true
  can_invoke_directly: true
  role: "format-producer-ebook"
  depends_on: ["init-script", "content-package"]
  input_source: "@tutorial/content"
  output_formats: ["pdf"]
---

# Tutorial Writer — 📚 电子书生成 v1.0.0

> **定位**: 电子书的出版商 (Format Producer - Ebook)
> **核心价值**: 将 Markdown 内容转换为专业排版的 PDF/EPUB 电子书
> **依赖**: @tutorial/content 包（唯一数据源）

## 📖 目录

- [快速启动](#快速启动)
- [PDF 生成（主力）](#pdf-生成主力)
- [EPUB 生成（可选）](#epub-生成可选)
- [LaTeX 模板管理](#latex-模板管理)
- [电子书样式](#电子书样式)
- [构建和预览](#构建和预览)
- [CI/CD 集成](#cicd-集成)
- [与其他子技能的关系](#与其他子技能的关系)
- [常见问题排查](#常见问题排查)
- [版本历史](#版本历史)

---

## 快速启动

## 前置条件

- [ ] Monorepo 项目已初始化
  详见根路由器 SKILL.md **Step 1**
- [ ] `packages/book/` 已创建
  - 推荐命令:
    `turbo gen workspace --name @<project>/book --type package`
  - 详见根路由器 SKILL.md **Step 4**
- [ ] Pandoc (>=2.0) 和 XeLaTeX 已安装
  - 检查: `pandoc --version` && `xelatex --version`
  - 未安装时见 [troubleshooting.md](./references/troubleshooting.md)
- [ ] `@<project>/content` 包存在且已在 book/package.json 中声明依赖

> **注意**: PDF 生成需要 LaTeX 环境。
> 如未安装，可跳过此子技能或使用 CI/CD 中的 Docker 容器。

### 第一个 PDF 生成示例

**最简命令**（使用默认配置）:

```bash
cd your-tutorial-project
pnpm --filter @tutorial/book build:pdf
```

**预期输出**:
```
📄 开始生成 PDF...
找到 5 个章节
✅ PDF 已生成: dist/tutorial.pdf
```

**手动执行 Pandoc 命令**（理解底层流程）:

```bash
pandoc \
  packages/content/src/chapters/*.md \
  --from markdown \
  --to pdf \
  --output dist/tutorial.pdf \
  --pdf-engine=xelatex \
  --metadata title="我的教程" \
  --toc \
  --toc-depth=3 \
  --highlight-style=tango \
  -V geometry:a4paper \
  -V geometry:margin=2.5cm \
  -V mainfont="Noto Sans CJK SC" \
  -V monofont="Noto Sans Mono CJK SC"
```

### 环境安装指南

#### macOS

```bash
# 安装 Homebrew（如果未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Pandoc
brew install pandoc

# 安装 TeX Live（完整版，约 4GB）
brew install --cask basictex  # 基础版（~100MB，够用）
# 或
brew install --cask mactex    # 完整版（推荐用于生产环境）

# 安装中文字体
brew install --cask font-noto-sans-cjk-sc
brew install --cask font-noto-mono-cjk-sc
```

#### Ubuntu/Debian

```bash
# 安装 Pandoc
sudo apt-get update
sudo apt-get install -y pandoc

# 安装 TeX Live（基础版 + XeLaTeX + 中文支持）
sudo apt-get install -y \
  texlive-xetex \
  texlive-lang-chinese \
  texlive-fonts-recommended

# 安装中文字体
sudo apt-get install -y fonts-noto-cjk
```

#### Windows

```powershell
# 使用 Chocolatey（推荐）
choco install pandoc -y
choco install miktex -y  # MiKTeX（自动按需安装包）

# 或使用 Scoop
scoop install pandoc
scoop install latex

# 手动下载中文字体
# 1. 访问 https://www.google.com/get/noto/help/cjk/
# 2. 下载 Noto Sans SC (OTF) 和 Noto Sans Mono CJK SC
# 3. 解压到 C:\Windows\Fonts\ 或用户字体目录
```

**验证安装**:

```bash
pandoc --version   # 应显示 >= 2.0
xelatex --version  # 应显示 XeTeX 版本信息
fc-list :lang=zh   # 列出中文字体（Linux/macOS）
```

---

## PDF 生成（主力） ⭐ 核心

### Pandoc 安装和配置

**Pandoc 是什么？**
> Universal document converter（通用文档转换器），支持 Markdown → PDF/HTML/DOCX/EPUB 等格式转换。

**为什么选择 Pandoc？**

| 特性 | Pandoc | 其他方案 |
|------|--------|---------|
| Markdown 支持 | ✅ 原生支持 | 需要插件 |
| 中文支持 | ✅ 通过 XeLaTeX | 配置复杂 |
| 代码高亮 | ✅ 内置主题 | 需要额外工具 |
| 数学公式 | ✅ LaTeX 渲染 | 有限支持 |
| 活跃维护 | ✅ 持续更新 | 维护状态不一 |

**Pandoc 核心参数说明**:

```bash
pandoc [INPUT_FILES...] [OPTIONS]
```

**常用选项速查表**:

| 参数 | 说明 | 示例 |
|------|------|------|
| `--from FORMAT` | 输入格式 | `--from markdown` |
| `--to FORMAT` | 输出格式 | `--to pdf` |
| `--output FILE` | 输出文件路径 | `--output dist/book.pdf` |
| `--pdf-engine ENGINE` | PDF 引擎 | `--pdf-engine=xelatex` |
| `--metadata KEY=VAL` | 元数据 | `--metadata title="教程"` |
| `--toc` | 生成目录 | （无参数） |
| `--toc-depth=N` | 目录深度 | `--toc-depth=3` |
| `-V KEY=VAL` | LaTeX 变量 | `-V geometry:a4paper` |
| `--highlight-style THEME` | 代码高亮主题 | `--highlight-style=tango` |
| `--resource-path=DIR` | 资源搜索路径 | `--resource-path=.` |

### XeLaTeX 引擎设置

**什么是 XeLaTeX？**
> 基于 Unicode 的 LaTeX 引擎，原生支持中文和现代字体。

**为什么不用 pdfLaTeX？**
- ❌ pdfLaTeX 不支持 UTF-8 中文
- ❌ 字体配置复杂（需要 CJK 宏包）
- ✅ XeLaTeX 原生 Unicode + 系统字体直接使用

**XeLaTeX 推荐发行版**:

| 发行版 | 平台 | 大小 | 适用场景 |
|--------|------|------|---------|
| **TeX Live** (Full) | 全平台 | ~4GB | 生产环境、完整功能 |
| **TeX Live** (Basic) | macOS | ~100MB | 快速开始、基础功能 |
| **MiKTeX** | Windows | 按需下载 | Windows 用户、自动包管理 |

**验证 XeLaTeX 可用性**:

```bash
# 测试编译简单文档
echo '\documentclass{article}\begin{document}测试\end{document}' > test.tex
xelatex test.tex
ls test.pdf  # 应该存在
rm test.*
```

### 中文字体配置

**默认字体方案**:

```latex
% packages/book/templates/default.latex
\usepackage{ctex}
\usepackage{xeCJK}

\setCJKmainfont{Noto Sans CJK SC}
\setCJKmonofont{Noto Sans Mono CJK SC}
```

**Pandoc 命令行字体设置**:

```bash
pandoc ... \
  -V mainfont="Noto Sans CJK SC" \        # 正文字体
  -V sansfont="Noto Sans CJK SC" \         # 无衬线字体
  -V monofont="Noto Sans Mono CJK SC" \    # 等宽字体（代码）
  -V CJKmainfont="Noto Serif CJK SC"       # CJK 主字体（可选）
```

**备选字体方案**（当 Noto 不可用时）:

| 场景 | 推荐字体 | 安装方式 |
|------|---------|---------|
| macOS | PingFang SC / STHeiti | 系统预装 |
| Windows | Microsoft YaHei | 系统预装 |
| Linux (Ubuntu) | Noto CJK SC / WenQuanYi | `apt install fonts-noto-cjk` |
| 学术论文 | Source Han Serif CN (思源宋体) | Adobe 开源 |

**字体回退策略**:

```bash
# 自动检测可用中文字体的脚本
if fc-list | grep -q "Noto Sans CJK SC"; then
  MAIN_FONT="Noto Sans CJK SC"
elif fc-list | grep -q "PingFang SC"; then
  MAIN_FONT="PingFang SC"
elif fc-list | grep -q "Microsoft YaHei"; then
  MAIN_FONT="Microsoft YaHei"
else
  echo "⚠️ 未找到合适的中文字体，请安装 Noto Sans CJK SC"
  exit 1
fi
```

### PDF 元数据

**元数据类型**:

| 字段 | 说明 | 示例 |
|------|------|------|
| `title` | 书籍标题 | `"RAG 实战指南"` |
| `author` | 作者姓名 | `"张三"` |
| `date` | 出版日期 | `"2026-05-31"` |
| `subtitle` | 副标题 | `"从入门到精通"` |
| `keywords` | 关键词 | `"RAG, AI, LLM"` |
| `description` | 描述 | `"全面介绍 RAG 技术的教程"` |

**设置元数据的 3 种方式**:

**方式 1: 命令行参数**:
```bash
pandoc ... \
  --metadata title="RAG 实战指南" \
  --metadata author="张三" \
  --metadata date="$(date +%Y-%m-%d)" \
  --metadata subtitle="从入门到精通"
```

**方式 2: YAML 头部**（在第一个 Markdown 文件开头）:
```yaml
---
title: "RAG 实战指南"
author: "张三"
date: 2026-05-31
subtitle: "从入门到精通"
keywords: [RAG, AI, LLM]
---

# 第一章
...
```

**方式 3: 元数据文件** (`metadata.yaml`):
```yaml
---
title: "RAG 实战指南"
author: "张三"
...
---
```
```bash
pandoc ... --metadata-file=metadata.yaml
```

**PDF 书签和属性**:

```bash
pandoc ... \
  --pdf-engine=xelatex \
  -V pdfauthor="张三" \
  -V pdftitle="RAG 实战指南" \
  -V pdfsubject="AI 教程" \
  -V pdfkeywords="RAG, AI, LLM" \
  -V pdfcreator="Tutorial Writer" \
  -V pdfproducer="Pandoc + XeLaTeX"
```

### 目录自动生成（TOC）配置

**基本 TOC 设置**:

```bash
pandoc ... \
  --toc \                    # 启用目录
  --toc-depth=3 \            # 目录深度（H1-H3）
  --number-sections          # 自动编号章节
```

**TOC 高级配置**:

```bash
# 自定义目录标题
pandoc ... --toc --toc-title="目 录"

# 只包含特定层级的标题
pandoc ... --toc-depth=2     # 仅 H1 和 H2

# 在特定位置插入目录（Markdown 中）
<!-- toc-start -->
<!-- toc-end -->

# 前言
...

<!-- TOC 将插入到这里 -->
```

**TOC 样式定制**（通过 LaTeX 模板）:

```latex
% 在 default.latex 中添加
\usepackage{tocloft}
\renewcommand{\contentsname}{目 录}           % 目录标题
\renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}}  % 点线连接
\setcounter{tocdepth}{3}                       % 显示到第 3 层
```

### 页面布局

**标准纸张尺寸**:

| 尺寸 | Pandoc 参数 | 用途 |
|------|------------|------|
| A4 | `-V geometry:a4paper` | 国际标准（默认） |
| Letter | `-V geometry:letterpaper` | 美国/加拿大 |
| Legal | `-V geometry:legalpaper` | 法律文档 |
| 自定义 | `-V geometry:paperwidth=20cm -V geometry:paperheight=28cm` | 特殊需求 |

**边距设置**:

```bash
# 统一边距
pandoc ... -V geometry:margin=2.5cm

# 分别设置四边
pandoc ... \
  -V geometry:top=2.5cm \
  -V geometry:bottom=2.5cm \
  -V geometry:left=2.5cm \
  -V geometry:right=2.5cm

# 不同页面的边距（需要 LaTeX 模板支持）
# 参见 references/latex-templates.md
```

**常见布局场景**:

**场景 1: 宽松阅读版**（适合大屏设备）:
```bash
pandoc ... \
  -V geometry:a4paper \
  -V geometry:margin=3cm \
  -V fontsize=12pt
```

**场景 2: 紧凑打印版**（节省纸张）:
```bash
pandoc ... \
  -V geometry:a4paper \
  -V geometry:margin=2cm \
  -V fontsize=10pt \
  -V linestretch=1.4
```

**场景 3: 双栏学术版**:
```bash
pandoc ... \
  -V geometry:twocolumn \
  -V geometry:columnsep=0.5cm
```

### 页眉页脚配置

**启用页眉页脚**:

```bash
pandoc ... \
  -V header-includes="\usepackage{fancyhdr}" \
  -V header-includes="\pagestyle{fancy}" \
  -V header-includes="\fancyhead[L]{\leftmark}" \
  -V header-includes="\fancyhead[R]{\thepage}" \
  -V header-includes="\fancyfoot[C]{\mytitle}"
```

**通过 LaTeX 模板配置**（推荐）:

```latex
% packages/book/templates/default.latex
\usepackage{fancyhdr}
\pagestyle{fancy}

% 页眉
\fancyhead[L]{\small\leftmark}      % 左侧：章节名
\fancyhead[R]{\small\thepage}       % 右侧：页码
\fancyfoot[C]{\small 我的教程}      % 页脚中央：书名

% 首页不显示页眉页脚
\fancypagestyle{plain}{
  \fancyhf{}
  \renewcommand{\headrulewidth}{0pt}
}
```

**页码样式**:

```bash
# 阿拉伯数字（默认）
-V fancyhdr[plain]  # 或在模板中设置

# 罗马数字（前言部分）
\pagenumbering{roman}

% 正文重新开始
\newpage
\pagenumbering{arabic}
\setcounter{page}{1}
```

### 代码高亮主题选择

**内置高亮主题列表**:

| 主题 | 风格 | 适用场景 |
|------|------|---------|
| `pygments` | 默认风格 | 通用 |
| `tango` | 彩色柔和 | 推荐（默认） |
| `espresso` | 深色背景 | 演示文稿 |
| `zenburn` | 暗色调 | 护眼模式 |
| `kate` | Kate 编辑器 | KDE 用户 |
| `monochrome` | 黑白 | 打印友好 |
| `haddock` | Haskell 风格 | 函数式编程 |
| `breezedark` | Breeze Dark | KDE Dark 主题 |

**应用主题**:

```bash
pandoc ... --highlight-style=tango
```

**自定义高亮样式**（高级用法）:

```bash
# 创建自定义主题文件 my-theme.theme
pandoc ... --highlight-style=my-theme.theme
```

**主题文件示例** (`tango-custom.theme`):
```text
{ "text-color": "#000000",
  "background-color": "#f8f8f8",
  "line-number-color": "#aaaaaa",
  "line-number-background-color": "#eeeeee"}
```

---

## EPUB 生成（可选）

> **当前版本状态**: v1.0.0 主要聚焦 PDF 生成
>
> **未来计划**: v1.1.0 将完善 EPUB 支持作为正式功能

### EPUB 元数据

**基本 EPUB 生成命令**:

```bash
pandoc chapters/*.md \
  --from markdown \
  --to epub \
  --output dist/tutorial.epub \
  --metadata title="教程名称" \
  --toc \
  --toc-depth=3 \
  --epub-cover-image=cover.jpg \
  --css=styles/epub.css
```

**EPUB 特有元数据**:

| 字段 | 说明 | 示例 |
|------|------|------|
| `identifier` | ISBN/唯一标识 | `"isbn:978-xxx"` |
| `language` | 语言代码 | `"zh-CN"` |
| `publisher` | 出版社 | `"自出版"` |
| `rights` | 版权声明 | `"CC BY-SA 4.0"` |
| `cover-image` | 封面图片 | `cover.jpg` |

### 封面图片处理

**封面图片要求**:

- 格式: JPG/PNG（推荐 JPG 以减小体积）
- 尺寸: 至少 1000×1600 像素（2:3 比例）
- 文件大小: < 500KB（推荐 < 200KB）
- 路径: 相对于 Markdown 文件的路径

**生成封面图片**（使用 ImageMagick）:

```bash
convert -size 1200x1920 xc:white \
  -gravity center -pointsize 72 -fill black \
  -annotate 0 "教程标题\n作者" \
  cover.jpg
```

### 章节划分规则

**EPUB 章节分割**:

```bash
# 每个 H1 开始新章节
pandoc ... --epub-chapter-level=1

# 每个 H2 也独立成章（适合长文档）
pandoc ... --epub-chapter-level=2
```

### CSS 样式定制

**EPUB CSS 文件** (`styles/epub.css`):

```css
body {
  font-family: 'Noto Sans CJK SC', serif;
  font-size: 1em;
  line-height: 1.6;
  margin: 1em;
}

h1 {
  font-size: 1.8em;
  page-break-before: always;
  border-bottom: 2px solid #333;
}

code {
  font-family: 'JetBrains Mono', monospace;
  background-color: #f5f5f5;
  padding: 0.2em 0.4em;
  border-radius: 3px;
}

pre {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  padding: 1em;
  overflow-x: auto;
  white-space: pre-wrap;
}
```

**应用自定义 CSS**:

```bash
pandoc ... --css=styles/epub.css
```

---

## LaTeX 模板管理

### 默认模板（适合技术教程）

**模板位置**: `packages/book/templates/default.latex`

**模板特点**:
- ✅ A4 纸张，11pt 字号
- ✅ 中文字体支持（ctex + xeCJK）
- ✅ 合理边距（2.5cm）
- ✅ 代码块语法高亮
- ✅ 超链接可点击
- ✅ 自动生成目录

**模板完整内容**:

```latex
\documentclass[a4paper,11pt]{article}

% ===== 中文支持 =====
\usepackage{ctex}
\usepackage{xeCJK}
\setCJKmainfont{Noto Sans CJK SC}
\setCJKmonofont{Noto Sans Mono CJK SC}

% ===== 页面布局 =====
\usepackage[
  a4paper,
  top=2.5cm,
  bottom=2.5cm,
  left=2.5cm,
  right=2.5cm
]{geometry}

% ===== 代码高亮 =====
\usepackage{listings}
\usepackage{xcolor}

% ===== 超链接 =====
\usepackage{hyperref}
\hypersetup{
  colorlinks=true,
  linkcolor=blue,
  urlcolor=blue,
  pdftitle={Tutorial},
  pdfauthor={Author}
}

% ===== 文档信息 =====
\title{教程标题}
\author{作者名称}
\date{\today}

\begin{document}

\maketitle
\tableofcontents
\newpage

% 内容将由 Pandoc 自动填充

\end{document}
```

### 模板参数说明

**如何自定义模板**:

**步骤 1: 复制默认模板**:
```bash
cp packages/book/templates/default.latex packages/book/templates/custom.latex
```

**步骤 2: 编辑模板**（根据需求修改参数）:

```latex
% 修改纸张尺寸
\documentclass[letterpaper,12pt]{article}

% 修改字体
\setCJKmainfont{Source Han Serif CN}  % 思源宋体

% 添加页码
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhead[R]{\thepage}

% 添加页眉图片
% \usepackage{background}
% \backgroundsetup{...}
```

**步骤 3: 使用自定义模板**:
```bash
pandoc ... --template=packages/book/templates/custom.latex
```

**常用模板修改点**:

| 修改项 | 位置 | 说明 |
|--------|------|------|
| 纸张尺寸 | `\documentclass[...]` | a4paper/letterpaper |
| 字号 | `\documentclass[...]` | 10pt/11pt/12pt |
| 主字体 | `\setCJKmainfont{}` | 更换中文字体 |
| 边距 | `geometry` 参数 | 调整页面边距 |
| 页眉页脚 | `fancyhdr` 包 | 添加页码/标题 |
| 行距 | `\linespread{1.5}` | 调整行间距 |
| 段落缩进 | `\parindent=2em` | 首行缩进 |

### 学术论文模板（可选扩展方向）

**适用场景**: 学位论文、期刊投稿、技术报告

**模板结构差异**:

```latex
% 学术论文模板
\documentclass[12pt,a4paper]{report}  % 使用 report 类

% 添加更多宏包
\usepackage{graphicx}        % 图片
\usepackage{float}           % 浮动体控制
\usepackage{amsmath}         % 数学公式
\usepackage{natbib}          % 参考文献
\usepackage{caption}         % 图表标题

% 添加摘要环境
\newenvironment{abstract}{...}

% 添加参考文献样式
\bibliographystyle{plain}
```

**何时考虑学术论文模板**:
- ✅ 目标是期刊或会议论文
- ✅ 需要严格的格式要求（如 IEEE/ACM 模板）
- ✅ 需要参考文献管理系统

**对于技术教程，默认模板已经足够！**

### 模板切换方法

**方法 1: 命令行指定**:
```bash
# 使用默认模板
pandoc ...

# 使用自定义模板
pandoc ... --template=packages/book/templates/custom.latex

# 不使用任何模板（完全由 Pandoc 控制）
pandoc ... --standalone
```

**方法 2: 配置文件管理** (`book-config.yaml`):

```yaml
template: packages/book/templates/default.latex
metadata:
  title: "教程名称"
  author: "作者"
layout:
  paper: a4paper
  margin: 2.5cm
  fontsize: 11pt
fonts:
  main: "Noto Sans CJK SC"
  mono: "Noto Sans Mono CJK SC"
```

**方法 3: 脚本封装** (`scripts/generate-pdf.sh`):

```bash
#!/bin/bash
TEMPLATE="${1:-default.latex}"

pandoc ... --template="packages/book/templates/${TEMPLATE}"
```

---

## 电子书样式 ⭐ 重要

### PDF 排版样式

**字体族配置**:

| 元素 | 推荐字体 | 备选字体 | 字号 |
|------|---------|---------|------|
| 正文 | Noto Sans CJK SC | PingFang SC | 11pt |
| 标题 | Noto Sans CJK SC (Bold) | Heiti SC | 24pt/18pt/14pt |
| 代码 | Noto Sans Mono CJK SC | JetBrains Mono | 9pt |
| 注释 | Noto Sans CJK SC (Light) | Kaiti SC | 9pt |

**字号层级**:

```latex
\titlespacing*{\section}{0pt}{12pt plus 2pt minus 2pt}{6pt plus 2pt minus 2pt}
\titlespacing*{\subsection}{0pt}{10pt plus 2pt minus 2pt}{4pt plus 2pt minus 2pt}
\titlespacing*{\subsubsection}{0pt}{8pt plus 2pt minus 2pt}{2pt plus 2pt minus 2pt}
```

**行距设置**:

| 场景 | 行距值 | Pandoc 参数 |
|------|--------|------------|
| 标准 | 1.6 | （默认） |
| 宽松 | 1.8 | `-V linestretch=1.8` |
| 紧凑 | 1.4 | `-V linestretch=1.4` |
| 双倍行距 | 2.0 | `-V linestretch=2.0` |

**段落间距和缩进**:

```latex
% 首行缩进 2 个字符
\setlength{\parindent}{2em}

% 段落间距
\setlength{\parskip}{0.5em}

% 标题前后间距
\titlespacing*{\section}{0pt}{1.5em}{0.8em}
```

### 代码块样式

**内联代码**:

```markdown
使用 `const app = express()` 创建应用。
```

**渲染效果**:
- 背景: #f5f5f5
- 内边距: 0.2em 0.4em
- 圆角: 3px
- 字号: 9pt（比正文小 2pt）

**代码块**:

```javascript
// JavaScript 示例
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(3000);
```

**代码块样式特性**:
- ✅ 语法高亮（Tango 主题）
- ✅ 背景色区分
- ✅ 等宽字体
- ✅ 避免跨页断行 (`page-break-inside: avoid`)
- ✅ 水平滚动条（超长代码）

**行号显示**（可选）:

```bash
pandoc ... --listings -V listings:numbers=left
```

**复制按钮**（PDF 不支持，仅 Web 可用）:
> PDF 是静态格式，不支持交互式元素。如需此功能，请使用 Web 格式。

### 表格样式

**基础表格**:

```markdown
| 功能 | Pandoc | 其他方案 |
|------|--------|---------|
| Markdown | ✅ 原生 | 需要插件 |
| 中文 | ✅ XeLaTeX | 配置复杂 |
```

**表格样式规则**:

| 样式元素 | 设置值 | 说明 |
|---------|--------|------|
| 边框 | 1px solid #ddd | 细线边框 |
| 斑马纹 | 奇数行背景 #f9f9f9 | 提升可读性 |
| 表头背景 | #f5f5f5 | 区分表头 |
| 内边距 | 0.5em | 舒适间距 |
| 对齐 | 左对齐（文本）/ 居中（数字） | 符合阅读习惯 |

**合并单元格**:

```markdown
| 列 1 | 列 2 | 列 3 |
|:-----|:-----|:-----|
| 跨 2 列 || 普通 |
| ^^^^ | 普通 | 普通 |
```

### 公式渲染

**行内公式**:

```markdown
爱因斯坦质能方程 $E = mc^2$
```

**块级公式**:

$$
\int_{-\infty}^{+\infty} e^{-x^2} dx = \sqrt{\pi}
$$

**公式渲染引擎**:

| 引擎 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **LaTeX（默认）** | 最高质量 | 需要 XeLaTeX | ⭐⭐⭐⭐⭐ |
| MathJax | 交互式 | 仅 HTML/EPUB | ⭐⭐⭐ |
| KaTeX | 快速渲染 | 功能有限 | ⭐⭐⭐ |

**复杂数学公式示例**:

$$
\mathcal{L}(\theta) = -\frac{1}{N} \sum_{i=1}^{N} \left[ y_i \log(\hat{y}_i) + (1-y_i) \log(1-\hat{y}_i) \right]
$$

### 打印优化

**分页控制**:

```markdown
<!-- 强制分页 -->
\newpage

<!-- 避免在此处分页 -->
<!-- 可能需要在 LaTeX 模板中配置 -->
```

**避免孤行和寡行** (Widow/Orphan Control):

```latex
% 在 default.latex 中添加
\usepackage[all]{nowidow}
\widowpenalty=1000
\clubpenalty=1000
```

**图片优化**:

```markdown
![架构图](images/architecture.png){ width=80% }
```

**打印友好的颜色方案**:

```css
@media print {
  body {
    color: #000;
    background: #fff;
  }
  
  a {
    color: #000;
    text-decoration: underline;
  }
  
  code {
    background: #f0f0f0;
    border: 1px solid #ccc;
  }
}
```

---

## 构建和预览

### 本地 PDF 预览

**方法 1: 使用脚本**:
```bash
pnpm --filter @tutorial/book preview
# 自动打开 dist/tutorial.pdf
```

**方法 2: 手动打开**:
```bash
# macOS
open dist/tutorial.pdf

# Linux (xdg-open)
xdg-open dist/tutorial.pdf

# Windows (start)
start dist/tutorial.pdf

# 使用 VS Code 扩展
code dist/tutorial.pdf  # 需要 PDF 预览扩展
```

**实时预览工作流**:

```bash
# 终端 1: 监听文件变化并自动重建
while true; do
  inotifywait -r -e modify packages/content/src/chapters/
  pnpm --filter @tutorial/book build:pdf
done

# 终端 2: 编辑 Markdown 文件
# 每次保存后自动重新生成 PDF
```

### 增量构建

**原理**: 只重新编译发生变化的章节

**实现方式**:

**方式 1: 文件时间戳对比**:

```bash
#!/bin/bash
CONTENT_DIR="packages/content/src/chapters"
OUTPUT_PDF="dist/tutorial.pdf"
CACHE_FILE=".build-cache"

if [ -f "$CACHE_FILE" ]; then
  CHANGED_FILES=$(find "$CONTENT_DIR" -name "*.md" -newer "$CACHE_FILE")
else
  CHANGED_FILES=$(find "$CONTENT_DIR" -name "*.md")
fi

if [ -z "$CHANGED_FILES" ]; then
  echo "✅ 无变化，跳过构建"
  exit 0
fi

echo "📝 变更文件:"
echo "$CHANGED_FILES"

# 执行全量构建（Pandoc 不支持真正的增量编译）
pandoc $(find "$CONTENT_DIR" -name "*.md" | sort) ... -o "$OUTPUT_PDF"

touch "$CACHE_FILE"
echo "✅ 构建完成"
```

**方式 2: Turborepo 缓存**:

```json
{
  "tasks": {
    "build:book": {
      "dependsOn": ["@tutorial/content#build"],
      "outputs": ["dist/**/*.pdf"],
      "inputs": ["packages/content/src/chapters/**/*.md"]
    }
  }
}
```

### 批量生成

**全量 PDF 生成**:

```bash
# 生成单个 PDF（包含所有章节）
pnpm --filter @tutorial/book build:pdf

# 输出: dist/tutorial.pdf
```

**分卷生成**（大型教程）:

```bash
#!/bin/bash
# scripts/generate-volumes.sh

VOLUME_1_CHAPTERS=$(ls packages/content/src/chapters/[0-3]*.md)
VOLUME_2_CHAPTERS=$(ls packages/content/src/chapters/[4-6]*.md)
VOLUME_3_CHAPTERS=$(ls packages/content/src/chapters/[7-9]*.md)

pandoc $VOLUME_1_CHAPTERS ... -o "dist/volume-1-基础篇.pdf"
pandoc $VOLUME_2_CHAPTERS ... -o "dist/volume-2-进阶篇.pdf"
pandoc $VOLUME_3_CHAPTERS ... -o "dist/volume-3-实战篇.pdf"
```

**多格式同时生成**:

```bash
#!/bin/bash
CHAPTERS=$(find packages/content/src/chapters -name "*.md" | sort)

# PDF
pandoc $CHAPTERS --to pdf -o dist/tutorial.pdf &

# EPUB（如果支持）
pandoc $CHAPTERS --to epub -o dist/tutorial.epub &

# Word（可选）
pandoc $CHAPTERS --to docx -o dist/tutorial.docx &

wait
echo "✅ 所有格式生成完毕"
```

### 质量检查

**自动化检查脚本** (`scripts/check-pdf-quality.sh`):

```bash
#!/bin/bash
PDF_FILE="${1:-dist/tutorial.pdf}"

if [ ! -f "$PDF_FILE" ]; then
  echo "❌ PDF 文件不存在: $PDF_FILE"
  exit 1
fi

echo "📊 PDF 质量检查报告"
echo "===================="

# 文件大小检查
FILE_SIZE=$(stat -f%z "$PDF_FILE" 2>/dev/null || stat -c%s "$PDF_FILE")
FILE_SIZE_MB=$(echo "scale=2; $FILE_SIZE / 1048576" | bc)
echo "📁 文件大小: ${FILE_SIZE_MB} MB"

if (( $(echo "$FILE_SIZE_MB > 50" | bc -l) )); then
  echo "⚠️ 文件过大，建议压缩图片"
fi

# 页数检查（需要 pdfinfo 工具）
if command -v pdfinfo &>/dev/null; then
  PAGE_COUNT=$(pdfinfo "$PDF_FILE" | grep Pages | awk '{print $2}')
  echo "📄 总页数: ${PAGE_COUNT}"
  
  if [ "$PAGE_COUNT" -lt 5 ]; then
    echo "⚠️ 页数过少，可能缺少内容"
  fi
fi

# 元数据检查
if command -v pdfinfo &>/dev/null; then
  TITLE=$(pdfinfo "$PDF_FILE" | grep Title | awk -F: '{print $2}' | xargs)
  AUTHOR=$(pdfinfo "$PDF_FILE" | grep Author | awk -F: '{print $2}' | xargs)
  echo "📝 标题: ${TITLE:-未设置}"
  echo "✍️ 作者: ${AUTHOR:-未设置}"
fi

# 图片完整性检查（需要 pdftoppm）
if command -v pdftoppm &>/dev/null; then
  IMAGE_COUNT=$(pdftoppm -png "$PDF_FILE" check-img 2>/dev/null | wc -l)
  rm -f check-img-*.png 2>/dev/null
  echo "🖼️ 嵌入图片数量: ${IMAGE_COUNT}"
fi

echo ""
echo "✅ 检查完成"
```

**运行质量检查**:

```bash
chmod +x scripts/check-pdf-quality.sh
./scripts/check-pdf-quality.sh dist/tutorial.pdf
```

**预期输出**:
```
📊 PDF 质量检查报告
====================
📁 文件大小: 12.35 MB
📄 总页数: 156
📝 标题: RAG 实战指南
✍️ 作者: 张三
🖼️ 嵌入图片数量: 42

✅ 检查完成
```

---

## CI/CD 集成

### GitHub Actions 自动生成 PDF

**Workflow 文件位置**: `.github/workflows/generate-pdf.yml`

**完整 Workflow 示例**:

```yaml
name: Generate PDF Ebook

on:
  push:
    branches: [main]
    paths:
      - 'packages/content/src/chapters/**'
      - 'packages/book/**'
  pull_request:
    branches: [main]

permissions:
  contents: write
  actions: read

jobs:
  generate-pdf:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      
    - name: Setup pnpm
      uses: pnpm/action-setup@v2
      with:
        version: 8
        
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: 20
        cache: 'pnpm'
        
    - name: Install dependencies
      run: pnpm install
      
    - name: Cache TeX Live
      id: cache-tex
      uses: actions/cache@v4
      with:
        path: ~/texlive
        key: texlive-${{ runner.os }}-v1
        restore-keys: |
          texlive-${{ runner.os }}-
          
    - name: Install TeX Live
      if: steps.cache-tex.outputs.cache-hit != 'true'
      run: |
        sudo apt-get update
        sudo apt-get install -y \
          texlive-xetex \
          texlive-lang-chinese \
          texlive-fonts-recommended \
          fonts-noto-cjk
          
    - name: Install Pandoc
      uses: pandoc/actions/setup@v1
      with:
        version: '3.x'  # 或 'latest'
        
    - name: Generate PDF
      run: |
        pnpm --filter @tutorial/book build:pdf
        
    - name: Upload PDF artifact
      uses: actions/upload-artifact@v4
      with:
        name: tutorial-pdf
        path: dist/tutorial.pdf
        retention-days: 30
        
    - name: Create Release (only on main branch)
      if: github.ref == 'refs/heads/main' && github.event_name == 'push'
      uses: softprops/action-gh-release@v1
      with:
        files: dist/tutorial.pdf
        tag_name: v${{ github.run_number }}
        name: "PDF Release v${{ github.run_number }}"
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 上传到 GitHub Releases

**触发条件**:
- 推送到 `main` 分支时自动创建 Release
- 或者打 Git Tag 时触发

**Release 命名规范**:

```
v<主版本>.<次版本>.<修订>-pdf
例如: v1.0.0-pdf
```

**Release 描述模板**:

```markdown
## 📚 教程 PDF 电子书

**生成时间**: {{ date }}
**提交哈希**: {{ commit_sha }}
**总页数**: {{ page_count }}
**文件大小**: {{ file_size }}

### 下载链接

- [tutorial.pdf](./tutorial.pdf) ({{ file_size }})

### 内容概览

<!-- 从 README 或 content 的 Frontmatter 自动提取 -->
```

### 缓存优化（LaTeX 依赖缓存策略）

**问题**: TeX Live 安装耗时较长（~5-10 分钟）

**解决方案**: 使用 GitHub Actions Cache

```yaml
- name: Cache TeX Live
  id: cache-tex
  uses: actions/cache@v4
  with:
    path: |
      ~/.texlive
      /usr/share/texlive
    key: texlive-${{ runner.os }}-${{ hashFiles('.github/tex-version') }}
    restore-keys: |
      texlive-${{ runner.os }}-

- name: Install TeX Live
  if: steps.cache-tex.outputs.cache-hit != 'true'
  run: |
    # 安装脚本...
```

**缓存失效策略**:
- 当 `.github/tex-version` 文件变化时强制重装
- 定期清理旧缓存（GitHub Actions 保留 7 天）

**缓存命中率优化**:
- 使用固定版本的 TeX Live
- 预安装常用宏包
- 分离字体缓存

### 与 web 构建并行执行

**Turborepo 并行任务配置**:

```json
{
  "tasks": {
    "build:web": {
      "dependsOn": ["@tutorial/content#build"],
      "cache": false
    },
    "build:book": {
      "dependsOn": ["@tutorial/content#build"],
      "cache": false
    },
    "build:all": {
      "dependsOn": ["build:web", "build:book"],
      "cache": false
    }
  }
}
```

**并行执行命令**:

```bash
# 同时构建 web 和 book
turbo run build:web build:book

# 或分别启动
turbo run build:web &
turbo run build:book &
wait
```

**CI Workflow 中的并行化**:

```yaml
jobs:
  build-web:
    runs-on: ubuntu-latest
    steps:
      - ...
      - run: pnpm --filter @tutorial/web build
      
  build-book:
    runs-on: ubuntu-latest
    steps:
      - ...
      - run: pnpm --filter @tutorial/book build:pdf
      
  deploy:
    needs: [build-web, build-book]
    runs-on: ubuntu-latest
    steps:
      - ...
      - run: echo "Web 和 Book 都已完成"
```

---

## 与其他子技能的关系 ⭐ 重要

### 数据流架构图

```
┌─────────────────────────────────────────┐
│         @tutorial/content               │
│    (唯一数据源: Markdown 章节内容)        │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴───────┐
       ▼               ▼
┌──────────────┐ ┌──────────────┐
│   📚 book    │ │    🌐 web    │
│  (PDF/EPUB)  │ │  (网站 HTML)  │
└──────────────┘ └──────────────┘
       │               │
       ▼               ▼
  ┌─────────┐   ┌──────────────┐
  │(未来)    │   │github-pages  │
  │epub-deploy│  │ (部署网站)    │
  └─────────┘   └──────────────┘
```

### 读取 @tutorial/content（唯一数据源）

**输入来源**:
```
packages/content/src/chapters/
├── 00-preface.md          # 前言
├── 01-introduction.md     # 第1章
├── 02-basics.md           # 第2章
├── ...
└── 99-appendix.md         # 附录
```

**数据访问方式**:

```bash
# 方式 1: 直接读取（推荐）
CONTENT_DIR="packages/content/src/chapters"
CHAPTERS=$(find "$CONTENT_DIR" -name "*.md" -type f | sort)

# 方式 2: 通过 workspace 依赖
# package.json 中声明: "@tutorial/content": "workspace:*"
# 运行时: pnpm --filter @tutorial/book build:pdf
```

**内容约定**:
- ✅ 文件命名: `{序号}-{英文slug}.md`
- ✅ 必须包含 YAML frontmatter（title, description 等）
- ✅ 图片相对路径: `../assets/images/xxx.png`
- ✅ 代码块语言标记: ```javascript

### 与 web 的平行关系

**共同点**:
- ✅ 都消费 @tutorial/content
- ✅ 都是输出格式（Format Producer）
- ✅ 可以并行构建
- ✅ 都有自己的样式系统

**差异点**:

| 维度 | book (PDF) | web (HTML) |
|------|-----------|------------|
| 输出格式 | PDF (静态) | HTML (交互式) |
| 引擎 | Pandoc + XeLaTeX | Astro + Starlight |
| 样式 | LaTeX/CSS | CSS/组件 |
| 交互能力 | ❌ 无 | ✅ 完整支持 |
| 离线阅读 | ✅ 完美 | ❌ 需要服务器 |
| 打印友好 | ✅ 原生 | ⚠️ 需优化 |
| 搜索功能 | ❌ PDF 内有限 | ✅ 全文搜索 |
| 更新频率 | 低频（版本发布） | 高频（持续部署） |

**协作边界**:
- book 不关心网站的导航、侧边栏、搜索
- web 不关心 PDF 的分页、页眉页脚、字体嵌入
- 两者只共享 content 层的数据

### 与 github-pages 的互补关系

**职责分工**:

| 子技能 | 职责 | 输出物 |
|--------|------|--------|
| **book** | 生成 PDF 电子书 | `dist/tutorial.pdf` |
| **github-pages** | 部署网站到 GitHub Pages | 公开访问的 URL |

**互补场景**:

**场景 1: 完整发布流程**
```bash
# Step 1: 生成 PDF
pnpm --filter @tutorial/book build:pdf

# Step 2: 构建网站
pnpm --filter @tutorial/web build

# Step 3: 部署到 GitHub Pages
pnpm --filter @tutorial/github-pages deploy
```

**场景 2: CI/CD 自动化**
```yaml
# .github/workflows/publish.yml
jobs:
  generate-ebook:
    outputs:
      pdf_path: dist/tutorial.pdf
    steps:
      - run: pnpm --filter @tutorial/book build:pdf
      
  deploy-site:
    needs: generate-ebook
    steps:
      - run: pnpm --filter @tutorial/github-pages deploy
      
  release-pdf:
    needs: generate-ebook
    steps:
      - uses: softprops/action-gh-release@v1
        with:
          files: dist/tutorial.pdf
```

**用户体验**:
- 🌐 在线阅读 → GitHub Pages 网站
- 📚 离线阅读 → 下载 PDF 电子书
- 🔗 两者互相链接（网站提供 PDF 下载按钮）

### 未来: 与 epub-deploy 的关系（预留）

**规划时间线**:
- v1.0.0: PDF only（当前版本）
- v1.1.0: EPUB support（实验性）
- v1.2.0: EPUB 正式支持 + epub-deploy 子技能
- v2.0.0: 多格式统一发布管道

**预留接口**:
```bash
# 当前: 只有 PDF
pnpm --filter @tutorial/book build:pdf

# 未来: 多格式
pnpm --filter @tutorial/book build:all  # PDF + EPUB
pnpm --filter @tutorial/book build:epub  # 仅 EPUB
```

**扩展设计原则**:
- EPUB 功能作为 book 的子集，不创建独立子技能
- 共享 Pandoc 配置和样式系统
- 复用 content 数据源
- epub-deploy 负责分发（类似 github-pages）

---

## 常见问题排查

### 问题 1: Pandoc 未找到或版本过低

**错误信息**:
```
❌ 未找到 Pandoc，请先安装
bash: pandoc: command not found
```

**解决方案**:

```bash
# 检查是否安装
pandoc --version

# 如果未安装，参考"环境安装指南"章节

# 如果版本过低 (< 2.0)
# macOS
brew upgrade pandoc

# Ubuntu
sudo apt-get install --only-upgrade pandoc

# Windows (Chocolatey)
choco upgrade pandoc
```

**最低版本要求**: Pandoc >= 2.17（推荐 >= 3.0）

### 问题 2: XeLaTeX 编译错误

**常见错误类型**:

**错误 A: 缺少宏包**:
```
! LaTeX Error: File `geometry.sty' not found.
```
**解决**:
```bash
# TeX Live
tlmgr install geometry

# MiKTeX（自动安装）
# 启动 MiKTeX Console → 设置 → 自动安装缺失包
```

**错误 B: 字体未找到**:
```
! Font "Noto Sans CJK SC" does not contain requested Script.
```
**解决**:
```bash
# 安装字体（参见"中文字体配置"章节）

# 或临时替换为系统字体
pandoc ... -V mainfont="SimSun"  # Windows
pandoc ... -V mainfont="PingFang SC"  # macOS
```

**错误 C: 编译超时/内存不足**:
```
! TeX capacity exceeded, sorry [main memory size].
```
**解决**:
```bash
# 增加 LaTeX 内存限制
export TEXMFVAR=~/.texlive/texmf-var
xelatex --extra-mem-bot=10000000 input.tex

# 或拆分为小章节分别编译
```

### 问题 3: 中文字体缺失或乱码

**症状**:
- PDF 中中文显示为方框 □□□
- 中文完全不显示
- 字体回退到丑陋的默认字体

**诊断步骤**:

```bash
# 1. 检查系统中文字体
fc-list :lang=zh family  # Linux/macOS

# 2. 查看具体字体文件
fc-match "Noto Sans CJK SC"

# 3. 测试 Pandoc 字体识别
pandoc --version | grep -i font
```

**解决方案**:

**方案 A: 安装 Noto 字体**（推荐）:
```bash
# macOS
brew install --cask font-noto-sans-cjk-sc

# Ubuntu
sudo apt-get install -y fonts-noto-cjk

# Windows
# 手动下载并安装（见"环境安装指南"）
```

**方案 B: 使用系统备用字体**:
```bash
# 检测并使用可用字体
if [[ "$OSTYPE" == "darwin"* ]]; then
  FONT="PingFang SC"
elif [[ "$OSTYPE" == "msys"* ]]; then
  FONT="Microsoft YaHei"
else
  FONT="Noto Sans CJK SC"
fi

pandoc ... -V mainfont="$FONT"
```

**方案 C: 嵌入字体到 PDF**（确保在任何设备上都能正确显示）:
```bash
pandoc ... \
  -V embed-fonts=true \
  -V subset-fonts=true  # 只嵌入使用的字符（减小体积）
```

### 问题 4: PDF 目录/书签异常

**症状**:
- 目录不显示
- 目录页码错误
- 书签无法点击

**解决方案**:

**问题 A: 目录为空**:
```bash
# 确保 Markdown 中有标题
# ✅ 正确: # 第一章
# ❌ 错误: 第一章（没有 # 号）

# 检查 TOC 参数
pandoc ... --toc --toc-depth=3
```

**问题 B: 目录页码不更新**:
```bash
# 需要编译两次以更新交叉引用
pandoc ... --to pdf
# 再次运行
pandoc ... --to pdf
```

**问题 C: 书签无法点击**:
```bash
# 确保 hyperref 包已加载
pandoc ... \
  -V header-includes="\usepackage{hyperref}" \
  -V hyperref-colorlinks=true
```

### 问题 5: 图片无法嵌入

**症状**:
- PDF 中图片显示为空白
- 报错: "File not found"
- 图片模糊或变形

**诊断与解决**:

```bash
# 1. 检查图片路径
# Markdown 中的相对路径应相对于 Markdown 文件本身
# ✅ 正确: ![图](../assets/images/arch.png)
# ❌ 错误: ![图](/absolute/path/to/image.png)

# 2. 检查图片是否存在
ls -la ../assets/images/arch.png

# 3. 指定资源搜索路径
pandoc ... --resource-path=.:packages/content/src/assets

# 4. 检查图片格式支持
# Pandoc/XeLaTeX 支持: PNG, JPG, PDF, SVG（需转换）
# SVG 转换:
inkscape image.svg --export-type=png --export-filename=image.png

# 5. 调整图片尺寸
![架构图](image.png){ width=80% height=auto }

# 6. 减小图片体积（避免 PDF 过大）
convert image.png -resize 800x600 -quality 85 image-small.png
```

### 问题 6: 内存不足（大文档）

**症状**:
- 编译过程卡住
- 系统内存耗尽
- XeLaTeX 进程被杀死

**解决方案**:

**方案 A: 拆分文档**:
```bash
# 将长文档拆分为多个 PDF
# 第一部分: 第 1-3 章
pandoc ch[1-3]*.md ... -o part1.pdf

# 第二部分: 第 4-6 章
pandoc ch[4-6]*.md ... -o part2.pdf

# 使用 PDF 工具合并
pdftk part1.pdf part2.pdf cat output full.pdf
```

**方案 B: 减少 LaTeX 内存占用**:
```bash
# 使用 draft 模式（不加载图片）
pandoc ... -V draft-mode=true

# 减少字体嵌入
pandoc ... -V subset-fonts=true

# 禁用不必要的功能
pandoc ... --no-highlight  # 禁用代码高亮
```

**方案 C: 增加系统资源**:
```bash
# Linux/macOS
ulimit -v unlimited  # 增加虚拟内存限制

# 或使用 Docker 容器（分配更多内存）
docker run --memory=8g pandoc-image pandoc ...
```

---

## 版本历史

### v1.0.0 (2026-05-31) — 初始版本

**新增功能**:
- ✅ PDF 生成核心功能（基于 Pandoc + XeLaTeX）
- ✅ 中文字体配置（Noto Sans CJK SC）
- ✅ 代码高亮（Tango 主题）
- ✅ 目录自动生成（TOC）
- ✅ 页面布局配置（A4/Letter/自定义）
- ✅ LaTeX 模板系统
- ✅ 电子书样式指南
- ✅ CI/CD 集成（GitHub Actions）
- ✅ 质量检查工具
- ✅ 增量构建支持
- ✅ EPUB 生成框架（预留扩展点）

**设计决策**:
- 选择 Pandoc 作为核心转换器（而非纯 LaTeX 手写）
- 选择 XeLaTeX 作为 PDF 引擎（Unicode + 中文支持）
- 聚焦 PDF 生成，EPUB 作为 v1.1.0 功能
- 明确声明对 @tutorial/content 的依赖
- 采用 Format Producer 角色（与 web 平行）

**已知限制**:
- ⚠️ EPUB 支持为实验性（v1.1.0 完善）
- ⚠️ 不支持交互式元素（PDF 固有局限）
- ⚠️ 大型文档（>300页）可能需要拆分
- ⚠️ 复杂排版需求可能需要自定义 LaTeX 模板

**后续计划**:
- v1.1.0: 完善 EPUB 生成 + 电子书分发
- v1.2.0: 更多 LaTeX 模板（学术论文、技术手册）
- v2.0.0: 多格式统一发布管道 + 增强样式系统

---

## 📚 参考资料

详细的技术文档请查看 `references/` 目录：

- [Pandoc 详细配置](references/pandoc-configuration.md) - Pandoc 命令行参数、过滤器、自定义输出
- [LaTeX 模板库](references/latex-templates.md) - 模板开发指南、参数详解、最佳实践
- [PDF 排版样式指南](references/pdf-styling.md) - 字体、间距、代码块、表格等样式细节
- [问题排查手册](references/troubleshooting.md) - 常见错误诊断、性能优化、调试技巧

---

## 🎯 快速参考卡片

### 常用命令速查

```bash
# 生成 PDF（默认配置）
pnpm --filter @tutorial/book build:pdf

# 手动执行 Pandoc
pandoc chapters/*.md --to pdf -o output.pdf --pdf-engine=xelatex

# 预览 PDF
pnpm --filter @tutorial/book preview

# 质量检查
./scripts/check-pdf-quality.sh dist/tutorial.pdf
```

### 核心配置参数

| 参数 | 值 | 说明 |
|------|-----|------|
| `--pdf-engine` | xelatex | PDF 引擎 |
| `--toc` | 启用 | 生成目录 |
| `--toc-depth` | 3 | 目录深度 |
| `--highlight-style` | tango | 代码高亮主题 |
| `geometry` | a4paper, 2.5cm | 页面布局 |
| `mainfont` | Noto Sans CJK SC | 中文字体 |

### 故障排除清单

- [ ] Pandoc >= 2.0 已安装？
- [ ] XeLaTeX 可用？
- [ ] 中文字体已安装？
- [ ] 章节文件存在且非空？
- [ ] 图片路径正确？
- [ ] 系统内存充足？

---

> **最后更新**: 2026-05-31 | **维护者**: skill-factory | **版本**: v1.0.0
