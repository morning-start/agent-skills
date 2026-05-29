# 等待机制参考

本文档详细介绍 DrissionPage 的等待机制。

## 概述

DrissionPage 内置智能等待机制，提高脚本稳定性和执行效率。

---

## 页面等待

### wait()

等待指定秒数。

```python
# 固定等待
tab.wait(2)

# 随机等待（1-3秒之间）
tab.wait(1, 3)
```

### wait.load_start()

等待页面开始加载。

```python
tab.wait.load_start()
```

### wait.doc_loaded()

等待文档加载完成。

```python
tab.wait.doc_loaded()
```

### wait.eles_loaded()

等待元素加载到 DOM。

```python
# 等待元素出现
tab.wait.eles_loaded('#new-element')

# 带超时
tab.wait.eles_loaded('#new-element', timeout=5)
```

---

## 元素等待

### wait.ele_visible()

等待元素可见。

```python
# 等待元素可见
tab.wait.ele_visible('#element')

# 带超时
tab.wait.ele_visible('#element', timeout=10)
```

### wait.ele_displayed()

等待元素显示（display != none）。

```python
tab.wait.ele_displayed('#modal')
```

### wait.ele_hidden()

等待元素隐藏。

```python
tab.wait.ele_hidden('#loading')
```

### wait.ele_deleted()

等待元素从 DOM 删除。

```python
tab.wait.ele_deleted('#toast')
```

### wait.ele_enabled()

等待元素可用。

```python
tab.wait.ele_enabled('#submit')
```

### wait.ele_clickable()

等待元素可点击。

```python
tab.wait.ele_clickable('#button')
```

---

## 元素实例方法

元素对象也有等待方法：

```python
ele = tab.ele('#element')

# 等待显示
ele.wait.displayed()

# 等待隐藏
ele.wait.hidden()

# 等待删除
ele.wait.deleted()

# 等待可用
ele.wait.enabled()

# 等待可点击
ele.wait.clickable()

# 等待停止运动
ele.wait.stop_moving()

# 等待不被遮挡
ele.wait.not_covered()
```

---

## 页面状态等待

### wait.url_change()

等待 URL 变化。

```python
# 等待 URL 包含某文本
tab.wait.url_change('example.com')

# 等待 URL 变化（任意）
tab.wait.url_change()
```

### wait.title_change()

等待标题变化。

```python
# 等待标题包含文本
tab.wait.title_change('新标题')

# 等待标题变化（任意）
tab.wait.title_change()
```

### wait.alert_closed()

等待弹窗关闭。

```python
tab.wait.alert_closed()
```

---

## 下载等待

### wait.download_begin()

等待下载开始。

```python
mission = tab.wait.download_begin()
```

### wait.downloads_done()

等待所有下载完成。

```python
# 无限等待
tab.wait.downloads_done()

# 带超时
tab.wait.downloads_done(timeout=60)
```

---

## 浏览器级别等待

### wait.new_tab()

等待新标签页出现。

```python
new_tab_id = browser.wait.new_tab()
```

---

## 超时设置

### 设置基础超时

```python
# 方式1：全局设置
from DrissionPage.common import Settings
Settings.set_default_timeout(10)

# 方式2：浏览器对象设置
browser.set.timeouts(base=10)

# 方式3：每次查找设置
tab.ele('#id', timeout=5)
```

### 超时参数说明

| 参数 | 说明 |
|------|------|
| `base` | 各种等待的默认超时 |
| `page_load` | 页面加载超时 |
| `script` | JavaScript 运行超时 |

---

## 抛出异常设置

### 找不到元素时抛出

```python
from DrissionPage.common import Settings
Settings.set_raise_when_ele_not_found(True)
```

### 等待超时时抛出

```python
Settings.set_raise_wait_timeout_failed(True)
```

### 点击失败时抛出

```python
Settings.set_raise_click_failed(True)
```

---

## 随机等待

```python
# 随机等待 1-3 秒
tab.wait(1, 3)

# 在元素等待中
tab.wait.ele_visible('#element', timeout=(5, 10))
```

---

## 最佳实践

1. **优先使用智能等待**：内置等待机制比固定 sleep 更稳定
2. **合理设置超时**：根据网络环境调整超时时间
3. **使用元素状态等待**：等待元素可用后再操作
4. **避免固定 sleep**：使用随机等待模拟人类行为

```python
# 推荐
tab.wait.ele_visible('#submit')
tab.ele('#submit').click()

# 不推荐
tab.wait(2)
tab.ele('#submit').click()
```
