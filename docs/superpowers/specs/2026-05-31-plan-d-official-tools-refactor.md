# Tutorial Writer v1.0.0 — Plan D 重构设计文档

> **设计日期**: 2026-05-31
> **方案**: Plan D (Official Tools + AI Orchestration)
> **类型**: 内部重构（消除维护负担）
> **版本影响**: 保持 v1.0.0 不变
> **状态**: ✅ 已批准

---

## 1. 执行摘要

### 1.1 重构目标

将 Tutorial Writer 从 **Plan C (自定义脚本 + 硬编码模板)** 升级到 **Plan D (官方工具链 + AI 编排)**：

- ❌ 删除自定义初始化系统 (scripts/ + templates/ = ~4000 行)
- ✅ 改用官方 CLI 工具链 (`create-turbo` + `turbo gen` + `create-astro`)
- ✅ 将命令序列内嵌到根路由器 SKILL.md (~120 行新增)
- ✅ 精简 monorepo-guide.md (2633 → ~300 行, -89%)

### 1.2 核心价值

| 维度 | Before (Plan C) | After (Plan D) |
|------|-----------------|----------------|
| **维护负担** | 🔴 高（需同步官方更新） | 🟢 **零维护** |
| **时效性** | 模板快照易过时 | **永远最新** |
| **代码量** | ~24,000 行 | **~17,500 行** (-27%) |
| **灵活性** | 固定参数 | AI 动态调整 |
| **学习曲线** | 需学自定义脚本 | 用标准工具 |

---

## 2. 变更清单

### 2.1 完全删除的内容

```
❌ process/tutorial-writer-skill/scripts/
    └── init-tutorial.sh                    (1002 行)
    原因: 被 create-turbo + turbo gen + create-astro 替代

❌ process/tutorial-writer-skill/templates/
    └── tutorial-starter/                   (24 个文件, ~3000 行)
    ├── turbo.json                          ← create-turbo 自动生成
    ├── pnpm-workspace.yaml                 ← create-turbo 自动生成
    ├── package.json                        ← create-turbo 自动生成
    ├── tsconfig.base.json                  ← create-turbo 自动生成
    ├── .gitignore                          ← create-turbo 自动生成
    ├── .editorconfig                       ← create-turbo 自动生成
    ├── README.md                           ← create-turbo 自动生成
    └── packages/
        ├── content/ (4 files)              ← turbo gen workspace 生成
        │   └── config.ts                   ⚠️ 已迁移到 content/references/
        ├── web/ (9 files)                  ← create-astro 生成
        │   └── astro.config.mjs            ⚠️ 示例保留在 web/SKILL.md
        └── book/ (5 files)                 ← turbo gen workspace 生成
            ├── generate-pdf.sh             ⚠️ 逻辑已在 book/SKILL.md
            ├── templates/default.latex      ⚠️ 已迁移到 book/references/
            └── styles/pdf.css               ⚠️ 已迁移到 book/references/

删除总计: 25 个文件/目录, ~4000 行代码
```

### 2.2 新增/修改的内容

#### 2.2.1 根路由器 SKILL.md — 新增"项目初始化"章节

**位置**: `process/tutorial-writer-skill/SKILL.md`
**变更**: 在现有内容后新增 ~120 行
**章节结构**:

```markdown
## 🚀 项目初始化 (Official Tools)

> **重要**: 使用官方 CLI 工具链创建项目，确保始终使用最新版本。

### 初始化流程概览
[Mermaid 流程图: Step 0 → Step 6]

### Step 0: 前置环境检查
[Node.js 版本、包管理器检查]

### Step 1: 创建 Monorepo 骨架
[create-turbo 命令 + 验证]

### Step 2: 添加 content 包
[turbo gen workspace 命令]

### Step 3: 创建 web 包
[create-astro --template starlight 命令]

### Step 4: 添加 book 包
[turbo gen workspace 命令]

### Step 5: 配置 Workspace 依赖
[package.json 依赖声明示例]

### Step 6: 注入 Tutorial Writer 配置
[指向 /content 和 /book 子技能的详细配置]

### 验证清单
[7 项检查点]

### 常见问题
[3 个 FAQ]
```

**具体命令序列**:

```bash
# Step 1: 创建 Monorepo
bunx create-turbo@latest <project-name>
cd <project-name> && pnpm install

# Step 2: 添加 content 包
turbo gen workspace \
  --name @<project-name>/content \
  --type package \
  --destination packages/content
mkdir -p packages/content/src/chapters

# Step 3: 创建 web 包
mkdir -p packages/web && cd packages/web
bunx create astro@latest . --template starlight
cd ../..

# Step 4: 添加 book 包
turbo gen workspace \
  --name @<project-name>/book \
  --type package \
  --destination packages/book

# Step 5: 配置依赖（手动编辑 package.json）
# 见设计文档第 5 章
```

#### 2.2.2 monorepo-guide.md — 大幅精简

**位置**: `process/tutorial-writer-skill/references/monorepo-guide.md`
**变更**: 2633 行 → ~300 行 (-89%)
**新结构**:

```markdown
# Monorepo 快速参考 (Tutorial Writer 特有)

## 1. 三包架构 (~80行)
- 设计理念
- 包职责表
- 推荐 turbo.json 配置

## 2. Workspace 依赖规则 (~60行)
- 正确依赖声明示例
- 禁止的反向依赖

## 3. 日常工作流速查 (~80行)
- 命令速查表
- 内容创作流程

## 4. 常见问题 (TW 特有) (~80行)
- Q1-Q4 (仅 TW 特有问题)

## 5. 相关资源链接 (~20行)
- 官方文档链接集合
```

**删除的章节及理由**:

| 章节 | 原行数 | 决策 | 理由 |
|------|--------|------|------|
| 1.1 一键初始化 | ~60 | ❌ 删除 | → 根路由器 SKILL.md |
| 3. Turborepo 配置详解 | ~400 | ❌ 删除 90% | 官方文档更准确 |
| 4. Workspace 管理 | ~300 | ❌ 删除 80% | 只保留依赖规则 |
| 5. 工作流详情 | ~400 | ⚠️ 精简到 80行 | 改为速查表 |
| 6. 包配置细节 | ~500 | ❌ 删除 85% | 在各子技能中 |
| 7. CI/CD 集成 | ~300 | ❌ 完全删除 | → /github-pages |
| 8. 性能优化 | ~200 | ❌ 完全删除 | 官方文档覆盖 |

#### 2.2.3 子技能前置条件更新

**只修改 3 个子技能** (共 ~40 行):

##### tutorial-writer-content/SKILL.md

```markdown
## 前置条件 (更新后)

- [ ] 已使用官方工具创建 Monorepo 项目
  - 推荐命令: `bunx create-turbo@latest <project-name>`
  - 或手动创建（详见根路由器 SKILL.md 的"项目初始化"章节）
- [ ] 已添加 content 包:
  `turbo gen workspace --name @<project>/content --type package`
- [ ] `packages/content/src/` 目录存在
- [ ] Node.js >= 18 已安装

> **重要**: 本子技能假设 `packages/content/` 已经存在。
> 如果还没有，请先执行根路由器中的 Step 0-2。
```

##### tutorial-writer-web/SKILL.md

```markdown
## 前置条件 (更新后)

- [ ] Monorepo 项目已初始化（含 turbo.json, pnpm-workspace.yaml）
- [ ] `packages/web/` 已通过 Starlight 模板创建
  - 推荐命令: 在 `packages/web/` 下运行
    `bunx create astro@latest . --template starlight`
  - 详见根路由器 SKILL.md 的 Step 3
- [ ] `@<project>/content` 包存在且已在 web/package.json 中声明依赖
  ```json
  { "dependencies": { "@<project>/content": "workspace:*" } }
  ```

> **注意**: 本子技能专注于 Astro + Starlight 配置和组件开发，
> 不包含项目创建逻辑。项目初始化请参考根路由器的"项目初始化"章节。
```

##### tutorial-writer-book/SKILL.md

```markdown
## 前置条件 (更新后)

- [ ] Monorepo 项目已初始化
- [ ] `packages/book/` 已创建
  - 推荐命令: `turbo gen workspace --name @<project>/book --type package`
  - 详见根路由器 SKILL.md 的 Step 4
- [ ] Pandoc (>=2.0) 和 XeLaTeX 已安装
  - 检查: `pandoc --version` && `xelatex --version`
- [ ] `@<project>/content` 包存在且已在 book/package.json 中声明依赖

> **注意**: PDF 生成需要 LaTeX 环境。
> 如未安装，可跳过此子技能或使用 CI/CD 中的 Docker 容器。
```

**不需要修改的 4 个子技能**:
- ✅ `tutorial-writer-research` — 不依赖项目结构
- ✅ `tutorial-writer-writing` — 只依赖 content 包存在
- ✅ `tutorial-writer-review` — 只依赖 content 包存在
- ✅ `tutorial-writer-github-pages` — 只依赖 web 包存在
- ✅ `tutorial-writer-decision` — 不依赖项目结构

---

## 3. 架构对比

### 3.1 Before vs After

```
Before (Plan C):                         After (Plan D):
                                         
SKILL.md (254行)                         SKILL.md (~374行)
├─ 引用 init-tutorial.sh                 ├─ 内嵌初始化流程 ✨新
│                                         │
scripts/ 💀删除                            │
├─ init-tutorial.sh (1002行)             │
│                                         │
templates/ 💀删除                          │
├─ tutorial-starter/ (24文件)            │
│                                         │
references/                               references/
├─ monorepo-guide.md (2633行)            ├─ monorepo-guide.md (~300行) ✨精简
│                                         │
skills/*                                  skills/*
├─ 前置条件: "运行 init 脚本"             ├─ 前置条件: "使用官方工具" ✨更新
```

### 3.2 文件变更统计

| 操作 | 文件数 | 行数变化 | 说明 |
|------|--------|---------|------|
| **删除** | 25 (1目录+24文件) | -4,000 | scripts/ + templates/ |
| **重写** | 1 | +120 (净增) | SKILL.md 根路由器 |
| **精简** | 1 | -2,333 (净减) | monorepo-guide.md |
| **更新** | 3 | +40 (净增) | content/web/book 前置条件 |
| **不变** | ~30 | 0 | 其他所有文件 |
| **合计** | **~60** | ****-6,173**** | **净减 27%** |

---

## 4. 官方工具链参考

### 4.1 Turborepo 工具

| 工具 | 命令 | 用途 | 文档链接 |
|------|------|------|---------|
| **create-turbo** | `bunx create-turbo@latest <name>` | 创建 Monorepo 骨架 | https://turborepo.org/docs/getting-started/installation |
| **turbo gen workspace** | `turbo gen workspace --name ...` | 添加新包 | https://turborepo.org/docs/guides/generating-code |
| **turbo gen workspace --copy** | `turbo gen workspace --copy ...` | 复制现有包 | 同上 |
| **turbo run** | `turbo run <task>` | 执行任务 | https://turborepo.org/docs/reference/cli |
| **turbo build** | `turbo run build` | 生产构建 | 同上 |

### 4.2 Astro 工具

| 工具 | 命令 | 用途 | 文档链接 |
|------|------|------|---------|
| **create-astro** | `bunx create astro@latest . --template starlight` | 创建 Starlight 项目 | https://starlight.astro.build/getting-started/ |

### 4.3 版本兼容性

| 工具 | 最低版本 | 推荐版本 | 说明 |
|------|---------|---------|------|
| Node.js | >=18 | >=20 LTS | 官方推荐 |
| pnpm | >=8 | >=9 | workspace 支持 |
| Turbero | latest | latest | 通过 npx/bunx 使用 |
| Astro | >=4 | >=4.x | Starlight 依赖 |

---

## 5. 实施计划

### 5.1 任务分解

```
Phase D-1: 清理删除 (可并行)
├── Task D-1.1: 删除 scripts/init-tutorial.sh
└── Task D-1.2: 删除 templates/tutorial-starter/

Phase D-2: 内容重构 (有依赖顺序)
├── Task D-2.1: 重写根路由器 SKILL.md (添加初始化章节)
├── Task D-2.2: 精简 monorepo-guide.md
└── Task D-2.3: 更新 3 个子技能的前置条件

Phase D-3: 验证与收尾
├── Task D-3.1: 全局搜索残留引用
├── Task D-3.2: 更新 .trae/ 文档记录此次重构
└── Task D-3.3: Git 提交
```

### 5.2 并行化分析

| 任务 | 依赖 | 可并行？ |
|------|------|---------|
| D-1.1 (删除 scripts/) | 无 | ✅ 可并行 |
| D-1.2 (删除 templates/) | 无 | ✅ 可与 D-1.1 并行 |
| D-2.1 (重写 SKILL.md) | D-1 完成 | ⚠️ 依赖 D-1 |
| D-2.2 (精简 guide) | 无 | ✅ 可与 D-2.1 并行 |
| D-2.3 (更新子技能) | D-2.1 完成 | ⚠️ 依赖 D-2.1 (保持一致性) |

**推荐执行顺序**:

```
Batch 1 (并行):
  ├─ SubAgent A: 删除 scripts/ + templates/
  └─ SubAgent B: 准备 monorepo-guide 精简版

Batch 2 (并行):
  ├─ SubAgent C: 重写根路由器 SKILL.md
  └─ SubAgent D: 应用 monorepo-guide 精简

Batch 3 (串行或并行):
  └─ SubAgent E: 更新 3 个子技能前置条件

Batch 4:
  └─ 全局验证 + 文档更新
```

---

## 6. 风险评估

### 6.1 潜在风险

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| **官方工具 API 变化** | 🟡 中 | 🟡 中 | 我们只使用稳定的核心命令；变化时只需更新 SKILL.md 中的命令 |
| **用户习惯改变** | 🟢 低 | 🟢 低 | 新方式更简单（标准工具），学习成本更低 |
| **信息密度降低** | 🟡 中 | 🟡 中 | 保留了所有 TW 特有信息；通用信息指向官方文档 |
| **AI 执行偏差** | 🟡 中 | 🔴 高 | SKILL.md 中的命令足够详细；增加了验证清单 |

### 6.2 回滚方案

如果发现问题：

```bash
# 回滚到 Plan C 状态
git revert <this-commit>

# 或从 git 历史恢复
git checkout <pre-plan-d-commit> -- scripts/ templates/
```

---

## 7. 成功标准

### 7.1 功能验收

- [ ] 删除 `scripts/` 和 `templates/` 后，skill 仍能正常工作
- [ ] 根路由器的初始化章节清晰可用
- [ ] AI 能根据初始化章节成功创建项目
- [ ] 所有子技能的前置条件正确引用官方工具
- [ ] 无残留的旧路径引用 (`init-tutorial.sh`, `templates/`)

### 7.2 质量验收

- [ ] 全局搜索无旧引用
- [ ] monorepo-guide.md < 400 行
- [ ] 根路由器 SKILL.md < 450 行
- [ ] 代码净减少 > 5000 行
- [ ] 所有增值配置可在 references/ 中找到

---

## 8. 版本策略

### 8.1 版本号决定

**保持 v1.0.0 不变**

理由：
1. 这是内部重构，不改变外部 API（7 子技能架构不变）
2. 用户可见的功能完全一致
3. 只是实现方式的优化（从自定义脚本→官方工具）

### 8.2 CHANGELOG 记录

```markdown
## v1.0.0 (Internal Refactor)

### Changed
- **Breaking**: 移除 `scripts/init-tutorial.sh` 自定义初始化脚本
- **Breaking**: 移除 `templates/tutorial-starter/` 项目模板目录
- 改用官方 CLI 工具链进行项目初始化:
  - `create-turbo` (Monorepo 骨架)
  - `turbo gen workspace` (添加包)
  - `create-astro --template starlight` (网站包)
- 精简 `references/monorepo-guide.md` (2633→300行, -89%)
- 更新 content/web/book 子技能的前置条件说明

### Removed
- `scripts/init-tutorial.sh` (1002行)
- `templates/tutorial-starter/` (24文件, ~3000行)

### Net Impact
- 代码净减少: ~6,200行 (-27%)
- 维护负担: 接近零（无需同步官方模板更新）
- 时效性: 永远使用最新版官方工具
```

---

## 9. 后续规划

### 9.1 不在本次范围内

- [ ] EPUB 格式支持 (v1.1.0)
- [ ] Windows 原生支持改进 (v1.1.0)
- [ ] 更多 LaTeX 模板 (v1.2.0)
- [ ] 交互式组件库 (v2.0.0)

### 9.2 可能的未来优化

- [ ] 考虑创建自定义 `turbo generator` (基于 Plop) 封装 TW 特有的初始化流程
- [ ] 添加 `package.json` 的 `"tutorial-writer": {"version": "1.0.0"}` 元数据用于版本检测
- [ ] 集成到 VS Code 的 Tutorial Writer 扩展（如果有的话）

---

## 附录 A: 完整的初始化命令序列

```bash
#!/bin/bash
# ============================================================
# Tutorial Writer v1.0.0 — Official Tools Initialization
# ============================================================
# Usage: Copy these commands to your terminal
# This replaces the old init-tutorial.sh script
# ============================================================

set -euo pipefail

# ====== Configuration ======
PROJECT_NAME="${1:?Usage: $0 <project-name>}"
PACKAGE_MANAGER="pnpm"  # or npm, yarn, bun

# ====== Colors ======
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $*"; }
log_success() { echo -e "${GREEN}[✓]${NC} $*"; }

# ====== Step 0: Environment Check ======
log_info "Step 0: Checking environment..."
node --version | grep -qE "v(18|19|20)\." || { echo "Error: Node.js >= 18 required"; exit 1; }
$PACKAGE_MANAGER --version >/dev/null || { echo "Error: $PACKAGE_MANAGER not found"; exit 1; }
log_success "Environment OK"

# ====== Step 1: Create Monorepo ======
log_info "Step 1: Creating Monorepo skeleton..."
if command -v bun &>/dev/null; then
  bunx create-turbo@latest "$PROJECT_NAME"
else
  npx create-turbo@latest "$PROJECT_NAME"
fi
cd "$PROJECT_NAME"
$PACKAGE_MANAGER install
log_success "Monorepo created: $(pwd)"

# ====== Step 2: Add content package ======
log_info "Step 2: Adding content package..."
turbo gen workspace \
  --name "@${PROJECT_NAME}/content" \
  --type package \
  --destination packages/content
mkdir -p packages/content/src/chapters
touch packages/content/src/chapters/.gitkeep
log_success "Content package ready"

# ====== Step 3: Create web package ======
log_info "Step 3: Creating web package (Starlight)..."
mkdir -p packages/web && cd packages/web
if command -v bun &>/dev/null; then
  bunx create astro@latest . --template starlight
else
  npx create astro@latest . --template starlight
fi
cd ../..
log_success "Web package ready"

# ====== Step 4: Add book package ======
log_info "Step 4: Adding book package..."
turbo gen workspace \
  --name "@${PROJECT_NAME}/book" \
  --type package \
  --destination packages/book
log_success "Book package ready"

# ====== Step 5: Configure dependencies ======
log_info "Step 5: Configuring workspace dependencies..."
# Using jq for JSON manipulation (or manual edit)
if command -v jq &>/dev/null; then
  # Add content dependency to web
  tmp=$(mktemp)
  jq ".dependencies.\"@${PROJECT_NAME}/content\" = \"workspace:*\"" \
    packages/web/package.json > "$tmp" && mv "$tmp" packages/web/package.json
  
  # Add content dependency to book
  jq ".dependencies.\"@${PROJECT_NAME}/content\" = \"workspace:*\"" \
    packages/book/package.json > "$tmp" && mv "$tmp" packages/book/package.json
else
  log_info "jq not found. Please manually edit:"
  log_info "  packages/web/package.json -> add \"@${PROJECT_NAME}/content\": \"workspace:*\""
  log_info "  packages/book/package.json -> add \"@${PROJECT_NAME}/content\": \"workspace:*\""
fi
log_success "Dependencies configured"

# ====== Done! ======
echo ""
log_success "========================================="
log_success " Tutorial Writer project initialized!"
log_success "========================================="
echo ""
log_info "Next steps:"
log_info "  1. Configure content Schema (see /content sub-skill)"
log_info "  2. Write your first chapter in packages/content/src/chapters/"
log_info "  3. Run 'turbo run dev' to start development"
log_info "  4. See root SKILL.md for complete initialization guide"
echo ""
```

---

## 附录 B: 文件完整性检查清单

执行重构后，逐项确认：

### 删除确认
- [ ] `scripts/init-tutorial.sh` 不存在
- [ ] `scripts/` 目录不存在（或为空）
- [ ] `templates/tutorial-starter/` 不存在
- [ ] `templates/` 目录不存在（或为空）

### 新增/修改确认
- [ ] `SKILL.md` (根路由器) 包含"🚀 项目初始化"章节
- [ ] `SKILL.md` 行数在 350-400 之间
- [ ] `references/monorepo-guide.md` 行数 < 400
- [ ] `monorepo-guide.md` 不包含"一键初始化"章节
- [ ] `skills/tutorial-writer-content/SKILL.md` 前置条件已更新
- [ ] `skills/tutorial-writer-web/SKILL.md` 前置条件已更新
- [ ] `skills/tutorial-writer-book/SKILL.md` 前置条件已更新

### 残留检查
- [ ] 全局搜索 `init-tutorial.sh` → 结果应为 0（仅在 .git 历史中）
- [ ] 全搜索 `templates/tutorial-starter` → 结果应为 0
- [ ] 全局搜索 `scripts/init` → 结果应为 0（仅在本文档中）

### 功能验证
- [ ] 根路由器仍能正确分发到 7 个子技能
- [ ] 初始化章节的命令序列清晰可执行
- [ ] 所有交叉引用有效（无断链）

---

**文档编写完成**: 2026-05-31
**下一步**: 用户审查批准后，调用 writing-plans skill 创建实施计划
