# aes 美学映射

## 目录
- [概览](#概览)
- [映射类型](#映射类型)
- [特殊函数](#特殊函数)

## 概览
aes() 将数据变量映射到视觉属性。

## 映射类型
```python
# 位置
aes(x="column1", y="column2")

# 颜色
aes(x="x", y="y", color="category")

# 大小
aes(x="x", y="y", size="numeric_col")

# 透明度
aes(x="x", y="y", alpha="category")
```

## 特殊函数

### after_stat()
```python
from plotnine import aes, after_stat

ggplot(df, aes("x", y=after_stat("count / sum(count)")))
```

### after_scale()
```python
from plotnine import aes, after_scale

ggplot(df, aes("x", color=after_scale("red")))
```

### factor()
```python
from plotnine import aes, factor

ggplot(df, aes("x", fill=factor("category")))
```

### reorder()
```python
from plotnine import aes, reorder

ggplot(df, aes(reorder("category", "value"), "value"))
```
