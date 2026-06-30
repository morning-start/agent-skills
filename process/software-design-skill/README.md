# Software Design Skill

软件架构设计与评估 Skill 包。

## 功能

两个核心场景 + 设计模式辅助：

| 场景 | 功能 | 对应子技能 |
|------|------|-----------|
| **场景一** | 从零开始设计系统架构 | `design-initiator` |
| **场景二** | 评估现有架构并提出改进建议 | `architecture-evaluator` |
| **辅助** | 设计模式推荐与速查 | `pattern-advisor` |

## 目录结构

```
software-design-skill/
├── SKILL.md                                    # 主入口：场景识别与调度
├── skills/
│   ├── design-initiator/SKILL.md               # 场景一：初始架构设计
│   ├── architecture-evaluator/SKILL.md         # 场景二：现状评估
│   └── pattern-advisor/SKILL.md                # 设计模式推荐
├── scripts/
│   ├── pre_check_hook.py                       # 前置检查钩子
│   └── report_generator.py                     # 报告生成器
├── references/
│   └── design_patterns_slim.md                 # 精简设计模式速查表
└── README.md
```

## 使用方式

1. 将 `software-design-skill/` 放入你的 Agent 的 skills 目录
2. Agent 在遇到架构相关问题时自动触发主 SKILL.md
3. 主 SKILL 根据用户输入关键词自动路由到对应子技能

### 手动调用

```
请使用 software-design 技能来处理这个架构设计需求。
```

### Python 脚本使用

```bash
# 前置检查
python scripts/pre_check_hook.py '{"business_goal": "构建电商平台", "feature_list": "用户+订单+支付", "current_state": "从零开始"}'

# 报告生成
python scripts/report_generator.py assessment_data.json --output output/report.md
```

## 输入要求

| 类型 | 字段 | 说明 |
|------|------|------|
| **必填** | `business_goal` | 核心业务目标（1-2 句话） |
| **必填** | `feature_list` | 功能列表或现状描述 |
| **必填** | `current_state` | 项目阶段（从零 / 已有 / 重构） |
| **选填** | `non_functional` | 性能 / 可用性 / 安全要求 |
| **选填** | `tech_stack` | 技术栈偏好或限制 |
| **选填** | `constraints` | 预算 / 时间 / 部署约束 |

## 版本

v2.0.0 — 基于 Superpowers 风格的架构设计 Skill 包
