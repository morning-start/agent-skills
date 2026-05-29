---
name: dashboard-core
version: v3.0.0
author: book-skills
description: 数据看板核心技能，掌握项目搭建、页面导航管理、数据流设计和模块化架构，实现高效的数据分析与展示应用
---

# Dashboard Core

## 任务目标
- 本 Skill 用于：搭建数据看板项目的整体架构
- 能力包含：项目初始化、目录设计、页面导航（st.navigation/st.page_link）、侧边栏管理、数据流管理、模块化开发
- 触发条件：需要从头创建数据看板项目时

## 操作步骤

### 项目初始化
```bash
uv pip install streamlit streamlit-echarts pandas pyecharts

# 创建项目结构
mkdir dashboard_project
cd dashboard_project
touch app.py
mkdir pages/
mkdir components/
mkdir utils/
```

### 基础目录结构
```
dashboard_project/
├── app.py              # 主入口
├── pages/              # 多页面
│   ├── overview.py
│   ├── analysis.py
│   └── report.py
├── components/         # 组件
│   ├── charts.py
│   └── tables.py
├── utils/             # 工具
│   ├── data_loader.py
│   └── formatters.py
└── .streamlit/
    └── config.toml
```

### Streamlit 配置
```toml
# .streamlit/config.toml
[general]
title = "数据看板"
favicon = "🏠"

[theme]
primaryColor = "#0078D4"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F5F5"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
```

### 页面导航：st.navigation 方式

```python
# app.py - 使用 st.navigation 实现灵活的多页面应用
import streamlit as st

st.set_page_config(page_title="数据看板", page_icon="📊", layout="wide")

# 定义所有页面
pages = {
    "数据概览": [
        st.Page("pages/01_overview.py", title="总览", icon="🏠"),
        st.Page("pages/02_metrics.py", title="核心指标", icon="📈"),
    ],
    "数据分析": [
        st.Page("pages/03_analysis.py", title="销售分析", icon="🔍"),
        st.Page("pages/04_comparison.py", title="同比对比", icon="📊"),
    ],
    "系统设置": [
        st.Page("pages/05_settings.py", title="偏好设置", icon="⚙️"),
    ],
}

# 运行导航
pg = st.navigation(pages)
pg.run()
```

### 页面导航：pages/ 目录方式

```
# 快速创建多页面应用（Streamlit 自动识别）
dashboard_project/
├── app.py              # 主入口（首页）
└── pages/              # 页面目录
    ├── 1_📊_概览.py      # 显示为 "📊 概览"
    ├── 2_📈_分析.py      # 显示为 "📈 分析"
    ├── 3_📋_报表.py      # 显示为 "📋 报表"
    └── 4_⚙️_设置.py      # 显示为 "⚙️ 设置"
```

```python
# 每个页面文件的头部设置
# pages/1_📊_概览.py
import streamlit as st

st.set_page_config(
    page_title="数据概览",
    page_icon="📊",
    layout="wide"
)

st.title("📊 数据概览")
# 页面内容...
```

### 自定义侧边栏导航

```python
# app.py - 使用 st.page_link 创建自定义导航
import streamlit as st

st.set_page_config(page_title="数据看板", layout="wide")

# 隐藏默认侧边栏导航（在 .streamlit/config.toml 中设置）
# [client]
# showSidebarNavigation = false

with st.sidebar:
    st.title("📊 数据看板")
    st.divider()
    
    st.page_link("app.py", label="首页", icon="🏠")
    st.page_link("pages/1_📊_概览.py", label="数据概览", icon="📊")
    st.page_link("pages/2_📈_分析.py", label="销售分析", icon="📈")
    st.page_link("pages/3_📋_报表.py", label="报表导出", icon="📋")
    
    st.divider()
    st.page_link("pages/4_⚙️_设置.py", label="设置", icon="⚙️")

# 主内容区域
st.title("欢迎使用数据看板")
```

### 动态导航（基于角色/权限）

```python
# menu.py - 动态导航菜单
import streamlit as st

def show_menu():
    """根据用户角色显示不同的导航菜单"""
    with st.sidebar:
        st.title("📊 数据看板")
        st.divider()
        
        # 所有用户可见
        st.page_link("app.py", label="首页", icon="🏠")
        st.page_link("pages/1_📊_概览.py", label="数据概览", icon="📊")
        
        # 仅分析师和管理员可见
        if st.session_state.get("role") in ["analyst", "admin"]:
            st.page_link("pages/2_📈_分析.py", label="销售分析", icon="📈")
        
        # 仅管理员可见
        if st.session_state.get("role") == "admin":
            st.page_link("pages/4_⚙️_设置.py", label="设置", icon="⚙️")

# app.py 中使用
from menu import show_menu

if "role" not in st.session_state:
    st.session_state.role = "viewer"

# 角色选择器（仅用于演示）
with st.sidebar:
    role = st.selectbox("模拟角色", ["viewer", "analyst", "admin"])
    st.session_state.role = role

show_menu()
```

### 带标签分组的侧边栏

```python
# app.py - 使用 Section 分组导航
import streamlit as st

st.set_page_config(page_title="数据看板", layout="wide")

# 方式一：使用字典分组（st.navigation 支持）
sections = {
    "核心功能": [
        st.Page("pages/1_📊_概览.py", title="数据概览", icon="📊"),
        st.Page("pages/2_📈_分析.py", title="销售分析", icon="📈"),
    ],
    "报告中心": [
        st.Page("pages/3_📋_报表.py", title="报表导出", icon="📋"),
        st.Page("pages/3b_📑_模板.py", title="模板管理", icon="📑"),
    ],
    "系统": [
        st.Page("pages/4_⚙️_设置.py", title="偏好设置", icon="⚙️"),
    ],
}

pg = st.navigation(sections)
pg.run()
```

### 数据加载模式
```python
# utils/data_loader.py
import streamlit as st
import pandas as pd

@st.cache_data
def load_data(source: str) -> pd.DataFrame:
    if source.endswith('.csv'):
        return pd.read_csv(source)
    elif source.endswith('.xlsx'):
        return pd.read_excel(source)
    else:
        raise ValueError(f"Unsupported source: {source}")

# 使用示例
df = load_data("data/sales.csv")
```

### 数据缓存策略
```python
import streamlit as st

# 缓存数据函数
@st.cache_data(ttl=3600)  # 1小时过期
def get_sales_data():
    return pd.read_csv("sales.csv")

# 缓存资源（如ML模型）
@st.cache_resource
def init_model():
    return load_ml_model("model.pkl")
```

### Session State 管理
```python
import streamlit as st

# 初始化 session state
if 'df' not in st.session_state:
    st.session_state.df = None

if st.session_state.df is None:
    st.session_state.df = load_data("data.csv")
```

## 资源索引
- Streamlit 官方文档：https://docs.streamlit.io/
- Streamlit 多页面：https://docs.streamlit.io/develop/concepts/multipage-apps
- 配置参考：https://docs.streamlit.io/develop/api-reference/configuration/config.toml

## 注意事项
- 使用 @st.cache_data 缓存耗时数据加载操作
- Session State 用于跨 rerun 保持用户状态
- 合理拆分页面，每个页面职责单一
- 使用子目录组织页面和组件
