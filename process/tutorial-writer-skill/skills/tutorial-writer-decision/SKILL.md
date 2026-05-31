---
name: tutorial-writer-decision
version: v1.0.0
author: skill-factory
description: Use when configuring, reviewing, updating technical decisions across the tutorial lifecycle
tags: [tutorial, decision, configuration, project-setup, consistency]
meta:
  architecture: "monorepo-v1"
---

# Tutorial Writer — 📐 决策贯穿

## 技能定位

本子技能负责教程创作的 **决策贯穿系统**（PRWRD+D 中的 DECISION 阶段），在所有阶段中提供决策的创建、查询、修改、冲突解决能力。不直接参与内容创作，而是为其他 4 个子技能提供"什么决策已确认"的权威来源。

**输入**: 决策需求（用户指令/阶段切换触发/冲突检测）
**输出**: 已更新的 decision-record.json + Memory 缓存

## 核心流程

```
① 加载/初始化决策记录（decision-record.json）
    │
    ├── ② 检查当前阶段涉及的决策是否已确认
    │     （见 references/decision-integration.md 各阶段决策检查点）
    │
    ├── ③ 如有缺失 → 发起讨论
    │   ├── 展示决策问题 + 选项
    │   ├── 记录用户选择（写入 JSON）
    │   └── 更新 Memory 缓存
    │
    ├── ④ 检测冲突
    │   ├── 新决策与已有决策矛盾？
    │   ├── 执行影响评估
    │   └── 呈现冲突选项供用户裁决
    │
    └── ⑤ 同步到全局缓存
        ├── Memory (decision:{id}:{field})
        └── 其他子技能按需读取
```

## 各阶段决策映射（Monorepo 7-Sub 架构）

| 触发阶段 | 子技能 | 决策类型 | 决策记录位置 | 详见 |
| -------- | ------ | -------- | ------------ | ---- |
| 调研规划 | /research | 方案选型 | `decisions/research/*.md` | `references/decision-data-model.md` |
| 撰写内容 | /writing | 写作决策 | `decisions/writing/*.md` | `references/decision-data-model.md` |
| **内容管理** | **/content** 🆕 | **Schema/结构决策** | **decisions/content/*** 🆕 | `references/decision-data-model.md` |
| **网站构建** | **/web** ✏️ | **技术决策** | **decisions/web/*** ✏️ | `references/decision-data-model.md` |
| **电子书生成** | **/book** 🆕 | **格式决策** | **decisions/book/*** 🆕 | `references/decision-data-model.md` |
| 质量校验 | /review | 质量标准 | `decisions/review/*.md` | `references/decision-data-model.md` |
| **部署发布** | **/github-pages** ✏️ | **运维决策** | **decisions/github-pages/*** ✏️ | `references/decision-data-model.md` |
| 全局 | /decision | 跨阶段决策 | `decisions/global/*.md` | `references/decision-discussion.md` |

> ✏️ = 从旧 publish 拆分/重命名　🆕 = 新增子技能

## 决策项速查（共 19 项）

| 分类     | 数量                 | 优先级          |
| -------- | -------------------- | --------------- |
| 基础配置 | 2                    | critical-high   |
| 技术选型 | 4                    | critical-high   |
| 内容策略 | 4                    | critical-medium |
| 风格偏好 | 3                    | medium-high     |
| 项目管理 | 6（含 4 项网页发布） | medium-low      |

详见 [决策记录索引](references/decision-record-full.md)（含 4 个专注文件导航）。

## 快速启动

```bash
# 初始化决策记录（首次使用）
cp ../../assets/decision-record-template.json ./decision-record.json

# 查看当前决策状态
# （交由 Agent 自动加载并展示）
```

## 参考文件

- [决策数据模型](references/decision-data-model.md) — 分类体系、状态机、字段定义
- [双存储方案](references/decision-storage.md) — JSON + Memory 双轨制
- [讨论与交互](references/decision-discussion.md) — Agent 讨论引导、动态更新、冲突解决
- [系统集成](references/decision-integration.md) — PRWRD 集成、快速启动、最佳实践
