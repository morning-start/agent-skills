# LaTeX 模板库

> **版本**: v1.0.0 | **最后更新**: 2026-05-31
> **适用范围**: Tutorial Writer Book 子技能

## 目录

- [模板系统概述](#模板系统概述)
- [默认技术教程模板](#默认技术教程模板)
- [模板参数详解](#模板参数详解)
- [自定义模板开发](#自定义模板开发)
- [学术模板扩展](#学术模板扩展)
- [企业品牌模板](#企业品牌模板)
- [最佳实践](#最佳实践)

---

## 模板系统概述

### Pandoc 模板工作原理

Pandoc 使用模板来生成输出。对于 PDF 输出，模板是一个 LaTeX 文件，定义了文档的整体结构和样式。

**模板处理流程**:
```
Markdown 文件
    ↓
Pandoc 解析器 (AST)
    ↓
应用模板 (LaTeX 模板)
    ↓
XeLaTeX 编译
    ↓
PDF 文件
```

### 默认模板位置

| 类型 | 位置 | 说明 |
|------|------|------|
| 内置模板 | Pandoc 安装目录 | 可通过 `pandoc -D latex` 查看 |
| 项目模板 | `packages/book/templates/` | 推荐的自定义位置 |
| 用户模板 | `~/.pandoc/templates/` | 全局共享模板 |

### 获取内置模板

```bash
# 导出当前使用的 LaTeX 模板
pandoc -D latex > my-template.latex

# 查看但不保存
pandoc -D latex | less
```

---

## 默认技术教程模板

### 完整模板代码

这是 Tutorial Writer 的默认 LaTeX 模板，专为技术教程优化：

```latex
%% ============================================================
%% Tutorial Writer - Default LaTeX Template v1.0.0
%% 适用于: 技术教程、编程书籍、API 文档
%% 编译引擎: XeLaTeX (推荐) 或 LuaLaTeX
%% ============================================================

\documentclass[a4paper,11pt]{article}

%% ===== 中文支持 (必须最先加载) =====
\usepackage{ctex}
\usepackage{xeCJK}

% 设置中文字体（可根据系统调整）
\setCJKmainfont{Noto Sans CJK SC}[BoldFont=Noto Sans CJK SC Bold]
\setCJKsansfont{Noto Sans CJK SC}
\setCJKmonofont{Noto Sans Mono CJK SC}

%% ===== 页面布局 =====
\usepackage[
  a4paper,
  top=2.5cm,
  bottom=2.5cm,
  left=2.5cm,
  right=2.5cm,
  headheight=14.5pt,
  headsep=20pt,
  footskip=20pt
]{geometry}

%% ===== 代码高亮设置 =====
\usepackage{listings}
\usepackage{xcolor}

% 定义代码样式
\definecolor{codebackground}{HTML}{F5F5F5}
\definecolor{codeborder}{HTML}{DDDDDD}
\definecolor{codecomment}{HTML}{6A9955}
\define{codestring}{HTML}{A31515}
\define{codekeyword}{HTML}{0000FF}
\define{codenumber}{HTML}{098658}

\lstset{
  basicstyle=\ttfamily\small,
  backgroundcolor=\color{codebackground},
  frame=single,
  framerule=0.5pt,
  rulecolor=\color{codeborder},
  breaklines=true,
  breakatwhitespace=true,
  showstringspaces=false,
  tabsize=2,
  captionpos=b,
  numbers=none,
  xleftmargin=1em,
  xrightmargin=1em,
  aboveskip=1em,
  belowskip=0.5em
}

%% ===== 超链接配置 =====
\usepackage{hyperref}
\hypersetup{
  colorlinks=true,
  linkcolor=blue!70!black,
  urlcolor=blue!70!black,
  citecolor=green!50!black,
  pdfauthor={$author$},
  pdftitle={$title$},
  pdfsubject={Tutorial},
  pdfkeywords={$for(keywords)$$keywords$$sep$, $endfor$},
  pdfcreator={Tutorial Writer v1.0.0},
  hidelinks=false
}

%% ===== 目录配置 =====
\usepackage[toc,page]{appendix}
\usepackage{tocloft}

% 目录标题
\renewcommand{\contentsname}{目 录}

% 目录样式
\renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}}
\renewcommand{\cftdotsep}{1}
\setcounter{tocdepth}{3}      % 显示到第 3 层标题
\setcounter{secnumdepth}{3}   % 编号到第 3 层

%% ===== 页眉页脚 =====
\usepackage{fancyhdr}

% 页面样式
\pagestyle{fancy}

% 清除默认设置
\fancyhf{}

% 页眉
\fancyhead[L]{\small\leftmark}           % 左侧: 章节名
\fancyhead[R]{\small\thepage}            % 右侧: 页码
\renewcommand{\headrulewidth}{0.4pt}     % 页眉线粗细

% 页脚
\fancyfoot[C]{\small $title$}            % 中央: 书名
\renewcommand{\footrulewidth}{0pt}       % 无页脚线

% 首页不显示页眉页脚
\fancypagestyle{plain}{
  \fancyhf{}
  \renewcommand{\headrulewidth}{0pt}
  \renewcommand{\footrulewidth}{0pt}
}

%% ===== 标题格式 =====
\usepackage{titlesec}

% H1 格式
\titleformat{\section}
  {\normalfont\Large\bfseries\color{black}}
  {这些ction\hspace{0.5em}}{0em}{}
\titlespacing*{\section}{0pt}{24pt plus 2pt minus 2pt}{12pt plus 2pt minus 2pt}

% H2 格式
\titleformat{\subsection}
  {\normalfont\large\bfseries\color{black!80}}
  {thesubsection\hspace{0.5em}}{0em}{}
\titlespacing*{\subsection}{0pt}{18pt plus 2pt minus 2pt}{8pt plus 2pt minus 2pt}

% H3 格式
\titleformat{\subsubsection}
  {\normalfont\normalsize\bfseries\color{black!70}}
  {thesubsubsection\hspace{0.5em}}{0em}{}
\titlespacing*{\subsubsection}{0pt}{12pt plus 2pt minus 2pt}{6pt plus 2pt minus 2pt}

%% ===== 段落和间距 =====
\setlength{\parindent}{2em}        % 首行缩进 2 字符
\setlength{\parskip{0.5em}}        % 段落间距
\linespread{1.5}                    % 行距 1.5 倍

%% ===== 表格增强 =====
\usepackage{booktabs}              % 专业表格线
\usepackage{array}                 % 列格式增强
\usepackage{tabularx}              % 自适应宽度表格
\usepackage{longtable}             % 跨页表格

%% ===== 图片支持 =====
\usepackage{graphicx}
\graphicspath{{../assets/images/}{images/}{./}}

% 图片默认位置选项
\floatplacement{figure}{htbp}
\floatplacement{table}{htbp}

%% ===== 数学公式支持 =====
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{mathtools}

%% ===== 孤行寡行控制 =====
\usepackage[all]{nowidow}
\widowpenalty=1000
\clubpenalty=1000

%% ============================================================
%% 文档开始
%% ============================================================

\title{$title$}
$if(author)$
\author{$for(author)$$author$$sep$, \and $endfor$}
$endif$
$if(date)$
\date{$date$}
$else$
\date{\today}
$endif$

\begin{document}

% 封面
\maketitle

% 目录
$if(toc)$
\newpage
\tableofcontents
\newpage
$endif$

% 正文内容（由 Pandoc 自动填充）
$body$

\end{document}
```

### 模板特点说明

#### ✅ 设计优势

1. **中文原生支持**
   - 使用 ctex + xeCJK 宏包
   - 支持所有 Unicode 中文字符
   - 自动处理中文标点和排版规则

2. **专业排版质量**
   - 合理的页面边距（2.5cm）
   - 优化的行距和段落间距
   - 清晰的层级结构

3. **代码友好**
   - 语法高亮支持
   - 自动换行
   - 等宽字体渲染

4. **可访问性**
   - PDF 书签自动生成
   - 超链接可点击
   - 元数据完整

#### 📐 尺寸规范

| 元素 | 值 | 说明 |
|------|-----|------|
| 纸张 | A4 (210×297mm) | 国际标准 |
| 字号 | 11pt | 正文标准大小 |
| 行距 | 1.5倍 | 舒适阅读 |
| 边距 | 2.5cm | 四边统一 |
| 首行缩进 | 2em | 中文排版惯例 |

---

## 模板参数详解

### 文档类选项

```latex
\documentclass[选项]{文档类}
```

**常用文档类**:

| 类名 | 适用场景 | 特点 |
|------|---------|------|
| `article` | 技术教程、短文 | 最常用，无章节划分 |
| `report` | 长篇教程、手册 | 支持章和部分 |
| `book` | 完整书籍 | 双面打印、更多结构 |
| `scrartcl` | KOMA-Script | 更现代的 article |
| `scrreprt` | KOMA-Script | 更现代的 report |

**文档类选项**:

```latex
\documentclass[
  a4paper,       % 纸张尺寸
  11pt,          % 字号 (10pt/11pt/12pt)
  oneside,       % 单面打印 (默认)
  twoside,       % 双面打印
  openright,     % 章从奇数页开始
  fleqn,         % 公式左对齐
  leqno          % 公式编号在左侧
]{article}
```

### 字体配置参数

#### 正文字体族

```latex
% 三种基本字体
\setmainfont{Times New Roman}         % 衬线字体（正文）
\setsansfont{Helvetica}               % 无衬线字体（标题）
\setmonofont{Courier New}             % 等宽字体（代码）

% 中文对应字体
\setCJKmainfont{Noto Serif CJK SC}    % 中文衬线
\setCJKsansfont{Noto Sans CJK SC}     % 中文无衬线
\setCJKmonofont{Noto Sans Mono CJK SC}% 中文等宽
```

**字体回退策略**:
```latex
% 如果主字体不可用，使用备选字体
\IfFontExistsTF{Noto Sans CJK SC}{
  \setCJKmainfont{Noto Sans CJK SC}
}{
  \IfFontExistsTF{PingFang SC}{
    \setCJKmainfont{PingFang SC}
  }{
    \setCJKmainfont{SimSun}  % 最终回退
  }
}
```

### 页面布局参数

#### geometry 包详细配置

```latex
\usepackage[
  paper=a4paper,              % 或 letterpaper/legalpaper
  portrait,                   % 纵向 (或 landscape 横向)
  top=2.5cm,                  % 上边距
  bottom=2.5cm,               % 下边距
  left=2.5cm,                 % 左边距
  right=2.5cm,                % 右边距
  headheight=14.5pt,          % 页眉高度
  headsep=20pt,               % 页眉与正文距离
  footskip=20pt,              % 页脚高度
  marginparwidth=2cm,         % 旁注宽度
  columnsep=0.5cm,            % 双栏间距 (如果启用 twocolumn)
  includeheadfoot,            % 边距包含页眉页脚
  centering                   % 内容居中 (用于特殊纸张)
]{geometry}
```

**预设布局方案**:

```latex
% 方案 A: 宽松阅读版
\usepackage[a4paper, margin=3cm, fontsize=12pt]{geometry}

% 方案 B: 紧凑打印版
\usepackage[a4paper, margin=2cm, fontsize=10pt]{geometry}

% 方案 C: 学术论文版
\usepackage[a4paper,
  top=2.54cm, bottom=2.54cm,
  left=3.17cm, right=3.17cm
]{geometry}  % 1 inch = 2.54cm
```

### 标题格式参数

#### titlesec 包配置

```latex
\usepackage{titlesec}

% 格式: \titleformat{命令}[形状]{格式}{标签}{间距}[前代码]

% H1 - 一级标题
\titleformat{\section}
  {\normalfont\Large\bfseries\color{blue!70!black}}  % 格式
  {这些ction\hspace{0.5em}}                           % 标签（如 "1."）
  {0em}                                                % 标签与标题间距
  {}                                                   % 后代码（钩子）

% H2 - 二级标题
\titleformat{\subsection}
  {\normalfont\large\bfseries}
  {thesubsection\hspace{0.3em}}
  {0em}
  {}

% H3 - 三级标题
\titleformat{\subsubsection}
  {\normalfont\normalsize\bfseries\itshape}
  {thesubsubsection\hspace{0.2em}}
  {0em}
  {}
```

**标题间距控制**:
```latex
\titlespacing*{\section}{左缩进}{前间距}{后间距}[右缩进]

% 示例
\titlespacing*{\section}{0pt}{24pt plus 2pt minus 2pt}{12pt plus 2pt minus 2pt}
% 左缩进: 0pt (不缩进)
% 前间距: 24pt (±2pt 弹性)
% 后间距: 12pt (±2pt 弹性)
```

### 代码块参数

#### listings 包高级配置

```latex
\lstset{
  % 语言定义
  language=Python,              % 默认语言
  morekeywords={async, await},  % 额外关键字
  
  % 字体样式
  basicstyle=\ttfamily\small,   % 基础样式
  keywordstyle=\color{blue}\bfseries,  % 关键字
  stringstyle=\color{red},             % 字符串
  commentstyle=\color{codecomment}\itshape,  % 注释
  numberstyle=\tiny\color{gray},        % 行号
  
  % 布局
  frame=single,                % 边框
  framerule=0.5pt,             % 边框粗细
  rulecolor=\color{gray},      % 边框颜色
  backgroundcolor=\color{white}, % 背景色
  breaklines=true,             % 自动换行
  breakatwhitespace=true,      % 在空白处换行
  tabsize=4,                   % Tab 宽度
  showstringspaces=false,      % 不显示空格标记
  
  % 行号
  numbers=left,                % 左侧行号
  numbersep=8pt,               % 行号与代码距离
  stepnumber=1,                % 每几行一个号
  numberfirstline,             % 第一行也编号
  
  % 边距
  xleftmargin=1.5em,           % 左边距
  xrightmargin=1em,            % 右边距
  aboveskip=1em,               % 上方间距
  belowskip=0.5em              % 下方间距
}
```

**多语言支持**:
```latex
\lstdefinestyle{python}{
  language=Python,
  morekeywords={self, True, False, None}
}

\lstdefinestyle{javascript}{
  language=[ECMAScript]6,
  morekeywords={const, let, async, await, =>}
}

\lstdefinestyle{bash}{
  language=bash,
  morekeywords={sudo, apt, npm, pip}
}

% 在代码块中指定语言
\begin{lstlisting}[style=python]
def hello():
    print("Hello World")
\end{lstlisting}
```

---

## 自定义模板开发

### 从零创建模板

#### 步骤 1: 导出基础模板

```bash
pandoc -D latex > templates/my-custom.latex
```

#### 步骤 2: 理解模板语法

Pandoc 模板使用特殊的变量和条件语法：

```latex
% 变量替换
$title$
$author$
$date$

% 条件判断
$if(title)$
  \title{$title$}
$endif$

% 循环
$for(author)$
  $author$$sep$, 
$endfor$

% 正文占位符
$body$
```

#### 步骤 3: 修改关键部分

**修改区域清单**:
1. ✅ `\documentclass` - 文档类和全局选项
2. ✅ 字体设置 - 中文字体和英文字体
3. ✅ geometry - 页面布局
4. ✅ hyperref - 超链接和元数据
5. ✅ titlesec - 标题格式
6. ✅ fancyhdr - 页眉页脚
7. ✅ listings - 代码高亮
8. ✅ `\begin{document}` ... `\end{document}` - 文档结构

#### 步骤 4: 测试模板

```bash
# 创建测试 Markdown 文件
cat > test.md << 'EOF'
---
title: 测试文档
author: 测试者
date: 2026-05-31
---

# 第一章 测试

这是一个测试段落。

## 1.1 小节测试

```python
print("Hello World")
```
EOF

# 使用新模板编译
pandoc test.md \
  --to pdf \
  --template=templates/my-custom.latex \
  --pdf-engine=xelatex \
  -o test-output.pdf

# 打开预览
open test-output.pdf  # macOS
xdg-open test-output.pdf  # Linux
start test-output.pdf  # Windows
```

### 模板变量参考表

#### 文档信息变量

| 变量 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `$title$` | string | 文档标题 | `"RAG 教程"` |
| `$author$` | list/string | 作者列表 | `["张三", "李四"]` |
| `$date$` | string | 日期 | `"2026-05-31"` |
| `$subtitle$` | string | 副标题 | `"从入门到精通"` |
| `$abstract$` | string | 摘要 | `"本书介绍..."` |
| `$keywords$` | list | 关键词 | `["RAG", "AI"]` |

#### 功能开关变量

| 变量 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `$toc$` | boolean | false | 是否生成目录 |
| `$toc-depth$` | number | 3 | 目录深度 |
| `$number-sections$` | boolean | false | 是否编号 |
| `$links-as-notes$` | boolean | false | 链接转脚注 |
| `$colorlinks$` | boolean | true | 彩色链接 |

#### 样式变量

| 变量 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `$fontsize$` | string | "10pt" | 基础字号 |
| `$mainfont$` | string | (auto) | 主字体 |
| `$monofont$` | string | (auto) | 等宽字体 |
| `$geometry$` | string | (auto) | 页面布局 |
| `$linestretch$` | number | 1.0 | 行距倍数 |
| `$documentclass$` | string | "article" | 文档类 |

#### 高级变量

| 变量 | 类型 | 说明 |
|------|------|------|
| `$header-includes$` | list | 头部插入的 LaTeX 代码 |
| `$include-before$` | list | 正文前的内容 |
| `$include-after$` | list | 正文后的内容 |
| `$body$` | 特殊 | Markdown 转换后的正文 |

### 模板调试技巧

#### 查看实际生成的 LaTeX

```bash
# 只生成 LaTeX 不编译
pandoc input.md --to latex --template=my-template.latex -o output.tex

# 查看并手动编译
xelatex output.tex
```

#### 定位错误来源

```bash
# 1. 使用最小化模板测试
pandoc input.md --to pdf -o minimal.pdf  # 不使用自定义模板

# 如果成功 → 问题在模板中
# 如果失败 → 问题在输入文件中

# 2. 分段注释模板代码
% 注释掉可疑的部分
% \usepackage{problematic-package}

# 3. 查看详细错误日志
--pdf-engine-opt="-interaction=nonstopmode"
--log=debug.log
```

---

## 学术模板扩展

### 论文模板需求

当需要生成学术论文时，可以基于默认模板扩展：

```latex
% 学术论文扩展模板
\documentclass[12pt,a4paper,twoside]{report}

% 添加摘要环境
\newenvironment{abstract}{
  \chapter*{摘 要}
  \addcontentsline{toc}{chapter}{摘 要}
  \begin{quote}
}{
  \end{quote}
}

% 添加参考文献
\usepackage[backend=biber,style=numeric]{biblatex}
\addbibresource{references.bib}

% 图表标题格式
\usepackage{caption}
\captionsetup{
  font=small,
  labelfont=bf,
  format=hang,
  justification=centering
}

% 定理环境
\usepackage{amsthm}
\newtheorem{theorem}{定理}[section]
\newtheorem{definition}{定义}[section]
\newtheorem{lemma}{引理}[section]

\begin{document}

% 封面页
\maketitle

% 声明
\chapter*{声 明}
...

% 摘要
\begin{abstract}
  本文研究...
\end{abstract}

% 目录
\tableofcontents

% 插图目录
\listoffigures

% 表格目录
\listoftables

% 正文
$body%

% 参考文献
\printbibliography

% 致谢
\chapter*{致 谢}
...

\end{document}
```

### 期刊模板集成

许多期刊提供官方 LaTeX 模板，可以通过以下方式集成：

```bash
# 下载期刊模板（以 IEEE 为例）
wget https://www.ieee.org/documents/IEEEtran.zip
unzip IEEEtran.zip -d templates/

# 使用期刊模板
pandoc input.md \
  --to pdf \
  --template=templates/IEEEtran.cls \
  --pdf-engine=xelatex \
  -o ieee-paper.pdf
```

---

## 企业品牌模板

### 品牌元素定制

为企业和组织定制品牌化的 PDF 模板：

```latex
% 企业品牌模板示例
\documentclass[a4paper,11pt]{article}

% ===== 品牌颜色定义 =====
\definecolor{brandprimary}{HTML}{0052CC}    % 主色 (Atlassian 蓝)
\definecolor{brandsecondary}{HTML}{00B8D9}   % 辅色
\definecolor{brandaccent}{HTML}{36B37E}      # 强调色

% ===== Logo 配置 =====
\usepackage{background}
\backgroundsetup{
  position=current page.north east,
  nodeanchor=north east,
  angle=0,
  scale=1,
  opacity=0.1,
  contents={\includegraphics[width=3cm]{logo.png}}
}

% ===== 品牌字体 =====
\setmainfont{BrandSerif}
\setsansfont{BrandSans}
\setmonofont{BrandMono}

% ===== 页眉带 Logo =====
\fancyhead[L]{
  \includegraphics[height=0.8cm]{logo.png}\hspace{1em}
  \leftmark
}

% ===== 页脚版权信息 =====
\fancyfoot[C]{\tiny © 2026 公司名称. All rights reserved.}

% ===== 标题使用品牌色 =====
\titleformat{\section}{
  \normalfont\Large\bfseries\color{brandprimary}
}{...}{...}{...}

\begin{document}
...
\end{document}
```

### 多品牌支持

```bash
# 根据环境变量选择模板
BRAND_TEMPLATE="${BRAND:-default}"
pandoc input.md \
  --template="templates/${BRAND_TEMPLATE}.latex" \
  ...
```

---

## 最佳实践

### ✅ 模板管理建议

1. **版本控制**
   ```bash
   git add templates/*.latex
   git commit -m "Update template: improve code block styling"
   ```

2. **模块化设计**
   ```
   templates/
   ├── base.latex              # 基础模板
   ├── chinese-support.sty     # 中文支持模块
   ├── code-highlighting.sty   # 代码高亮模块
   ├── page-layout.sty         # 页面布局模块
   └── brand-{name}.sty        # 品牌模块
   ```

3. **文档化**
   - 在模板头部添加注释说明用途
   - 记录修改历史
   - 提供使用示例

### ⚠️ 常见陷阱

1. **宏包冲突**
   - ctex 和某些宏包可能冲突
   - 解决：仔细阅读宏包文档，按正确顺序加载

2. **字体缺失**
   - 自定义字体在其他机器上可能不存在
   - 解决：使用通用字体或嵌入字体

3. **XeLaTeX vs pdfLaTeX**
   - XeLaTeX 使用不同的字体机制
   - 解决：始终使用 XeLaTeX 并用 `\setmainfont`

4. **编码问题**
   - 确保 UTF-8 编码
   - 解决：`\usepackage[utf8]{inputenc}` (pdfLaTeX) 或直接 UTF-8 (XeLaTeX)

### 📚 学习资源

- [LaTeX Wikibook](https://en.wikibooks.org/wiki/LaTeX)
- [Overleaf Documentation](https://www.overleaf.com/learn)
- [CTAN (Comprehensive TeX Archive Network)](https://ctan.org/)
- [Pandoc Templates](https://pandoc.org/MANUAL.html#templates)

---

> **相关文档**:
> - [Pandoc 详细配置](pandoc-configuration.md) - 命令行和过滤器
> - [PDF 排版样式指南](pdf-styling.md) - 视觉样式细节
> - [问题排查手册](troubleshooting.md) - 故障诊断
>
> **返回主文档**: [SKILL.md](../SKILL.md)
