---
name: memory-system
description: Hermes Agent Memory 系统技能，掌握跨会话持久化记忆管理、Memory Tool 操作接口（add/replace/remove）、冻结快照机制和容量优化策略
tags:
  - hermes-agent
  - memory-management
  - persistent-memory
  - memory-tool
---

# Memory System

## 任务目标
- 本 Skill 用于：掌握 Hermes Agent 的持久化记忆系统
- 能力包含：Memory Tool 操作、冻结快照机制、容量管理、内容分类
- 触发条件：需要配置或优化 Agent 记忆功能时

## 核心概念

Memory 系统提供**跨会话持久化记忆**能力，让 Agent 能够记住用户偏好、项目环境和工作经验。

**核心组件**：

| 文件 | 用途 | 字符限制 | 典型条目数 |
|------|------|----------|-----------|
| `MEMORY.md` | Agent 个人笔记（环境事实、约定、经验教训） | 2,200 chars (~800 tokens) | 8-15 条 |
| `USER.md` | 用户档案（偏好、沟通风格、期望） | 1,375 chars (~500 tokens) | 5-10 条 |

**存储位置**：`~/.hermes/memories/` 或 `$HERMES_HOME/memories/`

## 冻结快照机制

### 工作原理

```
会话启动
    │
    ▼
读取磁盘文件 (MEMORY.md + USER.md)
    │
    ▼
安全扫描 + 截断处理
    │
    ▼
注入系统提示词（冻结快照）
    │
    ▼
全程保持不变（保留前缀缓存）
```

**关键特性**：
- **冻结快照模式**：会话开始时一次性加载，中途不更新
- **即时持久化**：Agent 通过 memory tool 更改时立即写入磁盘
- **下次生效**：更改将在下一个新会话中可见

### 实际影响示例

```python
# Session 1 开始时：
# MEMORY.md 包含："User prefers dark mode"

# 用户在 Session 1 中说：
"I actually switched to light mode recently"

# Agent 执行：
memory(action="replace", target="user",
       old_text="dark mode",
       content="User prefers light mode in VS Code")

# ✅ Tool 返回：Success - Updated on disk
# ⚠️ 但 Session 1 的系统提示词仍显示旧值！

# Session 2 开始时：
# 系统提示词将显示更新后的值 ✅
```

## Memory Tool 操作接口

Agent 使用 `memory` tool 进行三种操作：

### 操作 1：add（添加新条目）

```python
memory(
    action="add",
    target="memory",      # "memory" 或 "user"
    content="User's project uses Rust with Axum framework"
)
```

**何时使用 add**：
- ✅ 用户首次表达偏好："我更喜欢 TypeScript"
- ✅ 发现环境事实："这台机器运行 Ubuntu 22.04"
- ✅ 学到新经验："Docker 命令不需要 sudo"
- ✅ 完成重要任务："2026-01-15 完成 MySQL 到 PostgreSQL 迁移"

### 操作 2：replace（替换现有条目）

```python
memory(
    action="replace",
    target="memory",
    old_text="dark mode",              # 唯一子字符串
    content="User prefers light mode in VS Code, dark mode in terminal"
)
```

**匹配规则**：
- `old_text` 只需是能唯一标识一条目的短子串
- 如果匹配多条目，返回错误要求更具体的匹配

**高级用法 - 部分更新**：
```python
# 场景：只想修改编辑器偏好，保留其他设置
memory(
    action="replace",
    target="user",
    old_text="dark mode in all editors",
    content="light mode in VS Code, dark mode in terminal"
)
```

### 操作 3：remove（删除条目）

```python
memory(
    action="remove",
    target="user",
    old_text="dislikes verbose explanations"   # 要删除条目的唯一标识
)
```

**何时使用 remove**：
- 信息过时：项目已迁移到新框架，删除旧框架相关记忆
- 信息错误：记录了错误的环境信息
- 不再相关：临时任务已完成，清理一次性信息
- 容量管理：为更重要信息腾出空间

## 内容分类指南

### MEMORY.md 应该保存（Agent 的个人笔记）

| 类别 | 示例 |
|------|------|
| 环境事实 | OS 版本、已安装工具、项目路径 |
| 项目约定 | 缩进风格、命名规范、框架选择 |
| 工具特性 | 发现的 quirks 和 workarounds |
| 已完成任务 | 重要里程碑、迁移记录 |
| 有效技巧 | 经过验证的最佳实践 |

### USER.md 应该保存（用户档案）

| 类别 | 示例 |
|------|------|
| 身份信息 | 姓名、角色、时区 |
| 沟通偏好 | 简洁 vs 详细、格式偏好 |
| 习惯禁忌 | pet peeves、应避免的事项 |
| 工作习惯 | 常用工作流、技术熟练度 |

### 不应该保存的内容

❌ 太模糊的信息："用户问了 Python 问题"
❌ 容易重新发现的事实："Python 3.12 支持 f-string 嵌套"
❌ 大量原始数据：代码块、日志、数据表
❌ 会话临时信息：临时文件路径、一次性调试上下文
❌ 已在上下文文件中的内容：SOUL.md / AGENTS.md 信息

## 容量管理策略

### 当 Memory 满时的处理流程

```
尝试添加新条目
    │
    ▼
检查剩余空间
    │
    ├── 有空间 → 直接添加
    │
    └── 空间不足
            │
            ▼
        智能合并策略：
        1. 合并相似条目
        2. 删除过时信息
        3. 压缩冗余描述
        4. 保留高价值信息
```

### 容量规划建议

| Store | 限制 | 建议策略 | 目标使用率 |
|-------|------|---------|-----------|
| memory | 2,200 chars | 优先保存环境和项目相关事实 | 60-80% |
| user | 1,375 chars | 只保存稳定的用户偏好特征 | 60-80% |

### 字符预算分配示例（MEMORY.md 2,200 chars）

```
项目环境信息：~600 chars (27%)
├── 技术栈描述：200 chars
├── 目录结构：150 chars
└── 部署环境：250 chars

约定和规范：~800 chars (36%)
├── 编码风格：300 chars
├── Git 工作流：250 chars
└── 测试策略：250 chars

经验和教训：~500 chars (23%)
├── 近期完成的重要工作：200 chars
├── 学到的技巧：200 chars
└── 已知问题：100 chars

缓冲空间：~300 chars (14%)
└── 用于紧急或高价值新信息
```

## 使用示例

### 示例 1：首次配置用户偏好

```bash
# 场景：用户表达了对简洁回复的偏好
# Agent 自动执行：
memory(action="add", target="user",
       content="Prefers concise responses, dislikes verbose explanations")
```

### 示例 2：记录项目环境

```bash
# 场景：发现项目使用特定技术栈
memory(action="add", target="memory",
       content="Project at ~/code/myapi uses Rust + Axum + SQLx")
```

### 示例 3：更新过时信息

```bash
# 场景：用户改变了编辑器偏好
memory(action="replace", target="memory",
       old_text="VS Code",
       content="User switched to Neovim as primary editor since 2026-02")
```

### 示例 4：记录教训

```bash
# 场景：踩了坑
memory(action="add", target="memory",
       content="⚠️ PITFALL: Don't use `apt install python3-pip` on Ubuntu 22.04 "
               "- it installs broken pip. Always use `get-pip.py` instead. "
               "Discovered on 2026-02-20 after 2 hours debugging.")
```

## 故障排除

### 问题 1：更改没有立即生效

**症状**：执行了 memory replace/remove，但 Agent 行为没变

**原因**：冻结快照机制 - 更改在下次会话才生效

**解决方案**：
1. 确认更改已写入磁盘（检查 tool 返回的 current state）
2. 启动新会话验证更改
3. 如果仍无效，检查是否有更高优先级的上下文文件覆盖

### 问题 2：字符限制错误

**症状**：`"Would exceed character limit"` 错误

**解决策略**：
1. **短期**：删除最低价值条目
2. **中期**：合并相似条目
3. **长期**：重新评估什么值得保存

### 问题 3：子字符串匹配失败

**症状**：`"Substring matches multiple entries"` 错误

**解决方案**：
```python
# ❌ 太模糊
old_text="uses"

# ✅ 更具体
old_text="uses Axum web framework"

# ✅ 最具体（包含更多上下文）
old_text="Uses Axum web framework with SQLx database"
```

## 资源索引
- **官方文档**：https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
- **母技能**：[SKILL.md](../SKILL.md) - 完整技能体系概览
- **关联子技能**：[memory-layered](../memory-layered/) - 五层记忆架构（高级）

## 注意事项
- Memory 有严格字符限制，只保存高价值信息
- 不要手动编辑 Memory 文件，应让 Agent 通过 memory tool 管理
- 不要存储敏感信息（密码、密钥）
- 定期审查内容，删除过时条目，合并相似信息
