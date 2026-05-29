# Scrapling 代理轮换

## 简介

代理轮换是网页抓取中规避 IP 封禁的重要技术。Scrapling 提供了 `ProxyRotator` 类，支持多种轮换策略，适用于大规模数据抓取场景。

## 基础概念

### 为什么要使用代理轮换

- **避免 IP 封禁**：单一 IP 频繁请求容易被目标网站封禁
- **分布式抓取**：使用多个代理并行抓取提高效率
- **地域伪装**：模拟不同地区的访问
- **反检测**：使请求看起来来自不同用户

### Scrapling 代理支持

Scrapling 支持多种代理协议：

| 协议 | 说明 | 示例 |
|------|------|------|
| HTTP | HTTP 代理 | `http://proxy.example.com:8080` |
| HTTPS | HTTPS 代理 | `https://proxy.example.com:8080` |
| SOCKS4 | SOCKS4 代理 | `socks4://proxy.example.com:1080` |
| SOCKS5 | SOCKS5 代理 | `socks5://proxy.example.com:1080` |

## ProxyRotator

### 创建基础轮换器

```python
from scrapling import ProxyRotator
from scrapling.fetchers import Fetcher

# 定义代理列表
proxies = [
    'http://proxy1.example.com:8080',
    'http://proxy2.example.com:8080',
    'http://proxy3.example.com:8080',
]

# 创建轮换器（默认循环策略）
rotator = ProxyRotator(proxies)

# 使用轮换器
fetcher = Fetcher(rotator=rotator)

for i in range(10):
    page = fetcher.fetch(f'https://example.com/page{i}')
    print(f"请求 {i+1} 使用代理: {rotator.current}")
```

### 轮换策略

#### 1. 循环策略（默认）

```python
from scrapling import ProxyRotator

proxies = [
    'http://proxy1:8080',
    'http://proxy2:8080',
    'http://proxy3:8080'
]

# 默认循环模式
rotator = ProxyRotator(proxies)

# 每次调用自动切换到下一个代理
print(rotator.get())  # proxy1
print(rotator.get())  # proxy2
print(rotator.get())  # proxy3
print(rotator.get())  # proxy1 (循环)
```

#### 2. 随机策略

```python
rotator = ProxyRotator(proxies, strategy='random')

# 随机选择代理
for i in range(10):
    proxy = rotator.get()
    print(f"随机选择: {proxy}")
```

#### 3. 自定义策略

```python
from scrapling import ProxyRotator

proxies = [
    'http://proxy1:8080',
    'http://proxy2:8080',
    'http://proxy3:8080'
]

def custom_strategy(proxies, last_used):
    """自定义策略：跳过失败的代理"""
    # 实现自定义逻辑
    index = proxies.index(last_used) if last_used in proxies else -1
    next_index = (index + 1) % len(proxies)
    return proxies[next_index]

rotator = ProxyRotator(proxies, strategy=custom_strategy)
```

### 失败重试策略

```python
from scrapling import ProxyRotator

proxies = ['http://proxy1:8080', 'http://proxy2:8080']

# 创建支持失败重试的轮换器
rotator = ProxyRotator(
    proxies,
    retry_failed=True,  # 失败后自动重试
    max_retries=3      # 最大重试次数
)

# 失败的代理会自动重试
for i in range(100):
    try:
        page = fetcher.fetch(f'https://example.com/page{i}')
    except Exception as e:
        print(f"请求失败: {e}")
        # 轮换器会自动处理失败
```

## 在不同会话中使用代理

### FetcherSession

```python
from scrapling import ProxyRotator
from scrapling.fetchers import FetcherSession

proxies = ['http://proxy1:8080', 'http://proxy2:8080']
rotator = ProxyRotator(proxies)

# 在会话中使用轮换器
with FetcherSession(rotator=rotator) as session:
    for i in range(10):
        page = session.fetch(f'https://example.com/page{i}')
        print(f"使用代理: {rotator.current}")
```

### DynamicSession

```python
from scrapling import ProxyRotator
from scrapling.fetchers import DynamicSession

proxies = ['http://proxy1:8080', 'http://proxy2:8080']
rotator = ProxyRotator(proxies)

with DynamicSession(rotator=rotator, headless=True) as session:
    page = session.fetch('https://example.com')
    print(f"使用代理: {rotator.current}")
```

### StealthySession

```python
from scrapling import ProxyRotator
from scrapling.fetchers import StealthySession

proxies = ['http://proxy1:8080', 'http://proxy2:8080']
rotator = ProxyRotator(proxies)

with StealthySession(rotator=rotator, headless=True) as session:
    page = session.fetch('https://example.com')
    print(f"使用代理: {rotator.current}")
```

## 动态代理管理

### 运行时添加/移除代理

```python
rotator = ProxyRotator(['http://proxy1:8080'])

# 运行时添加代理
rotator.add('http://proxy2:8080')
rotator.add('http://proxy3:8080')

# 运行时移除代理
rotator.remove('http://proxy1:8080')

# 查看当前代理列表
print(rotator.proxies)
```

### 代理状态跟踪

```python
rotator = ProxyRotator(proxies)

# 获取当前代理
print(f"当前代理: {rotator.current}")

# 获取代理使用统计
stats = rotator.get_stats()
print(f"使用统计: {stats}")
# {'proxy1': 10, 'proxy2': 5, 'proxy3': 3}

# 获取失败次数
failures = rotator.get_failures()
print(f"失败统计: {failures}")
```

### 代理健康检查

```python
from scrapling import ProxyRotator
import asyncio

async def check_proxy(proxy):
    """检查代理是否可用"""
    try:
        from scrapling.fetchers import Fetcher
        fetcher = Fetcher(proxy=proxy, timeout=5)
        page = fetcher.fetch('https://httpbin.org/ip')
        return True
    except:
        return False

async def main():
    proxies = ['http://proxy1:8080', 'http://proxy2:8080']
    rotator = ProxyRotator(proxies)
    
    # 过滤可用代理
    available = []
    for proxy in proxies:
        if await check_proxy(proxy):
            available.append(proxy)
    
    # 只使用健康的代理
    rotator.proxies = available
    
    print(f"可用代理: {rotator.proxies}")

asyncio.run(main())
```

## 带认证的代理

### 基本认证

```python
# 格式: protocol://username:password@host:port
proxies = [
    'http://user1:pass1@proxy1.example.com:8080',
    'http://user2:pass2@proxy2.example.com:8080',
]

rotator = ProxyRotator(proxies)
```

### 动态设置认证

```python
from scrapling import ProxyRotator

# 创建不带认证的轮换器
rotator = ProxyRotator(['http://proxy1:8080', 'http://proxy2:8080'])

# 为特定请求设置认证
session = Fetcher(proxy=rotator.get())
session.proxies.auth = {'user': 'username', 'pass': 'password'}
```

## 每个请求单独指定代理

### 覆盖默认轮换器

```python
from scrapling import ProxyRotator
from scrapling.fetchers import FetcherSession

proxies = ['http://proxy1:8080', 'http://proxy2:8080']
rotator = ProxyRotator(proxies)

session = FetcherSession(rotator=rotator)

# 使用默认轮换器
page1 = session.fetch('https://example.com/page1')

# 单个请求指定特定代理
page2 = session.fetch('https://example.com/page2', 
                     proxy='http://specific-proxy:8080')

# 也可以传递 None 跳过代理
page3 = session.fetch('https://example.com/page3', proxy=None)
```

### 动态切换轮换器

```python
session = FetcherSession()

# 初始轮换器
rotator1 = ProxyRotator(['http://proxy1:8080'])
session.set_rotator(rotator1)

# 根据条件切换
if some_condition:
    rotator2 = ProxyRotator(['http://proxy2:8080'])
    session.set_rotator(rotator2)
```

## 与 Spider 框架集成

```python
from scrapling.spiders import Spider, Response
from scrapling import ProxyRotator
from scrapling.fetchers import Fetcher

class ProxySpider(Spider):
    name = "proxy_spider"
    start_urls = [f"https://example.com/page{i}" for i in range(100)]
    
    def __init__(self):
        super().__init__()
        self.proxies = self.load_proxies()
        self.rotator = ProxyRotator(self.proxies)
    
    def load_proxies(self):
        """从文件加载代理列表"""
        with open('proxies.txt') as f:
            return [line.strip() for line in f if line.strip()]
    
    async def start_requests(self):
        # 创建 Fetcher 并配置轮换器
        fetcher = Fetcher(rotator=self.rotator)
        
        for url in self.start_urls:
            yield self.fetch(url, session=fetcher)
    
    def parse(self, response: Response):
        # 处理响应
        yield {
            'url': response.url,
            'proxy': self.rotator.current,
            'title': response.css('title::text').get()
        }

ProxySpider().start()
```

## 高级用法

### 代理池管理

```python
from scrapling import ProxyRotator
import random

class ProxyPool:
    """高级代理池管理"""
    
    def __init__(self):
        self.rotator = None
        self.failed_proxies = set()
        self.init_pool()
    
    def init_pool(self):
        # 初始化多个代理组
        self.proxy_groups = {
            'residential': [
                'http://residential1:8080',
                'http://residential2:8080',
            ],
            'datacenter': [
                'http://dc1:8080',
                'http://dc2:8080',
            ],
            'mobile': [
                'http://mobile1:8080',
            ]
        }
        self.set_group('residential')
    
    def set_group(self, group_name):
        """切换代理组"""
        proxies = self.proxy_groups.get(group_name, [])
        # 过滤失败的代理
        available = [p for p in proxies if p not in self.failed_proxies]
        self.rotator = ProxyRotator(available)
    
    def mark_failed(self, proxy):
        """标记失败的代理"""
        self.failed_proxies.add(proxy)
        print(f"代理 {proxy} 标记为失败")
    
    def get_proxy(self):
        """获取当前代理"""
        return self.rotator.get() if self.rotator else None

# 使用代理池
pool = ProxyPool()
session = Fetcher()

for url in urls:
    proxy = pool.get_proxy()
    try:
        page = session.fetch(url, proxy=proxy)
        # 处理成功
    except:
        pool.mark_failed(proxy)
        pool.set_group('datacenter')  # 切换到备用组
```

### 代理地理位置管理

```python
from scrapling import ProxyRotator

# 按地理位置分类代理
geo_proxies = {
    'us': [
        'http://us-proxy1:8080',
        'http://us-proxy2:8080',
    ],
    'eu': [
        'http://eu-proxy1:8080',
    ],
    'asia': [
        'http://asia-proxy1:8080',
        'http://asia-proxy2:8080',
    ]
}

def get_rotator_for_geo(country):
    proxies = geo_proxies.get(country, [])
    return ProxyRotator(proxies)

# 使用特定地区的代理
us_rotator = get_rotator_for_geo('us')
session = Fetcher(rotator=us_rotator)
```

## 最佳实践

### 1. 代理质量检查

```python
# 使用前检查代理
async def verify_proxies(proxies):
    valid = []
    for proxy in proxies:
        try:
            fetcher = Fetcher(proxy=proxy, timeout=10)
            page = fetcher.fetch('https://httpbin.org/ip')
            if page.status == 200:
                valid.append(proxy)
        except:
            pass
    return valid

# 过滤有效代理
valid_proxies = await verify_proxies(all_proxies)
rotator = ProxyRotator(valid_proxies)
```

### 2. 合理设置超时

```python
session = Fetcher(
    rotator=rotator,
    timeout=30,  # 合理超时
    connect_timeout=10  # 连接超时
)
```

### 3. 失败处理

```python
from scrapling import ProxyRotator
from scrapling.exceptions import ProxyError

rotator = ProxyRotator(proxies)

for i in range(100):
    try:
        page = session.fetch(url)
    except ProxyError as e:
        print(f"代理错误: {e}")
        # 跳过当前代理
        rotator.next()
    except Exception as e:
        print(f"其他错误: {e}")
```

### 4. 轮换频率控制

```python
import time

class RateLimitedRotator(ProxyRotator):
    """带频率限制的轮换器"""
    
    def __init__(self, proxies, min_interval=1):
        super().__init__(proxies)
        self.min_interval = min_interval
        self.last_request_time = {}
    
    def get(self, domain=None):
        if domain:
            last = self.last_request_time.get(domain, 0)
            elapsed = time.time() - last
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
            self.last_request_time[domain] = time.time()
        return super().get()
```

## 常见问题

### Q1: 代理不生效？

确保正确传递轮换器：

```python
# 正确
rotator = ProxyRotator(proxies)
session = FetcherSession(rotator=rotator)

# 错误：rotator 没有被正确传递
session = FetcherSession()
session.set_rotator(rotator)  # 需要这样设置
```

### Q2: 代理认证失败？

检查代理 URL 格式：

```python
# 正确格式
'http://username:password@proxy.example.com:8080'

# 错误格式
'http://proxy.example.com:8080'  # 缺少认证信息
```

### Q3: 如何获取免费代理？

```python
# 可以使用公开的代理列表（注意质量参差不齐）
proxies = [
    'http://ip:port',  # 需要自己验证可用性
]
# 建议使用付费代理服务以保证稳定性
```

## 相关链接

- [会话管理](./session-management.md)
- [域阻断](./domain-blocking.md)
