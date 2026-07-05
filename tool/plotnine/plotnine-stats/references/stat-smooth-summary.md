# stat_smooth 和 stat_summary

## 目录
- [stat_smooth](#stat_smooth)
- [stat_summary](#stat_summary)

## stat_smooth
平滑回归：
```python
(
    ggplot(df, aes("x", "y"))
    + stat_smooth(method="lm", se=True)
    + geom_point()
)
```

method 选项：
- "lm": 线性回归
- "ols": 普通最小二乘
- "rlm": 稳健回归
- "loess": 局部多项式

## stat_summary
汇总统计：
```python
(
    ggplot(df, aes("category", "value"))
    + stat_summary(
        fun_y="mean",
        geom="point",
        size=3
    )
    + stat_summary(
        fun_ymin="mean",
        fun_ymax="mean",
        geom="errorbar"
    )
)
```

fun_y 常用函数：
- "mean": 均值
- "median": 中位数
- "sum": 总和
- "sd": 标准差
