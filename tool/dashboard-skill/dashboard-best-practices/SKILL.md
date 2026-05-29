---
name: dashboard-best-practices
version: v2.0.0
author: book-skills
description: 数据看板最佳实践技能，掌握性能优化、状态管理、错误处理和安全部署，构建生产级数据应用
---

# Dashboard Best Practices

## 任务目标
- 本 Skill 用于：遵循数据看板开发最佳实践，构建生产级应用
- 能力包含：性能优化、状态管理、错误处理、安全部署、测试策略
- 触发条件：需要提升看板性能、可靠性和可维护性时

## 操作步骤

### 性能优化

#### 缓存策略选择
```python
import streamlit as st
import pandas as pd

# @st.cache_data：缓存可序列化数据（DataFrame、字典等）
@st.cache_data(ttl=3600)  # 1小时过期
def load_data(source: str) -> pd.DataFrame:
    return pd.read_csv(source)

# @st.cache_resource：缓存不可序列化对象（数据库连接、ML模型）
@st.cache_resource
def get_db_connection():
    from sqlalchemy import create_engine
    return create_engine("sqlite:///data.db")

# 选择指南：
# - 返回 DataFrame/列表/字典 → @st.cache_data
# - 返回数据库连接/模型对象 → @st.cache_resource
# - 需要自动过期 → 设置 ttl 参数
```

#### 避免不必要的重算
```python
# 使用 session_state 缓存中间计算结果
if 'processed_df' not in st.session_state:
    st.session_state.processed_df = heavy_processing(raw_df)

# 使用回调函数避免 rerun
def on_filter_change():
    st.session_state.filter_applied = True

st.selectbox("类别", options, on_change=on_filter_change)
```

#### 查询优化
```python
# 数据库层预聚合，减少传输数据量
@st.cache_data
def get_daily_summary():
    return pd.read_sql("""
        SELECT date, category, SUM(amount) as total
        FROM orders
        WHERE date >= :start_date
        GROUP BY date, category
    """, engine, params={"start_date": "2024-01-01"})
```

### 状态管理

#### Session State 模式
```python
# 初始化模式
def init_state():
    defaults = {
        "filters": {"category": None, "date_range": None},
        "page": 1,
        "data": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

# 更新模式
def apply_filters(category, date_range):
    st.session_state.filters = {
        "category": category,
        "date_range": date_range,
    }
    st.session_state.page = 1  # 重置分页
```

#### 跨页面状态共享
```python
# utils/state_manager.py
class AppState:
    """集中管理应用状态"""
    
    @staticmethod
    def get(key, default=None):
        return st.session_state.get(key, default)
    
    @staticmethod
    def set(key, value):
        st.session_state[key] = value
    
    @staticmethod
    def clear_filters():
        st.session_state.filters = {"category": None, "date_range": None}
```

### 错误处理

#### 分层错误处理
```python
import streamlit as st
import pandas as pd

def load_data_safely(source: str) -> pd.DataFrame | None:
    """安全加载数据，返回 None 表示失败"""
    try:
        if source.endswith('.csv'):
            return pd.read_csv(source)
        elif source.endswith('.xlsx'):
            return pd.read_excel(source)
        else:
            st.error(f"不支持的文件格式: {source}")
            return None
    except FileNotFoundError:
        st.error(f"文件不存在: {source}")
        return None
    except pd.errors.EmptyDataError:
        st.warning("文件为空")
        return None
    except Exception as e:
        st.error(f"加载失败: {e}")
        return None

# 使用
df = load_data_safely("data.csv")
if df is None:
    st.stop()  # 停止后续执行
```

#### 用户友好的错误提示
```python
# 使用不同级别的提示
st.error("严重错误，无法继续")      # 红色
st.warning("警告，结果可能不准确")   # 黄色
st.info("提示信息")                # 蓝色
st.success("操作成功")             # 绿色

# 异常展开（仅开发环境）
try:
    result = risky_operation()
except Exception as e:
    if st.secrets.get("debug", False):
        st.exception(e)  # 显示完整堆栈
    else:
        st.error("处理失败，请联系管理员")
```

### 数据安全

#### Secrets 管理
```python
# .streamlit/secrets.toml
[database]
host = "localhost"
port = 5432
user = "admin"
password = "your_password"

[api]
key = "your_api_key"

# 代码中使用
import streamlit as st

db_password = st.secrets["database"]["password"]
api_key = st.secrets["api"]["key"]
```

#### 输入验证
```python
def validate_date_range(start, end):
    if start > end:
        st.error("开始日期不能晚于结束日期")
        return False
    if (end - start).days > 365:
        st.warning("查询范围超过一年，加载可能较慢")
    return True

def validate_file_size(uploaded_file, max_mb=10):
    if uploaded_file.size > max_mb * 1024 * 1024:
        st.error(f"文件大小超过限制 ({max_mb}MB)")
        return False
    return True
```

### 部署配置

#### Docker 部署
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### docker-compose.yml
```yaml
services:
  dashboard:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

### 测试策略

#### Streamlit 应用测试
```python
# test_app.py
from streamlit.testing.v1 import AppTest

def test_app_loads():
    at = AppTest.from_file("app.py")
    at.run()
    assert not at.exception
    assert at.title[0].value == "数据看板"

def test_filter_interaction():
    at = AppTest.from_file("app.py")
    at.run()
    at.selectbox[0].select("科技").run()
    assert not at.exception
    assert len(at.dataframe) > 0
```

#### 数据处理测试
```python
# test_data_loader.py
import pandas as pd
import pytest
from utils.data_loader import load_data, clean_data

def test_load_csv():
    df = load_data("tests/fixtures/sample.csv")
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0

def test_clean_data_handles_missing():
    df = pd.DataFrame({"a": [1, None, 3]})
    cleaned = clean_data(df)
    assert cleaned["a"].isnull().sum() == 0
```

## 资源索引
- Streamlit 部署：https://docs.streamlit.io/deploy/
- Streamlit 测试：https://docs.streamlit.io/develop/api-reference/testing
- Streamlit 缓存：https://docs.streamlit.io/develop/api-reference/caching
- Streamlit 安全：https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app

## 注意事项
- 根据数据类型选择合适的缓存装饰器
- 所有外部输入都必须验证
- 敏感信息必须使用 secrets 管理
- 测试应覆盖数据处理和界面交互
