---
name: agent-skills
version: 1.0.0
description: AI Agent 技能集合仓库管理规范
---

# Agent Skills 仓库管理规范

## 目录分类规则

新技能加入时，按以下规则归类：

### lang/ — 语言与框架
- **条件**: 教学内容是某编程语言或完整开发框架
- **特征**: 教人用该技术构建完整应用
- **示例**: React, Go, Flutter, Rust, Svelte, Vue, Tauri

### tool/ — 工具
- **条件**: 教学内容是某具体工具或库
- **特征**: 在已有项目中使用该工具完成任务
- **示例**: Git, DrissionPage, Scrapling, ECharts, Plotnine

### process/ — 流程方法论
- **条件**: 教学内容是开发流程、架构方法或编码规范
- **特征**: 教人"怎么做"，而非"用什么做"
- **示例**: TDD, Clean Architecture, 代码审查, 项目管理

### utility/ — 辅助工具
- **条件**: 不属于以上任何类别的通用辅助技能
- **特征**: 跨界工具，解决特定非技术问题
- **示例**: 技术选型对比, 副业评估, 招聘处理

## 命名规范

- 目录名: `{short-name}`（全小写，连字符分隔）
- 主文档: `SKILL.md`
- 子技能: 放在父技能目录下，使用 `{parent}-{sub}` 格式
- SKILL.md 元数据 `name` 字段: 使用 `{short-name}`，与目录名一致

## 质量门禁

- [ ] 技能目录在正确的分类下
- [ ] 目录名符合 `{name}` 格式
- [ ] 包含 `SKILL.md` 主文档
- [ ] SKILL.md 包含 name/version/description/tags 元数据
- [ ] 无跨仓重复（旧仓库已废弃）
