# 密度图和直方图

## 目录
- [geom_histogram](#geom_histogram)
- [geom_density](#geom_density)
- [geom_freqpoly](#geom_freqpoly)

## geom_histogram
直方图：
```python
(
    ggplot(df, aes("value", fill="category"))
    + geom_histogram(bins=30, alpha=0.7)
)
```

常用参数：
- bins: 分箱数量
- binwidth: 分箱宽度
- center: 箱中心

## geom_density
密度图：
```python
(
    ggplot(df, aes("value", fill="category"))
    + geom_density(alpha=0.5)
)
```

常用参数：
- kernel: 核函数（"gaussian", "rectangular"）
- adjust: 带宽调整

## geom_freqpoly
频率多边形：
```python
(
    ggplot(df, aes("value", color="category"))
    + geom_freqpoly(bins=30)
)
```
