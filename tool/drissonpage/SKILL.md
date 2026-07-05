---
name: drissonpage
description: DrissionPage Python网页自动化工具库技能
version: 1.0.0
---

# DrissionPage 浏览器自动化技能

## 技能概述

DrissionPage 是一个强大的 Python 网页自动化工具库，能够控制 Chromium 内核浏览器（如 Chrome、Edge），同时支持收发数据包模式。它整合了 Selenium 和 Requests 的优势，既能处理 JavaScript 渲染的动态页面，又能以高效的数据包方式访问静态页面。

## 核心特性

- **无 WebDriver**：无需下载驱动，无 WebDriver 特征
- **双模式切换**：浏览器控制和数据包访问无缝切换
- **智能等待**：内置自动等待机制，提高稳定性
- **元素定位**：简洁强大的定位语法，支持相对定位
- **跨 iframe**：无需切入切出，直接跨 iframe 查找
- **多标签页**：同时操作多个标签页，无需切换
- **Shadow DOM**：支持处理非 open 状态的 shadow-root

## 快速开始

### 安装

```bash
pip install DrissionPage
```

### 第一个示例

```python
from DrissionPage import Chromium

# 创建浏览器对象
browser = Chromium()

# 获取标签页
tab = browser.latest_tab

# 访问网页
tab.get('https://www.baidu.com')

# 查找元素并操作
tab.ele('#kw').input('DrissionPage')
tab.ele('#su').click()

# 获取结果
print(tab.title)

# 关闭浏览器
browser.quit()
```

---

## 第一部分：浏览器控制

### 1.1 连接浏览器

DrissionPage 通过 `Chromium` 类连接浏览器，支持多种连接方式。

#### 默认连接

```python
from DrissionPage import Chromium

# 使用默认配置连接
browser = Chromium()
```

#### 指定端口

```python
# 指定端口连接
browser = Chromium(9333)

# 或使用地址字符串
browser = Chromium('127.0.0.1:9333')
```

#### 使用配置对象

```python
from DrissionPage import Chromium, ChromiumOptions

# 创建配置对象
co = ChromiumOptions()

# 设置无头模式
co.headless(True)

# 静音
co.mute(True)

# 不加载图片
co.no_imgs(True)

# 使用配置创建浏览器
browser = Chromium(addr_or_opts=co)
```

### 1.2 浏览器配置

`ChromiumOptions` 类提供丰富的配置选项。

#### 常用配置方法

| 方法 | 说明 | 示例 |
|------|------|------|
| `headless(on_off)` | 无头模式 | `co.headless(True)` |
| `mute(on_off)` | 静音 | `co.mute(True)` |
| `no_imgs(on_off)` | 不加载图片 | `co.no_imgs(True)` |
| `no_js(on_off)` | 不加载 JavaScript | `co.no_js(True)` |
| `incognito(on_off)` | 无痕模式 | `co.incognito(True)` |
| `set_browser_path(path)` | 设置浏览器路径 | `co.set_browser_path(r'D:\chrome.exe')` |
| `set_local_port(port)` | 设置端口 | `co.set_local_port(9333)` |
| `set_user_data_path(path)` | 用户数据目录 | `co.set_user_data_path(r'D:\data')` |
| `auto_port(on_off)` | 自动分配端口 | `co.auto_port(True)` |
| `set_proxy(proxy)` | 设置代理 | `co.set_proxy('http://ip:port')` |
| `set_download_path(path)` | 下载路径 | `co.set_download_path('./downloads')` |
| `set_timeouts(base, page_load, script)` | 超时设置 | `co.set_timeouts(base=10)` |
| `set_load_mode(mode)` | 加载模式 | `co.set_load_mode('eager')` |
| `set_user_agent(ua)` | 设置 User-Agent | `co.set_user_agent('Mozilla/5.0...')` |
| `ignore_certificate_errors(on_off)` | 忽略证书错误 | `co.ignore_certificate_errors(True)` |

#### 加载模式

```python
# normal - 等待所有资源下载完成（默认）
# eager - DOM 就绪即停止加载
# none - 网页连接成功即停止加载
co.set_load_mode('eager')
```

#### 保存配置

```python
# 保存到指定文件
co.save('config.ini')

# 保存到默认文件
co.save_to_default()
```

### 1.3 标签页管理

```python
# 获取当前标签页
tab = browser.latest_tab

# 新建标签页
new_tab = browser.new_tab('https://example.com')

# 获取所有标签页
all_tabs = browser.tabs()

# 按条件获取标签页
tab = browser.get_tab(title='百度')

# 关闭标签页
tab.close()

# 切换到标签页
browser.set.tab(tab_id)
```

### 1.4 访问网页

```python
# 基本访问
tab.get('https://www.baidu.com')

# 带超时访问
tab.get('https://example.com', timeout=10)

# 加载模式
tab.get('https://example.com', load_mode='eager')
```

---

## 第二部分：元素查找

### 2.1 定位语法

DrissionPage 提供简洁强大的定位语法。

#### 基本语法

| 语法 | 说明 | 示例 |
|------|------|------|
| `#id` | ID 选择器 | `#kw` |
| `.class` | 类选择器 | `.btn-primary` |
| `@attr=value` | 属性精确匹配 | `@name=username` |
| `@attr*=value` | 属性包含 | `@class*=btn` |
| `@attr^=value` | 属性开头匹配 | `@href^=http` |
| `@attr$=value` | 属性结尾匹配 | `@src$=jpg` |
| `text=text` | 文本精确匹配 | `text=登录` |
| `text:contains(text)` | 文本包含 | `text:contains(登录)` |
| `tag:tagName` | 标签名 | `tag:div` |
| `css:selector` | CSS 选择器 | `css:#container .item` |
| `xpath:path` | XPath | `xpath://div[@id='main']` |

#### 查找方法

```python
# 查找单个元素
ele = tab.ele('#kw')
ele = tab.ele('@name=username')
ele = tab.ele('text=登录')
ele = tab.ele('tag:input')

# 查找多个元素
eles = tab.eles('tag:a')

# 使用元组定位
ele = tab.ele(('css', '#kw'))
ele = tab.ele(('xpath', '//div'))
```

### 2.2 相对定位

```python
# 在元素内部查找
container = tab.ele('.container')
item = container.ele('tag:li')

# 链式查找
item = tab.ele('#form')('tag:input')

# 相对位置
ele = tab.ele('text=文档')
next_ele = ele.next()      # 后一个元素
prev_ele = ele.prev()     # 前一个元素
parent_ele = ele.parent   # 父元素
```

### 2.3 相对定位方法

| 方法 | 说明 |
|------|------|
| `ele.next()` | 获取后一个相邻元素 |
| `ele.prev()` | 获取前一个相邻元素 |
| `ele.parent` | 获取父元素 |
| `ele.eles()` | 获取所有子元素 |
| `ele.first()` | 获取第一个子元素 |
| `ele.last()` | 获取最后一个子元素 |

### 2.4 等待元素

```python
# 等待元素可见
tab.wait.ele_visible('#kw')

# 等待元素显示
tab.wait.ele_displayed('#modal')

# 等待元素隐藏
tab.wait.ele_hidden('#loading')

# 等待元素删除
tab.wait.ele_deleted('#toast')

# 等待元素可用
tab.wait.ele_enabled('#submit')
```

---

## 第三部分：元素交互

### 3.1 点击操作

```python
# 基本点击
ele.click()

# JavaScript 点击（无视遮挡）
ele.click(by_js=True)

# 右键点击
ele.click.right()

# 中键点击（在新标签页打开）
new_tab = ele.click.middle()

# 多次点击
ele.click.multi(3)

# 偏移点击（相对于元素左上角）
ele.click.at(10, 10)

# 点击等待新标签页
new_tab = ele.click.for_new_tab()
```

### 3.2 输入操作

```python
# 输入文本
ele.input('Hello World')

# 输入并回车
ele.input('search query\n')

# 输入前清空
ele.input('new text', clear=True)

# 使用 JavaScript 输入
ele.input('text', by_js=True)

# 清空
ele.clear()
ele.clear(by_js=True)

# 获取焦点
ele.focus()
```

### 3.3 组合键输入

```python
from DrissionPage.common import Keys

# 全选
ele.input((Keys.CTRL, 'a'))

# 复制粘贴
ele.input((Keys.CTRL, 'c'))
ele.input((Keys.CTRL, 'v'))

# 使用内置快捷键
ele.input(Keys.CTRL_A)  # 全选
ele.input(Keys.CTRL_C)  # 复制
ele.input(Keys.CTRL_V)  # 粘贴
ele.input(Keys.CTRL_X)  # 剪切
```

### 3.4 下拉选择

```python
# 获取 select 元素
select_ele = tab.ele('tag:select')

# 按文本选择
select_ele.select.by_text('选项1')

# 按 value 选择
select_ele.select.by_value('value1')

# 按索引选择（从1开始）
select_ele.select.by_index(1)

# 多选
select_ele.select.by_text(['选项1', '选项2'])

# 取消选择
select_ele.select.cancel_by_text('选项1')

# 全选
select_ele.select.all()

# 取消全选
select_ele.select.clear()

# 反选
select_ele.select.invert()
```

### 3.5 拖拽操作

```python
# 拖拽到相对位置
ele.drag(100, 50)

# 拖拽到目标元素
target = tab.ele('#target')
ele.drag_to(target)

# 拖拽到坐标
ele.drag_to((500, 300))

# 设置拖拽时间
ele.drag(100, 100, duration=1)
```

### 3.6 悬停操作

```python
# 悬停到元素
ele.hover()

# 带偏移悬停
ele.hover(10, -10)
```

---

## 第四部分：等待机制

DrissionPage 内置智能等待机制，提高脚本稳定性。

### 4.1 页面等待

```python
# 等待页面开始加载
tab.wait.load_start()

# 等待文档加载完成
tab.wait.doc_loaded()

# 等待元素加载到 DOM
tab.wait.eles_loaded('#new-element')

# 等待下载开始
mission = tab.wait.download_begin()

# 等待下载完成
tab.wait.downloads_done()
```

### 4.2 元素等待

```python
# 等待元素显示
ele.wait.displayed()
ele.wait.displayed(timeout=5)

# 等待元素隐藏
ele.wait.hidden()

# 等待元素删除
ele.wait.deleted()

# 等待元素可用
ele.wait.enabled()

# 等待元素不可用
ele.wait.disabled()

# 等待元素可点击
ele.wait.clickable()

# 等待元素停止运动
ele.wait.stop_moving()

# 等待元素不被遮挡
ele.wait.not_covered()
```

### 4.3 页面状态等待

```python
# 等待 URL 变化
tab.wait.url_change('example.com')

# 等待标题变化
tab.wait.title_change('新标题')

# 等待弹出框关闭
tab.wait.alert_closed()

# 等待新标签页
new_tab_id = browser.wait.new_tab()
```

### 4.4 随机等待

```python
# 固定等待
tab.wait(2)

# 随机等待（3.5-8.5秒之间）
tab.wait(3.5, 8.5)
```

---

## 第五部分：网络监听

### 5.1 基本用法

```python
# 开始监听
tab.listen.start('api.example.com')

# 执行操作触发请求
tab.ele('#load-more').click()

# 等待数据包
packet = tab.listen.wait()

# 获取请求信息
print(packet.request.url)
print(packet.request.method)
print(packet.request.headers)
print(packet.request.postData)

# 获取响应信息
print(packet.response.status)
print(packet.response.body)

# 停止监听
tab.listen.stop()
```

### 5.2 实时获取

```python
# 开始监听
tab.listen.start('api.')

# 实时获取多个数据包
for packet in tab.listen.steps():
    print(packet.url)
    if some_condition:
        break
```

### 5.3 监听设置

```python
# 监听多个域名
tab.listen.start(['api1.com', 'api2.com'])

# 使用正则表达式
tab.listen.start(r'api\d+\.com', is_regex=True)

# 监听特定请求类型
tab.listen.start('api.', method='POST')

# 监听特定资源类型
tab.listen.start('api.', res_type='xhr')

# 等待所有请求完成
tab.listen.wait_silent()
```

### 5.4 DataPacket 对象

```python
# 请求信息
packet.request.url         # 请求 URL
packet.request.method      # 请求方法
packet.request.params      # URL 参数
packet.request.headers     # 请求头
packet.request.cookies    # Cookie
packet.request.postData   # POST 数据

# 响应信息
packet.response.url        # 响应 URL
packet.response.status     # 状态码
packet.response.headers    # 响应头
packet.response.body       # 响应体（自动解析 JSON）

# 其他信息
packet.resourceType        # 资源类型
packet.is_failed          # 是否失败
```

---

## 第六部分：动作链

### 6.1 基本用法

```python
# 使用内置 actions 属性
tab.actions.move_to('#kw').click().type('DrissionPage')

# 或创建动作链对象
from DrissionPage.common import Actions
ac = Actions(tab)
ac.move_to('#kw').click().type('DrissionPage')
```

### 6.2 鼠标操作

```python
# 移动到元素
tab.actions.move_to('#element')

# 移动到坐标
tab.actions.move_to((100, 200))

# 相对移动
tab.actions.move(100, 50)
tab.actions.up(50)
tab.actions.down(50)
tab.actions.left(50)
tab.actions.right(50)

# 点击
tab.actions.click('#element')
tab.actions.r_click('#element')   # 右键
tab.actions.m_click('#element')   # 中键

# 按住和释放
tab.actions.hold('#element')      # 按住左键
tab.actions.release()              # 释放
tab.actions.release('#element')   # 释放（在目标上）
```

### 6.3 键盘操作

```python
from DrissionPage.common import Keys

# 按键按下和提起
tab.actions.key_down('ENTER')
tab.actions.key_up('ENTER')

# 输入文本
tab.actions.type('Hello')

# 组合键
tab.actions.type((Keys.CTRL, 'a'))
tab.actions.type((Keys.CTRL, 'c'))
```

### 6.4 滚轮滚动

```python
# 滚动
tab.actions.scroll(0, 500)   # 向下滚动
tab.actions.scroll(0, -500)  # 向上滚动
tab.actions.scroll(500, 0)    # 向右滚动
```

### 6.5 拖拽文件

```python
# 拖入文件
tab.actions.drag_in('#drop-zone', files=['path/to/file.txt'])

# 拖入文本
tab.actions.drag_in('#drop-zone', text='some text')
```

---

## 第七部分：SessionPage

### 7.1 基本用法

SessionPage 使用数据包方式访问网页，无需启动浏览器。

```python
from DrissionPage import SessionPage

page = SessionPage()

# GET 请求
page.get('https://example.com')

# POST 请求
page.post('https://api.example.com', data={'key': 'value'})

# 查找元素
title = page.ele('tag:h1')
items = page.eles('tag:li')

# 获取信息
print(page.title)
print(page.url)
print(page.html)
```

### 7.2 请求设置

```python
# 设置请求头
page.headers.update({'Authorization': 'Bearer token'})

# 设置代理
page.proxies.update({'http': 'http://proxy.com'})

# 携带 Cookie
page.cookies.set('name', 'value')
```

---

## 第八部分：JavaScript 执行

### 8.1 执行脚本

```python
# 执行 JavaScript
result = tab.run_js('return document.title')

# 带参数
result = tab.run_js('return arguments[0] * arguments[1]', 2, 3)

# 元素上执行
ele.run_js('this.scrollIntoView()')
result = ele.run_js('return this.offsetHeight')
```

### 8.2 异步执行

```python
# 异步执行（不等待结果）
tab.run_async_js('console.log("async")')
```

### 8.3 初始化脚本

```python
# 添加初始化脚本（在页面加载前执行）
script_id = ele.add_init_js('console.log("init")')

# 删除初始化脚本
ele.remove_init_js(script_id)
```

---

## 第九部分：Cookie 操作

### 9.1 获取 Cookie

```python
# 获取所有 Cookie
cookies = tab.cookies()

# 获取单个 Cookie
cookie = tab.cookie('name')

# 获取 Cookie 格式的 dict
cookies_dict = tab.cookies(as_dict=True)
```

### 9.2 设置 Cookie

```python
# 设置单个 Cookie
tab.set.cookies({'name': 'value'})

# 设置多个 Cookie
tab.set.cookies([
    {'name': 'name1', 'value': 'value1'},
    {'name': 'name2', 'value': 'value2'}
])

# 设置带属性的 Cookie
tab.set.cookies({
    'name': 'value',
    'domain': '.example.com',
    'path': '/',
    'expires': '2024-12-31'
})
```

### 9.3 删除 Cookie

```python
# 删除指定 Cookie
tab.delete.cookies('name')

# 删除所有 Cookie
tab.delete.cookies()
```

---

## 第十部分：下载功能

### 10.1 配置下载

```python
from DrissionPage import Chromium, ChromiumOptions

# 设置下载路径
co = ChromiumOptions()
co.set_download_path('./downloads')

browser = Chromium(addr_or_opts=co)
```

### 10.2 点击下载

```python
# 点击触发下载
mission = tab.ele('#download-btn').click.to_download(
    save_path='./downloads',
    rename='file.pdf'
)

# 等待下载完成
mission.wait()
print(mission.state)  # done, failed, canceled
```

### 10.3 下载任务对象

```python
# 获取下载状态
mission.state       # 状态
mission.file_path   # 文件路径
mission.total      # 总大小
mission.now        # 已下载
mission.rate       # 下载速度

# 取消下载
mission.cancel()

# 暂停/继续
mission.pause()
mission.resume()
```

---

## 第十一部分：iframe 操作

### 11.1 基本操作

```python
# 获取 iframe 元素
iframe = tab.ele('tag:iframe')

# 在 iframe 中查找元素
ele = iframe.ele('#content')

# 相当于直接操作
ele = tab.ele('iframe#frame')('#content')
```

---

## 第十二部分：截图和录像

### 12.1 截图

```python
# 对整个页面截图
tab.get_screenshot(path='page.png')

# 对视口截图
tab.get_screenshot(path='viewport.png', fullpage=False)

# 对元素截图
ele.screenshot(path='element.png')
```

### 12.2 录像

```python
# 开始录像
tab.record.start()

# ... 执行操作 ...

# 结束录像并保存
tab.record.stop(path='video.mp4')
```

---

## 第十三部分：错误处理

### 13.1 常用异常

```python
from DrissionPage.errors import (
    ElementNotFoundError,      # 元素未找到
    ElementLostError,          # 元素丢失
    TimeoutError,              # 超时错误
    CallError,                 # 调用错误
    BrowserConnectError,      # 浏览器连接错误
    LoginFailedError          # 登录失败
)
```

### 13.2 异常处理示例

```python
try:
    ele = tab.ele('#id')
    ele.click()
except ElementNotFoundError:
    print("元素未找到")
except TimeoutError:
    print("等待超时")
except Exception as e:
    print(f"其他错误: {e}")
```

---

## 第十四部分：最佳实践

### 14.1 常见场景

#### 场景1：百度搜索

```python
from DrissionPage import Chromium

browser = Chromium()
tab = browser.latest_tab

tab.get('https://www.baidu.com')
tab.ele('#kw').input('DrissionPage')
tab.ele('#su').click()

# 获取结果
results = tab.eles('tag:h3')
for r in results[:10]:
    print(r.text)

browser.quit()
```

#### 场景2：登录操作

```python
from DrissionPage import Chromium

browser = Chromium()
tab = browser.latest_tab

tab.get('https://login.example.com')
tab.ele('#username').input('myuser')
tab.ele('#password').input('mypass\n')

# 等待登录成功
tab.wait.url_change('example.com/dashboard')

browser.quit()
```

#### 场景3：分页数据采集

```python
from DrissionPage import Chromium

browser = Chromium()
tab = browser.latest_tab

all_data = []
page = 1

while page <= 10:
    tab.get(f'https://example.com/list?page={page}')
    
    items = tab.eles('.item')
    for item in items:
        all_data.append(item.text)
    
    # 点击下一页
    if not tab.ele('.next-page'):
        break
    tab.ele('.next-page').click()
    page += 1

print(f"共采集 {len(all_data)} 条数据")
browser.quit()
```

#### 场景4：API 数据监听

```python
from DrissionPage import Chromium

browser = Chromium()
tab = browser.latest_tab

tab.get('https://example.com')

# 开始监听 API
tab.listen.start('api.example.com/data')

# 触发请求
tab.ele('#load-data').click()

# 等待数据
packet = tab.listen.wait()

# 直接获取 JSON 数据
data = packet.response.body
print(data)

tab.listen.stop()
browser.quit()
```

### 14.2 性能优化

1. **使用 SessionPage**：静态页面使用 SessionPage 提高速度
2. **设置加载模式**：`set_load_mode('eager')` 减少等待时间
3. **禁用不必要的资源**：`no_imgs(True)` 减少加载
4. **复用浏览器**：调试完成后复用浏览器
5. **合理使用等待**：避免固定 sleep，使用智能等待

### 14.3 调试技巧

1. **非无头模式**：开发时使用 `headless=False` 观察行为
2. **保存 Cookie**：登录后可保存 Cookie 复用
3. **浏览器复用**：程序结束后不关闭浏览器便于调试

```python
# 开发配置
co = ChromiumOptions()
co.headless(False)  # 有头模式
co.set_timeouts(base=30)  # 增加超时
```

---

## 第十五部分：常见问题

### Q1: 浏览器启动失败

检查浏览器路径或端口是否被占用：
```python
co = ChromiumOptions()
co.set_browser_path(r'D:\chrome.exe')
co.set_local_port(9333)
```

### Q2: 元素找不到

使用智能等待：
```python
tab.wait.ele_visible('#element')
ele = tab.ele('#element')
```

### Q3: 下载失败

无头模式需要配置：
```python
co = ChromiumOptions()
co.set_download_path('./downloads')
co.headless(True)
```

### Q4: 被检测为自动化

使用默认配置，DrissionPage 无 WebDriver 特征。

### Q5: 内存占用高

使用无头模式并定期重启浏览器：
```python
# 使用临时用户目录
co = ChromiumOptions()
co.auto_port(True)
```

---

## 参考资源

- 官方文档：https://www.drissionpage.cn
- GitHub：https://github.com/g1879/DrissionPage
- Gitee：https://gitee.com/g1879/DrissionPage
