---
name: echart-finance-skill
version: v1.0.0
author: skill-factory
parent: echart-skill
description: ECharts 金融图技能，掌握K线图、雷达图、仪表盘等金融场景图表，用于股票走势、能力评估和指标监控
tags: [echarts, candlestick, radar, gauge, finance, kline]
dependency:
  parent: echart-skill
  requires: echart-basic-skill
---

# EChart Finance Skill - 金融图技能

## 任务目标

- **本 Skill 用于**：掌握金融场景数据可视化（股票走势、能力评估、指标监控）
- **核心能力**：
  - K线图：股票期货走势、波动分析
  - 雷达图：能力评估、多维对比
  - 仪表盘：进度监控、指标展示
- **触发条件**：展示金融数据、评估指标、进度监控时

## 图表类型

### K线图 (Candlestick)

**展示信息**：股票/期货的OHLC（开盘、最高、收盘、最低价）

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| xAxis | 类目轴/时间轴 | 横坐标（时间） |
| yAxis | 数值轴 | 纵坐标（价格） |
| series.data | 数组 | [open, close, lowest, highest] |
| series.itemStyle | 样式 | K线颜色配置 |

**变量关系**：时间序列的四个价格点

**子类型**：
- 基础K线图
- 上证指数K线图
- OHLC图（自定义系列）
- 大数据量K线图
- 触屏交互K线图
- 断轴K线图

```javascript
option = {
  xAxis: { type: 'category', data: ['2024-01', '2024-02', '2024-03'] },
  yAxis: { type: 'value' },
  series: [{
    type: 'candlestick',
    data: [
      [20, 30, 15, 35],   // [open, close, low, high]
      [25, 35, 20, 40],
      [30, 25, 18, 38]
    ],
    itemStyle: {
      color: '#eb5454',       // 上涨颜色
      color0: '#47b262',      // 下跌颜色
      borderColor: '#eb5454',
      borderColor0: '#47b262'
    }
  }]
};
```

### 雷达图 (Radar)

**展示信息**：多维度能力/属性对比

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| radar | 雷达坐标系 | 维度配置 |
| indicator | 指标数组 | [{name, max, min}] |
| series.data | 数组 | 各维度取值 |

**变量关系**：各维度数值的相对位置和面积

**子类型**：
- 基础雷达图
- 多雷达图（叠加）
- AQI雷达图
- 自定义样式雷达图
- 浏览器占比变化雷达图

```javascript
option = {
  radar: {
    indicator: [
      { name: '速度', max: 100 },
      { name: '价格', max: 100 },
      { name: '功能', max: 100 },
      { name: '外观', max: 100 },
      { name: '油耗', max: 100 }
    ],
    shape: 'polygon',        // 'polygon' | 'circle'
    splitNumber: 5
  },
  series: [{
    type: 'radar',
    data: [{
      value: [85, 60, 90, 75, 50],
      name: '车型A',
      areaStyle: { opacity: 0.3 }
    }, {
      value: [70, 80, 70, 85, 70],
      name: '车型B',
      areaStyle: { opacity: 0.3 }
    }]
  }]
};
```

### 仪表盘 (Gauge)

**展示信息**：单一指标与目标/范围的对比

**变量**：
| 变量 | 类型 | 说明 |
|-----|------|-----|
| series.data | 数值 | 当前值 |
| min | 最小值 | 刻度起始值 |
| max | 最大值 | 刻度结束值 |
| radius | 半径 | 仪表盘大小 |
| startAngle | 起始角度 | 指针起始 |
| endAngle | 结束角度 | 指针结束 |

**变量关系**：指针位置相对于整个刻度范围的比例

**子类型**：
- 基础仪表盘
- 速度仪表盘
- 进度仪表盘
- 多标题仪表盘
- 等级仪表盘
- 时钟仪表盘
- 汽车仪表盘

```javascript
option = {
  series: [{
    type: 'gauge',
    radius: '80%',
    startAngle: 200,
    endAngle: -20,
    min: 0,
    max: 100,
    splitNumber: 10,
    pointer: { length: '60%', width: 6 },
    axisLine: {
      lineStyle: {
        width: 20,
        color: [
          [0.3, '#47b262'],
          [0.7, '#fac858'],
          [1, '#eb5454']
        ]
      }
    },
    data: [{ value: 67, name: '进度' }],
    title: { offsetCenter: [0, '40%'] },
    detail: { valueAnimation: true, formatter: '{value}%' }
  }]
};
```

## 通用配置

### K线图专属配置

```javascript
series: [{
  type: 'candlestick',
  barWidth: '60%',
  itemStyle: {
    color: '#eb5454',        // 阳线（上涨）
    color0: '#47b262',       // 阴线（下跌）
    borderColor: '#eb5454',
    borderColor0: '#47b262'
  }
}]
```

### 雷达图专属配置

```javascript
radar: {
  indicator: [
    { name: '指标1', max: 100 },
    { name: '指标2', max: 100 }
  ],
  shape: 'polygon',
  splitNumber: 5,
  axisName: { color: '#333' },
  splitLine: { lineStyle: { color: '#ccc' } },
  splitArea: { areaStyle: { color: ['#fff', '#f5f5f5'] } }
}
```

### 仪表盘专属配置

```javascript
series: [{
  type: 'gauge',
  radius: '75%',
  center: ['50%', '60%'],
  startAngle: 180,
  endAngle: 0,
  min: 0,
  max: 240,
  splitNumber: 12,
  pointer: {
    icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
    length: '12%',
    width: 20,
    offsetCenter: [0, '-10%']
  },
  axisLine: { lineStyle: { width: 6 } },
  axisTick: { length: 12, lineStyle: { color: 'auto' } },
  splitLine: { length: 20, lineStyle: { color: 'auto' } },
  axisLabel: { color: '#464646', fontSize: 12, distance: -60 },
  detail: { valueAnimation: true, fontSize: 50, offsetCenter: [0, '70%'] }
}]
```

## 数据转换

### 股票数据转K线图

```javascript
function toCandlestick(stockData) {
  return stockData.map(item => {
    return [
      item.open,    // 开盘
      item.close,   // 收盘
      item.low,     // 最低
      item.high     // 最高
    ];
  });
}
```

### 评估数据转雷达图

```javascript
function toRadarData(evaluation) {
  return {
    value: [
      evaluation.speed,
      evaluation.power,
      evaluation.function,
      evaluation.appearance,
      evaluation.economy
    ],
    name: evaluation.name
  };
}
```

## 注意事项

1. **K线图**：确保OHLC数据顺序正确，颜色配置要区分涨跌
2. **雷达图**：指标数量建议5-8个，过多会导致图形拥挤
3. **仪表盘**：使用分段颜色直观展示进度/状态
4. **大数据量**：K线图超过1000条考虑使用dataZoom
5. **交互**：K线图常配合MA均线使用

## 相关技能

- [echart-basic-skill](../echart-basic-skill/SKILL.md) - 基础图表
- [echart-multi-skill](../echart-multi-skill/SKILL.md) - 多图组合（K线+成交量）
- [echart-advanced-skill](../echart-advanced-skill/SKILL.md) - 高级特性（dataZoom缩放）
