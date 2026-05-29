---
name: agents-writer
version: v1.0.0
author: book-skills
description: AGENTS.md 写作专家 — 从项目分析到质量验收的全流程行动指南，支持5种类型判定、28条最佳实践、生产级模板库和反模式检测，帮助AI Agent写出高质量的协作配置文件
tags: [agents-md, agent-config, writing-guide, best-practices, template, quality-check, project-handbook]
dependency:
  parent: none
  children: [1-analyze-project, 2-design-structure, 3-write-content, 4-select-template, 5-quality-check, 6-optimize-evolve]
---

# AGENTS.md 写作专家

## 激活条件

当用户需要以下任一操作时激活：
- 创建或重写项目的 AGENTS.md 文件
- 分析现有 AGENTS.md 的质量和问题
- 学习如何为不同类型的项目编写 AGENTS.md
- 获取 AGENTS.md 的模板或最佳实践
- 优化或迭代现有 AGENTS.md

## 意图路由

| 用户意图 | 触发示例 | 执行子技能 |
|---------|---------|-----------|
| **📊 分析项目需求** | "这个项目适合什么类型的AGENTS.md"、"帮我分析项目" | [1-analyze-project](skills/1-analyze-project/SKILL.md) |
| **🏗️ 设计文件结构** | "设计AGENTS.md结构"、"应该包含哪些章节" | [2-design-structure](skills/2-design-structure/SKILL.md) |
| **✍️ 编写核心内容** | "帮我写AGENTS.md"、"编写内容" | [3-write-content](skills/3-write-content/SKILL.md) |
| **📋 使用快速模板** | "给我一个模板"、"从模板开始" | [4-select-template](skills/4-select-template/SKILL.md) |
| **✅ 质量检查验证** | "检查这个AGENTS.md"、"是否符合规范" | [5-quality-check](skills/5-quality-check/SKILL.md) |
| **🔄 优化迭代维护** | "优化我的AGENTS.md"、"减少Token占用" | [6-optimize-evolve](skills/6-optimize-evolve/SKILL.md) |

## 通用工作流

```
用户请求
    │
    ▼
① 意图识别 ← 匹配触发关键词，确定子技能
    │
    ▼
② 信息收集 ← 读取项目上下文（README/package.json/技术栈）
    │
    ▼
③ 执行指南 ← 调用对应子技能的标准流程
    │
    ▼
④ 质量门禁 ← 对照规范清单验证输出
    │
    ▼
⑤ 交付成果 ← 提供可用的 AGENTS.md + 改进建议
```

## 质量门禁

### 必须通过的检查项

- [ ] **前言区完整性**: name/description/tags 全部存在且符合规范
- [ ] **触发条件明确**: 清晰说明何时使用此 AGENTS.md
- [ ] **意图路由清晰**: 至少包含 3 个常见任务的触发→执行映射
- [ ] **无反模式**: 不存在 [22个已知反模式](references/anti-patterns.md)
- [ ] **Token 效率合理**: 核心内容 ≤ 500 行（详见 [token-budget.md](references/token-budget.md)）

### 推荐执行命令

```bash
# 检查现有 AGENTS.md 质量
cat AGENTS.md | head -50  # 查看前50行判断结构完整性

# 统计行数和 Token 估算
wc -l AGENTS.md && echo "估算Token: $(($(wc -l < AGENTS.md) * 3))"
```

## 知识库索引

| 文件 | 内容 | 适用场景 |
|------|------|---------|
| [best-practices.md](references/best-practices.md) | 28条最佳实践（结构/内容/格式） | 编写时参考 |
| [type-classification.md](references/type-classification.md) | 5种AGENTS.md类型详解 | 项目分析阶段 |
| [anti-patterns.md](references/anti-patterns.md) | 22个反模式及修复方案 | 质量检查阶段 |
| [templates.md](references/templates.md) | 最小可行/标准/完整模板 | 快速开始场景 |
| [examples.md](references/examples.md) | 4个真实案例对比 | 学习参考 |
| [token-budget.md](references/token-budget.md) | Token预算分配策略 | 优化阶段 |

## 子技能总览

| # | 子技能 | 核心能力 | 典型输出 |
|---|--------|---------|---------|
| 1 | [1-analyze-project](skills/1-analyze-project/SKILL.md) | 项目分析+类型判定 | 类型推荐+复杂度评分 |
| 2 | [2-design-structure](skills/2-design-structure/SKILL.md) | 结构蓝图设计 | 章节规划+字段定义 |
| 3 | [3-write-content](skills/3-write-content/SKILL.md) | 内容编写实战 | 完整AGENTS.md草稿 |
| 4 | [4-select-template](skills/4-select-template/SKILL.md) | 模板选择定制 | 可直接使用的模板 |
| 5 | [5-quality-check](skills/5-quality-check/SKILL.md) | 质量检查验证 | 问题清单+修复建议 |
| 6 | [6-optimize-evolve](skills/6-optimize-evolve/SKILL.md) | 迭代优化策略 | 优化方案+维护计划 |

## 数据来源

本技能基于以下研究成果构建：
- **理论来源**: AGENTS.md 官方规范、Cursor/Windsurf/Claude Code 最佳实践
- **实践来源**: book-skills、moonbit-skills、flutter-skills、rust-skills 等 4 个真实项目的 AGENTS.md 对比分析
- **经验总结**: 28 条最佳实践、22 个反模式、Token 效率优化策略

## 注意事项

⚠️ **核心理念**: AGENTS.md 回答的是 "**HOW to work**"（如何工作），不是 "**WHAT is this**"（这是什么）。它是 Agent 的操作手册，不是项目说明书。

⚠️ **与 SKILL.md 的区别**:
- **AGENTS.md** = 项目级配置（告诉 Agent 如何在这个项目中工作）
- **SKILL.md** = 技能级配置（告诉 Agent 这个技能能做什么）

⚠️ **优先级**: 在多 Agent 协作环境中，AGENTS.md > CLAUDE.md > .cursorrules > README.md

## 版本历史

| 版本 | 日期 | 主要变更 |
|------|------|---------|
| **v1.0.0** | 2026-05-17 | 🎉 初始版本：完整的 AGENTS.md 写作专家技能，包含 6 个子技能和 6 个知识库文件 |
