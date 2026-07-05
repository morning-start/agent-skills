# DynamicFetcher 动态网站抓取

## 概述

DynamicFetcher 是 Scrapling 框架中用于处理动态渲染网页的获取器。它使用无头浏览器（Headless Browser）来执行 JavaScript 并等待页面完全渲染后再获取内容。

DynamicFetcher 特别适用于：
- JavaScript 框架构建的单页应用（SPA）
- 使用懒加载技术的网站
- 需要与页面交互（点击、滚动）才能获取完整内容的网站
- 无限滚动页面
- 需要等待 API 异步加载数据的页面

## 安装

```bash
pip install scrapling
pip install "scrapling[fetchers]"

# 下载浏览器依赖（必需）
scrapling install

# 或强制重新安装
scrapling install --force
```

## 基本用法

### 创建 DynamicFetcher

```python
from scrapling.fetchers import DynamicFetcher

# 创建默认配置的动态获取器
fetcher = DynamicFetcher()

# 获取动态渲染的页面
page = fetcher.fetch('https://example.com')

# 获取渲染后的 HTML
print(page.html)
```

### 浏览器选项

```python
# 配置浏览器
fetcher = DynamicFetcher(
    browser='chrome',    # chrome, firefox
    headless=True,      # 是否无头运行
    images=False,       # 禁用图片加载（提升速度）
    javascript=True,    # 启用 JavaScript（默认）
)
```

## 等待策略

DynamicFetcher 提供了多种等待策略来确保页面完全渲染。

### 等待选择器

```python
fetcher = DynamicFetcher()

# 等待指定选择器出现
page = fetcher.fetch('https://example.com', wait_for='#content')

# 等待多个选择器之一出现
page = fetcher.fetch('https://example.com', wait_for=['#main', '.content', 'section'])

# 等待选择器消失
page = fetcher.fetch('https://example.com', wait_for_selector_gone='.loading')
```

### 等待网络请求

```python
# 等待网络空闲（默认）
page = fetcher.fetch('https://example.com', wait_network=True)

# 等待网络空闲超时（毫秒）
page = fetcher.fetch('https://example.com', wait_network_idle_timeout=3000)

# 等待特定网络请求完成
page = fetcher.fetch('https://example.com', wait_for_request='**/api/data*')
```

### 等待时间

```python
# 等待固定时间（毫秒）
page = fetcher.fetch('https://example.com', wait_for=2000)
```

### 等待 JavaScript 条件

```python
# 等待 JavaScript 条件满足
page = fetcher.fetch('https://example.com', wait_for_js='document.readyState === "complete"')

# 等待自定义变量
page = fetcher.fetch('https://example.com', wait_for_js='window.isLoaded === true')

# 等待元素可见
page = fetcher.fetch('https://example.com', wait_for_js='''
    document.querySelector('.content') !== null && 
    getComputedStyle(document.querySelector('.content')).display !== 'none'
''')
```

### 等待 URL 变化

```python
# 等待 URL 匹配模式
page = fetcher.fetch('https://example.com', wait_for_url='**/done*')

# 等待 URL 包含特定内容
page = fetcher.fetch('https://example.com', wait_for_url='*example.com/results*')
```

## 页面滚动

DynamicFetcher 支持多种滚动策略来触发懒加载内容。

### 滚动到底部

```python
# 滚动到页面底部
page = fetcher.fetch('https://example.com', scroll_to_bottom=True)
```

### 滚动次数和间隔

```python
# 滚动指定次数
page = fetcher.fetch('https://example.com', scroll_times=5)

# 滚动间隔时间（毫秒）
page = fetcher.fetch('https://example.com', scroll_times=3, scroll_interval=1000)

# 滚动并等待
page = fetcher.fetch('https://example.com', scroll_times=5, wait_network=True)
```

### 滚动到元素

```python
# 执行滚动到元素
page = fetcher.fetch('https://example.com', scroll_to='#load-more')

# 滚动到特定位置
page = fetcher.fetch('https://example.com', scroll_position=500)
```

## JavaScript 执行

### 执行自定义 JavaScript

```python
fetcher = DynamicFetcher()

# 在页面加载后执行 JavaScript
page = fetcher.fetch('https://example.com', js_code='''
    // 获取页面数据
    window.pageData;
''')

# 返回数据
data = page.js_result

# 执行点击操作
page = fetcher.fetch('https://example.com', js_code='''
    document.querySelector('#load-more').click();
''')

# 填充表单
page = fetcher.fetch('https://example.com/form', js_code='''
    document.querySelector('#username').value = 'test';
    document.querySelector('#password').value = 'pass';
    document.querySelector('form').submit();
''')
```

### 加载后执行脚本

```python
# 页面完全加载后执行
page = fetcher.fetch('https://example.com', after_load_js='''
    console.log('页面已加载');
    window.scrollTo(0, document.body.scrollHeight);
''')
```

## 页面交互

### 点击元素

```python
# 通过选择器点击元素
page = fetcher.fetch('https://example.com', click='#load-more')

# 点击多个元素（逐个点击）
page = fetcher.fetch('https://example.com', click=['.load-more-1', '.load-more-2'])
```

### 表单处理

```python
# 填写表单并提交
page = fetcher.fetch('https://example.com/login', form={
    'username': 'user',
    'password': 'pass'
}, submit=True)

# 选择下拉选项
page = fetcher.fetch('https://example.com/form', select={
    'country': 'CN',
    'city': 'Shanghai'
})
```

### 键盘操作

```python
# 模拟键盘输入
page = fetcher.fetch('https://example.com', type_keys={
    'input.search': '搜索内容'
})

# 模拟特殊键
page = fetcher.fetch('https://example.com', press_key='#search-input', key='Enter')
```

## 加载策略

```python
# eager: 立即返回，不等待资源加载
fetcher = DynamicFetcher(load_strategy='eager')

# domcontentloaded: 等待 DOM 加载完成
fetcher = DynamicFetcher(load_strategy='domcontentloaded')

# normal: 等待所有资源加载完成（默认）
fetcher = DynamicFetcher(load_strategy='normal')
```

## 浏览器配置

### 无头模式

```python
# 默认无头模式
fetcher = DynamicFetcher(headless=True)

# 有头模式（调试用）
fetcher = DynamicFetcher(headless=False)
```

### 禁用资源

```python
# 禁用图片
fetcher = DynamicFetcher(images=False)

# 禁用 CSS
fetcher = DynamicFetcher(stylesheets=False)

# 禁用 JavaScript（变成普通获取器）
fetcher = DynamicFetcher(javascript=False)
```

### 用户数据目录

```python
# 使用已存在的用户数据目录（保持登录状态）
fetcher = DynamicFetcher(user_data_dir='/path/to/profile')

# 匿名模式（不保存 Cookie）
fetcher = DynamicFetcher(incognito=True)
```

### 代理配置

```python
# HTTP 代理
fetcher = DynamicFetcher(proxy='http://proxy.com:8080')

# 带认证的代理
fetcher = DynamicFetcher(proxy='http://user:pass@proxy.com:8080')

# SOCKS 代理
fetcher = DynamicFetcher(proxy='socks5://proxy.com:1080')
```

## Cookie 管理

```python
fetcher = DynamicFetcher()

# 设置 Cookie
page = fetcher.fetch('https://example.com', cookies={
    'session_id': 'abc123',
    'preferences': 'dark'
})

# 从响应获取 Cookie
page = fetcher.fetch('https://example.com')
print(page.cookies)

# 导出 Cookie
cookies = fetcher.dump_cookies()

# 加载 Cookie
fetcher.load_cookies(cookies)
```

## 错误处理

```python
from scrapling.fetchers import DynamicFetcher, FetcherError

fetcher = DynamicFetcher()

try:
    page = fetcher.fetch('https://example.com')
except FetcherError as e:
    print(f"获取失败: {e}")

# 使用错误处理
result = fetcher.fetch('https://example.com', handle_errors=True)
if result.error:
    print(f"错误: {result.error_message}")
else:
    page = result.response
```

## 选择器集成

DynamicFetcher 返回的对象完全支持 CSS 和 XPath 选择器。

```python
fetcher = DynamicFetcher()

page = fetcher.fetch('https://example.com')

# CSS 选择器
items = page.css('.product')
for item in items:
    print(item.css('.title::text').get())

# XPath 选择器
links = page.xpath('//a/@href').getall()

# 正则表达式
prices = page.css('.price::text').re(r'\d+\.?\d*')
```

## 场景示例

### 场景1：抓取懒加载图片

```python
from scrapling.fetchers import DynamicFetcher

fetcher = DynamicFetcher(images=False)

# 获取页面并滚动到底部
page = fetcher.fetch('https://example.com/gallery', scroll_to_bottom=True, scroll_times=3)

# 提取图片
images = page.css('img.lazy::attr(data-src)').getall()
print(f"找到 {len(images)} 张图片")
```

### 场景2：无限滚动页面

```python
from scrapling.fetchers import DynamicFetcher

fetcher = DynamicFetcher()

# 等待初始加载
page = fetcher.fetch('https://example.com/infinite-scroll', wait_for='.items')

# 滚动加载更多
for i in range(5):
    page = fetcher.fetch('https://example.com/infinite-scroll', 
                        scroll_to_bottom=True,
                        wait_network=True)
    print(f"滚动后条目数: {len(page.css('.item').getall())}")
```

### 场景3：点击加载更多

```python
from scrapling.fetchers import DynamicFetcher

fetcher = DynamicFetcher()

page = fetcher.fetch('https://example.com')

# 点击加载更多按钮
while page.css('.load-more'):
    page = fetcher.fetch('https://example.com', click='.load-more')
    page = fetcher.fetch('https://example.com', wait_network=True)

# 获取所有数据
items = page.css('.item::text').getall()
print(f"共获取 {len(items)} 条数据")
```

### 场景4：表单登录

```python
from scrapling.fetchers import DynamicFetcher

fetcher = DynamicFetcher()

# 提交登录表单
page = fetcher.fetch('https://example.com/login', form={
    'username': 'your_username',
    'password': 'your_password'
}, submit=True, wait_for='#dashboard')

# 验证登录成功
if page.css('.user-info'):
    print("登录成功")
```

### 场景5：处理模态框

```python
from scrapling.fetchers import DynamicFetcher

fetcher = DynamicFetcher()

page = fetcher.fetch('https://example.com')

# 点击打开模态框
page = fetcher.fetch('https://example.com', click='.open-modal')

# 等待模态框出现
page = fetcher.fetch('https://example.com', wait_for='.modal.show')

# 获取模态框内容
modal_content = page.css('.modal-body::text').get()

# 关闭模态框
page = fetcher.fetch('https://example.com', click='.modal-close')
```

### 场景6：等待 API 数据

```python
from scrapling.fetchers import DynamicFetcher

fetcher = DynamicFetcher()

# 等待特定 API 请求完成
page = fetcher.fetch('https://example.com', 
                    wait_for_request='**/api/data*',
                    wait_network=True)

# 提取 API 返回的数据
data = page.css('#app-data::text').get()
import json
app_data = json.loads(data)
print(app_data)
```

### 场景7：Shadow DOM 处理

```python
from scrapling.fetchers import DynamicFetcher

fetcher = DynamicFetcher()

page = fetcher.fetch('https://example.com')

# 处理 Shadow DOM
shadow_content = page.css('custom-element::shadow .content').get()

# 或使用 JavaScript
result = page.js('''
    document.querySelector('custom-element').shadowRoot.querySelector('.content').textContent
''')
```

## 性能优化

### 减少加载时间

```python
# 禁用图片
fetcher = DynamicFetcher(images=False)

# 禁用 CSS
fetcher = DynamicFetcher(stylesheets=False)

# 使用 eager 加载策略
fetcher = DynamicFetcher(load_strategy='eager')

# 禁用 JavaScript（如果不需要）
fetcher = DynamicFetcher(javascript=False)
```

### 并发处理

```python
# 减少等待时间
page = fetcher.fetch('https://example.com', wait_for=1000)

# 使用选择器等待替代网络等待
page = fetcher.fetch('https://example.com', wait_for='#content', wait_network=False)
```

### 资源限制

```python
# 限制内存使用
fetcher = DynamicFetcher(
    disable_gpu=False,
    no_sandbox=True,
    disable_dev_shm_usage=True
)
```

## 调试技巧

### 有头模式

```python
# 开启有头模式查看浏览器行为
fetcher = DynamicFetcher(headless=False)

page = fetcher.fetch('https://example.com')
```

### 保存截图

```python
# 保存页面截图
page = fetcher.fetch('https://example.com')
page.save_screenshot('page.png')

# 保存完整截图
page.save_screenshot('full.png', full_page=True)
```

### 获取控制台日志

```python
# 获取浏览器控制台输出
page = fetcher.fetch('https://example.com')
print(page.console_logs)
```

## 注意事项

1. **性能开销**：无头浏览器比普通 HTTP 请求慢很多，仅在需要时使用
2. **资源消耗**：占用较多内存和 CPU
3. **反检测**：某些网站会检测无头浏览器
4. **等待策略**：合理设置等待时间，避免过早返回
5. **频率控制**：避免过快请求被封禁

## 相关链接

- [Fetcher 基础 HTTP 请求](./fetcher.md)
- [StealthyFetcher 反检测抓取](./stealthy-fetcher.md)
- [官方文档](https://scrapling.readthedocs.io/en/latest/fetchers.html)
