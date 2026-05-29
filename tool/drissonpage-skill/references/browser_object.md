# 浏览器对象参考

本文档详细介绍 Chromium 浏览器对象的 API。

## 获取标签页

### get_tab()

获取一个标签页对象或 id。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `id_or_num` | `str`/`int` | `None` | 标签页 id 或序号，负数表示倒数第几个 |
| `title` | `str` | `None` | 匹配 title，模糊匹配 |
| `url` | `str` | `None` | 匹配 url，模糊匹配 |
| `tab_type` | `str`/`list` | `'page'` | 标签页类型 |
| `as_id` | `bool` | `False` | 是否返回 id 而非对象 |

```python
tab = browser.get_tab()  # 获取最新标签页
tab = browser.get_tab(title='百度')  # 按标题获取
tab = browser.get_tab(1)  # 按序号获取
```

### get_tabs()

获取多个符合条件的标签页。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `title` | `str` | `None` | 匹配 title |
| `url` | `str` | `None` | 匹配 url |
| `tab_type` | `str`/`list` | `'page'` | 标签页类型 |
| `as_id` | `bool` | `False` | 是否返回 id |

```python
tabs = browser.get_tabs(url='baidu')  # 获取所有包含 baidu 的标签页
```

### latest_tab

获取最后激活的标签页对象。

```python
tab = browser.latest_tab
```

### tabs_count

获取普通标签页数量。

```python
count = browser.tabs_count
```

### tab_ids

获取所有标签页 id 列表。

```python
ids = browser.tab_ids
```

---

## 标签页操作

### new_tab()

新建标签页。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `url` | `str` | `None` | 跳转网址 |
| `new_window` | `bool` | `False` | 是否在新窗口打开 |
| `background` | `bool` | `False` | 是否不激活新标签页 |
| `new_context` | `bool` | `False` | 是否创建独立环境 |

```python
new_tab = browser.new_tab('https://example.com')
```

### activate_tab()

激活标签页（使标签页显示到前端）。

```python
browser.activate_tab('tab_id')
browser.activate_tab(1)  # 按序号激活
```

### close_tabs()

关闭标签页。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `tabs_or_ids` | `str`/`Tab`/`list` | 必填 | 标签页对象或 id |
| `others` | `bool` | `False` | 是否关闭指定的以外的 |

```python
browser.close_tabs('tab_id')
browser.close_tabs([tab1, tab2])
browser.close_tabs(tab, others=True)  # 关闭除 tab 外的所有
```

---

## 单例模式

默认情况下，同一标签页只有一个 Tab 对象。关闭单例模式后，每次 `get_tab()` 会创建新对象。

```python
from DrissionPage.common import Settings

Settings.set_singleton_tab_obj(False)
```

---

## 浏览器运行参数

### user_data_path

用户文件夹路径。

```python
path = browser.user_data_path
```

### download_path

默认下载路径。

```python
path = browser.download_path
```

### timeouts

超时设置，包含 `base`、`page_load`、`script`。

```python
timeouts = browser.timeouts
print(timeouts.base)  # 基础超时
```

### timeout

基础超时设置。

### load_mode

页面加载模式：`'none'`、`'normal'`、`'eager'`。

---

## 浏览器运行设置

### set.timeouts()

设置超时时间。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `base` | `float` | `None` | 基础超时 |
| `page_load` | `float` | `None` | 页面加载超时 |
| `script` | `float` | `None` | 脚本运行超时 |

```python
browser.set.timeouts(base=10, page_load=30)
```

### set.load_mode()

设置加载模式。

```python
browser.set.load_mode.normal()  # 等待所有资源加载
browser.set.load_mode.eager()   # 文档加载完成即停止
browser.set.load_mode.none()    # 不主动停止加载
```

### set.retry_times()

设置重连次数。

```python
browser.set.retry_times(3)
```

### set.retry_interval()

设置重连间隔（秒）。

```python
browser.set.retry_interval(1)
```

### set.cookies()

设置 cookies。

```python
browser.set.cookies({'name': 'value', 'domain': '.example.com'})
```

### set.cookies.clear()

清除所有 cookies。

```python
browser.set.cookies.clear()
```

### set.auto_handle_alert()

设置自动处理 alert 弹窗。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `on_off` | `bool` | `True` | 是否启用 |
| `accept` | `bool` | `True` | 确定还是取消 |

```python
browser.set.auto_handle_alert(True, True)
```

### set.download_path()

设置下载路径。

```python
browser.set.download_path('./downloads')
```

### set.download_file_name()

设置下一个下载文件的名称。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `name` | `str` | `None` | 文件名 |
| `suffix` | `str` | `None` | 后缀名 |

```python
browser.set.download_file_name('report.pdf')
```

### set.when_download_file_exists()

设置同名文件存在时的处理方式。

| 参数 | 说明 |
|------|------|
| `'rename'`/`'r'` | 自动重命名 |
| `'overwrite'`/`'o'` | 覆盖 |
| `'skip'`/`'s'` | 跳过 |

```python
browser.set.when_download_file_exists('rename')
```

### set.NoneElement_value()

设置查找元素失败时的返回值。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `value` | `Any` | `None` | 返回值 |
| `on_off` | `bool` | `True` | 是否启用 |

```python
browser.set.NoneElement_value('N/A')
```

---

## 浏览器信息

### cookies()

获取所有 cookies。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `all_info` | `bool` | `False` | 是否返回全部信息 |

```python
cookies = browser.cookies()
print(cookies.as_str)   # 字符串格式
print(cookies.as_dict)  # 字典格式
print(cookies.as_json)  # JSON 格式
```

### process_id

浏览器进程 pid。

```python
pid = browser.process_id
```

### states

浏览器状态。

```python
browser.states.is_alive         # 是否可用
browser.states.is_existed       # 是否是接管而非创建
browser.states.is_headless      # 是否无头模式
browser.states.is_incognito     # 是否无痕模式
```

---

## 其它方法

### wait()

等待若干秒。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `second` | `float` | 必填 | 等待秒数 |
| `scope` | `float` | `None` | 随机范围结束值 |

```python
browser.wait(2)        # 等待2秒
browser.wait(1, 3)    # 随机等待1-3秒
```

### wait.new_tab()

等待新标签页出现。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `timeout` | `float` | `None` | 超时时间 |
| `curr_tab` | `str`/`Tab` | `None` | 当前标签页 |
| `raise_err` | `bool` | `None` | 超时是否报错 |

```python
new_tab_id = browser.wait.new_tab()
```

### wait.download_begin()

等待下载开始。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `timeout` | `float` | `None` | 超时时间 |
| `cancel_it` | `bool` | `False` | 是否取消 |

```python
mission = browser.wait.download_begin()
```

### wait.downloads_done()

等待所有下载完成。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `timeout` | `float` | `None` | 超时时间 |
| `cancel_if_timeout` | `bool` | `True` | 超时是否取消 |

```python
browser.wait.downloads_done()
```

### clear_cache()

清除缓存。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `cache` | `bool` | `True` | 清除缓存 |
| `cookies` | `bool` | `True` | 清除 cookies |

```python
browser.clear_cache()
```

### reconnect()

重新连接浏览器。

```python
browser.reconnect()
```

### quit()

关闭浏览器。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `timeout` | `float` | `5` | 等待超时 |
| `force` | `bool` | `False` | 强制终止 |
| `del_data` | `bool` | `False` | 删除用户文件夹 |

```python
browser.quit()
browser.quit(del_data=True)  # 关闭并删除用户数据
```
