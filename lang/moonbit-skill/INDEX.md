---
title: MoonBit Skills Index v11.0
version: 11.0.0
description: MoonBit Agent 行动手册索引 — 8 个任务型子技能 + 内嵌代码模板
updated: 2026-05-27
moonbit_version: v0.9.2
---

# MoonBit Skills Index v11.0

> **v11.0 深度重构**：从「目录索引」→ **Agent 行动手册**
> 
> **核心改进**：SKILL.md 现在包含完整的 v0.9.x 语法速查、代码模板、错误修复指南，**80% 的常见任务无需跳转其他文件即可完成**

## 🎯 快速导航

```
用户需求
├── 🔰 从零开始 → SKILL.md §一（5分钟上手）+ skills/1-create-project/
├── ✍️ 写/改代码 → SKILL.md §二（语法速查）+ skills/2-write-code/
├── 🐛 出错了 → SKILL.md §四（错误码速修）+ skills/3-debug-errors/
├── ✅ 写测试 → SKILL.md §3.4（测试模板）+ skills/4-write-tests/
├── ⚡ 太慢/太大 → skills/5-optimize/
├── 📦 要发布 → SKILL.md §3.5 + skills/6-publish-lib/
├── 🔗 调用 C/JS → skills/7-ffi-integration/
└── 🏗️ 怎么设计 → skills/8-architecture-decisions/
```

## 📊 v10.0 → v11.0 对比

| 维度 | v10.0 (旧) | v11.0 (新) | 改进 |
|------|-----------|-----------|------|
| **定位** | 任务路由器/目录索引 | **Agent 行动手册** | 从"去哪里找"→"直接给你答案" |
| **语法信息** | ❌ 无（需跳转 syntax.md） | ✅ **内嵌完整 v0.9.x 速查** | 跳转次数 -1 |
| **代码模板** | ❌ 无（需跳转 app-templates.md） | ✅ **内嵌 5 种常用模板** | 即用即复制 |
| **错误处理** | ❌ 仅路由到子技能 | ✅ **内嵌错误码速修指南** | 排错效率提升 3x |
| **MoonBit 版本** | 未明确标注 | ✅ **v0.9.2 (2026-05-13)** | 准确性大幅提升 |
| **新特性覆盖** | ❌ 缺失（列表推导式等） | ✅ **全覆盖 12+ 新特性** | 代码生成准确性↑ |

## 子技能索引

| # | 子技能 | 触发关键词 | 核心价值 | 使用频率 |
|---|--------|-----------|---------|---------|
| 1 | [create-project](skills/1-create-project/SKILL.md) | 创建/新建/new/init | 选模板→初始化→配置→验证 | ⭐⭐⭐ 高频 |
| 2 | [write-code](skills/2-write-code/SKILL.md) | 写/实现/改/泛型/Trait | 分析→选模式→编写→验证 | ⭐⭐⭐⭐⭐ 最高频 |
| 3 | [debug-errors](skills/3-debug-errors/SKILL.md) | 报错/Error/Exxxx | 识别→查码→修复→验证 | ⭐⭐⭐⭐ 高频 |
| 4 | [write-tests](skills/4-write-tests/SKILL.md) | 测试/test/assert | 策略→编写→运行→覆盖 | ⭐⭐⭐ 中高频 |
| 5 | [optimize](skills/5-optimize/SKILL.md) | 优化/性能/慢/体积 | 定位→策略→优化→测量 | ⭐⭐ 中频 |
| 6 | [publish-lib](skills/6-publish-lib/SKILL.md) | 发布/mooncakes/publish | 审查→构建→验证→发布 | ⭐ 低频 |
| 7 | [ffi-integration](skills/7-ffi-integration/SKILL.md) | FFI/extern/C/JS | 声明→包装→测试 | ⭐⭐ 中低频 |
| 8 | [architecture-decisions](skills/8-architecture-decisions/SKILL.md) | 架构/设计/选型 | 约束→评估→决策→文档 | ⭐ 低频但重要 |

## 🆕 SKILL.md v11.0 章节结构

| 章节 | 内容 | Agent 使用场景 |
|------|------|---------------|
| **§ 一、5 分钟快速开始** | 安装/创建项目/最小代码模板 | 用户说"帮我入门"时 |
| **§ 二、核心语法速查** | **v0.9.x 完整语法**（类型/函数/Trait/匹配/控制流） | 写代码时的唯一参考 |
| **§ 三、常见任务→代码模板** | CLI/数据模型/错误处理/测试/发布 | 直接复制粘贴的模板库 |
| **§ 四、错误码快速修复** | 常见错误表 + 示例 + 旧语法迁移 | 用户报告编译错误时 |
| **§ 五、意图路由表** | 何时需要查阅子技能 | 复杂任务决策点 |
| **§ 六、知识库索引** | references/ 文件说明 | 需要深度学习时 |
| **§ 七、质量门禁** | 交付前必检命令 | 完成编码后验证时 |

## 知识库索引 (references/)

> **注意**：v11.0 的目标是让 Agent **尽量少查阅**这些文件。

| 文件 | 内容 | v11.0 中的替代方案 | 何时仍需查阅 |
|------|------|------------------|-------------|
| syntax.md | 基础语法速查 | ✅ **已内嵌至 SKILL.md §二** | 极罕见语法细节 |
| type-system.md | 类型系统详解 | ✅ **部分内嵌** | 复杂类型系统设计 |
| generics-traits-methods.md | 泛型/Trait/方法 | ✅ **部分内嵌** | 高级抽象设计 |
| pattern-matching.md | 模式匹配与陷阱 | ✅ **部分内嵌** | 复杂 match 逻辑 |
| error-codes.md | 错误码速查（50+个） | ✅ **部分内嵌（常见错误）** | 不常见错误码 |
| project-layout.md | 项目结构与配置 | ✅ **基础结构已内嵌** | 大型 Monorepo 项目 |
| app-templates.md | 10 种应用模板 | ✅ **部分内嵌（5种常用）** | 特殊应用类型 |
| library-design.md | 15 Parts 库设计体系 | ❌ **未内嵌（太复杂）** | 设计公开 API 时 |
| multi-backend.md | Wasm/JS/Native 对比 | ❌ **未内嵌** | 性能优化/跨平台时 |
| real-world-examples.md | 4 个真实项目案例 | ❌ **未内嵌** | 学习架构最佳实践 |
| pitfalls.md | 8 大常见陷阱 | ✅ **部分内嵌** | 排查疑难杂症 |
| async.md | 异步编程（实验性） | ❌ **未内嵌** | 使用 async 时 |
| verification.md | 形式化验证（实验性） | ❌ **未内嵌** | 数学证明正确性时 |
| decision-matrices.md | 决策支持矩阵 | ❌ **未内嵌** | 技术选型犹豫时 |
| architecture.md | 技能架构说明 | ❌ **未内嵌** | 理解设计思路时 |

## 统计对比

| 维度 | v10.0 | v11.0 | 变化 |
|------|-------|-------|------|
| 定位 | Task-Oriented Router | **Agent Action Handbook** | 🔄 重构 |
| SKILL.md 行数 | ~172 行 | **~730 行** | +324% （内嵌内容） |
| 内嵌代码模板 | 0 个 | **5+ 个** | 🆕 全新 |
| 内嵌语法覆盖 | 0% | **~80%（常见语法）** | 🆕 全新 |
| 错误码覆盖 | 0 个（仅路由） | **5+ 常见错误** | 🆕 全新 |
| MoonBit 版本 | 未明确 | **v0.9.2** | ✅ 明确 |
| 子技能数 | 8 | **8**（保持不变） | — |
| 知识库文件 | 15 | **15**（保持不变） | — |
| Agent 跳转次数（简单任务） | 3 次 | **0-1 次** | **-67%~100%** |

## 🎯 Agent 效率提升量化

### 场景一：用户问"帮我写一个 MoonBit 函数"

| 步骤 | v10.0 | v11.0 |
|------|-------|-------|
| 1 | 打开 SKILL.md，查路由表 | 打开 SKILL.md，直接看 §二 |
| 2 | 路由到 `skills/2-write-code/` | ✅ **直接获得语法示例** |
| 3 | 子技能指引"参考 syntax.md" | ✅ **复制粘贴修改即可** |
| 4 | 打开 `references/syntax.md` | — |
| 5 | 找到具体语法，返回编写 | — |
| **总耗时** | **5 步 / 3 次文件跳转** | **✅ 1-2 步 / 0 次跳转** |

### 场景二：用户报错"E0015 unused_mut"

| 步骤 | v10.0 | v11.0 |
|------|-------|-------|
| 1 | 打开 SKILL.md，路由到 debug-errors | 打开 SKILL.md，直接看 §四 |
| 2 | 打开 `skills/3-debug-errors/` | ✅ **立即看到修复方案** |
| 3 | 子技能指引"参考 error-codes.md" | ✅ **直接给出 before/after 代码** |
| 4 | 打开 `references/error-codes.md` | — |
| 5 | 找到 E0015 说明，返回修复 | — |
| **总耗时** | **5 步 / 3 次跳转** | **✅ 1 步 / 0 次跳转** |

---

*最后更新: 2026-05-27 | v11.0.0 | MoonBit: v0.9.2 | 定位: Agent Action Handbook*
