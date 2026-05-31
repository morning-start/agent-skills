# Pandoc 详细配置

> **版本**: v1.0.0 | **最后更新**: 2026-05-31
> **适用范围**: Tutorial Writer Book 子技能

## 目录

- [Pandoc 基础](#pandoc-基础)
- [命令行参数详解](#命令行参数详解)
- [输入格式配置](#输入格式配置)
- [输出格式配置](#输出格式配置)
- [元数据管理](#元数据管理)
- [过滤器系统](#过滤器系统)
- [高级用法](#高级用法)
- [性能优化](#性能优化)

---

## Pandoc 基础

### 什么是 Pandoc？

Pandoc 是一个通用的文档转换工具，由 John MacFarlane 开发，使用 Haskell 编写。它能够将一种标记格式转换为另一种标记格式。

**核心特性**:
- 支持 40+ 输入/输出格式
- 扩展的 Markdown 语法
- 强大的过滤器和模板系统
- 活跃的开源社区

**官方资源**:
- 网站: https://pandoc.org/
- 文档: https://pandoc.org/MANUAL.html
- GitHub: https://github.com/jgm/pandoc

### 版本选择

| 版本 | 发布日期 | 特性 | 推荐度 |
|------|---------|------|--------|
| 3.x (最新) | 2024+ | 新功能、性能优化 | ⭐⭐⭐⭐⭐ |
| 2.19.x | 2023 | 稳定、广泛测试 | ⭐⭐⭐⭐ |
| 2.17.x | 2022 | 最低要求版本 | ⭐⭐⭐ |

**检查当前版本**:
```bash
pandoc --version | head -1
# pandoc 3.1.9
```

---

## 命令行参数详解

### 基本语法

```bash
pandoc [OPTIONS] [FILES]
```

### 输入输出控制

#### 文件指定

```bash
# 单个文件
pandoc input.md -o output.pdf

# 多个文件（按顺序合并）
pandoc ch1.md ch2.md ch3.md -o book.pdf

# 使用通配符（需要 shell 展开）
pandoc chapters/*.md -o book.pdf

# 标准输入
cat input.md | pandoc -f markdown -t pdf -o output.pdf
```

#### 格式指定

```bash
# 显式指定输入格式
--from markdown          # 标准 Markdown
--from markdown-phpextra # 扩展 Markdown（支持表格、定义列表等）
--from commonmark        # 严格 CommonMark 兼容

# 显式指定输出格式
--to pdf                 # PDF（需要 PDF 引擎）
--to html                # HTML
--to docx                # Word 文档
--to epub                # EPUB 电子书
--to latex               # LaTeX 源码
```

### PDF 引擎选项

#### XeLaTeX 配置

```bash
# 基础配置
--pdf-engine=xelatex

# 传递额外参数给 XeLaTeX
--pdf-engine-opt=-shell-escape
--pdf-engine-opt="-interaction=nonstopmode"

# 减少编译时间（不生成辅助文件）
--pdf-engine-opt="-draftmode"
```

#### 其他 PDF 引擎

| 引擎 | 中文支持 | 速度 | 适用场景 |
|------|---------|------|---------|
| **xelatex** | ✅ 原生 | 中等 | 推荐（默认） |
| **lualatex** | ✅ 通过 Lua | 较慢 | 特殊字体需求 |
| **pdflatex** | ❌ 需要配置 | 最快 | 纯英文文档 |

### 元数据选项

#### 命令行元数据

```bash
# 简单键值对
--metadata title="我的教程"
--metadata author="张三"

# 多值字段（列表）
--metadata tags="[tag1, tag2, tag3]"

# 从文件读取
--metadata-file=metadata.yaml
```

#### YAML Frontmatter

在 Markdown 文件开头添加 YAML 块：

```yaml
---
title: "RAG 实战指南"
author:
  - "张三"
  - "李四"
date: 2026-05-31
abstract: |
  这是一本关于 RAG 技术的完整教程，
  从基础概念到高级应用。
keywords: [RAG, AI, LLM, Vector Database]
toc: true
toc-depth: 3
header-includes: |
  \usepackage{graphicx}
  \usepackage{booktabs}
---
```

**优先级规则**:
1. YAML Frontmatter（最高）
2. `--metadata-file` 参数
3. `--metadata` 命令行参数（最低）

---

## 输入格式配置

### Markdown 扩展语法

Pandoc 支持多种 Markdown 扩展：

#### 启用扩展

```bash
# 启用所有扩展（推荐）
--from markdown

# 或显式启用特定扩展
--from markdown+raw_html+tex_math_dollars
```

#### 常用扩展列表

| 扩展名 | 功能 | 示例 |
|--------|------|------|
| `tables` | 表格 | `\| col1 \| col2 \|` |
| `task_lists` | 任务列表 | `- [x] 完成` |
| `strikeout` | 删除线 | `~~删除~~` |
| `superscript` | 上标 | `H~2~O` |
| `subscript` | 下标 | `X~ij~` |
| `raw_html` | 原始 HTML | `<div class="note">` |
| `tex_math_dollars` | LaTeX 公式 | `$E=mc^2$` |
| `fenced_code_blocks` | 围栏代码块 | ``` ```python ``` |
| `backtick_code_blocks` | 反引号代码块 | `` ``` `` |
| `inline_code_attributes` | 内联代码属性 | `` `code`{.python} `` |
| `markdown_in_html_blocks` | HTML 中的 Markdown | `<div>*italic*</div>` |
| `footnotes` | 脚注 | `[^1]` |
| `definition_lists` | 定义列表 | `: term : definition` |

#### 自定义扩展组合

```bash
# 仅启用需要的扩展
--from \
  markdown\
  +tables\
  +pipe_tables\
  +strikeout\
  +superscript\
  +subscript\
  +raw_html\
  +tex_math_dollars\
  +fenced_code_blocks\
  +footnotes\
  +definition_lists\
  +intraword_underscores\
  +hash_headers\
  +all_symbols_escapable
```

### 内容包含指令

```markdown
{{< include file="common/intro.md" >}}
```

需要在 Pandoc 过滤器中实现此功能（参见"过滤器系统"章节）。

---

## 输出格式配置

### PDF 输出选项

#### 页面设置

```bash
# 纸张尺寸
-V geometry:a4paper           # A4（默认）
-V geometry:letterpaper       # Letter
-V geometry:legalpaper        # Legal
-V geometry:paperwidth=20cm   # 自定义宽度
-V geometry:paperheight=28cm  # 自定义高度

# 边距
-V geometry:margin=2.5cm      # 统一边距
-V geometry:top=2.5cm         # 上边距
-V geometry:bottom=2.5cm      # 下边距
-V geometry:left=2.5cm        # 左边距
-V geometry:right=2.5cm       # 右边距

# 双栏模式
-V geometry:twocolumn
-V geometry:columnsep=0.5cm   # 栏间距
```

#### 字体配置

```bash
# 正文字体
-V mainfont="Noto Sans CJK SC"
-V sansfont="Noto Sans CJK SC"
-V monofont="Noto Sans Mono CJK SC"

# 字体大小
-V fontsize=11pt              # 默认 10pt
-V fontsize=12pt              # 大字号

# 行距
-V linestretch=1.6            # 默认 1.0
```

#### 目录和编号

```bash
# 目录
--toc                          # 启用目录
--toc-depth=3                 # 显示到 H3
--toc-title="目 录"            # 目录标题
--number-sections             # 自动编号

# 章节深度
--section-divs                # 使用 <div> 包裹章节
```

#### 代码高亮

```bash
# 内置主题
--highlight-style=tango       # 彩色柔和（推荐）
--highlight-style=pygments    # 默认风格
--highlight-style=kate        # Kate 编辑器
--highlight-style=monochrome  # 黑白打印
--highlight-style=espresso    # 深色背景
--highlight-style=zenburn     # 暗色调
--highlight-style=haddock     # Haskell 风格

# 自定义主题文件
--highlight-style=my-theme.theme
```

#### 超链接和交叉引用

```bash
# hyperref 配置
-V colorlinks=true            # 彩色链接
-V linkcolor=blue             # 内部链接颜色
-V urlcolor=blue              # URL 颜色
-V tocolor=blue               # TOC 链接颜色
-V citecolor=green            # 引用颜色
-V anchorcolor=black          # 锚点颜色

# PDF 书签
-V bookmarks=true             # 生成书签
-V bookmark-level=2           # 书签起始级别
```

### HTML 输出选项（参考）

虽然本书技能聚焦 PDF，但了解 HTML 选项有助于调试：

```bash
# 独立 HTML 文件
--standalone --to html

# CSS 样式
--css=styles.css
--css=highlight.css

# 数学公式渲染
--mathjax                     # MathJax
--katex=...                   # KaTeX（更快）

# 自包含（内联所有资源）
--self-contained
```

---

## 元数据管理

### 元数据变量

Pandoc 定义了许多内置元数据变量：

#### 文档信息

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `title` | 文档标题 | （无） |
| `author` | 作者（字符串或列表） | （无） |
| `date` | 日期 | 当前日期 |
| `subtitle` | 副标题 | （无） |
| `abstract` | 摘要 | （无） |
| `keywords` | 关键词列表 | （无） |

#### 样式控制

| 变量 | 说明 | 示例值 |
|------|------|--------|
| `fontsize` | 字号 | `11pt` |
| `geometry` | 页面布局 | `a4paper, margin=2.5cm` |
| `mainfont` | 主字体 | `Noto Sans CJK SC` |
| `monofont` | 等宽字体 | `JetBrains Mono` |
| `linestretch` | 行距 | `1.6` |
| `documentclass` | 文档类 | `article` |

#### 功能开关

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `toc` | 是否生成目录 | false |
| `toc-depth` | 目录深度 | 3 |
| `number-sections` | 是否编号 | false |
| `links-as-notes` | 链接转为脚注 | false |
| `colorlinks` | 彩色链接 | true |

### 条件元数据处理

根据不同输出格式应用不同的元数据：

```yaml
---
title: "教程标题"
author: "作者"

# 仅用于 PDF
header-includes: |
  \usepackage{fancyhdr}

# 仅用于 HTML
css: styles.html.css
---
```

---

## 过滤器系统

### 什么是过滤器？

Pandoc 过滤器是处理 AST（抽象语法树）的程序，可以在转换过程中修改或增强内容。

### Lua 过滤器（推荐）

从 Pandoc 2.0 开始支持内置 Lua 过滤器：

```lua
-- filters/add-timestamp.lua
function Header(elem)
  if elem.level == 1 then
    return pandoc.Header(1, {elem.content, pandoc.Space(), pandoc.Str(os.date("%Y-%m-%d"))})
  end
  return elem
end
```

**使用方法**:
```bash
pandoc input.md --lua-filter=filters/add-timestamp.lua -o output.pdf
```

### 常用 Lua 过滤器示例

#### 1. 自动添加章号

```lua
-- filters/chapter-number.lua
local chapter_num = 0

function Header(elem)
  if elem.level == 1 then
    chapter_num = chapter_num + 1
    local num = pandoc.String(string.format("第 %d 章 ", chapter_num))
    table.insert(elem.content, 1, num)
  end
  return elem
end
```

#### 2. 图片路径修正

```lua
-- filters/fix-image-paths.lua
function Image(img)
  -- 将相对路径转换为绝对路径
  if img.src and not img.src:match("^/") then
    img.src = "../assets/images/" .. img.src
  end
  return img
end
```

#### 3. 代码块添加复制按钮占位符

```lua
-- filters/code-copy-button.lua
function CodeBlock(block)
  -- 在代码块前添加提示文本
  local note = pandoc.Para({pandoc.Str("📋 点击代码可复制")})
  return {note, block}
end
```

### Python 过滤器（panflute）

安装 panflute 库：
```bash
pip install panflute
```

示例过滤器：
```python
# filters/wordcount.py
import panflute

def action(elem, doc):
    if isinstance(elem, panflute.Para):
        count = len(elem.text.split())
        print(f"Paragraph word count: {count}")

def main(doc=None):
    return panflute.run_filter(action, doc=doc)

if __name__ == "__main__":
    main()
```

**使用方法**:
```bash
pandoc input.md --filter=filters/wordcount.py -o output.pdf
```

### 过滤器链

可以同时应用多个过滤器：
```bash
pandoc input.md \
  --lua-filter=filters/chapter-number.lua \
  --lua-filter=filters/fix-image-paths.lua \
  --lua-filter=filters/add-footer.lua \
  -o output.pdf
```

**执行顺序**: 从左到右依次执行

---

## 高级用法

### 模板系统

Pandoc 使用模板来控制输出格式。默认模板可以通过以下方式查看：

```bash
# 查看 PDF 默认模板
pandoc -D latex > default-latex.template

# 查看 HTML 默认模板
pandoc -D html > default-html.template

# 查看 EPUB 默认模板
pandoc -D epub > default-epub.template
```

### 自定义模板变量

在模板中使用 `$variable$` 语法引用变量：

```latex
\title{$title$}
\author{$for(author)$$author$$sep$, $endfor$}
\date{$date$}

\begin{document}
$if(title)$
\maketitle
$endif$

$if(toc)$
\tableofcontents
$endif$

$body$
\end{document}
```

### 部分渲染（Partial Render）

只渲染文档的一部分用于预览：

```bash
# 只渲染第 1 章
pandoc ch1.md --to pdf -o preview-ch1.pdf

# 渲染前 100 行
head -n 100 input.md | pandoc -f markdown -t pdf -o preview.pdf
```

### 批量转换

```bash
#!/bin/bash
# batch-convert.sh

INPUT_DIR="chapters"
OUTPUT_DIR="dist"

mkdir -p "$OUTPUT_DIR"

for file in "$INPUT_DIR"/*.md; do
  basename=$(basename "$file" .md)
  echo "Converting: $basename"
  pandoc "$file" \
    --from markdown \
    --to pdf \
    --output "$OUTPUT_DIR/${basename}.pdf" \
    --pdf-engine=xelatex \
    --metadata title="$basename"
done

echo "✅ Batch conversion completed"
```

---

## 性能优化

### 编译速度优化

#### 1. 减少 LaTeX 编译次数

```bash
# 默认情况下 XeLaTeX 会编译多次以解决交叉引用
# 如果不需要精确的页码引用，可以减少次数
--pdf-engine-opt="-interaction=batchmode"
```

#### 2. 使用缓存

```bash
# Turborepo 缓存
turbo run build:book

# 手动缓存（基于文件哈希）
#!/bin/bash
CACHE_DIR=".cache/pandoc"
FILE_HASH=$(md5sum chapters/*.md | md5sum | awk '{print $1}')

if [ -f "$CACHE_DIR/$FILE_HASH.pdf" ]; then
  echo "✅ Using cached PDF"
  cp "$CACHE_DIR/$FILE_HASH.pdf" dist/tutorial.pdf
else
  echo "🔄 Building PDF..."
  pandoc ... -o dist/tutorial.pdf
  mkdir -p "$CACHE_DIR"
  cp dist/tutorial.pdf "$CACHE_DIR/$FILE_HASH.pdf"
fi
```

#### 3. 并行处理

```bash
# GNU Parallel
find chapters -name "*.md" | parallel pandoc {} --to pdf -o {.}.pdf

# xargs（简单并行）
find chapters -name "*.md" | xargs -P 4 -I{} pandoc {} --to pdf -o {.}.pdf
```

### 内存优化

#### 处理大文档

```bash
# 方法 1: 分块处理
split -l 500 large-doc.md chunk-
for chunk in chunk-*; do
  pandoc "$chunk" --to pdf -o "${chunk}.pdf"
done
pdftk chunk-*.pdf cat output full.pdf

# 方法 2: 减少 LaTeX 内存占用
--pdf-engine-opt="--max-memory=100000000"  # 100MB

# 方法 3: 禁用不必要的功能
--no-highlight                    # 禁用代码高亮
-V draft-mode=true               # 草稿模式
```

### 输出体积优化

#### 压缩 PDF

```bash
# 使用 Ghostscript 压缩
gs -sDEVICE=pdfwrite \
   -dCompatibilityLevel=1.4 \
   -dPDFSETTINGS=/ebook \
   -dNOPAUSE -dBATCH \
   -sOutputFile=output-compressed.pdf \
   input.pdf

# PDFSETTINGS 选项:
# /screen   (72 dpi)  - 最小体积
# /ebook    (150 dpi) - 平衡质量和大小
# /printer  (300 dpi) - 高质量
# /prepress (300 dpi) - 印刷质量
```

#### 图片优化

```bash
# 转换图片为合适 DPI
convert input.png -resize 1200x1200 -density 150 output.png

# 使用有损压缩（JPEG）
convert input.png -quality 85 output.jpg

# 使用 PNG 优化工具
optipng -o7 input.png
```

---

## 调试技巧

### 查看中间结果

```bash
# 查看 Markdown 解析后的 AST
pandoc input.md -t native

# 查看 LaTeX 中间代码
pandoc input.md -t latex

# 查看 HTML 中间结果
pandoc input.md -t html
```

### 日志输出

```bash
# 详细日志
--verbose

# 调试 LaTeX 编译过程
--pdf-engine-opt="-interaction=nonstopmode"
--log=build.log

# 只显示错误
--fail-if-warnings
```

### 常见问题速查

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| 编译卡住 | XeLaTeX 循环 | 增加 `-interaction=nonstopmode` |
| 字体缺失 | 未安装字体 | 安装字体或替换为系统字体 |
| 图片不显示 | 路径错误 | 使用 `--resource-path` 指定 |
| 乱码 | 编码问题 | 确保 UTF-8 编码 |
| 目录为空 | 缺少标题 | 检查 Markdown 是否有 H1-H3 |

---

## 最佳实践清单

### ✅ 推荐做法

- [ ] 使用最新稳定版 Pandoc (>= 3.0)
- [ ] 始终指定 `--pdf-engine=xelatex`
- [ ] 使用 YAML frontmatter 管理元数据
- [ ] 创建自定义模板以满足品牌需求
- [ ] 使用 Lua 过滤器增强内容
- [ ] 实现增量构建以提高效率
- [ ] 为 CI/CD 环境编写自动化脚本
- [ ] 版本控制模板和样式文件

### ⚠️ 应避免的做法

- [ ] 不要硬编码路径（使用相对路径）
- [ ] 不要忽略字体回退策略
- [ ] 不要在生产环境使用 `--draftmode`
- [ ] 不要忘记测试中文内容
- [ ] 不要忽略 PDF 可访问性（PDF/A 标准）

---

> **相关文档**:
> - [LaTeX 模板库](latex-templates.md) - 模板开发和定制
> - [PDF 排版样式指南](pdf-styling.md) - 视觉样式细节
> - [问题排查手册](troubleshooting.md) - 故障诊断
>
> **返回主文档**: [SKILL.md](../SKILL.md)
