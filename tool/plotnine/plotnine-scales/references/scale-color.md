# 颜色标度

## 目录
- [离散颜色](#离散颜色)
- [连续颜色](#连续颜色)
- [手动颜色](#手动颜色)

## 离散颜色
```python
# Brewer 颜色
scale_color_brewer(type="qual")  # 分类
scale_color_brewer(type="seq")    # 序列
scale_color_brewer(type="div")    # 发散

# Hue 颜色
scale_color_hue(l=0.45, h=0.75)
```

## 连续颜色
```python
# 渐变色
scale_fill_gradient(low="blue", high="red")

# 三点渐变
scale_fill_gradient2(low="red", mid="white", high="blue")

# n点渐变
scale_fill_gradientn(colors=["red", "yellow", "green"])
```

## 手动颜色
```python
scale_fill_manual(values={"A": "red", "B": "blue", "C": "green"})
scale_color_manual(values={"A": "red", "B": "blue"})
```
