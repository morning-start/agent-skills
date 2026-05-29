# StealthyFetcher 反检测抓取

## 概述

StealthyFetcher 是 Scrapling 框架中的反检测 HTTP 请求获取器，专门设计用于绕过反爬虫机制。它通过模拟真实浏览器的请求行为、浏览器指纹和请求头，使爬虫请求看起来像真实用户的浏览器访问。

StealthyFetcher 特别适用于：
- 需要绕过反爬虫检测的网站
- Cloudflare 等 CDN 保护的网站
- 有严格 User-Agent 检查的网站
- 需要模拟真实浏览器行为的场景

## 安装

```bash
pip install scrapling
pip install "scrapling[fetchers]"

# 下载浏览器依赖（用于更高级的检测）
scrapling install
```

## 基本用法

### 创建 StealthyFetcher

```python
from scrapling.fetchers import StealthyFetcher

# 创建默认配置的反检测获取器
fetcher = StealthyFetcher()

# 发送请求
page = fetcher.fetch('https://example.com')
print(page.html)
```

### 浏览器配置

```python
# 配置浏览器类型
fetcher = StealthyFetcher(
    browser='chrome',   # chrome, firefox, edge
    platform='win32',   # win32, macos, linux
    mobile=False,       # 是否模拟移动设备
)

page = fetcher.fetch('https://example.com')
```

### 语言和地区配置

```python
# 配置语言和地区
fetcher = StealthyFetcher(
    locales=['zh-CN', 'zh', 'en-US', 'en'],  # 语言优先级
    timezone='Asia/Shanghai',                # 时区
)

page = fetcher.fetch('https://example.com')
```

### 屏幕配置

```python
# 配置屏幕分辨率
fetcher = StealthyFetcher(
    screen=(1920, 1080),  # 屏幕分辨率
    screen_density=2.0,     # 屏幕密度
)
```

## 等待策略

### 等待 DOM 元素

```python
fetcher = StealthyFetcher()

# 等待指定选择器出现
page = fetcher.fetch('https://example.com', wait_for='#content')

# 等待多个选择器之一出现
page = fetcher.fetch('https://example.com', wait_for=['#main', '.content'])

# 等待网络空闲
page = fetcher.fetch('https://example.com', wait_for_idle=True)
```

### 等待时间

```python
# 等待固定时间（毫秒）
page = fetcher.fetch('https://example.com', wait_for=2000)

# 等待 JavaScript 条件满足
page = fetcher.fetch('https://example.com', wait_for='document.readyState === "complete"')
```

## Cloudflare 支持

StealthyFetcher 内置 Cloudflare 挑战处理功能。

### 自动处理

```python
fetcher = StealthyFetcher()

# 自动处理 Cloudflare 挑战
page = fetcher.fetch('https://cloudflare-protected-site.com')
```

### 手动触发

```python
# 强制触发 Cloudflare 挑战
page = fetcher.fetch('https://cloudflare-protected-site.com', cloudflare=True)

# 设置挑战超时
page = fetcher.fetch('https://cloudflare-protected-site.com', cloudflare=True, cloudflare_timeout=120)
```

### 挑战回调

```python
def on_challenge(challenge_type):
    print(f"检测到 {challenge_type} 挑战")
    # 自定义处理逻辑

fetcher = StealthyFetcher(on_challenge=on_challenge)
page = fetcher.fetch('https://cloudflare-protected-site.com')
```

## 浏览器指纹

StealthyFetcher 自动模拟以下浏览器指纹：

### 请求头

- **User-Agent**：随机真实浏览器 User-Agent
- **Accept**：浏览器通常发送的 Accept 头
- **Accept-Language**：浏览器语言设置
- **Accept-Encoding**：支持的编码格式
- **Connection**：keep-alive
- **Cache-Control**：缓存控制头
- **Upgrade-Insecure-Requests**：升级不安全请求

### TLS 指纹

```python
# 自定义 TLS 配置
fetcher = StealthyFetcher(
    tls_min_version='TLSv1.2',
    tls_max_version='TLSv1.3',
)
```

### 行为模拟

- 随机请求间隔
- 合理的访问频率
- 完整的三次握手
- 正确的请求顺序

## 代理配置

### 单个代理

```python
fetcher = StealthyFetcher()

# 使用 HTTP 代理
page = fetcher.fetch('https://example.com', proxy='http://proxy.com:8080')

# 使用 SOCKS 代理
page = fetcher.fetch('https://example.com', proxy='socks5://proxy.com:1080')
```

### 代理认证

```python
# 带认证的代理
page = fetcher.fetch('https://example.com', proxy='http://user:pass@proxy.com:8080')
```

### 代理轮换

```python
# 配置代理列表
fetcher = StealthyFetcher(
    proxies=[
        'http://proxy1.com:8080',
        'http://proxy2.com:8080',
        'http://proxy3.com:8080',
    ],
    proxy_rotation='random'  # random, round_robin, sequential
)

# 随机轮换
fetcher = StealthyFetcher(
    proxies=proxies,
    proxy_rotation='random'
)

# 顺序轮换
fetcher = StealthyFetcher(
    proxies=proxies,
    proxy_rotation='round_robin'
)

# 失败后切换
fetcher = StealthyFetcher(
    proxies=proxies,
    proxy_rotation='sequential'  # 失败后自动切换下一个
)
```

### 代理验证

```python
# 自定义代理验证函数
def validate_proxy(proxy):
    try:
        response = requests.get('http://httpbin.org/ip', proxies={'http': proxy}, timeout=5)
        return response.status_code == 200
    except:
        return False

fetcher = StealthyFetcher(
    proxies=proxies,
    validate_proxy=validate_proxy
)
```

## 请求自定义

### 自定义请求头

```python
fetcher = StealthyFetcher()

# 覆盖默认请求头
page = fetcher.fetch('https://example.com', headers={
    'X-Custom-Header': 'value',
    'Referer': 'https://custom-referer.com'
})

# 完全自定义 User-Agent
page = fetcher.fetch('https://example.com', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...'
})
```

### Cookie 管理

```python
fetcher = StealthyFetcher()

# 设置初始 Cookie
page = fetcher.fetch('https://example.com', cookies={
    'session_id': 'abc123',
    'preferences': 'dark_mode'
})

# 获取响应 Cookie
page = fetcher.fetch('https://example.com')
print(page.cookies)

# 导出所有 Cookie
cookies = fetcher.dump_cookies()
```

### 持久化会话

```python
# 保存会话
fetcher = StealthyFetcher()
fetcher.new_session()

page1 = fetcher.fetch('https://example.com/page1')
page2 = fetcher.fetch('https://example.com/page2')

# 导出 Cookie 用于后续使用
session_data = fetcher.dump_cookies()

# 恢复会话
fetcher2 = StealthyFetcher()
fetcher2.load_cookies(session_data)
```

## 重试和错误处理

```python
fetcher = StealthyFetcher()

# 设置重试
page = fetcher.fetch('https://example.com', retries=3, retry_delay=2)

# 设置超时
page = fetcher.fetch('https://example.com', timeout=60)

# 自定义错误处理
def handle_error(error):
    print(f"请求失败: {error}")
    return True  # 返回 True 表示已处理，不抛出异常

fetcher = StealthyFetcher(error_handler=handle_error)
```

## 选择器集成

StealthyFetcher 返回的对象与 ParselResponse 完全兼容，支持所有选择器功能。

```python
fetcher = StealthyFetcher()

page = fetcher.fetch('https://example.com')

# CSS 选择器
titles = page.css('h1::text').getall()
products = page.css('.product')

# XPath 选择器
links = page.xpath('//a/@href').getall()

# 正则表达式
emails = page.re(r'[\w\.-]+@[\w\.-]+\.\w+')
```

## 场景示例

### 场景1：绕过基础反爬虫

```python
from scrapling.fetchers import StealthyFetcher

fetcher = StealthyFetcher()

# 使用真实浏览器指纹
page = fetcher.fetch('https://anti-crawler-site.com')

if page.status == 200:
    print("成功获取页面")
    print(page.css('title::text').get())
else:
    print(f"请求失败: {page.status}")
```

### 场景2：处理 Cloudflare 保护

```python
from scrapling.fetchers import StealthyFetcher

fetcher = StealthyFetcher()

# 访问 Cloudflare 保护的网站
page = fetcher.fetch('https://cloudflare-protected-site.com', cloudflare=True, cloudflare_timeout=120)

if page.status == 200:
    content = page.css('.protected-content').get()
    print(f"获取内容: {content}")
```

### 场景3：代理轮换抓取

```python
from scrapling.fetchers import StealthyFetcher
import time

proxies = [
    'http://proxy1.com:8080',
    'http://proxy2.com:8080',
    'http://proxy3.com:8080',
]

fetcher = StealthyFetcher(proxies=proxies, proxy_rotation='random')

urls = [
    'https://site.com/page1',
    'https://site.com/page2',
    'https://site.com/page3',
]

for url in urls:
    page = fetcher.fetch(url)
    print(f"URL: {url}, 状态: {page.status}")
    time.sleep(1)  # 请求间隔
```

### 场景4：登录后抓取

```python
from scrapling.fetchers import StealthyFetcher

fetcher = StealthyFetcher()

# 登录
login_page = fetcher.fetch('https://example.com/login', method='POST', data={
    'username': 'your_username',
    'password': 'your_password'
})

# 访问需要登录的页面
dashboard = fetcher.fetch('https://example.com/dashboard')

# 提取数据
user_info = dashboard.css('.user-name::text').get()
print(f"用户名: {user_info}")
```

### 场景5：大规模抓取

```python
from scrapling.fetchers import StealthyFetcher
import random

proxies = [...]  # 代理列表

def fetch_with_retry(url, max_retries=3):
    fetcher = StealthyFetcher(proxies=proxies, proxy_rotation='random')
    
    for attempt in range(max_retries):
        try:
            # 随机延迟
            time.sleep(random.uniform(1, 3))
            
            page = fetcher.fetch(url, timeout=30)
            if page.status == 200:
                return page
        except Exception as e:
            print(f"重试 {attempt + 1}: {e}")
    
    return None

# 批量抓取
for url in urls:
    page = fetch_with_retry(url)
    if page:
        data = page.css('.data::text').getall()
        # 处理数据
```

## 性能优化

### 减少指纹特征

```python
# 减少等待时间
fetcher = StealthyFetcher(wait_for=1000)

# 禁用不必要的等待
page = fetcher.fetch('https://example.com', wait_for_idle=False)
```

### 连接复用

```python
# 复用会话
fetcher = StealthyFetcher()

# 保持连接
for url in urls:
    page = fetcher.fetch(url)  # 使用同一个连接池
```

## 注意事项

1. **合理设置请求间隔**：避免过快请求被检测
2. **使用代理**：大规模抓取时使用代理轮换
3. **处理 JavaScript**：某些网站仍需要 DynamicFetcher
4. **更新指纹库**：定期更新以应对反爬虫升级
5. **遵守网站规则**：遵守 robots.txt 和网站使用条款

## 相关链接

- [Fetcher 基础 HTTP 请求](./fetcher.md)
- [DynamicFetcher 动态网站抓取](./dynamic-fetcher.md)
- [官方文档](https://scrapling.readthedocs.io/en/latest/fetchers.html)
