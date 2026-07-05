# 散点图和线图

## 目录
- [geom_point](#geom_point)
- [geom_line](#geom_line)
- [geom_path](#geom_path)
- [geom_jitter](#geom_jitter)

## geom_point
散点图：
```python
geom_point(mapping=None, data=None, stat="identity", position="identity", ...)
```

常用参数：
- size: 点大小
- color: 点颜色
- shape: 点形状
- alpha: 透明度

## geom_line
线图：
```python
geom_line(mapping=None, data=None, stat="identity", position="identity", ...)
```

常用参数：
- linetype: 线型
- color: 线颜色
- size: 线宽度

## geom_path
按数据顺序连接点：
```python
geom_path(mapping=None, data=None, stat="identity", position="identity", ...)
```

## geom_jitter
随机抖动散点（减少重叠）：
```python
geom_jitter(width=0.4, height=0.4, ...)
```

示例：
```python
(
    ggplot(df, aes("x", "y"))
    + geom_jitter(width=0.2, height=0.2, alpha=0.6)
)
```
