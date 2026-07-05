---
name: planning
version: v1.0.0
author: book-skills
description: 项目规划专家 — 支持远期路线图(ROADMAP)和近期任务规划(TODO)的全流程行动指南，集成OKR/SMART/Eisenhower矩阵/MoSCoW等最佳实践方法论，帮助AI Agent产出高质量的项目规划文档
tags: [planning, roadmap, todo, okr, smart, project-management, goal-setting, prioritization]
dependency:
  parent: none
  children: [1-roadmap-planner, 2-todo-planner]
---

# 项目规划专家 (Planning Skill)

## 激活条件

当用户需要以下任一操作时激活：
- 制定或更新项目的**远期规划**（ROADMAP / 路线图）
- 制定或更新项目的**近期任务计划**（TODO / 待办清单）
- 设定**目标和关键结果**（OKR）
- 进行**优先级排序**或任务分解
- 建立**里程碑**或**进度跟踪机制**

## 意图路由

| 用户意图 | 触发关键词/示例 | 执行子技能 | 核心输出 | 优先级 |
|---------|----------------|-----------|---------|--------|
| **🗺️ 远期规划** | "roadmap"/"路线图"/"远期目标"/"季度规划"/"年度计划" | [1-roadmap-planner](skills/1-roadmap-planner/SKILL.md) | `ROADMAP.md` 文件 | P0 |
| **✅ 近期规划** | "todo"/"待办"/"近期任务"/"本周计划"/"任务分解" | [2-todo-planner](skills/2-todo-planner/SKILL.md) | `TODO.md` 文件 | P0 |
| **🎯 设定OKR** | "okr"/"目标与关键结果"/"对齐目标" | [1-roadmap-planner](skills/1-roadmap-planner/SKILL.md) → OKR 章节 | OKR 对齐表 | P1 |
| **📊 优先级排序** | "优先级"/"MoSCoW"/"重要还是紧急"/"排序" | [2-todo-planner](skills/2-todo-planner/SKILL.md) → 排序方法 | 优先级矩阵 | P1 |
| **📍 里程碑管理** | "milestone"/"里程碑"/"阶段目标"/"节点" | [1-roadmap-planner](skills/1-roadmap-planner/SKILL.md) → 里程碑 | 里程碑时间轴 | P2 |
| **📈 进度跟踪** | "进度"/"跟踪"/"燃尽图"/"看板"/"健康度" | 见 [progress-tracking](references/progress-tracking.md) | 跟踪方案 | P2 |

## 通用工作流

所有规划任务遵循 **ANALYZE → DESIGN → CREATE → VALIDATE → DELIVER** 流程：

```
① ANALYZE（分析需求）
   │
   ├── 明确规划范围（远期 vs 近期？个人 vs 团队？）
   ├── 收集输入信息（项目现状/战略目标/资源约束/利益相关者）
   ├── 识别时间跨度（季度/年度/月度/周？）
   └── 确定使用的方法论组合（OKR? SMART? MoSCoW?）
   │
   ▼
② DESIGN（设计方案）
   │
   ├── 选择合适的模板（见 [roadmap-templates](references/roadmap-templates.md)）
   ├── 定义目标层级结构（愿景 → 年度目标 → 季度OKR → 月度任务）
   ├── 设计度量体系（如何衡量成功？）
   └── 规划评审节奏（何时回顾和调整？）
   │
   ▼
③ CREATE（生成文档）
   │
   ├── 编写 ROADMAP.md（如需远期规划）
   │   ├─ 战略愿景（1-3年方向）
   │   ├─ 季度目标（O + KR）
   │   ├─ 里程碑时间轴
   │   └─ 资源与风险
   │
   ├── 编写 TODO.md（如需近期规划）
   │   ├─ 当前冲刺/周期任务
   │   ├─ 优先级标记（P0/P1/P2 或 MoSCoW）
   │   ├─ 责任人与截止日期
   │   └─ 依赖关系与阻塞项
   │
   └── （可选）生成辅助文档
       ├─ OKR 对齐表
       └─ 进度跟踪配置
   │
   ▼
④ VALIDATE（质量验证）
   │
   ├── SMART 检查（目标是否具体/可衡量/可达成/相关/有时限？）
   ├── 完整性检查（是否覆盖所有关键维度？）
   ├── 可行性评估（资源和时间是否合理？）
   └── 利益相关者对齐（是否与上级目标一致？）
   │
   ▼
⑤ DELIVER（交付成果）
   │
   ├── 输出最终文档（ROADMAP.md / TODO.md）
   ├── 提供维护建议（多久更新一次？如何调整？）
   └── （可选）建立跟踪机制（看板/仪表盘/定期会议）
```

## 质量门禁

### 必须通过的检查项

#### 对于 ROADMAP.md（远期规划）

- [ ] **愿景清晰**: 有明确的 1-3 年方向描述
- [ ] **目标符合 OKR 标准**: O（定性激励性）+ KR（量化可衡量）
- [ ] **KR 符合 SMART**: 具体(S)/可衡量(M)/可实现(A)/相关(R)/有时限(T)
- [ ] **时间轴合理**: 里程碑分布均匀，无过度集中
- [ ] **包含风险评估**: 至少标注 3 个关键风险点
- [ ] **有明确的负责团队/人**

#### 对于 TODO.md（近期规划）

- [ ] **任务符合 SMART**: 每个任务都明确且可执行
- [ ] **优先级清晰**: 使用统一的标准（P0-P3 或 MoSCoW）
- [ ] **有时间约束**: 有明确的截止日期或时间盒
- [ ] **责任人明确**: 每个任务有 Owner
- [ ] **依赖关系可见**: 阻塞关系已标注
- [ ] **工作量估算**: 有预估工时或故事点

### 推荐验证命令

```bash
# 检查 ROADMAP 质量
if [ -f ROADMAP.md ]; then
  echo "=== ROADMAP 质量检查 ==="
  echo "行数: $(wc -l < ROADMAP.md)"
  grep -c "^## " ROADMAP.md  # 章节数
  grep -ciE "(Q[1-4]|202[0-9]|里程碑)" ROADMAP.md  # 时间标记数
fi

# 检查 TODO 质量
if [ -f TODO.md ]; then
  echo "=== TODO 质量检查 ==="
  echo "任务数: $(grep -c '^- \[' TODO.md)"
  grep -cE "\[P[0-3]\]|\[Must\]|\[Should\]" TODO.md  # 优先级标记数
  grep -cE "@.*\|负责人:" TODO.md  # 责任人标记数
fi
```

## 知识库索引

| 文件 | 内容概要 | 适用场景 |
|------|---------|---------|
| [okr-methodology.md](references/okr-methodology.md) | OKR完整方法论：目标设定/关键结果编写/对齐机制/评分复盘 | 设定远期目标时必读 |
| [smart-principle.md](references/smart-principle.md) | SMART原则5维实战指南 + 自检清单 | 验证目标质量时使用 |
| [roadmap-templates.md](references/roadmap-templates.md) | 4类ROADMAP模板（战略型/技术型/功能型/敏捷型） | 选择模板时参考 |
| [todo-methods.md](references/todo-methods.md) | 3种TODO方法（Eisenhower矩阵/MoSCoW/时间盒） | 任务排序时使用 |
| [progress-tracking.md](references/progress-tracking.md) | 进度跟踪方法（里程碑/燃尽图/看板/健康度指标） | 建立跟踪机制时参考 |
| [planning-examples.md](references/planning-examples.md) | 不同规模项目的真实规划案例 | 学习参考 |

## 子技能总览

| # | 子技能 | 核心能力 | 典型输出 | 适用场景 |
|---|--------|---------|---------|---------|
| 1 | [1-roadmap-planner](skills/1-roadmap-planner/SKILL.md) | 远期路线图规划 | `ROADMAP.md` | 季度/年度规划、OKR设定、里程碑定义 |
| 2 | [2-todo-planner](skills/2-todo-planner/SKILL.md) | 近期任务规划 | `TODO.md` | 周/月任务分解、优先级排序、Sprint规划 |

## 核心方法论速查

### 🎯 OKR（目标与关键结果）

```
目标 (Objective): 定性、激励性、回答"我们要做什么"
    ↓
关键结果 (Key Results): 量化、可衡量、回答"怎么知道做到了"
    ├─ KR1: 具体指标 + 目标值 + 时间
    ├─ KR2: 具体指标 + 目标值 + 时间
    └─ KR3: 具体指标 + 目标值 + 时间

标准配置: 1-3 个 O，每个 O 对应 2-5 个 KR
周期推荐: 季度（3个月）/ 月度跟踪 / 年度对齐
```

> 📖 详见: [okr-methodology.md](references/okr-methodology.md)

### 📏 SMART 原则

| 维度 | 问题 | 检验标准 |
|------|------|---------|
| **S**pecific | 要完成什么？ | 清晰明确，无歧义 |
| **M**easurable | 如何衡量？ | 可量化（数字/百分比/频率） |
| **A**chievable | 能做到吗？ | 跳一跳够得着，非遥不可及 |
| **R**elevant | 为什么重要？ | 与大目标/战略一致 |
| **T**ime-bound | 何时完成？ | 有明确截止日期 |

> 📖 详见: [smart-principle.md](references/smart-principle.md)

### 📊 优先级方法对比

| 方法 | 适用场景 | 核心逻辑 | 输出格式 |
|------|---------|---------|---------|
| **P0-P3** | 通用任务分级 | 影响力×紧急度 | 4级优先级 |
| **MoSCoW** | 需求/功能排序 | Must/Should/Could/Won't | 4类标签 |
| **Eisenhower** | 个人效率 | 重要×紧急 | 4象限矩阵 |
| **RICE** | 产品功能 | Reach×Impact×Confidence/Effort | 数值评分 |
| **WSJF** | 敏捷开发 | 价值/Size/Job/Complexity/Failure | 故事点权重 |

> 📖 详见: [todo-methods.md](references/todo-methods.md)

## 数据来源

本技能基于以下研究和实践构建：
- **理论来源**: OKR (John Doerr/Andy Grove)、SMART (Peter Drucker)、MoSCoW (敏捷开发)
- **实践来源**: Atlassian/Google/Intel 的 OKR 实施指南、产品路线图最佳实践（ProcessOn/Lark）
- **工具参考**: Jira Roadmap/Trello/Asana/Notion 的规划功能设计

## 注意事项

⚠️ **核心理念**: 本技能产出的是**规划文档**（ROADMAP/TODO），不是执行计划（那是 Project Manager 的工作）。规划 = "做什么 + 为什么 + 何时"，而非 "怎么做"。

⚠️ **规划 vs 计划的区别**:
- **规划 (Planning)**: 战略层面，确定方向、目标、优先级（本技能的范围）
- **计划 (Scheduling)**: 战术层面，拆解任务、分配资源、排期（超出本技能范围）

⚠️ **动态调整意识**: 规划不是静态文档！建议：
  - ROADMAP: 季度评审 + 必要时调整
  - TODO: 周/双周更新 + 每日站会同步

⚠️ **方法论选择建议**:
  - **个人项目** → SMART + 简单 TODO 即可
  - **小团队 (2-5人)** → OKR (简化版) + MoSCoW TODO
  - **中大型团队 (5+人)** → 完整 OKR + Eisenhower + 看板跟踪
  - **企业级** → OKR 全套 + RICE评分 + 仪表盘监控

⚠️ **避免过度规划**:
  - 规划时间不应超过执行时间的 10%
  - 远期规划（>6个月）的细节度应递减
  - 保持"现在-接下来-未来"(Now-Next-Later)的三段式结构

## 版本历史

| 版本 | 日期 | 主要变更 |
|------|------|---------|
| **v1.0.0** | 2026-05-17 | 🎉 初始版本：完整的规划技能，包含 ROADMAP + TODO 双模块，集成 6 大方法论 |
