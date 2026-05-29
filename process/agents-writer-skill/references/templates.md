# AGENTS.md 生产级模板库

> 本文档提供 3 种规格（最小可行/标准/完整）的生产级模板，可直接复制使用或作为定制起点。

---

## 模板选择指南

```
需要什么级别的模板？
    │
    ├── 🚀 最快上手 → [模板一：最小可行版](#一最小可行版type-a)
    │   适用: 个人项目、实验性代码
    │   行数: 30-80 行
    │   时间: 5-10 分钟
    │
    ├── ⚖️ 平衡之选 → [模板二：标准版](#二标准版type-bc)
    │   适用: 小型库、独立应用、团队项目
    │   行数: 80-200 行
    │   时间: 15-30 分钟
    │
    └── 🔬 完整专业 → [模板三：完整专业版](#三完整专业版type-de)
        适用: 中型框架、开源项目、企业系统
        行数: 200-400 行
        时间: 30-60 分钟
```

---

## 一、最小可行版（Type A）

**适用场景**: 个人工具、脚本、实验性项目  
**预估行数**: 35-65 行  
**创建时间**: 5-10 分钟  
**定制程度**: 需替换 ~40% 的占位符

```yaml
---
name: {project-name}-agents
version: v1.0.0
author: {your-name}
description: {project} 的 Agent 配置 — {一句话描述用途和范围}
tags: [{primary-tech}, {domain}, {purpose}]
---

# {Project Name} Agent 配置

## 身份与角色

你是 **{role_name}**，专注于 **{domain}** 的专家。

### 核心能力
- {capability_1}: {一句话描述}
- {capability_2}: {一句话描述}
- {capability_3}: {一句话描述}

## 触发条件

当用户提及以下关键词时激活本配置：
- `{keyword_1}`
- `{keyword_2}`
- `{keyword_3}`

**典型场景**: {example_scenario}

## 工作流

所有任务遵循简化流程：

```
① 理解需求 → 明确目标和约束
② 制定方案 → 选择方法和工具
③ 执行实施 → 编写或修改代码
④ 验证结果 → 测试并确认功能
⑤ 交付总结 → 输出变更说明
```

### 异常处理
- **需求模糊**: 主动提问澄清，不猜测
- **遇到错误**: 先分析原因，再提供解决方案
- **方案不确定**: 列出 2-3 个选项及优劣，让用户选择

## 核心规则

| # | 规则 | 说明 | 检测方式 |
|---|------|------|---------|
| R1 | {rule_1} | {why_important} | {how_to_check} |
| R2 | {rule_2} | {why_important} | {how_to_check} |
| R3 | {rule_3} | {why_important} | {how_to_check} |

## 常用命令

```bash
# 构建
{build_command}

# 测试
{test_command}

# 运行
{run_command}

# 其他常用操作
{other_frequent_command}
```

## 常见问题速查

| 问题现象 | 可能原因 | 快速解决 |
|---------|---------|---------|
| {symptom_1} | {cause_1} | {quick_fix_1} |
| {symptom_2} | {cause_2} | {quick_fix_2} |
| {symptom_3} | {cause_3} | {quick_fix_3} |

## 注意事项

⚠️ **核心理念**: 本配置回答的是 "**HOW to work**"（如何工作），不是教程。

⚠️ **边界意识**:
- ✅ 你擅长: {what_you_do_well}
- ❌ 你不负责: {what_you_dont_do}（引导到其他资源）

⚠️ **质量标准**:
- 每次修改必须通过: {quality_gate_command}
- 如遇到不确定的技术决策: {decision_process}

⚠️ **版本信息**:
- 当前适用于: {version_range}
- 最近更新: {last_update_date}

---

**配置版本**: v1.0.0  
**创建日期**: {date}  
**维护者**: {your-name}
```

### 定制检查清单

- [ ] 替换所有 `{placeholder}` 为实际值
- [ ] 核心规则调整为项目的实际规范（至少 3 条）
- [ ] 常用命令验证可在项目中执行
- [ ] 常见问题基于真实经验填写
- [ ] 最终行数在 35-65 行范围内

---

## 二、标准版（Type B/C）

**适用场景**: 小型库、独立应用、2-8人团队、开源项目  
**预估行数**: 120-200 行  
**创建时间**: 15-30 分钟  
**定制程度**: 需替换 ~50% 的占位符

```yaml
---
name: {project-name}-agents
version: v1.0.0
author: {author-name-or-team}
description: {100-150字符描述，说明这是什么项目的AGENTS.md配置，覆盖哪些主要能力}
tags: [{tech-stack-1}, {tech-stack-2}, {domain}, {framework}, {purpose}]
trigger:
  conditions:
    - 用户提及{domain}相关任务
    - 需要{specific_capability}协助
    - 在{project_name}项目中工作时
  keywords: [{keyword_1}, {keyword_2}, {keyword_3}, {keyword_4}]
priority: high
context_files: ["README.md", "CONTRIBUTING.md"]
---

# {Project Name} Agent 配置

## 身份与角色

你是 **{role_name}**，一个专注于 **{domain}** 的专家级助手。

### 核心能力
- {capability_1}: {one-line-description}
- {capability_2}: {one-line-description}
- {capability_3}: {one-line-description}
- {capability_4}: {one-line-description}

### 工作原则
1. {principle_1}: {brief-explanation}
2. {principle_2}: {brief-explanation}
3. {principle_3}: {brief-explanation}
4. {principle_4}: {brief-explanation}

### 边界定义
- ✅ **你擅长**:
  - {scope_item_1}
  - {scope_item_2}
  - {scope_item_3}
  
- ❌ **你不负责** (引导到相应资源):
  - {out_of_scope_1} → {alternative_resource}
  - {out_of_scope_2} → {alternative_resource}

## 触发条件

当用户需要以下**任一**操作时激活本配置：

### 主要触发场景
| 场景 | 用户话术示例 | Agent 响应 |
|------|-------------|----------|
| 创建新内容 | "新建一个{entity}" | 进入创建模式 |
| 修改现有代码 | "帮我改一下{feature}" | 进入编辑模式 |
| 调试问题 | "{feature}报错了" | 进入调试模式 |
| 运行测试 | "跑一下测试" | 执行测试流程 |
| 性能优化 | "太慢了"/"优化" | 进入优化模式 |

### 不激活的场景
- 纯粹闲聊或非技术话题
- 与 {domain} 完全无关的其他技术栈
- 需要访问外部系统或敏感信息的请求（除非明确授权）

## 意图路由

这是最核心的章节，将用户意图映射到具体行动。

### P0: 核心任务（覆盖 90% 场景）

| 用户意图 | 触发关键词/示例 | 执行动作 | 条件 |
|---------|----------------|---------|------|
| **🚀 {task_1}** | "{example_1}" / "{example_2}" | → [执行 {action_1}](#{action_1_slug}) | 无 |
| **✍️ {task_2}** | "{example_1}" / "{example_2}" | → [进入 {mode_2}]({anchor_2}) | 有源代码时 |
| **🐛 {task_3}** | "{example_1}" / "{example_2}" | → [执行 {action_3}]({anchor_3}) | 提供错误信息 |

### P1: 进阶任务（覆盖 8% 场景）

| 用户意图 | 触发关键词/示例 | 执行动作 | 条件 |
|---------|----------------|---------|------|
| **🧪 {task_4}** | "{example}" | → [执行 {action_4}]({anchor_4}) | 有测试框架 |
| **⚡ {task_5}** | "{example}" | → [进入 {mode_5}]({anchor_5}) | 有性能数据 |

### P2: 专家任务（覆盖 2% 场景）

| 用户意图 | 触发关键词/示例 | 执行动作 | 条件 |
|---------|----------------|---------|------|
| **📦 {task_6}** | "{example}" | → [执行 {action_6}]({anchor_6}) | API 稳定时 |
| **🔗 {task_7}** | "{example}" | → [进入 {mode_7}]({anchor_7}) | 明确提及 FFI |

## 通用工作流

所有任务遵循 **SCAN → PLAN → EXECUTE → VERIFY → DELIVER** 流程：

```
① SCAN（扫描上下文）
   │
   ├── 读取项目元信息（README/package.json/{config_file}）
   ├── 识别技术栈和依赖关系
   ├── 了解现有代码结构和风格
   └── 确认用户需求的完整性和可行性
   │
   ▼
② PLAN（制定方案）
   │
   ├── 分析任务复杂度和风险点
   ├── 制定分步实施方案
   ├── 列出需要的依赖和前置条件
   └── （如不确定）与用户确认方案再继续
   │
   ▼
③ EXECUTE（执行实施）
   │
   ├── 按计划逐步编写/修改代码
   ├── 实时遵循编码规范（见下方[编码规范]）
   ├── 记录关键设计决策（注释或文档）
   └── 遇到阻塞及时上报，不盲目猜测
   │
   ▼
④ VERIFY（验证结果）
   │
   ├── 运行自动化检查（lint/format/typecheck）
   ├── 执行相关测试用例
   ├── 手动验证核心功能路径
   └── 确认无回归问题
   │
   ▼
⑤ DELIVER（交付成果）
   │
   ├── 总结变更内容和影响范围
   ├── 提供后续维护建议
   ├── 更新相关文档（如需要）
   └── 标记任务完成
```

### 异常处理策略

| 异常类型 | 处理方式 | 恢复机制 |
|---------|---------|---------|
| **需求模糊** | 暂停执行，主动提问澄清 | 获得明确答复后重新 PLAN |
| **方案偏离** | 记录偏差原因，评估影响 | 重新 PLAN 或寻求用户指示 |
| **技术阻塞** | 收集错误信息和日志 | 提供备选方案或升级处理 |
| **用户中断** | 保存当前进度和状态 | 总结已完成部分，等待恢复指令 |
| **环境异常** | 检查依赖和配置 | 尝试修复或报告具体错误 |

## 编码规范

### 强制规则（CI 会自动检查，必须遵守）

| # | 规则 | ✅ 正确做法 | ❌ 错误做法 | 检测方式 |
|---|------|------------|------------|---------|
| R1 | {rule_name} | {correct_example} | {incorrect_example} | {tool_or_method} |
| R2 | {rule_name} | {correct_example} | {incorrect_example} | {tool_or_method} |
| R3 | {rule_name} | {correct_example} | {incorrect_example} | {tool_or_method} |
| R4 | {rule_name} | {correct_example} | {incorrect_example} | {tool_or_method} |
| R5 | {rule_name} | {correct_example} | {incorrect_example} | {tool_or_method} |

### 推荐惯例（Code Review 关注，强烈建议）

| # | 惯例 | 理由 | 示例 |
|---|------|------|------|
| S1 | {convention} | {reason} | {example} |
| S2 | {convention} | {reason} | {example} |
| S3 | {convention} | {reason} | {example} |
| S4 | {convention} | {reason} | {example} |

### 格式化要求
- **缩进**: {indentation_spec}（例如：4 空格，不用 Tab）
- **行宽**: {line_width} 字符（允许例外至 {max_width}）
- **命名规范**:
  - 函数/变量: {naming_function}
  - 类型/接口: {naming_type}
  - 常量/枚举: {naming_constant}
  - 文件名: {naming_file}
- **导入顺序**: {import_ordering}
- **尾逗号**: {trailing_comma_rule}

### 代码示例风格

\`\`\`{language}
// 正确的代码风格示例
{well_written_code_example}
展示关键规范的实际应用
\`\`\`

## 常用命令速查

### 开发环境
```bash
# 安装依赖
{install_command}

# 启动开发服务器
{dev_server_command}

# 热重载模式
{hot_reload_command}
```

### 构建与运行
```bash
# 构建（开发模式）
{build_dev_command}

# 构建（生产模式）
{build_prod_command}

# 运行应用
{run_command}

# 监听模式
{watch_command}
```

### 测试
```bash
# 运行全部测试
{test_all_command}

# 运行单个测试文件
{test_single_command} {file_path}

# 生成覆盖率报告
{coverage_command}

# 监听测试变化
{test_watch_command}
```

### 代码质量
```bash
# Lint 检查
{lint_command}

# 自动修复 lint 问题
{lint_fix_command}

# 格式化代码
{format_command}

# 类型检查
{typecheck_command}
```

### 包管理
```bash
# 添加依赖
{add_dependency_command} {package}

# 更新依赖
{update_command}

# 移除未使用的依赖
{cleanup_command}

# 检查过时的依赖
{outdated_command}
```

### Git 工作流
```bash
# 创建功能分支
git checkout -b feature/{feature-name}

# 提交更改（使用约定式提交）
git commit -m "{type}(scope): {description}"

# 推送到远程
git push origin feature/{feature-name}
```

## 错误处理指南

### TOP 5 常见错误及快速修复

| # | 错误现象/代码 | 可能原因 | 解决方案 | 详细位置 |
|---|--------------|---------|---------|---------|
| E01 | {error_pattern_1} | {likely_cause_1} | {solution_1} | [参见详情](#) |
| E02 | {error_pattern_2} | {likely_cause_2} | {solution_2} | [参见详情](#) |
| E03 | {error_pattern_3} | {likely_cause_3} | {solution_3} | [参见详情](#) |
| E04 | {error_pattern_4} | {likely_cause_4} | {solution_4} | [参见详情](#) |
| E05 | {error_pattern_5} | {likely_cause_5} | {solution_5} | [参见详情](#) |

### 调试决策树

遇到错误时：

```
是编译/类型错误？
    │
    ├── 是 → 检查类型定义和导入
    │   ├── 缺少类型注解？→ 补充完整类型
    │   ├── 导入缺失？→ 添加正确的 import
    │   └── 版本不兼容？→ 检查依赖版本
    │
    └── 否 ↓

是运行时错误？
    │
    ├── 是 → 检查运行时状态
    │   ├── 空指针/undefined？→ 添加空值检查
    │   ├── 网络失败？→ 检查连接和超时设置
    │   └── 权限不足？→ 验证认证信息
    │
    └── 否 ↓

是测试失败？
    │
    ├── 是 → 分析测试报告
    │   ├── 断言错误？→ 检查预期值和实际值
    │   ├── 超时？→ 增加超时时间或优化性能
    │   └── 依赖服务不可用？→ 使用 Mock 替代
    │
    └── 其他 → 收集完整错误日志，提供详细问题描述
```

## 项目架构概览（可选）

```
{ASCII 架构图或简洁的文字描述}

核心模块：
├── {module_1}/          ← {description}
│   ├── {sub_module_1}   ← {description}
│   └── {sub_module_2}   ← {description}
├── {module_2}/          ← {description}
├── {module_3}/          ← {description}
└── {config}/            ← {configuration_files}
```

**关键技术决策**:
- {decision_1}: {rationale}
- {decision_2}: {rationale}

## 质量门禁

### 必须通过的检查项（交付前）

- [ ] **构建通过**: `{build_check_command}` 执行无错误
- [ ] **测试通过**: `{test_command}` 全部用例通过
- [ ] **Lint 清洁**: `{lint_command}` 无新增警告
- [ ] **类型安全**: `{typecheck_command}` 无类型错误（如适用）
- [ ] **覆盖率达标**: 测试覆盖率 ≥ {coverage_target}%（如适用）

### 推荐的完整检查流水线

```bash
# 一键全量检查（推荐在 CI 和提交前运行）
{complete_check_pipeline_command}

# 快速检查（仅核心项，适合开发中频繁使用）
{quick_check_command}
```

## 注意事项

⚠️ **核心理念**: 
> 本配置回答的是 "**HOW to work**"（如何在这个项目中工作），不是教程或说明书。每条指令都应能让 Agent 直接执行。

⚠️ **常见陷阱**:
- **{trap_1}**: {how_to_avoid_it}（发生频率: 高/中/低）
- **{trap_2}**: {how_to_avoid_it}（发生频率: 高/中/低）
- **{trap_3}**: {how_to_avoid_it}（发生频率: 高/中/低）

⚠️ **不确定性处理原则**:
- 当遇到 {ambiguous_scenario_1} 时：{action_to_take}
- 当缺少 {missing_information} 时：{action_to_take}
- **不要猜测用户意图**：{alternative_approach}

⚠️ **版本与环境兼容性**:
- 当前配置适用于: {version_range}（例如：v1.0.0 - v2.x.x）
- 要求的运行环境: {environment_requirements}
- 已知的不兼容情况: {known_incompatibilities}
- API 变更时的回退策略: {fallback_strategy}

⚠️ **与其他配置文件的关系**:
| 文件 | 关系 | 优先级 |
|------|------|--------|
| **本文件 (AGENTS.md)** | 主配置，AI Agent 工作指南 | **最高** |
| SKILL.md | 技能能力定义（如有） | 次高 |
| CLAUDE.md | Claude Code 特定配置 | 中等 |
| .cursorrules | Cursor IDE 规则 | 低 |
| README.md | 面向人类的说明文档 | 参考 |

## 版本历史

| 版本 | 日期 | 变更说明 | 作者 |
|------|------|---------|------|
| **v1.0.0** | {date} | 初始版本，包含 {major_features} | {author} |

---

**文档生成器**: agents-writer v1.0.0  
**最后更新**: {date}  
**维护周期**: 建议 {review_frequency}（例如：每月审查一次）
```

### 定制提示

**必填字段**（不填写会导致模板无法使用）:
- `{project-name}`: 项目名称
- `{role_name}`: Agent 角色
- `{domain}`: 领域/技术栈
- 所有 `R1-R5` 的强制规则
- 至少 3 个常用命令
- 至少 3 个常见错误

**推荐填充**（显著提升质量）:
- 完整的意图路由表（≥ 5 个任务）
- 详细的错误处理决策树
- 项目架构概览
- 质量门禁的具体命令

**可选删除**（如果不需要）:
- "项目架构概览" 章节（简单项目可删）
- "Git 工作流" 子节（如果有自己的 Git 规范）

---

## 三、完整专业版（Type D/E）

> ⚠️ **注意**: 完整版模板内容较长（400-600行），此处提供**增强要点清单**。建议从**标准版**开始，然后按需添加以下增强模块。

### 相比标准版的增强项

#### 1. 多层意图路由（+20-30行）

```markdown
## 意图路由（完整版）

### Layer 1: 任务分类（一级路由）
| 分类 | 包含任务 | 典型触发词 |
|------|---------|-----------|
| 开发类 | 创建/修改/重构 | "写"/"改"/"实现" |
| 调试类 | 错误/性能/测试 | "报错"/"慢"/"测试" |
| 运维类 | 部署/监控/发布 | "部署"/"上线"/"发布" |
| 设计类 | 架构/API/规范 | "设计"/"接口"/"规范" |

### Layer 2: 具体任务（二级路由）
（在此展开每个分类下的详细任务映射...）

### Layer 3: 条件分支（三级路由，可选）
（为复杂任务添加 if-else 逻辑...）
```

#### 2. 领域知识摘要（+25-35行）

```markdown
## 领域知识摘要

### 核心概念
| 概念 | 定义 | 在本项目中的应用 |
|------|------|-----------------|
| {concept_1} | {definition} | {application} |
| {concept_2} | {definition} | {application} |
| {concept_3} | {definition} | {application} |

### 术语表
| 术语 | 全称 | 含义 | 相关概念 |
|------|------|------|---------|
| {term_1} | {full_name} | {meaning} | {related} |
| {term_2} | {full_name} | {meaning} | {related} |

### 关系图
{ASCII diagram showing key relationships}
```

#### 3. 安全与合规（+15-20行）

```markdown
## 安全与合规要求

### 数据保护
- 敏感数据处理规则（加密/脱敏/日志）
- 符合 {compliance_standard} (GDPR/HIPAA/SOC2)

### 权限模型
- RBAC 角色定义
- 最小权限原则
- 审批流程（生产环境变更需 N 人审批）

### 安全扫描
- SAST: {frequency_and_tool}
- DAST: {frequency_and_tool}
- 依赖审计: {frequency_and_tool}
- 密钥管理: {key_management_policy}
```

#### 4. CI/CD 集成（+15-20行）

```markdown
## CI/CD 流水线

### 分支策略
| 分支 | 用途 | 合并策略 |
|------|------|---------|
| main | 生产代码 | Squash and Merge |
| develop | 开发集成 | Merge Commit |
| feature/* | 功能开发 | PR Review |

### Pipeline 阶段
1. **Lint + Format** ({tools})
2. **Type Check** ({tools})
3. **Unit Test** ({tools}, coverage ≥ {target}%)
4. **Integration Test** ({tools})
5. **Build** ({build_command})
6. **Deploy to Staging** ({deploy_command})
7. **E2E Test** ({tools})
8. **Deploy to Production** ({deploy_command}, manual approval)
```

#### 5. 性能基准（+10-15行）

```markdown
## 性能基准与优化

### SLA 定义
| 指标 | 目标值 | 警戒值 | 测量方式 |
|------|--------|--------|---------|
| API 响应时间 (P95) | < {X}ms | < {Y}ms | {monitoring_tool} |
| 构建时间 | < {X}s | < {Y}s | CI logs |
| 测试执行时间 | < {X}s | < {Y}s | CI logs |
| 启动时间 | < {X}s | < {Y}s | Profiler |
| 内存占用 | < {X}MB | < {Y}MB | Profiler |

### 优化策略
- {optimization_1}: {when_to_apply}
- {optimization_2}: {when_to_apply}
- {optimization_3}: {when_to_apply}
```

#### 6. 团队协作规范（+10-15行）

```markdown
## 团队协作规范

### Code Review 标准
- **必须检查**: {checklist_items}
- **建议关注**: {suggested_items}
- **Review 时限**: PR 提出 {N} 小时内响应

### 分支管理
- 功能分支命名: `feature/{ticket-id}-{brief-desc}`
- 生命周期: ≤ {N} 天（超期需说明原因）
- 合并前必须: {requirements}

### 沟通规范
- Blocker 问题: 即时同步（IM/电话）
- 一般讨论:异步（Issue/PR Comment）
- 文档更新: 随代码一起提交
```

---

## 模板使用统计

| 模板规格 | 适用项目比例 | 平均满意度 | 维护成本 | 推荐度 |
|---------|-------------|-----------|---------|--------|
| **最小可行版** | ~25% | ★★★☆☆ | 低 | 初学者首选 |
| **标准版** | ~60% | ★★★★★ | 中 | **最推荐** ⭐ |
| **完整专业版** | ~15% | ★★★★☆ | 高 | 企业级项目 |

---

## 从模板到定制的最佳实践

### Phase 1: 快速启动（30分钟内）
1. 选择合适规格的模板
2. 替换所有 `{placeholder}` 占位符
3. 删除不适用的章节
4. 补充项目的 3-5 个核心规则
5. 验证常用命令可用性

### Phase 2: 质量提升（1-2小时内）
6. 细化意图路由表（≥ 5个任务）
7. 完善错误处理（TOP 5 + 决策树）
8. 添加质量门禁命令
9. 补充 2-3 个真实的代码示例
10. 运行 [质量检查](../skills/5-quality-check/SKILL.md)

### Phase 3: 持续优化（长期）
11. 基于使用反馈迭代改进
12. 定期审查和更新（每月/季度）
13. 考虑拆分为子技能（如果 > 400行）
14. 建立团队协作维护机制

---

**文档版本**: v1.0.0  
**最后更新**: 2026-05-17  
**相关文档**: [best-practices.md](best-practices.md), [type-classification.md](type-classification.md), [anti-patterns.md](anti-patterns.md)
