# stat_bin 和 stat_density

## 目录
- [stat_bin](#stat_bin)
- [stat_density](#stat_density)

## stat_bin
分箱计数统计：
```python
stat_bin(mapping=None, data=None, geom="histogram", position="stack", bins=None, binwidth=None, center=None, ...)
```

常用参数：
- bins: 分箱数量
- binwidth: 分箱宽度
- closed: 箱边界（"right" 或 "left"）

## stat_density
密度估计：
```python
stat_density(mapping=None, data=None, geom="density", position="identity", kernel="gaussian", adjust=1, ...)
```

常用参数：
- kernel: 核函数
- adjust: 带宽调整系数
- trim: 是否裁剪尾部
