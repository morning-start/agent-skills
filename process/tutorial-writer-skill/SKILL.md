---
name: tutorial-writer
version: v6.1.0
author: skill-factory
description: Use when creating, writing, reviewing, building, publishing technical tutorial content via GitHub Pages with Content-First v2 architecture, or managing decisions across the full tutorial lifecycle
tags: [tutorial, writing, technical-documentation, router, research, review, build, publishing, decision-record, github-pages, astro, starlight, content-first]
dependency:
  parent: none
  children:
    - tutorial-writer-research
    - tutorial-writer-writing
    - tutorial-writer-review
    - tutorial-writer-build
    - tutorial-writer-publish
    - tutorial-writer-decision
meta:
  architecture_version: "content-first-v2"
  build_version_requirement: ">=2.0.0"
  publish_version_requirement: ">=7.0.0"
---

# Tutorial Writer v6.1 — 6-Sub Router (Content-First v2)

> **定位**: 轻量路由枢纽 — 将教程创作请求分发到 6 个独立子技能
> **架构**: 6-Entry Router (root → skills/ = Layer 0 → Layer 1)
> **升级亮点**: 构建与发布分离，高频操作路径优化
> **架构版本**: **Content-First v2**（内容优先 + 增强层分离）

## 目标

将教程创作的完整生命周期（调研规划 → 撰写执行 → 质量校验 → 网站构建 → 网页发布 → 决策贯穿）通过统一入口分发，每个阶段有独立的技能文件和细则。

**能做什么**:
- 智能路由用户请求到 6 个自含型子技能
- 提供全局速查（铁律/分类）
- 展示子技能概览和相互依赖关系

**不能做什么**:
- 不包含具体操作步骤（各子技能负责）
- 不执行校验或构建或发布（→ `/review` `/build` `/publish`）

---

## 🏗️ Content-First v2 架构概览

> **设计来源**: [tutorial-writer-suggest.md](.trae/documents/tutorial-writer-suggest.md)
> **核心哲学**: **内容是主角，代码是配角**

### 架构核心理念

| 传统做法 | Content-First v2 |
|---------|-----------------|
| 内容藏在 `src/content/docs/` 深处 | **内容在根目录 `content/`，一目了然** |
| 可能维护 book/ 和 site/ 两份内容 | **只有一份内容源，通过管道生成多形态产物** |
| 文件名随意（中文），URL 丑陋 | **英文 slug 文件名 + 中文标题，URL 干净** |
| 组件和样式混杂 | **增强层分离：components/scripts/styles 各司其职** |
| 仅能生成网站 | **天然支持网站 + PDF/EPUB + 其他格式** |

### 目标项目结构

```
tutorial-project/
├── content/                       ← 📝 内容层（唯一真相源）
│   ├── chapters/
│   │   ├── 01-rag-overview.md     ← 英文 slug 文件名
│   │   └── 02-rag-evolution.md
│   ├── index.mdx                  ← 首页
│   └── config.ts                  ← Content Collections schema
├── src/                           ← 🔧 增强层
│   ├── components/                ← 按功能分组 (interactive/charts/code/ui)
│   ├── layouts/
│   ├── styles/
│   └── scripts/                   ← 构建时增强管道
├── astro.config.mjs
└── package.json
```

### 版本兼容性要求

| 子技能 | 最低版本 | 当前版本 | 架构支持 |
|--------|---------|---------|---------|
| **build** | **v2.0.0+** | v2.0.0 | ✅ Content-First v2 |
| **publish** | **v7.0.0+** | v7.0.0 | ✅ Content-First v2 + 多形态发布 |

⚠️ **重要**: 本路由器要求 build ≥ v2.0.0 且 publish ≥ v7.0.0。旧版子技能（build v1.x / publish ≤ v6.1.0）使用传统架构，与本版本不兼容。

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

## 🧭 6-Sub 路由表

```
用户说...                                  → 调用
──────────────────────────────────        ─────────────────────────────────────
"搜索/调研/规划/找资料/设计章节结构"       → 📚 /research    (调研与规划)
"写/撰写/创作/编写章节"                    → ✍️ /writing     (撰写执行)
"检查/校对/质量/门禁/评分"                → ✅ /review      (质量校验)
"构建网站/Astro/Starlight/组件/配置"      → 🏗️ /build       (网站构建) ⭐ 高频
"部署/GitHub Pages/Actions/CI-CD/域名"     → 🚀 /publish     (网站发布) 🟢 低频
"配置/决策/改决策/看看决策/冲突"           → 📐 /decision    (决策系统)
```

### 复合场景

| 用户意图 | 执行顺序 |
|---------|---------|
| 完整创作一个教程 | research → writing → review → build → publish |
| 优化已有章节 | review → writing → review → build → publish |
| 创建新教程项目 | decision → research → writing → review → build → publish |
| 仅修改配置 | decision |
| 仅构建/重构网站 | build（可独立反复调用）|
| 仅重新部署 | publish（可独立调用）|

### 歧义处理

不确定用户意图时提供选项：

> "您是想：a) 📚 调研规划 b) ✍️ 撰写/修改内容 c) ✅ 质量检查 d) 🏗️ 构建网站 e) 🚀 部署发布 f) 📐 管理决策？"

---

## 📂 子技能一览

| 子技能 | 版本 | 职责 | 触发词 | 关键特性 | 频率 |
|--------|------|------|--------|---------|------|
| [research](skills/tutorial-writer-research/SKILL.md) | - | 调研规划 | 搜索/规划/设计结构 | 搜索方法论+长度规划+标准概览 | 低 |
| [writing](skills/tutorial-writer-writing/SKILL.md) | - | 撰写执行 | 写/撰写/完成章节 | 写作流程+素材管理+规范R1-R6 | 中 |
| [review](skills/tutorial-writer-review/SKILL.md) | - | 质量校验 | 检查/校对/门禁 | 14项质量门禁+评分卡 | 中 |
| **[build](skills/tutorial-writer-build/SKILL.md)** | **v2.0.0** | **网站构建** | **构建/Astro/Starlight/组件/配置** | **Content-First v2 + 增强管道 + 组件分组** | **🔴 高** |
| [publish](skills/tutorial-writer-publish/SKILL.md) | **v7.0.0** | 网站发布 | 部署/GitHub Pages/Actions/CI-CD/PDF | **Content-First v2 + 多形态发布(PDF/EPUB)** | 🟢 低 |
| [decision](skills/tutorial-writer-decision/SKILL.md) | - | 决策贯穿 | 配置/决策 | 决策方法论+阶段映射+冲突解决 | 贯穿 |

> 每个子技能完全自含：独立 SKILL.md + references/ + 阶段性决策细则
>
> **频率说明**: build 为高频子技能（预计每项目 10-20 次调用），publish 为低频（2-3 次）
>
> **架构说明**: build (v2.0.0+) 和 publish (v7.0.0+) 已升级至 Content-First v2 架构，确保两者完全对齐

---

## 📂 项目结构

```
tutorial-writer/
├── SKILL.md                              ← 本文件 (6-Sub 路由器 ~130行)
├── references/                           ← 全局共享参考
│   ├── design-principles.md              ← 铁律+分类+架构说明
│   ├── cross-chapter-rules.md            ← R7-R10 跨章一致性规则
│   └── phase-mapping.md                  ← 阶段→决策项映射
├── assets/                               ← 全局共享模板
│   ├── decision-record-schema.json
│   └── decision-record-template.json
└── skills/                               ← Layer 1: 6个独立子技能
    ├── tutorial-writer-research/         ← 📚 调研规划
    ├── tutorial-writer-writing/          ← ✍️ 撰写执行
    ├── tutorial-writer-review/           ← ✅ 质量校验
    ├── tutorial-writer-build/            ← 🏗️ 网站构建 (高频)
    ├── tutorial-writer-publish/          ← 🚀 网站发布 (低频)
    └── tutorial-writer-decision/         ← 📐 决策贯穿
```

---

## ⚠️ 注意事项

- **子技能优先**: 根文件仅做路由，详细逻辑在各子技能中
- **每个子技能可独立使用**: 有自己的 description，Agent 可直接触发
- **全局 references/ 仅放跨子技能公共内容**: 设计原则/跨章规则/阶段映射
- **职能归属明确**: 搜索规划在 research，撰写在 writing，校验在 review，发布在 publish，决策在 decision
- **决策贯穿所有阶段**: 每个子技能内有独立的 `decision-record-rules.md` 定义本阶段决策细则
- **🆕 架构一致性要求 (Content-First v2)**:
  - build 和 publish **必须使用匹配的架构版本**
  - 当前要求: **build ≥ v2.0.0** 且 **publish ≥ v7.0.0**
  - 内容目录必须使用 `content/chapters/`（根目录），**禁止**使用旧版 `src/content/docs/`
  - 文件命名必须遵循：英文 slug + 中文标题（Frontmatter）
  - 如需使用旧版架构，请降级到 tutorial-writer v6.0.0

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| **v6.1.0** | 2026-05-31 | **🎯 Content-First v2 架构对齐**: 新增 `architecture_version: "content-first-v2"` 元数据；新增完整的 **Content-First v2 架构概览** 章节（核心理念对比表、目标项目结构、版本兼容性要求）；子技能一览表增强（新增版本列、更新 build/publish 关键特性描述、添加架构对齐说明）；注意事项新增架构一致性要求（版本匹配、目录规范、命名规范）；description 和 tags 更新（新增 content-first）；标题标注架构版本 |
| **v6.0.0** | 2026-05-30 | **6-Sub Router 重构**: 从 5-Sub 升级为 6-Sub Router；新增独立 L1 子技能 tutorial-writer-build（网站构建，高频操作）；publish 简化为纯发布职责；路由表和复合场景更新；项目结构图更新 |
| **v4.1.0** | 2026-05-30 | **模块化配置 + 插件生态**: publish 新增模块化配置分层(基础/社交/导航/搜索/插件)、Starlight 配置全景表(18项)、Content Collections 扩展方案；新增 19 个社区插件和 3 个官方插件的选择策略和配置示例；新增交互组件框架选择表(React/Vue/Svelte/Solid/Preact)；新增社区构建经验(内容组织/性能/多语言/版本化/常见陷阱)；新增章节 Frontmatter 完整示例 |
| **v4.0.0** | 2026-05-30 | Astro + Starlight 发布方案（前版本） |
| **v3.2.0** | 2026-05-29 | Tag 驱动发布 + skill-factory 接管（前版本） |
| **v3.1.0** | 2026-05-29 | Web 富交互增强（前版本） |
| **v3.0.0** | 2026-05-29 | **5-Sub Router 重构**: 从扁平文档拆分为 5 个独立子技能（research/writing/review/publish/decision），每个技能自含 references/ 和阶段性决策细则；全局 references 精简为 3 个跨子技能共享文件 |
| v2.2.0 | 2026-05-29 | Web Publishing 增强（前版本） |
| v2.1.0 | 2026-05-29 | 跨章一致性升级（前版本） |

---

**最后更新**: 2026-05-31
