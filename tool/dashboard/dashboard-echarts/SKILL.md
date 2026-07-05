---
name: dashboard-echarts
version: v2.0.0
author: book-skills
description: ECharts 可视化技能，掌握 PyECharts 和 Streamlit-ECharts 的图表配置，实现丰富的交互式数据可视化
---

# Dashboard ECharts

## 任务目标
- 本 Skill 用于：使用 ECharts 创建交互式图表
- 能力包含：PyECharts 图表、Streamlit-ECharts 集成、图表配置
- 触发条件：需要在看板中展示复杂交互图表时

## 操作步骤

### 安装依赖
```bash
uv pip install streamlit-echarts pyecharts
# 或
uv pip install streamlit-echarts[pyecharts]
```

### 基础折线图
```python
import streamlit as st
from streamlit_echarts import st_echarts

options = {
    "xAxis": {
        "type": "category",
        "data": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    },
    "yAxis": {"type": "value"},
    "series": [{
        "data": [820, 932, 901, 934, 1290, 1330, 1320],
        "type": "line",
        "smooth": True
    }]
}

st_echarts(options=options, height="400px")
```

### 柱状图
```python
options = {
    "xAxis": {"type": "category", "data": ["A", "B", "C", "D"]},
    "yAxis": {"type": "value"},
    "series": [{
        "data": [120, 200, 150, 80],
        "type": "bar",
        "itemStyle": {"color": "#5470C6"}
    }]
}
st_echarts(options=options)
```

### 饼图
```python
options = {
    "series": [{
        "type": "pie",
        "radius": ["40%", "70%"],
        "data": [
            {"value": 1048, "name": "搜索引擎"},
            {"value": 735, "name": "直接访问"},
            {"value": 580, "name": "邮件营销"}
        ],
        "label": {"show": True, "formatter": "{b}: {c} ({d}%)"}
    }]
}
st_echarts(options=options)
```

### 散点图
```python
import random
data = [[random.randint(1, 100) for _ in range(10)] for _ in range(3)]

options = {
    "xAxis": {"type": "value"},
    "yAxis": {"type": "value"},
    "series": [{
        "type": "scatter",
        "symbolSize": 20,
        "data": data[0],
        "itemStyle": {"color": "#5470C6"}
    }]
}
st_echarts(options=options, height="500px")
```

### 多系列图表
```python
options = {
    "legend": {"data": ["蒸发量", "降水量"]},
    "xAxis": {"type": "category", "data": ["1月", "2月", "3月", "4月", "5月"]},
    "yAxis": {"type": "value"},
    "series": [
        {
            "name": "蒸发量",
            "type": "bar",
            "data": [2.0, 4.9, 7.0, 23.2, 25.6]
        },
        {
            "name": "降水量",
            "type": "bar",
            "data": [2.6, 5.9, 9.0, 26.4, 28.7]
        }
    ]
}
st_echarts(options=options)
```

### PyECharts 方式
```python
from pyecharts import options as opts
from pyecharts.charts import Bar, Line
from streamlit_echarts import st_pyecharts

# 使用 PyECharts 构建图表
bar = (
    Bar()
    .add_xaxis(["Microsoft", "Amazon", "IBM", "Oracle", "Google"])
    .add_yaxis("2023营收(亿)", [2100, 1850, 650, 520, 1820])
    .set_global_opts(
        title_opts=opts.TitleOpts(title="云服务商营收对比"),
        toolbox_opts=opts.ToolboxOpts(),
        legend_opts=opts.LegendOpts(selected_mode="single")
    )
)
st_pyecharts(bar, height="400px")
```

### 动态交互
```python
from streamlit_echarts import st_echarts

options = {
    "tooltip": {"trigger": "axis"},
    "legend": {"data": ["销量"]},
    "xAxis": {"type": "category", "data": ["衬衫", "毛衣", "领带", "裤子", "高跟鞋"]},
    "yAxis": {"type": "value"},
    "series": [{"data": [5, 20, 36, 10, 10], "type": "line"}]
}

# 添加点击事件
events = {
    "click": "function(params) { return params.name; }"
}
result = st_echarts(options=options, events=events, key="chart1")
st.write(f"点击了: {result}")
```

### 地图可视化
```python
from pyecharts import options as opts
from pyecharts.charts import Map
from streamlit_echarts import st_pyecharts

# 中国地图示例
china_map = (
    Map()
    .add("销售额", 
         [("广东", 500), ("北京", 350), ("上海", 420), ("浙江", 380)], 
         "china")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="中国地图"),
        visualmap_opts=opts.VisualMapOpts(max_=500)
    )
)
st_pyecharts(china_map, height="500px")
```

### 主题配置
```python
# 深色主题
st_echarts(options=options, theme="dark", height="400px")

# 自定义主题色
custom_theme = {
    "color": ["#5470C6", "#91CC75", "#FAC858", "#EE6666"]
}
st_echarts(options=options, theme=custom_theme)
```

### 响应式尺寸
```python
st_echarts(
    options=options,
    height="400px",      # 高度
    width="100%",        # 宽度
    renderer="canvas"   # 或 "svg"
)
```

## 常用配置

### 标题与工具箱
```python
opts.TitleOpts(
    title="主标题",
    subtitle="副标题",
    pos_left="center"
)

opts.ToolboxOpts(
    feature=opts.ToolBoxFeatureSaveAsImage()
)
```

### 图例配置
```python
opts.LegendOpts(
    data=["系列1", "系列2"],
    selected_mode=False  # 禁用图例点击
)
```

### 提示框
```python
opts.TooltipOpts(
    trigger="item",  # 或 "axis"
    trigger_on="mousemove",
    formatter="{b}: {c}"
)
```

## 资源索引
- Streamlit-ECharts：https://github.com/andfanilo/streamlit-echarts
- PyECharts 文档：https://pyecharts.readthedocs.io/
- ECharts 示例：https://echarts.apache.org/examples/

## 注意事项
- 使用 PyECharts 构建复杂图表更方便
- st_echarts 支持原生 ECharts 配置
- height 和 width 支持 CSS 单位
- renderer="svg" 更适合打印和辅助功能
- 使用 on_select 参数处理选择事件
