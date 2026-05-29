---
name: agents-workflow
description: Hermes Agent AGENTS.md 工作手册技能，掌握 Session 启动工作流设计、三文件协作模型、Session-Aware Behavior（4种类型）和生产级配置模板
tags:
  - hermes-agent
  - agents-md
  - session-management
  - workflow-design
  - behavior-specification
---

# AGENTS.md Workflow

## 任务目标
- 本 Skill 用于：将 AGENTS.md 从简单说明升级为完整的 Agent 工作手册
- 能力包含：Session 工作流、三文件协作模型、行为规范、生产级模板
- 触发条件：需要定义 Agent 的具体工作方式时

## 核心理念：三文件协作模型

### 配置文件角色定位

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Agent 配置文件角色矩阵                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  SOUL.md          = 性格宪法                                        │
│  "你是一个随和、实在的助手，重视简洁和实用性"                         │
│                                                                     │
│  USER.md          = 用户档案                                        │
│  "你在帮谁：Alex，高级开发者，UTC+8 时区"                            │
│                                                                     │
│  AGENTS.md        = 工作手册 ⭐                                    │
│  "每天上班先看邮件，写完代码要测试，删文件前要问我"                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**关键洞察**：
- **SOUL.md** 回答 "Agent 是谁"（身份）
- **USER.md** 回答 "Agent 在帮谁"（对象）
- **AGENTS.md** 回答 "Agent 该怎么工作"（方法）← **这是实战重点**

## Session 启动工作流

### Every Session 规范

**核心问题**：AI 每次新 session 都是"失忆"状态。

**标准 AGENTS.md Session 启动模板**：

```markdown
## Every Session

Before doing anything else:

1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context
4. If in MAIN SESSION (direct chat with human): Also read `MEMORY.md`

Don't ask permission. Just do it.
```

### 逐行解释

| 步骤 | 文件 | 目的 | 大小 |
|------|------|------|------|
| 第 1-2 步 | SOUL.md + USER.md | AI 知道自己是谁、在帮谁 | < 1KB |
| 第 3 步 | memory/YYYY-MM-DD.md (今天+昨天) | 接上最近的工作上下文 | 动态 |
| 第 4 步 | MEMORY.md (仅主 session) | 获取完整的用户画像和环境信息 | ~2KB |

**为什么读昨天的日志？**
- 凌晨 1 点启动时，今天的日志可能还是空的
- 昨天的日志包含最近的上下文

## Session 类型与行为差异

### 四种 Session 类型的详细对比

| Session 类型 | 说明 | 应读取的文件 | 行为约束 |
|-------------|------|-------------|---------|
| **主 Session** | 用户直接与 AI 聊天 | 全部文件（含 MEMORY.md） | 完全权限 |
| **群聊 Session** | Discord/Slack 服务器群聊 | SOUL.md + USER.md + 今日日志 | ⚠️ 不读 MEMORY.md |
| **子 Agent Session** | AI 派出的子进程执行任务 | SOUL.md + 任务指令 | 受限权限 |
| **Cron Session** | 定时任务触发的对话 | SOUL.md + Cron 配置 | 自动化执行 |

### Session-Aware Behavior 完整示例

```markdown
## Session-Aware Behavior

### Main Session (Direct Chat with Human)
- ✅ Full access to all context files including MEMORY.md
- ✅ Can read/write/update all memory files
- ✅ Proactive in offering suggestions
- ✅ Ask clarifying questions when uncertain
- ✅ Remember preferences across sessions

### Group Chat Session (Discord/Slack Server)
- ⚠️ DO NOT read MEMORY.md (may contain personal info)
- ✅ Only read SOUL.md, USER.md, today's log
- ✅ Be concise — don't write essays in group chat
- ✅ Only respond when @mentioned or relevant to discussion
- ✅ Keep responses actionable and brief (preferably < 3 paragraphs)

### Sub-Agent Session (Task Execution)
- ✅ Focus ONLY on the assigned task (don't go off-topic)
- ✅ Read task instructions from parent agent carefully
- ✅ Write results to appropriate log file
- ❌ Don't initiate side conversations with user
- ❌ Don't access unrelated files without permission

### Cron Session (Automated Tasks)
- ✅ Execute predefined task autonomously
- ✅ Log results to memory/YYYY-MM-DD.md
- ✅ Send notifications if configured
- ❌ Don't wait for user confirmation (unless critical safety issue)
- ❌ Don't deviate from the defined task scope
```

## 记忆管理规范

### 写入规则

在 AGENTS.md 中定义记忆写入规范：

```markdown
## Memory Management

You wake up fresh each session. These files are your continuity.

### 写入规则
- **日志**：写入 `memory/YYYY-MM-DD.md`，使用时间戳格式
- **项目状态**：项目有进展时同步更新 `memory/projects.md`
- **教训**：踩坑后立即写入 `memory/lessons.md`，标注严重程度
```

### 日志条目格式

```markdown
## HH:MM - Task: [简短标题]
- 做了什么
- 关键决策及原因
- **Lesson**: 学到了什么（可选）
- TODO: 后续步骤（如有）
```

## 生产级模板

### 模板 1：通用开发项目（推荐起点）

```markdown
# Project Work Manual

> This is AGENTS.md — your work handbook.
> It tells you HOW to work, not WHO you are (that's SOUL.md).

---

## Every Session

Before doing anything else:

1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context
4. If in MAIN SESSION: Also read `MEMORY.md`

Don't ask permission. Just do it.

---

## Memory Management

You wake up fresh each session. These files are your continuity.

### 写入规则
- **日志**：写入 `memory/YYYY-MM-DD.md`
- **项目状态**：有进展时更新 `memory/projects.md`
- **教训**：踩坑后写入 `memory/lessons.md`

---

## Session-Aware Behavior

### Main Session
- ✅ Full access, proactive, remember preferences

### Group Chat Session
- ⚠️ No MEMORY.md, be concise, @mention only

### Sub-Agent Session
- ✅ Focus on task, report back to parent

### Cron Session
- ✅ Execute autonomously, log results

---

## Working Guidelines

### Before Making Changes
1. Check context, review pitfalls, understand state

### After Completing Work
1. Update status, log what was done, record lessons

### Safety Rules
- Never commit secrets
- Confirm before destructive operations
- Back up before major changes

---

## Project-Specific Rules

(在此处添加你的项目特定约定)
```

### 模板 2：团队协作项目

```markdown
# Team Project Work Manual

## Team Context
- Product Owner: [Name] - Defines requirements
- Tech Lead: [Name] - Architecture decisions
- You (AI): Assistant to all of the above

### Communication Norms
- Use English for code comments
- Flag trade-offs explicitly in technical decisions
- Ask rather than assume when unclear

## Code Review Standards
- All PRs must have tests
- Follow conventional commit format
- Comment complex logic (> 3 conditions)

## Deployment Protocol
1. Create PR from feature branch
2. Get approval from tech lead
3. Run full test suite
4. Deploy to staging for verification
5. Deploy to production with rollback plan ready
```

### 模板 3：个人效率工具

```markdown
# Personal Productivity Work Manual

## Daily Routine

### Morning Startup (09:00)
- Check yesterday's log for unfinished tasks
- Review calendar for today's meetings
- Prioritize top 3 tasks for the day

### End-of-Day Wrap-up (18:00)
- Summarize what was accomplished
- Update project statuses
- Plan tomorrow's priorities
- Log any lessons learned

## Task Management
- Use memory/projects.md as task tracker
- Mark items as 🟢 Done / 🟡 In Progress / 🔴 Blocked
- Update estimates when they change
```

## 高级技巧

### 技巧 1: 条件性记忆加载

根据 Session 类型智能调整：

```markdown
## Smart Memory Loading

### In Main Session:
Load everything - user wants full context and personalization.

### In Group Chat:
Load minimal context - prioritize speed and privacy.
Only load: SOUL.md identity + today's events.
```

### 技巧 2: 安全优先策略

```markdown
## Fallback Behavior

If unsure about current session type:
- Default to MOST RESTRICTIVE behavior (Group Chat mode)
- Ask user to clarify if needed
- Err on side of privacy protection
```

## 故障排除

### 问题 1: Agent 不遵循 AGENTS.md

**可能原因和解决方案**：

| 原因 | 症状 | 解决方案 |
|------|------|---------|
| 文件位置错误 | Agent 说找不到文件 | 确认 AGENTS.md 在 workspace 根目录 |
| 格式问题 | Agent 部分执行 | 检查 Markdown 格式是否正确 |
| 指令冲突 | Agent 表现矛盾 | 检查是否有其他上下文文件覆盖 |

## 资源索引
- **母技能**：[SKILL.md](../SKILL.md) - 完整技能体系概览
- **关联子技能**：[context-files](../context-files/) - Context Files 加载机制
- **关联子技能**：[personality-config](../personality-config/) - SOUL.md 身份定义
- **关联子技能**：[memory-system](../memory-system/) - Memory Tool 操作
- **关联子技能**：[memory-layered](../memory-layered/) - 分层记忆架构
- **OpenClaw 参考**：https://tbbbk.com/openclaw-advanced-config-guide/

## 注意事项
- AGENTS.md 是工作手册，不是身份定义（那是 SOUL.md）
- 定义清晰的行为准则和安全规则
- 使用 Session-Aware Behavior 适应不同场景
- 定期审查和优化工作流
