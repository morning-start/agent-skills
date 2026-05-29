# 下载功能参考

本文档详细介绍 DrissionPage 的下载功能。

## 概述

DrissionPage 提供以下下载管理功能：

- 每个 tab 独立设置下载路径
- 下载前指定文件名（重命名）
- 设置同名文件处理方式
- 获取下载进度
- 等待下载完成
- 取消任务
- 拦截下载任务

## 注意事项

1. **必须等待下载结束**：程序在下载结束时才能重命名，之前文件名是临时任务 id
2. **多 Tab 时设置总路径**：多个 Tab 触发下载时，建议给 Chromium 对象设置总路径
3. **启动下载管理**：需要设置下载路径或调用 `set.download_path()` 才生效

---

## click.to_download()

点击触发下载并返回任务对象。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `save_path` | `str`/`Path` | 必填 | 保存路径 |
| `rename` | `str` | `None` | 重命名 |
| `suffix` | `str` | `None` | 文件后缀 |
| `new_tab` | `bool` | `False` | 下载是否在新标签页 |
| `by_js` | `bool` | `False` | 是否用 JS 点击 |
| `timeout` | `float` | `None` | 超时时间 |

```python
from DrissionPage import Chromium

tab = Chromium().latest_tab
tab.get('https://example.com')
mission = tab.ele('#download').click.to_download(
    save_path='./downloads',
    rename='file.pdf'
)
mission.wait()
```

---

## 设置下载路径

### Chromium 对象设置（全局）

```python
browser = Chromium()
browser.set.download_path('./downloads')
```

### Tab 对象设置（仅当前标签页）

```python
tab = Chromium().latest_tab
tab.set.download_path('./downloads')
```

---

## 设置文件名

设置下一个下载文件的名称。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `name` | `str` | `None` | 文件名 |
| `suffix` | `str` | `None` | 后缀名 |

```python
tab.set.download_file_name('report')
tab.ele('tag:a').click()

mission = tab.wait.download_begin()
mission.wait()
```

---

## 等待下载

### 等待下载开始

```python
mission = tab.wait.download_begin()
# 返回 DownloadMission 对象
# 超时返回 False
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `timeout` | `float` | `None` | 超时时间 |
| `cancel_it` | `bool` | `False` | 是否取消任务 |

### 等待所有下载完成（浏览器级别）

```python
browser.wait.downloads_done()
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `timeout` | `float` | `None` | 超时时间 |
| `cancel_if_timeout` | `bool` | `True` | 超时是否取消 |

### 等待当前 Tab 下载完成

```python
tab.wait.downloads_done()
```

---

## 拦截下载任务

```python
tab.ele('tag:a').click()
data = tab.wait.download_begin(cancel_it=True)
# data 包含 url 等信息
# 可以用其他方式下载
tab.download(data.url)
```

---

## 同名文件处理

### 自动重命名

```python
browser.set.when_download_file_exists('rename')
# 已有 file.txt -> 新 file_1.txt
```

### 覆盖

```python
browser.set.when_download_file_exists('overwrite')
```

### 跳过

```python
browser.set.when_download_file_exists('skip')
```

---

## DownloadMission 对象

### 属性

| 属性 | 说明 |
|------|------|
| `url` | 下载链接 |
| `tab_id` | 触发标签页 ID |
| `id` | 任务 ID |
| `folder` | 保存文件夹 |
| `name` | 文件名 |
| `tmp_path` | 临时文件路径 |
| `state` | 状态 (running/done/canceled/skipped) |
| `total_bytes` | 总字节数 |
| `received_bytes` | 已下载字节数 |
| `final_path` | 最终路径（完成后） |
| `is_done` | 是否完成 |
| `rate` | 下载速度 |

### 方法

#### wait()

等待下载完成。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `show` | `bool` | `True` | 打印下载信息 |
| `timeout` | `float` | `None` | 超时时间 |
| `cancel_if_timeout` | `bool` | `False` | 超时是否取消 |

```python
mission.wait()
# 返回最终路径或 False
```

#### cancel()

取消任务（已下载文件也会删除）。

```python
mission.cancel()
```

#### pause()/resume()

暂停/继续下载。

```python
mission.pause()
mission.resume()
```

---

## 完整示例

```python
from DrissionPage import Chromium

browser = Chromium()
browser.set.download_path('./downloads')
browser.set.when_download_file_exists('rename')

tab = browser.latest_tab
tab.get('https://example.com')

# 点击下载
mission = tab.ele('#download').click.to_download(
    save_path='./downloads',
    rename='report.pdf'
)

# 等待下载完成
file_path = mission.wait()
print(f"文件保存至: {file_path}")

browser.quit()
```
