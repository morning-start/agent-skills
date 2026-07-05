# DataFrame 支持

## 目录
- [概览](#概览)
- [Pandas](#pandas)
- [Polars](#polars)
- [管道操作](#管道操作)

## 概览
Plotnine 支持 Pandas 和 Polars DataFrame。

## Pandas
```python
import pandas as pd
from plotnine import ggplot, aes, geom_point

df = pd.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y": [2, 4, 6, 8, 10],
    "category": ["A", "B", "A", "B", "A"]
})

ggplot(df, aes("x", "y")) + geom_point()
```

## Polars
```python
import polars as pl
from plotnine import ggplot, aes, geom_point

df = pl.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y": [2, 4, 6, 8, 10]
})

ggplot(df, aes("x", "y")) + geom_point()
```

## 管道操作
```python
import polars as pl
from plotnine import ggplot, aes, geom_point

(
    pl.DataFrame({"x": [1, 2, 3], "y": [2, 4, 6]})
    >> ggplot(aes("x", "y"))
    + geom_point()
)
```
