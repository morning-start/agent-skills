---
name: dashboard-pandas
version: v2.0.0
author: book-skills
description: Pandas 数据处理技能，掌握数据读取、清洗、转换和聚合，为数据看板提供高质量的数据源
---

# Dashboard Pandas

## 任务目标
- 本 Skill 用于：使用 Pandas 进行数据处理和准备
- 能力包含：数据读取、数据清洗、数据转换、数据聚合
- 触发条件：需要处理外部数据或准备看板数据源时

## 操作步骤

### 数据读取
```python
import pandas as pd

# CSV 文件
df = pd.read_csv('data.csv')

# Excel 文件
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# JSON
df = pd.read_json('data.json')

# SQL
from sqlalchemy import create_engine
engine = create_engine('sqlite:///data.db')
df = pd.read_sql('SELECT * FROM table', engine)

# URL
df = pd.read_csv('https://example.com/data.csv')
```

### 数据预览
```python
# 基本信息
df.head()           # 前5行
df.tail()           # 后5行
df.info()           # 数据类型和缺失值
df.describe()       # 统计描述
df.shape            # 行列数
df.columns          # 列名列表
df.dtypes           # 每列数据类型
```

### 数据选择
```python
# 列选择
df['name']              # 单列
df[['name', 'age']]    # 多列

# 行选择
df.iloc[0:10]          # 位置索引
df.loc[0:10]          # 标签索引

# 条件筛选
df[df['age'] > 18]                    # 单条件
df[(df['age'] > 18) & (df['city'] == 'Beijing')]  # 多条件

# 查询语法
df.query('age > 18 and city == "Beijing"')
```

### 数据清洗
```python
# 缺失值处理
df.isnull().sum()           # 统计缺失值
df.dropna()                 # 删除缺失行
df.fillna(0)                # 填充缺失值
df['col'].fillna(df['col'].mean())  # 用均值填充

# 重复值处理
df.duplicated().sum()       # 统计重复
df.drop_duplicates()       # 删除重复

# 类型转换
df['date'] = pd.to_datetime(df['date'])
df['price'] = df['price'].astype(float)
```

### 数据转换
```python
# 列重命名
df.rename(columns={'old': 'new', 'col2': 'name2'})

# 添加/修改列
df['total'] = df['price'] * df['quantity']
df['year'] = df['date'].dt.year

# 删除列
df.drop(columns=['col1', 'col2'])

# 排序
df.sort_values('price', ascending=False)
df.sort_index()

# 字符串处理
df['name'].str.lower()
df['name'].str.strip()
df['code'].str.contains('ABC')
```

### 数据聚合
```python
# 分组统计
df.groupby('category')['price'].sum()
df.groupby('category').agg({'price': 'sum', 'quantity': 'mean'})

# 透视表
pd.pivot_table(df, values='sales', index='region', columns='quarter', aggfunc='sum')

# 交叉表
pd.crosstab(df['A'], df['B'])

# 时间序列重采样
df.set_index('date').resample('M')['sales'].sum()
```

### 数据合并
```python
# 合并
pd.merge(df1, df2, on='key', how='inner')

# 拼接
pd.concat([df1, df2], axis=0)   # 纵向
pd.concat([df1, df2], axis=1)   # 横向

# 追加
df1.append(df2)
```

### 常用统计
```python
# 描述统计
df['price'].count()
df['price'].mean()
df['price'].median()
df['price'].std()
df['price'].quantile([0.25, 0.5, 0.75])

# 累计计算
df['cumsum'] = df['value'].cumsum()
df['pct_change'] = df['value'].pct_change()

# 排名
df['rank'] = df['score'].rank(ascending=False)
```

### 数据导出
```python
# CSV
df.to_csv('output.csv', index=False)

# Excel
df.to_excel('output.xlsx', index=False)

# JSON
df.to_json('output.json', orient='records')

# 剪贴板
df.to_clipboard()
```

## 资源索引
- Pandas 文档：https://pandas.pydata.org/docs/
- 10分钟入门：https://pandas.pydata.org/docs/user_guide/10min.html
- 数据清洗：https://pandas.pydata.org/docs/user_guide/missing_data.html
- 分组聚合：https://pandas.pydata.org/docs/user_guide/groupby.html

## 注意事项
- 读取大文件时使用 chunksize 分块读取
- 使用 query() 提高复杂筛选可读性
- 避免在循环中修改 DataFrame，使用向量化操作
- 处理时间序列时先 set_index 再操作
