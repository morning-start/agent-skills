---
name: 5-quality-check
version: v1.0.0
author: book-skills
description: AGENTS.md质量检查与验证 — 通过6大维度22项检查清单自动检测问题，输出结构化的质量报告和修复建议，确保符合生产级标准
tags: [quality-assurance, validation, checklist, anti-patterns, lint]
dependency:
  parent: agents-writer
---

# ⑤ 质量检查与验证

## 任务目标

对已有的或新编写的 AGENTS.md 进行**全面质量检查**，通过 6 大维度 22 项检查清单自动检测问题，输出结构化的质量报告和修复建议。

## 触发条件

当用户说以下任一话术时激活：
- "检查这个AGENTS.md"
- "是否符合规范"
- "质量验证"
- "帮我审查"
- "有什么问题"

## 检查维度总览

```
┌─────────────────────────────────────────────┐
│           质量检查 6 大维度                   │
├──────────┬──────────┬───────────────────────┤
│ 维度      │ 权重     │ 检查项数              │
├──────────┼──────────┼───────────────────────┤
│ ① 结构完整性 │ 20%      │ 4 项                 │
│ ② 内容质量  │ 25%      │ 6 项                 │
│ ③ 可操作性  │ 20%      │ 4 项                 │
│ ④ 格式规范  │ 15%      │ 4 项                 │
│ ⑤ 反模式检测 │ 10%      │ 22项（单独计分）      │
│ ⑥ Token效率 │ 10%      │ 3 项                 │
└──────────┴──────────┴───────────────────────┘
总分: 100分（不含反模式扣分）
反模式: 每个 -2 分（上限 -20 分）
```

## 操作步骤

### Step 1: 收集待检文件

```bash
# 定位文件
ls -la AGENTS.md .claude* .cursorrules 2>/dev/null

# 如果未指定，查找可能的 Agent 配置文件
find . -maxdepth 2 -name "AGENTS.md" -o -name ".claude*" -o -name ".cursorrules" 2>/dev/null

# 读取文件基本信息
wc -l AGENTS.md                    # 总行数
head -20 AGENTS.md                 # 前20行（查看前言区）
tail -20 AGENTS.md                 # 后20行（查看结尾）
```

### Step 2: 执行 6 维度检查

#### 维度 1: 结构完整性 (20分)

| # | 检查项 | 权重 | 通过标准 | 得分 |
|---|--------|------|---------|------|
| 1.1 | **前言区存在** | 5分 | YAML frontmatter 存在且 `---` 包裹 | ?/5 |
| 1.2 | **必需字段完整** | 5分 | name/version/description/tags 全部存在 | ?/5 |
| 1.3 | **章节层次清晰** | 5分 | 至少有 3 个 `##` 一级章节 | ?/5 |
| 1.4 | **整体连贯** | 5分 | 章节间有逻辑顺序，无突兀跳跃 | ?/5 |
| | **小计** | | | **?/20** |

**自动检测命令**：

```bash
# 检查前言区
if head -1 AGENTS.md | grep -q "^---$"; then echo "✅ 前言区存在"; else echo "❌ 缺少前言区"; fi

# 检查必需字段
for field in name version description tags; do
  if grep -q "^${field}:" AGENTS.md; then echo "✅ ${field} 存在"; else echo "❌ 缺少 ${field}"; fi
done

# 统计章节数
chapter_count=$(grep -c "^## " AGENTS.md)
echo "章节数: ${chapter_count}"
```

---

#### 维度 2: 内容质量 (25分)

| # | 检查项 | 权重 | 通过标准 | 得分 |
|---|--------|------|---------|------|
| 2.1 | **身份定义清晰** | 5分 | 不是泛泛的"AI助手"，有具体领域定位 | ?/5 |
| 2.2 | **触发条件明确** | 5分 | 清晰说明"何时激活"，含示例 | ?/5 |
| 2.3 | **意图路由存在** | 5分 | 有将用户请求映射到行为的机制 | ?/5 |
| 2.4 | **行动导向** | 5分 | 内容以"怎么做"为主，非教程式 | ?/5 |
| 2.5 | **无冗余信息** | 3分 | 无大段背景介绍或废话 | ?/3 |
| 2.6 | **专业性准确** | 2分 | 技术细节正确，无过时信息 | ?/2 |
| | **小计** | | | **?/25** |

**检测方法**：

```bash
# 检查是否是行动导向（而非教程）
tutorial_words=$(grep -ciE "(简介|介绍|什么是|how it works|background)" AGENTS.md)
action_words=$(grep -ciE "(执行|操作|步骤|命令|run|execute|step)" AGENTS.md)
echo "教程词汇: ${tutorial_words}, 行动词汇: ${action_words}"
if [ $action_words -gt $tutorial_words ]; then echo "✅ 行动导向"; else echo "⚠️ 偏向教程风格"; fi

# 检查意图路由
if grep -qiE "(意图|路由|intent|routing|trigger)" AGENTS.md; then echo "✅ 有意图路由"; else echo "❌ 缺少意图路由"; fi
```

---

#### 维度 3: 可操作性 (20分)

| # | 检查项 | 权重 | 通过标准 | 得分 |
|---|--------|------|---------|------|
| 3.1 | **指令可直接执行** | 7分 | 规则/命令无需额外解释就能用 | ?/7 |
| 3.2 | **示例真实可用** | 5分 | 代码示例能实际运行（或明确标注伪代码） | ?/5 |
| 3.3 | **有决策指引** | 4分 | 对模糊场景提供判断逻辑（如果...则...） | ?/4 |
| 3.4 | **错误处理覆盖** | 4分 | 包含常见问题的解决方案 | ?/4 |
| | **小计** | | | **?/20** |

**检测方法**：

```bash
# 统计可执行指令数量
executable_count=$(grep -cE '(`[^`]+`|→|- \*\*)' AGENTS.md)
echo "可执行指令数: ${executable_count}"

# 检查是否有代码块
code_blocks=$(grep -c '```' AGENTS.md)
echo "代码块数: $((${code_blocks} / 2))"

# 检查是否有条件判断
conditionals=$(grep -cE "(如果|当|若|if.*then|when)" AGENTS.md)
echo "条件判断语句: ${conditionals}"
```

---

#### 维度 4: 格式规范 (15分)

| # | 检查项 | 权重 | 通过标准 | 得分 |
|---|--------|------|---------|------|
| 4.1 | **Markdown 规范** | 5分 | 标题层级正确，列表格式统一 | ?/5 |
| 4.2 | **表格使用合理** | 4分 | 规则类内容用表格呈现 | ?/4 |
| 4.3 | **链接有效** | 3分 | 内部链接指向存在的文件 | ?/3 |
| 4.4 | **无语法错误** | 3分 | YAML/Markdown 无明显语法错误 | ?/3 |
| | **小计** | | | **?/15** |

**自动检测命令**：

```bash
# 检查 Markdown 层级（不应跳级）
grep -n "^#" AGENTS.md | head -20

# 检查链接有效性
links=$(grep -oP '\([^\)]+\)' AGENTS.md | grep -v '^http' | sed 's/[()]//g')
for link in $links; do
  if [ -f "$link" ]; then echo "✅ $link"; else echo "❌ 断链: $link"; fi
done

# 检查表格数量
table_count=$(grep -c '|.*|.*|' AGENTS.md)
echo "表格数: ${table_count}"
```

---

#### 维度 5: 反模式检测 (额外扣分，上限 -20分)

基于 [anti-patterns.md](../references/anti-patterns.md) 的 22 个反模式进行检测。

#### 5.1 内容反模式 (12个，每个 -1分)

| # | 反模式 | 检测关键词 | 扣分 |
|---|--------|-----------|------|
| AP-C1 | 教程化倾向 | "简介"、"什么是"、"背景介绍" | -1 |
| AP-C2 | 冗余啰嗦 | 单段 > 10 行 | -1 |
| AP-C3 | 过于抽象 | 缺少具体示例 | -1 |
| AP-C4 | 信息过载 | 单章节 > 80 行 | -1 |
| AP-C5 | 缺少边界 | 无"不做什么"说明 | -1 |
| AP-C6 | 规则模糊 | 使用"适当"、"合理"、"应该"等模糊词 > 3次 | -1 |
| AP-C7 | 示例不可用 | 代码无法实际运行 | -1 |
| AP-C8 | 过时信息 | 提到已废弃的API/版本 | -1 |
| AP-C9 | 技术错误 | 明显的技术性错误 | -1 |
| AP-C10 | 语言不一致 | 中英文混用不规范 | -1 |
| AP-C11 | 缺乏优先级 | 所有问题同等重要 | -1 |
| AP-C12 | 无决策树 | 复杂场景缺少判断逻辑 | -1 |

#### 5.2 结构反模式 (6个，每个 -1分)

| # | 反模式 | 检测特征 | 扣分 |
|---|--------|---------|------|
| AP-S1 | 缺少前言区 | 无 YAML frontmatter | -1 |
| AP-S2 | 章节过多 | > 15 个一级章节 | -1 |
| AP-S3 | 层级混乱 | 标题跳级（## → ####） | -1 |
| AP-S4 | 缺少触发条件 | 未说明何时激活 | -1 |
| AP-S5 | 缺少导航 | 大文件无目录/索引 | -1 |
| AP-S6 | 单体膨胀 | > 500 行且未拆分 | -1 |

#### 5.3 维护反模式 (4个，每个 -1分)

| # | 反模式 | 检测特征 | 扣分 |
|---|--------|---------|------|
| AP-M1 | 无版本号 | 前言区无 version 字段 | -1 |
| AP-M2 | 无更新记录 | 无版本历史/CHANGELOG | -1 |
| AP-M3 | 硬编码路径 | 绝对路径或特定用户名 | -1 |
| AP-M4 | 缺少所有者 | 无 author/maintainer 信息 | -1 |

**反模式得分计算**：

```bash
# 自动检测部分反模式（需人工确认）
echo "=== 反模式自动检测 ==="

# AP-C1: 教程化
if grep -qiE "(^## .*简介|^### .*介绍|what is)" AGENTS.md; then
  echo "⚠️ 可能存在教程化倾向 (AP-C1)"
fi

# AP-S1: 缺少前言区
if ! head -1 AGENTS.md | grep -q "^---$"; then
  echo "❌ 缺少前言区 (AP-S1)"
fi

# AP-S6: 单体膨胀
lines=$(wc -l < AGENTS.md)
if [ $lines -gt 500 ]; then
  echo "⚠️ 文件过长 (${lines}行)，考虑拆分 (AP-S6)"
fi

# AP-M1: 无版本号
if ! grep -q "^version:" AGENTS.md; then
  echo "❌ 缺少版本号 (AP-M1)"
fi
```

---

#### 维度 6: Token 效率 (10分)

| # | 检查项 | 权重 | 通过标准 | 得分 |
|---|--------|------|---------|------|
| 6.1 | **行数合理** | 4分 | 在类型推荐的范围内（见 type-classification.md） | ?/4 |
| 6.2 | **信息密度高** | 3分 | 平均每行 > 30 字符的有效信息 | ?/3 |
| 6.3 | **无重复内容** | 3分 | 无大段复制粘贴或循环引用 | ?/3 |
| | **小计** | | | **?/10** |

**Token 估算**：

```bash
# 行数统计
total_lines=$(wc -l < AGENTS.md)
echo "总行数: ${total_lines}"

# Token 估算（粗略：每行 ~3 token）
estimated_tokens=$((total_lines * 3))
echo "估算Token数: ~${estimated_tokens}"

# 信息密度（去除空行和注释后的平均字符数）
effective_lines=$(grep -v '^[[:space:]]*$' AGENTS.md | grep -v '^[[:space:]]*#' | wc -l)
avg_chars=$(awk '{print length}' AGENTS.md | awk '{s+=$1} END {print s/NR}')
echo "有效行数: ${effective_lines}, 平均行长: ${avg_chars}字符"

# 效率评级
if [ $estimated_tokens -lt 300 ]; then
  echo "✅ Token 效率: 优秀 (< 300)"
elif [ $estimated_tokens -lt 600 ]; then
  echo "✅ Token 效率: 良好 (300-600)"
elif [ $estimated_tokens -lt 1000 ]; then
  echo "⚠️ Token 效率: 一般 (600-1000)"
else
  echo "❌ Token 效率: 较低 (> 1000)，考虑精简"
fi
```

> 📖 详细的 Token 预算策略见 [token-budget.md](../references/token-budget.md)

### Step 3: 生成质量报告

#### 标准报告格式

```markdown
# 📋 AGENTS.md 质量检查报告

## 基本信息
- **文件**: {path/to/AGENTS.md}
- **行数**: {XXX} 行
- **估算Token**: ~{XXXX}
- **检查日期**: {date}
- **检查员**: agents-writer v1.0.0

## 总评分

| 维度 | 得分 | 满分 | 得分率 | 状态 |
|------|------|------|--------|------|
| ① 结构完整性 | XX | 20 | XX% | ✅/⚠️/❌ |
| ② 内容质量 | XX | 25 | XX% | ✅/⚠️/❌ |
| ③ 可操作性 | XX | 20 | XX% | ✅/⚠️/❌ |
| ④ 格式规范 | XX | 15 | XX% | ✅/⚠️/❌ |
| ⑤ 反模式扣分 | -XX | -20 | - | ⚠️/✅ |
| ⑥ Token效率 | XX | 10 | XX% | ✅/⚠️/❌ |
| **总分** | **XX** | **100** | **XX%** | **等级** |

### 等级定义
- **A级 (90-100)**: 优秀，可直接使用
- **B级 (75-89)**: 良好，有小问题需修复
- **C级 (60-74)**: 及格，有明显缺陷需改进
- **D级 (< 60)**: 不合格，需要重大修订

## 详细发现

### ✅ 通过项 ({count}项)
{list of passed items}

### ⚠️ 警告项 ({count}项)
{list of warnings with fix suggestions}

### ❌ 问题项 ({count}项)
{list of critical issues with fix suggestions}

## 反模式检测结果

### 检出的反模式 ({count}个)
| ID | 反模式 | 严重程度 | 位置 | 修复建议 |
|----|--------|---------|------|---------|
| AP-XX | {name} | 高/中/低 | Line XX | {suggestion} |

### 未检出的反模式 ({count}个)
（这些反模式未在此文件中发现，值得肯定）

## 修复建议（按优先级排序）

### P0: 必须修复（影响使用）
1. **{issue_1}**
   - 问题: {description}
   - 影响: {impact}
   - 修复方案: {fix}
   - 预估工作量: {time}

### P1: 应该修复（影响质量）
1. **{issue_2}**
   - ...

### P2: 建议修复（锦上添花）
1. **{issue_3}**
   - ...

## 下一步行动

- [ ] 修复 P0 问题（预计 {time}）
- [ ] 修复 P1 问题（预计 {time}）
- [ ] （可选）修复 P2 问题
- [ ] 重新运行质量检查验证修复效果
- [ ] （可选）进入 [⑥ 优化迭代](../skills/6-optimize-evolve/SKILL.md)

---

**报告生成时间**: {timestamp}
**工具版本**: agents-writer v1.0.0
```

### Step 4: 给出总体评价和改进路线图

#### 评价模板

```markdown
## 总体评价

### 一句话评价
{例如："这是一个结构完整的 AGENTS.md，但在行动导向性和 Token 效率方面还有提升空间"}

### 亮点 👍
1. {strength_1}
2. {strength_2}
3. {strength_3}

### 待改进 👎
1. {weakness_1}（影响: 高/中/低）
2. {weakness_2}（影响: 高/中/低）
3. {weakness_3}（影响: 高/中/低）

### 改进路线图

#### Phase 1: 紧急修复（1-2小时）
- [ ] {critical_fix_1}
- [ ] {critical_fix_2}
预期效果: 评分提升 {X} → {Y}

#### Phase 2: 质量提升（半天）
- [ ] {quality_improvement_1}
- [ ] {quality_improvement_2}
预期效果: 评分提升 {X} → {Y}

#### Phase 3: 优化迭代（持续）
- [ ] 进入 [⑥ 优化迭代](../skills/6-optimize-evolve/SKILL.md)
预期效果: 评分提升至 A 级并维持
```

## 快速检查模式

如果用户只需要**快速评估**（非全面检查）：

```bash
# 5分钟快速检查（仅核心项）
echo "=== 快速质量检查 ==="
echo "1. 行数: $(wc -l < AGENTS.md)"
echo "2. 有前言区: $(head -1 AGENTS.md | grep -c '^---$')"
echo "3. 有意图路由: $(grep -ciE '(意图|路由|intent|routing|trigger)' AGENTS.md)"
echo "4. 章节数: $(grep -c '^## ' AGENTS.md)"
echo "5. Token估算: ~$(($(wc -l < AGENTS.md) * 3))"
echo ""
echo "快速评级:"
if [ $(wc -l < AGENTS.md) -lt 100 ] && grep -q "^---$" AGENTS.md; then
  echo "✅ 基础质量合格（建议进行全面检查）"
else
  echo "⚠️ 需要改进（建议运行完整质量检查）"
fi
```

## 常见问题

**Q: 评分很低怎么办？**

A: 按照 P0 → P1 → P2 的优先级依次修复。通常修复前 3 个 P0 问题就能提升 10-15 分。

**Q: 反模式很多是不是很糟糕？**

A: 不一定。少量反模式（< 5个）是正常的，特别是早期版本。重点关注**高频影响**的反模式（如教程化、缺少触发条件）。

**Q: 质量检查会自动修复吗？**

A: **不会自动修复**。本技能只负责**检测和报告**，修复需要手动执行或调用 [③ 编写内容](../skills/3-write-content/SKILL.md) 重新生成问题章节。

**Q: 多久检查一次？**

A: 建议：
- **每次重大修改后**：立即检查
- **定期维护**：每月 1 次
- **版本发布前**：必须检查

## 注意事项

⚠️ **客观性**: 评分应基于可量化的事实，避免主观偏好。

⚠️ **上下文感知**: 同样的内容在不同类型的项目中可能有不同的评分标准（例如个人项目不需要像企业项目那么严格）。

⚠️ **建设性反馈**: 每个问题都必须附带**可操作的修复建议**，而不是仅仅指出问题。
