---
name: echart-skill
version: v1.0.0
author: skill-factory
description: Apache ECharts 技能族，掌握折线图、柱状图、饼图、散点图、关系图、地图、K线图等各类图表可视化，适用于数据可视化开发
tags: [echarts, visualization, chart, javascript, skill-family]
---

# EChart Skills - Apache ECharts 技能族

## 技能族概述

EChart Skills 是 Apache ECharts 技术栈的完整技能族，包含以下子技能：

- **echart-basic-skill**：基础图表技能（折线图、柱状图、饼图、散点图）
- **echart-relation-skill**：关系图技能（关系图、桑基图、树图、旭日图）
- **echart-statistics-skill**：统计图技能（热力图、盒须图、平行坐标、矩阵）
- **echart-finance-skill**：金融图技能（K线图、雷达图、仪表盘）
- **echart-geo-skill**：地理图技能（地图、3D地球、航班图）
- **echart-3d-skill**：3D图表技能（3D柱状图、3D散点图、3D曲面）
- **echart-advanced-skill**：高级特性技能（dataset、dataZoom、自定义系列）
- **echart-multi-skill**：多图组合技能（grid、polar、timeline、联动）

## 子技能列表

| 子技能 | 版本 | 描述 | 依赖 |
|--------|------|------|------|
| echart-basic-skill | v1.0.0 | 基础图表（折线图、柱状图、饼图、散点图） | 无 |
| echart-relation-skill | v1.0.0 | 关系图（关系图、桑基图、树图、旭日图） | echart-basic-skill |
| echart-statistics-skill | v1.0.0 | 统计图（热力图、盒须图、平行坐标、矩阵） | echart-basic-skill |
| echart-finance-skill | v1.0.0 | 金融图（K线图、雷达图、仪表盘） | echart-basic-skill |
| echart-geo-skill | v1.0.0 | 地理图（地图、3D地球、3D地图） | echart-basic-skill |
| echart-3d-skill | v1.0.0 | 3D图表（3D柱状图、3D散点图、3D曲面） | echart-basic-skill |
| echart-advanced-skill | v1.0.0 | 高级特性（dataset、dataZoom、自定义系列） | echart-basic-skill |
| echart-multi-skill | v1.0.0 | 多图组合（grid、polar、timeline、联动） | 多个基础技能 |

## 使用方式

### 单独使用子技能

```bash
# 使用 ECharts 基础图表技能
/ Skill echart-basic-skill

# 使用 ECharts 关系图技能
/ Skill echart-relation-skill

# 使用 ECharts 金融图技能
/ Skill echart-finance-skill
```

### 使用完整技能族

```bash
# 使用 ECharts 全技能族
/ Skill echart-skill
```

## 技能族结构

```
echart-skill/
├── SKILL.md                    # 母技能定义
├── references/
│   └── overview.md            # 技能族概述
└── skills/                     # 子技能目录
    ├── echart-basic-skill/
    ├── echart-relation-skill/
    ├── echart-statistics-skill/
    ├── echart-finance-skill/
    ├── echart-geo-skill/
    ├── echart-3d-skill/
    ├── echart-advanced-skill/
    └── echart-multi-skill/
```

## 学习路径

1. **echart-basic-skill**（先学）- 掌握折线图、柱状图、饼图、散点图
2. **echart-finance-skill** / **echart-statistics-skill**（并行）- 根据需求选择
3. **echart-relation-skill** / **echart-geo-skill**（并行）- 进阶图表
4. **echart-advanced-skill** / **echart-multi-skill**（后学）- 高级特性和组合

## 版本兼容性

- ECharts 5.0+
- ECharts GL 1.0+
