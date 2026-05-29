# Flutter Skills - 快速索引

本文档提供所有参考资源的快速查找索引。

## 按类别快速查找

### 📦 Discipline-Enforcing Skills（强制工作流）
| 资源 | 路径 | 说明 |
|------|------|------|
| TDD 工作流 | references/testing-guide.md | TDD 流程和测试模式 |
| 架构规范 | references/architecture-guide.md | Clean Architecture、BLoC 模式 |
| TDD Coach | references/agents/tdd-coach.md | 交互式 TDD 指导 |
| Code Reviewer | references/agents/code-reviewer.md | 代码质量审查 |

### 📚 Reference Skills（参考指南）
| 资源 | 路径 | 说明 |
|------|------|------|
| 架构指南 | references/architecture-guide.md | 架构设计指南 |
| 测试指南 | references/testing-guide.md | 测试编写指南 |
| 库选型指南 | references/packages-guide.md | 库选型指南 |
| 命令指南 | references/commands-guide.md | 命令参考 |

### 🔍 Diagnostic Skills（故障排除）
| 资源 | 路径 | 说明 |
|------|------|------|
| 构建错误 | references/diagnostic/build-errors.md | 构建问题诊断 |
| 运行时错误 | references/diagnostic/runtime-errors.md | 运行时问题诊断 |
| 状态调试 | references/diagnostic/state-debugging.md | 状态调试 |
| 性能分析 | references/diagnostic/performance-profiler.md | 性能优化 |

### ⚡ Commands（命令脚本）
| 脚本 | 路径 | 说明 |
|------|------|------|
| generate_feature | scripts/generate_feature.py | 生成 Feature 结构 |
| generate_model | scripts/generate_model.py | 生成 Freezed 模型 |
| generate_bloc | scripts/generate_bloc.py | 生成 BLoC 结构 |
| generate_test | scripts/generate_test.py | 生成测试模板 |

### 🤖 Agents（智能助手）
| Agent | 路径 | 触发方式 |
|-------|------|----------|
| TDD Coach | references/agents/tdd-coach.md | "请帮我用 TDD 实现" |
| Code Reviewer | references/agents/code-reviewer.md | "请审查这段代码" |
| Test Writer | references/agents/test-writer.md | "编写测试" |
| Architecture Reviewer | references/agents/architecture-reviewer.md | "审查架构" |

## 按主题快速查找

### 架构相关
- **综合指南**：references/architecture-guide.md
- **详细技能**：
  - references/skills/architecture/bloc-architecture.md
  - references/skills/architecture/clean-architecture.md
  - references/skills/architecture/dependency-injection.md
  - references/skills/architecture/error-handling.md
  - references/skills/architecture/feature-structure.md
- **架构审计**：references/agents/architecture-reviewer.md

### 测试相关
- **综合指南**：references/testing-guide.md
- **详细技能**：
  - references/skills/testing/tdd-workflow.md
  - references/skills/testing/unit-testing.md
  - references/skills/testing/widget-testing.md
  - references/skills/testing/bloc-testing.md
  - references/skills/testing/mocking-patterns.md
- **相关 Agents**：
  - references/agents/tdd-coach.md
  - references/agents/test-writer.md

### 网络与数据
- **库选型**：references/packages-guide.md（网络请求章节）
- **详细命令**：references/commands/generate-bloc.md

### 状态管理
- **综合指南**：references/architecture-guide.md（BLoC 章节）
- **详细技能**：references/skills/architecture/bloc-architecture.md
- **库选型**：references/packages-guide.md（状态管理章节）

### 路由与导航
- **库选型**：references/packages-guide.md（路由导航章节）
- **详细命令**：references/commands/generate-feature.md

### 代码生成
- **库选型**：references/packages-guide.md（工具与辅助章节）
- **详细命令**：
  - references/commands/generate-model.md
  - references/commands/generate-feature.md
  - references/commands/generate-test.md

## 按使用场景查找

### 🚀 创建新项目
1. **技术栈选型**：references/packages-guide.md
2. **项目初始化**：SKILL.md（操作步骤）
3. **架构设计**：references/architecture-guide.md

### 📝 开发新功能
1. **生成 Feature 结构**：scripts/generate_feature.py
2. **TDD 开发**：references/agents/tdd-coach.md
3. **编写测试**：references/agents/test-writer.md
4. **代码审查**：references/agents/code-reviewer.md

### 🐛 修复 Bug
1. **构建错误**：references/diagnostic/build-errors.md
2. **运行时错误**：references/diagnostic/runtime-errors.md
3. **状态问题**：references/diagnostic/state-debugging.md

### ⚡ 性能优化
1. **性能分析**：references/diagnostic/performance-profiler.md
2. **性能监控**：references/packages-guide.md（性能与调试章节）

### 📚 学习与培训
1. **架构学习**：references/skills/architecture/
2. **测试学习**：references/skills/testing/
3. **代码生成学习**：references/skills/generation/
4. **TDD 实践**：references/agents/tdd-coach.md

## 按关键词快速查找

| 关键词 | 推荐资源 |
|--------|----------|
| BLoC | references/skills/architecture/bloc-architecture.md |
| Clean Architecture | references/skills/architecture/clean-architecture.md |
| TDD | references/agents/tdd-coach.md |
| 测试 | references/testing-guide.md |
| 依赖注入 | references/skills/architecture/dependency-injection.md |
| 状态管理 | references/packages-guide.md |
| 网络请求 | references/packages-guide.md |
| 数据库 | references/packages-guide.md |
| 代码生成 | references/commands/ |
| 路由 | references/packages-guide.md |
| 国际化 | references/packages-guide.md |

## 资源依赖关系

```
SKILL.md（入口）
├── scripts/（独立脚本）
│   ├── generate_feature.py
│   ├── generate_model.py
│   ├── generate_bloc.py
│   └── generate_test.py
│
└── references/（参考文档）
    ├── agents/（智能助手）
    │   ├── tdd-coach.md
    │   ├── code-reviewer.md
    │   ├── test-writer.md
    │   └── architecture-reviewer.md
    │
    ├── skills/（详细技能）
    │   ├── architecture/（5个）
    │   ├── generation/（1个）
    │   └── testing/（5个）
    │
    ├── diagnostic/（4个）
    ├── commands/（9个）
    ├── architecture-guide.md
    ├── testing-guide.md
    ├── packages-guide.md
    └── commands-guide.md
```

## 使用建议

### 对于 AI 智能体
1. **先读取 SKILL.md**：了解整体流程和决策逻辑
2. **根据场景选择资源**：使用本索引快速定位
3. **优先使用 Agents**：遇到复杂任务时触发对应 Agent
4. **参考详细技能**：深入理解特定主题时读取 skills/ 下的文档

### 对于开发者
1. **快速开始**：SKILL.md → 操作步骤
2. **深入学习**：references/skills/ 下的详细文档
3. **遇到问题**：references/diagnostic/ 下的诊断指南
4. **技术选型**：references/packages-guide.md
