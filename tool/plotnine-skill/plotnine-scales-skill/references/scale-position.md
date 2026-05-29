# 位置标度

## 目录
- [连续位置](#连续位置)
- [离散位置](#离散位置)
- [变换](#变换)

## 连续位置
```python
scale_x_continuous(breaks=None, labels=None, limits=None, expand=None)
scale_y_continuous(breaks=None, labels=None, limits=None, expand=None)
```

## 离散位置
```python
scale_x_discrete(limits=None, labels=None)
scale_y_discrete(limits=None, labels=None)
```

## 变换
```python
scale_x_log10()      # 对数变换
scale_y_log10()
scale_x_sqrt()       # 平方根变换
scale_y_sqrt()
scale_x_reverse()    # 反向
scale_y_reverse()
scale_x_symlog()     # 对称对数
```

## 限制范围
```python
xlim(0, 100)    # x范围
ylim(0, 50)     # y范围
lims(x=(0, 100), y=(0, 50))  # 同时设置
```
