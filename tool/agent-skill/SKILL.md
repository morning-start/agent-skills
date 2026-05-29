---
name: agent
description: Hermes Agent 配置系统技能库，掌握 Memory 持久化记忆、Context Files 上下文注入、Personality 个性化配置、AGENTS.md 工作手册和分层记忆系统的完整技能体系
---

# Hermes Agent Config Skills

## 任务目标
- 本 Skill 用于：全面掌握 Hermes Agent 的配置系统和最佳实践
- 能力包含：Memory 管理、上下文文件、个性化定制、工作流设计、记忆架构
- 触发条件：需要配置或优化 Hermes Agent 环境时

## 技能地图

### 核心基础
- [memory-system](memory-system/) - Memory 系统：持久化记忆管理、Memory Tool 操作接口、冻结快照机制
- [context-files](context-files/) - Context Files 系统：优先级加载链、渐进式发现、安全处理机制
- [personality-config](personality-config/) - Personality 配置：SOUL.md 身份定义、/personality 命令、个性模板

### 实战进阶
- [agents-workflow](agents-workflow/) - AGENTS.md 工作手册：Session 工作流设计、行为规范、生产级模板
- [memory-layered](memory-layered/) - 记忆分层系统：五层架构、写入规范、容量管理策略

## 学习路径

### 🚀 快速入门（首次配置）
1. **[personality-config](personality-config/)** - 定义 Agent 身份和沟通风格
2. **[context-files](context-files/)** - 理解上下文文件加载机制
3. **[agents-workflow](agents-workflow/)** - 编写 AGENTS.md 工作手册

### 📈 效率优化（进阶使用）
4. **[memory-system](memory-system/)** - 掌握 Memory Tool 和跨会话记忆
5. **[memory-layered](memory-layered/)** - 实施五层记忆架构（高级）

### 🎯 生产部署（完整掌握）
按需组合使用各子技能，实现最优配置方案

## 快速开始

### 最小可用配置（3 步上手）

**Step 1: 定义身份** → 参考 `personality-config` 子技能
```markdown
# ~/.hermes/SOUL.md
# Personality
You are a pragmatic senior engineer.
## Style
- Be direct without being cold
- Prefer substance over filler
```

**Step 2: 编写工作手册** → 参考 `agents-workflow` 子技能
```markdown
# AGENTS.md (项目根目录)
## Every Session
1. Read SOUL.md — this is who you are
2. Read USER.md — this is who you're helping
3. Read memory/YYYY-MM-DD.md for recent context
```

**Step 3: 启动验证**
```bash
# 启动 Hermes，观察是否正确加载配置
# 检查点：
# ✅ Agent 行为符合 SOUL.md 定义的风格
# ✅ Agent 自动读取 AGENTS.md 中的启动流程
```

## 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                  Hermes Agent 配置体系                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 1: Identity (身份层)                                  │
│  └── personality-config → SOUL.md + /personality            │
│                                                             │
│  Layer 2: Context (上下文层)                                 │
│  └── context-files → AGENTS.md + 优先级机制                  │
│                                                             │
│  Layer 3: Workflow (工作流层)                                │
│  └── agents-workflow → Session 设计 + 行为规范              │
│                                                             │
│  Layer 4: Memory (记忆层)                                    │
│  ├── memory-system → Memory Tool + 冻结快照                 │
│  └── memory-layered → 五层架构 + 写入规范                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 资源索引
- **官方文档 - Memory**: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
- **官方文档 - Context Files**: https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files
- **官方文档 - Personality**: https://hermes-agent.nousresearch.com/docs/user-guide/features/personality
- **OpenClaw 进阶参考**: https://tbbbk.com/openclaw-advanced-config-guide/

## 注意事项
- 建议按学习路径顺序逐步掌握各子技能
- 子技能可独立使用，也可组合解决复杂问题
- 生产环境建议完整掌握全部 5 个子技能
- 定期审查和优化配置以保持最佳效果
