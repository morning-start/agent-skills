# AGENTS.md 反模式（22个）

> 本文档列出编写 AGENTS.md 时应避免的 22 个反模式，分为**内容反模式**（12个）、**结构反模式**（6个）、**维护反模式**（4个）三类，每个反模式都配有检测方法和修复建议。

---

## 反模式总览

```
┌─────────────────────────────────────────────────────┐
│               22 个反模式                            │
├──────────────┬──────────┬───────────────────────────┤
│ 类别          │ 数量      │ 影响程度                   │
├──────────────┼──────────┼───────────────────────────┤
│ 内容反模式     │ 12 个    │ ★★★★★ (严重影响质量)       │
│ 结构反模式     │ 6 个     │ ★★★☆☆ (影响可读性)         │
│ 维护反模式     │ 4 个     | ★★☆☆☆ (影响可持续性)       │
└──────────────┴──────────┴───────────────────────────┘
```

**扣分规则**: 每检出 1 个反模式扣 **1-2 分**（质量检查总分为 100 分），上限 **-20 分**。

---

## 一、内容反模式（12个）

这些反模式直接影响 AGENTS.md 的**实用性和可靠性**。

---

### AP-C1: 教程化倾向

**定义**: 将 AGENTS.md 写成教程或说明书，而非操作指南。

**错误示例** ❌:
```markdown
## MoonBit 简介
MoonBit 是一个由张宏波博士团队开发的现代化编程语言。
它设计之初就考虑了 WebAssembly 作为首要目标，
同时也支持编译到 JavaScript 和 Native 代码。
MoonBit 拥有强大的类型系统，包括泛型编程、
Trait 系统、方法调用等先进特性...

（200+ 字的背景介绍，Agent 并不需要这些知识）
```

**正确示例** ✅:
```markdown
## 身份与角色
你是 MoonBit 语言专家。当用户提及 MoonBit 任务时：
- 优先使用官方推荐的惯用法
- 遵循 trait-based 设计模式
- 注意两层级可变性语义
```

**检测方法**:
```bash
# 检查教程化词汇
tutorial_count=$(grep -ciE "(^## .*简介|^### .*介绍|what is|background|overview)" AGENTS.md)
if [ $tutorial_count -gt 2 ]; then
  echo "⚠️ 检测到教程化倾向 (${tutorial_count}处)"
fi
```

**修复方案**:
1. 删除所有"XX是什么"的介绍段落
2. 将背景知识移入 `references/background.md`
3. 替换为"你应该怎么做"的行动指令

**严重程度**: 🔴 **高**（影响 Agent 的启动效率）

---

### AP-C2: 冗余啰嗦

**定义**: 使用过多的文字表达简单的意思，信息密度低。

**错误示例** ❌:
```markdown
## 关于代码格式化的重要性

在我们的项目中，保持代码格式的一致性是非常重要的。
因为如果代码格式不一致的话，会给代码审查带来很大的困难，
同时也会影响代码的可读性和可维护性。
所以我们强烈建议所有的开发者在使用编辑器的时候，
都开启自动格式化功能，这样可以大大提高代码的一致性...
（150字，核心意思只有一句："开启自动格式化"）
```

**正确示例** ✅:
```markdown
## 格式化要求
- **必须**: 保存时自动格式化（EditorConfig + Prettier）
- **禁止**: 手动调整格式（除非有特殊原因）
- **检查**: CI 会拒绝未格式化的 PR
```

**检测方法**:
```bash
# 检查超长段落
awk '/^$/{if(length(p)>300) print NR-length(p), "长段落("length(p)"字)"; p=""} {p=p"\n"$0} END{if(length(p)>300) print NR-length(p), "长段落("length(p)"字)"}' AGENTS.md
```

**修复方案**:
1. 用要点列表替代段落
2. 删除过渡词（"此外"、"因此"、"值得注意的是"）
3. 用表格呈现结构化信息

**严重程度**: 🟡 **中**（浪费 Token，降低效率）

---

### AP-C3: 过于抽象

**定义**: 规则或指导过于抽象，缺乏具体示例，难以执行。

**错误示例** ❌:
```markdown
## 编码规范
- 写出清晰的代码
- 遵循最佳实践
- 保持代码简洁
- 注重性能优化
```

**正确示例** ✅:
```markdown
## 编码规范

| # | 规则 | ✅ 正确做法 | ❌ 错误做法 | 检测方式 |
|---|------|------------|------------|---------|
| R1 | 函数单一职责 | 每个函数只做一件事 | 函数 > 30 行 | 代码审查 |
| R2 | 命名语义化 | `fetch_user_by_id(id)` | `getData(x)` | Lint 规则 |
| R3 | 早返回 | 错误情况优先 return | 深层嵌套 if | Code Review |
```

**检测方法**:
- 统计"适当"、"合理"、"应该"等模糊词汇的出现次数
- 如果 > 3 次，则存在抽象化问题

**修复方案**:
1. 为每条规则添加正反例对比
2. 提供可量化的检测方式
3. 给出具体的命令或工具

**严重程度**: 🔴 **高**（Agent 无法准确执行）

---

### AP-C4: 信息过载

**定义**: 单个章节包含过多信息，超过认知负荷限制。

**错误示例** ❌:
```markdown
## 编码规范（120行的巨型章节）

### 1. 命名规范（20行）
（详细的命名规则说明）

### 2. 格式化要求（15行）
（缩进、空格、换行规则）

### 3. 注释规范（15行）
（何时写注释、注释格式）

### 4. 错误处理（20行）
（错误类型、日志级别）

### 5. 性能要求（20行）
（时间复杂度、空间复杂度）

### 6. 安全要求（15行）
（输入验证、SQL注入防护）

...（还有更多）
```

**正确示例** ✅:
```markdown
## 编码规范（30行的精简版）

### 核心规则速查
| # | 规则 | 一句话 |
|---|------|--------|
| R1 | snake_case | 函数/变量命名 |
| R2 | 4空格缩进 | 统一格式 |
| R3 | Early Return | 减少嵌套 |

→ 详见 [编码规范完整版](skills/coding-standards/SKILL.md)
```

**检测方法**:
```bash
# 检查超长章节
awk '/^## /{if(title && (NR-title_start)>80) print title": "(NR-title_start)"行"; title=$0; title_start=NR} END{if(title&&(NR-title_start)>80) print title": "(NR-title_start)"行"}' AGENTS.md
```

**修复方案**:
1. 将 > 50 行的章节拆分为子技能
2. 主文件只保留摘要（< 30 行）
3. 详细内容放入 `skills/` 或 `references/`

**严重程度**: 🟡 **中**（影响查找效率）

---

### AP-C5: 缺少边界定义

**定义**: 只说明"做什么"，不说明"不做什么"，导致 Agent 越权。

**错误示例** ❌:
```markdown
## 身份与角色
你是一个全栈开发专家，可以帮助用户解决各种技术问题。
```

**正确示例** ✅:
```markdown
## 身份与角色
你是 React 前端专家。

### ✅ 你擅长
- React 组件开发和优化
- Redux/ Zustand 状态管理
- React Router 路由设计
- Tailwind CSS 样式定制

### ❌ 你不负责
- 后端 API 设计（引导到 backend agent）
- DevOps/CI 配置（引导到 devops agent）
- 数据库查询优化（引导到 DBA）
```

**检测方法**:
```bash
# 检查是否有边界定义
if ! grep -qiE "(不负责|不擅长|超出范围|out of scope)" AGENTS.md; then
  echo "⚠️ 缺少边界定义"
fi
```

**修复方案**:
1. 添加"你不负责"章节
2. 对于越权请求，给出引导建议

**严重程度**: 🟠 **中高**（可能导致错误建议）

---

### AP-C6: 规则模糊

**定义**: 使用模棱两可的词汇，无法客观判断是否遵守。

**错误示例** ❌:
```markdown
- 代码应该保持整洁
- 函数长度适当即可
- 注释要写得合理
- 性能尽量优化
```

**正确示例** ✅:
```markdown
- 函数长度 < 30 行（强制，CI 检查）
- 注释解释"为什么"而非"做什么"（Code Review 标准）
- API 响应时间 < 200ms (P95)（性能基线）
```

**检测方法**:
```bash
# 检查模糊词汇
fuzzy_words=$(grep -ioE "(适当|合理|应该|尽量|尽可能|良好|整洁)" AGENTS.md | wc -l)
if [ $fuzzy_words -gt 3 ]; then
  echo "⚠️ 发现 ${fuzzy_words} 个模糊词汇"
fi
```

**修复方案**:
1. 将模糊词替换为**可量化指标**
2. 提供**检测工具或命令**
3. 给出**通过/不通过**的二进制判断标准

**严重程度**: 🔴 **高**（规则无法执行）

---

### AP-C7: 示例不可用

**定义**: 代码示例无法在实际环境中运行，或省略关键部分。

**错误示例** ❌:
```python
// 这是一个简单的函数
def process(data):
    # ... 处理逻辑 ...
    return result
```

**正确示例** ✅:
```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def process_user_data(user_id: int) -> Optional[dict]:
    """处理用户数据，返回处理结果或 None（失败时）"""
    try:
        user = fetch_user_from_db(user_id)
        if not user:
            logger.warning(f"User {user_id} not found")
            return None
        
        result = {
            "id": user["id"],
            "name": user["name"].strip(),
            "email": user["email"].lower(),
        }
        
        logger.info(f"Successfully processed user {user_id}")
        return result
    
    except Exception as e:
        logger.error(f"Failed to process user {user_id}: {e}")
        return None
```

**检测方法**:
- 人工审查代码示例
- 尝试在本地环境运行（如果可行）

**修复方案**:
1. 补全导入语句和类型注解
2. 添加错误处理逻辑
3. 包含真实的业务逻辑（非占位符）

**严重程度**: 🟡 **中**（降低可信度）

---

### AP-C8: 过时信息

**定义**: 包含已废弃的 API、旧版本特性或不准确的描述。

**错误示例** ❌:
```markdown
## 安装
使用 npm install react@16 安装 React 16
# React 16 已于 2023 年停止维护
```

**正确示例** ✅:
```markdown
## 安装
```bash
npm install react@19
npm install react-dom@19
```
**要求**: React 18+ (推荐 19), TypeScript 5.0+
```

**检测方法**:
```bash
# 检查可能的过时版本号
grep -oE "[a-z]+@\d+\.\d+" AGENTS.md | while read pkg; do
  echo "检查包版本: ${pkg}"
done
```

**修复方案**:
1. 定期审核第三方依赖版本
2. 移除已废弃特性的描述
3. 添加"当前适用于"版本声明

**严重程度**: 🔴 **高**（导致错误操作）

---

### AP-C9: 技术错误

**定义**: 包含事实性的技术错误，误导 Agent。

**错误示例** ❌:
```markdown
# JavaScript 中 == 和 === 没有区别
# （这是错误的！）
```

**正确示例** ✅:
```markdown
## 比较运算符
- **必须使用** `===` (严格相等)
- **禁止使用** `==` (宽松相等，会导致类型转换)
```

**检测方法**:
- 人工技术审查
- 社区反馈（Issue/PR）

**修复方案**:
1. 立即修正错误
2. 在版本历史中记录修正
3. 如有必要，发送更正通知

**严重程度**: 🔴 **高**（严重误导）

---

### AP-C10: 语言风格不一致

**定义**: 中英文混用不规范，或者同一概念有多种表达方式。

**错误示例** ❌:
```markdown
## Coding Standard（编码规范）
- function length should be reasonable（函数长度应当合理）
- 使用 snake_case 命名（use snake_case for naming）
- Error handling is important（错误处理很重要）
```

**正确示例** ✅:
```markdown
## 编码规范（Coding Standards）
- 函数长度 < 30 行
- 使用 snake_case 命名
- 错误处理优先（Early Return）
```

**检测方法**:
- 统一中英文比例（建议统一用中文，技术术语保留英文）

**修复方案**:
1. 确定主导语言（中文 or 英文）
2. 技术术语保留英文原文
3. 统一翻译风格

**严重程度**: 🟢 **低**（影响可读性，但不影响功能）

---

### AP-C11: 缺乏优先级

**所有内容同等重要**，无法区分核心和边缘。

**错误示例** ❌:
```markdown
## 规则列表
1. 使用 4 空格缩进
2. 函数命名用 snake_case
3. 每行不超过 120 字符
4. 变量必须有类型注解
5. 导入按字母排序
6. 注释使用英文
7. 错误要用自定义类型
8. 日志要用结构化格式
9. 测试覆盖率 > 80%
10. 不能用 any 类型
...（20条规则，没有优先级区分）
```

**正确示例** ✅:
```markdown
## 编码规范

### 强制规则（必须遵守，CI 会检查）
| # | 规则 | 检测方式 |
|---|------|---------|
| R1 | 禁止 `any` 类型 | tsc --strict |
| R2 | 函数 < 30 行 | ESLint rule |
| R3 | 测试覆盖率 > 80% | Coverage 工具 |

### 推荐惯例（强烈建议，Code Review 关注）
| # | 惯例 | 理由 |
|---|------|------|
| S1 | 4 空格缩进 | 统一风格 |
| S2 | snake_case 命名 | Python 惯例 |
| S3 | 结构化日志 | 便于检索 |

### 个人偏好（可选，不强求）
- 导入按字母排序
- 注释使用英文
```

**检测方法**:
- 检查是否有"强制/推荐/可选"的分层标记

**修复方案**:
1. 将规则分为 2-3 个优先级层级
2. 标记每个规则的强制程度
3. 提供不同层级的检测方式

**严重程度**: 🟡 **中**（Agent 无法判断重点）

---

### AP-C12: 无决策树

**复杂场景缺少判断逻辑**，只有平铺的列表。

**错误示例** ❌:
```markdown
## 错误处理
- 网络错误: 重试
- 权限错误: 返回 403
- 参数错误: 返回 400
- 服务器错误: 重试
- 超时错误: 重试
```

**正确示例** ✅:
```markdown
## 错误处理决策树

遇到错误?
    │
    ├── 客户端错误 (4xx)?
    │   ├── 400 Bad Request → 验证输入，返回友好提示
    │   ├── 401 Unauthorized → 刷新 Token，重试 1 次
    │   ├── 403 Forbidden → 记录日志，通知管理员
    │   └── 404 Not Found → 返回空或默认值
    │
    └── 服务器错误 (5xx)?
        ├── 502/503/504 → 指数退避重试 (1s/2s/4s)，最多 3 次
        ├── 500 Internal Error → 固定间隔重试 (1s)，最多 2 次
        └── 其他 5xx → 不重试，上报监控
```

**检测方法**:
- 检查是否有"如果...则..."的条件逻辑
- 如果全是平行列表，则缺少决策树

**修复方案**:
1. 识别多分支的场景
2. 绘制 ASCII 决策树
3. 覆盖边界情况和默认分支

**严重程度**: 🟡 **中**（复杂场景处理不当）

---

## 二、结构反模式（6个）

这些反模式影响 AGENTS.md 的**可读性和可维护性**。

---

### AP-S1: 缺少前言区

**定义**: 没有 YAML frontmatter，缺少元数据。

**错误示例** ❌:
```markdown
# 项目 AGENTS.md

这是一个项目的 Agent 配置文件...
```

**正确示例** ✅:
```yaml
---
name: project-agents
version: v1.0.0
author: team-name
description: 一句话描述
tags: [tag1, tag2, tag3]
---

# 项目 AGENTS.md
...
```

**检测方法**:
```bash
if ! head -1 AGENTS.md | grep -q "^---$"; then
  echo "❌ 缺少 YAML 前言区"
fi
```

**修复方案**:
添加标准的 YAML frontmatter（见 [best-practices.md](best-practices.md)#SP-1）

**严重程度**: 🔴 **高**（Agent 无法快速解析元数据）

---

### AP-S2: 章节过多

**定义**: 一级章节（##）数量过多，导致导航困难。

**阈值**:
- Type A/B: > 10 个章节
- Type C/D/E: > 15 个章节

**检测方法**:
```bash
chapter_count=$(grep -c "^## " AGENTS.md)
echo "一级章节数: ${chapter_count}"
if [ $chapter_count -gt 15 ]; then
  echo "⚠️ 章节过多，考虑合并或拆分"
fi
```

**修复方案**:
1. 合并相关的小章节
2. 将低频内容移入子技能
3. 使用分组标题（### ）组织

**严重程度**: 🟡 **中**（影响导航效率）

---

### AP-S3: 层级混乱

**定义**: Markdown 标题层级跳级（如 ## 直接跳到 ####）。

**错误示例** ❌:
```markdown
## 第一章
#### 1.1 小节  ← 跳过了 ###
###### 1.1.1 详情 ← 又跳过了 ####
```

**正确示例** ✅:
```markdown
## 第一章
### 1.1 小节
#### 1.1.1 详情
```

**检测方法**:
```bash
# 检查层级跳跃
prev_level=0
grep -n "^#+ " AGENTS.md | while read line; do
  level=$(echo "$line" | grep -o "^#" | wc -c)
  line_num=$(echo "$line" | cut -d: -f1)
  if [ $level -gt $((prev_level + 1)) ] && [ $prev_level -gt 0 ]; then
    echo "⚠️ Line ${line_num}: 层级跳跃 (${prev_level} → ${level})"
  fi
  prev_level=$level
done
```

**修复方案**:
重新规划层级结构，确保逐级递进

**严重程度**: 🟢 **低**（影响渲染效果）

---

### AP-S4: 缺少触发条件

**定义**: 未说明"何时应该使用此 AGENTS.md"。

**检测方法**:
```bash
if ! grep -qiE "(触发|激活|when|condition|trigger)" AGENTS.md; then
  echo "❌ 缺少触发条件"
fi
```

**修复方案**:
添加"触发条件"章节（见 [best-practices.md](best-practices.md)#SP-2）

**严重程度**: 🟠 **中高**（Agent 不知道何时激活）

---

### AP-S5: 缺少导航

**定义**: 大文件（> 150 行）没有目录或快速导航。

**检测方法**:
```bash
lines=$(wc -l < AGENTS.md)
has_toc=$(grep -qcE "(^## 目录|^## 快速开始|^## 导航)" AGENTS.md)
if [ $lines -gt 150 ] && [ $has_toc -eq 0 ]; then
  echo "⚠️ 大文件缺少导航"
fi
```

**修复方案**:
添加目录或快速链接块（见 [best-practices.md](best-practices.md)#SP-8）

**严重程度**: 🟡 **中**（影响查找效率）

---

### AP-S6: 单体膨胀

**定义**: 文件超过 500 行且未拆分为子技能或参考文档。

**检测方法**:
```bash
lines=$(wc -l < AGENTS.md)
if [ $lines -gt 500 ]; then
  has_subskills=$(ls -d skills/*/SKILL.md 2>/dev/null | wc -l)
  if [ $has_subskills -eq 0 ]; then
    echo "❌ 文件过长 (${lines}行) 且未拆分"
  fi
fi
```

**修复方案**:
1. 识别 > 50 行的章节
2. 提取到 `skills/{chapter}/SKILL.md`
3. 主文件保留摘要 + 链接

**严重程度**: 🟡 **中**（Token 效率低，加载慢）

---

## 三、维护反模式（4个）

这些反模式影响 AGENTS.md 的**长期可持续性**。

---

### AP-M1: 无版本号

**定义**: 前言区缺少 version 字段，无法追踪演化历史。

**检测方法**:
```bash
if ! grep -q "^version:" AGENTS.md; then
  echo "❌ 缺少版本号"
fi
```

**修复方案**:
添加 `version: v1.0.0` 到前言区

**严重程度**: 🟠 **中高**（无法追踪变更）

---

### AP-M2: 无更新记录

**定义**: 没有版本历史或 CHANGELOG，不知道何时改了什么。

**修复方案**:
添加版本历史章节（见 [best-practices.md](best-practices.md)#SP-9）

**严重程度**: 🟡 **中**（协作时易冲突）

---

### AP-M3: 硬编码路径

**定义**: 包含绝对路径或特定用户名，不具备移植性。

**错误示例** ❌:
```markdown
- 配置文件位于 `/home/john/.config/app/settings.json`
- 使用 `D:\Projects\my-app` 作为项目根目录
```

**正确示例** ✅:
```markdown
- 配置文件位于 `{PROJECT_ROOT}/config/settings.json`
- 或通过环境变量 `{APP_CONFIG_PATH}` 指定
```

**检测方法**:
```bash
# 检查绝对路径
grep -nE "/home/[a-z]+/|C:\\\\Users\\\\" AGENTS.md
```

**修复方案**:
1. 使用相对路径
2. 使用环境变量占位符
3. 使用 `{PROJECT_ROOT}` 等通用标记

**严重程度**: 🟢 **低**（影响移植性）

---

### AP-M4: 缺少所有者

**定义**: 没有 author 或 maintainer 信息，不清楚谁负责维护。

**修复方案**:
添加 `author: name/team` 到前言区

**严重程度**: 🟢 **低**（影响责任认定）

---

## 反模式检测工具

### 一键检测脚本

```bash
#!/bin/bash
# agents-md-lint.sh: AGENTS.md 反模式快速检测

FILE="${1:-AGENTS.md}"

echo "=== AGENTS.md 反模式检测 ==="
echo "文件: ${FILE}"
echo "行数: $(wc -l < ${FILE})"
echo ""

score=100
warnings=()
errors=()

# 检查 AP-S1: 前言区
if ! head -1 "${FILE}" | grep -q "^---$"; then
  errors+=("❌ AP-S1: 缺少 YAML 前言区")
  score=$((score - 2))
fi

# 检查 AP-C1: 教程化
tutorial=$(grep -ciE "(^## .*简介|^### .*介绍|what is)" "${FILE}")
if [ $tutorial -gt 2 ]; then
  warnings+=("⚠️ AP-C1: 可能存在教程化倾向 (${tutorial}处)")
  score=$((score - 1))
fi

# 检查 AP-S6: 单体膨胀
lines=$(wc -l < "${FILE}")
if [ $lines -gt 500 ]; then
  warnings+=("⚠️ AP-S6: 文件较长 (${lines}行，建议 < 500)")
  score=$((score - 1))
fi

# 检查 AP-M1: 版本号
if ! grep -q "^version:" "${FILE}"; then
  errors+=("❌ AP-M1: 缺少版本号")
  score=$((score - 1))
fi

# 输出结果
echo ""
echo "=== 检测结果 ==="
echo "得分: ${score}/100"

if [ ${#errors[@]} -gt 0 ]; then
  echo ""
  echo "❌ 错误 (${#errors[@]}项):"
  for err in "${errors[@]}"; do
    echo "  ${err}"
  done
fi

if [ ${#warnings[@]} -gt 0 ]; then
  echo ""
  echo "⚠️ 警告 (${#warnings[@]}项):"
  for warn in "${warnings[@]}"; do
    echo "  ${warn}"
  done
fi

if [ $score -ge 90 ]; then
  echo ""
  echo "✅ 总体评价: A级 (优秀)"
elif [ $score -ge 75 ]; then
  echo ""
  echo "✅ 总体评价: B级 (良好)"
elif [ $score -ge 60 ]; then
  echo ""
  echo "⚠️ 总体评价: C级 (及格)"
else
  echo ""
  echo "❌ 总体评价: D级 (需改进)"
fi
```

**使用方法**:
```bash
chmod +x agents-md-lint.sh
./agents-md-lint.sh AGENTS.md
```

---

## 总结：反模式优先级矩阵

| 反模式ID | 类别 | 严重程度 | 发生频率 | 修复难度 | 优先级 |
|---------|------|---------|---------|---------|--------|
| AP-C1 | 内容 | 🔴 高 | 高频 | 低 | **P0** |
| AP-C3 | 内容 | 🔴 高 | 中频 | 中 | **P0** |
| AP-C6 | 内容 | 🔴 高 | 高频 | 低 | **P0** |
| AP-C8 | 内容 | 🔴 高 | 低频 | 低 | **P0** |
| AP-C9 | 内容 | 🔴 高 | 低频 | 低 | **P0** |
| AP-S1 | 结构 | 🔴 高 | 中频 | 低 | **P0** |
| AP-S4 | 结构 | 🟠 中高 | 中频 | 低 | **P1** |
| AP-C5 | 内容 | 🟠 中高 | 中频 | 低 | **P1** |
| AP-M1 | 维护 | 🟠 中高 | 高频 | 低 | **P1** |
| AP-C2 | 内容 | 🟡 中 | 高频 | 中 | **P1** |
| AP-C4 | 内容 | 🟡 中 | 中频 | 中 | **P1** |
| AP-C11 | 内容 | 🟡 中 | 高频 | 低 | **P1** |
| AP-C12 | 内容 | 🟡 中 | 中频 | 中 | **P2** |
| AP-C7 | 内容 | 🟡 中 | 中频 | 中 | **P2** |
| AP-S6 | 结构 | 🟡 中 | 中频 | 中 | **P2** |
| AP-S2 | 结构 | 🟡 中 | 低频 | 中 | **P2** |
| AP-S5 | 结构 | 🟡 中 | 中频 | 低 | **P2** |
| AP-C10 | 内容 | 🟢 低 | 低频 | 低 | **P3** |
| AP-M2 | 维护 | 🟡 中 | 高频 | 低 | **P2** |
| AP-M3 | 维护 | 🟢 低 | 低频 | 低 | **P3** |
| AP-M4 | 维护 | 🟢 低 | 中频 | 低 | **P3** |
| AP-S3 | 结构 | 🟢 低 | 低频 | 低 | **P3** |

---

**文档版本**: v1.0.0  
**最后更新**: 2026-05-17  
**相关文档**: [best-practices.md](best-practices.md), [5-quality-check](../skills/5-quality-check/SKILL.md)
