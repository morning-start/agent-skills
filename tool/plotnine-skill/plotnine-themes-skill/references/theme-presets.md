# 预置主题

## 目录
- [主题列表](#主题列表)
- [对比](#对比)

## 主题列表
| 主题 | 说明 |
|------|------|
| theme_minimal | 最小化背景，无网格 |
| theme_bw | 白色背景，黑色网格 |
| theme_classic | 经典风格，无网格 |
| theme_dark | 暗色背景 |
| theme_light | 浅色线条背景 |
| theme_matplotlib | Matplotlib 默认风格 |
| theme_void | 仅保留轴线，无背景 |
| theme_tufte | Tufte 极简风格 |
| theme_538 | FiveThirtyEight 风格 |
| theme_xkcd | XKCD 手绘风格 |
| theme_seaborn | Seaborn 风格 |

## 对比
```python
# 简洁主题
ggplot(df, aes("x", "y")) + geom_point() + theme_minimal()

# 经典主题
ggplot(df, aes("x", "y")) + geom_point() + theme_classic()

# Tufte 主题（适合出版）
ggplot(df, aes("x", "y")) + geom_point() + theme_tufte()
```
