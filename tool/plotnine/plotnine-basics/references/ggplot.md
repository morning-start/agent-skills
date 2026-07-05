# ggplot 对象

## 目录
- [概览](#概览)
- [参数](#参数)
- [方法](#方法)
- [示例](#示例)

## 概览
ggplot 是 Plotnine 的核心对象，用于创建绑图。

## 参数
| 参数 | 类型 | 说明 |
|------|------|------|
| data | DataLike | 绑图数据 |
| mapping | aes | 美学映射 |

## 方法
| 方法 | 说明 |
|------|------|
| show() | 显示图表 |
| draw() | 渲染图表 |
| save() | 保存为图片 |

## save() 参数
| 参数 | 类型 | 说明 |
|------|------|------|
| filename | str | 文件名 |
| format | str | 图片格式 |
| width | float | 宽度 |
| height | float | 高度 |
| dpi | int | DPI |

## 示例
```python
from plotnine import ggplot, aes, geom_point

p = ggplot(df, aes("x", "y"))
p + geom_point()
p.save("plot.png", width=4, height=3, dpi=300)
```
