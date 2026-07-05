# 动作链参考

本文档详细介绍 DrissionPage 动作链的完整 API。

## 概述

动作链（Actions）用于执行复杂的鼠标和键盘操作序列。

## 获取动作链对象

```python
# 从页面对象获取
ac = tab.actions

# 导入 Actions 类
from DrissionPage.common import Actions
ac = Actions(tab)
```

---

## 鼠标操作

### 移动

```python
# 移动到元素
ac.move_to('#element')

# 移动到坐标
ac.move_to((100, 200))

# 相对移动
ac.move(100, 50)      # 移动到相对位置
ac.up(50)             # 向上移动
ac.down(50)           # 向下移动
ac.left(50)           # 向左移动
ac.right(50)          # 向右移动
```

### 点击

```python
# 左键点击
ac.click('#element')
ac.click()            # 点击当前位置

# 右键点击
ac.r_click('#element')
ac.right_click('#element')

# 中键点击
ac.m_click('#element')
ac.middle_click('#element')

# 双击
ac.double_click('#element')
ac.dbl_click('#element')
```

### 按住和释放

```python
# 按住左键
ac.hold('#element')
ac.hold()             # 按住当前位置

# 按住右键
ac.hold_right('#element')

# 释放
ac.release()         # 释放所有按键
ac.release('#element') # 在元素位置释放
ac.release_right()    # 释放右键
```

---

## 键盘操作

### 按键

```python
from DrissionPage.common import Keys

# 按下按键
ac.key_down('Enter')
ac.key_down(Keys.ENTER)

# 提起按键
ac.key_up('Enter')

# 按一下（按下+提起）
ac.key_in('Enter')
```

### 输入文本

```python
# 输入文本
ac.type('Hello World')

# 输入组合键
ac.type((Keys.CTRL, 'a'))   # 全选
ac.type((Keys.CTRL, 'c'))   # 复制
ac.type((Keys.CTRL, 'v'))   # 粘贴
```

---

## 滚轮滚动

```python
# 滚动
ac.scroll(0, 500)    # 向下滚动
ac.scroll(0, -500)  # 向上滚动
ac.scroll(500, 0)    # 向右滚动

# 滚动到元素
ac.scroll_to_element('#element')
```

---

## 文件拖入

```python
# 拖入文件
ac.drag_in('#dropzone', files=['path/to/file.txt'])

# 拖入文本
ac.drag_in('#dropzone', text='some text')
```

---

## 链式调用

动作链支持链式调用：

```python
# 完整链式操作
(
    tab.actions
    .move_to('#input')
    .click()
    .type('text')
    .key_down(Keys.ENTER)
)
```

---

## 常用示例

### 模拟拖拽

```python
# 拖拽到相对位置
tab.actions.hold('#draggable')
tab.actions.move(100, 50)
tab.actions.release()

# 拖拽到目标元素
tab.actions.hold('#draggable')
tab.actions.move_to('#target')
tab.actions.release()
```

### 模拟输入

```python
# 聚焦并输入
tab.actions.move_to('#input').click().type('text')

# 快捷键组合
tab.actions.click('#input')
tab.actions.type((Keys.CTRL, 'a'))
tab.actions.type('new text')
```

### 鼠标悬停菜单

```python
# 悬停显示菜单
tab.actions.move_to('.menu-item')
tab.actions.move_to('.submenu')
tab.actions.click()
```

### 复杂手势

```python
# Z字形移动
tab.actions.move_to((100, 100))
tab.actions.down(50)
tab.actions.right(100)
tab.actions.up(50)
tab.actions.right(100)
```

---

## Keys 预定义常量

```python
Keys.ENTER        # 回车
Keys.ESCAPE       # ESC
Keys.SPACE        # 空格
Keys.TAB          # Tab
Keys.BACKSPACE    # 退格
Keys.DELETE       # Delete
Keys.ARROW_UP     # 上箭头
Keys.ARROW_DOWN   # 下箭头
Keys.ARROW_LEFT   # 左箭头
Keys.ARROW_RIGHT  # 右箭头
Keys.CTRL         # Ctrl
Keys.CTRL_A       # Ctrl+A
Keys.CTRL_C       # Ctrl+C
Keys.CTRL_V       # Ctrl+V
Keys.CTRL_X       # Ctrl+X
Keys.CTRL_Z       # Ctrl+Z
Keys.CTRL_Y       # Ctrl+Y
Keys.SHIFT        # Shift
Keys.ALT          # Alt
```
