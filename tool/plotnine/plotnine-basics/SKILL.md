---
name: plotnine-basics
description: 掌握Plotnine基础语法，包括ggplot对象创建、美学映射、数据框支持、基础绑图流程和管道操作
dependency:
  python:
    - plotnine>=0.12.0
    - pandas>=1.5.0
---

# Plotnine Basics

## 任务目标
- 本 Skill 用于：掌握 Plotnine 数据可视化的基础语法和核心概念
- 能力包含：ggplot 创建、aes 美学映射、DataFrame 支持、管道操作、图表保存
- 触发条件：当用户需要使用 Plotnine 创建基础数据可视化时

## 前置准备
- 环境安装：
  ```bash
  pip install plotnine pandas
  # 或安装完整依赖
  pip install 'plotnine[extra]'
  ```

## 操作步骤

### 标准流程

#### 1. 创建基础散点图
```python
from plotnine import ggplot, aes, geom_point, labs
from plotnine.data import penguins

(
    ggplot(penguins, aes("bill_length_mm", "bill_depth_mm", color="species"))
    + geom_point()
)
```

#### 2. 理解 ggplot 核心概念
```python
ggplot(data, mapping)
```
- `data`：DataFrame 数据
- `mapping`：aes() 美学映射
- 使用 `+` 添加图层

#### 3. 美学映射 (aes)
```python
aes(x="column1", y="column2")
aes(x="column1", y="column2", color="category")
aes(x="column1", y="column2", size="numeric_col", alpha="category")
```

#### 4. DataFrame 支持
```python
import pandas as pd
import polars as pl

# Pandas
df = pd.DataFrame({...})
ggplot(df, aes("x", "y"))

# Polars 支持管道操作
df_pl = pl.from_pandas(df)
df_pl >> ggplot(aes("x", "y")) + geom_point()
```

#### 5. 保存图表
```python
# 方法1：使用 save 方法
p = ggplot(df, aes("x", "y")) + geom_point()
p.save("plot.png", width=4, height=3, dpi=300)

# 方法2：显示图表
p.show()
```

### 可选分支

#### 当需要多图层时
```python
(
    ggplot(df, aes("x", "y"))
    + geom_point()           # 第一层：散点
    + geom_smooth(method="lm")  # 第二层：平滑线
    + labs(title="Title", x="X Label", y="Y Label")
)
```

## 资源索引

### 必要脚本
- scripts/quick_plot.py：快速绑图脚本

### 领域参考
- [references/ggplot.md](references/ggplot.md)
  - 何时读取：需要深入了解 ggplot 对象时
  - 内容：ggplot 参数、方法、save/draw/show

- [references/aes.md](references/aes.md)
  - 何时读取：需要使用美学映射时
  - 内容：aes 参数、映射类型、after_stat/after_scale

- [references/dataframe-support.md](references/dataframe-support.md)
  - 何时读取：需要处理数据框时
  - 内容：Pandas/Polars 支持、管道操作

## 注意事项

### 字符串表达式
- 在 aes 中使用字符串引用列名
- 支持 numpy 和 pandas 函数
- 使用 after_stat() 访问统计计算的变量

### 性能
- 大数据集可能渲染较慢
- 使用 sample() 采样数据进行快速探索
