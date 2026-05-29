# 决策记录系统完整规范

> 本文档是决策记录系统的主索引，将完整规范按主题拆分为 4 个专注文件。

## 文件索引

| # | 文件 | 内容 | 行数 |
|---|------|------|------|
| 1 | [决策数据模型](decision-data-model.md) | 5 大类 20 个预定义决策项 + 状态机 + 字段定义 | ~150 行 |
| 2 | [双存储方案](decision-storage.md) | JSON 文件主存储 + Memory 缓存 + 同步策略 | ~130 行 |
| 3 | [Agent 讨论与用户交互](decision-discussion.md) | 讨论引导 + 动态更新 + 冲突解决 + 交互协议 | ~380 行 |
| 4 | [决策系统集成指南](decision-integration.md) | 架构定位 + PRWRD 集成 + 快速启动 + 最佳实践 | ~240 行 |

## 快速导航

| 关注点 | 查阅文件 |
|--------|---------|
| 有哪些决策项？各是什么类型？ | [决策数据模型](decision-data-model.md) |
| 状态机如何流转？ | [决策数据模型 → 状态机](decision-data-model.md#决策项状态机) |
| 数据如何持久化？ | [双存储方案](decision-storage.md) |
| Agent 如何引导讨论？ | [Agent 讨论与用户交互 → 6 步法](decision-discussion.md#讨论引导流程6-步法) |
| 如何修改已有决策？ | [Agent 讨论与用户交互 → 修改流程](decision-discussion.md#修改决策的标准流程) |
| 冲突如何处理？ | [Agent 讨论与用户交互 → 冲突检测](decision-discussion.md#冲突检测与处理) |
| 如何集成到 PRWRD 工作流？ | [集成指南 → 各阶段检查点](decision-integration.md#各阶段的决策检查点) |
| 如何快速初始化？ | [集成指南 → 快速启动](decision-integration.md#快速启动指南) |

---

**最后更新**: 2026-05-29
**版本**: v1.1.0（拆分为 4 个专注文件）
