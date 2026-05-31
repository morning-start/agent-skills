# 问题排查手册

> **版本**: v1.0.0 | **最后更新**: 2026-05-31
> **适用范围**: Tutorial Writer Book 子技能

## 目录

- [诊断流程](#诊断流程)
- [环境问题](#环境问题)
- [Pandoc 问题](#pandoc-问题)
- [XeLaTeX 编译错误](#xelatex-编译错误)
- [字体相关问题](#字体相关问题)
- [内容渲染问题](#内容渲染问题)
- [PDF 输出质量问题](#pdf-输出质量问题)
- [性能问题](#性能问题)
- [CI/CD 问题](#cicd-问题)
- [调试工具和技巧](#调试工具和技巧)

---

## 诊断流程

### 系统化排查步骤

当遇到 PDF 生成问题时，按照以下流程进行诊断：

```
Step 1: 环境检查
    ↓ Pandoc 是否安装？版本是否足够？XeLaTeX 可用？
    ↓
Step 2: 输入验证
    ↓ Markdown 文件是否存在？格式是否正确？路径是否有效？
    ↓
Step 3: 最小化测试
    ↓ 使用最简单的命令测试：echo "test" | pandoc -o test.pdf
    ↓
Step 4: 逐步增加复杂度
    ↓ 添加字体、模板、选项等，定位问题引入点
    ↓
Step 5: 查看详细日志
    ↓ 启用 verbose 模式，查看 LaTeX 日志
    ↓
Step 6: 隔离变量
    ↓ 逐一排除可能的原因（字体、图片、宏包等）
```

### 快速诊断脚本

```bash
#!/bin/bash
# diagnose.sh - PDF 生成环境诊断工具

echo "=========================================="
echo "📋 Tutorial Writer Book 诊断报告"
echo "=========================================="
echo ""

# 1. 检查 Pandoc
echo "📦 Pandoc 检查:"
if command -v pandoc &>/dev/null; then
  PANDOC_VERSION=$(pandoc --version | head -1)
  echo "  ✅ 已安装: $PANDOC_VERSION"
  
  # 版本检查
  PANDOC_MAJOR=$(pandoc --version | head -1 | grep -oE '[0-9]+\.[0-9]+' | cut -d'.' -f1)
  if [[ "$PANDOC_MAJOR" -ge 3 ]] || [[ "$PANDOC_MAJOR" == "2" && $(echo "$PANDOC_VERSION" | grep -oE '\.[0-9]+' | head -1 | cut -d'.' -f2) -ge 17 ]]; then
    echo "  ✅ 版本满足要求 (>= 2.17)"
  else
    echo "  ⚠️ 版本过低，建议升级到 >= 2.17"
  fi
else
  echo "  ❌ 未安装 Pandoc"
fi
echo ""

# 2. 检查 XeLaTeX
echo "📝 XeLaTeX 检查:"
if command -v xelatex &>/dev/null; then
  XELATEX_VERSION=$(xelatex --version | head -1)
  echo "  ✅ 已安装: $XELATEX_VERSION"
else
  echo "  ❌ 未安装 XeLaTeX"
fi
echo ""

# 3. 检查中文字体
echo "🔤 中文字体检查:"
if command -v fc-list &>/dev/null; then
  CJK_FONTS=$(fc-list :lang=zh family | sort -u | head -5)
  if [[ -n "$CJK_FONTS" ]]; then
    echo "  ✅ 找到中文字体:"
    echo "$CJK_FONTS" | sed 's/^/     /'
  else
    echo "  ⚠️ 未找到中文字体（可能影响中文显示）"
  fi
else
  echo "  ⚠️ 无法检测字体（fc-list 不可用）"
fi
echo ""

# 4. 检查项目结构
echo "📁 项目结构检查:"
REQUIRED_DIRS=("packages/content/src/chapters" "packages/book")
for dir in "${REQUIRED_DIRS[@]}"; do
  if [[ -d "$dir" ]]; then
    CHAPTER_COUNT=$(find "$dir" -name "*.md" -type f 2>/dev/null | wc -l)
    echo "  ✅ $dir/ ($CHAPTER_COUNT 个 Markdown 文件)"
  else
    echo "  ❌ $dir/ 不存在"
  fi
done
echo ""

# 5. 内存检查
echo "💾 系统资源:"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  TOTAL_MEM=$(free -g | awk '/^Mem:/{print $2}')
  echo "  总内存: ${TOTAL_MEM}GB"
  if [[ "$TOTAL_MEM" -lt 4 ]]; then
    echo "  ⚠️ 内存可能不足（建议 >= 4GB）"
  else
    echo "  ✅ 内存充足"
  fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
  TOTAL_MEM=$(sysctl -n hw.memsize | awk '{print $1/1024/1024/1024 " GB"}')
  echo "  总内存: $TOTAL_MEM"
fi
echo ""

echo "=========================================="
echo "诊断完成！请根据上述信息解决问题。"
echo "=========================================="
```

**使用方法**:
```bash
chmod +x diagnose.sh
./diagnose.sh
```

---

## 环境问题

### 操作系统特定问题

#### macOS

**问题**: Homebrew 安装的 TeX Live 不完整

**症状**:
```
! LaTeX Error: File `xeCJK.sty' not found.
```

**解决方案**:
```bash
# 方案 A: 使用完整版 MacTeX
brew uninstall --cask basictex
brew install --cask mactex

# 方案 B: 手动安装缺失的包
sudo tlmgr install xeCJK ctex

# 方案 C: 切换到 BasicTeX 并手动添加
brew install --cask basictex
sudo tlmgr install scheme-full  # 完整安装所有包（耗时较长）
```

**问题**: 字体缓存过期

**解决方案**:
```bash
# 更新字体缓存
sudo atsutil databases -remove
sudo atsutil server -shutdown
sudo atsutil server -start
```

#### Ubuntu/Debian

**问题**: apt 安装缺少中文支持

**症状**: 中文显示为方框或乱码

**解决方案**:
```bash
# 安装完整的中文支持
sudo apt-get install -y \
  texlive-xetex \
  texlive-lang-chinese \
  texlive-fonts-recommended \
  texlive-fonts-extra \
  fonts-noto-cjk \
  fonts-wqy-zenhei \
  fonts-wqy-microhei

# 刷新字体缓存
sudo fc-cache -f -v
```

**问题**: 权限问题导致无法写入 TeX 目录

**解决方案**:
```bash
# 添加用户到 texgroup（如果存在）
sudo usermod -aG tex $(whoami)

# 或修改 TEXMFHOME 到用户目录
export TEXMFHOME=$HOME/texmf
mkdir -p $TEXMFHOME
```

#### Windows

**问题**: MiKTeX 自动安装失败

**症状**:
```
The package xxx could not be installed.
```

**解决方案**:
```powershell
# 方法 1: 使用 Chocolatey 安装完整版
choco uninstall miktex
choco install miktex -y --params="'/INSTALLERPATH=C:\Program Files\MiKTeX'"

# 方法 2: 手动配置自动安装
# 打开 MiKTeX Console → Settings → Always install missing packages on-the-fly → Yes

# 方法 3: 预先下载所有依赖包
miktexsetup --shared=yes basic
tlmgr install <package-name>
```

**问题**: 路径中的中文或空格字符

**症状**: 命令执行失败但无明确错误信息

**解决方案**:
```powershell
# 避免在路径中使用中文和空格
# 错误: C:\Users\张三\我的文档\tutorial\
# 正确: C:\tutorials\my-project\

# 或使用短路径名
cd "C:\Users\张三\我的文档\tutorial\"
# 获取短路径
cmd /c for %I in ("%CD%") do @echo %~sI
```

---

## Pandoc 问题

### 安装和版本问题

#### 错误 1: Pandoc 未找到

**错误信息**:
```
bash: pandoc: command not found
```

**诊断**:
```bash
which pandoc          # Linux/macOS
where pandoc           # Windows PowerShell
```

**解决方案**:

| 平台 | 安装方法 |
|------|---------|
| macOS | `brew install pandoc` |
| Ubuntu | `sudo apt-get update && sudo apt-get install pandoc` |
| Windows | `choco install pandoc` 或 `scoop install pandoc` |

**验证安装**:
```bash
pandoc --version
# 应输出: pandoc 3.x.x
```

#### 错误 2: 版本过低

**症状**: 缺少某些功能或参数不被识别

**诊断**:
```bash
pandoc --version | head -1
# 如果显示 pandoc 2.x 且 x < 17，则需要升级
```

**升级方法**:
```bash
# macOS
brew upgrade pandoc

# Ubuntu (如果仓库版本过旧)
# 添加官方 PPA 或从源码编译
wget https://github.com/jgm/pandoc/releases/download/3.1.9/pandoc-3.1.9-1-amd64.deb
sudo dpkg -i pandoc-3.1.9-1-amd64.deb

# Windows
choco upgrade pandoc
```

### 参数解析错误

#### 错误 3: 无效的参数

**错误信息**:
```
pandoc: unrecognized option '--invalid-option'
```

**常见原因**:
- 参数拼写错误
- 使用了不支持的旧版参数
- 参数值格式不正确

**解决方案**:
```bash
# 查看帮助文档确认正确参数名
pandoc --help | grep -i "toc"

# 示例: 正确的 TOC 参数
--toc                    # 正确
--table-of-contents      # 错误（不存在）
```

#### 错误 4: 文件编码问题

**症状**: 中文乱码、特殊字符丢失

**诊断**:
```bash
file input.md
# 应输出: input.md: UTF-8 Unicode text

# 如果不是 UTF-8
iconv -f GBK -t UTF-8 input.md > input-utf8.md
```

**解决方案**:
```bash
# 确保 Markdown 文件是 UTF-8 编码
# VS Code: 右下角点击编码 → UTF-8
# Vim: :set fileencoding=utf-8

# 强制指定输入编码
pandoc input.md --from markdown+smart ... -o output.pdf
```

---

## XeLaTeX 编译错误

### 宏包相关错误

#### 错误 5: 缺少宏包

**错误信息示例**:
```
! LaTeX Error: File `geometry.sty' not found.

Type X to quit or <RETURN> to try next,
or type <command> for help.
```

**解决方案**:

**TeX Live**:
```bash
# 自动安装缺失的宏包
sudo tlmgr install geometry

# 批量安装常用宏包
sudo tlmgr install \
  geometry hyperref fancyhdr titlesec \
  booktabs listings xcolor graphicx \
  amsmath amssymb nowidow tocloft
```

**MiKTeX**:
```powershell
# 方法 1: 通过 MiKTeX Console
# 打开 MiKTeX Console → Packages → 搜索包名 → 安装

# 方法 2: 命令行（需要管理员权限）
mpm --install=geometry
```

**预防措施**:
```bash
# 创建宏包依赖列表文件 packages.txt
geometry
hyperref
fancyhdr
titlesec
booktabs
listings
xcolor
graphicx
amsmath
amssymb
nowidow
tocloft
ctex
xeCJK

# 批量安装
cat packages.txt | xargs sudo tlmgr install
```

#### 错误 6: 宏包冲突

**症状**: 编译成功但有警告，或输出异常

**常见冲突组合**:
- `ctex` 与 `CJK` 宏包
- `hyperref` 与其他超链接宏包
- 多个 `titlesec` 配置

**诊断**:
```bash
# 查看 LaTeX 日志中的警告
grep -i "warning" build.log | head -20

# 查看宏包加载顺序
grep -i "\\\\usepackage" default.latex | head -20
```

**解决方案**:
```latex
% 解决方案 1: 移除冗余宏包
% \usepackage{CJK}  % 与 ctex 冲突，删除此行

% 解决方案 2: 调整加载顺序
% hyperref 应该最后加载
\usepackage{...}
\usepackage{hyperref}  % 放在最后

% 解决案 3: 使用 \PassOptionsToPackage
\PassOptionsToPackage{colorlinks}{hyperref}
\usepackage{hyperref}
```

### 字体相关错误

#### 错误 7: 字体未找到

**错误信息**:
```
! Font "Noto Sans CJK SC" does not contain requested Script "CJK".
```

**诊断步骤**:
```bash
# 1. 检查字体是否安装
fc-list | grep -i "noto sans cjk sc"

# 2. 检查字体名称是否完全匹配
fc-list :lang=zh family style

# 3. 测试 XeLaTeX 能否找到字体
echo '\documentclass{article}\usepackage{fontspec}\setmainfont{Noto Sans CJK SC}\begin{document}测试\end{document}' | xelatex -jobname=test-font
```

**解决方案**:

**方案 A: 安装正确的字体**
```bash
# macOS
brew install --cask font-noto-sans-cjk-sc

# Ubuntu
sudo apt-get install -y fonts-noto-cjk

# Windows
# 从 Google Noto Fonts 下载并手动安装
```

**方案 B: 使用备选字体**
```bash
# 根据操作系统选择可用字体
case "$OSTYPE" in
  darwin*)
    FONT="PingFang SC"
    ;;
  msys*|cygwin*)
    FONT="Microsoft YaHei"
    ;;
  linux*)
    FONT="Noto Sans CJK SC"
    ;;
esac

pandoc ... -V mainfont="$FONT"
```

**方案 C: 使用字体回退机制**
```latex
% 在 LaTeX 模板中使用条件判断
\IfFontExistsTF{Noto Sans CJK SC}{
  \setmainfont{Noto Sans CJK SC}
}{
  \setmainfont{SimSun}  % 回退到宋体
}
```

### 编译过程错误

#### 错误 8: 编译卡住/无限循环

**症状**: XeLaTeX 进程长时间运行无输出

**原因分析**:
- 存在交叉引用循环
- 复杂表格或公式导致内存耗尽
- 文件过大超出处理能力

**解决方案**:

**立即终止**:
```bash
# 按 Ctrl+C 终止进程
# 或强制杀死
killall xelatex
```

**防止再次发生**:
```bash
# 限制编译时间（超时）
timeout 300 pandoc ... --to pdf -o output.pdf  # 5 分钟超时

# 减少编译次数
--pdf-engine-opt="-interaction=nonstopmode"

# 分块处理大文档
# 将长文档拆分为多个部分分别编译
```

#### 错误 9: 内存不足

**错误信息**:
```
! TeX capacity exceeded, sorry [main memory size=<number>].
```

**解决方案**:

**方案 A: 增加 LaTeX 内存限制**:
```bash
# Unix/Linux/macOS
export TEXMFVAR=~/.texlive/texmf-var
xelatex --extra-mem-bot=10000000 input.tex

# Windows (CMD)
set TEXMFVAR=%USERPROFILE%\texlive\texmf-var
xelatex --extra-mem-bot=10000000 input.tex
```

**方案 B: 优化文档以减少内存使用**:
```bash
# 禁用不必要的功能
--no-highlight              # 禁用代码高亮
-V draft-mode=true         # 草稿模式（不加载图片）
-V embed-fonts=false        # 不嵌入字体

# 减小图片分辨率
convert image.png -resize 50% image-small.png
```

**方案 C: 拆分文档**:
```bash
# 按章节拆分
for i in {1..10}; do
  pandoc ch${i}.md --to pdf -o part${i}.pdf
done

# 合并 PDF
pdftk part*.pdf cat output full.pdf
```

---

## 字体相关问题

### 中文字体乱码

#### 错误 10: 显示为方框 □□□

**根本原因**: XeLaTeX 无法找到或渲染指定的中文字体

**完整修复流程**:

```bash
#!/bin/bash
# fix-chinese-fonts.sh

echo "🔧 开始修复中文字体问题..."

# Step 1: 检测系统可用的中文字体
echo ""
echo "📋 检测到的中文字体:"
AVAILABLE_FONTS=$(fc-list :lang=zh family | sort -u)
if [[ -z "$AVAILABLE_FONTS" ]]; then
  echo "  ❌ 未找到任何中文字体"
  echo ""
  echo "正在尝试安装 Noto Sans CJK SC..."
  
  if [[ "$OSTYPE" == "darwin"* ]]; then
    brew install --cask font-noto-sans-cjk-sc || {
      echo "⚠️ Homebrew 安装失败，请手动安装字体"
      exit 1
    }
  elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt-get install -y fonts-noto-cjk || {
      echo "⚠️ apt 安装失败，请手动安装字体"
      exit 1
    }
  else
    echo "❌ 请手动安装中文字体后重试"
    exit 1
  fi
  
  # 刷新字体缓存
  sudo fc-cache -f -v
else
  echo "$AVAILABLE_FONTS" | sed 's/^/  ✅ /'
fi

# Step 2: 选择最佳字体
echo ""
echo "🎯 推荐字体配置:"
if fc-list | grep -q "Noto Sans CJK SC"; then
  MAIN_FONT="Noto Sans CJK SC"
  MONO_FONT="Noto Sans Mono CJK SC"
elif fc-list | grep -q "PingFang SC"; then
  MAIN_FONT="PingFang SC"
  MONO_FONT="Menlo"
elif fc-list | grep -q "Microsoft YaHei"; then
  MAIN_FONT="Microsoft YaHei"
  MONO_FONT="Consolas"
elif fc-list | grep -q "WenQuanYi Zen Hei"; then
  MAIN_FONT="WenQuanYi Zen Hei"
  MONO_FONT="WenQuanYi Micro Hei Mono"
else
  echo "⚠️ 使用系统默认字体"
  MAIN_FONT="SimSun"
  MONO_FONT="SimSun"
fi

echo "  正文字体: $MAIN_FONT"
echo "  代码字体: $MONO_FONT"

# Step 3: 生成测试文件
cat > font-test.md << EOF
---
title: 字体测试
---
# 中文字体测试

这是正文内容，应该正常显示中文。

## 代码块测试

\`\`\`javascript
console.log("中文代码注释");
\`\`\`

## 数学公式测试

$$ E = mc^2 $$

EOF

# Step 4: 测试编译
echo ""
echo "🔄 测试编译..."
pandoc font-test.md \
  --from markdown \
  --to pdf \
  --output font-test.pdf \
  --pdf-engine=xelatex \
  -V mainfont="$MAIN_FONT" \
  -V monofont="$MONO_FONT" \
  --toc

if [[ $? -eq 0 ]]; then
  echo ""
  echo "✅ 字体配置成功！生成的测试文件: font-test.pdf"
  echo ""
  echo "请在未来的 Pandoc 命令中使用以下参数:"
  echo "  -V mainfont=\"$MAIN_FONT\""
  echo "  -V monofont=\"$MONO_FONT\""
else
  echo ""
  echo "❌ 编译仍然失败，请查看上方错误信息"
  exit 1
fi

# 清理临时文件
rm -f font-test.md font-test.aux font-test.log font-test.out font-test.toc
```

**使用方法**:
```bash
chmod +x fix-chinese-fonts.sh
./fix-chinese-fonts.sh
```

### 字体嵌入问题

#### 错误 11: PDF 在其他设备上无法显示字体

**症状**: 在创建机器上正常，在其他电脑上字体变成默认字体

**解决方案**:
```bash
# 嵌入所有使用的字体
pandoc ... -V embed-fonts=true

# 只嵌入实际使用的字符子集（减小体积）
pandoc ... -V subset-fonts=true

# 验证字体是否已嵌入
pdffonts output.pdf | head -20
# 查找 "embedded" 列，应为 "yes"
```

---

## 内容渲染问题

### 图片相关问题

#### 错误 12: 图片无法显示

**可能原因及解决方案**:

**原因 1: 路径错误**
```markdown
# 错误: 绝对路径
![图](C:/Users/name/image.png)

# 错误: 相对路径不正确
![图](./image.png)  # 如果图片不在当前目录

# 正确: 相对于 Markdown 文件的路径
![图](../assets/images/arch.png)
```

**解决方法**:
```bash
# 指定资源搜索路径
pandoc ... --resource-path=.:../assets/images:images

# 或使用绝对路径（基于项目根目录）
pandoc ... --resource-path=$(pwd)/packages/content/src/assets
```

**原因 2: 图片格式不支持**

XeLaTeX 直接支持: PNG, JPG, PDF, EPS

对于 SVG 格式需要转换:
```bash
# 使用 Inkscape 转换
inkscape diagram.svg --export-type=png --export-dpi=150 --export-filename=diagram.png

# 或使用 rsvg-convert (更轻量)
rsvg-convert -f png -d 150 -o diagram.png diagram.svg
```

**原因 3: 图片文件损坏或过大**
```bash
# 检查图片文件
file image.png
# 应输出: image.png: PNG image data, ...

# 如果过大 (>10MB)，进行压缩
convert image.png -resize 1200x1200 -quality 85 image-compressed.png
```

#### 错误 13: 图片位置不当

**症状**: 图片出现在错误的位置或跨页断裂

**解决方案**:
```latex
% 在 LaTeX 模板中控制浮动行为
\usepackage{float}

% 强制图片在此位置（不浮动）
\begin{figure}[H]
  \centering
  \includegraphics[width=0.8\textwidth]{image.png}
  \caption{说明文字}
\end{figure}

% 允许浮动但限制范围
\begin{figure}[htbp]  % h=here, t=top, b=bottom, p=page
  ...
\end{figure}
```

### 代码块渲染问题

#### 错误 14: 语法高亮不工作

**症状**: 代码块没有颜色，或颜色不正确

**解决方案**:
```bash
# 确保启用了高亮
pandoc ... --highlight-style=tango

# 如果仍无效，检查 listings 包配置
# 在 LaTeX 模板中确保已加载:
\usepackage{listings}
\usepackage{xcolor}
```

**自定义高亮失效时**:
```bash
# 退回到内置主题
--highlight-style=tango  # 尝试不同的主题

# 或完全禁用以排查问题
--no-highlight            # 如果禁用后能编译，说明问题在高亮配置
```

#### 错误 15: 代码块溢出页面边界

**解决方案**:
```latex
% 启用自动换行
\lstset{
  breaklines=true,
  breakatwhitespace=true,
  postbreak=\hfill\space,  % 对齐续行
  breakindent=1em           % 缩进续行
}

% 或减小字号
\lstset{
  basicstyle=\ttfamily\tiny  % 使用更小的字号
}
```

### 目录和书签问题

#### 错误 16: 目录为空或不完整

**原因**: Markdown 文件中没有足够的标题层级

**检查清单**:
```markdown
# 必须有 H1 标题
## 可以有 H2
### 可以有 H3
#### H4 及以下可选
```

**解决方案**:
```bash
# 确保启用目录
pandoc ... --toc --toc-depth=3

# 检查 Markdown 文件是否有标题
grep "^#" chapters/*.md | head -20

# 如果标题使用了 = 或 - 下划线语法，转换为 #
# 旧: 标题文本
# ========
# 新: # 标题文本
```

#### 错误 17: 目录页码不准确

**原因**: LaTeX 的交叉引用需要多次编译才能解析

**解决方案**:
```bash
# 方法 1: 运行两次 Pandoc
pandoc ... -o output.pdf
pandoc ... -o output.pdf

# 方法 2: 手动运行 XeLaTeX 两次
pandoc ... -o output.tex
xelatex output.tex
xelatex output.tex

# 方法 3: 使用 make 工具自动化
Makefile:
output.pdf: chapters/*.md
	pandoc $^ --to pdf -o output.pdf
	pandoc $^ --to pdf -o output.pdf
```

---

## PDF 输出质量问题

### 视觉问题

#### 错误 18: 页边距不正确

**症状**: 内容被裁剪或留白过多

**诊断**:
```bash
# 检查实际页面尺寸
pdfinfo output.pdf | grep "Page size"

# 应输出类似: Page size:      595 x 842 pts (A4)
```

**解决方案**:
```bash
# 明确指定页面布局
pandoc ... \
  -V geometry:a4paper \
  -V geometry:margin=2.5cm \
  -V geometry:top=2.5cm \
  -V geometry:bottom=2.5cm \
  -V geometry:left=2.5cm \
  -V geometry:right=2.5cm
```

#### 错误 19: 文件体积过大

**目标**: PDF 文件应 < 50MB（理想 < 20MB）

**诊断**:
```bash
ls -lh output.pdf
# 查看文件大小

# 分析占用空间的内容
pdfimages -list output.pdf | head -20
# 查看嵌入的图片及其大小
```

**优化策略**:

**1. 压缩图片**:
```bash
# 降低 DPI（屏幕阅读 150 即可）
for img in assets/images/*.png; do
  convert "$img" -density 150 -resize 1200x1200 "${img%.png}-opt.png"
done

# JPEG 有损压缩（适合照片）
convert photo.png -quality 85 photo.jpg
```

**2. 嵌入字体子集化**:
```bash
pandoc ... -V subset-fonts=true

# 或使用 Ghostscript 后处理
gs -sDEVICE=pdfwrite \
   -dCompatibilityLevel=1.4 \
   -dPDFSETTINGS=/ebook \
   -dNOPAUSE -dBATCH \
   -sOutputFile=output-compressed.pdf \
   output.pdf
```

**3. 移除元数据**:
```bash
# 使用 qpdf 清理
qpdf --empty --pages output.pdf -- clean.pdf
```

### 功能性问题

#### 错误 20: 超链接不可点击

**解决方案**:
```bash
# 确保 hyperref 已正确配置
pandoc ... \
  -V header-includes="\usepackage{hyperref}" \
  -V colorlinks=true \
  -V linkcolor=blue \
  -V urlcolor=blue

# 检查 PDF 阅读器设置
# Adobe Acrobat: 编辑 → 首选设置 → 一般 → 基本工具 → 选择 → 链接
```

#### 错误 21: 搜索功能不工作

**原因**: PDF 可能是扫描件图像而非文本层

**诊断**:
```bash
# 尝试提取文本
pdftotext output.pdf -
# 如果无输出，说明 PDF 中没有可搜索的文本
```

**解决方案**:
```bash
# 确保不是通过打印方式生成的 PDF
# 应该直接从源文件转换，而非打印到 PDF
```

---

## 性能问题

### 编译速度慢

#### 优化策略

**1. 减少 LaTeX 编译次数**:
```bash
# 使用 batchmode 减少交互式暂停
--pdf-engine-opt="-interaction=batchmode"

# 使用 draftmode（不生成最终输出，仅检查错误）
--pdf-engine-opt="-draftmode"
```

**2. 缓存中间结果**:
```bash
#!/bin/bash
# incremental-build.sh

CONTENT_DIR="packages/content/src/chapters"
OUTPUT_PDF="dist/tutorial.pdf"
HASH_FILE=".content-hash"

# 计算内容的哈希值
CURRENT_HASH=$(find "$CONTENT_DIR" -name "*.md" -type f -exec md5sum {} \; | md5sum | cut -d' ' -f1)

# 检查是否有变化
if [[ -f "$HASH_FILE" ]]; then
  PREVIOUS_HASH=$(cat "$HASH_FILE")
  if [[ "$CURRENT_HASH" == "$PREVIOUS_HASH" ]]; then
    echo "✅ 内容未变化，跳过构建"
    exit 0
  fi
fi

echo "🔄 检测到内容变化，开始构建..."

# 执行构建
pandoc $(find "$CONTENT_DIR" -name "*.md" | sort) ... -o "$OUTPUT_PDF"

# 保存哈希值
echo "$CURRENT_HASH" > "$HASH_FILE"
echo "✅ 构建完成"
```

**3. 并行处理** (适用于批量生成):
```bash
# GNU Parallel
find chapters -name "*.md" | parallel -j 4 'pandoc {} --to pdf -o {.}.pdf'

# 或使用 xargs
find chapters -name "*.md" | print0 | xargs -0 -P 4 -I{} pandoc {} ...
```

**4. 使用 Turborepo 缓存**:
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

### 大文档处理

#### 拆分策略

**按章节拆分**:
```bash
#!/bin/bash
# split-and-merge.sh

INPUT_DIR="chapters"
OUTPUT_DIR="dist"

# 创建临时目录
TEMP_DIR=$(mktemp -d)

# 按章节编号分组
declare -a VOLUMES
VOLUME_1=($(ls "$INPUT_DIR"/0[1-3]*.md 2>/dev/null))
VOLUME_2=($(ls "$INPUT_DIR"/0[4-6]*.md 2>/dev/null))
VOLUME_3=($(ls "$INPUT_DIR"/0[7-9]*.md 2>/dev/null))

# 分别编译
if [[ ${#VOLUME_1[@]} -gt 0 ]]; then
  echo "📗 编译第一部分 (基础篇)..."
  pandoc "${VOLUME_1[@]}" ... -o "$TEMP_DIR/volume-1.pdf"
fi

if [[ ${#VOLUME_2[@]} -gt 0 ]]; then
  echo "📘 编译第二部分 (进阶篇)..."
  pandoc "${VOLUME_2[@]}" ... -o "$TEMP_DIR/volume-2.pdf"
fi

if [[ ${#VOLUME_3[@]} -gt 0 ]]; then
  echo "📙 编译第三部分 (实战篇)..."
  pandoc "${VOLUME_3[@]}" ... -o "$TEMP_DIR/volume-3.pdf"
fi

# 合并为完整 PDF
echo "📚 合并所有部分..."
if ls "$TEMP_DIR"/*.pdf 1>/dev/null 2>&1; then
  pdftk "$TEMP_DIR"/*.pdf cat output "$OUTPUT_DIR/full-tutorial.pdf"
  echo "✅ 完整教程已生成: $OUTPUT_DIR/full-tutorial.pdf"
fi

# 清理
rm -rf "$TEMP_DIR"
```

---

## CI/CD 问题

### GitHub Actions 特有问题

#### 错误 22: TeX Live 安装耗时过长

**问题**: CI 流水线中每次都重新安装 TeX Live (~5-10分钟)

**解决方案**: 缓存 TeX Live

```yaml
- name: Cache TeX Live
  id: cache-tex
  uses: actions/cache@v4
  with:
    path: |
      ~/texlive
      ~/.texlive/var
    key: texlive-${{ runner.os }}-${{ hashFiles('**/.tex-version') }}
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
```

#### 错误 23: 中文字体在 CI 中不可用

**症状**: 本地正常，CI 环境中文乱码

**解决方案**:
```yaml
- name: Install Chinese Fonts
  run: |
    sudo apt-get install -y fonts-noto-cjk
    sudo fc-cache -f -v
    
    # 验证字体安装
    fc-list :lang=zh | head -5
```

#### 错误 24: 构建产物上传失败

**解决方案**:
```yaml
- name: Upload PDF Artifact
  uses: actions/upload-artifact@v4
  with:
    name: tutorial-pdf
    path: dist/tutorial.pdf
    retention-days: 30
    if-no-files-found: warn  # 即使文件不存在也不失败

- name: Create Release
  if: startsWith(github.ref, 'refs/tags/')
  uses: softprops/action-gh-release@v1
  with:
    files: dist/tutorial.pdf
    fail_on_unmatched_files: false  # 文件不存在时不失败
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 调试工具和技巧

### 日志收集

**启用详细日志**:
```bash
# Pandoc 详细模式
pandoc --verbose input.md -o output.pdf

# LaTeX 详细日志
pandoc ... --log=build.log --pdf-engine-opt="-interaction=nonstopmode"

# 查看日志的关键部分
grep -E "(Error|Warning|Missing)" build.log | head -50
```

**日志分析工具**:
```bash
#!/bin/bash
# analyze-log.sh

LOGFILE="${1:-build.log}"

echo "📊 LaTeX 日志分析报告"
echo "====================="
echo ""

# 统计错误数量
ERRORS=$(grep -c "!.*Error" "$LOGFILE" 2>/dev/null || echo "0")
echo "❌ 错误数: $ERRORS"

# 统计警告数量
WARNINGS=$(grep -c "Warning:" "$LOGFILE" 2>/dev/null || echo "0")
echo "⚠️ 警告数: $WARNINGS"

# 统计缺失的包
MISSING_PKGS=$(grep -oP "File `\K[^']+(?='\.sty)" "$LOGFILE" | sort -u)
if [[ -n "$MISSING_PKGS" ]]; then
  echo ""
  echo "📦 缺失的宏包:"
  echo "$MISSING_PKGS" | sed 's/^/   - /'
fi

# 统计缺失的字体
MISSING_FONTS=$(grep -oP "Font `\K[^']+'" "$LOGFILE" | sort -u)
if [[ -n "$MISSING_FONTS" ]]; then
  echo ""
  echo "🔤 缺失的字体:"
  echo "$MISSING_FONTS" | sed 's/^/   - /'
fi

echo ""
echo "🔍 前 10 条错误/警告:"
grep -E "(!.*Error|Warning:)" "$LOGFILE" | head -10 | sed 's/^/   /'
```

### 中间结果检查

**查看 AST (抽象语法树)**:
```bash
# 查看 Pandoc 如何解析你的 Markdown
pandoc input.md -t native | less

# 查看生成的 LaTeX 代码
pandoc input.md -t latex -o intermediate.tex

# 手动编译 LaTeX 以获取更详细的错误信息
xelatex interaction=nonstopmode intermediate.tex
```

**隔离问题来源**:
```bash
# 最小化测试
echo "# Test\n\nHello 世界" | pandoc --from markdown --to pdf -o minimal.pdf

# 如果最小测试成功 → 问题在你的输入文件
# 如果最小测试失败 → 问题在环境配置

# 逐步添加复杂性
echo "# Test\n\nHello \`code\`" | pandoc ... -o test1.pdf
echo "# Test\n\nHello \`code\`\n\n![img](test.png)" | pandoc ... -o test2.pdf
```

### 性能分析

**测量编译时间**:
```bash
# 使用 time 命令
time pandoc input.md -o output.pdf

# 或使用更详细的统计
/usr/bin/time -v pandoc input.md -o output.pdf 2>&1 | grep -E "(Maximum resident|Elapsed)"

# 分析瓶颈
# 1. Pandoc 解析时间
time pandoc input.md -t native > /dev/null

# 2. LaTeX 编译时间
time xelatex intermediate.tex
```

### 常用快速修复命令

```bash
# 🔄 清理辅助文件（解决残留文件导致的奇怪问题）
rm -f *.aux *.log *.out *.toc *.lof *.lot *.bbl *.bcf *.blg *.run.xml *.synctex.gz

# 🔄 刷新字体缓存
sudo fc-cache -f -v

# 🔄 重置 TeX Live（如果遇到奇怪的包冲突）
sudo tlmgr conf texmf TEXMFVAR ~/.texlive/texmf-var

# 🔍 查找占用空间最大的文件
du -ah . | sort -rh | head -20

# 📊 分析 PDF 结构
pdfinfo output.pdf
pdfimages -list output.pdf | wc -l  # 图片数量
pdffonts output.pdf | wc -l         # 字体数量
```

---

## 故障速查表

### 按症状查找

| 症状 | 可能原因 | 快速解决方案 |
|------|---------|-------------|
| `command not found` | 未安装 | 安装 Pandoc/XeLaTeX |
| 中文显示为 □□□ | 字体缺失 | 安装 Noto Sans CJK SC |
| 编译卡住 | 内存不足/死循环 | Ctrl+C, 拆分文档 |
| `File not found` | 缺失宏包 | `tlmgr install <pkg>` |
| 图片不显示 | 路径错误 | 检查 `--resource-path` |
| 目录为空 | 缺少标题 | 检查 Markdown 的 `#` 标题 |
| PDF 过大 | 图片未压缩 | 压缩图片至 150 DPI |
| 链接不可点击 | hyperref 未加载 | 添加 `-V header-includes` |
| CI 失败 | 环境差异 | 添加缓存和字体安装步骤 |

### 按错误消息查找

| 错误关键字 | 章节 | 优先级 |
|-----------|------|--------|
| `command not found` | [环境问题](#环境问题) | 🔴 高 |
| `File .* not found` | [XeLaTeX 编译错误](#xelatex-编译错误) | 🔴 高 |
| `Font .* not found` | [字体相关问题](#字体相关问题) | 🔴 高 |
| `capacity exceeded` | [XeLaTeX 编译错误](#xelatex-编译错误) | 🟡 中 |
| `undefined control sequence` | [XeLaTeX 编译错误](#xelatex-编译错误) | 🟡 中 |
| `Missing \$ inserted` | [内容渲染问题](#内容渲染问题) | 🟢 低 |

---

## 获取帮助

### 自助资源

1. **Pandoc 官方文档**: https://pandoc.org/MANUAL.html
2. **TeX Stack Exchange**: https://tex.stackexchange.com/
3. **CTAN 宏包库**: https://ctan.org/
4. **本项目文档**: [SKILL.md](../SKILL.md)

### 报告问题

如果以上方法都无法解决问题，请收集以下信息：

```bash
# 1. 系统信息
uname -a
pandoc --version
xelatex --version

# 2. 完整的错误日志
pandoc ... --log=full-debug.log 2>&1

# 3. 最小复现示例
# 创建一个最小的 Markdown 文件能够触发相同的问题

# 4. 环境
cat diagnose.sh | bash  # 运行诊断脚本
```

---

> **相关文档**:
> - [Pandoc 详细配置](pandoc-configuration.md) - 参数和配置
> - [LaTeX 模板库](latex-templates.md) - 模板开发
> - [PDF 排版样式指南](pdf-styling.md) - 视觉样式
>
> **返回主文档**: [SKILL.md](../SKILL.md)
