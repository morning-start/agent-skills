---
name: 4-select-template
version: v1.0.0
author: book-skills
description: AGENTS.md模板选择与定制 — 提供3种规格的生产级模板（最小可行/标准/完整），支持快速启动和按需定制，降低从零开始的门槛
tags: [template, quick-start, customization, boilerplate]
dependency:
  parent: agents-writer
---

# ④ 模板选择与定制

## 任务目标

为用户提供**开箱即用**的 AGENTS.md 模板，支持 3 种规格（最小/标准/完整），用户可以基于模板快速启动，再根据项目需求定制。

## 触发条件

当用户说以下任一话术时激活：
- "给我一个模板"
- "快速开始"
- "从模板开始"
- "有没有现成的"

## 模板规格选择决策树

```
需要什么级别的模板？
    │
    ├── 🚀 最快上手 → 最小可行版（30-80行）
    │   适用：个人项目、实验性代码、工具脚本
    │   特点：5分钟内可完成，覆盖核心功能
    │
    ├── ⚖️ 平衡之选 → 标准版（80-200行）
    │   适用：小型库、独立应用、2-5人团队
    │   特点：结构完整，内容适中，最常用
    │
    └── 🔬 完整专业 → 完整版（200-400行）
        适用：中型框架、开源项目、多模块系统
        特点：涵盖所有最佳实践，企业级质量
```

## 模板一：最小可行版（Type A）

**适用场景**: 个人工具、脚本、实验性项目  
**预估行数**: 30-80 行  
**创建时间**: 5-10 分钟

```yaml
---
name: {project-name}-agents
version: v1.0.0
author: {your-name}
description: {project} 的 AGENTS.md — {一句话描述}
tags: [{tag1}, {tag2}, {tag3}]
---

# {Project Name} Agent 配置

## 身份与角色

你是 {role} 专家，专注于 {domain}。

### 核心能力
- {ability_1}
- {ability_2}
- {ability_3}

## 触发条件

当用户提及 {keyword1}/{keyword2}/{keyword3} 相关任务时激活。

## 工作流

```
① 理解需求 → ② 制定方案 → ③ 执行实施 → ④ 验证结果 → ⑤ 交付总结
```

## 核心规则

| # | 规则 | 说明 |
|---|------|------|
| R1 | {rule_1} | {detail} |
| R2 | {rule_2} | {detail} |
| R3 | {rule_3} | {detail} |

## 常用命令

```bash
# 构建
{build_command}

# 测试
{test_command}

# 运行
{run_command}
```

## 注意事项

⚠️ **重点**: {most_important_thing}

⚠️ **避免**: {common_pitfall}

⚠️ **不确定时**: {what_to_do_when_unsure}
```

**定制要点**：
- 填写所有 `{placeholder}` 字段
- 核心规则控制在 **3-5 条**
- 常用命令只保留**最常用的 3-5 个**

---

## 模板二：标准版（Type B/C）

**适用场景**: 小型库、独立应用、2-8人团队、开源项目  
**预估行数**: 80-200 行  
**创建时间**: 15-30 分钟

```yaml
---
name: {project-name}-agents
version: v1.0.0
author: {author/team}
description: {100-150字符描述，说明这是什么项目的AGENTS.md配置}
tags: [{5-10个标签}]
trigger:
  conditions:
    - 用户提及{domain}相关任务
    - 需要{specific_capability}协助
  keywords: [{keyword1}, {keyword2}, {keyword3}]
priority: high
context_files: ["README.md", "CONTRIBUTING.md"]
---

# {Project Name} Agent 配置

## 身份与角色

你是 {role_name}，一个专注于 {domain} 的专家级助手。

### 核心能力
- {capability_1}: {one-line description}
- {capability_2}: {one-line description}
- {capability_3}: {one-line description}
- {capability_4}: {one-line description}

### 工作原则
1. {principle_1}
2. {principle_2}
3. {principle_3}

### 边界
- ✅ 你擅长: {within_scope}
- ❌ 你不负责: {out_of_scope}（请引导到 appropriate resource）

## 激活条件

当用户需要以下**任一**操作时激活本配置：

- {scenario_1_with_example}
- {scenario_2_with_example}
- {scenario_3_with_example}

**不激活的场景**: {when_not_to_activate}

## 意图路由

| 用户意图 | 触发示例 | 执行动作 | 优先级 |
|---------|---------|---------|--------|
| **🚀 {task_1}** | "{example}" | → {action_description} | P0 |
| **✍️ {task_2}** | "{example}" | → {action_description} | P0 |
| **🐛 {task_3}** | "{example}" | → {action_description} | P0 |
| **🧪 {task_4}** | "{example}" | → {action_description} | P1 |
| **⚡ {task_5}** | "{example}" | → {action_description} | P1 |

## 通用工作流

所有任务遵循 **SCAN → PLAN → EXECUTE → VERIFY → DELIVER** 流程：

```
① SCAN（扫描）
   - 读取项目上下文
   - 识别技术栈和约束

② PLAN（规划）
   - 制定实施方案
   - 列出关键步骤

③ EXECUTE（执行）
   - 按计划逐步实施
   - 遵循编码规范

④ VERIFY（验证）
   - 运行检查命令
   - 验证正确性

⑤ DELIVER（交付）
   - 总结变更
   - 提供维护建议
```

### 异常处理
- **方案偏离**: 暂停 → 重新规划 → 确认后继续
- **遇到阻塞**: 记录问题 → 提供备选方案
- **用户中断**: 保存进度 → 总结已完成部分

## 编码规范

### 必须遵守的规则

| # | 规则 | ✅ 正确做法 | ❌ 错误做法 | 检测方式 |
|---|------|------------|------------|---------|
| R1 | {rule_name} | {correct} | {incorrect} | {how_to_check} |
| R2 | {rule_name} | {correct} | {incorrect} | {how_to_check} |
| R3 | {rule_name} | {correct} | {incorrect} | {how_to_check} |

### 推荐惯例

| # | 惯例 | 理由 |
|---|------|------|
| S1 | {convention} | {reason} |
| S2 | {convention} | {reason} |

### 格式化要求
- 缩进: {indentation_spec}
- 行宽: {line_width}
- 命名规范: {naming_convention}

## 常用命令

### 构建与运行
```bash
{build_command}          # 构建项目
{run_command}            # 运行应用
{watch_command}          # 监听模式（如有）
```

### 测试
```bash
{test_command}           # 运行所有测试
{unit_test_command}      # 仅单元测试
{integration_test_command}  # 集成测试
{coverage_command}       # 覆盖率报告
```

### 代码质量
```bash
{lint_command}           # 代码检查
{format_command}         # 格式化
{typecheck_command}      # 类型检查
```

### 包管理
```bash
{add_dependency_command}     # 添加依赖
{update_dependency_command}  # 更新依赖
{publish_command}            # 发布版本
```

## 错误处理指南

### 常见错误及解决方案

| 错误信息/代码 | 可能原因 | 解决方案 |
|---------------|---------|---------|
| {error_pattern_1} | {cause_1} | {solution_1} |
| {error_pattern_2} | {cause_2} | {solution_2} |
| {error_pattern_3} | {cause_3} | {solution_3} |

### 调试流程
1. {debug_step_1}
2. {debug_step_2}
3. {debug_step_3}

## 项目架构概览（可选）

```
{ASCII architecture diagram or brief description}
```

**核心模块**:
- `{module_1}`: {description}
- `{module_2}`: {description}
- `{module_3}`: {description}

## 质量门禁

### 必须通过的检查
- [ ] {check_1}
- [ ] {check_2}
- [ ] {check_3}

### 推荐执行命令
```bash
{quality_gate_command_1}
{quality_gate_command_2}
```

## 注意事项

⚠️ **核心理念**: 本配置回答的是 "**HOW to work**"，不是教程。

⚠️ **常见陷阱**:
- {trap_1}: {how_to_avoid}
- {trap_2}: {how_to_avoid}

⚠️ **不确定性处理**:
- 当遇到 {ambiguous_scenario} 时: {action}
- 不要猜测用户意图: {alternative}

⚠️ **版本兼容性**:
- 当前适用于: {version_range}
- API 变更时的回退策略: {fallback}

⚠️ **与其他文件的关系**:
- vs README.md: {relationship}
- vs CONTRIBUTING.md: {relationship}
- 优先级: AGENTS.md > CLAUDE.md > .cursorrules

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0.0 | {date} | 初始版本 |
```

**定制要点**：
- 意图路由表至少包含 **5 个常见任务**
- 编码规范的规则数量根据项目实际情况调整（3-8条）
- 常用命令按**使用频率**排序

---

## 模板三：完整专业版（Type D/E）

**适用场景**: 中大型框架、企业级系统、高合规要求项目  
**预估行数**: 200-400 行  
**创建时间**: 30-60 分钟

> 💡 **提示**: 完整版模板内容较长，详见 [templates.md](../references/templates.md) 中的完整版本。

**核心增强点**（相比标准版）：

| 增强项 | 内容 | 行数增量 |
|--------|------|---------|
| **多层意图路由** | P0/P1/P2 三级分组 + 条件判断 | +20-30 行 |
| **领域知识摘要** | 核心概念/术语表/关系图 | +25-35 行 |
| **详细工作流** | 含分支逻辑和异常处理策略 | +15-20 行 |
| **安全与合规** | 审计要求/权限模型/数据保护 | +15-20 行 |
| **CI/CD 集成** | 流水线配置/自动化检查 | +15-20 行 |
| **性能基准** | SLA 定义/优化建议/监控指标 | +10-15 行 |
| **团队协作规范** | Code Review 标准/分支策略/发布流程 | +15-20 行 |

## 快速定制流程

### 从模板到定制的 5 步

```
① 选择模板规格（最小/标准/完整）
    ↓
② 替换占位符（{project-name} 等）
    ↓
③ 删除不适用的章节（如项目无 FFI 则删除 FFI 章节）
    ↓
④ 补充项目特有内容（技术栈细节/业务规则）
    ↓
⑤ 执行 [⑤ 质量检查](../skills/5-quality-check/SKILL.md) 验证
```

### 定制检查清单

- [ ] 所有 `{placeholder}` 已替换为实际值
- [ ] 删除了不适用的章节（标记为"可选"且不需要的）
- [ ] 补充了 ≥ 3 个项目特有的编码规则
- [ ] 常用命令已验证可在项目中实际执行
- [ ] 意图路由表覆盖了项目的 **TOP 5** 高频任务
- [ ] 错误处理包含了项目的 **TOP 3** 常见错误
- [ ] 行数在目标范围内（±10%）

## 常见问题

**Q: 应该选哪个模板？**

A: 使用以下快速判定：
- **个人项目 + < 50 文件** → 最小可行版
- **小团队 + 有一定复杂度** → 标准版（**最常用**）
- **框架/库/开源项目** → 完整专业版

**Q: 可以混合使用吗？**

A: **可以**！推荐方式：
- 从**标准版**开始作为基础
- 选择性地从**完整版**中复制需要的章节
- 删除不需要的部分保持简洁

**Q: 模板中的示例代码需要保留吗？**

A: **选择性保留**：
- ✅ 保留：通用模式（如 5 步工作流、意图路由表格式）
- ❌ 删除：特定技术的示例（替换为你自己的）
- ⚠️ 修改：半通用的示例（调整参数和命名）

## 注意事项

⚠️ **模板是起点不是终点**: 定制程度应 ≥ 30%（至少修改 30% 的内容），否则过于通用会降低效果。

⚠️ **先填关键信息**: 优先填写前言区、身份、意图路由这 3 个核心章节，其他可以后续迭代。

⚠️ **保持更新**: 当项目发生重大变化（新框架、新架构、新团队成员）时，及时更新 AGENTS.md。
