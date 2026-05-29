# 柱状图和箱线图

## 目录
- [geom_bar](#geom_bar)
- [geom_col](#geom_col)
- [geom_boxplot](#geom_boxplot)
- [geom_violin](#geom_violin)

## geom_bar
计数柱状图（stat="count"）：
```python
ggplot(df, aes("category")) + geom_bar()
```

## geom_col
值柱状图（stat="identity"）：
```python
ggplot(df, aes("category", "value")) + geom_col()
```

## geom_boxplot
箱线图：
```python
(
    ggplot(df, aes("category", "value", fill="category"))
    + geom_boxplot(alpha=0.7)
)
```

常用参数：
- outlier.color: 异常点颜色
- outlier.shape: 异常点形状
- notch: 是否显示置信区间

## geom_violin
小提琴图：
```python
(
    ggplot(df, aes("category", "value", fill="category"))
    + geom_violin(trim=False)
)
```
