---
name: context-files
description: Hermes Agent Context Files 系统技能，掌握上下文文件优先级加载链（.hermes.md → AGENTS.md → CLAUDE.md → .cursorrules）、渐进式发现机制和安全处理流程
tags:
  - hermes-agent
  - context-files
  - agents-md
  - soul-md
  - priority-chain
---

# Context Files System

## 任务目标
- 本 Skill 用于：掌握 Hermes Agent 的上下文文件系统
- 能力包含：优先级加载机制、AGENTS.md 渐进式发现、SOUL.md 特殊地位、安全处理
- 触发条件：需要配置项目上下文或理解文件加载顺序时

## 核心概念

Context Files 系统自动发现并加载配置文件，塑造 Agent 的行为方式。

**支持的文件类型**：

| 文件 | 用途 | 发现方式 | 优先级 |
|------|------|---------|--------|
| `.hermes.md` / `HERMES.md` | 项目指令（最高优先级） | Walk to git root | ⭐⭐⭐⭐⭐ |
| `AGENTS.md` | 项目指令、架构、约定 | CWD + 子目录渐进 | ⭐⭐⭐⭐ |
| `CLAUDE.md` | Claude Code 上下文兼容 | CWD + 子目录渐进 | ⭐⭐⭐ |
| `.cursorrules` | Cursor IDE 编码规范 | 仅 CWD | ⭐⭐ |
| `.cursor/rules/*.md` | Cursor 规则模块 | 仅 CWD | ⭐⭐ |
| **SOUL.md** | **全局个性定制** | **仅 HERMES_HOME** | **始终加载 (slot #1)** |

## 优先级加载机制

### First Match Wins 算法

```
启动检测流程：
    │
    ▼
检查 .hermes.md ──→ 存在？→ 加载它，停止检测
    │               不存在 ↓
    ▼
检查 AGENTS.md ──→ 存在？→ 加载它，停止检测
    │               不存在 ↓
    ▼
检查 CLAUDE.md ──→ 存在？→ 加载它，停止检测
    │               不存在 ↓
    ▼
检查 .cursorrules → 存在？→ 加载它
    │
    ▼
（独立加载）SOUL.md → 始终从 HERMES_HOME 加载
```

**重要规则**：
- 每个会话只加载**一个**项目上下文类型（first match wins）
- **SOUL.md 始终独立加载**作为 Agent 身份（不受上述优先级影响）
- 优先级不可自定义，按固定顺序检测

## AGENTS.md 渐进式发现

### 工作机制

```
my-project/
├── AGENTS.md              ← 启动时加载（系统提示词）
├── frontend/
│   ├── src/
│   │   └── App.tsx       ← Agent 读取此文件时
│   └── AGENTS.md          ← 发现并注入 frontend/AGENTS.md
├── backend/
│   ├── main.py            ← Agent 读取此文件时
│   └── AGENTS.md          ← 发现并注入 backend/AGENTS.md
└── shared/
    └── utils.ts
```

### 三大优势

**优势 1: 避免 Prompt Bloat**
```
传统方式（全部加载）：50,000 tokens overhead ❌
渐进式发现方式：只加载需要的部分 ✅
```

**优势 2: Prefix Cache Preservation**
```
Without: Large cache size, slower invalidation
With: Smaller caches, faster overall ✅
```

**优势 3: Context Relevance**
```
When working on frontend code → Only see frontend conventions
When working on backend code → Only see backend rules ✅
```

## SOUL.md 特殊地位

### 与其他上下文文件的关键区别

| 维度 | SOUL.md | AGENTS.md / 其他 |
|------|---------|------------------|
| **加载来源** | 仅 HERMES_HOME | 项目工作目录 |
| **作用域** | 全局（跟随实例） | 项目级别 |
| **系统位置** | Slot #1（身份） | Project Context 部分 |
| **发现方式** | 不探测工作目录 | 渐进式目录发现 |
| **覆盖机制** | 可被 /personality 覆盖 | 无覆盖机制 |

### SOUL.md 设计原则
- ✅ **应该包含**：语气、沟通风格、直接程度、默认交互方式
- ❌ **不应该包含**：一次性项目指令、具体文件路径、仓库约定

## 安全处理机制

### 多层安全管道

```
文件内容
    │
    ▼
[Layer 1: UTF-8 编码验证]
    │
    ▼
[Layer 2: Prompt Injection 扫描]
    │
    ├── 检测到恶意内容 → 阻止加载
    └── 安全通过 ↓
            ▼
        [Layer 3: 长度检查]
            │
            ├── ≤ 20,000 chars → 完整加载
            └── > 20,000 chars → 头尾截断 (70%头 + 20%尾)
```

### 截断算法

当文件超过 20,000 字符时自动截断：

```
Original (25,000 chars):
# Project Guide (完整文档)

After truncation (20,000 chars max):
┌────────────────────────────┐
│ 前 14,000 chars (70%)     │  ← 主要内容
├────────────────────────────┤
│ [CONTENT TRUNCATED]       │  ← 截断标记
│ Original: 25,000 chars    │
└────────────────────────────┘
└── 后 4,000 chars (20%)     │  ← 结尾内容
```

## 使用示例

### 示例 1：创建标准 AGENTS.md

```markdown
# Project Context

This is a Next.js 14 web application with Python FastAPI backend.

## Architecture
- Frontend: Next.js 14 with App Router in `/frontend`
- Backend: FastAPI in `/backend`, uses SQLAlchemy ORM
- Database: PostgreSQL 16
- Deployment: Docker Compose on Hetzner VPS

## Conventions
- Use TypeScript strict mode for all frontend code
- Python code follows PEP 8, use type hints everywhere
- All API endpoints return JSON with `{data, error, meta}` shape
- Tests go in `__tests__/` (frontend) or `tests/` (backend)

## Important Notes
- Never modify migration files directly — use Alembic commands
- The `.env.local` file has real API keys, don't commit it
- Frontend port is 3000, backend is 8000, DB port is 5432
```

### 示例 2：创建个性化 SOUL.md

```markdown
# Personality

You are a pragmatic senior engineer with strong taste.
You optimize for truth, clarity, and usefulness over politeness theater.

## Style
- Be direct without being cold
- Prefer substance over filler
- Push back when something is a bad idea
- Admit uncertainty plainly
- Keep explanations compact unless depth is useful

## What to avoid
- Sycophancy
- Hype language
- Repeating the user's framing if it's wrong
- Overexplaining obvious things

## Technical posture
- Prefer simple systems over clever systems
- Care about operational reality, not idealized architecture
- Treat edge cases as part of the design, not cleanup
```

### 示例 3：多层级项目结构

```
company-monorepo/
├── AGENTS.md                    # 公司级规范（启动时加载）
├── packages/
│   ├── web-app/
│   │   ├── AGENTS.md            # Web 应用特定规范（访问时发现）
│   │   └── src/
│   └── api-service/
│       ├── AGENTS.md            # API 服务特定规范（访问时发现）
│       └── src/
```

## 高级技巧

### 技巧 1：利用 .cursorrules 兼容性

如果你已经在使用 Cursor IDE，可以直接复用配置：

```bash
# 现有 .cursorrules 文件会被 Hermes 自动识别
# （前提是没有更高优先级的 .hermes.md 或 AGENTS.md）
```

### 技巧 2：动态上下文切换

使用符号链接快速切换项目配置：

```bash
# 创建多个配置变体
cat > AGENTS.dev.md << 'EOF'
# Development Mode
- Enable verbose logging
- Use hot reload
- Run linting in watch mode
EOF

cat > AGENTS.prod.md << 'EOF'
# Production Mode
- Optimize for performance
- Minimize bundle size
- Strict type checking
EOF

# 快速切换
ln -sf AGENTS.dev.md AGENTS.md   # 切换到开发模式
ln -sf AGENTS.prod.md AGENTS.md  # 切换到生产模式
```

### 技巧 3：Token 预算分配

**建议的系统提示词预算**（假设 128K context window）：

```
总预算: ~128,000 tokens
│
├── SOUL.md: ~2,000 tokens (1.5%)        ← 身份定义
├── Project Context: ~5,000 tokens (4%)   ← 项目指令
├── Dynamic Context: ~10,000 tokens (8%)  ← 渐进式发现
├── Memory: ~1,300 tokens (1%)           ← 持久化记忆
├── Conversation History: ~80,000 tokens (62.5%)
├── Tool Results: ~20,000 tokens (15.6%)
└── System Overhead: ~9,700 tokens (7.6%)
```

## 故障排除

### 问题 1：上下文文件未被加载

**诊断步骤**：
```bash
# 1. 检查文件是否存在
ls -la AGENTS.md .hermes.md CLAUDE.md .cursorrules

# 2. 检查文件名是否正确（区分大小写）
#    AGENTS.md ≠ Agents.md ≠ agents.md

# 3. 检查是否有更高优先级文件覆盖了它
ls -la .hermes.md  # 如果存在，会覆盖 AGENTS.md
```

### 问题 2：子目录 AGENTS.md 未被发现

**解决方案**：
1. 确保 Agent 先读取子目录中的文件
2. 手动提示 Agent 检查该目录
3. 如果经常需要在某子目录工作，考虑将该目录的内容提升到根 AGENTS.md

### 问题 3：SOUL.md 更改不生效

**原因**：同 Memory 的冻结快照机制

**解决方案**：
```bash
# 1. 确认编辑了正确的文件
#    应该是 ~/.hermes/SOUL.md
#    不是项目目录下的 SOUL.md（不会被加载）

# 2. 重启 Hermes 会话
#    SOUL.md 只在会话开始时加载
```

## 资源索引
- **官方文档**：https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files
- **母技能**：[SKILL.md](../SKILL.md) - 完整技能体系概览
- **关联子技能**：[agents-workflow](../agents-workflow/) - AGENTS.md 工作手册实战
- **关联子技能**：[personality-config](../personality-config/) - SOUL.md 配置详解

## 注意事项
- 优先级不可自定义，按固定顺序检测
- SOUL.md 只从 HERMES_HOME 加载，不放工作目录
- 超长文件 (>20,000 chars) 会被自动截断
- 所有文件都会经过 prompt injection 扫描
- 版本控制 AGENTS.md，将项目上下文纳入 Git 管理
