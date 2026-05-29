---
name: analytics-data-processing
description: 数据获取与处理技能，掌握数据采集、清洗、转换、建模全链路，具备构建高质量分析数据的能力
---

# Analytics Data Processing

## 任务目标
- 本 Skill 用于：掌握数据从获取到建模的完整处理流程
- 能力包含：数据获取、数据清洗、数据转换、数据建模
- 触发条件：需要准备分析数据、构建数据模型时

## 数据获取

### 数据源类型

| 类型 | 来源 | 获取方式 |
|------|------|----------|
| 业务系统 | CRM、ERP、电商等 | 数据库直连、API |
| 用户行为 | APP、Web、小程序 |埋点数据、日志 |
| 外部数据 | 第三方、公开数据 | 文件导入、爬虫 |
| 实时数据 | IoT、传感器 | 流式采集 |

### 数据获取模式

#### 批量获取
```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:pass@host:5432/db')

df = pd.read_sql("""
    SELECT *
    FROM orders
    WHERE created_at >= '2024-01-01'
""", engine)
```

#### API获取
```python
import requests
import pandas as pd

response = requests.get(
    'https://api.example.com/data',
    params={
        'start_date': '2024-01-01',
        'end_date': '2024-12-31',
        'page': 1,
        'page_size': 1000
    },
    headers={'Authorization': 'Bearer xxx'}
)

data = response.json()['data']
df = pd.DataFrame(data)
```

#### 文件导入
```python
import pandas as pd

df_csv = pd.read_csv('data.csv', encoding='utf-8')
df_excel = pd.read_excel('data.xlsx', sheet_name='Sheet1')
df_json = pd.read_json('data.json', orient='records')
```

### 数据质量评估

```python
def assess_data_quality(df):
    report = {
        'total_rows': len(df),
        'total_cols': len(df.columns),
        'missing_values': df.isnull().sum().to_dict(),
        'missing_rate': (df.isnull().sum() / len(df) * 100).to_dict(),
        'duplicates': df.duplicated().sum(),
        'dtypes': df.dtypes.to_dict()
    }
    return report
```

## 数据清洗

### 缺失值处理

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'A': [1, 2, np.nan, 4],
    'B': [5, np.nan, np.nan, 8],
    'C': ['a', 'b', 'c', 'd']
})

df_dropna = df.dropna()

df_fill_mean = df.fillna(df.mean())

df_fill_forward = df.fillna(method='ffill')

df_interpolate = df.interpolate()
```

### 异常值处理

```python
import pandas as pd
import numpy as np

def handle_outliers(df, column, method='iqr'):
    if method == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        return df[(df[column] >= lower) & (df[column] <= upper)]
    elif method == 'zscore':
        z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
        return df[z_scores < 3]

df_clean = handle_outliers(df, 'amount', method='iqr')
```

### 数据类型转换

```python
df['date'] = pd.to_datetime(df['date'])
df['price'] = df['price'].astype(float)
df['category'] = df['category'].astype('category')
df['flag'] = df['flag'].map({'Y': 1, 'N': 0})
```

### 重复值处理

```python
df_dedup = df.drop_duplicates()
df_dedup_subset = df.drop_duplicates(subset=['order_id', 'product_id'])
```

## 数据转换

### 聚合统计

```python
sales_summary = df.groupby(['year', 'month', 'category'])['amount'].agg([
    ('销量', 'sum'),
    ('笔数', 'count'),
    ('均价', 'mean'),
    ('最大值', 'max'),
    ('最小值', 'min')
]).reset_index()
```

### 透视表

```python
pivot = pd.pivot_table(
    df,
    values='amount',
    index=['year', 'month'],
    columns='category',
    aggfunc='sum',
    fill_value=0
)
```

### 时间序列转换

```python
df.set_index('date', inplace=True)

df_daily = df.resample('D').sum()
df_monthly = df.resample('M').sum()
df_quarterly = df.resample('Q').sum()

df_rolling = df['amount'].rolling(window=7).mean()
df_cumulative = df['amount'].expanding().sum()
```

### 数据归一化

```python
from sklearn.preprocessing import MinMaxScaler, StandardScaler

scaler = MinMaxScaler()
df_normalized = pd.DataFrame(
    scaler.fit_transform(df[['amount', 'quantity']]),
    columns=['amount_norm', 'quantity_norm']
)

scaler = StandardScaler()
df_standardized = pd.DataFrame(
    scaler.fit_transform(df[['amount', 'quantity']]),
    columns=['amount_std', 'quantity_std']
)
```

## 数据建模

### 维度表设计

```python
dim_user = pd.DataFrame({
    'user_id': [1, 2, 3],
    'user_name': ['张三', '李四', '王五'],
    'user_type': ['VIP', '普通', 'VIP'],
    'join_date': ['2023-01-01', '2023-06-15', '2023-03-20'],
    'age_group': ['25-30', '31-35', '26-30']
})
```

### 事实表设计

```python
fact_orders = pd.DataFrame({
    'order_id': [1001, 1002, 1003],
    'user_id': [1, 2, 1],
    'product_id': [101, 102, 103],
    'order_date': ['2024-01-15', '2024-01-16', '2024-01-18'],
    'amount': [299, 599, 1299],
    'quantity': [1, 2, 1],
    'discount': [0, 50, 100]
})

fact_orders['order_date'] = pd.to_datetime(fact_orders['order_date'])
```

### 指标计算

```python
fact_orders['unit_price'] = fact_orders['amount'] / fact_orders['quantity']

fact_orders['is_vip_order'] = fact_orders['user_id'].map(
    dim_user.set_index('user_id')['user_type'] == 'VIP'
)

fact_orders['order_month'] = fact_orders['order_date'].dt.to_period('M')
```

### 层级汇总

```python
daily_summary = fact_orders.groupby('order_date').agg({
    'order_id': 'count',
    'amount': 'sum',
    'quantity': 'sum'
}).rename(columns={
    'order_id': 'order_count',
    'amount': 'total_amount',
    'quantity': 'total_quantity'
})

monthly_summary = daily_summary.resample('M').sum()
monthly_summary['avg_order_amount'] = (
    monthly_summary['total_amount'] / monthly_summary['order_count']
)
```

## 数据工厂架构

### 典型分层

```
┌─────────────────────────────────────────────────────────────┐
│                    数据工厂分层架构                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐                                          │
│  │  数据应用层  │  ← 面向业务定制，数据产品和分析结果       │
│  └──────┬──────┘                                          │
│         │                                                  │
│  ┌──────┴──────┐                                          │
│  │  汇总明细层  │  ← 主题建模，衍生/复合指标                │
│  └──────┬──────┘                                          │
│         │                                                  │
│  ┌──────┴──────┐                                          │
│  │   整合层    │  ← 数据清洗、转换、统一编码                │
│  └──────┬──────┘                                          │
│         │                                                  │
│  ┌──────┴──────┐                                          │
│  │   贴源层    │  ← 原始数据集成，不做清洗转换             │
│  └─────────────┘                                          │
└─────────────────────────────────────────────────────────────┘
```

### 贴源层（ODS）
```sql
CREATE TABLE ods_orders (
    order_id STRING,
    user_id STRING,
    product_id STRING,
    order_date STRING,
    amount STRING,
    quantity STRING,
    discount STRING,
    etl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 整合层（DWD）
```sql
CREATE TABLE dwd_orders (
    order_id BIGINT,
    user_id BIGINT,
    product_id BIGINT,
    order_date DATE,
    amount DECIMAL(10,2),
    quantity INT,
    discount DECIMAL(10,2),
    is_vip STRING
);
```

### 汇总层（DWS）
```sql
CREATE TABLE dws_user_daily_summary (
    stat_date DATE,
    user_id BIGINT,
    order_count INT,
    order_amount DECIMAL(12,2),
    avg_order_amount DECIMAL(10,2)
);
```

## 常用Python工具

### Pandas 进阶操作

```python
import pandas as pd
import numpy as np

df = pd.read_csv('sales.csv')

df.query('amount > 100 and category == "电子产品"')

df.pipe(lambda x: x[x['amount'] > 0])

df.assign(
    amount_after_discount=lambda x: x['amount'] * (1 - x['discount_rate']),
    month=lambda x: pd.to_datetime(x['date']).dt.month
)

pd.get_dummies(df, columns=['category'], prefix='cat')

df.groupby('user_id').filter(lambda x: len(x) >= 3)
```

### SQL 窗口函数

```sql
SELECT
    order_date,
    user_id,
    amount,
    SUM(amount) OVER (PARTITION BY user_id ORDER BY order_date) as cumulative_amount,
    AVG(amount) OVER (PARTITION BY user_id ORDER BY order_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as rolling_7d_avg,
    LAG(amount, 1) OVER (PARTITION BY user_id ORDER BY order_date) as prev_amount,
    amount - LAG(amount, 1) OVER (PARTITION BY user_id ORDER BY order_date) as amount_change
FROM orders
ORDER BY user_id, order_date;
```

## 数据质量监控

### 监控指标

```python
def data_quality_monitor(df, date_col='order_date'):
    yesterday = pd.Timestamp.now() - pd.Timedelta(days=1)
    today_data = df[df[date_col] == yesterday]

    metrics = {
        'record_count': len(today_data),
        'null_rate': today_data.isnull().mean().to_dict(),
        'duplicate_rate': today_data.duplicated().mean(),
        'amount_sum': today_data['amount'].sum() if 'amount' in today_data else None,
        'amount_avg': today_data['amount'].mean() if 'amount' in today_data else None
    }

    return metrics
```

### 异常检测

```python
def detect_anomaly(df, column, threshold=3):
    mean = df[column].mean()
    std = df[column].std()
    anomalies = df[np.abs(df[column] - mean) > threshold * std]
    return anomalies

def detect_trend_change(df, column, window=7):
    rolling_mean = df[column].rolling(window=window).mean()
    trend_change = np.abs(rolling_mean.diff()) > df[column].std() * 2
    return trend_change
```

## 资源索引
- Pandas 文档：https://pandas.pydata.org/
- 数据建模参考：[数据可视化全链路](https://www.woshipm.com/pd/1562144.html)

## 注意事项
- 数据清洗是数据分析的基础，质量比速度更重要
- 保留原始数据，处理后的数据新建字段
- 数据口径要明确记录，便于后续追溯
- 与业务方确认指标定义，避免理解偏差
