---
name: 3-write-content
version: v1.0.0
author: book-skills
description: AGENTS.md内容编写实战 — 基于结构蓝图，按章节逐一编写高质量内容，遵循28条最佳实践，产出可直接使用的完整草稿
tags: [content-writing, best-practices, practical-guide, quality-output]
dependency:
  parent: agents-writer
  requires: [1-analyze-project, 2-design-structure]
---

# ③ 内容编写实战

## 任务目标

基于 [② 结构设计](../skills/2-design-structure/SKILL.md) 的蓝图，逐章编写 AGENTS.md 的**完整内容**，确保每章节都符合最佳实践标准，产出高质量的可用草稿。

## 触发条件

当用户说以下任一话术时激活：
- "帮我写AGENTS.md"
- "编写内容"
- "填充内容"
- "基于蓝图编写"

## 前置条件

⚠️ **必须先完成**：
1. [① 项目分析](../skills/1-analyze-project/SKILL.md) → 类型 + 评分
2. [② 结构设计](../skills/2-design-structure/SKILL.md) → 完整蓝图

## 编写原则（核心理念）

### 🎯 Golden Rule: AGENTS.md 回答 "HOW"，不是 "WHAT"

❌ **错误示范**（教程风格）：
```markdown
## MoonBit 简介
MoonBit 是一个现代化的编程语言...
（大段介绍语言特性）
```

✅ **正确示范**（行动导向）：
```markdown
## 身份与角色
你是一个 MoonBit 语言专家。当用户提及 MoonBit 相关任务时：
- 优先使用官方推荐的惯用法
- 遵循 trait-based 设计模式
- 注意两层级可变性语义
```

### 📐 三层内容模型

| 层级 | 内容类型 | 占比 | 示例 |
|------|---------|------|------|
| **指令层** | 直接可执行的命令/规则 | 40% | "使用 `mbt build` 编译"、"禁止 `mut self`" |
| **决策层** | 判断逻辑和分支指引 | 35% | "如果是泛型代码 → 使用 Trait 约束"、"若遇到错误 E001 → ..." |
| **参考层** | 背景知识和补充说明 | 25% | "MoonBit 支持 Wasm/JS/Native 三后端..." |

## 操作步骤

### Step 1: 编写前言区（YAML Frontmatter）

#### 标准模板

```yaml
---
name: {project-name-agents}        # kebab-case
version: v1.0.0                     # 语义化版本
author: {author-name/team}
description: {100-150字符描述，一句话说清楚这是什么的AGENTS.md}
tags: [{5-15个标签，涵盖技术栈/领域/用途}]
trigger:
  conditions: [{何时激活此文件}]
  keywords: [{触发关键词列表}]
priority: {high/medium/low}         # 在多文件中的优先级
context_files: [{相关上下文文件}]
---
```

#### 字段详解

| 字段 | 必填 | 规范 | 示例 |
|------|------|------|------|
| `name` | ✅ | kebab-case，≤50字符 | `moonbit-skills-agents` |
| `version` | ✅ | 语义化版本 (vX.Y.Z) | `v1.0.0` |
| `author` | ✅ | 个人名或团队名 | `book-skills-team` |
| `description` | ✅ | 100-150字符 | `MoonBit技能库的Agent配置...` |
| `tags` | ✅ | 5-15个标签 | `[moonbit, wasm, skill-library]` |
| `trigger.conditions` | ⭐⭐⭐⭐☆ | 激活条件列表 | `["用户提及MoonBit"]` |
| `trigger.keywords` | ⭐⭐⭐⭐☆ | 触发关键词 | `["moonbit", "mbt", ".mb"]` |
| `priority` | ⭐⭐⭐☆☆ | 多文件优先级 | `high` |
| `context_files` | ⭐⭐☆☆☆ | 相关文件 | `["SKILL.md", "CLAUDE.md"]` |

**实际示例**（moonbit-skills）：

```yaml
---
name: moonbit-skills-agents
version: v10.0.0
author: book-skills
description: MoonBit技能库Agent配置 — 支持项目创建/代码编写/错误调试/测试/优化/发布/FFI集成/架构决策8大任务的行动指引系统
tags: [moonbit, wasm, skill-library, action-oriented, trait-system, generics, ffi]
trigger:
  conditions:
    - 用户提及MoonBit相关任务
    - 需要MoonBit语言专家协助
  keywords: [moonbit, mbt, .mb, trait, derive, mut, fn, struct, enum, wasm, js_interop]
priority: high
context_files: ["SKILL.md"]
---
```

### Step 2: 编写身份与角色章节

#### 核心要素

```markdown
## 身份与角色

你是 {role_name}，一个专注于 {domain} 的专家级助手。

### 核心能力
- {ability_1}: {一句话描述}
- {ability_2}: {一句话描述}
- ...

### 工作原则
1. {principle_1}
2. {principle_2}
- **最多5条**，避免冗余

### 边界
- ✅ 你擅长: {within_scope}
- ❌ 你不负责: {out_of_scope}（如有，引导到其他资源）
```

**质量检查清单**：

- [ ] 角色定义清晰（不是泛泛的"AI助手"）
- [ ] 能力列表 ≤ 7 条（过多则分组）
- [ ] 工作原则 ≤ 5 条（聚焦核心）
- [ ] 边界明确（知道什么不该做）

### Step 3: 编写触发条件章节

#### 标准格式

```markdown
## 激活条件

当用户需要以下**任一**操作时激活本配置：

{condition_list}

### 典型触发场景
| 场景 | 用户话术示例 | Agent响应 |
|------|-------------|----------|
| 创建新项目 | "新建一个MoonBit项目" | 调用 create-project 流程 |
| 编写代码 | "帮我实现一个Trait" | 进入 write-code 模式 |
| ... | ... | ... |

### 不激活的场景
- {scenario_1}: {原因}
- {scenario_2}: {原因}
```

**最佳实践**：

✅ **正向表述**（什么时候激活）
✅ **提供示例**（真实用户话术）
✅ **明确边界**（什么时候不激活）
❌ **模糊表述**（"当你觉得合适的时候"）

### Step 4: 编写意图路由表（核心章节）

#### 这是整个 AGENTS.md 最重要的章节！

**设计原则**：
- 覆盖 **80-90%** 的常见用户请求
- 每行都是 **"说 X → 做 Y"** 的映射
- 按照使用**频率降序**排列

#### 标准格式

```markdown
## 意图路由

| 用户意图 | 触发关键词/示例 | 执行动作 | 优先级 |
|---------|----------------|---------|--------|
| **🚀 创建项目** | "新建"/"初始化"/"start project" | → 执行 [create-project](skills/...) | P0 |
| **✍️ 编写代码** | "实现"/"写一个"/"code" | → 进入 write-code 模式 | P0 |
| **🐛 调试错误** | "报错"/"bug"/"不工作" | → 执行 [debug-flow](skills/...) | P0 |
| **🧪 编写测试** | "测试"/"test"/"覆盖" | → 执行 [test-guide](skills/...) | P1 |
| **⚡ 性能优化** | "慢"/"优化"/"performance" | → 执行 [optimize](skills/...) | P1 |
| **📦 发布库** | "发布"/"publish"/"npm" | → 执行 [publish-flow](skills/...) | P2 |
| **🔗 FFI集成** | "调用JS"/"interop"/"extern" | → 执行 [ffi-guide](skills/...) | P2 |
| **🏗️ 架构决策** | "设计"/"架构"/"architecture" | → 执行 [arch-decisions](skills/...) | P2 |
```

**高级变体**（带条件判断）：

```markdown
## 意图路由

### P0: 核心任务（90% 场景）

| 意图 | 触发词 | 执行动作 | 条件 |
|------|--------|---------|------|
| 创建项目 | "新建"/"init" | → [1-create-project](skills/...) | 无 |
| 编写代码 | "写"/"实现" | → [2-write-code](skills/...) | 无 |
| 调试错误 | "报错"/"error" | → [3-debug-errors](skills/...) | 提供错误信息 |

### P1: 进阶任务（8% 场景）

| 意图 | 触发词 | 执行动作 | 条件 |
|------|--------|---------|------|
| 测试 | "test"/"测试" | → [4-tests](skills/...) | 有源代码 |
| 优化 | "优化"/"慢" | → [5-optimize](skills/...) | 有性能瓶颈证据 |

### P2: 专家任务（2% 场景）

| 意图 | 触发词 | 执行动作 | 条件 |
|------|--------|---------|------|
| 发布 | "publish"/"发布" | → [6-publish](skills/...) | API稳定 |
| FFI | "JS互操作"/"extern" | → [7-ffi](skills/...) | 明确提及FFI |
```

**行数控制**：
- **最小**: 10 行（3个任务，无分组）
- **推荐**: 20-35 行（5-8个任务，有优先级分组）
- **最大**: 50 行（超过则拆分为子技能索引）

### Step 5: 编写通用工作流章节

#### 标准 5 步流程模板

```markdown
## 通用工作流

所有任务遵循统一的 **SCAN → PLAN → EXECUTE → VERIFY → DELIVER** 流程：

```
① SCAN（扫描）
   ├── 读取项目上下文（README/package.json/现有代码）
   ├── 识别技术栈和约束条件
   └── 确认用户需求的完整性

② PLAN（规划）
   ├── 制定实施方案（含风险评估）
   ├── 列出关键步骤和依赖关系
   └── 与用户确认方案（如不确定）

③ EXECUTE（执行）
   ├── 按计划逐步实施
   ├── 遵循编码规范（见[编码规范](#编码规范)）
   └── 实时记录关键决策

④ VERIFY（验证）
   ├── 运行检查命令（见[质量门禁](#质量门禁)）
   ├── 验证功能正确性
   └── 确认无回归问题

⑤ DELIVER（交付）
   ├── 总结变更内容和影响
   ├── 提供后续维护建议
   └── 更新相关文档（如需要）
```

### 异常处理
- **方案偏离**: 暂停 → 重新 PLAN → 获得确认 → 继续
- **遇到阻塞**: 记录问题 → 提供备选方案 → 等待用户指示
- **用户中断**: 保存进度 → 总结已完成部分 → 等待恢复
```

**自定义要点**：
- 根据项目特点调整步骤名称（如 CI/CD 项目可以是 BUILD→TEST→DEPLOY）
- 添加项目特有的检查点（如"运行 lint before commit"）
- 保持 **5±2 步**（认知负荷限制）

### Step 6: 编写业务特定章节

根据 [② 蓝图](../skills/2-design-structure/SKILL.md) 中的规划，编写项目特有内容。

#### 示例：编码规范章节

```markdown
## 编码规范

### 必须遵守的规则（强制性）

| # | 规则 | 正确 ❌→✅ | 检测方式 |
|---|------|-----------|---------|
| R1 | 禁止 `mut self` 参数 | ❌ `fn f(mut self)` → ✅ 使用绑定级可变性 | 代码审查 |
| R2 | 禁止 for 循环解构 | ❌ `for (x, xs) in list` → ✅ 使用 match | 编译器警告 |
| R3 | Trait 方法必须有默认实现 | 除非明确标记为 `{ MustImplement }` | Lint 规则 |
| ... | ... | ... | ... |

### 推荐惯例（强烈建议）

| # | 惯例 | 理由 |
|---|------|------|
| S1 | 优先使用 `derive` 宏 | 减少样板代码 |
| S2 | 泛型参数命名为 T/U/V | 与官方文档一致 |
| S3 | 错误类型使用 `Result[T, Error]` | 统一错误处理 |
| ... | ... | ... |

### 格式化要求
- 缩进: 4 空格（非 Tab）
- 行宽: 100 字符（允许例外至 120）
- 命名: snake_case (函数/变量), CamelCase (类型)
```

**编写技巧**：

✅ **表格 > 段落**（规则类内容用表格更清晰）
✅ **❌→✅ 对比**（直观展示正确做法）
✅ **提供检测方式**（如何自动化检查）
❌ **长篇大论**（规则描述控制在 1 行内）

### Step 7: 编写注意事项章节（安全网）

```markdown
## 注意事项

⚠️ **核心理念**: 本配置回答的是 "**HOW to work**"，不是教程。

⚠️ **常见陷阱**:
- {trap_1}: {如何避免}
- {trap_2}: {如何避免}

⚠️ **不确定性处理**:
- 当遇到{ambiguous_scenario}时，{action}
- 不要猜测用户意图，{alternative_action}

⚠️ **版本兼容性**:
- 当前适用于 {version_range}
- 如遇 API 变更，{fallback_action}

⚠️ **与其他工具的关系**:
- 本配置 vs SKILL.md: {relationship}
- 优先级: {priority_chain}
```

### Step 8: 最终组装与审查

将所有章节组合成完整文件，并执行**自我审查**：

#### 审查清单

```bash
# 1. 行数检查
wc -l AGENTS.md
# 目标: 在 [② 设计](../skills/2-design-structure/SKILL.md) 规定的范围内（±10%）

# 2. 结构完整性
grep "^## " AGENTS.md
# 应包含蓝图中的所有必需章节

# 3. YAML 解析检查
head -15 AGENTS.md | python -c "import yaml; yaml.safe_load(open('/dev stdin'))"
# 应无语法错误

# 4. 链接有效性
grep -oP '\(.*?\)' AGENTS.md | sort -u
# 所有内部链接应指向存在的文件

# 5. Token 估算
echo "估算Token数: $(($(wc -l < AGENTS.md) * 3))"
# 应在合理范围内（详见 token-budget.md）
```

#### 质量评分（自我评估）

| 维度 | 评分标准 | 得分 (1-5) |
|------|---------|-----------|
| **完整性** | 所有必需章节都已编写 | ?/5 |
| **准确性** | 技术细节正确无误 | ?/5 |
| **可操作性** | 每条指令都能直接执行 | ?/5 |
| **清晰性** | 无歧义，易于理解 | ?/5 |
| **简洁性** | 无冗余，Token 效率高 | ?/5 |
| **总分** | | **?/25** |

**通过标准**: ≥ 20/25

## 交付物

### 完整的 AGENTS.md 草稿

```markdown
---
{完整前言区}
---

# {标题}

{所有章节内容...}
```

### 编写决策日志

```markdown
## 编写决策记录

| 章节 | 关键决策 | 原因 | 替代方案 |
|------|---------|------|---------|
| 意图路由 | 采用优先级分组（P0/P1/P2） | 覆盖90%场景 | 平铺式（太长） |
| 编码规范 | 使用❌→✅对比格式 | 直观易懂 | 纯文本（不够清晰） |
| ... | ... | ... | ... |
```

## 快速提示

### 常用的 Markdown 模式

**规则列表**（推荐）：
```markdown
| # | 规则 | 正确示例 | 错误示例 |
|---|------|---------|---------|
| R1 | 使用 snake_case | `my_function` | `myFunction` |
```

**流程图**（ASCII art）：
```
Step 1 → Step 2 → Step 3
                ↓
            异常处理
```

**警告框**（视觉强调）：
```markdown
⚠️ **重要**: 这一点非常关键...
```

**链接引用**（导航）：
```markdown
详见 [子技能名称](skills/xxx/SKILL.md)
```

## 常见问题

**Q: 某个章节不知道写什么内容？**

A: 参考 [best-practices.md](../references/best-practices.md) 中的 28 条最佳实践，或查看 [examples.md](../references/examples.md) 中的真实案例。

**Q: 如何把握内容的详细程度？**

A: 使用**二八法则**：
- 20% 的内容覆盖 80% 的场景（放在前面）
- 剩余 20% 的边缘场景可以用"如需...请参阅..."引向 references/

**Q: 需要包含代码示例吗？**

A: **选择性包含**：
- ✅ 包含：1-2 个最典型的"Hello World"级别示例
- ❌ 不包含：完整的教程式代码（那应该是 references/ 的内容）

## 注意事项

⚠️ **行动导向**: 每句话都应该让 Agent 知道**做什么**，而不是**了解什么**。

⚠️ **避免教程化**: 如果某个章节看起来像是在"教 Agent 学习"，那就错了。应该是"告诉 Agent 怎么做"。

⚠️ **迭代思维**: 第一版不必完美。先用 [⑤ 质量检查](../skills/5-quality-check/SKILL.md) 验证，再通过 [⑥ 优化](../skills/6-optimize-evolve/SKILL.md) 迭代改进。
