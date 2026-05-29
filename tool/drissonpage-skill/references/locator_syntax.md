# 元素定位语法参考

本文档详细介绍 DrissionPage 的元素定位语法。

## 定位符类型

### ID 和类选择器

| 语法 | 说明 | 示例 |
|------|------|------|
| `#id` | ID 选择器 | `#kw` |
| `.class` | 类选择器 | `.btn-primary` |

### 属性定位

| 语法 | 说明 | 示例 |
|------|------|------|
| `@attr` | 属性存在 | `@name` |
| `@attr=value` | 属性等于 | `@name=username` |
| `@attr!=value` | 属性不等于 | `@name!=username` |
| `@attr*=value` | 属性包含 | `@class*=btn` |
| `@attr^=value` | 属性开头 | `@href^=http` |
| `@attr$=value` | 属性结尾 | `@src$=jpg` |
| `@attr~=value` | 属性空格分隔 | `@class~=active` |

### 文本定位

| 语法 | 说明 | 示例 |
|------|------|------|
| `text=value` | 精确文本 | `text=登录` |
| `text:contains(value)` | 文本包含 | `text:contains(登录)` |
| `text:starts(value)` | 文本开头 | `text:starts=百度` |
| `text:ends(value)` | 文本结尾 | `text:ends=官网` |

### 标签定位

| 语法 | 说明 | 示例 |
|------|------|------|
| `tag:tagName` | 标签名 | `tag:div` |
| `tag:a` | 链接 | `tag:a` |
| `tag:input` | 输入框 | `tag:input` |
| `tag:img` | 图片 | `tag:img` |

### CSS 和 XPath

| 语法 | 说明 | 示例 |
|------|------|------|
| `css:selector` | CSS 选择器 | `css:#container .item` |
| `xpath:path` | XPath | `xpath://div[@id='main']` |

---

## 使用方法

### 基本查找

```python
ele = tab.ele('#kw')           # ID
ele = tab.ele('.class')        # 类
ele = tab.ele('@name=value')   # 属性
ele = tab.ele('text=text')     # 文本
ele = tab.ele('tag:div')       # 标签
```

### 查找多个

```python
eles = tab.eles('tag:a')       # 所有链接
eles = tab.eles('.item')       # 所有 item
```

### 相对定位

```python
# 链式查找
container = tab.ele('.container')
item = container.ele('tag:li')

# 简写
item = tab('.container')('tag:li')

# 相对位置
next_ele = ele.next()           # 后一个
prev_ele = ele.prev()          # 前一个
parent = ele.parent            # 父元素
children = ele.eles()          # 所有子元素
first = ele.first()            # 第一个子元素
last = ele.last()              # 最后一个子元素
```

### 查找范围

```python
# 在元素内查找
ele.ele('tag:a')               # 查找子元素
ele.eles('tag:a')              # 查找多个子元素
```

---

## 定位符组合

### 多条件组合

```python
# 同时满足多个条件
ele = tab.ele('@class=btn @type=submit')
```

### 或运算

```python
# 满足任一条件
ele = tab.ele('text=登录 | text=Sign in')
```

---

## 定位符优先级

定位符从左到右匹配，效率从高到低：

1. `#id` - 最高效
2. `@attr` - 高效
3. `text=` - 中等
4. `tag:` - 较快
5. `css:` - 较慢
6. `xpath:` - 最慢

**建议**：优先使用稳定的唯一属性

---

## 查找行为

### 等待元素

```python
# 默认等待 10 秒
ele = tab.ele('#id')

# 自定义等待时间
ele = tab.ele('#id', timeout=5)
```

### 找不到元素

```python
# 默认返回 NoneElement
ele = tab.ele('#not-exist')
if ele:
    print('找到')
else:
    print('未找到')

# 立即抛出异常
from DrissionPage.common import Settings
Settings.set_raise_when_ele_not_found(True)
```

---

## 简化写法

### 省略 ele()

```python
# 完整写法
ele = tab.ele('#id')

# 简化写法
ele = tab('#id')
```

### 省略标签名

```python
# 完整
ele = tab.ele('tag:input')

# 简化 - 自动识别 input 类型
ele = tab.ele('@type=text')
```

---

## 常见示例

```python
# 百度搜索框
tab.ele('#kw')

# 登录按钮
tab.ele('text=登录')
tab.ele('@type=submit')

# 图片链接
tab.eles('tag:a img')

# 表单输入
tab.ele('@name=username')
tab.ele('@placeholder=请输入')

# 下拉框
tab.ele('tag:select')

# 表格单元格
tab.ele('xpath://table/tr[1]/td[2]')
```
