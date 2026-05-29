---
name: memory-layered
description: Hermes Agent 分层记忆系统技能，掌握五层记忆架构（索引/项目/基础设施/教训/日志）、标准化写入格式、容量管理策略和维护流程
tags:
  - hermes-agent
  - memory-architecture
  - layered-memory
  - knowledge-management
  - memory-maintenance
---

# Memory Layered System

## 任务目标
- 本 Skill 用于：实施和管理 Hermes Agent 的分层记忆架构
- 能力包含：五层架构设计、写入规范、容量优化、维护策略
- 触发条件：需要解决记忆混乱、流水账或容量溢出问题时
- **前置要求**：建议先掌握 [memory-system](../memory-system/) 子技能

## 核心问题与解决方案

### 未分层的典型问题

```
❌ 问题 1: 流水账式 MEMORY.md
User asked about Python. User likes TypeScript. Project uses Rust.
Deployed to production. Fixed a bug. User changed editor...
(200+ lines of unstructured text)
→ 无法快速找到关键信息
→ 达到字符限制后无法添加新信息

❌ 问题 2: 失忆式 Agent
Session 1: User tells AI "I prefer concise responses"
         AI: Okay! (但没有保存)

Session 2 (next day):
AI: [长篇大论的解释...]  ← 忘记了用户的偏好！

❌ 问题 3: 教训不传承
Session 1: AI makes mistake, wastes 2 hours
         Lesson learned: "Don't use apt install python3-pip"

Session 2 (next week):
AI: Let me install python3-pip using apt...
        [重复同样的错误]  ← 教训没有被记录
```

### 分层架构解决方案

```
✅ 分层后:

MEMORY.md (索引层, <40行)
├── User Profile Summary (3行)
├── Active Projects Index (5行)
├── Quick Links to detailed files (5行)
└── Key Facts (10行)

memory/projects.md (项目层)
├── Project A: Status, stack, current phase...
├── Project B: Status, stack, current phase...

memory/lessons.md (教训层)
├── 🔴 Critical: Never repeat these mistakes
├── 🟡 Warning: Be careful with these
└── 🟢 Tips: Best practices discovered

memory/2026-04-24.md (日志层)
├── 09:00 - Session Start
├── 09:30 - Task: Auth Design
└── ...

→ 信息组织清晰 ✅
→ 快速找到需要的内容 ✅
→ 跨 Session 保持连续性 ✅
→ 教训被传承 ✅
```

## 五层架构详解

### 架构总览

```
Layer 1: INDEX LAYER (索引层)     → MEMORY.md (<40行)
Layer 2: PROJECT LAYER (项目层)   → memory/projects.md
Layer 3: INFRASTRUCTURE LAYER    → memory/infra.md
Layer 4: LESSONS LAYER (教训层)  → memory/lessons.md
Layer 5: DAILY LOG LAYER (日志层) → memory/YYYY-MM-DD.md
```

### Layer 1: MEMORY.md（记忆索引）

**核心约束**：严格限制在 **40 行以内**

**标准模板**：

```markdown
# Memory Index

> Last Updated: 2026-04-24
> Total Projects: 2 Active | 1 Archived

## User Profile Summary
- **Name**: Alex Chen
- **Role**: Senior Full-Stack Developer
- **Timezone**: UTC+8
- **Communication Style**: Concise, code-first

## Active Projects Index

| Project | Status | Stack | Current Focus |
|---------|--------|-------|---------------|
| myapi | 🟢 Active | Rust+Axum+SQLx | Auth Module |
| frontend-app | 🟡 Review | Next.js+Tailwind | API Integration |

## Quick Navigation

| Need | Go To |
|------|-------|
| Project details | memory/projects.md |
| Infrastructure | memory/infra.md |
| Past mistakes | memory/lessons.md |
| Today's work | memory/2026-04-24.md |

## Environment Snapshot
- **OS**: Ubuntu 22.04 LTS
- **Docker**: v24.x, running 5 containers
- **Primary DB**: PostgreSQL 16

---
*Lines used: 34/40 (85% capacity)*
```

**维护策略**：每周整理一次

### Layer 2: memory/projects.md（项目状态追踪）

**数据模型**：

每个项目包含：
- Status: 🟢 Active / 🟡 In Review / 🔴 Blocked / ⚪ Paused / ✅ Completed
- Location: 项目路径
- Stack: 技术栈列表
- Current Phase: 当前阶段
- Blockers: 阻塞项
- Next Steps: 下一步行动
- Last Updated: 最后更新日期

**标准模板**：

```markdown
# Project Status Tracker

## myapi (Rust Web Service)
- **Status**: 🟢 Active Development
- **Location**: `~/code/myapi`
- **Stack**: Rust 1.75+, Axum 0.7, SQLx 0.7, PostgreSQL 16
- **Current Phase**: Sprint 3 - User Authentication Module
- **Blockers**: None ✅
- **Next Steps**: Implement JWT refresh token logic
- **Last Updated**: 2026-04-23

## frontend-app (Next.js Dashboard)
- **Status**: 🟡 In Review (Waiting for Dependencies)
- **Location**: `~/code/frontend-app`
- **Stack**: Next.js 14, React 18, Tailwind CSS 3.4
- **Blockers**: ⚠️ Waiting for myapi v2 endpoints
- **Next Steps**: Connect to /api/users endpoint
- **Last Updated**: 2026-04-20
```

**更新时机**：项目有进展时立即更新

### Layer 3: memory/infra.md（基础设施速查）

**适用场景**：需要快速查找服务器 IP、部署命令、环境变量等

**标准模板**：

```markdown
# Infrastructure Reference

> Last Updated: 2026-03-15

## Servers
| Name | IP | Purpose | SSH Key |
|------|-----|---------|---------|
| production | 203.0.113.50 | Main API server | ~/.ssh/prod_key |
| staging | 203.0.113.51 | Staging env | ~/.ssh/staging_key |

## Services
- PostgreSQL: localhost:5432 (dev), prod-db:5432 (prod)
- Redis: localhost:6379

## Deployment
- Main branch: main
- Deploy command: ./deploy.sh production
- Rollback: ./deploy.sh rollback [version]

## Environment Variables (.env.template)
DATABASE_URL=postgresql://...
JWT_SECRET=your-secret-here
REDIS_URL=redis://localhost:6379
```

**特点**：相对稳定，只在基础设施变更时更新

### Layer 4: memory/lessons.md（教训库）

**严重程度分级系统**：

```
🔴 CRITICAL (红色) - 绝不能再犯的错误
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
标准：
- 造成数据丢失或安全漏洞
- 浓费大量时间 (> 4小时)
- 造成生产事故或客户影响

行为规则：
- Agent 必须主动检查相关教训后再行动
- 如果涉及的操作匹配 🔴 教训，必须提醒用户


🟡 WARNING (黄色) - 需要小心的陷阱
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
标准：
- 容易踩的坑，但不致命
- 会浪费 30分钟 - 2 小时
- 非显而易见的配置或行为

行为规则：
- Agent 在遇到相关技术栈时应提及
- 作为预防性提示给出


🟢 TIPS (绿色) - 最佳实践和优化
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
标准：
- 提升效率的发现
- 经过验证的最佳实践
- 工作流改进

行为规则：
- 作为建议性提示给出
- 在相关场景中主动分享
```

**标准模板**：

```markdown
# Lessons Learned Library

> Total: 12 lessons (3 Critical, 5 Warning, 4 Tips)

## 🔴 CRITICAL - Never Repeat These Mistakes

### 1. Never Commit .env Files or Secrets
- **Date**: 2026-01-15
- **Impact**: API keys exposed for 2 hours; had to rotate all keys
- **Solution**: Always add `.env` to `.gitignore`; use pre-commit hooks
- **Tags**: security, git, secrets, critical

### 2. Don't Use `apt install python3-pip` on Ubuntu 22.04+
- **Date**: 2026-02-20
- **Impact**: Wasted 2+ hours debugging broken pip
- **Solution**: Use `get-pip.py` or `ensure-pip` module
- **Tags**: ubuntu, python, pip, critical

## 🟡 WARNING - Be Careful With These

### 3. Axum Async Handlers Must Return `impl IntoResponse`
- **Date**: 2026-03-15
- **Issue**: Compilation error with confusing message
- **Solution**: Use `impl IntoResponse` return type
- **Tags**: rust, axum, async

## 🟢 TIPS - Best Practices & Optimizations

### 4. Use memoryFlush for Long Conversations (>50 messages)
- **Date**: 2026-04-01
- **Benefit**: Prevents context window overflow
- **Tags**: memory, optimization
```

### Layer 5: memory/YYYY-MM-DD.md（每日日志）

**时间戳格式规范**：

```markdown
## HH:MM - [TYPE]: [Title]

**Context**: [Optional background]

- [What happened - start with verb]
- [Key decisions and reasoning]
- [Outcomes or deliverables]

**Lesson**: [If something was learned] (optional)
**TODO**: [Follow-up items] (optional)
**Tags**: tag1, tag2 (optional)
```

**类型分类**：

| 类型 | 用途 | 示例 |
|------|------|------|
| `Session Start` | 会话开始 | 记录启动时读取了哪些文件 |
| `Task` | 主要工作任务 | 实现功能、编写文档、设计架构 |
| `Interruption` | 突发中断 | 紧急 Bug 修复、临时请求 |
| `Meeting` | 会议/讨论 | 技术讨论、需求评审 |
| `Learning` | 学习新知识 | 阅读文档、尝试新技术 |
| `Decision` | 重要决策 | 技术选型、架构决策 |

**完整的一天示例**：

```markdown
# 2026-04-24 Daily Log

## 08:55 - Session Start
- Started new session
- Read SOUL.md, USER.md, MEMORY.md (full index loaded)
- Ready to continue work

## 09:00 - Task: Continue Auth Module Implementation
- Reviewed docs/auth-design.md from yesterday
- Confirmed: bcrypt for passwords, JWT for tokens
- Created file structure: src/auth/
- Implemented models.rs with request/response structs
- Progress: ~20% of login endpoint complete

## 14:00 - Interruption: Critical Bug in Production
- Alert: payment calculation off by $0.01
- Root cause: floating point precision issue
- Fix: switched to Decimal type
- Deployed hotfix v1.2.1
- Resolution Time: 45 minutes

## 14:45 - Lesson Learned: Use Decimal for Financial Calculations
- Impact: Caught in testing (would have caused real discrepancies)
- → Also recorded to memory/lessons.md as 🟢 Tip #10

## 17:00 - End of Day Wrap-up
### Completed Today ✅
- [x] Auth module structure created
- [x] Models and error types implemented
- [x] Production bug fixed

### Deferred to Tomorrow 📅
- [ ] Complete login endpoint
- [ ] Implement refresh endpoint
- [ ] Write integration tests
```

## 写入时机决策树

```
发生了一件事，要不要记录？

    │
    ▼
这件事值得记住吗？
    │
    ├── 不值得 → 忽略（太琐碎）
    │
    └── 值得 ↓
            │
            ▼
        是什么类型的信息？
            │
            ├── 用户偏好/个人信息
            │   └── → USER.md (via memory tool)
            │
            ├── 项目进展/状态变化
            │   └── → memory/projects.md
            │
            ├── 踩坑/错误/重要发现
            │   └── → memory/lessons.md
            │
            ├── 今天做了什么/决策过程
            │   └── → memory/YYYY-MM-DD.md
            │
            └── 环境/基础设施事实
                └── → MEMORY.md (如果重要且稳定)
                   or memory/infra.md (如果详细)
```

## 跨层数据流动

### 信息流转图

```
Layer 5: Daily Log (数据源)
    │
    ├──→ Layer 4: Lessons (提取教训)
    │       发现错误/技巧 → 立即写入
    │
    ├──→ Layer 2: Projects (更新状态)
    │       项目进展 → 同步更新
    │
    └──→ Layer 1: Memory Index (每周整理)
            汇总关键信息
            更新链接和摘要
```

### 具体示例

**场景：修复了一个生产 Bug**

```
Step 1: Layer 5 - 记录到当日日志
## 14:00 - Interruption: Payment Calculation Bug
- Discovered floating point issue
- Fixed with Decimal type
- Deployed hotfix v1.2.1

Step 2: Layer 4 - 提取教训
### Use Decimal for Financial Calculations
- Date: 2026-04-24
- Solution: Always use rust_decimal

Step 3: Layer 2 - 更新项目状态
myapi project:
- Current Phase: Bug fixes (was: Auth Module)
- Next Steps: Return to auth implementation

Step 4: Layer 1 - 周末整理
Key Facts:
- Added: "Using Decimal for finances (since 2026-04-24)"
```

## 容量管理与优化

### 各层容量规划

| 层级 | 建议大小 | 最大值 | 增长速度 | 清理策略 |
|------|---------|--------|---------|---------|
| Layer 1 (Index) | 20-35 行 | **40 行** (硬限) | 很慢 | 每周压缩 |
| Layer 2 (Projects) | 5-15 行/项目 | 动态 | 中等 | 归档已完成项目 |
| Layer 3 (Infra) | 100-300 行 | 500 行 | 很慢 | 仅重大变更时更新 |
| Layer 4 (Lessons) | 10-20 条/月 | 无硬限 | 慢慢增长 | 月度审查归档 |
| Layer 5 (Logs) | 20-50 行/天 | 无硬限 | 最快 | 90天后删除或压缩 |

### 压缩策略

**当任何层接近容量限制时**：

```
Layer 1 接近 40 行:
├── 移除过时的 "Key Facts"
├── 合并相似的条目
└── 归档已完成项目

Layer 2 过于庞大 (> 100 行):
├── 归档已完成项目 (✅ Completed → Archived)
└── 只保留活跃项目的详细信息

Layer 4 课程过多 (> 50 条):
├── 将已广泛知晓的 🔴 降级为 🟡
├── 将已解决的 🟡 移至 "Resolved" archive
└── 保留真正有价值的内容

Layer 5 日志过多:
├── 删除 > 90 天的旧日志
├── 或压缩为周总结 (2026-W17-summary.md)
└── 重要信息应已提取到其他层级
```

## 定期维护计划

### 每周维护清单（推荐周五 EOD）

```
□ Review memory/projects.md
  - Archive completed projects
  - Update stalled projects status
  - Remove projects no longer active

□ Clean up memory/YYYY-MM-DD.md files
  - Extract important lessons to memory/lessons.md
  - Compress verbose entries
  - Delete logs older than 90 days (optional)

□ Validate MEMORY.md index
  - Check all links still valid
  - Update "Last Updated" date
  - Ensure < 40 lines constraint

□ Review memory/lessons.md
  - Promote/demote severity levels if warranted
  - Look for patterns (multiple lessons = systemic fix needed)
  - Archive obsolete lessons
```

### 月度审查（推荐每月第一个周一）

```
□ Statistics & Trends Analysis
  - Count lessons by category
  - Track month-over-month growth
  - Identify repeat mistake prevention success rate

□ Quality Metric Check
  - Repeat Mistakes: 0? (all 🔴 lessons successfully avoided)
  - Lessons Applied Preventively: How many times caught issues early?

□ Optimization Opportunities
  - Any patterns that deserve a dedicated guide?
  - Need to reorganize layers?
  - Capacity adjustments needed?
```

## 故障排除

### 问题 1: 记忆文件混乱

**症状**：memory/ 目录下文件杂乱，找不到信息

**解决方案**：
```bash
# 步骤 1: 查看当前状态
ls -la memory/
wc -l memory/*.md

# 步骤 2: 执行清理
# 让 Agent 执行以下操作：
# 1. 将重要信息迁移到正确层级
# 2. 压缩冗余内容
# 3. 删除过时或无用的文件
# 4. 重建索引 (MEMORY.md)
```

### 问题 2: 教训不生效

**症状**：记录了教训但仍然重复犯错

**可能原因**：
1. 教训写得太模糊（不够具体）
2. Agent 没有主动检查 lessons.md
3. 严重程度标记不准确

**解决方案**：
```markdown
# 改进教训记录质量：

❌ 模糊教训：
"Be careful with database migrations"

✅ 具体教训：
### Don't Run Migrations Without Backup on Production
- **Date**: 2026-03-10
- **Impact**: Lost 3 days of user data
- **Root Cause**: Assumed migration was safe without reading it
- **Correct Action**:
  1. Always `pg_dump` before any schema migration
  2. Read migration file completely before running
  3. Test on staging first
- **Prevention Checklist**:
  - [ ] Backup created?
  - [ ] Migration reviewed?
  - [ ] Tested on staging?
- **Tags**: database, postgresql, migration, backup, critical
```

## 资源索引
- **母技能**：[SKILL.md](../SKILL.md) - 完整技能体系概览
- **前置子技能**：[memory-system](../memory-system/) - Memory Tool 操作接口
- **关联子技能**：[agents-workflow](../agents-workflow/) - 工作手册中的记忆管理部分
- **OpenClaw 参考**：https://tbbbk.com/openclaw-advanced-config-guide/

## 注意事项
- 这是高级功能，建议先掌握基础 Memory 系统
- 保持各层职责单一，避免信息冗余
- 定期执行维护计划，防止记忆腐烂
- 教训库是最有价值的资产，认真维护
