---
name: tutorial-writer-research
version: v1.0.0
author: skill-factory
description: Use when researching technical topics, planning chapter outlines, designing chapter structure, or collecting reference materials before writing
tags: [tutorial, research, planning, outline, length-planning, reference-collection]
meta:
  architecture: "monorepo-v1"
---

# Tutorial Writer — 📚 调研与规划

## 技能定位

本子技能负责教程创作的 **前期调研与规划阶段**（PRWRD+D 中的 PLAN + RESEARCH），产出经确认的章节执行计划。

**输入**: 大纲 / 用户需求 / 待写章节编号
**输出**: 已确认的章节执行计划（含目标长度、资料清单、小节结构）

## 核心流程

```
① 阅读大纲/需求 → 确定章节定位
    │
    ├── ②a 自动判断章节类型与目标长度
    │     （见 references/length-planning.md）
    │
    ├── ②b 拆解为小节，规划每节要点
    │
    └── ③ 与用户确认规划后继续
         │
         └── ④a 基于规划确定搜索关键词
              │
              ├── ④b 执行 WebSearch（至少 3 组不同关键词）
              │
              ├── ④c 筛选高质量来源并获取内容
              │
              ├── ④d 归档到 reference/ 并更新索引
              │
              └── ⑤ 确认资料充足后才进入 WRITE 阶段
```

## 参考文件

- [搜索方法论](references/research-methodology.md) — 搜索策略、质量判断、归档规范
- [长度规划规则](references/length-planning.md) — 阶段基准、小节数微调、密度因子
- [本阶段决策细则](references/decision-record-rules.md) — research 阶段涉及的决策项

## 输出物与下游对接

调研结果将用于：
- `packages/content/src/chapters/` 中的 Markdown 文件（由 `/writing` 撰写）
- 后续经 `/web` 构建为网站 或 `/book` 转换为电子书
- 最终由 `/github-pages` 部署发布

## 质量自检

进入 writing 前必须通过以下检查：

| # | 检查项 | 标准 |
|---|--------|------|
| RQ1 | 规划已确认 | 有结构草图且经用户确认 |
| RQ2 | 资料已归档 | reference/ 中新增 ≥1 个资料文件 |
| RQ3 | 索引已更新 | 00-资源索引与链接.md 已更新 |
| RQ4 | 搜索次数达标 | ≥3 次 WebSearch（不同关键词组） |
| RQ5 | 资料质量达标 | 无过时/来源不明/纯观点资料 |
