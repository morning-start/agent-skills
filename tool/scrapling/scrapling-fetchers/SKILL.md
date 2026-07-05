---
name: scrapling-fetchers
description: Scrapling Fetchers 获取器技能
version: 1.0.0
---

# Scrapling Fetchers 获取器技能

## 技能概述

Scrapling Fetchers 是 Scrapling 框架中的 HTTP 请求组件，提供了多种获取器来满足不同的网页抓取需求。Fetchers 模块能够自动处理反爬虫机制，支持 JavaScript 渲染页面，并提供类似浏览器的请求能力。

Scrapling 提供了三种主要的获取器：
- **Fetcher**：基础 HTTP 请求获取器，基于 httpx 库
- **StealthyFetcher**：反检测抓取获取器，模拟真实浏览器行为
- **DynamicFetcher**：动态网站获取器，支持 JavaScript 渲染

## 核心特性

- **多种获取器类型**：从简单请求到复杂反爬虫场景
- **自动 Cookie 处理**：会话级别的 Cookie 管理
- **自动重定向处理**：智能处理 HTTP 重定向
- **请求/响应拦截**：支持中间件扩展
- **反检测能力**：StealthyFetcher 模拟真实浏览器
- **JavaScript 支持**：DynamicFetcher 执行 JS 渲染页面
- **代理支持**：内置代理轮换和认证
- **会话管理**：多会话支持，独立 Cookie 罐

## 快速开始

### 安装

```bash
pip install scrapling
pip install "scrapling[fetchers]"

# 下载浏览器依赖（DynamicFetcher 需要）
scrapling install
```

### 第一个示例

```python
from scrapling.fetchers import Fetcher

# 创建获取器实例
fetcher = Fetcher()

# 获取网页
page = fetcher.fetch('https://example.com')

# page 直接支持 CSS 选择器
print(page.css('h1::text').get())

# 获取原始 HTML
print(page.text)
```

---

## 第一部分：Fetcher 基础获取器

### 1.1 创建和使用

Fetcher 是最基础的获取器，基于 httpx 库实现。

```python
from scrapling.fetchers import Fetcher

# 创建获取器
fetcher = Fetcher()

# 基本 GET 请求
page = fetcher.fetch('https://example.com')

# 获取响应内容
print(page.text)           # 原始文本
print(page.html)           # HTML 内容
print(page.status)         # 状态码
print(page.url)            # 最终 URL（处理重定向后）
```

### 1.2 请求选项

```python
fetcher = Fetcher()

# 带参数的 GET 请求
page = fetcher.fetch('https://api.example.com/search', params={'q': 'python'})

# POST 请求
page = fetcher.fetch('https://api.example.com/login', method='POST', data={
    'username': 'user',
    'password': 'pass'
})

# JSON 请求
page = fetcher.fetch('https://api.example.com/data', method='POST', json={
    'key': 'value'
})
```

### 1.3 请求头管理

```python
fetcher = Fetcher()

# 自定义请求头
page = fetcher.fetch('https://example.com', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://google.com'
})

# 设置默认请求头
fetcher = Fetcher(defaults={'User-Agent': 'MyBot/1.0'})
```

### 1.4 超时和重试

```python
fetcher = Fetcher()

# 设置超时
page = fetcher.fetch('https://example.com', timeout=30)

# 设置重试
page = fetcher.fetch('https://example.com', retries=3, retry_delay=2)

# 设置连接超时和读取超时
page = fetcher.fetch('https://example.com', timeout=(5, 30))  # (连接, 读取)
```

---

## 第二部分：StealthyFetcher 反检测获取器

### 2.1 创建和使用

StealthyFetcher 专门设计用于绕过反爬虫检测，模拟真实浏览器的请求行为。

```python
from scrapling.fetchers import StealthyFetcher

# 创建反检测获取器
fetcher = StealthyFetcher()

# 基本请求（自动添加浏览器指纹）
page = fetcher.fetch('https://example.com')

# 支持 JavaScript 执行前的等待
page = fetcher.fetch('https://example.com', wait_for='body')
```

### 2.2 浏览器指纹

StealthyFetcher 自动模拟以下浏览器特征：

- **User-Agent**：随机真实浏览器 User-Agent
- **Accept-Language**：真实浏览器语言头
- **Accept-Encoding**：真实浏览器编码
- **Connection**：keep-alive
- **Cache-Control**：浏览器缓存控制

```python
# 自定义浏览器配置
fetcher = StealthyFetcher(
    # 浏览器配置
    browser='chrome',  # chrome, firefox, edge
    platform='win32',  # win32, macos, linux
    mobile=False,
    
    # 语言配置
    locales=['zh-CN', 'zh', 'en-US', 'en'],
    
    # 屏幕配置
    screen=(1920, 1080),
    
    # 时区
    timezone='Asia/Shanghai'
)
```

### 2.3 等待策略

```python
fetcher = StealthyFetcher()

# 等待 DOM 元素出现
page = fetcher.fetch('https://example.com', wait_for='#content')

# 等待指定时间（毫秒）
page = fetcher.fetch('https://example.com', wait_for=2000)

# 等待 JavaScript 条件满足
page = fetcher.fetch('https://example.com', wait_for='document.readyState === "complete"')

# 等待网络空闲
page = fetcher.fetch('https://example.com', wait_for_idle=True)
```

### 2.4 处理 Cloudflare

```python
fetcher = StealthyFetcher()

# Cloudflare 挑战处理（自动）
page = fetcher.fetch('https://cloudflare-protected-site.com')

# 强制等待挑战完成
page = fetcher.fetch('https://cloudflare-protected-site.com', cloudflare=True)

# 设置挑战超时
page = fetcher.fetch('https://cloudflare-protected-site.com', cloudflare_timeout=60)
```

### 2.5 代理轮换

```python
# 使用代理
fetcher = StealthyFetcher(proxy='http://user:pass@proxy.com:8080')

# 代理列表轮换
fetcher = StealthyFetcher(
    proxies=[
        'http://proxy1.com:8080',
        'http://proxy2.com:8080',
    ],
    proxy_rotation='random'  # random, round_robin
)
```

---

## 第三部分：DynamicFetcher 动态网站获取器

### 3.1 创建和使用

DynamicFetcher 使用无头浏览器执行 JavaScript，适用于需要渲染动态内容的网站。

```python
from scrapling.fetchers import DynamicFetcher

# 创建动态获取器
fetcher = DynamicFetcher()

# 获取动态渲染的页面
page = fetcher.fetch('https://example.com')

# 获取渲染后的 HTML
print(page.html)
```

### 3.2 浏览器配置

```python
fetcher = DynamicFetcher()

# 配置浏览器选项
fetcher = DynamicFetcher(
    # 浏览器类型
    browser='chrome',  # chrome, firefox
    
    # 无头模式（默认 True）
    headless=True,
    
    # 禁用图片加载（提升速度）
    images=False,
    
    # 禁用 JavaScript（可选）
    # javascript=False,
    
    # 页面加载策略
    # eager: 立即返回，domcontentloaded: 等待 DOM，normal: 等待完全加载
    load_strategy='eager'
)
```

### 3.3 等待策略

```python
fetcher = DynamicFetcher()

# 等待指定选择器出现
page = fetcher.fetch('https://example.com', wait_for='.content')

# 等待多个选择器之一出现
page = fetcher.fetch('https://example.com', wait_for=['#main', '.content'])

# 等待网络请求完成
page = fetcher.fetch('https://example.com', wait_network=True)

# 等待指定时间
page = fetcher.fetch('https://example.com', wait_for=3000)

# 等待 JavaScript 条件
page = fetcher.fetch('https://example.com', wait_for_js='window.isLoaded === true')

# 等待 URL 变化
page = fetcher.fetch('https://example.com', wait_for_url='**/done*')
```

### 3.4 滚动和交互

```python
fetcher = DynamicFetcher()

# 获取页面并滚动到底部（触发懒加载）
page = fetcher.fetch('https://example.com', scroll_to_bottom=True)

# 滚动次数
page = fetcher.fetch('https://example.com', scroll_times=5)

# 滚动间隔（毫秒）
page = fetcher.fetch('https://example.com', scroll_interval=1000)
```

### 3.5 执行自定义 JavaScript

```python
fetcher = DynamicFetcher()

# 在页面加载后执行 JavaScript
page = fetcher.fetch('https://example.com', js_code='''
    // 点击按钮
    document.querySelector('#load-more').click();
    
    // 返回页面数据
    window.pageData;
''')

# 执行额外脚本
page = fetcher.fetch('https://example.com', after_load_js='''
    // 页面加载后执行
    console.log('Page loaded');
''')
```

---

## 第四部分：高级用法

### 4.1 会话管理

```python
fetcher = Fetcher()

# 创建新会话
fetcher.new_session()

# 指定会话 ID
fetcher.new_session(session_id='my_session')

# 清除会话
fetcher.clear_session()

# 获取当前会话 ID
print(fetcher.session_id)
```

### 4.2 Cookie 管理

```python
fetcher = Fetcher()

# 从响应获取 Cookie
page = fetcher.fetch('https://example.com')
cookies = page.cookies

# 设置 Cookie
page = fetcher.fetch('https://example.com', cookies={
    'session_id': 'abc123',
    'user_preference': 'dark'
})

# 从字典加载 Cookie
fetcher.load_cookies({'session': 'value'})

# 导出 Cookie
cookies_dict = fetcher.dump_cookies()
```

### 4.3 代理配置

```python
fetcher = Fetcher()

# 使用单个代理
page = fetcher.fetch('https://example.com', proxy='http://proxy.com:8080')

# 使用代理认证
page = fetcher.fetch('https://example.com', proxy='http://user:pass@proxy.com:8080')

# StealthyFetcher 代理轮换
stealthy = StealthyFetcher(proxies=[
    'http://proxy1.com:8080',
    'http://proxy2.com:8080',
])

# 代理验证失败时自动切换
stealthy = StealthyFetcher(
    proxies=['http://proxy1.com:8080', 'http://proxy2.com:8080'],
    proxy_rotation='sequential'
)
```

### 4.4 SSL 和证书

```python
fetcher = Fetcher()

# 禁用 SSL 验证（不推荐）
page = fetcher.fetch('https://example.com', verify=False)

# 使用自定义 CA 证书
page = fetcher.fetch('https://example.com', verify='/path/to/ca.crt')

# 客户端证书
page = fetcher.fetch('https://example.com', cert='/path/to/client.crt')
```

### 4.5 错误处理

```python
from scrapling.fetchers import Fetcher, FetcherError, NetworkError, TimeoutError

fetcher = Fetcher()

try:
    page = fetcher.fetch('https://example.com')
except TimeoutError:
    print("请求超时")
except NetworkError as e:
    print(f"网络错误: {e}")
except FetcherError as e:
    print(f"获取器错误: {e}")

# 或者使用返回的错误对象
result = fetcher.fetch('https://example.com', handle_errors=True)
if result.error:
    print(f"错误: {result.error_message}")
else:
    page = result.response
```

---

## 第五部分：选择器集成

### 5.1 直接使用选择器

所有获取器返回的对象都支持 CSS/XPath 选择器。

```python
from scrapling.fetchers import Fetcher

fetcher = Fetcher()
page = fetcher.fetch('https://example.com')

# CSS 选择器
titles = page.css('h1::text').getall()
items = page.css('.product .title::text').getall()

# XPath 选择器
links = page.xpath('//a/@href').getall()
```

### 5.2 链式请求

```python
from scrapling.fetchers import Fetcher

fetcher = Fetcher()

# 登录并获取数据
login_page = fetcher.fetch('https://example.com/login', method='POST', data={
    'username': 'user',
    'password': 'pass'
})

# 访问需要登录的页面（自动使用同一会话）
data_page = fetcher.fetch('https://example.com/dashboard')

# 提取数据
items = data_page.css('.item::text').getall()
```

### 5.3 多页面抓取

```python
from scrapling.fetchers import Fetcher

fetcher = Fetcher()

# 批量获取多个页面
urls = [
    'https://example.com/page1',
    'https://example.com/page2',
    'https://example.com/page3',
]

results = []
for url in urls:
    page = fetcher.fetch(url)
    results.append({
        'url': url,
        'title': page.css('h1::text').get(),
        'content': page.css('.content::text').get()
    })

print(results)
```

---

## 第六部分：最佳实践

### 6.1 场景1：简单网页抓取

```python
from scrapling.fetchers import Fetcher

fetcher = Fetcher()

# 抓取简单页面
page = fetcher.fetch('https://example.com')

# 提取数据
data = {
    'title': page.css('title::text').get(),
    'headings': page.css('h1::text').getall(),
    'links': page.css('a::attr(href)').getall()
}
```

### 6.2 场景2：反爬虫网站

```python
from scrapling.fetchers import StealthyFetcher

# 使用反检测获取器
fetcher = StealthyFetcher()

# 模拟浏览器请求
page = fetcher.fetch('https://anti-bot-site.com')

# 处理可能的 Cloudflare
page = fetcher.fetch('https://cloudflare-protected.com', cloudflare=True)

# 提取数据
products = page.css('.product')
for product in products:
    print(product.css('.title::text').get())
```

### 6.3 场景3：动态内容网站

```python
from scrapling.fetchers import DynamicFetcher

# 动态网站抓取
fetcher = DynamicFetcher()

# 等待内容加载
page = fetcher.fetch('https://spa-example.com', wait_for='.loaded')

# 滚动加载更多内容
page = fetcher.fetch('https://infinite-scroll.com', scroll_to_bottom=True)

# 执行交互
page = fetcher.fetch('https://example.com', js_code='''
    document.querySelector('.load-more').click();
''')

# 提取动态渲染的内容
items = page.css('.dynamic-item::text').getall()
```

### 6.4 场景4：API 请求

```python
from scrapling.fetchers import Fetcher

fetcher = Fetcher()

# 调用 REST API
page = fetcher.fetch('https://api.example.com/users', params={
    'page': 1,
    'limit': 10
})

# 处理 JSON 响应
import json
data = json.loads(page.text)

# 或使用选择器（如果返回 HTML）
items = page.css('.user::text').getall()
```

### 6.5 场景5：代理轮换

```python
from scrapling.fetchers import StealthyFetcher

# 配置代理列表
proxies = [
    'http://proxy1.com:8080',
    'http://proxy2.com:8080',
    'http://proxy3.com:8080',
]

# 使用随机轮换
fetcher = StealthyFetcher(proxies=proxies, proxy_rotation='random')

# 批量请求，每个请求使用不同代理
for url in urls:
    page = fetcher.fetch(url)
    # 处理 page
```

### 6.6 性能优化

1. **使用 Fetcher 替代 DynamicFetcher**：除非需要 JS 渲染
2. **禁用图片加载**（DynamicFetcher）：`images=False`
3. **使用 eager 加载策略**：`load_strategy='eager'`
4. **减少等待时间**：设置合理的超时和等待
5. **复用会话**：避免频繁创建新会话

```python
# 优化示例
fetcher = DynamicFetcher(
    headless=True,
    images=False,
    load_strategy='eager'
)

page = fetcher.fetch('https://example.com', wait_for='#content', wait_for_idle=True)
```

---

## 第七部分：故障排除

### 7.1 常见问题

**问题1：请求超时**
```python
# 增加超时时间
page = fetcher.fetch('https://example.com', timeout=60)
```

**问题2：被检测**
```python
# 使用 StealthyFetcher
fetcher = StealthyFetcher()

# 或增加等待时间
page = fetcher.fetch('https://example.com', wait_for=3000)
```

**问题3：Cloudflare 挑战失败**
```python
# 增加挑战超时
page = fetcher.fetch('https://example.com', cloudflare=True, cloudflare_timeout=120)
```

**问题4：动态内容未加载**
```python
# 使用 DynamicFetcher
fetcher = DynamicFetcher()

# 滚动加载
page = fetcher.fetch('https://example.com', scroll_to_bottom=True)

# 执行加载更多
page = fetcher.fetch('https://example.com', js_code='loadMoreData()')
```

### 7.2 调试技巧

```python
from scrapling.fetchers import Fetcher

# 启用调试模式
fetcher = Fetcher(debug=True)

# 查看请求详情
page = fetcher.fetch('https://example.com')
print(page.request_headers)
print(page.response_headers)

# 保存响应到文件
with open('response.html', 'w', encoding='utf-8') as f:
    f.write(page.html)
```

---

## 参考资源

- 官方文档：https://scrapling.readthedocs.io
- Fetchers 文档：https://scrapling.readthedocs.io/en/latest/fetchers.html
- GitHub：https://github.com/pyd4vinci/scrapling
- PyPI：https://pypi.org/project/scrapling/
