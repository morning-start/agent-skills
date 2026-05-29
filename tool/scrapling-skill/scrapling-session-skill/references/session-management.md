# Scrapling 会话管理基础

## 简介

会话管理是 Scrapling 框架的核心功能之一，它允许在多个请求之间保持状态，如登录信息、Cookie、用户偏好设置等。本文档详细介绍 Scrapling 中的会话管理机制。

## 会话概念

### 什么是会话

会话（Session）是一个在客户端和服务器之间维护状态的机制。在网页抓取中，会话主要用于：

- 保持用户登录状态
- 维护购物车内容
- 存储用户偏好设置
- 跟踪用户行为

### Scrapling 会话架构

Scrapling 提供了统一的会话接口，支持多种会话类型：

```
┌─────────────────────────────────────┐
│          FetcherSession              │
│     (HTTP 请求会话，轻量级)           │
├─────────────────────────────────────┤
│         DynamicSession               │
│   (Playwright Chromium 动态渲染)    │
├─────────────────────────────────────┤
│         StealthySession              │
│    (隐身会话，反爬虫绕过)             │
└─────────────────────────────────────┘
```

## FetcherSession

### 基本用法

```python
from scrapling.fetchers import FetcherSession

# 创建会话（支持上下文管理器）
with FetcherSession() as session:
    # 执行请求
    page = session.fetch('https://example.com')
    print(page.css('h1::text').get())
```

### 会话配置

```python
session = FetcherSession(
    headers={'User-Agent': 'Mozilla/5.0'},  # 自定义请求头
    timeout=30,  # 超时时间
    encoding='utf-8',  # 编码
)
```

### 发送不同类型请求

```python
# GET 请求
page = session.fetch('https://example.com/page')

# POST 请求（表单数据）
page = session.fetch('https://example.com/login', 
                     method='POST',
                     data={'username': 'user', 'password': 'pass'})

# POST 请求（JSON 数据）
page = session.fetch('https://example.com/api',
                     method='POST',
                     json={'key': 'value'})

# 带查询参数
page = session.fetch('https://example.com/search', 
                     params={'q': 'keyword', 'page': 1})
```

## DynamicSession

### 概述

DynamicSession 使用 Playwright 的 Chromium 浏览器来渲染动态内容，适用于需要 JavaScript 执行的网站。

```python
from scrapling.fetchers import DynamicSession

with DynamicSession(headless=True) as session:
    page = session.fetch('https://example.com/dynamic')
    content = page.css('.loaded-content::text').get()
    print(content)
```

### 浏览器配置

```python
session = DynamicSession(
    headless=False,  # 显示浏览器窗口
    slow_mo=100,  # 慢动作模式
    viewport={'width': 1920, 'height': 1080},  # 视口大小
)
```

### 执行 JavaScript

```python
session = DynamicSession()

# 获取页面
page = session.fetch('https://example.com')

# 执行 JavaScript
result = page.evaluate('document.title')

# 点击元素
page.click('.button')

# 填写表单
page.fill('#username', 'myuser')
page.fill('#password', 'mypass')
page.click('button[type="submit"]')
```

## StealthySession

### 概述

StealthySession 是最高级的会话类型，提供浏览器指纹欺骗和反检测功能，能够绕过 Cloudflare 等反爬虫机制。

```python
from scrapling.fetchers import StealthySession

with StealthySession(headless=True) as session:
    page = session.fetch('https://cloudflare-protected.example.com')
    print(page.css('h1::text').get())
```

### 隐身配置

```python
session = StealthySession(
    headless=True,
    stealth=True,  # 启用隐身模式
    fingerprint='random',  # 随机指纹
)
```

### 反 Cloudflare

```python
# 绕过 Cloudflare Turnstile
session = StealthySession(
    headless=True,
    solve_cloudflare=True,  # 自动解决 Cloudflare 挑战
    wait_for_cloudflare=True,  # 等待 Cloudflare 验证完成
)

page = session.fetch('https://cloudflare.example.com')
```

## Cookie 管理

### 自动 Cookie 处理

Scrapling 会话会自动处理 Cookie：

```python
with FetcherSession() as session:
    # 登录（服务器设置 Cookie）
    session.fetch('https://example.com/login', 
                  method='POST',
                  data={'user': 'test', 'pass': '123'})
    
    # 后续请求自动携带 Cookie
    page = session.fetch('https://example.com/dashboard')
    # 此时已登录
```

### 手动 Cookie 操作

```python
session = FetcherSession()

# 设置单个 Cookie
session.set_cookie('name', 'value', domain='example.com')
session.set_cookie('token', 'abc123', path='/', secure=True, httponly=True)

# 获取所有 Cookie
cookies = session.get_cookies()
print(cookies)

# 清除所有 Cookie
session.clear_cookies()

# 清除特定域名的 Cookie
session.clear_cookies(domain='example.com')
```

### Cookie 序列化

```python
import json

# 保存 Cookie 到文件
with FetcherSession() as session:
    session.fetch('https://example.com/login', 
                  method='POST',
                  data={'user': 'test', 'pass': '123'})
    
    cookies = session.get_cookies()
    with open('cookies.json', 'w') as f:
        json.dump(cookies, f)

# 从文件加载 Cookie
session2 = FetcherSession()
with open('cookies.json', 'r') as f:
    cookies = json.load(f)
session2.set_cookies(cookies)

# 使用已登录的会话
page = session2.fetch('https://example.com/profile')
```

### Cookie 属性

```python
# Cookie 属性说明
cookie = {
    'name': 'session_id',        # Cookie 名称
    'value': 'abc123',           # Cookie 值
    'domain': '.example.com',   # 所属域名
    'path': '/',                 # 路径
    'secure': True,              # 仅 HTTPS
    'httponly': True,            # 仅 HTTP
    'expires': 1700000000,       # 过期时间戳
    'samesite': 'Lax'           # SameSite 策略
}
```

## 异步会话

### AsyncFetcherSession

```python
import asyncio
from scrapling.fetchers import AsyncFetcherSession

async def main():
    async with AsyncFetcherSession() as session:
        # GET 请求
        page = await session.fetch('https://example.com')
        
        # POST 请求
        await session.fetch('https://example.com/login',
                           method='POST',
                           data={'user': 'test', 'pass': '123'})
        
        # 获取登录后的页面
        page = await session.fetch('https://example.com/dashboard')
        print(page.css('.username::text').get())

asyncio.run(main())
```

### AsyncDynamicSession

```python
import asyncio
from scrapling.fetchers import AsyncDynamicSession

async def main():
    async with AsyncDynamicSession() as session:
        page = await session.fetch('https://example.com/spa')
        content = await page.evaluate('document.body.innerText')
        print(content)

asyncio.run(main())
```

## 会话状态管理

### 检查会话状态

```python
session = FetcherSession()

# 获取会话信息
info = session.get_info()
print(info)

# 检查是否包含特定 Cookie
has_session = session.has_cookie('session_id')

# 获取 Cookie 数量
cookie_count = len(session.get_cookies())
```

### 会话超时

```python
# 设置空闲超时（秒）
session = FetcherSession(
    idle_timeout=300,  # 5 分钟无活动则超时
)

# 手动保持会话活跃
session.ping()
```

### 错误恢复

```python
from scrapling.exceptions import SessionError, RequestError

session = FetcherSession()

try:
    page = session.fetch('https://example.com/data')
except RequestError as e:
    print(f"请求失败: {e}")
    # 重试
    page = session.fetch('https://example.com/data', retry=3)
except SessionError as e:
    print(f"会话错误: {e}")
    # 重建会话
    session = FetcherSession()
```

## 最佳实践

### 1. 使用上下文管理器

```python
# 推荐
with FetcherSession() as session:
    page = session.fetch('https://example.com')

# 不推荐
session = FetcherSession()
page = session.fetch('https://example.com')
session.close()  # 容易忘记关闭
```

### 2. 复用会话

```python
# 推荐：复用会话
with FetcherSession() as session:
    for url in urls:
        page = session.fetch(url)  # 高效

# 不推荐：频繁创建会话
for url in urls:
    with FetcherSession() as session:
        page = session.fetch(url)  # 效率低
```

### 3. 适当选择会话类型

| 场景 | 推荐会话类型 |
|------|-------------|
| 静态 HTML | FetcherSession |
| JavaScript 渲染 | DynamicSession |
| 反爬虫网站 | StealthySession |

### 4. 错误处理

```python
from scrapling.exceptions import RequestError, ProxyError

with FetcherSession() as session:
    try:
        page = session.fetch('https://example.com')
    except RequestError as e:
        print(f"请求失败: {e}")
    except ProxyError as e:
        print(f"代理错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")
```

## 常见问题

### Q1: 会话 Cookie 不生效？

确保请求的是同一域名：

```python
# 登录
session.fetch('https://example.com/login', ...)

# 访问同一域名
session.fetch('https://example.com/dashboard')  # Cookie 生效

# 访问不同域名
session.fetch('https://other.com/page')  # Cookie 不共享
```

### Q2: 如何处理会话过期？

```python
with FetcherSession() as session:
    # 检查是否需要重新登录
    page = session.fetch('https://example.com/dashboard')
    if page.css('.login-required'):
        # 重新登录
        session.fetch('https://example.com/login', ...)
```

### Q3: DynamicSession 和 StealthySession 的区别？

- **DynamicSession**：使用真实 Chromium 浏览器，适合需要 JavaScript 渲染的页面
- **StealthySession**：在 DynamicSession 基础上增加了反检测功能，适合反爬虫严格的网站

## 下一步

- 学习[代理轮换](./proxy-rotation.md)
- 学习[域阻断](./domain-blocking.md)
