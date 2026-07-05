# 元素信息参考

本文档详细介绍获取元素信息的 API。

## 内容和属性

### tag

元素标签名。

```python
ele.tag  # 'div'
```

### html

元素 outerHTML。

```python
ele.html  # '<div id="test">...</div>'
```

### inner_html

元素 innerHTML。

```python
ele.inner_html
```

### text

格式化后的文本（已转码，去除多余换行）。

```python
ele.text
```

### raw_text

原始文本。

```python
ele.raw_text
```

### texts()

获取所有直接子节点文本。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `text_node_only` | `bool` | `False` | 是否只返回文本节点 |

```python
texts = ele.texts()  # ['文本1', '文本2', ...]
```

### comments

获取元素内注释列表。

```python
comments = ele.comments
```

### attrs

获取所有属性字典。

```python
attrs = ele.attrs  # {'id': 'test', 'class': 'btn', ...}
```

### attr()

获取指定属性值。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `name` | `str` | 必填 | 属性名称 |

```python
ele.attr('id')     # 'test'
ele.attr('href')   # 自动补充完整路径
```

### property()

获取 property 属性值。

```python
ele.property('value')
```

### value

获取元素 value 值。

```python
ele.value
```

### link

获取 href 或 src 属性。

```python
ele.link  # 自动补充完整路径
```

### pseudo.before

获取 ::before 伪元素内容。

```python
ele.pseudo.before
```

### pseudo.after

获取 ::after 伪元素内容。

```python
ele.pseudo.after
```

### style()

获取 CSS 样式属性。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `style` | `str` | 必填 | 样式属性名 |
| `pseudo_ele` | `str` | `''` | 伪元素名称 |

```python
ele.style('color')
ele.style('color', 'before')  # 伪元素
```

### shadow_root

获取 shadow-root 对象。

```python
shadow = ele.shadow_root
```

### child_count

获取第一级子元素个数。

```python
count = ele.child_count
```

---

## 大小和位置

### rect.size

元素大小。

```python
size = ele.rect.size  # (width, height)
```

### rect.location

元素左上角在页面中的坐标。

```python
loc = ele.rect.location  # (x, y)
```

### rect.midpoint

元素中点在页面中的坐标。

```python
mid = ele.rect.midpoint  # (x, y)
```

### rect.click_point

元素点击点在页面中的坐标。

```python
point = ele.rect.click_point
```

### rect.corners

元素四个角在页面中的坐标。

```python
corners = ele.rect.corners  # [(左上), (右上), (右下), (左下)]
```

### rect.viewport_corners

元素四个角在视口中的坐标。

### rect.viewport_location

元素左上角在视口中的坐标。

### rect.viewport_midpoint

元素中点在视口中的坐标。

### rect.viewport_click_point

元素点击点在视口中的坐标。

### rect.screen_location

元素左上角在屏幕中的坐标。

### rect.screen_midpoint

元素中点在屏幕中的坐标。

### rect.screen_click_point

元素点击点在屏幕中的坐标。

### rect.scroll_position

元素内滚动条位置。

```python
pos = ele.rect.scroll_position  # (x, y)
```

### xpath

获取元素 xpath 路径。

```python
path = ele.xpath
```

### css_path

获取元素 CSS 选择器路径。

```python
path = ele.css_path
```

---

## 元素列表批量获取

元素列表自带 `get` 属性。

### get.attrs()

批量获取属性。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `name` | `str` | 必填 | 属性名称 |

```python
attrs = eles.get.attrs('href')
```

### get.links()

批量获取链接。

```python
links = eles.get.links()
```

### get.texts()

批量获取文本。

```python
texts = eles.get.texts()
```

---

## 状态信息

### timeout

获取超时设置。

```python
timeout = ele.timeout
```

### states.is_in_viewport

元素是否在视口中。

```python
ele.states.is_in_viewport
```

### states.is_whole_in_viewport

元素是否整个在视口中。

### states.is_alive

元素是否仍可用。

```python
ele.states.is_alive
```

### states.is_checked

单选/多选框是否选中。

```python
ele.states.is_checked
```

### states.is_selected

select 元素项是否选中。

```python
ele.states.is_selected
```

### states.is_enabled

元素是否可用。

```python
ele.states.is_enabled
```

### states.is_displayed

元素是否可见。

```python
ele.states.is_displayed
```

### states.is_covered

元素是否被覆盖。

```python
covered = ele.states.is_covered
# 返回 False 或覆盖元素 id
```

### states.is_clickable

元素是否可点击。

```python
ele.states.is_clickable
```

### states.has_rect

元素是否有大小位置信息。

```python
rect = ele.states.has_rect
# 返回坐标列表或 False
```

---

## 保存元素资源

### src()

获取元素 src 属性资源。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `timeout` | `float` | `None` | 加载超时 |
| `base64_to_bytes` | `bool` | `True` | base64 转 bytes |

```python
data = ele.src()  # 返回 str 或 bytes
```

### save()

保存资源到文件。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `path` | `str`/`Path` | `None` | 保存路径 |
| `name` | `str` | `None` | 文件名 |
| `timeout` | `float` | `None` | 加载超时 |
| `rename` | `bool` | `True` | 遇到重名是否重命名 |

```python
ele.save('D:/img.png')
```

---

## 元素比较

两个元素可以用 `==` 比较是否指向同一元素。

```python
ele1 = tab.ele('t:div')
ele2 = tab.ele('t:div')
print(ele1 == ele2)  # True 或 False
```
