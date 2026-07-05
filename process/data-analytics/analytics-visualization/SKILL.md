---
name: analytics-visualization
version: 1.0.1
description: Use when the user needs multi-dimensional data visualization, chart selection guidance, or interactive presentation patterns.
tags: [visualization, charting, plotly, dashboard, data-presentation]
---

# Analytics Visualization

## 任务目标
- 本 Skill 用于：掌握复杂数据的多维度可视化呈现
- 能力包含：多维度变量展示、图表选型、交互设计、可视化原则
- 触发条件：需要展示多维度数据、呈现分析结果时

## 适用场景
- 需要把多维数据压缩成容易理解的图表
- 需要在趋势、对比、分布、关系和路径之间选图
- 需要做交互式图表或分析仪表盘

## 核心原则

### 可视化黄金法则
```
1. 明确可视化目标（比较、趋势、分布、关系、占比）
2. 选择适合数据类型的图表
3. 减少视觉干扰，突出关键信息
4. 引导读者关注重点
5. 提供足够的上下文帮助理解
```

### 图表选择决策树
```
数据维度数量
    │
    ├── 1维（单一变量）→ 折线图、柱状图
    │
    ├── 2维（两个变量）→ 散点图、气泡图
    │
    ├── 3维（三个变量）→ 3D散点图、热力图
    │
    └── 多维（4+变量）→ 雷达图、平行坐标、桑基图
                            ↓
                    考虑降维或分面展示
```

## 多维度变量展示方案

### 1. 气泡图（适合3-4个维度）

**维度映射**：
- X轴：第一个变量
- Y轴：第二个变量
- 气泡大小：第三个变量
- 气泡颜色：第四个变量

**示例**：
```python
import plotly.express as px

df = px.data.iris()
fig = px.scatter(
    df,
    x="sepal_width",
    y="sepal_length",
    size="petal_length",      # 第四维：点大小
    color="species",           # 第五维：颜色区分
    hover_name="species"
)
fig.show()
```

**适用场景**：用户/产品/业务的多维度对比分析

### 2. 热力图（适合展示矩阵关系）

**核心原理**：通过颜色深浅表达数值大小

**示例 - 指标与时间维度交叉**：
```python
import plotly.graph_objects as go
import pandas as pd
import numpy as np

data = np.random.rand(10, 12)  # 10个指标 x 12个月
labels_x = [f"2024-{str(i).zfill(2)}" for i in range(1, 13)]
labels_y = [f"指标{i}" for i in range(1, 11)]

fig = go.Figure(data=go.Heatmap(
    z=data,
    x=labels_x,
    y=labels_y,
    colorscale='RdYlGn',
    hovertemplate='指标: %{y}<br>时间: %{x}<br>值: %{z:.2f}<extra></extra>'
))
fig.show()
```

**适用场景**：指标波动监控、相关性分析、用户行为矩阵

### 3. 雷达图（适合对比多个维度）

**核心原理**：将多维度展开到同心圆轴线上

**示例 - 用户画像多维度对比**：
```python
import plotly.graph_objects as go

categories = ['活跃度', '购买力', '忠诚度', '传播力', '满意度', '复购率']

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=[85, 72, 90, 65, 88, 78],
    theta=categories,
    fill='toself',
    name='高价值用户',
    line_color='red'
))

fig.add_trace(go.Scatterpolar(
    r=[45, 55, 60, 40, 65, 50],
    theta=categories,
    fill='toself',
    name='普通用户',
    line_color='blue'
))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    showlegend=True,
    title="用户画像多维度对比"
)
fig.show()
```

**适用场景**：用户分群、产品属性对比、能力评估

### 4. 平行坐标图（适合5+维度）

**核心原理**：每个维度一条垂直轴，数据点用线连接

**示例**：
```python
import plotly.express as px

df = px.data.iris()
fig = px.parallel_coordinates(
    df,
    color="species",
    dimensions=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'],
    color_continuous_scale=px.colors.diverging.Tealrose
)
fig.show()
```

**适用场景**：多指标监控、高维数据探索、聚类结果展示

### 5. 旭日图（适合层级结构+占比）

**核心原理**：环形图的多层扩展

**示例 - 业务营收层级分解**：
```python
import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    'labels': ['总营收', '产品A', '产品B', '产品A-区域1', '产品A-区域2', '产品B-区域1', '产品B-区域2'],
    'parents': ['', '总营收', '总营收', '产品A', '产品A', '产品B', '产品B'],
    'values': [100, 60, 40, 35, 25, 22, 18]
})

fig = px.sunburst(df, names='labels', parents='parents', values='values')
fig.show()
```

**适用场景**：营收分解、组织架构、业务结构分析

### 6. 桑基图（适合流量/转化分析）

**核心原理**：展示流量从源头到终点的分配

**示例 - 用户转化路径**：
```python
import plotly.graph_objects as go

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=["访问", "注册", "下单", "支付", "复购"],
        color=["blue", "green", "orange", "red", "purple"]
    ),
    link=dict(
        source=[0, 1, 2, 1, 3, 2],
        target=[1, 2, 3, 4, 4, 4],
        value=[1000, 400, 300, 100, 200, 150]
    )
)])
fig.show()
```

**适用场景**：转化漏斗、流量分析、路径追踪

### 7. 分面图（适合分组对比）

**核心原理**：将数据分组，在多个子图中并排展示

**示例 - 按类别分组的时间序列**：
```python
import plotly.express as px

df = px.data.tips()
fig = px.line(
    df,
    x="size",
    y="total_bill",
    color="sex",
    facet_col="smoker",
    facet_row="time",
    title="各维度组合下的消费对比"
)
fig.show()
```

**适用场景**：多维度交叉分析、分组对比

### 8. 组合图表（适合混合数据类型）

**核心原理**：在一个图表区叠加多种图表类型

**示例 - 趋势+目标线+异常标记**：
```python
import plotly.graph_objects as go
import pandas as pd

dates = pd.date_range('2024-01-01', periods=30)
values = [100 + i*2 + (i%7)*5 + (i**1.1) + 50*((i%5)/5) for i in range(30)]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=dates,
    y=values,
    mode='lines+markers',
    name='实际值',
    line=dict(color='blue')
))

fig.add_trace(go.Scatter(
    x=dates,
    y=[120]*30,
    mode='lines',
    name='目标线',
    line=dict(color='green', dash='dash')
))

fig.add_trace(go.Scatter(
    x=dates[values.index(max(values))],
    y=[max(values)],
    mode='markers+text',
    marker=dict(color='red', size=15),
    text=['峰值'],
    name='异常点'
))

fig.update_layout(
    title="30天趋势监控（多元素组合）",
    xaxis_title="日期",
    yaxis_title="数值"
)
fig.show()
```

**适用场景**：KPI监控、趋势分析、异常检测

## 进阶可视化技术

### 地理可视化（基于位置的多维度）

**散点地图 + 颜色/大小编码**：
```python
import plotly.express as px

df = px.data.gapminder().query("year == 2007")

fig = px.scatter_geo(
    df,
    locations="iso_alpha",
    size="pop",
    color="lifeExp",
    hover_name="country",
    projection="natural earth",
    title="全球预期寿命分布"
)
fig.show()
```

### 箱线图 + 小提琴图（分布多维度）

**组合展示**：
```python
import plotly.express as px

df = px.data.tips()
fig = px.violin(
    df,
    y="total_bill",
    x="day",
    color="sex",
    box=True,
    points="all",
    hover_data=df.columns
)
fig.show()
```

### 3D散点图（真正三维展示）

```python
import plotly.express as px

df = px.data.iris()
fig = px.scatter_3d(
    df,
    x='sepal_length',
    y='sepal_width',
    z='petal_length',
    color='species',
    size='petal_width',
    title="鸢尾花数据集 3D 可视化"
)
fig.show()
```

## 配色与主题

### 配色原则
| 场景 | 推荐色板 | 说明 |
|------|----------|------|
| 数值递增 | RdYlGn（红-黄-绿） | 直观表达大小 |
| 数值递减 | YlOrRd（黄-橙-红） | 警示类常用 |
| 分类对比 | 类别色板 | 区分不同类别 |
| 正负对比 | 蓝色-红色 | 正面-负面 |
| 统一主题 | 单色渐变 | 强调一致性 |

### 交互最佳实践
```python
fig.update_layout(
    hovermode="x unified",      # 统一悬停
    hoverlabel=dict(
        bgcolor="white",
        font_size=12
    ),
    dragmode="pan"              # 拖拽平移
)
fig.show(config={"scrollZoom": True})
```

## 图表选型速查表

| 分析目的 | 推荐图表 |
|----------|----------|
| 趋势分析 | 折线图、面积图 |
| 比较大小 | 柱状图、条形图 |
| 占比分布 | 饼图、环形图、旭日图 |
| 相关关系 | 散点图、热力图 |
| 分布形态 | 直方图、箱线图、小提琴图 |
| 转化路径 | 桑基图、漏斗图 |
| 地理分布 | 地图、散点地图 |
| 多维对比 | 雷达图、平行坐标、气泡图 |
| 分组对比 | 分面图、组合图 |

## 常见问题处理

### 维度过多怎么办？
1. **降维**：使用PCA或因子分析
2. **分面**：按某维度拆分多个子图
3. **交互**：提供筛选器动态切换
4. **聚合**：高维转低维聚合指标

### 数据量过大怎么办？
1. **采样**：随机抽样或分箱
2. **聚合**：预聚合后展示
3. **渐进加载**：先概览后细节
4. **数据窗口**：时间窗口切片

### 颜色使用误区
1. 不使用红绿色（色盲不友好）
2. 不使用过多颜色（≤7种）
3. 颜色要有语义一致性
4. 深浅表达数值大小

## 资源索引
- Plotly 图表库：https://plotly.com/python/
- ECharts 示例库：https://echarts.apache.org/examples/
- 颜色工具：https://colorbrewer2.org/

## 注意事项
- 可视化是手段，不是目的，让数据说话才是目的
- 多维度展示要考虑受众的理解能力
- 交互要适度，避免过度复杂
- 静态图表优先考虑打印/分享场景
