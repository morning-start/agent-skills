---
name: code-optimizer
version: v1.0.0
author: skill-manager
description: 代码优化专家技能，基于三层分析漏斗架构（静态合规层、逻辑与结构层、性能与安全层），提供专业代码诊断和重构建议
tags: [code-optimization, refactoring, code-review, static-analysis, performance]
---

# 代码优化专家 (Code Optimizer)

## 任务目标

本技能是一个专业的代码优化和分析工具，旨在通过分层、多维度、可解释的分析框架，提升代码质量并作为 AI 辅助编程的核心能力。

### 核心价值

- **分层分析**: 避免"过度优化"或"无效建议"，采用三层分析漏斗架构
- **专业诊断**: 基于 20 年资深架构师经验，提供精准的代码问题诊断
- **可执行建议**: 不仅指出问题，更提供具体的重构方案和代码示例
- **技术栈感知**: 根据不同编程语言和框架，提供针对性的优化建议

### 适用场景

- 代码审查 (Code Review)
- 重构遗留代码
- 性能瓶颈分析
- 安全性审计
- 技术债务清理
- 最佳实践指导

---

## 核心架构设计：三层分析漏斗

```
┌─────────────────────────────────────────────────────────────┐
│  L1: 静态合规层 (Static Compliance)                           │
│  ├── 命名规范检查                                              │
│  ├── 注释缺失检测                                              │
│  ├── 未使用的变量/函数                                         │
│  ├── 死代码识别                                                │
│  └── 潜在语法错误                                              │
├─────────────────────────────────────────────────────────────┤
│  L2: 逻辑与结构层 (Logic & Structure)                         │
│  ├── DRY 原则：重复代码块识别                                  │
│  ├── 单一职责：函数/类长度分析                                 │
│  ├── 魔法数字/字符串：硬编码值提取                             │
│  ├── 循环复杂度：嵌套深度检测                                  │
│  └── 抽象不足：设计模式应用建议                                │
├─────────────────────────────────────────────────────────────┤
│  L3: 性能与安全层 (Performance & Security)                    │
│  ├── 时间/空间复杂度分析                                       │
│  ├── SQL 注入风险检测                                          │
│  ├── 资源泄漏：文件句柄/数据库连接                             │
│  ├── 并发竞争条件                                              │
│  └── 安全漏洞：XSS/CSRF/硬编码密钥                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 操作步骤

### 第一步：上下文理解

在分析代码前，先理解代码的业务场景和使用环境：

**关键问题**:
1. 这段代码的用途是什么？（高频交易接口 vs 后台管理脚本）
2. 性能要求如何？（低延迟 vs 批处理）
3. 安全性要求？（公开 API vs 内部工具）
4. 技术栈是什么？（Python/Java/JavaScript/Go等）

### 第二步：三层分析扫描

按照 L1 → L2 → L3 的顺序逐层分析：

1. **L1 静态合规层**: 检查命名规范、注释完整性、未使用代码、死代码、语法风险
2. **L2 逻辑与结构层**: 检查重复代码、函数长度、魔法数字、循环嵌套、圈复杂度
3. **L3 性能与安全层**: 检查算法复杂度、资源泄漏、安全风险、并发问题

**详细检测清单**: 见 [references/checklist.md](references/checklist.md)

### 第三步：生成优化报告

按照标准格式生成包含问题汇总、重构方案、性能建议的完整报告。

**报告模板**: 见 [references/report-template.md](references/report-template.md)

---

## 核心能力

### 1. 三层分析漏斗

- **L1 静态合规**: 基础语法和最佳实践检查
- **L2 逻辑结构**: 代码重复、抽象程度、可维护性分析
- **L3 性能安全**: 性能瓶颈、安全漏洞、并发问题检测

**详细架构**: 见 [references/architecture.md](references/architecture.md)

### 2. Prompt Engineering 策略

- **角色设定**: 20 年资深架构师和代码审查专家
- **思维链工作流**: 上下文理解 → 三层扫描 → 报告生成
- **输出原则**: 先诊断后建议、拒绝过度设计、保持向后兼容

**详细策略**: 见 [references/prompt-strategy.md](references/prompt-strategy.md)

### 3. 技术栈感知

根据技术栈推荐相应工具链：

- **Python**: mypy, pylint, black, pytest
- **Java**: SpotBugs, SonarQube, JUnit
- **JavaScript/TypeScript**: ESLint, TypeScript, Jest
- **Go**: golangci-lint, pprof, testing

**完整推荐**: 见 [references/tech-stack.md](references/tech-stack.md)

---

## 输出格式规范

### 问题优先级定义

| 优先级 | 标识 | 描述 | 响应时间 |
|--------|------|------|----------|
| **P0** | 🔴 | 严重 Bug/安全漏洞，必须立即修复 | 立即 |
| **P1** | 🟠 | 性能瓶颈/逻辑缺陷，尽快修复 | 24 小时内 |
| **P2** | 🟡 | 可维护性问题，计划内修复 | 下次迭代 |
| **P3** | 🟢 | 优化建议，有空时处理 | 技术债务 |

### 标准报告结构

1. 总体评估（复杂度、可维护性、主要风险）
2. 问题汇总（按优先级排序）
3. 关键问题与重构方案（含代码对比）
4. 性能优化建议
5. 安全性检查清单
6. 后续行动计划

**完整模板**: 见 [references/report-template.md](references/report-template.md)

---

## 使用示例

### 示例 1: Python 代码优化

优化包含魔法数字、嵌套过深的订单处理函数。

**查看完整示例**: [references/examples.md#示例-1-python-代码优化](references/examples.md#示例-1-python-代码优化)

### 示例 2: JavaScript 性能优化

修复 N+1 查询问题和 SQL 注入漏洞。

**查看完整示例**: [references/examples.md#示例-2-javascript-性能优化](references/examples.md#示例-2-javascript-性能优化)

---

## 进阶功能

### 1. 交互式重构

采用对话式交互，先列出检测到的问题，让用户选择优先查看哪个问题的详细分析。

### 2. 测试用例生成

在优化代码的同时，自动生成对应的单元测试，确保重构没有破坏原有逻辑。

### 3. 技术债务量化

评估当前技术债务（以小时为单位），并给出债务构成和建议优先级。

**详细说明**: 见 [references/advanced-features.md](references/advanced-features.md)

---

## 注意事项

### ⚠️ 避免过度优化

- **不要过早优化**: 如果代码简单且高效，不要强行引入复杂的模式
- **考虑 ROI**: 优化带来的收益应该大于投入的成本
- **保持简单**: 简单的代码优于复杂的"优化"代码

### ✅ 最佳实践

- **测试先行**: 重构前确保有充足的测试覆盖
- **小步迭代**: 每次只重构一小部分，确保可回滚
- **代码审查**: 重要重构应该经过团队审查
- **性能基准**: 优化前后都应该有性能数据支撑

### 📊 量化指标

建议跟踪的优化效果指标：

| 指标 | 工具 | 目标值 |
|------|------|--------|
| 圈复杂度 | eslint-complexity | < 15 |
| 重复率 | sonarqube | < 5% |
| 测试覆盖 | coverage.py | > 80% |
| 技术债务 | sonarqube | < 5 天 |
| 安全漏洞 | bandit/snyk | 0 |

---

## 资源索引

- **架构设计**: [references/architecture.md](references/architecture.md) - 三层分析漏斗详细架构
- **检测清单**: [references/checklist.md](references/checklist.md) - 完整的检测维度清单
- **Prompt 策略**: [references/prompt-strategy.md](references/prompt-strategy.md) - 角色设定和思维链工作流
- **报告模板**: [references/report-template.md](references/report-template.md) - 标准报告格式和示例
- **使用示例**: [references/examples.md](references/examples.md) - 多场景完整示例
- **技术栈推荐**: [references/tech-stack.md](references/tech-stack.md) - 各技术栈工具链推荐
- **进阶功能**: [references/advanced-features.md](references/advanced-features.md) - 交互式重构、测试生成等

---

## 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v1.0.0 | 2026-04-11 | 初始版本，实现三层分析漏斗架构 |

---

## 参考资源

- **代码整洁之道** - Robert C. Martin
- **重构：改善既有代码的设计** - Martin Fowler
- **设计模式：可复用面向对象软件的基础** - Gang of Four
- **Clean Architecture** - Robert C. Martin
- **SonarQube 规则文档**: https://rules.sonarsource.com/
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
