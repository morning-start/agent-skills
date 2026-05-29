# agents-writer 快速导航

## 🗺️ 使用流程图

```
用户需求
    │
    ├── 新项目？ ──→ ① 分析项目 → ② 设计结构 → ③ 编写内容 → ⑤ 质量检查
    │
    ├── 要模板？ ──→ ④ 选择模板 → 按需定制 → ⑤ 质量检查
    │
    ├── 已有文件？──→ ⑤ 质量检查 → ⑥ 优化迭代
    │
    └── 学习？ ─────→ 查看 examples.md + best-practices.md
```

## 📚 子技能索引

| # | 子技能 | 触发条件 | 核心输出 |
|---|--------|---------|---------|
| 1 | [1-analyze-project](skills/1-analyze-project/SKILL.md) | "分析项目"、"什么类型" | 类型判定 + 复杂度评分 (0-100) |
| 2 | [2-design-structure](skills/2-design-structure/SKILL.md) | "设计结构"、"包含哪些章节" | 结构蓝图 + 字段清单 |
| 3 | [3-write-content](skills/3-write-content/SKILL.md) | "写AGENTS.md"、"编写内容" | 完整草稿 + 注释说明 |
| 4 | [4-select-template](skills/4-select-template/SKILL.md) | "给我模板"、"快速开始" | 可用模板 (3种规格) |
| 5 | [5-quality-check](skills/5-quality-check/SKILL.md) | "检查规范"、"质量验证" | 问题清单 + 修复建议 |
| 6 | [6-optimize-evolve](skills/6-optimize-evolve/SKILL.md) | "优化"、"减少Token" | 优化方案 + 维护计划 |

## 📖 知识库索引

| 文件 | 大小估算 | 内容概要 | 推荐阅读场景 |
|------|---------|---------|-------------|
| [best-practices.md](references/best-practices.md) | ~400行 | 28条最佳实践（结构10+内容12+格式6） | 编写前必读 |
| [type-classification.md](references/type-classification.md) | ~300行 | 5种类型详解 + 判定决策树 | 项目分析阶段 |
| [anti-patterns.md](references/anti-patterns.md) | ~350行 | 22个反模式（内容12+结构6+维护4） | 质量检查阶段 |
| [templates.md](references/templates.md) | ~500行 | 最小可行/标准/完整3套模板 | 快速开始场景 |
| [examples.md](references/examples.md) | ~400行 | 4个真实案例对比分析 | 学习参考 |
| [token-budget.md](references/token-budget.md) | ~250行 | Token预算分配 + 效率策略 | 优化阶段 |

## 📊 统计信息

| 维度 | 数据 |
|------|------|
| 子技能数量 | 6 |
| 知识库文件 | 6 |
| 最佳实践条数 | 28 |
| 反模式数量 | 22 |
| 模板规格 | 3 种（最小/标准/完整） |
| 真实案例 | 4 个 |
| 预估总行数 | ~2600 行（主文件+子技能+知识库） |

## 🔗 相关技能

- **skill-factory**: 技能创建方法论（本技能的元技能）
- **book-skills**: AGENTS.md 的实际应用案例
- **moonbit-skills**: 行动导向型 AGENTS.md 示例
