# 控制台信息参考

本文档详细介绍控制台信息获取 API。

## 概述

获取 JavaScript 控制台输出的信息。

注意：只有通过 `console.log()` 等方法输出到控制台的信息才能获取。

---

## 启动和停止

### console.start()

启动控制台监听。

```python
tab.console.start()
```

### console.stop()

停止监听。

```python
tab.console.stop()
```

---

## 获取信息

### console.wait()

等待一条控制台信息。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `timeout` | `float` | `None` | 超时时间 |

```python
data = tab.console.wait()
print(data.text)
```

### console.steps()

实时获取控制台信息（迭代器）。

```python
for data in tab.console.steps():
    print(data.text)
```

### console.messages

获取所有缓存的信息（获取后清空）。

```python
messages = tab.console.messages
for msg in messages:
    print(msg.text)
```

---

## 其它属性和方法

### console.listening

是否正在监听。

```python
if tab.console.listening:
    print("正在监听")
```

### console.clear()

清空缓存。

```python
tab.console.clear()
```

---

## ConsoleData 对象

获取到的控制台信息对象。

### 属性

| 属性 | 说明 |
|------|------|
| `source` | 来源 |
| `level` | 类型 (log/warning/error) |
| `text` | 内容文本 |
| `body` | JSON 解析后的内容 |
| `url` | 网址 |
| `line` | 行号 |
| `column` | 列号 |

---

## 示例

```python
from DrissionPage import Chromium

tab = Chromium().latest_tab
tab.get('https://example.com')

# 启动监听
tab.console.start()

# 执行 JS 输出
tab.run_js('console.log("Hello");')
tab.run_js('console.warn("Warning");')

# 获取信息
data = tab.console.wait()
print(data.text)    # Hello
print(data.level)   # log

# 停止监听
tab.console.stop()
```
