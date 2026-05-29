# 主题元素

## 目录
- [element_rect](#element_rect)
- [element_line](#element_line)
- [element_text](#element_text)
- [element_blank](#element_blank)

## element_rect
矩形元素：
```python
from plotnine import element_rect

element_rect(
    fill=None,        # 填充颜色
    color=None,       # 边框颜色
    size=None,        # 边框大小
    linetype=None     # 线型
)
```

使用示例：
```python
theme(
    plot_background=element_rect(fill="white"),
    panel_background=element_rect(fill="lightgray"),
    legend_background=element_rect(fill="transparent")
)
```

## element_line
线条元素：
```python
from plotnine import element_line

element_line(
    color=None,     # 颜色
    size=None,      # 大小
    linetype=None   # 线型
)
```

## element_text
文本元素：
```python
from plotnine import element_text

element_text(
    family=None,      # 字体
    face=None,        # 字重（bold, italic）
    color=None,       # 颜色
    size=None,        # 大小
    hjust=None,       # 水平对齐
    vjust=None,       # 垂直对齐
    angle=None        # 旋转角度
)
```

## element_blank
移除元素：
```python
from plotnine import element_blank

theme(
    panel_grid_minor=element_blank(),
    axis_ticks_minor=element_blank()
)
```
