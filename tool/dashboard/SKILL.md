---
name: dashboard
version: v3.0.0
author: book-skills
description: 数据看板技能库，使用 Python + Streamlit + ECharts + Pandas 快速构建数据分析和可视化应用，掌握从数据处理到界面展示的完整技能体系
---

# Dashboard Skills

## 任务目标
- 本 Skill 用于：使用 Python 快速构建数据看板和可视化应用
- 能力包含：Streamlit 界面开发、Pandas 数据处理、ECharts 图表可视化、项目架构设计、页面导航管理、生产最佳实践
- 触发条件：需要快速创建数据分析和展示应用时

## 技能地图

### 基础技能
- [dashboard-core](dashboard-core/) - 核心架构：项目初始化、页面导航（st.navigation/st.page_link）、侧边栏、缓存策略
- [dashboard-streamlit](dashboard-streamlit/) - Streamlit 基础：文本、表格、图表、输入组件、布局容器
- [dashboard-pandas](dashboard-pandas/) - Pandas 数据处理：数据读取、清洗、转换、聚合

### 进阶技能
- [dashboard-echarts](dashboard-echarts/) - ECharts 可视化：PyECharts、Streamlit-ECharts、交互图表

### 工程技能
- [dashboard-best-practices](dashboard-best-practices/) - 最佳实践：性能优化、状态管理、错误处理、安全部署、测试

## 学习路径

### 快速入门
1. [dashboard-core](dashboard-core/) - 了解项目结构
2. [dashboard-streamlit](dashboard-streamlit/) - 掌握基础组件
3. [dashboard-pandas](dashboard-pandas/) - 数据处理基础

### 图表进阶
4. [dashboard-echarts](dashboard-echarts/) - ECharts 高级图表

### 生产部署
5. [dashboard-best-practices](dashboard-best-practices/) - 性能与部署

## 快速开始

### 安装依赖
```bash
uv pip install streamlit streamlit-echarts pandas pyecharts
```

### 创建第一个看板
```python
import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts

st.title("我的数据看板")

# 读取数据
df = pd.read_csv("sales.csv")

# 显示数据
st.dataframe(df)

# 绑定筛选
with st.sidebar:
    category = st.selectbox("选择类别", df['category'].unique())

# 图表
options = {
    "xAxis": {"type": "category", "data": df['date'].tolist()},
    "yAxis": {"type": "value"},
    "series": [{"data": df['sales'].tolist(), "type": "line"}]
}
st_echarts(options=options)
```

## 资源索引
- Streamlit 文档：https://docs.streamlit.io/
- PyECharts：https://pyecharts.readthedocs.io/
- Streamlit-ECharts：https://github.com/andfanilo/streamlit-echarts
- Pandas 文档：https://pandas.pydata.org/

## 注意事项
- 使用 uv 管理 Python 依赖
- 合理使用 @st.cache_data 缓存
- Session State 管理跨 rerun 状态
- 生产环境使用 secrets 管理敏感配置
