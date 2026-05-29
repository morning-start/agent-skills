---
name: echart-statistics-skill
version: v1.0.0
author: skill-factory
parent: echart-skill
description: ECharts 统计图技能，掌握热力图、盒须图、平行坐标、矩阵等统计型图表，用于分布分析、多维对比和模式识别
tags: [echarts, heatmap, boxplot, parallel, matrix, statistics]
dependency:
  parent: echart-skill
  requires: echart-basic-skill
---

# EChart Statistics Skill - 统计图技能

## 任务目标

- **本 Skill 用于**：掌握统计型数据可视化（分布分析、多维对比、模式识别）
- **核心能力**：
  - 热力图：密度分析、模式识别
  - 盒须图：分布统计、异常检测
  - 平行坐标：多维分析、聚类识别
  - 矩阵：相关性分析、对比矩阵
- **触发条件**：展示统计数据分布、多维度对比时

## 图表类型

### 热力图 (Heatmap)

**展示信息**：二维数据的密度/强度分布

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| xAxis | 类目轴/数值轴 | 横坐标 |
| yAxis | 类目轴/数值轴 | 纵坐标 |
| series.data | 二维数组 | [[x, y, value], ...] |
| visualMap | 视觉映射 | 颜色渐变 |
| label | 标签配置 | 是否显示数值 |

**变量关系**：x和y确定位置，value确定颜色/强度

**子类型**：
- 笛卡尔坐标系热力图
- 散点热力图（基于地理/极坐标）
- 日历热力图
- 颜色离散映射热力图
- 大规模热力图

```javascript
option = {
  xAxis: { type: 'category', data: ['A', 'B', 'C', 'D'] },
  yAxis: { type: 'category', data: ['W', 'X', 'Y', 'Z'] },
  visualMap: { min: 0, max: 100, calculable: true, orient: 'vertical' },
  series: [{
    type: 'heatmap',
    data: [[0, 0, 5], [0, 1, 10], [1, 0, 15], [1, 1, 20]],
    label: { show: true },
    emphasis: { itemStyle: { shadowBlur: 10 } }
  }]
};
```

### 盒须图 (Boxplot)

**展示信息**：数据的统计分布（中位数、四分位、异常点）

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| xAxis | 类目轴 | 横坐标（每个类目一个盒须图） |
| yAxis | 数值轴 | 纵坐标 |
| series.data | 五维数组 | [min, Q1, median, Q3, max] |
| outlier | 异常点数组 | 超出须的范围的点 |

**变量关系**：展示数据的统计特征分布

**子类型**：
- 水平盒须图
- 多系列盒须图
- 带异常点的盒须图

```javascript
option = {
  xAxis: { type: 'category', data: ['Group1', 'Group2', 'Group3'] },
  yAxis: { type: 'value' },
  series: [{
    type: 'boxplot',
    data: [
      [[856, 940, 968, 1025, 1080], [850, 900, 950, 980, 1050]],  // Group1
      [[880, 920, 960, 1000, 1100], [860, 910, 940, 990, 1060]],  // Group2
      [[900, 940, 980, 1040, 1120], [880, 930, 970, 1020, 1090]]   // Group3
    ]
  }]
};
```

### 平行坐标 (Parallel)

**展示信息**：多维度数据的并行对比

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| parallelAxis | 平行轴数组 | 每个维度的配置 |
| parallel | 坐标系配置 | 平行坐标系的布局 |
| series.data | 多维数组 | [dim1, dim2, dim3, ...] |

**变量关系**：同一数据点在各维度上的取值

**子类型**：
- 基础平行坐标图
- AQI分布平行坐标
- 营养结构平行坐标

```javascript
option = {
  parallelAxis: [
    { dim: 0, name: '密度' },
    { dim: 1, name: '价格' },
    { dim: 2, name: '评分' }
  ],
  parallel: { left: '5%', right: '10%', bottom: '10%', top: '20%' },
  series: [{
    type: 'parallel',
    data: [
      [0.5, 100, 4.5],
      [0.6, 200, 4.2],
      [0.7, 150, 4.8]
    ],
    lineStyle: { width: 2, opacity: 0.5 }
  }]
};
```

### 矩阵 (Matrix)

**展示信息**：行列交叉数据、相关性矩阵

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| xAxis | 类目轴 | 列 |
| yAxis | 类目轴 | 行 |
| series.data | 二维数组 | [[row, col, value], ...] |
| visualMap | 视觉映射 | 颜色编码 |

**变量关系**：行与列的交叉点值

**子类型**：
- 相关矩阵（热力图形式）
- 混淆矩阵
- 协方差矩阵
- 股市矩阵图
- 元素周期表

```javascript
option = {
  xAxis: { type: 'category', data: ['A', 'B', 'C', 'D'] },
  yAxis: { type: 'category', data: ['W', 'X', 'Y', 'Z'] },
  visualMap: { min: -1, max: 1, calculable: true, orient: 'vertical' },
  series: [{
    type: 'heatmap',
    data: [[0, 0, 1], [0, 1, 0.5], [1, 0, 0.5], [1, 1, 0.8]],
    label: { show: true },
    emphasis: { itemStyle: { borderColor: '#333', borderWidth: 2 } }
  }]
};
```

## 通用配置

### 视觉映射 (VisualMap)

```javascript
visualMap: {
  min: 0,                          // 最小值
  max: 100,                        // 最大值
  calculable: true,                 // 是否可拖拽
  orient: 'vertical',              // 方向
  left: 'right',                   // 位置
  inRange: {                        // 颜色范围
    color: ['#50a3ba', '#eac736', '#d94e5d']
  },
  textStyle: { color: '#333' }
}
```

### 标签配置

```javascript
label: {
  show: true,                      // 显示标签
  position: 'top',                 // 位置
  formatter: '{c}',                // 格式化
  fontSize: 12,
  color: '#333'
}
```

### 高亮状态

```javascript
emphasis: {
  itemStyle: {
    shadowBlur: 10,
    shadowColor: 'rgba(0,0,0,0.3)'
  },
  label: { show: true }
}
```

## 数据转换

### 原始数据转热力图

```javascript
function toHeatmapData(rawData, xField, yField, valueField) {
  const data = [];
  rawData.forEach(item => {
    data.push([item[xField], item[yField], item[valueField]]);
  });
  return data;
}
```

### 统计结果转盒须图

```javascript
function toBoxplotData(statData) {
  return statData.map(item => {
    return [
      item.min,
      item.q1,
      item.median,
      item.q3,
      item.max
    ];
  });
}
```

## 注意事项

1. **热力图颜色**：选择合适的颜色渐变突出重点区域
2. **盒须图数据**：确保数据已正确计算五个统计量
3. **平行坐标**：维度过多时考虑降维或筛选
4. **矩阵排序**：行列可按相似性排序发现模式
5. **大规模数据**：超过5000点考虑采样或聚合

## 相关技能

- [echart-basic-skill](../echart-basic-skill/SKILL.md) - 基础图表
- [echart-multi-skill](../echart-multi-skill/SKILL.md) - 多图组合
- [echart-advanced-skill](../echart-advanced-skill/SKILL.md) - 高级特性（dataset聚合）
