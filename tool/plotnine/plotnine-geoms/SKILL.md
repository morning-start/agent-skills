---
name: plotnine-geoms
description: 掌握Plotnine几何对象层，包括散点图、线图、柱状图、箱线图、密度图等40+种geom的使用方法和场景选择
dependency:
  python:
    - plotnine>=0.12.0
---

# Plotnine Geoms

## 任务目标
- 本 Skill 用于：掌握 Plotnine 各种几何对象的用途和使用方法
- 能力包含：散点图、线图、柱状图、箱线图、密度图、面积图等 geom 选择
- 触发条件：当用户需要创建特定类型的数据可视化图表时

## 前置准备
- 环境要求：已完成 plotnine-basics 学习

## 操作步骤

### 标准流程

#### 1. 散点图 (geom_point)
```python
from plotnine import ggplot, aes, geom_point

(
    ggplot(df, aes("x", "y", color="category"))
    + geom_point(size=3, alpha=0.7)
)
```

#### 2. 线图 (geom_line)
```python
from plotnine import ggplot, aes, geom_line

(
    ggplot(df, aes("time", "value", linetype="group"))
    + geom_line()
)
```

#### 3. 柱状图 (geom_bar / geom_col)
```python
# geom_bar: 计数柱状图
ggplot(df, aes("category")) + geom_bar()

# geom_col: 值柱状图
ggplot(df, aes("category", "value")) + geom_col()
```

#### 4. 箱线图 (geom_boxplot)
```python
from plotnine import geom_boxplot

(
    ggplot(df, aes("category", "value", fill="category"))
    + geom_boxplot(alpha=0.7)
)
```

#### 5. 密度图 (geom_density)
```python
from plotnine import geom_density

(
    ggplot(df, aes("value", fill="category"))
    + geom_density(alpha=0.5)
)
```

### 常用 Geom速查

| Geom | 用途 | 关键参数 |
|------|------|---------|
| geom_point | 散点图 | size, color, shape, alpha |
| geom_line | 线图 | linetype, color, size |
| geom_bar | 计数柱状图 | fill, color |
| geom_col | 值柱状图 | fill, color |
| geom_boxplot | 箱线图 | fill, color, outlier |
| geom_density | 密度图 | fill, color, alpha |
| geom_histogram | 直方图 | bins, fill |
| geom_smooth | 平滑线 | method, se, color |
| geom_jitter | 抖动散点 | width, height |
| geom_violin | 小提琴图 | fill, color, trim |
| geom_area | 面积图 | fill, alpha |
| geom_ribbon | 带状图 | fill, alpha |
| geom_errorbar | 误差棒 | width, size |
| geom_text | 文本标注 | label, size |

### 可选分支

#### 当需要组合多个 geom 时
```python
(
    ggplot(df, aes("x", "y"))
    + geom_point()           # 散点
    + geom_line()            # 线
    + geom_smooth(method="lm")  # 平滑线
)
```

## 资源索引

### 领域参考
- [references/geom-point-line.md](references/geom-point-line.md)
  - 何时读取：需要创建散点图或线图时
  - 内容：geom_point, geom_line, geom_path, geom_jitter

- [references/geom-bar-boxplot.md](references/geom-bar-boxplot.md)
  - 何时读取：需要创建柱状图或箱线图时
  - 内容：geom_bar, geom_col, geom_boxplot, geom_violin

- [references/geom-density-histogram.md](references/geom-density-histogram.md)
  - 何时读取：需要创建分布图时
  - 内容：geom_density, geom_histogram, geom_freqpoly

## 注意事项

### Geom 与 Stat 配对
- geom_bar 默认使用 stat_count
- geom_smooth 默认使用 stat_smooth
- 可以显式指定 stat 参数

### 位置调整 (position)
- position_dodge: 躲避
- position_fill: 堆叠填充
- position_jitter: 抖动减少重叠
- position_stack: 堆叠
