---
name: tutorial-writer-review
version: v3.2.0
author: skill-factory
description: Use when checking, reviewing, scoring finished tutorial content, or running quality gates before delivery
tags: [tutorial, review, quality-gate, cross-chapter, validation, scorecard]
---

# Tutorial Writer — ✅ 质量校验

## 技能定位

本子技能负责教程创作的 **后期质量校验阶段**（PRWRD+D 中的 REVIEW），在交付前对章节内容进行全量门禁检查。

**输入**: 完成初稿的章节 .md 文件
**输出**: 质量评分卡（通过/不通过判定 + 问题清单）

## 核心流程

```
① 通读全文 → 建立整体印象
    │
    ├── ② 逐项执行质量门禁
    │   ├── Q1-Q2: 阻塞项（规划先行、搜索先行）
    │   ├── Q3-Q9: 标准项（长度、支撑、结构、语言等）
    │   └── Q10-Q14: 增强项（跨章一致性、网页构建）
    │
    ├── ③ 跨章一致性检查
    │   ├── R7: 技术栈与决策记录一致
    │   ├── R8: 数据结构与相邻章节兼容
    │   └── R9: 代码逻辑审查
    │
    ├── ④ 填写质量评分卡
    │
    └── ⑤ 输出判定
        ├── 阻塞项全过 + 非阻塞项 ≥ 11/12 → ✅ 通过
        └── 任意阻塞项不通过 → ❌ 回退修正
```

## 14 项质量门禁速查

| # | 缩写 | 级别 | 通过标准 |
|---|------|------|---------|
| Q1 | PLAN | **P0-阻塞** | 有内容规划且经确认 |
| Q2 | SEARCH | **P0-阻塞** | 已搜索并归档资料 |
| Q3 | LENGTH | P1-警告 | 行数在目标范围 ±20% |
| Q4 | SOURCE | P1-警告 | 关键数据有资料支持 |
| Q5 | ALIGN | P1-警告 | 内容与大纲结构一致 |
| Q6 | LANG | P1-警告 | 无注释/占位符 |
| Q7 | CITE | P2-建议 | 数据来源已标注 |
| Q8 | FMT | P2-建议 | 代码块/表格规范 |
| Q9 | ARCHIVE | P2-建议 | 资料已归档更新索引 |
| Q10 | TECH | P1-警告 | 技术栈与全书一致 |
| Q11 | DATA | **P0-阻塞** | 数据格式与相邻兼容 |
| Q12 | COVERAGE | P1-警告 | 大纲要点全覆盖 |
| Q13 | DEPTH | P1-警告 | 核心概念 S5 ≥ 4/6 |
| **Q14** | **WEB** | **P1-警告** | **mkdocs build 无报错** |

## 参考文件

- [完整质量门禁](references/quality-gates.md) — 14 项检查的详细方法与修正措施
- [跨章一致性规则](/references/cross-chapter-rules.md) — R7-R10 全局规则
- [本阶段决策细则](references/decision-record-rules.md) — review 阶段涉及的决策项
