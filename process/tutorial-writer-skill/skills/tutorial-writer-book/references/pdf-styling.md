# PDF 排版样式指南

> **版本**: v1.0.0 | **最后更新**: 2026-05-31
> **适用范围**: Tutorial Writer Book 子技能

## 目录

- [排版设计原则](#排版设计原则)
- [字体系统](#字体系统)
- [层级结构](#层级结构)
- [段落和间距](#段落和间距)
- [代码块样式](#代码块样式)
- [表格设计](#表格设计)
- [图片处理](#图片处理)
- [数学公式](#数学公式)
- [引用和注释](#引用和注释)
- [打印优化](#打印优化)
- [可访问性](#可访问性)

---

## 排版设计原则

### 核心目标

PDF 电子书的排版应遵循以下原则：

1. **可读性优先**
   - 舒适的字号和行距
   - 清晰的视觉层次
   - 合适的行长（每行 60-80 字符）

2. **专业性**
   - 一致的样式规范
   - 精确的对齐和间距
   - 高质量的字体渲染

3. **品牌一致性**
   - 符合教程项目的整体风格
   - 与网站版本保持视觉连贯

4. **打印友好**
   - 避免纯装饰性元素
   - 考虑黑白打印效果
   - 优化分页控制

### 设计度量标准

| 指标 | 推荐值 | 说明 |
|------|--------|------|
| 正文字号 | 10-11pt | 标准阅读大小 |
| 行距 | 1.5-1.6倍 | 舒适阅读 |
| 行长 | 60-80字符 | 最佳阅读体验 |
| 段落间距 | 0.5-1em | 区分段落 |
| 页边距 | 2-3cm | 标准学术/书籍 |
| 标题缩进 | 0pt (居左) | 现代风格 |

---

## 字体系统

### 字体族配置

#### 中文字体选择

**推荐字体组合**:

| 用途 | 主选字体 | 备选字体 | 特点 |
|------|---------|---------|------|
| 正文衬线 | Noto Serif CJK SC | Source Han Serif CN | 传统、正式 |
| 正文无衬线 | Noto Sans CJK SC | PingFang SC | 现代、清晰 |
| 标题粗体 | Noto Sans CJK SC Bold | Heiti SC | 强调、醒目 |
| 代码等宽 | Noto Sans Mono CJK SC | JetBrains Mono | 技术、专业 |

**字体安装检查**:
```bash
# macOS
fc-list :lang=zh family style | grep -E "(Noto|PingFang|Heiti)"

# Linux
fc-list :lang=zh family

# Windows (PowerShell)
[System.Drawing.FontFamily]::Families | Where-Object { $_.Name -like "*Noto*" }
```

#### 英文字体搭配

**最佳实践**:
```latex
% 中文正文 + 英文无衬线
\setCJKmainfont{Noto Serif CJK SC}
\setmainfont{TeX Gyre Termes}          % Times 类似字体

% 或中文无衬线 + 英文无衬线
\setCJKmainfont{Noto Sans CJK SC}
\setmainfont{TeX Gyre Heros}           % Helvetica 类似字体
```

#### 代码字体

**推荐等宽字体**:

| 字体 | 特点 | 适用场景 |
|------|------|---------|
| JetBrains Mono | 连字支持、清晰 | 现代 IDE 风格 |
| Fira Code | 大量连字 | 编程展示 |
| Source Code Pro | Adobe 出品 | 学术/技术文档 |
| Consolas | Windows 预装 | 兼容性优先 |
| Monaco | macOS 预装 | Apple 生态 |

### 字号体系

#### 层级化字号

```latex
% 基础字号: 11pt
\documentclass[11pt]{article}

% 各级标题字号
\titleformat{\section}{\Large\bfseries}{...}     % ~18pt
\titleformat{\subsection}{\large\bfseries}{...}   % ~14pt
\titleformat{\subsubsection}{\normalsize\bfseries}{...}  % ~11pt

% 正文
% 11pt (基础字号)

% 小字文本
\small    % ~9pt  (注释、图注)
\footnotesize  % ~8pt  (脚注、版权信息)
\tiny     % ~5pt  (极小信息)
```

**字号对比表**:

| 元素 | 相对大小 | 绝对值 (11pt 基础) | 使用场景 |
|------|---------|-------------------|---------|
| H1 | \Large | 18pt | 章节标题 |
| H2 | \large | 14pt | 小节标题 |
| H3 | \normalsize | 11pt | 三级标题 |
| 正文 | \normalsize | 11pt | 段落文本 |
| 注释 | \small | 9pt | 旁注、提示 |
| 图注 | \footnotesize | 8pt | 图片说明 |
| 脚注 | \scriptsize | 7pt | 页面底部 |

---

## 层级结构

### 标题系统

#### 视觉层级

```
H1 (章节标题)
├── 24pt / Bold / 上方 24pt 间距
│
├── H2 (小节标题)
│   ├── 18pt / Bold / 上方 18pt 间距
│   │
│   ├── H3 (子节标题)
│   │   ├── 14pt / Bold / 上方 12pt 间距
│   │   │
│   │   └── 正文段落
│   │       └── 11pt / Regular / 首行缩进
│   │
│   └── 正文段落
│
└── 正文段落
```

#### LaTeX 实现

```latex
\usepackage{titlesec}

% H1: 章节标题 - 最醒目
\titleformat{\section}[block]
  {\normalfont\Large\bfseries\color{black}}
  {这些ction\hspace{0.8em}}        % "第1章 "
  {0em}
  {}
\titlespacing*{\section}{
  0pt                              % 左边距
  {24pt plus 4pt minus 4pt}       % 前间距 (弹性)
  {12pt plus 2pt minus 2pt}       % 后间距
}

% H2: 小节标题 - 次级强调
\titleformat{\subsection}[hang]
  {\normalfont\large\bfseries\color{black!85}}
  {thesubsection\hspace{0.6em}}   % "1.1 "
  {0em}
  {}
\titlespacing*{\subsection}{
  0pt
  {18pt plus 3pt minus 3pt}
  {10pt plus 2pt minus 2pt}
}

% H3: 子节标题 - 轻微强调
\titleformat{\subsubsection}[hang]
  {\normalfont\normalsize\bfseries\color{black!70}}
  {thesubsubsection\hspace{0.4em}} % "1.1.1 "
  {0em}
  {}
\titlespacing*{\subsubsection}{
  0pt
  {12pt plus 2pt minus 2pt}
  {6pt plus 1pt minus 1pt}
}

% H4 及以下: 加粗行内文本 (不单独成段)
\titleformat{\paragraph}[runin]
  {\normalfont\normalsize\bfseries\itshape\color{black!60}}
  {theparagraph}{0em}
  {: }                             % 冒号分隔
\titlespacing*{\paragraph}{
  0pt
  {8pt plus 2pt minus 1pt}
  {0pt}                            % 不换行
}
```

### 分隔线使用

```latex
% H1 下划线
\titleformat{\section}{
  \normalfont\Large\bfseries
}{
  这些ction\hspace{0.8em}
}{0em}{
  \titlerule[1.5pt]               % 1.5pt 实线下划线
}

% H2 下划线（更细）
\titleformat{\subsection}{
  \normalfont\large\bfseries
}{
  thesubsection\hspace{0.6em}
}{0em}{
  \titlerule[0.8pt]               % 0.8pt 细线
}
```

---

## 段落和间距

### 缩进和对齐

#### 中文排版惯例

```latex
% 首行缩进 2 个字符（中文标准）
\setlength{\parindent}{2em}

% 或者使用相对单位
\setlength{\parindent}{2\ccwd}    % \ccwd = 当前字符宽度

% 西文排版：首行不缩进，用空行分段
\setlength{\parindent}{0pt}
\setlength{\parskip{0.5em}}

% 推荐：混合模式（中文缩进 + 段落间距）
\setlength{\parindent}{2em}
\setlength{\parskip{0.3em plus 0.1em minus 0.1em}
```

#### 对齐方式

```latex
% 两端对齐（默认，最常用）
\raggedright                       % 左对齐（代码示例）
\centering                         % 居中（短文本）
\raggedleft                        % 右对齐（特殊情况）

% 自动调整单词间距以实现两端对齐
\sloppy                            % 减少过度连字符
\frenchspacing                    % 句号后不增加额外空格
```

### 行距设置

#### 标准行距值

| 场景 | 行距倍数 | Pandoc 参数 | 适用性 |
|------|---------|------------|--------|
| 标准 | 1.5 | `-V linestretch=1.5` | 技术文档 ⭐⭐⭐⭐⭐ |
| 宽松 | 1.8 | `-V linestretch=1.8` | 轻松阅读 |
| 紧凑 | 1.3 | `-V linestretch=1.3` | 节省空间 |
| 双倍 | 2.0 | `-V linestretch=2.0` | 校对稿 |

**LaTeX 设置**:
```latex
% 全局行距
\linespread{1.5}                  % 1.5 倍行距

% 或使用 setspace 包（更精确）
\usepackage{setspace}
\onehalfspacing                   % 1.5 倍
\doublespacing                    % 2.0 倍
\setstretch{1.6}                  % 自定义值

% 仅对特定部分调整
{
  \setstretch{1.3}
  这段文字使用紧凑行距。
}
```

### 段落间距控制

```latex
% 固定间距
\setlength{\parskip{0.5em}}       % 段间 0.5em

% 弹性间距（允许 TeX 微调）
\setlength{\parskip{0.5em plus 0.2em minus 0.2em}}

% 标题前后间距（已在 titlesec 配置）
% 参见"层级结构"章节

% 列表环境间距
\usepackage{enumitem}
\setlist{
  noitemsep,                      % 列表项之间无额外间距
  topsep=0.3em,                   % 列表前间距
  parsep=0.2em                     % 段落间间距
}
```

---

## 代码块样式

### 内联代码

**Markdown 语法**:
```markdown
使用 `const app = express()` 创建 Express 应用。
```

**渲染效果要求**:
- 背景: `#F5F5F5` (浅灰)
- 内边距: `0.15em 0.4em`
- 圆角: `3px`
- 字体: 等宽字体，比正文小 1-2pt
- 颜色: 与正文相同或略深

**LaTeX 实现**:
```latex
% 使用 listings 的 \lstinline 或自定义命令
\newcommand{\code}[1]{%
  \tikz[baseline=(text.base)]{
    \node[fill=gray!10, rounded corners=2pt, inner sep=2pt] (text) {
      \texttt{\small #1}
    };
  }%
}

% 使用: \code{variable_name}
```

### 代码块

#### 基础样式

```markdown
```javascript
// JavaScript 示例
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```
```

**视觉规范**:

| 属性 | 值 | 说明 |
|------|-----|------|
| 背景色 | #F5F5F5 | 浅灰背景 |
| 边框 | 1px solid #E0E0E0 | 细边框 |
| 圆角 | 4-6px | 轻微圆角 |
| 内边距 | 1em 1.2em | 舒适空间 |
| 字体 | JetBrains Mono, 9pt | 等宽字体 |
| 行高 | 1.4 | 紧凑但清晰 |
| 最大宽度 | 100% | 自适应容器 |

#### 语法高亮主题

**Tango 主题配色** (推荐):

| 元素 | 颜色 | 十六进制 |
|------|------|----------|
| 关键字 | 蓝色 | #0000FF |
| 字符串 | 深红 | #A31515 |
| 注释 | 绿色 | #008000 |
| 数字 | 深绿 | #098658 |
| 函数名 | 黑色 | #000000 |
| 类型 | 蓝黑 | #267F99 |
| 背景 | 浅灰 | #F5F5F5 |

**LaTeX listings 配置**:
```latex
\definecolor{codebg}{HTML}{F5F5F5}
\definecolor{codeborder}{HTML}{E0E0E0}
\definecolor{keywordblue}{HTML}{0000FF}
\definecolor{stringred}{HTML}{A31515}
\definecolor{commentgreen}{HTML}{008000}
\definecolor{numbergreen}{HTML}{098659}

\lstset{
  backgroundcolor=\color{codebg},
  frame=single,
  rulecolor=\color{codeborder},
  keywordstyle=\color{keywordblue}\bfseries,
  stringstyle=\color{stringred},
  commentstyle=\color{commentgreen}\itshape,
  numberstyle=\tiny\color{numbergreen},
  basicstyle=\ttfamily\footnotesize,
  breaklines=true,
  showstringspaces=false,
  tabsize=2,
  xleftmargin=1em,
  xrightmargin=1em,
  aboveskip=1em,
  belowskip=0.5em
}
```

#### 行号显示

**启用行号**:
```bash
pandoc ... --listings \
  -V listings:numbers=left \
  -V listings:numberstyle=\tiny\color{gray} \
  -V listings:numbersep=8pt \
  -V listings:stepnumber=1
```

**行号样式选项**:
- `none` - 无行号（默认）
- `left` - 左侧行号
- `right` - 右侧行号

#### 代码块标题

```markdown
```javascript {.file-name="app.js"}
// 代码内容
```
```

**显示文件名的 Lua 过滤器**:
```lua
-- filters/code-caption.lua
function CodeBlock(block)
  local filename = block.attributes["file-name"]
  if filename then
    local caption = pandoc.Para({
      pandoc.Str("📄 "),
      pandoc.Code(filename, ""),
      pandoc.Str(" (点击复制)")
    })
    return {caption, block}
  end
  return block
end
```

---

## 表格设计

### 基础表格样式

**Markdown 语法**:
```markdown
| 功能 | 描述 | 示例 |
|------|------|------|
| 查询 | RAG 检索 | `vector_store.search()` |
| 生成 | LLM 输出 | `llm.generate(prompt)` |
| 组合 | 完整流程 | `rag_chain.query("问题")` |
```

**视觉规范**:

| 属性 | 值 | 说明 |
|------|-----|------|
| 边框 | 1px solid #DDD | 细灰边框 |
| 表头背景 | #F5F5F5 | 浅灰区分 |
| 表头字体 | Bold | 加粗强调 |
| 单元格内边距 | 0.6em 0.8em | 舒适间距 |
| 斑马纹 | 奇数行 #FAFAFA | 提升可读性 |
| 对齐 | 左(文本)/居中(数字) | 符合习惯 |

**LaTeX booktabs 实现**:
```latex
\usepackage{booktabs}
\usepackage{colortbl}

% 斑马纹表格
\rowcolors{2}{white}{gray!5}      % 从第2行开始交替

\begin{table}[htbp]
\centering
\caption{功能对比表}
\label{tab:features}
\begin{tabular}{lll}
\toprule
\textbf{功能} & \textbf{描述} & \textbf{示例} \\
\midrule
查询 & RAG 检索 & \texttt{vector\_store.search()} \\
生成 & LLM 输出 & \texttt{llm.generate(prompt)} \\
组合 & 完整流程 & \texttt{rag\_chain.query()} \\
\bottomrule
\end{tabular}
\end{table}
```

### 高级表格特性

#### 合并单元格

```latex
\usepackage{multirow}
\usepackage{multicol}

\begin{tabular}{|c|c|c|}
\hline
\multirow{2}{*}{跨两行} & 第一列 & 第二列 \\
\cline{2-3}
& 内容 A & 内容 B \\
\hline
\end{tabular}
```

#### 自适应宽度

```latex
\usepackage{tabularx}

\begin{tabularx}{\textwidth}{X X X}
% X 列自动填充剩余空间
\end{tabularx}
```

#### 长表格（跨页）

```latex
\usepackage{longtable}

\begin{longtable}{lll}
\caption{长表格标题} \\
\toprule
列 1 & 列 2 & 列 3 \\
\midrule
\endfirsthead  % 首页表头
\multicolumn{3}{c}{续表} \\
\toprule
列 1 & 列 2 & 列 3 \\
\midrule
\endhead       % 续页表头
% 表格内容...
\bottomrule
\end{longtable}
```

---

## 图片处理

### 图片插入规范

**Markdown 语法**:
```markdown
![RAG 架构图](../assets/images/rag-architecture.png){ width=80% }

图 1-1: RAG 系统整体架构
```

**尺寸指南**:

| 类型 | 推荐宽度 | 最大高度 | DPI |
|------|---------|---------|-----|
| 架构图 | 70-90% | 页面的 50% | 150 |
| 流程图 | 80-100% | 页面的 40% | 150 |
| 截图 | 100% | 页面的 60% | 144 |
| 图标 | 1-2cm | 2cm | 300 |
| Logo | 2-3cm | 1.5cm | 300 |

### 图片优化

#### 减小体积

```bash
# PNG 优化
optipng -o7 input.png -o output.png

# JPEG 压缩
convert input.png -quality 85 output.jpg

# 调整分辨率（屏幕显示 150 DPI 即可）
convert input.png -density 150 -resize 1200x1200 output.png

# SVG 转 PNG（如果 PDF 渲染有问题）
inkscape input.svg --export-type=png --export-dpi=150 --export-filename=output.png
```

#### 图片位置控制

```latex
% 强制图片在此处（避免浮动）
\usepackage{float}
\begin{figure}[H]              % H = Here (绝对位置)
  \centering
  \includegraphics[width=0.8\textwidth]{image.png}
  \caption{图片说明}
  \label{fig:example}
\end{figure}

% 或使用更宽松的浮动策略
\begin{figure}[htbp]           % h=here, t=top, b=bottom, p=page
  ...
\end{figure}
```

### 图注格式

```latex
\usepackage{caption}

\captionsetup{
  font=small,                   % 图注字号
  labelfont=bf,                 % "图 1-1" 加粗
  format=hang,                  % 悬挂缩进
  justification=centering,      % 居中对齐
  margin=1cm,                   % 左右边距
  skip=10pt                     % 与图片的间距
}

% 自定义标签格式
\renewcommand{\figurename}{图}
% 输出: "图 1-1" 而非 "Figure 1.1"
```

---

## 数学公式

### 行内公式

**Markdown 语法**:
```markdown
爱因斯坦质能方程 $E = mc^2$ 是物理学中最著名的公式之一。
```

**渲染效果**: 爱因斯坦质能方程 *E = mc²* 是物理学中最著名的公式之一。

### 块级公式

**Markdown 语法**:
$$
\mathcal{L}(\theta) = -\frac{1}{N} \sum_{i=1}^{N} \left[ y_i \log(\hat{y}_i) + (1-y_i) \log(1-\hat{y}_i) \right]
$$

**公式编号**:
$$
\int_{-\infty}^{+\infty} e^{-x^2} dx = \sqrt{\pi} \tag{1.1}
$$

### 公式样式优化

```latex
\usepackage{amsmath}
\usepackage{amssymb}

% 公式字体大小
\everymath{\displaystyle}         % 所有公式使用 displaystyle

% 公式颜色（用于强调）
\newcommand{\highlight}[1]{\textcolor{red}{#1}}

% 使用: $\highlight{x^2}$

% 多行公式对齐
\begin{align}
  f(x) &= ax^2 + bx + c \\
       &= a(x - h)^2 + k \notag
\end{align}
```

---

## 引用和注释

### 块引用

**Markdown 语法**:
```markdown
> RAG (Retrieval-Augmented Generation) 是一种结合检索和生成的 AI 架构，
> 能够显著提升大语言模型的准确性和可靠性。
>
> —— Lewis et al., 2020
```

**样式规范**:

| 属性 | 值 |
|------|-----|
| 左边框 | 4px solid #3178C6 (TypeScript 蓝) |
| 背景色 | #F0F7FF (极淡蓝) |
| 内边距 | 1em 1.5em |
| 字体斜度 | Italic |
| 字体颜色 | #555 (深灰) |
| 字号 | Normal (不变) |

**LaTeX 实现**:
```latex
\usepackage{tcolorbox}

\newtcolorbox{quote}{
  colback=blue!5,
  colframe=blue!75!black,
  leftrule=4mm,
  arc=0mm,
  boxrule=0pt,
  fontupper=\itshape\color{black!70},
  left=8pt,
  right=8pt,
  top=4pt,
  bottom=4pt
}

% 使用
\begin{quote}
  \begin{quote}
    引用的文本内容...
  \end{quote}
  \hfill —— 作者, 年份
\end{quote}
```

### 脚注

**Markdown 语法**:
```markdown
RAG 技术最早由 Facebook AI Research 提出[^1]，并在 2020 年发表在 NeurIPS 会议上。

[^1]: Lewis, P., et al. "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." NeurIPS 2020.
```

**样式设置**:
```latex
% 脚注格式
\renewcommand{\thefootnote}{\arabic{footnote}}  % 阿拉伯数字
\setlength{\footnotesep}{8pt}                    % 脚注间距
\deffootnote{1.5em}{1em}{\thefootmark.\ }        % 格式: "1. "

% 脚注字号
\renewcommand{\footnotelayout}{\fontsize{8pt}{10pt}\selectfont}
```

### 提示框（Callout）

**自定义提示框类型**:

```markdown
::: tip 💡 提示
这是一个有用的提示信息。
:::

::: warning ⚠️ 注意
需要注意的重要事项。
:::

::: error ❌ 错误
可能导致问题的错误用法。
:::
```

**LaTeX tcolorbox 实现**:
```latex
\usepackage[most]{tcolorbox}

% 提示框
\newtcolorbox{tip}[1][]{
  colback=green!5,
  colframe=green!50!black,
  fonttitle=\bfseries,
  title={#1},
  before upper={\parindent0pt}
}

% 警告框
\newtcolorbox{warning}[1][]{
  colback=yellow!10,
  colframe=orange!80!black,
  fonttitle=\bfseries,
  title={#1},
  before upper={\parindent0pt}
}

% 错误框
\newtcolorbox{error}[1][]{
  colback=red!5,
  colframe=red!75!black,
  fonttitle=\bfseries,
  title={#1},
  before upper={\parindent0pt}
}

% 使用
\begin{tip}[💡 提示]
有用的提示信息...
\end{tip}
```

---

## 打印优化

### 分页控制

#### 避免不良分页

```latex
% 孤行寡行控制
\usepackage[all]{nowidow}
\widowpenalty=1000              % 孤行惩罚
\clubpenalty=1000               # 寡行惩罚
\brokenpenalty=1000             % 断词惩罚

% 防止元素跨页断裂
\begin{table}[htbp]
  \centering
  \begin{tabular}{...}
  \end{tabular}
\end{table}

% 代码块不分页
\lstset{
  frame=single,
  breakatwhitespace=false,      % 不在空白处分页
  postbreak=\space             % 分页后添加空格
}
```

#### 手动分页控制

```markdown
<!-- 强制在新页面开始 -->
\newpage

<!-- 在此之前完成当前章节 -->
<!-- 可能需要分页 -->
\pagebreak[0]                   % 0 = 尽可能但不强制

% LaTeX 中
\clearpage                      % 强制清空浮动体并分页
\cleardoublepage                % 双面打印时从奇数页开始
```

### 打印友好的颜色

**黑白打印适配**:
```css
@media print {
  body {
    color: #000 !important;
    background: #fff !important;
  }
  
  /* 将彩色转为灰色 */
  h1, h2, h3 {
    color: #000 !important;
    border-bottom: 2px solid #000 !important;
  }
  
  code {
    background: #eee !important;
    border: 1px solid #999 !important;
  }
  
  a[href]:after {
    content: " (" attr(href) ")";  /* 打印链接地址 */
  }
}
```

**LaTeX 打印模式**:
```latex
% 定义打印模式命令
\newif\ifprintmode
\printmodefalse                  % 默认: 彩色模式

% 启用打印模式
\printmodetrue

\ifprintmode
  % 黑白配色方案
  \definecolor{primary}{HTML}{000000}
  \definecolor{secondary}{HTML}{333333}
  \definecolor{accent}{HTML}{666666}
\else
  % 彩色配色方案
  \definecolor{primary}{HTML}{0052CC}
  \definecolor{secondary}{HTML}{00B8D9}
  \definecolor{accent}{HTML}{36B37E}
\fi
```

### 页码和导航

**页码样式**:
```latex
% 阿拉伯数字（正文）
\pagenumbering{arabic}

% 罗马数字（前言）
\pagenumbering{roman}

% 重置页码
\setcounter{page}{1}

% 自定义页码格式
\renewcommand{\thepage}{\arabic{page}/\pageref{LastPage}}
% 显示为 "1/156"
```

---

## 可访问性

### PDF/A 标准

生成符合存档标准的 PDF：

```bash
# 使用 Ghostscript 转换为 PDF/A-2b
gs -dPDFA -dPDFACompatibilityPolicy=2 \
   -sDEVICE=pdfwrite \
   -dNOPAUSE -dBATCH \
   -sOutputFile=output-pdfa.pdf \
   input.pdf
```

### 书签和元数据

确保 PDF 包含完整的导航结构：

```bash
--toc                          % 生成目录
-V bookmarks=true              % 生成书签
-V bookmark-level=2            % 书签起始级别
-V bookmarks-numbered=true     % 书签带编号
-V bookmarks-open-level=1      % 默认展开到第 1 层
```

### 字体嵌入

```bash
# 嵌入所有字体（确保在任何设备上正确显示）
-V embed-fonts=true

# 只嵌入使用的字符（减小体积）
-V subset-fonts=true

# 检查是否已嵌入
pdffonts output.pdf | head -20
```

### 替代文本

为图片添加描述（辅助阅读器）:

```markdown
![系统架构图：包含用户界面、API 服务、数据库三层](architecture.png){ width=80% }
```

---

## 样式检查清单

### ✅ 发布前检查项

- [ ] 字体在目标平台可用（或已嵌入）
- [ ] 所有图片清晰且路径正确
- [ ] 代码块语法高亮正常
- [ ] 表格不溢出页面边界
- [ ] 公式渲染完整且清晰
- [ ] 目录页码准确
- [ ] 超链接可点击且有效
- [ ] 页眉页脚信息正确
- [ ] 孤行寡行控制在合理范围
- [ ] 文件大小合理 (< 50MB 为佳)

### 📏 排版质量指标

| 指标 | 优秀 | 良好 | 需改进 |
|------|------|------|--------|
| 可读性得分 | > 90 | 75-90 | < 75 |
| 视觉一致性 | 完全一致 | 基本一致 | 不一致 |
| 信息密度 | 适中 | 可接受 | 过密/过疏 |
| 专业程度 | 出版级 | 准出版级 | 初级 |

---

> **相关文档**:
> - [Pandoc 详细配置](pandoc-configuration.md) - 命令行参数
> - [LaTeX 模板库](latex-templates.md) - 模板开发
> - [问题排查手册](troubleshooting.md) - 故障诊断
>
> **返回主文档**: [SKILL.md](../SKILL.md)
