---
name: tutorial-writer
version: v3.0.0
author: RAG 教程项目组
description: Use when creating, writing, reviewing, publishing technical tutorial content, or managing decisions across the full lifecycle
tags: [tutorial, writing, technical-documentation, router, research, review, publishing, decision-record]
dependency:
  parent: none
  children:
    - tutorial-writer-research
    - tutorial-writer-writing
    - tutorial-writer-review
    - tutorial-writer-publish
    - tutorial-writer-decision
---

# Tutorial Writer v3 — 5-Sub Router

> **定位**: 轻量路由枢纽 — 将教程创作请求分发到 5 个独立子技能
> **架构**: 5-Entry Router (root → skills/ = Layer 0 → Layer 1)

## 目标

将教程创作的完整生命周期（调研规划 → 撰写执行 → 质量校验 → 网页发布 → 决策贯穿）通过统一入口分发，每个阶段有独立的技能文件和细则。

**能做什么**:
- 智能路由用户请求到 5 个自含型子技能
- 提供全局速查（铁律/分类）
- 展示子技能概览和相互依赖关系

**不能做什么**:
- 不包含具体操作步骤（各子技能负责）
- 不执行校验或发布（→ `/review` `/publish`）

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

## 🧭 5-Sub 路由表

```
用户说...                                  → 调用
──────────────────────────────────        ─────────────────────────────────────
"搜索/调研/规划/找资料/设计章节结构"       → 📚 /research    (调研与规划)
"写/撰写/创作/编写章节"                    → ✍️ /writing     (撰写执行)
"检查/校对/质量/门禁/评分"                → ✅ /review      (质量校验)
"发布/部署/网页/mkdocs/网站"              → 🌐 /publish     (网页发布)
"配置/决策/改决策/看看决策/冲突"           → 📐 /decision    (决策系统)
```

### 复合场景

| 用户意图 | 执行顺序 |
|---------|---------|
| 完整创作一个章节 | research → writing → review → publish |
| 优化已有章节 | review → writing → publish |
| 创建新教程项目 | decision → research → writing → review |
| 仅修改配置 | decision |

### 歧义处理

不确定用户意图时提供选项：

> "您是想：a) 📚 调研规划新章节 b) ✍️ 撰写/修改内容 c) ✅ 质量检查 d) 🌐 网页发布 e) 📐 管理决策？"

---

## 📂 子技能一览

| 子技能 | 职责 | 触发词 | 关键文件 |
|--------|------|--------|---------|
| [research](skills/tutorial-writer-research/SKILL.md) | 调研规划 | 搜索/规划/设计结构 | 搜索方法论+长度规划+标准概览 |
| [writing](skills/tutorial-writer-writing/SKILL.md) | 撰写执行 | 写/撰写/完成章节 | 写作流程+素材管理+规范R1-R6 |
| [review](skills/tutorial-writer-review/SKILL.md) | 质量校验 | 检查/校对/门禁 | 14项质量门禁+评分卡 |
| [publish](skills/tutorial-writer-publish/SKILL.md) | 网页发布 | 发布/部署/网页 | MkDocs+交互组件+GitHub Pages |
| [decision](skills/tutorial-writer-decision/SKILL.md) | 决策贯穿 | 配置/决策 | 决策方法论+阶段映射+冲突解决 |

> 每个子技能完全自含：独立 SKILL.md + references/ + 阶段性决策细则

---

## 📂 项目结构

```
tutorial-writer/
├── SKILL.md                              ← 本文件 (路由器 ~120行)
├── references/                           ← 全局共享参考
│   ├── design-principles.md              ← 铁律+分类+架构说明
│   ├── cross-chapter-rules.md            ← R7-R10 跨章一致性规则
│   └── phase-mapping.md                  ← 阶段→决策项映射
├── assets/                               ← 全局共享模板
│   ├── decision-record-schema.json
│   └── decision-record-template.json
└── skills/                               ← Layer 1: 5个独立子技能
    ├── tutorial-writer-research/         ← 📚 调研规划
    ├── tutorial-writer-writing/          ← ✍️ 撰写执行
    ├── tutorial-writer-review/           ← ✅ 质量校验
    ├── tutorial-writer-publish/          ← 🌐 网页发布
    └── tutorial-writer-decision/         ← 📐 决策贯穿
```

---

## ⚠️ 注意事项

- **子技能优先**: 根文件仅做路由，详细逻辑在各子技能中
- **每个子技能可独立使用**: 有自己的 description，Agent 可直接触发
- **全局 references/ 仅放跨子技能公共内容**: 设计原则/跨章规则/阶段映射
- **职能归属明确**: 搜索规划在 research，撰写在 writing，校验在 review，发布在 publish，决策在 decision
- **决策贯穿所有阶段**: 每个子技能内有独立的 `decision-record-rules.md` 定义本阶段决策细则

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| **v3.0.0** | 2026-05-29 | **5-Sub Router 重构**: 从扁平文档拆分为 5 个独立子技能（research/writing/review/publish/decision），每个技能自含 references/ 和阶段性决策细则；全局 references 精简为 3 个跨子技能共享文件 |
| v2.2.0 | 2026-05-29 | Web Publishing 增强（前版本） |
| v2.1.0 | 2026-05-29 | 跨章一致性升级（前版本） |

---

**最后更新**: 2026-05-29
