---
name: echart-advanced-skill
version: v1.0.0
author: skill-factory
parent: echart-skill
description: ECharts 高级特性技能，掌握数据集、数据区域缩放、自定义系列等高级功能，用于数据处理、交互探索和定制渲染
tags: [echarts, dataset, dataZoom, custom, series, advanced]
dependency:
  parent: echart-skill
  requires: echart-basic-skill
---

# EChart Advanced Skill - 高级特性技能

## 任务目标

- **本 Skill 用于**：掌握ECharts高级特性（数据处理、交互探索、定制渲染）
- **核心能力**：
  - 数据集(Dataset)：行列数据映射、数据变换
  - 数据区域缩放(DataZoom)：滑块缩放、框选缩放
  - 自定义系列(Custom Series)：自定义渲染逻辑
  - 富文本(Rich Text)：丰富的文字样式
- **触发条件**：处理复杂数据、需要深度交互、定制渲染时

## 图表类型

### 数据集 (Dataset)

**展示信息**：结构化表格数据的可视化

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| dimensions | 维度定义 | 列名和类型 |
| source | 数据源 | 数组/对象数组 |
| encode | 编码映射 | 指定x/y/series映射 |
| transform | 数据变换 | filter/sort/aggregate |

**变量关系**：行列数据到图表的映射关系

```javascript
option = {
  dataset: {
    dimensions: ['product', 'sales', 'profit'],
    source: [
      { product: 'A', sales: 120, profit: 30 },
      { product: 'B', sales: 200, profit: 50 },
      { product: 'C', sales: 150, profit: 40 }
    ]
  },
  xAxis: { type: 'category', name: 'Product', encode: { x: 'product' } },
  yAxis: { type: 'value', name: 'Value' },
  series: [
    { type: 'bar', encode: { y: 'sales' } },
    { type: 'line', encode: { y: 'profit' } }
  ]
};
```

### 数据变换

```javascript
dataset: [{
  source: [...]  // 原始数据
}, {
  transform: {
    type: 'filter',
    config: { dimension: 3, '>=': 100 }
  }
}, {
  transform: {
    type: 'sort',
    config: { dimension: 1, order: 'desc' }
  }
}, {
  transform: {
    type: 'aggregate',
    config: {
      dimensions: ['category'],
      groups: 'category',
      aggregate: 'sum'
    }
  }
}]
```

### 数据区域缩放 (DataZoom)

**展示信息**：数据的局部放大和浏览

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| start | 起始位置 | 0-100百分比 |
| end | 结束位置 | 0-100百分比 |
| type | 类型 | 'inside'/'slider'/'rect' |
| xAxisIndex | 绑定轴 | 关联的x轴索引 |
| yAxisIndex | 绑定轴 | 关联的y轴索引 |

**变量关系**：缩放范围与原始数据的映射

**子类型**：
- 内置滚轮缩放(inside)
- 滑块缩放(slider)
- 框选手动选择(rect)
- 多轴缩放
- 时间轴缩放

```javascript
option = {
  dataZoom: [
    {
      type: 'inside',
      xAxisIndex: 0,
      start: 0,
      end: 100
    },
    {
      type: 'slider',
      xAxisIndex: 0,
      start: 20,
      end: 80,
      height: 20,
      bottom: 10
    }
  ],
  xAxis: { type: 'category', data: [...] },
  yAxis: { type: 'value' },
  series: [{ type: 'line', data: [...] }]
};
```

### 自定义系列 (Custom Series)

**展示信息**：完全自定义的渲染逻辑

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| type | 'custom' | 自定义类型 |
| renderItem | 渲染函数 | 返回图形对象 |
| encode | 编码映射 | 数据到坐标的映射 |
| data | 数据数组 | 渲染使用的数据 |

**变量关系**：数据到自定义图形的映射

**子类型**：
- 自定义柱状图趋势线
- 自定义误差范围
- 甘特图
- 火焰图
- 风向图
- 六边形分箱图

```javascript
series: [{
  type: 'custom',
  renderItem: function(params, api) {
    var xValue = api.value(0);
    var yValue = api.value(1);
    var point = api.coord([xValue, yValue]);
    return {
      type: 'rect',
      shape: { x: point[0], y: point[1], width: 20, height: 40 },
      style: { fill: '#5470C6' }
    };
  },
  data: [
    [0, 50], [1, 70], [2, 60]
  ]
}]
```

### 富文本 (Rich Text)

**展示信息**：丰富的文字样式和布局

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| rich | 富文本定义 | 样式名称和配置 |
| textStyle | 文本样式 | 使用rich引用 |
| formatter | 格式化 | 富文本模板 |

```javascript
option = {
  series: [{
    type: 'pie',
    radius: ['30%', '70%'],
    label: {
      formatter: [
        '{name|{b}}',
        '{value|{c}}',
        '{percent|{d}%}'
      ].join('\n'),
      rich: {
        name: { fontSize: 14, color: '#333', fontWeight: 'bold' },
        value: { fontSize: 20, color: '#5470C6' },
        percent: { fontSize: 12, color: '#999' }
      }
    }
  }]
};
```

## 通用配置

### DataZoom 详细配置

```javascript
dataZoom: [{
  type: 'slider',
  show: true,
  xAxisIndex: [0, 1],           // 关联多个轴
  start: 0,
  end: 100,
  height: 30,
  bottom: 50,
  borderColor: '#ccc',
  fillerColor: 'rgba(84,112,198,0.2)',
  handleStyle: {
    color: '#5470C6',
    borderColor: '#5470C6'
  },
  textStyle: { color: '#333' },
  dataBackground: {
    lineStyle: { color: '#ccc' },
    areaStyle: { color: '#eee' }
  },
  selectedDataBackground: {
    lineStyle: { color: '#5470C6' },
    areaStyle: { color: 'rgba(84,112,198,0.2)' }
  }
}]
```

### 自定义系列 renderItem 参数

```javascript
renderItem: function(params, api) {
  // params: { context, batch, info }
  // api.value(dim): 获取数据值
  // api.coord([x, y]): 数据转像素坐标
  // api.size([width, height]): 数据宽度转像素
  // api.theme: 主题配置
  // api.getWidth(): 画布宽度
  // api.getHeight(): 画布高度

  var categoryIndex = api.value(0);
  var value = api.value(1);
  var point = api.coord([categoryIndex, value]);

  return {
    type: 'group',
    children: [{
      type: 'rect',
      shape: { x: point[0], y: point[1], width: 30, height: 60 },
      style: { fill: '#5470C6' }
    }]
  };
}
```

## 数据转换

### Dataset encode 映射

```javascript
encode: {
  x: 0,                        // 第一列映射到x轴
  y: [1, 2],                   // 第2、3列映射到y轴（多系列）
  tooltip: [0, 1, 2],          // 提示框显示这些列
  legend: 1,                   // 图例使用第2列
  seriesName: [0, 1]           // 系列名称
}
```

### 数据变换链式调用

```javascript
dataset: [{
  id: 'raw',
  source: rawData
}, {
  id: 'filtered',
  fromDatasetId: 'raw',
  transform: { type: 'filter', config: { dimension: 'year', '>=': 2020 } }
}, {
  id: 'sorted',
  fromDatasetId: 'filtered',
  transform: { type: 'sort', config: { dimension: 'sales', order: 'desc' } }
}]
```

## 注意事项

1. **Dataset性能**：复杂变换可能影响性能，大数据量测试后再使用
2. **DataZoom联动**：多个图表需要设置dataZoomIndex并绑定同一轴
3. **自定义系列**：renderItem必须返回ZRender图形对象
4. **Canvas渲染**：自定义系列默认使用canvas渲染
5. **调试**：使用console.log输出api.value()检查数据映射

## 相关技能

- [echart-basic-skill](../echart-basic-skill/SKILL.md) - 基础图表
- [echart-multi-skill](../echart-multi-skill/SKILL.md) - 多图组合（联动）
- [echart-finance-skill](../echart-finance-skill/SKILL.md) - 金融图（K线图+DataZoom）
