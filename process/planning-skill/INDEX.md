# planning-skill 快速导航

## 🗺️ 使用流程图

```
用户需求
    │
    ├── 需要远期规划？ ──→ ① roadmap-planner → ROADMAP.md
    │   触发词: "roadmap"/"路线图"/"季度目标"/"年度规划"
    │   输出: 战略愿景 + OKR + 里程碑 + 风险评估
    │
    ├── 需要近期任务？ ──→ ② todo-planner → TODO.md
    │   触发词: "todo"/"待办"/"本周计划"/"任务分解"
    │   输出: 任务列表 + 优先级 + 责任人 + 截止日期
    │
    ├── 仅需设定目标？ ──→ ① → OKR 章节（轻量模式）
    │   触发词: "okr"/"设定目标"/"对齐"
    │
    └── 仅需排序？ ──→ ② → 排序方法章节（快速模式）
        触发词: "优先级"/"排序"/"重要紧急"
```

## 📚 子技能索引

| # | 子技能 | 触发条件 | 核心输出 | 典型耗时 |
|---|--------|---------|---------|---------|
| 1 | [1-roadmap-planner](skills/1-roadmap-planner/SKILL.md) | 远期/战略/季度/年度/OKR/milestone | `ROADMAP.md` (50-150行) | 30-60min |
| 2 | [2-todo-planner](skills/2-todo-planner/SKILL.md) | 近期/待办/周/月/sprint/todo | `TODO.md` (30-100行) | 15-30min |

## 📖 知识库索引

| 文件 | 大小估算 | 内容概要 | 推荐阅读场景 |
|------|---------|---------|-------------|
| [okr-methodology.md](references/okr-methodology.md) | ~400行 | OKR完整方法论（目标/KR/对齐/评分/复盘） | 设定OKR前必读 |
| [smart-principle.md](references/smart-principle.md) | ~250行 | SMART 5维详解 + 自检清单 + 常见错误 | 验证目标质量 |
| [roadmap-templates.md](references/roadmap-templates.md) | ~450行 | 4类模板（战略/技术/功能/敏捷）+ 选择指南 | 创建ROADMAP时参考 |
| [todo-methods.md](references/todo-methods.md) | ~350行 | Eisenhower/MoSCoW/时间盒 + 对比表 + 实战技巧 | 任务排序时使用 |
| [progress-tracking.md](references/progress-tracking.md) | ~300行 | 里程碑/燃尽图/看板/健康度指标 | 建立跟踪机制 |
| [planning-examples.md](references/planning-examples.md) | ~350行 | 3个真实案例（个人/小团队/企业） | 学习参考 |

## 🎯 方法论选择决策树

```
项目类型？
    │
    ├── 个人项目
    │   ├── 目标简单? → SMART原则 + 简单TODO ✅
    │   └── 有长期目标? → 简化版OKR (1个O + 3KR) + 月度TODO
    │
    ├── 小团队 (2-5人)
    │   ├── 季度规划? → OKR (2-3个O) + MoSCoW TODO + 周站会
    │   └── 敏捷开发? → Sprint Planning + Story Mapping + 燃尽图
    │
    ├── 中型团队 (6-15人)
    │   ├── 多部门协作? → 完整OKR对齐 + RICE优先级 + 里程碑跟踪
    │   └── 产品导向? → 产品路线图(Now-Next-Later) + 功能MoSCoW
    │
    └── 大型企业 (15+人)
        ├── 战略层 → 公司OKR → 部门OKR → 团队OKR（三层对齐）
        ├── 执行层 → 季度Roadmap + 月度KPI + 周Sprint
        └── 监控层 → 仪表盘 + 自动化报告 + 季度Business Review
```

## 📊 输出文件规范

### ROADMAP.md 标准结构

```markdown
# {项目名} 路线图 ({时间范围})

## 🎯 愿景与战略方向
{1-3年的北极星目标}

## 📅 {当前年份} 目标与里程碑

### Q{N} (或 H{N})
**目标 O{N}**: {定性描述}

| KR | 指标 | 当前值 | 目标值 | 负责人 | 截止日期 | 状态 |
|----|------|--------|--------|--------|----------|------|
| KR1 | {可量化指标} | {X} | {Y} | {Who} | {When} | 🔴🟢🟢 |

#### 关键里程碑
- **M{N}**: {里程碑描述} ({日期})
- **M{N+1}:** {下一个里程碑}

### Q{N+1}
...

## ⚠️ 风险与依赖
| 风险 | 影响 | 概率 | 应对策略 |
|------|------|------|---------|
| ... | ... | ... | ... |

## 📚 相关文档
- OKR 详细版: [okr-{year}-q{n}.md]
- TODO 近期: [TODO.md](../TODO.md)
```

### TODO.md 标准结构

```markdown
# {项目名} 待办事项 ({周期})

## 📍 本周期重点
{本 sprint/周/月的核心目标（1-2句话）}

## 🚀 P0 - 必须完成 (Must)

### [ ] {任务1}
- **负责人**: @{who}
- **截止**: {when}
- **预估**: {story points 或 hours}
- **依赖**: 无 / #{issue}
- **验收标准**: {done的定义}

## ⭐ P1 - 应该完成 (Should)
...

## 💡 P2 - 可以完成 (Could)
...

## ❄ P3 - 未来考虑 (Won't)
...

## 🚧 阻塞项 & 依赖
| 任务 | 被谁阻塞 | 预计解除 | 备注 |
|------|---------|---------|------|
| ... | ... | ... | ... |

## 📈 进度概览
- 总任务数: {N}
- 已完成: {X} ({%})
- 进行中: {Y}
- 未开始: {Z}
```

## 🔗 相关技能

- **agents-writer**: 如何写 AGENTS.md（规划完成后可能需要更新）
- **skill-factory**: 技能创建方法论（如果规划的是技能库项目）

## 统计信息

| 维度 | 数据 |
|------|------|
| 子技能数量 | 2 |
| 知识库文件 | 6 |
| 方法论数量 | 6 (OKR/SMART/RICE/MoSCoW/Eisenhower/WSJF) |
| 模板数量 | 4+ (战略/技术/功能/敏捷) |
| 预估总行数 | ~2100 行（主文件+子技能+知识库） |
