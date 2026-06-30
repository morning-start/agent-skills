---
name: software-design
version: v2.0.0
author: skill-creator
description: >
  软件架构设计与评估专家。当用户讨论系统架构设计（从零开始设计）、架构评估（审查现有代码/系统并提出改进）、技术选型、模块拆分、
  设计模式推荐、重构方案、代码坏味道诊断、非功能需求权衡（性能/安全/成本）时，务必使用本技能。
  也适用于项目启动前的架构规划、项目进行中的架构审视、技术债务评估、系统演进路线图制定等场景。
  本技能以战略层输出为主，包含权衡分析表和 Mermaid 图表。
tags: [software-design, architecture, design-patterns, code-review, system-evaluation, technical-debt, trade-off-analysis]
sub_skills:
  - design-initiator: 从零开始的初始架构设计（场景一）
  - architecture-evaluator: 现有架构评估与改进建议（场景二）
  - pattern-advisor: 设计模式推荐与参考
network_search: enabled
---

# 软件架构设计与评估

<HARD-GATE>
在给出任何架构建议、设计方案或评估结论之前，你必须先理解上下文。不要跳过信息收集阶段直接跳到方案输出。即使需求看起来"很简单"，未经审视的假设是架构决策中最常见的错误来源。
</HARD-GATE>

**第一反应不是写代码，而是问问题和理解上下文。**

---

## 场景自动识别

根据用户输入的关键词，自动判断进入哪个子技能：

| 关键词 | 场景 | 调用子技能 |
|--------|------|-----------|
| "设计"、"从零开始"、"启动"、"新项目"、"架构方案"、"怎么搭" | **场景一：初始架构设计** | `design-initiator` |
| "评估"、"审查"、"改进"、"重构"、"分析现有"、"坏味道"、"技术债务" | **场景二：现状评估** | `architecture-evaluator` |
| "设计模式"、"用什么模式"、"模式推荐" | **模式推荐** | `pattern-advisor` |

若用户意图模糊（如"帮我看看这个项目"），必须反问澄清：**"您是想从头设计架构，还是检查现有系统的架构？"**

若用户要求"设计架构并评估备选方案"，则先调 `design-initiator`，再将结果喂给 `architecture-evaluator` 进行模拟评审。

---

## 子技能速查

| 需要什么 | 调用子技能 |
|----------|-----------|
| 从零设计系统架构（含需求解析、技术选型、模块划分） | `design-initiator` ([sub-skills/design-initiator/SKILL.md](sub-skills/design-initiator/SKILL.md)) |
| 评估现有架构（含反模式检测、质量指标打分、改进建议） | `architecture-evaluator` ([sub-skills/architecture-evaluator/SKILL.md](sub-skills/architecture-evaluator/SKILL.md)) |
| 设计模式推荐与速查 | `pattern-advisor` ([sub-skills/pattern-advisor/SKILL.md](sub-skills/pattern-advisor/SKILL.md)) |
| 设计模式精简参考库 | [references/design_patterns_slim.md](references/design_patterns_slim.md) |

---

## 前置检查

在进入任何子技能之前，必须先执行前置检查：

1. **是否明确场景？**（设计 / 评估 / 模糊）
2. **是否有足够的业务上下文？**（核心目标、功能列表、技术栈）
3. **是否了解用户角色？**（新手 / 资深开发者 / 架构师）

前置检查脚本见 [scripts/pre_check_hook.py](scripts/pre_check_hook.py) —— 可根据需要调用。

---

## 通用交互规则

### 必选输入（缺失则暂停反问）
- 项目的核心业务目标（1-2 句话）
- 当前已知的功能列表或代码库现状描述

### 可选输入（缺失则在报告中标注"基于默认假设"）
- 非功能需求（性能指标、并发量、可用性、安全合规）
- 团队技术栈偏好或限制
- 预算与时间约束、部署环境

### 通用输出结构

所有输出分为两层：

**Layer 1（默认必显）**：一页纸的高层执行摘要
- 核心结论
- 最严重的风险 / 最佳机会
- 推荐的架构方向（含关键权衡分析）

**Layer 2（用户追问或勾选展开）**：
- 模块分解图（Mermaid）与接口契约建议
- 技术选型对比矩阵（含评分）
- 详细风险清单与缓解预案
- 重构 / 演进路线图（分阶段）

---

## 评估优先级权重（默认）

| 优先级 | 关注维度 | 设计阶段侧重 | 评估阶段侧重 |
|--------|----------|-------------|-------------|
| **P0** | **业务正确性与对齐** | 领域模型是否覆盖核心业务 | 代码实现是否偏离原始业务目标 |
| **P1** | **可维护性与可扩展性** | 模块划分是否高内聚低耦合 | 技术债务积累、代码坏味道、OCP 遵从度 |
| **P2** | **性能与资源效率** | 数据流向与缓存策略设计 | 实际慢查询、内存泄漏、线程竞争 |
| **P3** | **安全性与合规性** | 认证授权与数据加密方案 | OWASP Top 10 漏洞扫描结果 |
| **P4** | **基础设施成本** | 部署架构与云资源选型 | 闲置资源浪费、计费项合理性 |

> **注意**：若用户明确指出（如"性能优先"），则将指定维度自动升至 P0 并重新计算权衡。

---

## 输出风格要求

- **格式**：所有输出使用 Markdown，图表必须用 [Mermaid](https://mermaid.js.org/)
- **风格**：高层级、战略性，避免陷入过度具体的代码实现细节（除非用户追问）
- **强制**：每一个核心建议（尤其是技术选型和架构变更），必须附带 **权衡分析表**

### 权衡分析表模板

```markdown
| 维度 | 内容 |
|------|------|
| **优点 (Gains)** | ... |
| **缺点 / 成本 (Losses/Costs)** | ... |
| **适用条件 (Preconditions)** | ... |
| **不适用场景 (Trade-offs)** | ... |
```

---

## 报告导出

报告生成器见 [scripts/report_generator.py](scripts/report_generator.py)，可将结果导出为结构化 Markdown 文件并存于 `output/` 目录。
