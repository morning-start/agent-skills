---
name: doc-phase-analysis
version: 0.1.0
description: 分析阶段协调器，负责项目分析、需求解析、现状扫描，为后续文档生成提供基础数据
---

# Analysis Phase Coordinator

## 职责

- 分析项目类型、规模、技术栈
- 解析用户需求，提取关键信息
- 扫描现有文档（如有），评估现状
- 输出标准化的 `project-profile.yaml`

## 子技能

| 执行者 | 职责 | 路径 |
|--------|------|------|
| project-analyzer | 项目类型/规模/技术栈分析 | [查看](project-analyzer/SKILL.md) |
| requirement-parser | 需求解析与结构化 | [查看](requirement-parser/SKILL.md) |
| current-state-scanner | 现有文档扫描与评估 | [查看](current-state-scanner/SKILL.md) |

## 输入

- 用户的项目描述或需求文档
- 可选：现有代码仓库路径、现有文档路径

## 输出

```yaml
project-profile.yaml:
  project_type: frontend|backend|fullstack|mobile|desktop|game|cli
  scale: small|medium|large
  tech_stack: [react, node, postgresql]
  platforms: [web, mobile]
  existing_docs:
    - type: requirement
      path: docs/srs.md
      quality: 0.7
  requirements_summary:
    core_features: [...]
    non_functional: [...]
    constraints: [...]
```

## 工作流程

1. 读取用户输入
2. 调用 project-analyzer 分析项目特征
3. 调用 requirement-parser 结构化需求
4. 如有现有文档，调用 current-state-scanner 评估
5. 合并输出 project-profile.yaml

## 注意事项

- 规模判断基于：功能数量、团队规模、复杂度
- 技术栈识别优先从代码/描述中提取，不足时询问用户
- 现有文档评估需输出质量分数（0-1）
