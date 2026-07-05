# 分面 (Facets)

## 目录
- [facet_wrap](#facet_wrap)
- [facet_grid](#facet_grid)

## facet_wrap
按单变量分面：
```python
facet_wrap(facets, nrow=None, ncol=None, scales="fixed")
```

scales 选项：
- "fixed": x和y刻度相同
- "free": x和y刻度自由
- "free_x": x刻度自由
- "free_y": y刻度自由

示例：
```python
ggplot(df, aes("x", "y")) + geom_point() + facet_wrap("category")
ggplot(df, aes("x", "y")) + geom_point() + facet_wrap("~ category + group")
```

## facet_grid
按双变量分面：
```python
facet_grid(rows, cols, scales="fixed")
```

示例：
```python
ggplot(df, aes("x", "y")) + geom_point() + facet_grid("category ~ group")
ggplot(df, aes("x", "y")) + geom_point() + facet_grid(". ~ category")
ggplot(df, aes("x", "y")) + geom_point() + facet_grid("category ~ .")
```

## labeller
分面标签：
```python
from plotnine import as_labeller, label_both, label_value

facet_grid("category ~ group", labeller=label_value)
facet_grid("category ~ group", labeller=label_both)
```
