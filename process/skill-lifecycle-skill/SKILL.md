---
name: skill-lifecycle
version: v3.0.0
author: skill-lifecycle
description: 技能全生命周期管理系统，基于轻/重/薄/厚四维分类，提供研究、分析、判定、生成、验证五阶段流程和五大场景指南
tags: [skill-management, lifecycle, classification, four-dimensions]
---

# Skill Lifecycle - 技能生命周期管理

## 任务目标

本 Skill 用于管理技能的全生命周期，从需求分析到最终交付的完整流程。

**触发条件**: 当你需要创建、修改、优化、整合或拆分技能时使用。

---

## 四维分类体系

```mermaid
flowchart TB
    subgraph 四维分类法
        direction LR
        L1["功能维度<br/>━━━━━━━━━━<br/>轻 单一功能<br/>重 多模块"]
        L2["内容维度<br/>━━━━━━━━━━<br/>厚 内容丰富<br/>薄 内容精简"]
    end
    
    Q1["🟢 轻+薄<br/>简单技能<br/>单文件 SKILL.md"]
    Q2["🔵 重+薄<br/>技能族-薄<br/>skills 子目录"]
    Q3["🟠 轻+厚<br/>复杂单技能<br/>SKILL.md + refs"]
    Q4["🟣 重+厚<br/>技能族-厚<br/>混合模式"]
    
    style Q1 fill:#e8f5e9,stroke:#4caf50,color:#1b5e20
    style Q2 fill:#e3f2fd,stroke:#2196f3,color:#0d47a1
    style Q3 fill:#fff3e0,stroke:#ff9800,color:#e65100
    style Q4 fill:#f3e5f5,stroke:#9c27b0,color:#4a148c
```

### 维度定义

| 维度 | 定义 | 判断标准 | 输出结构 |
|------|------|---------|---------|
| **轻** | 功能单一 | 1 个核心能力，逻辑简单 | 单个 SKILL.md |
| **重** | 功能复杂 | 多个模块，可独立使用 | `skills/{子}/SKILL.md` |
| **薄** | 内容精简 | 单文件 <300 行能描述清楚 | 无需额外文件 |
| **厚** | 内容丰富 | 需要详细说明、示例、代码等 | `references/` + 可选 `scripts/` `templates/` |

### 四种组合与输出结构

| 组合 | 类型 | 目录结构 | 典型场景 |
|------|------|---------|---------|
| **轻+薄** | 简单技能 | `{name}/SKILL.md` | 工具类、格式转换 |
| **重+薄** | 技能族(薄) | `{name}-family/SKILL.md` + `skills/{子}/SKILL.md` | CLI工具集、工作流编排器 |
| **轻+厚** | 复杂单技能 | `{name}/SKILL.md` + `references/*.md` | 数据处理管道、详细教程 |
| **重+厚** | 技能族(厚) | `{name}-family/SKILL.md` + `skills/{子}/` (+ 部分 `references/`) | 大型框架学习包 |

### 组织方式决策原则

```
┌─────────────────────────────────────────────────────────────┐
│                    组织方式设计原则                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  子技能 (skills/)          references (/)                   │
│  ┌───────────────┐         ┌───────────────┐               │
│  │   解耦模式     │         │   内聚模式      │               │
│  │   类似: 微服务  │         │   类似: 单体分层  │               │
│  └───────────────┘         └───────────────┘               │
│                                                             │
│  ★ 优先级：子技能拆分 > references 补充                     │
│  ★ 可共存：子技能内部可有 references                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| 维度 | 子技能 (skills/) | references (/) |
|------|------------------|----------------|
| 本质 | 解耦 | 内聚 |
| 类比 | 微服务 / 模块化 | 单体内部分层 |
| 适用 | 职责清晰、可独立调用 | 高度内聚、无法拆分 |
| 优先级 | ⭐ 首选 | ⭐ 兜底 |

---

## 五阶段工作流程

```mermaid
flowchart LR
    A[用户输入] --> R[① 研究 researcher]
    
    R -->|需求明确| N[需求文档]
    
    N --> AN[② 分析 analyzer]
    AN --> PL[③ 规划 planner]
    PL --> GE[④ 生成 generator]
    GE --> PA[⑤ 验证 packager]
    PA --> OUT[输出 技能包]
    
    subgraph 研究阶段内部
        direction TB
        R1[浏览内容]
        R2[交互确认]
        R3[搜索补充]
    end
    
    style A fill:#f5f5f5,color:#424242
    style R fill:#e8eaf6,stroke:#3f51b5,stroke-width:2px,color:#1a237e
    style N fill:#c5cae9,stroke:#303f9f,color:#1a237e
    style AN fill:#e3f2fd,stroke:#2196f3,color:#0d47a1
    style PL fill:#fff3e0,stroke:#ff9800,color:#e65100
    style GE fill:#e8f5e9,stroke:#4caf50,color:#1b5e20
    style PA fill:#fce4ec,stroke:#e91e63,color:#880e4f
```

### 阶段职责总览

| 阶段 | 核心职责 | 关键输出 | 对应 skill-factory 子技能 |
|------|----------|---------|------------------------|
| **① 研究** | 接收输入、交互确认、补充信息 | 需求文档 | researcher |
| **② 分析** | 提取技术信息，评估功能数量和内容体量 | 分析报告 | analyzer |
| **③ 规划** | 判定轻重薄厚，选择输出结构 | 拆分计划 | planner |
| **④ 生成** | 按四种类型生成对应目录和文件 | SKILL.md 文件 | generator |
| **⑤ 验证** | 验证对应结构的完整性 | 验证报告 | packager |

### 全程回调机制

在后续任何阶段发现信息不足时，都可以回调研究阶段：

```mermaid
sequenceDiagram
    participant User as 用户
    participant Res as 研究阶段
    participant Ana as 分析阶段
    
    User->>Res: 输入 URL 或需求
    Res->>Res: 浏览加交互加补充
    Res->>Ana: 需求文档
    
    Ana->>Ana: 分析中...
    Ana-->>Res: 缺少关键信息!
    
    Res->>User: 确认具体需求?
    User-->>Res: 明确了
    
    Res->>A: 补充完成
    Ana->>A: 继续分析
```

---

## 快速决策树

```mermaid
flowchart TD
    Start[需要操作技能?] --> Type{操作类型?}
    
    Type -->|创建新技能| C[scenario-create]
    Type -->|修改现有技能| M{变更类型?}
    Type -->|提升质量| O[scenario-optimize]
    Type -->|合并技能| I[scenario-integrate]
    Type -->|拆分技能| D[scenario-decompose]
    Type -->|编排工作流| W[workflow-generation]
    
    M -->|修复错误| M1[Fix: 小修补]
    M -->|添加功能| M2[Feature: 新增]
    M -->|破坏性变更| M3[Breaking: 大改]
    
    O -->|诊断问题| O1[原子化拆分]
    O -->|应用模式| O2[标准化接口]
    
    style C fill:#e8f5e9,stroke:#4caf50,color:#1b5e20
    style M fill:#e3f2fd,stroke:#2196f3,color:#0d47a1
    style O fill:#fff3e0,stroke:#ff9800,color:#e65100
    style I fill:#f3e5f5,stroke:#9c27b0,color:#4a148c
    style D fill:#fce4ec,stroke:#e91e63,color:#880e4f
    style W fill:#e8eaf6,stroke:#3f51b5,color:#1a237e
```

### 场景与四维分类映射

| 场景 | 适用情况 | 通常产出类型 | 推荐先判定 |
|------|---------|------------|-----------|
| scenario-create | 从零创建 | 先判定轻重薄厚 | 用户需求明确？ |
| scenario-modify | 修改已有 | 保持原类型或升级 | 变更影响范围？ |
| scenario-optimize | 提升质量 | 可能升级（薄→厚） | 问题根源是什么？ |
| scenario-integrate | 合并多技能 | 通常是重+薄或重+厚 | 模块间依赖关系？ |
| scenario-decompose | 拆分复杂 | 从重+厚 → 多个轻+薄 | 能否解耦？ |
| workflow-generation | 编排工作流 | 重+薄（协调器） | 流程是否固定？ |

---

## 场景索引

| 场景 | 适用情况 | 生命周期 | 输出物 | 类型判定参考 |
|------|---------|---------|--------|-------------|
| [scenario-create](skills/scenario-create/SKILL.md) | 从零创建新技能 | 设计→开发→测试→发布 | 新技能 SKILL.md | 用户输入 → researcher → 判定类型 |
| [scenario-modify](skills/scenario-modify/SKILL.md) | 修改已有技能 | 开发→测试→发布→维护 | 更新后的 SKILL.md | 变更类型 → 版本策略 |
| [scenario-optimize](skills/scenario-optimize/SKILL.md) | 提升技能质量 | 设计→开发→测试→发布 | 优化后的 SKILL.md | 问题诊断 → 优化策略 |
| [scenario-integrate](skills/scenario-integrate/SKILL.md) | 合并多个技能 | 设计→开发→测试→发布 | 整合后的 SKILL.md | 依赖分析 → 整合模式 |
| [scenario-decompose](skills/scenario-decompose/SKILL.md) | 拆分复杂技能 | 设计→开发→测试→发布 | 多个独立技能 | 能否解耦 → 拆分方案 |
| [workflow-generation](skills/workflow-generation/SKILL.md) | 编排工作流 | 设计→开发→测试→发布 | WORKFLOW.md | 流程特点 → 工作流模式 |

---

## 核心规范速查

### SKILL.md 必需结构

```yaml
---
name: <skill-name>           # 小写字母+连字符
version: v1.0.0              # v主.次.补丁
author: <作者>
description: <100-150字符描述>
tags: [tag1, tag2, tag3]    # 至少3个标签
---
```

### 正文必需章节

```markdown
## 任务目标
- 本 Skill 用于: <一句话说明>
- 核心能力: <能力要点>
- 触发条件: <何时使用>

## 操作步骤
1. <步骤1>
2. <步骤2>

## 使用示例
<示例>

## 注意事项
<注意点>
```

### 质量标准

| 检查项 | 标准 |
|-------|------|
| 正文行数 | < 500 行 |
| description | 100-150 字符 |
| tags | >= 3 个 |
| 必需章节 | 任务目标、操作步骤、示例 |

### 目录结构规范

| 类型 | 结构 | 说明 |
|------|------|------|
| **轻+薄** | `{name}/SKILL.md` | 单文件即可 |
| **重+薄** | `{name}-family/SKILL.md` + `skills/{子}/SKILL.md` | 外层解耦 |
| **轻+厚** | `{name}/SKILL.md` + `references/*.md` | 内聚分层 |
| **重+厚** | `{name}-family/SKILL.md` + `skills/(部分有references/)` | 混合模式 |

---

## 与 skill-factory 的关系

```mermaid
flowchart TB
    SL[skill-lifecycle<br/>生命周期管理] --> SF[skill-factory<br/>技能工厂]
    
    SL --> L1[场景操作指南<br/>create/modify/optimize<br/>integrate/decompose]
    SL --> L2[标准化规范<br/>skill-standards]
    SL --> L3[工作流编排<br/>workflow-generation]
    
    SF --> F1[研究阶段 researcher]
    SF --> F2[分析阶段 analyzer]
    SF --> F3[规划阶段 planner]
    SF --> F4[生成阶段 generator]
    SF --> F5[验证阶段 packager]
    
    L1 -->|使用| F1
    L2 -->|遵循| F1
    L3 -->|使用| F1
    
    style SL fill:#e8eaf6,stroke:#3f51b5,color:#1a237e
    style SF fill:#fff3e0,stroke:#ff9800,color:#e65100
    style L1 fill:#c5cae9,stroke:#303f9f,color:#1a237e
    style L2 fill:#c5cae9,stroke:#303f9f,color:#1a237e
    style L3 fill:#c5cae9,stroke:#303f9f,color:#1a237e
```

| 层次 | 定位 | 核心价值 |
|------|------|----------|
| **skill-lifecycle** | 顶层管理器 | 定义场景、提供规范、指导操作 |
| **skill-factory** | 执行引擎 | 五阶段流水线、四维分类判定、文件生成 |

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| v3.0.0 | 2026-04-30 | 整合四维分类体系、五阶段流程、与 skill-factory 对齐 |
| v2.1.0 | 2026-04-30 | 简化框架，增加决策树，移除冗余内容 |
| v2.0.0 | 2026-04-30 | 引入子技能结构 |
