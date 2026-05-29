---
name: architecture-decisions
version: 10.0.0
description: >
  高级架构决策。Monorepo vs Single-pkg、Wasm vs JS vs Native、
  Trait vs Enum、设计模式选择、SOLID 原则落地。
  Use when making architectural decisions for MoonBit projects,
  choosing between design patterns, or evaluating trade-offs.
trigger:
  - "架构" / "设计" / "该不该" / "选型"
  - "Monorepo" / "workspace" / "多包"
  - "设计模式" / "SOLID" / "Builder" / "DSL"
  - "Trait 还是 enum" / "怎么组织代码"
tags: [architecture, decision, monorepo, design-patterns, solid, dsl, trade-offs]
---

# 高级架构决策

## 触发条件
用户面临**技术选型或架构决策**时激活。

## 决策矩阵

### Monorepo vs Single Package

| 维度 | Single Package | Monorepo |
|------|---------------|----------|
| 代码量 | < 5000 行 | > 5000 行 |
| 包数量 | 1 个 | 2-10 个 |
| 团队规模 | 1-2 人 | 3+ 人 |
| 发布形式 | 单一产物 | 多产物（库+CLI+绑定）|
| 复杂度 | 低 | 中高 |
| **选择** | 大多数项目从这开始 | moon-lottie/morm 采用此模式 |

### Wasm-GC vs JS vs Native

| 目标 | 适用场景 | 优势 | 劣势 |
|------|---------|------|------|
| **wasm-gc** | 浏览器/边缘计算 | 安全沙箱、高性能 | 工具链较新 |
| **js** | Node.js/全栈 | 生态丰富、调试好 | 无类型安全 |
| **native** | 高性能/系统编程 | 最高性能 | 平台相关 |
| **双目标** | 需要 browser + server | 最大兼容 | 维护两套配置 |

### Trait vs Enum（多态选择）

| 场景 | 选择 | 原因 |
|------|------|------|
| 需要外部实现 | **pub(open)trait** | 开放扩展 |
| 固定变体集合 | **enum** | 编译期穷尽性检查 |
| 运行时策略切换 | **enum + match** | 简单直接 |
| 库作者定义接口 | **pub trait** | 封闭控制 |
| 回调/事件 | **函数类型** | 最轻量 |

### 设计模式选择

| 需求 | 推荐模式 | 来源 |
|------|---------|------|
| 复杂对象构建 | **Builder 模式** | morm CSRGraph |
| 类型间转换 | **Converter 模式** | mbtgraph 6 种 to_xxx |
| 平台差异抽象 | **Trait 多态** | moon-lottie PlatformRenderer |
| 条件分支替代 | **独立类型 + Trait** | mbtgraph 有向/无向分离 |
| DSL/配置 | **属性驱动** | morm #morm.* 属性 |

## 执行步骤

### Step 1: 明确约束
- 团队规模？目标平台？性能要求？交付时间？

### Step 2: 评估选项
对照上述决策矩阵评估备选方案。

### Step 3: 做出决策并记录
- 记录决策理由（ADR: Architecture Decision Record）
- 记录放弃的选项及原因

### Step 4: 验证可行性
- 创建原型验证关键假设
- 确认工具链支持

### Step 5: 文档化
- 将决策记录在项目 docs/ 或 ARCHITECTURE.md

## SOLID 原则在 MoonBit 中的体现

- **S (单一职责)**: 每个 .mbt 文件/包只做一件事
- **O (开闭)**: 用 pub(open)trait 扩展，不用修改已有代码
- **L (里氏替换)**: CSRGraph 不实现 GraphWritable（只读格式不应有 write 方法）
- **I (接口隔离)**: GraphEdgeIterable 和 GraphBatchReadable 是独立的小 trait
- **D (依赖倒转)**: 依赖 PlatformRenderer Trait 而非具体实现

## 详细知识
🔗 `references/library-design.md` Parts 12/14/15 — 架构模式和 SOLID
🔗 `references/project-layout.md` — Monorepo 模板（3种）
🔗 `references/real-world-examples.md` — 4 个真实项目架构案例
🔗 `references/multi-backend.md` — 双运行时架构
🔗 `references/decision-matrices.md` — 更多决策矩阵