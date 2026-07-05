# Flutter Skills - 场景映射表

本文档定义用户意图、触发条件和执行路径的映射关系，帮助 AI 智能体快速响应不同场景。

## 场景分类决策树

```
用户请求
│
├─ 创建/初始化类
│  ├─ 新项目初始化 → packages-guide.md + architecture-guide.md
│  ├─ 生成功能模块 → scripts/generate_feature.py
│  ├─ 生成数据模型 → scripts/generate_model.py
│  ├─ 生成 BLoC → scripts/generate_bloc.py
│  └─ 生成测试 → scripts/generate_test.py
│
├─ 开发实现类
│  ├─ TDD 开发 → agents/tdd-coach.md
│  ├─ 架构设计 → architecture-guide.md + skills/architecture/
│  ├─ 状态管理 → architecture-guide.md + packages-guide.md
│  ├─ 网络请求 → packages-guide.md
│  └─ 数据存储 → packages-guide.md
│
├─ 测试类
│  ├─ 编写测试 → agents/test-writer.md
│  ├─ TDD 流程 → agents/tdd-coach.md
│  └─ 测试指南 → testing-guide.md
│
├─ 审查优化类
│  ├─ 代码审查 → agents/code-reviewer.md
│  ├─ 架构审查 → agents/architecture-reviewer.md
│  └─ 性能优化 → diagnostic/performance-profiler.md
│
└─ 故障排除类
   ├─ 构建错误 → diagnostic/build-errors.md
   ├─ 运行时错误 → diagnostic/runtime-errors.md
   ├─ 状态调试 → diagnostic/state-debugging.md
   └─ 性能问题 → diagnostic/performance-profiler.md
```

## 详细场景映射

### 1. 创建/初始化类

#### 场景 1.1：新项目初始化
**触发条件**：
- "创建新项目"
- "初始化 Flutter 项目"
- "搭建项目架构"

**执行路径**：
1. 读取 references/packages-guide.md，选择技术栈
2. 读取 references/architecture-guide.md，设计架构
3. 使用 scripts/generate_feature.py 生成初始结构
4. 配置依赖注入（references/skills/architecture/dependency-injection.md）

**推荐资源**：
- references/packages-guide.md（技术栈推荐）
- references/architecture-guide.md（架构规范）
- SKILL.md（标准流程）

---

#### 场景 1.2：生成功能模块
**触发条件**：
- "创建用户认证功能"
- "添加商品列表模块"
- "生成新的 feature"

**执行路径**：
1. 调用 scripts/generate_feature.py --feature-name <name>
2. 读取 references/skills/architecture/feature-structure.md
3. 生成数据模型：scripts/generate_model.py
4. 生成 BLoC：scripts/generate_bloc.py
5. 配置路由：references/packages-guide.md（路由章节）

**推荐资源**：
- scripts/generate_feature.py
- references/skills/architecture/feature-structure.md

---

#### 场景 1.3：生成数据模型
**触发条件**：
- "创建 User 模型"
- "生成 Freezed 模型"
- "定义数据结构"

**执行路径**：
1. 调用 scripts/generate_model.py --model-name <name> --fields <spec>
2. 读取 references/packages-guide.md（freezed 章节）
3. 运行 build_runner 生成代码

**推荐资源**：
- scripts/generate_model.py
- references/commands/generate-model.md

---

### 2. 开发实现类

#### 场景 2.1：TDD 开发
**触发条件**：
- "请帮我用 TDD 实现"
- "遵循 TDD 流程"
- "先写测试再写代码"

**执行路径**：
1. 触发 agents/tdd-coach.md（扮演 TDD Coach）
2. 按照 Red/Green/Refactor 循环开发
3. 使用 agents/test-writer.md 生成测试代码
4. 使用 agents/code-reviewer.md 审查代码

**推荐资源**：
- references/agents/tdd-coach.md
- references/testing-guide.md

---

#### 场景 2.2：架构设计
**触发条件**：
- "设计 Clean Architecture"
- "规划项目结构"
- "如何组织代码"

**执行路径**：
1. 读取 references/architecture-guide.md
2. 深入学习 references/skills/architecture/
3. 使用 agents/architecture-reviewer.md 审计设计

**推荐资源**：
- references/architecture-guide.md
- references/skills/architecture/clean-architecture.md
- references/skills/architecture/feature-structure.md

---

#### 场景 2.3：状态管理实现
**触发条件**：
- "实现 BLoC 状态管理"
- "管理应用状态"
- "设计状态转换"

**执行路径**：
1. 读取 references/skills/architecture/bloc-architecture.md
2. 调用 scripts/generate_bloc.py 生成结构
3. 读取 references/skills/testing/bloc-testing.md 编写测试

**推荐资源**：
- references/skills/architecture/bloc-architecture.md
- references/skills/testing/bloc-testing.md
- references/commands/generate-bloc.md

---

### 3. 测试类

#### 场景 3.1：编写测试
**触发条件**：
- "编写单元测试"
- "为这个函数写测试"
- "添加 Widget 测试"

**执行路径**：
1. 触发 agents/test-writer.md（扮演 Test Writer）
2. 读取 references/testing-guide.md 了解测试模式
3. 使用 scripts/generate_test.py 生成模板

**推荐资源**：
- references/agents/test-writer.md
- references/testing-guide.md
- references/skills/testing/

---

#### 场景 3.2：TDD 测试流程
**触发条件**：
- "先写测试"
- "Red-Green-Refactor"
- "测试驱动开发"

**执行路径**：
1. 触发 agents/tdd-coach.md
2. Phase 1：编写失败的测试（Red）
3. Phase 2：实现代码使测试通过（Green）
4. Phase 3：重构代码（Refactor）

**推荐资源**：
- references/agents/tdd-coach.md
- references/skills/testing/tdd-workflow.md

---

### 4. 审查优化类

#### 场景 4.1：代码审查
**触发条件**：
- "审查这段代码"
- "检查代码质量"
- "review my code"

**执行路径**：
1. 触发 agents/code-reviewer.md（扮演 Code Reviewer）
2. 按照审查清单逐项检查
3. 识别问题并提供修复建议

**推荐资源**：
- references/agents/code-reviewer.md

---

#### 场景 4.2：架构审查
**触发条件**：
- "审查项目架构"
- "检查架构合规性"
- "审计代码结构"

**执行路径**：
1. 触发 agents/architecture-reviewer.md（扮演 Architecture Reviewer）
2. 检查依赖规则
3. 验证层次分离
4. 评估架构质量

**推荐资源**：
- references/agents/architecture-reviewer.md
- references/skills/architecture/

---

#### 场景 4.3：性能优化
**触发条件**：
- "优化应用性能"
- "应用卡顿"
- "内存泄漏"

**执行路径**：
1. 读取 references/diagnostic/performance-profiler.md
2. 使用 DevTools 分析性能
3. 识别性能瓶颈
4. 应用优化策略

**推荐资源**：
- references/diagnostic/performance-profiler.md
- references/packages-guide.md（性能与调试章节）

---

### 5. 故障排除类

#### 场景 5.1：构建错误
**触发条件**：
- "构建失败"
- "编译错误"
- "build error"

**执行路径**：
1. 读取 references/diagnostic/build-errors.md
2. 识别错误类型（依赖、配置、版本冲突）
3. 应用对应修复方案

**推荐资源**：
- references/diagnostic/build-errors.md
- references/commands/clean-rebuild.md

---

#### 场景 5.2：运行时错误
**触发条件**：
- "应用崩溃"
- "空指针异常"
- "运行时错误"
- "runtime error"

**执行路径**：
1. 读取 references/diagnostic/runtime-errors.md
2. 分析错误堆栈
3. 定位问题根因
4. 应用修复方案

**推荐资源**：
- references/diagnostic/runtime-errors.md
- references/diagnostic/state-debugging.md

---

#### 场景 5.3：状态调试
**触发条件**：
- "状态不更新"
- "BLoC 不工作"
- "状态管理问题"

**执行路径**：
1. 读取 references/diagnostic/state-debugging.md
2. 使用 DevTools 调试状态
3. 检查事件流和状态转换
4. 修复状态逻辑

**推荐资源**：
- references/diagnostic/state-debugging.md
- references/skills/architecture/bloc-architecture.md

---

## 关键词映射表

| 用户关键词 | 推荐资源 | Agent |
|-----------|----------|-------|
| TDD、测试驱动 | testing-guide.md, tdd-coach.md | TDD Coach |
| 审查、review、检查 | code-reviewer.md, architecture-reviewer.md | Code Reviewer / Architecture Reviewer |
| 构建、编译、build | build-errors.md, commands-guide.md | - |
| 崩溃、错误、bug | runtime-errors.md, state-debugging.md | - |
| 性能、优化、卡顿 | performance-profiler.md | - |
| 架构、结构、组织 | architecture-guide.md, skills/architecture/ | Architecture Reviewer |
| BLoC、状态 | bloc-architecture.md, state-debugging.md | - |
| 生成、create、new | scripts/, commands/ | - |
| 模型、model、实体 | packages-guide.md, generate-model.py | - |
| 测试、test | testing-guide.md, test-writer.md | Test Writer |

## 执行优先级

### 高优先级（立即触发 Agent）
- TDD 开发 → TDD Coach
- 代码审查 → Code Reviewer
- 架构审查 → Architecture Reviewer
- 测试编写 → Test Writer

### 中优先级（读取指南 + 执行脚本）
- 生成功能模块 → scripts/generate_feature.py
- 生成数据模型 → scripts/generate_model.py
- 生成 BLoC → scripts/generate_bloc.py

### 低优先级（参考文档）
- 技术选型 → packages-guide.md
- 学习知识 → skills/architecture/, skills/testing/
- 故障排除 → diagnostic/

## 多步骤工作流

### 完整功能开发流程
1. **规划**：architecture-guide.md + packages-guide.md
2. **生成**：scripts/generate_feature.py
3. **设计**：agents/tdd-coach.md
4. **实现**：TDD 循环（Red/Green/Refactor）
5. **测试**：agents/test-writer.md
6. **审查**：agents/code-reviewer.md + agents/architecture-reviewer.md

### Bug 修复流程
1. **诊断**：diagnostic/build-errors.md 或 runtime-errors.md
2. **定位**：分析错误堆栈和日志
3. **修复**：应用对应修复方案
4. **验证**：运行测试
5. **审查**：agents/code-reviewer.md

### 性能优化流程
1. **分析**：diagnostic/performance-profiler.md
2. **定位**：使用 DevTools 识别瓶颈
3. **优化**：应用优化策略
4. **验证**：性能测试
5. **监控**：持续监控

## 注意事项

1. **Agent 优先**：遇到复杂任务时优先触发对应的 Agent
2. **渐进式加载**：先读取核心指南，需要时再读取详细技能
3. **上下文保持**：在同一会话中保持上下文，避免重复读取
4. **错误恢复**：遇到错误时优先使用诊断指南，而不是盲目重试
5. **用户反馈**：根据用户反馈调整策略，灵活切换资源
