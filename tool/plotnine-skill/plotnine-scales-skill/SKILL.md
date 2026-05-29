---
name: plotnine-scales
description: 掌握Plotnine标度系统，包括颜色、位置、大小、形状等视觉属性的映射控制和图例/坐标轴定制
dependency:
  python:
    - plotnine>=0.12.0
---

# Plotnine Scales

## 任务目标
- 本 Skill 用于：掌握 Plotnine 标度系统，自定义图表的视觉映射
- 能力包含：颜色标度、位置标度、大小标度、分面布局
- 触发条件：当用户需要自定义图表的视觉映射或创建分面图时

## 前置准备
- 环境要求：已完成 plotnine-basics-skill 学习

## 操作步骤

### 标准流程

#### 1. 颜色标度 (scale_color_* / scale_fill_*)
```python
from plotnine import scale_color_brewer, scale_fill_brewer

# 离散颜色
ggplot(df, aes("x", "y", color="category")) + scale_color_brewer(type="qual")

# 连续颜色
ggplot(df, aes("x", "y", fill="value")) + scale_fill_gradient(low="blue", high="red")

# 分段颜色
ggplot(df, aes("x", "y", fill="value")) + scale_fill_gradient2(low="red", high="blue", mid="white")
```

#### 2. 位置标度 (scale_x_* / scale_y_*)
```python
from plotnine import scale_x_log10, scale_y_continuous, xlim, ylim

# 对数坐标
ggplot(df, aes("x", "y")) + scale_x_log10()

# 限制范围
ggplot(df, aes("x", "y")) + xlim(0, 100) + ylim(0, 50)

# 连续
ggplot(df, aes("x", "y")) + scale_y_continuous(breaks=[0, 25, 50, 75, 100])
```

#### 3. 大小标度 (scale_size_*)
```python
from plotnine import scale_size

ggplot(df, aes("x", "y", size="value")) + scale_size(range=(1, 10))
```

#### 4. 手动标度 (scale_*_manual)
```python
from plotnine import scale_color_manual

ggplot(df, aes("x", "y", color="category")) + scale_color_manual(
    values={"A": "red", "B": "blue", "C": "green"}
)
```

### 常用 Scale速查

| 类型 | 函数 | 用途 |
|------|------|------|
| 颜色-离散 | scale_color_brewer, scale_color_hue | 分类数据 |
| 颜色-连续 | scale_color_gradient, scale_color_cmap | 数值数据 |
| 位置 | scale_x_continuous, scale_y_log10 | 坐标轴 |
| 大小 | scale_size, scale_size_area | 点大小映射 |
| 形状 | scale_shape_manual | 分类形状 |
| 透明度 | scale_alpha | 数值/分类 |

### 可选分支

#### 当需要分面时
```python
from plotnine import facet_wrap, facet_grid

# 按单变量分面
ggplot(df, aes("x", "y")) + geom_point() + facet_wrap("category")

# 按双变量分面
ggplot(df, aes("x", "y")) + geom_point() + facet_grid("row ~ col")
```

## 资源索引

### 领域参考
- [references/scale-color.md](references/scale-color.md)
  - 何时读取：需要自定义颜色映射时
  - 内容：brewer, gradient, hue, manual 颜色标度

- [references/scale-position.md](references/scale-position.md)
  - 何时读取：需要自定义坐标轴时
  - 内容：continuous, log10, discrete, limits

- [references/facet.md](references/facet.md)
  - 何时读取：需要创建分面图时
  - 内容：facet_wrap, facet_grid, labeller

## 注意事项

### 标度命名约定
- scale_color_*：线条/点颜色
- scale_fill_*：填充颜色
- scale_shape_*：点形状
- scale_linetype_*：线型

### lims() 函数
```python
from plotnine import lims

lims(x=(0, 100), y=(0, 50))  # 同时设置x和y范围
```
