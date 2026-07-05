---
name: echart-multi
version: v1.0.0
author: skill-factory
parent: echart
description: ECharts 多图组合技能，掌握grid、polar、timeline、联动等组合图表技术，用于多维度数据对比和复杂可视化场景
tags: [echarts, grid, polar, timeline, connect, combination, multi-chart]
dependency:
  parent: echart
  requires: echart-basic
---

# EChart Multi Skill - 多图组合技能

## 任务目标

- **本 Skill 用于**：掌握多图表组合技术（坐标系叠加、时间轴联动、图表联动）
- **核心能力**：
  - Grid组合：多2D图表并排/叠加
  - Polar组合：极坐标下多图表叠加
  - Timeline组合：时间轴驱动的动态切换
  - 联动(Connect)：多图表同步操作
- **触发条件**：需要展示多维度对比、复杂可视化、动态数据时

## 图表类型

### Grid 组合

**展示信息**：多个2D图表共享坐标系或并排显示

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| grid | 坐标系数组 | 多个grid区域 |
| xAxis | 多轴配置 | 多个x轴 |
| yAxis | 多轴配置 | 多个y轴 |
| series | 多系列 | 分布在不同grid |

**变量关系**：共享或独立的坐标系统

**子类型**：
- 上下排列（多行grid）
- 左右排列（多列grid）
- 共享x轴的双y轴图
- 折线柱状混合图
- 多X轴图

```javascript
option = {
  grid: [
    { left: '10%', right: '10%', top: '10%', height: '35%' },
    { left: '10%', right: '10%', top: '55%', height: '35%' }
  ],
  xAxis: [
    { type: 'category', data: [...], gridIndex: 0 },
    { type: 'category', data: [...], gridIndex: 1 }
  ],
  yAxis: [
    { type: 'value', gridIndex: 0 },
    { type: 'value', gridIndex: 1 }
  ],
  series: [
    { type: 'line', xAxisIndex: 0, yAxisIndex: 0, data: [...] },
    { type: 'bar', xAxisIndex: 1, yAxisIndex: 1, data: [...] }
  ]
};
```

### Polar 组合

**展示信息**：极坐标下的多图表叠加

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| polar | 极坐标系 | 极坐标配置 |
| radiusAxis | 径向轴 | 半径轴 |
| angleAxis | 角度轴 | 角度轴 |
| series | 多个系列 | 叠加在同一极坐标 |

**变量关系**：共享极坐标中心

**子类型**：
- 柱状图+折线图+饼图叠加
- 极坐标散点图
- 雷达图（polar的特殊形式）
- 南极鱼玫瑰图（极坐标面积图）

```javascript
option = {
  polar: { center: ['50%', '50%'], radius: '80%' },
  radiusAxis: { max: 100 },
  angleAxis: {
    type: 'category',
    data: ['A', 'B', 'C', 'D', 'E'],
    startAngle: 90
  },
  series: [
    {
      type: 'bar',
      data: [80, 60, 90, 70, 50],
      coordinateSystem: 'polar',
      name: '系列1',
      stack: 'group'
    },
    {
      type: 'line',
      data: [60, 40, 70, 50, 30],
      coordinateSystem: 'polar',
      name: '系列2'
    }
  ]
};
```

### Timeline 时间轴

**展示信息**：时间轴驱动的数据动态切换

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| timeline | 时间轴配置 | 自动播放控制 |
| options | 选项数组 | 每个时间点的配置 |
| currentIndex | 当前索引 | 当前显示的时间点 |

**变量关系**：时间点与数据配置的映射

**子类型**：
- 动态折线图（数据随时间变化）
- 动态柱状图排名
- 动态地图数据
- 自定义时间轴

```javascript
option = {
  baseOption: {
    title: { text: '动态数据展示' },
    xAxis: { type: 'category', data: ['A', 'B', 'C', 'D'] },
    yAxis: { type: 'value' },
    series: [{ type: 'bar', data: [] }]
  },
  options: [
    { series: [{ data: [120, 200, 150, 80] }] },
    { series: [{ data: [100, 180, 190, 120] }] },
    { series: [{ data: [140, 220, 170, 100] }] }
  ],
  timeline: {
    data: ['2020', '2021', '2022'],
    autoPlay: true,
    playInterval: 2000,
    loop: true
  }
};
```

### 联动 (Connect)

**展示信息**：多个图表同步操作

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| echarts.connect | 连接组 | 将多个图表关联 |
| group | 组标识 | 连接组的ID |

**变量关系**：同一组的图表共享交互状态

**子类型**：
- 刷选联动
- 缩放联动
- 提示框联动
- 图例联动

```javascript
// 方式1：直接连接
echarts.connect('dashboard');

// 方式2：使用bindGroup
var chart1 = echarts.init(document.getElementById('chart1'));
var chart2 = echarts.init(document.getElementById('chart2'));
chart1.group = 'dashboard';
chart2.group = 'dashboard';
echarts.connect('dashboard');

// 断开连接
echarts.disConnect('dashboard');
```

### 叠加 (Overlay)

**展示信息**：多个系列叠加在同一坐标系

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| series | 系列数组 | 多个系列 |
| xAxisIndex | 轴索引 | 共享x轴 |
| yAxisIndex | 轴索引 | 共享y轴 |

**变量关系**：共享坐标轴的多个数据系列

```javascript
option = {
  xAxis: { type: 'category', data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'] },
  yAxis: { type: 'value' },
  series: [
    {
      type: 'bar',
      data: [100, 200, 150, 80, 120],
      barWidth: '40%'
    },
    {
      type: 'line',
      data: [120, 180, 160, 90, 110],
      smooth: true,
      itemStyle: { color: '#eb5454' }
    },
    {
      type: 'scatter',
      symbolSize: 15,
      data: [[1, 170], [3, 165]],
      itemStyle: { color: '#5470C6' }
    }
  ]
};
```

## 多图布局方案

### 上下布局

```javascript
grid: [
  { top: '5%', height: '40%' },   // 上图
  { top: '55%', height: '40%' }   // 下图
]
```

### 左右布局

```javascript
grid: [
  { left: '5%', width: '43%' },   // 左图
  { right: '5%', width: '43%' }   // 右图
]
```

### 复杂布局

```javascript
grid: [
  { left: '5%', top: '5%', width: '60%', height: '40%' },      // 主图
  { right: '5%', top: '5%', width: '30%', height: '40%' },    // 侧边图
  { left: '5%', top: '55%', width: '85%', height: '40%' }      // 底部大图
]
```

## 通用配置

### 连接组配置

```javascript
// 连接多个图表
echarts.connect('myGroup');

// 取消连接
echarts.disConnect('myGroup');

// 获取已连接图表列表
echarts.getConnected('myGroup');
```

### Axis Pointer 联动

```javascript
tooltip: {
  trigger: 'axis',
  axisPointer: {
    type: 'cross',              // 'line' | 'shadow' | 'cross'
    crossStyle: { color: '#999' }
  }
}

axisPointer: {
  link: [{ xAxisIndex: 'all' }],
  label: { backgroundColor: '#333' }
}
```

## 注意事项

1. **Grid重叠**：避免grid区域重叠导致渲染问题
2. **坐标轴唯一性**：每个series必须指定xAxisIndex和yAxisIndex
3. **Polar限制**：极坐标下某些图表类型不支持
4. **Timeline数据**：确保每个时间点数据格式一致
5. **联动性能**：过多联动图表可能影响性能

## 相关技能

- [echart-basic](../echart-basic/SKILL.md) - 基础图表
- [echart-finance](../echart-finance/SKILL.md) - 金融图（K线+成交量组合）
- [echart-geo](../echart-geo/SKILL.md) - 地理图（地图+散点+航线组合）
- [echart-advanced](../echart-advanced/SKILL.md) - 高级特性（DataZoom联动）
