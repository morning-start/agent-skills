# 全局设置参考

本文档详细介绍 DrissionPage 的全局设置 API。

## 导入

```python
from DrissionPage.common import Settings
```

---

## 设置方法

### set_default_timeout()

设置默认超时时间。

```python
Settings.set_default_timeout(10)
```

---

### set_retry_times()

设置重试次数。

```python
Settings.set_retry_times(3)
```

---

### set_singleton_tab_obj()

设置单例模式。

```python
Settings.set_singleton_tab_obj(False)  # 关闭单例
```

---

### set_raise_when_ele_not_found()

设置找不到元素时是否抛出异常。

```python
Settings.set_raise_when_ele_not_found(True)  # 立即抛出
```

---

### set_raise_click_failed()

设置点击失败时是否抛出异常。

```python
Settings.set_raise_click_failed(True)
```

---

### set_raise_wait_timeout_failed()

设置等待超时是否抛出异常。

```python
Settings.set_raise_wait_timeout_failed(True)
```

---

### set_headless_events()

设置无头模式是否产生事件。

```python
Settings.set_headless_events(True)
```

---

### set_夸()

设置是否自动处理弹窗。

```python
Settings.auto_handle_alert(True)
```

---

## 获取设置

```python
Settings.default_timeout  # 获取默认超时
Settings.retry_times     # 获取重试次数
Settings.singleton_tab_obj  # 获取单例模式状态
```
