---
name: echart-3d-skill
version: v1.0.0
author: skill-factory
parent: echart-skill
description: ECharts 3D图表技能，掌握3D柱状图、3D散点图、3D曲面等三维可视化，用于立体对比、空间分布和曲面分析
tags: [echarts, bar3D, scatter3D, surface3D, line3D, 3D, visualization]
dependency:
  parent: echart-skill
  requires: echart-basic-skill
---

# EChart 3D Skill - 3D图表技能

## 任务目标

- **本 Skill 用于**：掌握三维数据可视化（立体对比、空间分布、曲面分析）
- **核心能力**：
  - 3D柱状图：三维柱形对比
  - 3D散点图：空间三维分布
  - 3D曲面：连续曲面拟合
  - 3D路径图：空间轨迹
- **触发条件**：需要展示三维数据或立体可视化时

## 图表类型

### 3D柱状图 (Bar3D)

**展示信息**：三维坐标系中的柱形对比

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| grid3D | 三维坐标系 | x、y、z轴配置 |
| xAxis3D | 类目/数值轴 | x轴 |
| yAxis3D | 类目/数值轴 | y轴 |
| zAxis3D | 数值轴 | z轴（高度） |
| series.data | 三维数组 | [x, y, z] |

**变量关系**：x、y确定底面位置，z确定高度

**子类型**：
- 基础3D柱状图
- 全球人口3D柱状图
- 3D堆叠柱状图
- 透明3D柱状图
- 3D柱状图+地球

```javascript
option = {
  grid3D: {
    viewControl: { projection: 'perspective', autoRotateAngle: 30 },
    light: { main: { intensity: 1.2 }, ambient: { intensity: 0.3 } }
  },
  xAxis3D: { type: 'category', data: ['A', 'B', 'C'] },
  yAxis3D: { type: 'category', data: ['X', 'Y', 'Z'] },
  zAxis3D: { type: 'value', max: 100 },
  series: [{
    type: 'bar3D',
    data: [
      [0, 0, 50], [1, 0, 70], [2, 0, 60],
      [0, 1, 40], [1, 1, 80], [2, 1, 65]
    ],
    shading: 'realistic',
    itemStyle: { color: '#5470C6', opacity: 0.8 }
  }]
};
```

### 3D散点图 (Scatter3D)

**展示信息**：三维空间中的点分布

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| grid3D | 三维坐标系 | 坐标轴配置 |
| series.data | 四维数组 | [x, y, z, value] |
| symbolSize | 数值/函数 | 点的大小 |
| visualMap | 视觉映射 | 颜色编码第四维 |

**变量关系**：x、y、z确定位置，value编码颜色/大小

**子类型**：
- 基础3D散点图
- 全球人口3D散点图
- 正交投影3D散点图
- 3D散点+散点矩阵

```javascript
option = {
  grid3D: { viewControl: { projection: 'orthographic' } },
  xAxis3D: { type: 'value', name: 'X' },
  yAxis3D: { type: 'value', name: 'Y' },
  zAxis3D: { type: 'value', name: 'Z' },
  series: [{
    type: 'scatter3D',
    data: [
      [10, 20, 30, 100],
      [15, 25, 35, 80],
      [20, 15, 40, 120]
    ],
    symbolSize: function(data) { return data[3] / 20; },
    visualMap: { min: 0, max: 150, dimension: 3 }
  }]
};
```

### 3D曲面 (Surface)

**展示信息**：连续曲面的拟合和展示

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| grid3D | 三维坐标系 | 坐标系配置 |
| series.type | 'surface' | 曲面图 |
| series.data | 三维矩阵 | height Matrix |
| series.surface公式 | 函数 | 自定义曲面方程 |

**变量关系**：x、y确定平面位置，z确定高度

**子类型**：
- 参数曲面
- 球面参数曲面
- 金属曲面
- 玫瑰曲面
- 波形曲面

```javascript
option = {
  grid3D: { viewControl: { autoRotate: true } },
  xAxis3D: { type: 'value', min: -3, max: 3 },
  yAxis3D: { type: 'value', min: -3, max: 3 },
  zAxis3D: { type: 'value', min: -3, max: 3 },
  series: [{
    type: 'surface',
    parametric: true,
    equation: {
      x: function(u, v) { return Math.sin(u) * Math.sin(v); },
      y: function(u, v) { return Math.sin(u) * Math.cos(v); },
      z: function(u, v) { return Math.cos(u); }
    },
    uStep: 30,
    vStep: 30,
    itemStyle: { color: '#5470C6', opacity: 0.8 }
  }]
};
```

### 3D路径图 (Lines3D)

**展示信息**：三维空间中的轨迹路径

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| globe3D | 地球坐标系 | 用于地球轨迹 |
| series.type | 'lines3D' | 3D路径图 |
| series.data | 数组 | [{coords: [[lng1,lat1,h1], [lng2,lat2,h2]]}] |

**变量关系**：起点到终点的三维轨迹

**子类型**：
- 地球航线图
- 3D路径动画
- 飞线效果

```javascript
option = {
  globe3D: {
    baseTexture: 'world.jpg',
    heightTexture: 'height.jpg',
    shading: 'realistic',
    light: { main: { intensity: 0.8 } }
  },
  series: [{
    type: 'lines3D',
    coordinateSystem: 'globe3D',
    data: [{
      name: 'Flight',
      coords: [
        [116.46, 39.92, 0],
        [-74.0, 40.7, 0]
      ],
      lineStyle: { color: '#5470C6', width: 3 }
    }]
  }]
};
```

## 通用配置

### 三维坐标系配置

```javascript
grid3D: {
  viewControl: {
    projection: 'perspective',   // 'perspective' | 'orthographic'
    autoRotate: true,             // 自动旋转
    autoRotateSpeed: 30,          // 旋转速度
    distance: 100,                // 视角距离
    alpha: 40,                    // 视角绕x轴旋转角度
    beta: 40,                     // 视角绕y轴旋转角度
    center: [0, 0, 0]             // 中心点
  },
  light: {
    main: {
      intensity: 1.2,
      shadow: true,
      shadowQuality: 'high'
    },
    ambient: { intensity: 0.3 }
  },
  axisLine: { lineStyle: { color: '#ccc' } },
  axisLabel: { textStyle: { color: '#333' } },
  splitLine: { lineStyle: { color: '#eee' } }
}
```

### 材质和渲染

```javascript
itemStyle: {
  color: '#5470C6',
  opacity: 0.8,
  borderColor: '#fff',
  borderWidth: 1
},
shading: 'realistic',           // 'realistic' | 'lambert' | 'color' | 'normal'
realisticMaterial: {
  roughness: 0.6,
  metalness: 0.1
}
```

## 注意事项

1. **ECharts GL**：3D图表需要引入 ECharts GL 组件
2. **性能**：3D图表性能消耗大，数据量过大会卡顿
3. **视角控制**：使用viewControl配置交互
4. **光照**：复杂场景需要配置光源避免黑面
5. **兼容**：部分浏览器可能不支持WebGL

## 相关技能

- [echart-basic-skill](../echart-basic-skill/SKILL.md) - 基础图表
- [echart-geo-skill](../echart-geo-skill/SKILL.md) - 地理图
- [echart-multi-skill](../echart-multi-skill/SKILL.md) - 多图组合
