# 出版级图表

## 目录
- [Tufte 主题](#tufte-主题)
- [坐标轴定制](#坐标轴定制)
- [完整示例](#完整示例)

## Tufte 主题
```python
from plotnine import theme_tufte

(
    ggplot(df, aes("x", "y"))
    + geom_point(color="steelblue", size=3)
    + theme_tufte(base_family="Arial", base_size=12)
)
```

## 坐标轴定制
```python
from plotnine import element_line

(
    ggplot(df, aes("x", "y"))
    + geom_point()
    + theme_tufte()
    + theme(
        axis_line=element_line(color="#4d4d4d"),
        axis_ticks_major=element_line(color="#00000000"),
        axis_title=element_blank()
    )
)
```

## 完整示例
```python
from plotnine import *

(
    ggplot(anscombe_quartet, aes("x", "y"))
    + geom_point(color="sienna", fill="orange", size=3)
    + geom_smooth(method="lm", se=False, color="steelblue", size=1)
    + facet_wrap("dataset")
    + labs(title="Anscombe's Quartet")
    + scale_y_continuous(breaks=(4, 8, 12))
    + coord_fixed(xlim=(3, 22), ylim=(2, 14))
    + theme_tufte(base_family="Arial", base_size=16)
    + theme(
        axis_line=element_line(color="#4d4d4d"),
        panel_spacing=0.09
    )
)
```
