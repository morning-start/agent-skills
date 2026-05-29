# 异常参考

本文档详细介绍 DrissionPage 中的所有异常类。

## 导入

```python
from DrissionPage.errors import *
```

或导入特定异常：

```python
from DrissionPage.errors import ElementNotFoundError, TimeoutError
```

---

## 异常列表

### ElementNotFoundError

找不到元素时抛出。

```python
from DrissionPage.errors import ElementNotFoundError

try:
    ele = tab.ele('#not-exist')
except ElementNotFoundError:
    print("元素未找到")
```

---

### AlertExistsError

执行 JS 或调用通过 JS 实现的功能时，若存在未处理的弹出框则抛出。

```python
from DrissionPage.errors import AlertExistsError
```

---

### ContextLostError

页面被刷新后仍调用其中的元素时抛出。

```python
from DrissionPage.errors import ContextLostError

try:
    # 页面刷新后
    ele.click()
except ContextLostError:
    print("页面已刷新")
```

---

### ElementLostError

元素因页面或自身被刷新而失效后，仍对其进行调用时抛出。

```python
from DrissionPage.errors import ElementLostError
```

---

### CDPError

调用 CDP 方法产生异常时抛出。

```python
from DrissionPage.errors import CDPError
```

---

### PageDisconnectedError

页面关闭或连接断开后仍调用其功能时抛出。

```python
from DrissionPage.errors import PageDisconnectedError
```

---

### JavaScriptError

JavaScript 运行错误时抛出。

```python
from DrissionPage.errors import JavaScriptError

try:
    tab.run_js('invalid js code')
except JavaScriptError as e:
    print(f"JS错误: {e}")
```

---

### NoRectError

对没有大小和位置信息的元素获取这些信息时抛出。

```python
from DrissionPage.errors import NoRectError
```

---

### BrowserConnectError

连接浏览器出错时抛出。

```python
from DrissionPage.errors import BrowserConnectError

try:
    browser = Chromium(9999)  # 错误端口
except BrowserConnectError:
    print("连接失败")
```

---

### NoResourceError

元素 `src()` 和 `save()` 获取资源失败时抛出。

```python
from DrissionPage.errors import NoResourceError

try:
    img.src()
except NoResourceError:
    print("资源获取失败")
```

---

### CanNotClickError

点击元素时如元素不可点击，且设置允许抛出时抛出。

```python
from DrissionPage.errors import CanNotClickError
```

---

### GetDocumentError

获取页面文档失败时抛出。

```python
from DrissionPage.errors import GetDocumentError
```

---

### WaitTimeoutError

自动等待失败，且设置允许抛出时抛出。

```python
from DrissionPage.errors import WaitTimeoutError

try:
    tab.wait.ele_visible('#element', timeout=5)
except WaitTimeoutError:
    print("等待超时")
```

---

### IncorrectURLError

访问格式不正确的 URL 时抛出。

```python
from DrissionPage.errors import IncorrectURLError
```

---

### StorageError

操作数据时，如网站禁止操作则抛出。

```python
from DrissionPage.errors import StorageError
```

---

### CookieFormatError

导入 cookie 时如格式不正确则抛出。

```python
from DrissionPage.errors import CookieFormatError
```

---

### LocatorError

传入的定位符格式不正确时抛出。

```python
from DrissionPage.errors import LocatorError
```

---

### UnknownError

发生未知错误时抛出。

```python
from DrissionPage.errors import UnknownError
```

---

## 全局设置

### 找不到元素时立即抛出异常

```python
from DrissionPage.common import Settings

Settings.set_raise_when_ele_not_found(True)
```

### 点击失败时抛出异常

```python
Settings.set_raise_click_failed(True)
```

### 等待超时抛出异常

```python
Settings.set_raise_wait_timeout_failed(True)
```
