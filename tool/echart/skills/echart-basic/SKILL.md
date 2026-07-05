---
name: echart-basic
version: v1.0.0
author: skill-factory
parent: echart
description: ECharts 基础图表技能，掌握折线图、柱状图、饼图、散点图的配置和用法，包含数据系列、坐标轴、样式定制等
tags: [echarts, line, bar, pie, scatter, basic, chart]
dependency:
  parent: echart
  requires: null
---

# EChart Basic Skill - 基础图表技能

## 任务目标

- **本 Skill 用于**：掌握 ECharts 基础图表（折线图、柱状图、饼图、散点图）的配置和使用
- **核心能力**：
  - 折线图：趋势变化、对比分析
  - 柱状图：分类对比、数量统计
  - 饼图：占比分析、分布统计
  - 散点图：相关性分析、多维度分布
- **触发条件**：需要展示基础数据可视化时

## 图表类型

### 折线图 (Line Chart)

**展示信息**：数据随时间/类目的变化趋势

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| xAxis | 类目轴/数值轴 | 横坐标 |
| yAxis | 数值轴 | 纵坐标 |
| series.data | 数组 | 每个点的数值 |

**变量关系**：x轴与y轴一一对应，支持多系列对比

**子类型**：
- 基础折线图
- 平滑折线图 (smooth)
- 面积图 (areaStyle)
- 堆叠折线图 (stack)
- 渐变面积图
- 阶梯折线图 (step)
- 多X轴折线图

```javascript
option = {
  xAxis: { type: 'category', data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] },
  yAxis: { type: 'value' },
  series: [{
    type: 'line',
    data: [820, 932, 901, 934, 1290, 1330, 1320],
    smooth: true,
    areaStyle: { gradient: [...] }
  }]
};
```

### 柱状图 (Bar Chart)

**展示信息**：不同类目的数值对比

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| xAxis | 类目轴 | 横坐标 |
| yAxis | 数值轴 | 纵坐标 |
| series.data | 数组 | 每个柱子的数值 |

**变量关系**：x轴类目与y轴数值一一对应

**子类型**：
- 基础柱状图
- 堆叠柱状图 (stack)
- 环形柱状图 (barWidth + radius)
- 瀑布图
- 南北对比柱状图
- 极坐标柱状图

```javascript
option = {
  xAxis: { type: 'category', data: ['Apple', 'Banana', 'Orange'] },
  yAxis: { type: 'value' },
  series: [{
    type: 'bar',
    data: [120, 200, 150],
    itemStyle: { color: '#5470C6' }
  }]
};
```

### 饼图 (Pie Chart)

**展示信息**：部分与整体的比例关系

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| series.data | 对象数组 | [{name: 'A', value: 100}] |
| radius | 数值/数组 | 半径 |
| center | 数组 | 圆心位置 |

**变量关系**：各数据项之和为整体

**子类型**：
- 基础饼图
- 环形图 (radius: ['40%', '70%'])
- 南丁格尔玫瑰图 (roseType: 'area')
- 半环形图
- 嵌套饼图
- 富文本标签饼图

```javascript
option = {
  series: [{
    type: 'pie',
    radius: ['40%', '70%'],
    data: [
      { name: 'Apple', value: 100 },
      { name: 'Banana', value: 200 },
      { name: 'Orange', value: 150 }
    ],
    roseType: 'area'
  }]
};
```

### 散点图 (Scatter Chart)

**展示信息**：两个数值变量的相关性，多维度分布

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| xAxis | 数值轴 | 横坐标 |
| yAxis | 数值轴 | 纵坐标 |
| series.data | 二维数组/对象 | [x, y] 或 [x, y, size] |
| symbolSize | 数值/函数 | 点的大小 |
| visualMap | 视觉映射 | 颜色编码第三维度 |

**变量关系**：x与y的相关性，size编码额外维度

**子类型**：
- 基础散点图
- 气泡图 (size编码第三维)
- 涟漪特效散点图 (effectScatter)
- 大规模散点图
- 回归散点图 (线性/多项式/对数)

```javascript
option = {
  xAxis: { type: 'value' },
  yAxis: { type: 'value' },
  series: [{
    type: 'scatter',
    symbolSize: function(data) { return data[2]; },
    data: [[10, 5, 20], [20, 15, 40], [30, 25, 60]],
    visualMap: { min: 0, max: 100, dimension: 2 }
  }]
};
```

## 通用配置

### 坐标轴配置

```javascript
xAxis: {
  type: 'category',  // 类目轴
  data: ['类目1', '类目2', '类目3']
},
yAxis: {
  type: 'value',     // 数值轴
  min: 0,            // 最小值
  max: 100,          // 最大值
  splitNumber: 5     // 分割段数
}
```

### 系列通用配置

```javascript
series: [{
  type: 'line',      // 图表类型
  name: '系列名称',   // 系列名
  data: [...],       // 数据
  itemStyle: {        // 样式
    color: '#5470C6'
  },
  emphasis: {        // 高亮状态
    itemStyle: { shadowBlur: 10 }
  }
}]
```

### 提示框(Tooltip)

```javascript
tooltip: {
  trigger: 'item',   // 'item' | 'axis' | 'none'
  formatter: function(params) {
    return params.name + ': ' + params.value;
  }
}
```

## 数据格式

### 数组格式

```javascript
data: [120, 200, 150]  // 简单数值数组
```

### 对象数组格式

```javascript
data: [
  { name: 'Mon', value: 120 },
  { name: 'Tue', value: 200 }
]
```

### 多维数组格式

```javascript
data: [
  [10, 20, 30],  // [x, y, size]
  [15, 25, 40]
]
```

## 样式定制

### 颜色

```javascript
color: ['#5470C6', '#91CC75', '#FAC858', '#EE6666']
```

### 文字样式

```javascript
textStyle: {
  fontFamily: 'Arial',
  fontSize: 12,
  color: '#333'
}
```

### 图形样式

```javascript
itemStyle: {
  color: '#5470C6',
  borderColor: '#fff',
  borderWidth: 2,
  shadowBlur: 10,
  shadowColor: 'rgba(0,0,0,0.3)'
}
```

## 注意事项

1. **数据量**：超过1000个数据点考虑使用 dataZoom 或采样
2. **坐标轴类型**：时间数据用 'time' 类型，类目用 'category'
3. **饼图标签**：避免标签过多导致重叠，使用引导线或富文本
4. **散点大小**：symbolSize 函数要控制好返回值范围
5. **动画**：大数据量时考虑关闭动画 (animation: false)

## 相关技能

- [echart-finance](../echart-finance/SKILL.md) - 金融图表（K线图、雷达图）
- [echart-multi](../echart-multi/SKILL.md) - 多图组合（grid叠加）
- [echart-advanced](../echart-advanced/SKILL.md) - 高级特性（dataset数据处理）
