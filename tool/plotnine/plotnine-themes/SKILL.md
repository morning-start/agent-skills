---
name: plotnine-themes
description: 掌握Plotnine主题系统，包括预置主题、自定义元素、主题可配置项和出版级图表样式定制
dependency:
  python:
    - plotnine>=0.12.0
---

# Plotnine Themes

## 任务目标
- 本 Skill 用于：掌握 Plotnine 主题系统，自定义图表非数据元素的样式
- 能力包含：预置主题、主题元素、自定义主题、出版级图表
- 触发条件：当用户需要美化和定制图表外观时

## 前置准备
- 环境要求：已完成 plotnine-basics 学习

## 操作步骤

### 标准流程

#### 1. 使用预置主题
```python
from plotnine import theme_minimal, theme_bw, theme_classic, theme_void

(
    ggplot(df, aes("x", "y"))
    + geom_point()
    + theme_minimal()  # 简洁主题
)
```

#### 2. 常用预置主题

| 主题 | 特点 |
|------|------|
| theme_minimal | 最小化背景 |
| theme_bw | 黑白网格 |
| theme_classic | 经典无网格 |
| theme_dark | 暗色主题 |
| theme_light | 浅色线条 |
| theme_matplotlib | Matplotlib 风格 |
| theme_tufte | Tufte 极简风格 |
| theme_xkcd | XKCD 手绘风格 |

#### 3. 自定义主题元素
```python
from plotnine import theme, element_rect, element_line, element_text

(
    ggplot(df, aes("x", "y"))
    + geom_point()
    + theme(
        plot_background=element_rect(fill="white"),
        panel_background=element_rect(fill="lightgray"),
        axis_line=element_line(color="black"),
        axis_text=element_text(size=12),
        title=element_text(size=14, weight="bold")
    )
)
```

#### 4. 图例和位置
```python
(
    ggplot(df, aes("x", "y", color="category"))
    + geom_point()
    + theme(
        legend_position="right",  # top, bottom, left, none
        legend_title=element_text(size=12),
        legend_text=element_text(size=10)
    )
)
```

#### 5. 坐标轴和网格
```python
(
    ggplot(df, aes("x", "y"))
    + geom_point()
    + theme(
        panel_grid_major=element_line(color="gray", size=0.5),
        panel_grid_minor=element_blank(),
        axis_ticks_major=element_line(color="black"),
        axis_ticks_minor=element_blank()
    )
)
```

### 可选分支

#### 当需要出版级图表时
```python
from plotnine import theme_tufte, element_line

(
    ggplot(df, aes("x", "y"))
    + geom_point(color="steelblue", size=3)
    + geom_smooth(method="lm", color="darkred", se=False)
    + theme_tufte(base_family="Arial", base_size=12)
    + theme(
        axis_line=element_line(color="#4d4d4d"),
        axis_ticks_major=element_line(color="#00000000")
    )
)
```

## 资源索引

### 领域参考
- [references/theme-presets.md](references/theme-presets.md)
  - 何时读取：需要选择主题时
  - 内容：所有预置主题对比和使用场景

- [references/theme-elements.md](references/theme-elements.md)
  - 何时读取：需要自定义主题时
  - 内容：element_rect, element_line, element_text, element_blank

- [references/theme-publication.md](references/theme-publication.md)
  - 何时读取：需要出版级样式时
  - 内容：Tufte 主题、字体设置、边框调整

## 注意事项

### Themeable 元素类型
- element_rect：矩形（背景、面板）
- element_line：线条（轴线、网格）
- element_text：文本（标签、标题）
- element_blank()：移除元素

### 全局主题设置
```python
from plotnine import theme_minimal

# 设置当前全局主题
theme_minimal()

# 或使用 with_options
from plotnine import options
options.figure_size = (6, 4)
```
