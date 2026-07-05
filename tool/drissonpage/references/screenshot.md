# 截图和录像参考

本文档详细介绍截图和录像功能。

---

## 页面截图

### get_screenshot()

对页面进行截图。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `path` | `str`/`Path` | `None` | 保存路径 |
| `name` | `str` | `None` | 文件名 |
| `as_bytes` | `str`/`True` | `None` | 返回字节 |
| `as_base64` | `str`/`True` | `None` | 返回 base64 |
| `full_page` | `bool` | `False` | 整页截图 |
| `left_top` | `tuple` | `None` | 截取左上角 |
| `right_bottom` | `tuple` | `None` | 截取右下角 |

```python
# 基本截图
tab.get_screenshot(path='tmp', name='pic.png')

# 整页截图
tab.get_screenshot(path='page.png', full_page=True)

# 截取指定区域
tab.get_screenshot(path='region.png', left_top=(0, 0), right_bottom=(800, 600))

# 返回字节
img_bytes = tab.get_screenshot(as_bytes='png')

# 返回 base64
img_base64 = tab.get_screenshot(as_base64=True)
```

---

## 元素截图

### ele.get_screenshot()

对元素进行截图。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `path` | `str`/`Path` | `None` | 保存路径 |
| `name` | `str` | `None` | 文件名 |
| `as_bytes` | `str`/`True` | `None` | 返回字节 |
| `as_base64` | `str`/`True` | `None` | 返回 base64 |
| `scroll_to_center` | `bool` | `True` | 截图前滚动到中央 |

```python
# 元素截图
ele = tab.ele('tag:img')
ele.get_screenshot(path='element.png')

# 返回字节
img_bytes = ele.get_screenshot(as_bytes='png')
```

---

## 页面录像

### 设置录制模式

```python
# 视频模式（无声音）
tab.screencast.set_mode.video_mode()

# 节约模式（有变化才录制）
tab.screencast.set_mode.frugal_video_mode()

# JS 模式（可录制声音）
tab.screencast.set_mode.js_video_mode()

# 图片模式（持续截图）
tab.screencast.set_mode.imgs_mode()

# 节约图片模式（有变化才保存）
tab.screencast.set_mode.frugal_imgs_mode()
```

### 设置保存路径

```python
tab.screencast.set_save_path('./video')
```

### 开始录制

```python
tab.screencast.start()
# 或指定路径
tab.screencast.start(save_path='./video')
```

### 停止录制

```python
file_path = tab.screencast.stop(
    video_name='my_video',
    suffix='mp4',
    coding='mp4v'
)
```

---

## 注意事项

1. 视频模式保存路径和文件名必须是英文
2. 需要安装 opencv：`pip install opencv-python`
3. 无头模式可能不支持录像功能
4. 元素超出视口截图需要 Chrome 90+

---

## 示例

```python
from DrissionPage import Chromium

tab = Chromium().latest_tab
tab.get('https://example.com')

# 截图
tab.get_screenshot(path='screenshot.png')

# 录像
tab.screencast.set_save_path('video')
tab.screencast.set_mode.video_mode()
tab.screencast.start()
tab.wait(5)
tab.screencast.stop('output')
```
