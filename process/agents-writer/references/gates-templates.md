# 门禁模板与检查方法

> 用于阶段 4（4-gate-check）的详细检查指南。每个门禁的具体检查命令、通过标准和修复方法。

---

## 执行检查命令

```bash
# 设置检查目标
TARGET="AGENTS.md"   # 或实际文件路径

# 基础检查
echo "=== 文件信息 ==="
wc -l $TARGET
echo ""

echo "=== YAML 前言区 ==="
head -20 $TARGET
echo ""

echo "=== 门禁标记统计 ==="
echo "HARD-GATE 数量: $(grep -c '<HARD-GATE>' $TARGET 2>/dev/null || echo 0)"
echo "GATE 数量: $(grep -c '<GATE>' $TARGET 2>/dev/null || echo 0)"
echo ""

echo "=== 禁止操作章节 ==="
echo "禁止/不允许数量: $(grep -cE '(禁止|不允许|不允许|不能|不要)' $TARGET 2>/dev/null || echo 0)"
echo ""

echo "=== 教程检测 ==="
echo "教程关键词数量: $(grep -ciE '(简介|介绍|什么是|what is|background|overview)' $TARGET 2>/dev/null || echo 0)"
```

---

## 每项门禁的详细检查

### G1: 产品定位清晰

**检查方法**：
```
grep -A5 "^## 核心原则" AGENTS.md
```
检查核心原则中是否有体现产品定位的规则，例如：
```
R1: 始终优先实现核心的数据处理功能，非核心的展示层优化可以延后
```

**常见问题**：没有与产品定位相关的原则，全是通用的"好代码"规则。

---

### G2: 目标用户明确

**检查方法**：通读全文，判断语气是否一致。

**语气判断指南**：
- **面向开发者**：可包含技术术语，可直接给出命令
- **面向 PM 或新手**：需要解释，"请"字开头
- **混用**：矛盾，需要统一

---

### G3: 功能边界定义

**检查方法**：
```
grep -cE "(禁止|不允许|不能|不要|never|don't)" AGENTS.md
```

如果结果 < 3，说明边界定义不够。

**完整的边界格式**：
```
### ❌ 禁止的操作
| 操作 | 原因 | 替代方案 |
```

检查重点：
- 每条禁止操作都有具体的路径或命令模式
- 都有"为什么禁止"的解释
- 都有替代方案（如果可以的话）

---

### G4: 安全检查完备

参考 [security-checklist.md](security-checklist.md) 的完整清单。

**检查方法**：根据项目画像的安全等级，检查对应的安全规则是否都覆盖了。

**最低要求**：
- 如果安全等级 ≥ 中：必须有 `<HARD-GATE>` 标记的安全红线
- 如果涉及用户数据：必须包含数据处理规则
- 如果涉及生产环境：必须包含部署操作规则

---

### G5: 架构正确反映

**检查命令**：
```bash
# 提取所有路径引用
grep -oP '`[^`]+`' AGENTS.md | grep -E '(/|\.)' | while read p; do
  actual_path=$(echo "$p" | sed 's/`//g')
  if [ -e "$actual_path" ] 2>/dev/null; then
    echo "✅ $actual_path"
  else
    echo "⚠️ $actual_path (可能不在当前目录)"
  fi
done
```

---

### G6: G13 行为层门禁

需要逐条通读 AGENTS.md，使用以下清单快速扫描：

```bash
echo "=== 行为层快速扫描 ==="
echo "G6 触发条件: description 是否有具体触发词？"
echo "G7 可执行性: 随机抽查 3 条规则"
echo "G8 红线: 有无 <HARD-GATE>？"
echo "G9 可操作性: 工作流步骤是否以动词开头？"
echo "G10 异常处理: 有无'不确定时提问'？"
echo "G11 优先级: 有无 P0/P1/P2？"
echo "G12 职责: 多 Agent 时职责是否不重叠？"
echo "G13 量化: 质量要求是否有数字阈值？"
```

---

### G14: 反模式扫描

**检查命令**：
```bash
# 反模式关键词扫描
ap_count=$(grep -ciE "(简介|介绍|什么是|what is|^#.*教程|background|overview|^# 快速开始)" AGENTS.md)
if [ $ap_count -gt 2 ]; then
  echo "⚠️ 可能包含教程化反模式，命中 $ap_count 次"
fi
```

完整反模式清单见 [anti-patterns.md](anti-patterns.md)。

---

### G17: Token 优化

**估算 Token 的方法**：
```bash
# 粗略估算
line_count=$(wc -l < AGENTS.md)
rough_token=$((line_count * 3))
echo "粗略 Token 估算: $rough_token"

# 如果超过 500 行
if [ $line_count -gt 500 ]; then
  echo "⚠️ 超过 500 行，建议拆分或压缩"
fi
```

---

## 验收报告模板

```yaml
summary:
  total_gates: 21
  passed: 0
  failed: 0
  pass_rate: "0%"

strategic_layer:
  - gate: "G1-产品定位"
    status: "⏳ 待检查"
    evidence: "-"
    fix: "-"
  - gate: "G2-目标用户"
    status: "⏳ 待检查"
    evidence: "-"
    fix: "-"
  - gate: "G3-功能边界"
    status: "⏳ 待检查"
    evidence: "-"
    fix: "-"
  - gate: "G4-安全检查"
    status: "⏳ 待检查"
    evidence: "-"
    fix: "-"
  - gate: "G5-架构正确性"
    status: "⏳ 待检查"
    evidence: "-"
    fix: "-"

behavior_layer:
  - gate: "G6-触发条件"
    status: "⏳ 待检查"
    evidence: "-"
    fix: "-"
  - gate: "G7-规则可执行"
    status: "⏳ 待检查"
    evidence: "-"
    fix: "-"
  - gate: "G8-红线清晰"
    status: "⏳ 待检查"
    evidence: "-"
    fix: "-"
  - gate: "G9-可操作性"
    status: "⏳ 待检查"
    evidence: "-"
    fix: "-"
  - gate: "G10-异常处理"
    status: "⏳ 待检查"
    evidence: "-"
    fix: "-"
  - gate: "G11-优先级"
    status: "⏳ 待检查"
    evidence: "-"
    fix: "-"
  - gate: "G12-职责边界"
    status: "⏳ 待检查"
    evidence: "-"
    fix: "-"
  - gate: "G13-质量标准"
    status: "⏳ 待检查"
    evidence: "-"
    fix: "-"

format_layer:
  - gate: "G14-无反模式"
    status: "⏳ 待检查"
    evidence: "-"
    fix: "-"
  - gate: "G15-非教程"
    status: "⏳ 待检查"
    evidence: "-"
    fix: "-"
  - gate: "G16-YAML完整"
    status: "⏳ 待检查"
    evidence: "-"
    fix: "-"
  - gate: "G17-Token效率"
    status: "⏳ 待检查"
    evidence: "-"
    fix: "-"
  - gate: "G18-路径正确"
    status: "⏳ 待检查"
    evidence: "-"
    fix: "-"
  - gate: "G19-层级深度"
    status: "⏳ 待检查"
    evidence: "-"
    fix: "-"
  - gate: "G20-无重复"
    status: "⏳ 待检查"
    evidence: "-"
    fix: "-"
  - gate: "G21-语气一致"
    status: "⏳ 待检查"
    evidence: "-"
    fix: "-"

recommendations:
  critical: []
  suggested: []
  optional: []
```
