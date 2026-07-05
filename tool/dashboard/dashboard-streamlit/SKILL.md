---
name: dashboard-streamlit
version: v2.0.0
author: book-skills
description: Streamlit 数据展示技能，掌握文本、图表、表格、交互组件的用法，实现丰富的数据可视化界面
---

# Dashboard Streamlit

## 任务目标
- 本 Skill 用于：使用 Streamlit 组件构建数据展示界面
- 能力包含：文本显示、数据表格、图表渲染、表单输入
- 触发条件：需要在看板中展示数据或接收用户输入时

## 操作步骤

### 文本显示
```python
import streamlit as st

st.title("页面标题")
st.header("章节标题")
st.subheader("子标题")
st.markdown("**加粗** 和 *斜体* 文本")
st.caption("小字体说明文字")
st.code("print('Hello')", language="python")
st.text("固定宽度文本")
st.divider()
```

### 数据展示
```python
import streamlit as st
import pandas as pd

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'score': [85, 92, 78]
})

# 交互式表格
st.dataframe(df, hide_index=True)

# 静态表格
st.table(df)

# 编辑数据
edited_df = st.data_editor(df, num_rows="dynamic")
```

### 指标展示
```python
import streamlit as st

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("总收入", "¥1,234,567", "+12.5%")

with col2:
    st.metric("用户数", "8,888", "+5.2%")

with col3:
    st.metric("转化率", "3.8%", "-0.3%")
```

### 图表组件
```python
import streamlit as st
import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C'])

# 内置图表
st.line_chart(df)
st.area_chart(df)
st.bar_chart(df)
st.scatter_chart(df)

# 地图
st.map(df[['lat', 'lon']])
```

### PyDeck 图表
```python
import streamlit as st
import pydeck as pdk

st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(latitude=37.76, longitude=-122.4, zoom=11),
    layers=[pdk.Layer('ScatterplotLayer', data=df, get_position='[lon, lat]')]
))
```

### 表单与输入
```python
import streamlit as st

with st.form(key='my_form'):
    name = st.text_input("姓名")
    choice = st.selectbox("选择", ["A", "B", "C"])
    submitted = st.form_submit_button("提交")

if submitted:
    st.success(f"收到: {name}, {choice}")
```

### 侧边栏
```python
import streamlit as st

with st.sidebar:
    st.title("筛选")
    min_val = st.slider("最小值", 0, 100, 50)
    options = st.multiselect("类别", ["科技", "金融", "医疗"])

st.write(f"选择了: {min_val}, {options}")
```

### 标签页和折叠
```python
import streamlit as st

tab1, tab2, tab3 = st.tabs(["销售", "用户", "库存"])

with tab1:
    st.write("销售数据")

with tab2:
    st.write("用户数据")

with st.expander("查看详情"):
    st.write("详细数据...")
```

### 布局容器
```python
import streamlit as st

# 横向布局
col1, col2 = st.columns([2, 1])
with col1:
    st.line_chart(data)
with col2:
    st.metric("当前值", value)

# 空容器（动态替换）
placeholder = st.empty()
placeholder.line_chart(data)

# 模态对话框
@st.dialog("确认")
def confirm():
    if st.button("确定"):
        st.session_state.confirmed = True
```

### 文件上传与下载
```python
import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("上传 CSV", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

# 下载
csv = df.to_csv(index=False)
st.download_button("下载 CSV", csv, "data.csv")
```

### 状态与反馈
```python
import streamlit as st

# 加载状态
with st.spinner("加载中..."):
    result = load_data()

st.success("加载完成!")

# Toast 提示
st.toast("操作成功", icon="✅")

# 进度条
progress = st.progress(0)
for i in range(100):
    progress.progress(i + 1)

# 气球庆祝
st.balloons()
```

## 资源索引
- Streamlit API：https://docs.streamlit.io/develop/api-reference
- 文本组件：https://docs.streamlit.io/develop/api-reference/text
- 数据框架：https://docs.streamlit.io/develop/api-reference/data
- 图表：https://docs.streamlit.io/develop/api-reference/charts
- 组件：https://docs.streamlit.io/develop/api-reference/components

## 注意事项
- st.dataframe 支持排序和筛选，适合大数据
- st.table 适合小数据静态展示
- 表单使用 with st.form() 批量提交
- 侧边栏适合放置筛选器
