---
name: data-analytics
version: 1.1.0
description: Use when the user needs a data analysis skill entry point, a recommended analytics sub-skill, or a guided overview of the analysis workflow.
tags: [analytics, data-analysis, visualization, reporting, workflow]
---

# Data Analytics Skills

## 任务目标
- 作为数据分析技能库的入口，帮助用户快速选到正确的子技能
- 提供统一的分析流程视图，避免把流程、处理、可视化和报告混在一起
- 触发条件：用户提到数据分析、数据处理、可视化、分析报告，或需要推荐该用哪个子技能

## 技能地图

### 核心流程
- [analytics-core](analytics-core/) - 分析流程：目标设定、七阶段流程、价值实现

### 数据处理
- [analytics-data-processing](analytics-data-processing/) - 数据处理：获取、清洗、转换、建模准备

### 结果呈现
- [analytics-visualization](analytics-visualization/) - 可视化：多维度展示、图表选型、交互设计
- [analytics-report](analytics-report/) - 报告：结构化输出、受众分层、模板化交付

## 使用方式

### 1. 先判断用户需求
| 用户说法 | 优先子技能 |
|----------|------------|
| 想知道分析该怎么做 | analytics-core |
| 需要拉数据、清洗或建模前处理 | analytics-data-processing |
| 需要图表、仪表盘、交互展示 | analytics-visualization |
| 需要报告、周报、专题分析稿 | analytics-report |

### 2. 再进入对应技能
- 单一任务：直接使用对应子技能
- 组合任务：先用 `analytics-core` 定义目标，再接 `analytics-data-processing`、`analytics-visualization` 或 `analytics-report`
- 不明确时：先从 `analytics-core` 开始，它负责把分析问题拆清楚

## 分析流程总览
1. 明确问题和目标
2. 获取并理解数据
3. 清洗与转换数据
4. 建模或分析
5. 可视化呈现结果
6. 提炼业务结论
7. 形成报告或行动建议

## 注意事项
- 这个技能库是入口，不负责替代具体子技能的详细方法
- 分析任务优先明确目标，再选择工具和表现形式
- 报告和可视化的质量，取决于前面的数据处理是否可靠
