# 并发爬取配置

本文档详细介绍 Scrapling Spider 的并发控制功能，包括并发请求数、下载延迟、域名单限流等配置。

---

## 1. 并发配置概述

Scrapling Spider 提供了丰富的并发控制选项，可以通过 `custom_settings` 进行配置。这些设置帮助你在爬取效率和对目标网站的负载之间取得平衡。

---

## 2. 基础并发配置

### 2.1 CONCURRENT_REQUESTS

设置全局最大并发请求数：

```python
class ConcurrentSpider(Spider):
    name = "concurrent"
    start_urls = [f"https://example.com/page/{i}" for i in range(100)]

    custom_settings = {
        'CONCURRENT_REQUESTS': 16
    }

    def parse(self, response: Response):
        yield {'url': response.url}
```

**推荐值：**
- 目标网站负载能力好：16-32
- 普通网站：8-16
- 敏感网站：1-4

### 2.2 DOWNLOAD_DELAY

设置请求之间的延迟（秒）：

```python
class DelayedSpider(Spider):
    name = "delayed"
    start_urls = [f"https://example.com/item/{i}" for i in range(50)]

    custom_settings = {
        'CONCURRENT_REQUESTS': 4,
        'DOWNLOAD_DELAY': 1.0  # 每个请求之间等待 1 秒
    }
```

**推荐值：**
- 小型网站：0.5-1 秒
- 中型网站：1-2 秒
- 大型网站：2-5 秒

### 2.3 组合配置

```python
class BalancedSpider(Spider):
    name = "balanced"

    custom_settings = {
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0.5,
    }
```

---

## 3. 域名单限流

### 3.1 CONCURRENT_REQUESTS_PER_DOMAIN

限制单个域名的并发请求数：

```python
class DomainLimitedSpider(Spider):
    name = "domain_limited"
    start_urls = [
        "https://site1.com/page/1",
        "https://site2.com/page/1",
    ]

    custom_settings = {
        'CONCURRENT_REQUESTS': 16,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,  # 每个域名最多 2 个并发
        'DOWNLOAD_DELAY': 1.0,
    }
```

### 3.2 CONCURRENT_REQUESTS_PER_IP

限制单个 IP 的并发请求数（当使用代理时有用）：

```python
class IPLimitedSpider(Spider):
    name = "ip_limited"

    custom_settings = {
        'CONCURRENT_REQUESTS': 32,
        'CONCURRENT_REQUESTS_PER_IP': 4,  # 每个 IP 最多 4 个并发
    }
```

### 3.3 多个域名配置

```python
class MultiDomainSpider(Spider):
    name = "multi_domain"

    # 不同域名使用不同的并发配置
    domain_settings = {
        'site1.com': {
            'concurrency': 4,
            'delay': 2.0
        },
        'site2.com': {
            'concurrency': 8,
            'delay': 1.0
        }
    }
```

---

## 4. 自动限速（AutoThrottle）

### 4.1 启用自动限速

AutoThrottle 会根据服务器的响应时间自动调整爬取速度：

```python
class AutoThrottleSpider(Spider):
    name = "autothrottle"

    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 0.5,   # 初始延迟（秒）
        'AUTOTHROTTLE_MAX_DELAY': 10,     # 最大延迟（秒）
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 8.0,  # 目标并发数
    }
```

### 4.2 AutoThrottle 配置说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `AUTOTHROTTLE_ENABLED` | 是否启用自动限速 | False |
| `AUTOTHROTTLE_START_DELAY` | 初始下载延迟 | 0.5 |
| `AUTOTHROTTLE_MAX_DELAY` | 最大延迟 | 60 |
| `AUTOTHROTTLE_MIN_DELAY` | 最小延迟 | 0 |
| `AUTOTHROTTLE_TARGET_CONCURRENCY` | 目标并发数 | 1.0 |
| `AUTOTHROTTLE_DEBUG` | 调试模式 | False |

### 4.3 自动限速示例

```python
class SmartThrottleSpider(Spider):
    name = "smart_throttle"

    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 30,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 4.0,
    }
```

---

## 5. 代理配置

### 5.1 简单代理配置

```python
class ProxiedSpider(Spider):
    name = "proxied"

    custom_settings = {
        'PROXY': 'http://proxy.example.com:8080'
    }
```

### 5.2 代理列表轮换

```python
class ProxyPoolSpider(Spider):
    name = "proxy_pool"

    custom_settings = {
        'PROXY_LIST': [
            'http://proxy1.example.com:8080',
            'http://proxy2.example.com:8080',
            'http://proxy3.example.com:8080',
        ],
        'PROXY_ROTATION': True,  # 启用轮换
    }
```

### 5.3 代理认证

```python
class AuthProxySpider(Spider):
    name = "auth_proxy"

    custom_settings = {
        'PROXY': 'http://user:password@proxy.example.com:8080'
    }
```

### 5.4 按域名使用代理

```python
class DomainProxySpider(Spider):
    name = "domain_proxy"

    proxy_by_domain = {
        'site1.com': 'http://proxy1:8080',
        'site2.com': 'http://proxy2:8080',
    }
```

---

## 6. 请求头配置

### 6.1 自定义 User-Agent

```python
class CustomUASpider(Spider):
    name = "custom_ua"

    custom_settings = {
        'USER_AGENT': 'MyBot/1.0 (+https://example.com/bot)',
    }
```

### 6.2 完整请求头

```python
class HeadersSpider(Spider):
    name = "headers"

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://example.com/',
        }
    }
```

---

## 7. 内存和性能优化

### 7.1 内存限制

```python
class MemoryOptimizedSpider(Spider):
    name = "memory_opt"

    custom_settings = {
        'CONCURRENT_REQUESTS': 8,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 4,
        'DOWNLOAD_DELAY': 0.5,
        'MEMUSAGE_ENABLED': True,      # 启用内存限制
        'MEMUSAGE_LIMIT_MB': 512,      # 限制 512MB
    }
```

### 7.2 DNS 缓存

```python
class DNSCacheSpider(Spider):
    name = "dns_cache"

    custom_settings = {
        'DNSCACHE_ENABLED': True,
        'DNSCACHE_SIZE': 10000,
    }
```

### 7.3 连接池配置

```python
class ConnectionPoolSpider(Spider):
    name = "conn_pool"

    custom_settings = {
        'CONCURRENT_REQUESTS': 32,
        'DOWNLOADER_CLIENTCONTEXTFABRIC_DEFAULT_CLOSING': True,
        'DOWNLOADER_CLIENTCONTEXTFABRIC_MAX': 10,
    }
```

---

## 8. 错误处理和重试

### 8.1 重试配置

```python
class RetrySpider(Spider):
    name = "retry"

    custom_settings = {
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 3,           # 最大重试次数
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 408, 429],  # 重试的状态码
        'RETRY_DELAY': 1.0,          # 重试延迟（秒）
    }
```

### 8.2 自定义重试回调

```python
class CustomRetrySpider(Spider):
    name = "custom_retry"

    def parse(self, response: Response):
        if response.status == 429:
            retry_after = response.headers.get('Retry-After', 5)
            yield self.request(
                response.url,
                callback=self.parse,
                dont_filter=True,
                meta={'priority': -1}
            )
        else:
            yield {'data': 'parsed'}
```

---

## 9. 限流最佳实践

### 9.1 礼貌爬取

```python
class PoliteSpider(Spider):
    name = "polite"

    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'DOWNLOAD_DELAY': 2.0,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
        'ROBOTSTXT_OBEY': True,
    }
```

### 9.2 快速爬取

```python
class FastSpider(Spider):
    name = "fast"

    custom_settings = {
        'CONCURRENT_REQUESTS': 32,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
        'DOWNLOAD_DELAY': 0,
        'AUTOTHROTTLE_ENABLED': False,
        'TELNETCONSOLE_ENABLED': False,
    }
```

### 9.3 平衡模式

```python
class BalancedSpider(Spider):
    name = "balanced"

    custom_settings = {
        'CONCURRENT_REQUESTS': 16,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 4,
        'DOWNLOAD_DELAY': 0.5,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 4.0,
        'AUTOTHROTTLE_START_DELAY': 0.5,
    }
```

---

## 10. 实战示例

### 10.1 电商网站爬虫

```python
class EcommerceSpider(Spider):
    name = "ecommerce"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com/products"]

    custom_settings = {
        'CONCURRENT_REQUESTS': 8,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 1.5,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 2.0,
        'RETRY_TIMES': 3,
    }

    def parse(self, response: Response):
        for product in response.css('.product'):
            yield {
                'name': product.css('.name::text').get(),
                'price': product.css('.price::text').get()
            }

        next_page = response.css('.pagination a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
```

### 10.2 API 数据爬虫

```python
class APISpider(Spider):
    name = "api"

    custom_settings = {
        'CONCURRENT_REQUESTS': 32,
        'DOWNLOAD_DELAY': 0.1,
        'AUTOTHROTTLE_ENABLED': False,
    }

    def parse(self, response: Response):
        data = response.json()
        for item in data.get('results', []):
            yield item
```

### 10.3 多域名爬虫

```python
class MultiSiteSpider(Spider):
    name = "multi_site"

    custom_settings = {
        'CONCURRENT_REQUESTS': 16,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 1.0,
    }

    def start_requests(self):
        sites = [
            'https://site1.com/',
            'https://site2.com/',
            'https://site3.com/',
        ]
        for url in sites:
            yield self.request(url, callback=self.parse)
```
