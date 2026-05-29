---
name: scrapling-session-skill
description: Scrapling 会话管理技能
version: 1.0.0
---

# Scrapling 会话管理技能

## 技能概述

Scrapling 提供了强大的会话管理功能，支持 Cookie 持久化、代理轮换和域阻断等高级特性。这些功能使 Scrapling 能够处理需要登录的网站、规避反爬虫检测以及管理大规模爬取任务。

## 核心特性

- **多会话类型支持**：FetcherSession、DynamicSession、StealthySession
- **Cookie 持久化**：跨请求保持登录状态
- **代理轮换**：ProxyRotator 支持循环和自定义策略
- **域阻断**：阻止特定域名的请求
- **异步支持**：完整的异步会话管理

---

## 第一部分：会话基础

### 1.1 为什么要使用会话

在网页抓取中，会话用于维护用户状态，如登录状态、购物车内容等。没有会话管理，每次请求都是独立的，无法保持登录状态。

```python
# 无会话：每次请求都是新的，无法保持登录
from scrapling.fetchers import Fetcher

fetcher = Fetcher()
page1 = fetcher.fetch('https://example.com/login', method='POST', data={'user': 'test', 'pass': '123'})
page2 = fetcher.fetch('https://example.com/dashboard')  # 未登录状态

# 使用会话：保持 Cookie 和状态
from scrapling.fetchers import FetcherSession

with FetcherSession() as session:
    session.fetch('https://example.com/login', method='POST', data={'user': 'test', 'pass': '123'})
    page = session.fetch('https://example.com/dashboard')  # 已登录状态
```

### 1.2 会话类型

Scrapling 提供三种会话类型：

| 会话类型 | 用途 | 特性 |
|---------|------|------|
| FetcherSession | HTTP 请求 | 轻量级，支持 TLS 指纹 |
| DynamicSession | 动态渲染页面 | 使用 Playwright Chromium |
| StealthySession | 反爬虫绕过 | 浏览器指纹欺骗 |

```python
from scrapling.fetchers import FetcherSession, DynamicSession, StealthySession

# HTTP 会话
http_session = FetcherSession()

# 动态页面会话（需要 Playwright）
dynamic_session = DynamicSession()

# 隐身会话（高级反爬虫）
stealthy_session = StealthySession()
```

---

## 第二部分：Cookie 管理

### 2.1 基本 Cookie 使用

```python
from scrapling.fetchers import FetcherSession

with FetcherSession() as session:
    # 登录
    session.fetch('https://example.com/login', method='POST', 
                  data={'username': 'user', 'password': 'pass'})
    
    # 后续请求自动携带 Cookie
    profile = session.fetch('https://example.com/profile')
    print(profile.css('.username::text').get())
```

### 2.2 手动设置 Cookie

```python
session = FetcherSession()

# 设置 Cookie
session.set_cookie('session_id', 'abc123', domain='example.com')
session.set_cookie('user_pref', 'dark_mode', domain='example.com')

# 获取页面
page = session.fetch('https://example.com')
```

### 2.3 Cookie 持久化到文件

```python
import json
from scrapling.fetchers import FetcherSession

# 保存 Cookie
session = FetcherSession()
session.fetch('https://example.com/login', method='POST', data={'user': 'test', 'pass': '123'})

cookies = session.get_cookies()
with open('cookies.json', 'w') as f:
    json.dump(cookies, f)

# 加载 Cookie
session2 = FetcherSession()
with open('cookies.json', 'r') as f:
    cookies = json.load(f)
session2.set_cookies(cookies)

page = session2.fetch('https://example.com/dashboard')
```

### 2.4 在不同会话类型间传递 Cookie

```python
from scrapling.fetchers import FetcherSession, StealthySession

# 在 FetcherSession 登录
with FetcherSession() as http_session:
    http_session.fetch('https://example.com/login', method='POST', data={'user': 'test'})
    cookies = http_session.get_cookies()

# 将 Cookie 转移到 StealthySession
with StealthySession() as stealth_session:
    stealth_session.set_cookies(cookies)
    page = stealth_session.fetch('https://example.com/protected')
```

---

## 第三部分：代理轮换

### 3.1 基础代理设置

```python
from scrapling.fetchers import FetcherSession

# 单个代理
session = FetcherSession(proxy='http://proxy1.example.com:8080')
page = session.fetch('https://example.com')

# 带认证的代理
session = FetcherSession(proxy='http://user:pass@proxy1.example.com:8080')
```

### 3.2 使用 ProxyRotator

```python
from scrapling import ProxyRotator
from scrapling.fetchers import Fetcher, StealthyFetcher

# 创建代理列表
proxies = [
    'http://proxy1.example.com:8080',
    'http://proxy2.example.com:8080',
    'socks5://proxy3.example.com:1080'
]

# 创建轮换器（默认循环模式）
rotator = ProxyRotator(proxies)

# 使用轮换器
session = Fetcher(rotator=rotator)

for i in range(10):
    page = session.fetch(f'https://example.com/page{i}')
    print(f"请求 {i+1} 使用代理: {rotator.current}")
```

### 3.3 自定义轮换策略

```python
from scrapling import ProxyRotator

proxies = [
    'http://proxy1.example.com:8080',
    'http://proxy2.example.com:8080',
    'http://proxy3.example.com:8080'
]

# 随机策略
rotator = ProxyRotator(proxies, strategy='random')

# 自定义策略
def custom_strategy(proxies, last_used):
    """失败后跳过代理的自定义策略"""
    # 实现自定义逻辑
    return next_proxy

rotator = ProxyRotator(proxies, strategy=custom_strategy)
```

### 3.4 会话级别的代理

```python
from scrapling import ProxyRotator
from scrapling.fetchers import FetcherSession

proxies = ['http://proxy1:8080', 'http://proxy2:8080']
rotator = ProxyRotator(proxies)

# 方式1：在创建时指定
session = FetcherSession(rotator=rotator)

# 方式2：动态切换
session.set_rotator(ProxyRotator(['http://new-proxy:8080']))
```

### 3.5 每个请求覆盖代理

```python
session = FetcherSession()

# 使用默认轮换器
page1 = session.fetch('https://example.com/page1')

# 单个请求指定代理
page2 = session.fetch('https://example.com/page2', proxy='http://specific-proxy:8080')
```

---

## 第四部分：域阻断

### 4.1 基础域阻断

```python
from scrapling.fetchers import DynamicFetcher

# 创建Fetcher并设置阻断列表
fetcher = DynamicFetcher(
    block_domains=['google-analytics.com', 'doubleclick.net', 'facebook.com']
)

# 获取页面时，阻断列表中的域名请求会被阻止
page = fetcher.fetch('https://example.com')
```

### 4.2 动态管理阻断列表

```python
fetcher = DynamicFetcher()

# 添加阻断域名
fetcher.block_domain('ads.example.com')
fetcher.block_domain('tracker.example.com')

# 移除阻断
fetcher.unblock_domain('tracker.example.com')

# 获取阻断列表
blocked = fetcher.get_blocked_domains()
print(blocked)
```

### 4.3 使用通配符阻断

```python
fetcher = DynamicFetcher(
    block_domains=['*.google.com', '*.doubleclick.net']
)

# 这会阻断以下域名:
# www.google.com
# maps.google.com
# analytics.google.com
```

### 4.4 在 StealthyFetcher 中使用

```python
from scrapling.fetchers import StealthyFetcher

fetcher = StealthyFetcher(
    block_domains=['google-analytics.com', 'hotjar.com', 'intercom.io'],
    headless=True
)

page = fetcher.fetch('https://example.com')
```

---

## 第五部分：高级用法

### 5.1 多会话管理

```python
from scrapling.fetchers import FetcherSession

# 为不同网站创建不同会话
sessions = {
    'site_a': FetcherSession(),
    'site_b': FetcherSession(),
    'site_c': FetcherSession()
}

# 登录不同网站
sessions['site_a'].fetch('https://site-a.com/login', method='POST', data={'user': 'a'})
sessions['site_b'].fetch('https://site-b.com/login', method='POST', data={'user': 'b'})

# 使用相应会话
page_a = sessions['site_a'].fetch('https://site-a.com/data')
page_b = sessions['site_b'].fetch('https://site-b.com/data')
```

### 5.2 异步会话

```python
import asyncio
from scrapling.fetchers import AsyncFetcherSession

async def main():
    async with AsyncFetcherSession() as session:
        # 登录
        await session.fetch('https://example.com/login', method='POST', 
                           data={'user': 'test', 'pass': '123'})
        
        # 获取数据
        page = await session.fetch('https://example.com/data')
        print(page.css('.data::text').getall())

asyncio.run(main())
```

### 5.3 会话与 Spider 框架集成

```python
from scrapling.spiders import Spider, Response
from scrapling.fetchers import FetcherSession

class MultiSessionSpider(Spider):
    name = "multi_session"
    start_urls = ["https://example.com/"]
    
    def start_requests(self):
        # 创建会话
        session = FetcherSession()
        self.session = session
        
        for url in self.start_urls:
            yield self.fetch(url, session=session)
    
    def parse(self, response: Response):
        # 使用会话继续请求
        next_page = response.css('.next::attr(href)').get()
        if next_page:
            yield self.fetch(response.urljoin(next_page), session=self.session)

# 运行爬虫
MultiSessionSpider().start()
```

### 5.4 会话状态监控

```python
from scrapling.fetchers import FetcherSession

session = FetcherSession()

# 获取会话信息
info = session.get_info()
print(f"会话 ID: {info.get('session_id')}")
print(f"当前代理: {info.get('current_proxy')}")
print(f"Cookie 数量: {len(info.get('cookies', {}))}")

# 监控请求统计
stats = session.get_stats()
print(f"已发送请求: {stats.get('request_count')}")
print(f"失败请求: {stats.get('failed_count')}")
```

---

## 第六部分：最佳实践

### 6.1 常见场景

#### 场景1：电商网站批量抓取

```python
from scrapling import ProxyRotator
from scrapling.fetchers import FetcherSession

# 配置代理轮换
proxies = [
    'http://proxy1:8080',
    'http://proxy2:8080',
    'http://proxy3:8080'
]
rotator = ProxyRotator(proxies)

# 创建会话
with FetcherSession(rotator=rotator) as session:
    # 登录
    session.fetch('https://shop.example.com/login', 
                  method='POST', 
                  data={'email': 'user@example.com', 'password': 'pass123'})
    
    # 批量获取商品
    for page_num in range(1, 101):
        page = session.fetch(f'https://shop.example.com/products?page={page_num}')
        products = page.css('.product-item')
        
        for product in products:
            print({
                'name': product.css('.name::text').get(),
                'price': product.css('.price::text').get()
            })
```

#### 场景2：社交媒体账号管理

```python
from scrapling.fetchers import StealthySession
import json

# 使用隐身会话绕过反爬
with StealthySession(headless=True) as session:
    # 登录社交媒体
    session.fetch('https://social.example.com/login', 
                  method='POST',
                  data={'username': 'my_account', 'password': 'secret'})
    
    # 保存会话状态
    cookies = session.get_cookies()
    with open('social_cookies.json', 'w') as f:
        json.dump(cookies, f)
    
    # 获取时间线
    timeline = session.fetch('https://social.example.com/feed')
    posts = timeline.css('.post::text').getall()
    
    for post in posts[:10]:
        print(post)
```

#### 场景3：自动化测试

```python
from scrapling.fetchers import DynamicSession
from scrapling import ProxyRotator

# 创建测试环境
proxies = ['http://test-proxy:8080']
rotator = ProxyRotator(proxies)

with DynamicSession(rotator=rotator) as session:
    # 加载应用
    session.fetch('https://app.example.com')
    
    # 执行测试操作
    session.fetch('https://app.example.com/action1')
    session.fetch('https://app.example.com/action2')
    
    # 验证结果
    result = session.fetch('https://app.example.com/result')
    assert result.css('.status::text').get() == 'success'
```

### 6.2 错误处理

```python
from scrapling.fetchers import FetcherSession
from scrapling.exceptions import ProxyError, SessionError

session = FetcherSession()

try:
    page = session.fetch('https://example.com/data')
except ProxyError as e:
    print(f"代理错误: {e}")
    # 切换到备用代理
    session.set_rotator(ProxyRotator(['http://backup-proxy:8080']))
except SessionError as e:
    print(f"会话错误: {e}")
    # 重新创建会话
    session = FetcherSession()
except Exception as e:
    print(f"其他错误: {e}")
```

### 6.3 性能优化

1. **复用会话**：不要每次请求都创建新会话
2. **合理使用代理**：对不需要代理的请求不使用代理
3. **Cookie 管理**：定期清理过期 Cookie

```python
# 不推荐：每次请求创建新会话
for url in urls:
    session = FetcherSession()  # 性能开销大
    page = session.fetch(url)

# 推荐：复用会话
session = FetcherSession()
for url in urls:
    page = session.fetch(url)  # 高效
```

---

## 参考资源

- 官方文档：https://scrapling.readthedocs.io
- GitHub：https://github.com/pyd4vinci/scrapling
- 会话管理文档：[session-management.md](./references/session-management.md)
- 代理轮换文档：[proxy-rotation.md](./references/proxy-rotation.md)
- 域阻断文档：[domain-blocking.md](./references/domain-blocking.md)
