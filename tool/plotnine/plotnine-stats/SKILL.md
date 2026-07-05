---
name: plotnine-stats
description: 掌握Plotnine统计变换层，包括数据聚合、密度估计、回归分析、计数统计等stat转换及其与geom的配对
dependency:
  python:
    - plotnine>=0.12.0
---

# Plotnine Stats

## 任务目标
- 本 Skill 用于：掌握 Plotnine 统计变换功能，实现数据聚合和计算
- 能力包含：直方图统计、密度估计、回归分析、汇总统计
- 触发条件：当用户需要对数据进行统计计算后再绑图时

## 前置准备
- 环境要求：已完成 plotnine-basics 学习

## 操作步骤

### 标准流程

#### 1. 直方图统计 (stat_bin)
```python
from plotnine import ggplot, aes, geom_histogram

(
    ggplot(df, aes("value"))
    + geom_histogram(bins=30, fill="steelblue", alpha=0.7)
)
```

#### 2. 密度估计 (stat_density)
```python
from plotnine import stat_density

(
    ggplot(df, aes("value", fill="category"))
    + stat_density(alpha=0.5)
)
```

#### 3. 平滑回归 (stat_smooth)
```python
from plotnine import geom_smooth

(
    ggplot(df, aes("x", "y"))
    + geom_smooth(method="lm", se=True)  # 线性回归 + 置信区间
    + geom_point()
)
```

#### 4. 计数统计 (stat_count)
```python
from plotnine import geom_bar

ggplot(df, aes("category")) + geom_bar()
# 等价于 ggplot(df, aes("category")) + geom_bar(stat="count")
```

#### 5. 汇总统计 (stat_summary)
```python
from plotnine import stat_summary

(
    ggplot(df, aes("category", "value"))
    + stat_summary(fun_y="mean", geom="point", size=3)
    + stat_summary(fun_ymin="mean", fun_ymax="mean", geom="errorbar")
)
```

### 常用 Stat速查

| Stat | 功能 | 配对 Geom |
|------|------|----------|
| stat_bin | 分箱计数 | geom_histogram, geom_freqpoly |
| stat_count | 计数 | geom_bar |
| stat_density | 密度估计 | geom_density |
| stat_smooth | 平滑回归 | geom_smooth |
| stat_boxplot | 箱线图统计 | geom_boxplot |
| stat_summary | 汇总统计 | point, errorbar, ribbon |
| stat_ecdf | 经验累积分布 | line |
| stat_qq | Q-Q 图 | geom_qq |
| stat_function | 函数曲线 | - |
| stat_identity | 原始数据 | 任意 |

### 可选分支

#### 当需要使用 after_stat() 时
```python
from plotnine import aes, after_stat

(
    ggplot(df, aes("x", y=after_stat("count / sum(count)")))
    + geom_bar()
)
```

## 资源索引

### 领域参考
- [references/stat-bin-density.md](references/stat-bin-density.md)
  - 何时读取：需要创建直方图或密度图时
  - 内容：stat_bin, stat_density, bins, kernel, adjust

- [references/stat-smooth-summary.md](references/stat-smooth-summary.md)
  - 何时读取：需要回归分析或汇总统计时
  - 内容：stat_smooth, stat_summary, method 参数

## 注意事项

### Stat vs Geom
- stat 是数据转换，geom 是视觉表示
- 同一 stat 可配不同 geom
- 使用 `geom_xxx(stat="xxx")` 或 `stat_xxx(geom="xxx")`

### 访问计算值
- 使用 after_stat() 在 aes 中访问 stat 计算的值
- 常用计算值：count, density, n, xmin, xmax
