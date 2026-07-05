# DrissionPage API 参考手册

本文档提供 DrissionPage 框架的完整 API 参考。

## 核心类

### Chromium

浏览器控制主类，用于管理浏览器实例。

```python
from DrissionPage import Chromium

browser = Chromium(addr_or_opts=None, session_options=None)
```

#### 初始化参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `addr_or_opts` | `str`/`int`/`ChromiumOptions` | `None` | 浏览器地址、端口或配置对象 |
| `session_options` | `SessionOptions`/`None`/`False` | `None` | Session 配置 |

#### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `latest_tab` | `ChromiumTab` | 获取最后激活的标签页 |
| `tabs` | `list` | 获取所有标签页列表 |
| `title` | `str` | 浏览器标题 |
| `mode` | `str` | 当前模式 |

#### 方法

| 方法 | 说明 |
|------|------|
| `new_tab(url)` | 新建标签页并访问 URL |
| `get_tab(id)` | 获取指定标签页 |
| `set.tab(tab_id)` | 切换到指定标签页 |
| `quit()` | 关闭浏览器 |
| `wait.new_tab()` | 等待新标签页出现 |

---

### ChromiumOptions

浏览器启动配置类，用于配置浏览器启动参数。

```python
from DrissionPage import ChromiumOptions

co = ChromiumOptions(read_file=True, ini_path=None)
```

#### 初始化参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `read_file` | `bool` | `True` | 是否从 ini 文件读取配置 |
| `ini_path` | `str`/`Path` | `None` | ini 文件路径 |

#### 配置方法

##### 浏览器路径和端口

| 方法 | 说明 |
|------|------|
| `set_browser_path(path)` | 设置浏览器可执行文件路径 |
| `set_local_port(port)` | 设置本地端口 |
| `set_address(address)` | 设置浏览器地址 (ip:port 或 ws://) |
| `auto_port(on_off)` | 自动分配端口和临时用户目录 |
| `set_tmp_path(path)` | 设置临时文件路径 |
| `set_user_data_path(path)` | 设置用户数据文件夹路径 |
| `use_system_user_path(on_off)` | 使用系统浏览器用户目录 |
| `set_cache_path(path)` | 设置缓存路径 |

##### 浏览器选项

| 方法 | 说明 |
|------|------|
| `headless(on_off)` | 无头模式 |
| `mute(on_off)` | 静音 |
| `no_imgs(on_off)` | 不加载图片 |
| `no_js(on_off)` | 不加载 JavaScript |
| `incognito(on_off)` | 无痕模式 |
| `new_env(on_off)` | 全新环境 |
| `existing_only(on_off)` | 仅使用已启动的浏览器 |
| `ignore_certificate_errors(on_off)` | 忽略证书错误 |

##### 页面加载

| 方法 | 说明 |
|------|------|
| `set_timeouts(base, page_load, script)` | 设置超时时间 |
| `set_load_mode(mode)` | 设置加载模式 (normal/eager/none) |
| `set_retry(times, interval)` | 设置重试次数和间隔 |
| `set_proxy(proxy)` | 设置代理服务器 |
| `set_download_path(path)` | 设置下载保存路径 |

##### 用户配置

| 方法 | 说明 |
|------|------|
| `set_user(user)` | 设置用户配置文件夹名称 |
| `set_pref(arg, value)` | 设置用户首选项 |
| `set_user_agent(user_agent)` | 设置 User-Agent |
| `add_extension(path)` | 添加扩展 |

##### 命令行参数

| 方法 | 说明 |
|------|------|
| `set_argument(arg, value)` | 设置启动参数 |
| `remove_argument(arg)` | 删除启动参数 |
| `clear_arguments()` | 清空所有参数 |
| `set_flag(flag, value)` | 设置实验项 |

##### 保存配置

| 方法 | 说明 |
|------|------|
| `save(path)` | 保存配置到文件 |
| `save_to_default()` | 保存到默认配置 |

#### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `address` | `str` | 浏览器地址 |
| `browser_path` | `str` | 浏览器路径 |
| `user_data_path` | `str` | 用户数据目录 |
| `tmp_path` | `str` | 临时目录 |
| `download_path` | `str` | 下载路径 |
| `timeouts` | `dict` | 超时设置 |
| `arguments` | `list` | 启动参数列表 |
| `is_headless` | `bool` | 是否无头模式 |

---

### Tab 对象 (ChromiumTab)

页面标签页操作类。

#### 属性

| 属性 | 说明 |
|------|------|
| `title` | 页面标题 |
| `url` | 当前 URL |
| `html` | 页面 HTML |
| `json` | 页面 JSON 数据 |
| `cookies` | 页面 Cookie |
| `tab_id` | 标签页 ID |

#### 页面操作

| 方法 | 说明 |
|------|------|
| `get(url)` | 访问 URL |
| `get(url, timeout)` | 带超时访问 |
| `get(url, load_mode)` | 指定加载模式 |
| `back()` | 后退 |
| `forward()` | 前进 |
| `refresh()` | 刷新 |
| `close()` | 关闭标签页 |

#### 元素查找

| 方法 | 说明 |
|------|------|
| `ele(locator)` | 查找单个元素 |
| `eles(locator)` | 查找多个元素 |
| `wait.ele_visible(locator)` | 等待元素可见 |
| `wait.ele_displayed(locator)` | 等待元素显示 |
| `wait.ele_hidden(locator)` | 等待元素隐藏 |
| `wait.ele_deleted(locator)` | 等待元素删除 |
| `wait.ele_enabled(locator)` | 等待元素可用 |

#### JavaScript

| 方法 | 说明 |
|------|------|
| `run_js(script, *args)` | 执行 JavaScript |
| `run_async_js(script, *args)` | 异步执行 JavaScript |

#### 滚动

| 方法 | 说明 |
|------|------|
| `scroll.up(pixel)` | 向上滚动 |
| `scroll.down(pixel)` | 向下滚动 |
| `scroll.to_bottom()` | 滚动到底部 |
| `scroll.to_top()` | 滚动到顶部 |
| `scroll.to_location(x, y)` | 滚动到指定位置 |

#### Cookie 操作

| 方法 | 说明 |
|------|------|
| `cookies()` | 获取所有 Cookie |
| `cookie(name)` | 获取指定 Cookie |
| `set.cookies(cookies)` | 设置 Cookie |
| `delete.cookies(name)` | 删除 Cookie |

#### 网络监听

| 方法 | 说明 |
|------|------|
| `listen.start(targets)` | 开始监听 |
| `listen.wait()` | 等待数据包 |
| `listen.steps()` | 实时获取数据包 |
| `listen.stop()` | 停止监听 |

#### 动作链

| 方法 | 说明 |
|------|------|
| `actions` | 动作链对象 |

#### 下载

| 方法 | 说明 |
|------|------|
| `wait.download_begin()` | 等待下载开始 |
| `wait.downloads_done()` | 等待下载完成 |

---

### SessionPage

无需浏览器的页面操作类。

```python
from DrissionPage import SessionPage

page = SessionPage()
```

#### 属性

| 属性 | 说明 |
|------|------|
| `title` | 页面标题 |
| `url` | 当前 URL |
| `html` | 页面 HTML |
| `json` | 页面 JSON 数据 |
| `status_code` | 响应状态码 |
| `headers` | 响应头 |

#### 方法

| 方法 | 说明 |
|------|------|
| `get(url)` | 发送 GET 请求 |
| `post(url, data)` | 发送 POST 请求 |
| `put(url, data)` | 发送 PUT 请求 |
| `delete(url)` | 发送 DELETE 请求 |
| `ele(locator)` | 查找单个元素 |
| `eles(locator)` | 查找多个元素 |

#### 请求设置

| 方法 | 说明 |
|------|------|
| `headers.update(dict)` | 更新请求头 |
| `cookies.set(name, value)` | 设置 Cookie |
| `proxies.update(dict)` | 设置代理 |

---

## 元素定位

### 定位语法

#### 选择器语法

| 语法 | 说明 | 示例 |
|------|------|------|
| `#id` | ID 选择器 | `#kw` |
| `.class` | 类选择器 | `.btn` |
| `@attr` | 属性存在 | `@name` |
| `@attr=value` | 属性等于 | `@name=username` |
| `@attr*=value` | 属性包含 | `@class*=btn` |
| `@attr^=value` | 属性开头 | `@href^=http` |
| `@attr$=value` | 属性结尾 | `@src$=jpg` |
| `text=value` | 文本匹配 | `text=登录` |
| `text:contains(value)` | 文本包含 | `text:contains(登录)` |
| `tag:tagName` | 标签名 | `tag:div` |
| `css:selector` | CSS 选择器 | `css:#container` |
| `xpath:path` | XPath | `xpath://div` |

#### 相对定位

| 方法 | 说明 |
|------|------|
| `ele.next()` | 后一个相邻元素 |
| `ele.prev()` | 前一个相邻元素 |
| `ele.parent` | 父元素 |
| `ele.eles()` | 所有子元素 |
| `ele.first()` | 第一个子元素 |
| `ele.last()` | 最后一个子元素 |

---

## 元素操作

### 点击操作

| 方法 | 说明 |
|------|------|
| `ele.click()` | 左键点击 |
| `ele.click(by_js=True)` | JS 点击 |
| `ele.click.right()` | 右键点击 |
| `ele.click.middle()` | 中键点击 |
| `ele.click.multi(times)` | 多次点击 |
| `ele.click.at(x, y)` | 偏移点击 |
| `ele.click.for_new_tab()` | 点击并等待新标签页 |
| `ele.click.to_download()` | 点击触发下载 |

### 输入操作

| 方法 | 说明 |
|------|------|
| `ele.input(text)` | 输入文本 |
| `ele.input(text, clear=True)` | 输入前清空 |
| `ele.input(text, by_js=True)` | JS 方式输入 |
| `ele.clear()` | 清空 |
| `ele.focus()` | 获取焦点 |

### 下拉选择

| 方法 | 说明 |
|------|------|
| `select.by_text(text)` | 按文本选择 |
| `select.by_value(value)` | 按值选择 |
| `select.by_index(index)` | 按索引选择 |
| `select.all()` | 全选 |
| `select.clear()` | 取消选择 |
| `select.invert()` | 反选 |

### 拖拽操作

| 方法 | 说明 |
|------|------|
| `ele.drag(x, y)` | 拖拽到相对位置 |
| `ele.drag_to(target)` | 拖拽到目标元素 |
| `ele.drag_to((x, y))` | 拖拽到坐标 |
| `ele.hover()` | 悬停 |

### 滚动操作

| 方法 | 说明 |
|------|------|
| `ele.scroll.to_see()` | 滚动到可见 |
| `ele.scroll.to_top()` | 滚动到顶部 |
| `ele.scroll.to_bottom()` | 滚动到底部 |
| `ele.scroll.to_center()` | 滚动到中间 |

---

## 等待机制

### 页面等待

| 方法 | 说明 |
|------|------|
| `wait(second)` | 等待指定秒数 |
| `wait(second, scope)` | 随机等待 |
| `wait.load_start()` | 等待页面开始加载 |
| `wait.doc_loaded()` | 等待文档加载完成 |
| `wait.eles_loaded(locator)` | 等待元素加载 |

### 元素等待

| 方法 | 说明 |
|------|------|
| `wait.displayed()` | 等待显示 |
| `wait.hidden()` | 等待隐藏 |
| `wait.deleted()` | 等待删除 |
| `wait.enabled()` | 等待可用 |
| `wait.disabled()` | 等待不可用 |
| `wait.clickable()` | 等待可点击 |
| `wait.stop_moving()` | 等待停止运动 |
| `wait.not_covered()` | 等待不被遮挡 |

### 页面状态等待

| 方法 | 说明 |
|------|------|
| `wait.url_change(text)` | 等待 URL 变化 |
| `wait.title_change(text)` | 等待标题变化 |
| `wait.alert_closed()` | 等待弹窗关闭 |

---

## 动作链

### 鼠标操作

| 方法 | 说明 |
|------|------|
| `move_to(ele)` | 移动到元素 |
| `move_to((x, y))` | 移动到坐标 |
| `move(x, y)` | 相对移动 |
| `up(pixel)` | 向上移动 |
| `down(pixel)` | 向下移动 |
| `left(pixel)` | 向左移动 |
| `right(pixel)` | 向右移动 |
| `click(ele)` | 点击 |
| `r_click(ele)` | 右键点击 |
| `m_click(ele)` | 中键点击 |
| `hold(ele)` | 按住左键 |
| `release(ele)` | 释放 |

### 键盘操作

| 方法 | 说明 |
|------|------|
| `key_down(key)` | 按下按键 |
| `key_up(key)` | 提起按键 |
| `type(text)` | 输入文本 |
| `scroll(delta_y, delta_x)` | 滚轮滚动 |

### 文件拖入

| 方法 | 说明 |
|------|------|
| `drag_in(ele, files)` | 拖入文件 |
| `drag_in(ele, text)` | 拖入文本 |

---

## 网络监听

### 监听方法

| 方法 | 说明 |
|------|------|
| `listen.start(targets)` | 开始监听 |
| `listen.set_targets(targets)` | 设置目标 |
| `listen.wait(count)` | 等待数据包 |
| `listen.steps(count)` | 实时获取 |
| `listen.pause()` | 暂停 |
| `listen.resume()` | 恢复 |
| `listen.stop()` | 停止 |

### DataPacket 属性

| 属性 | 说明 |
|------|------|
| `url` | 请求 URL |
| `method` | 请求方法 |
| `resourceType` | 资源类型 |
| `request.url` | 请求 URL |
| `request.method` | 请求方法 |
| `request.headers` | 请求头 |
| `request.params` | URL 参数 |
| `request.postData` | POST 数据 |
| `request.cookies` | 请求 Cookie |
| `response.status` | 响应状态码 |
| `response.headers` | 响应头 |
| `response.body` | 响应体 |
| `is_failed` | 是否失败 |

---

## 错误处理

### 异常类

```python
from DrissionPage.errors import (
    ElementNotFoundError,      # 元素未找到
    ElementLostError,          # 元素丢失
    TimeoutError,              # 超时错误
    CallError,                 # 调用错误
    BrowserConnectError,       # 浏览器连接错误
    LoginFailedError,          # 登录失败
    NoRectError               # 无位置信息错误
)
```

---

## 常用工具

### Keys 类

```python
from DrissionPage.common import Keys

Keys.ENTER
Keys.ESCAPE
Keys.SPACE
Keys.TAB
Keys.BACKSPACE
Keys.DELETE
Keys.ARROW_UP
Keys.ARROW_DOWN
Keys.ARROW_LEFT
Keys.ARROW_RIGHT
Keys.CTRL
Keys.CTRL_A
Keys.CTRL_C
Keys.CTRL_V
Keys.CTRL_X
Keys.CTRL_Z
Keys.CTRL_Y
Keys.SHIFT
Keys.ALT
```

### Settings 类

```python
from DrissionPage.common import Settings

Settings.set_default_timeout(10)
Settings.set_retry_times(3)
Settings.set_raise_click_failed(True)
```

### Actions 类

```python
from DrissionPage.common import Actions

ac = Actions(page)
ac.move_to('#kw').click().type('text')
```
