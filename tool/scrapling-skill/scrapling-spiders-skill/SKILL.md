---
name: scrapling-spiders-skill
description: Scrapling Spider 爬虫框架技能
version: 1.0.0
---

# Scrapling Spider 爬虫框架技能

## 技能概述

Scrapling Spider 是 Scrapling 框架中的爬虫组件，提供了一个完整且可扩展的爬取解决方案。它基于核心解析引擎，添加了请求调度、响应处理、并发控制、暂停/恢复等企业级功能。

Scrapling Spider 设计理念是简化爬虫开发流程，同时保持足够的灵活性以满足复杂的爬取需求。

## 核心特性

- **简洁的 API**：定义爬虫只需继承 Spider 类并实现回调方法
- **自动请求调度**：支持 start_urls 自动发起请求
- **灵活的响应处理**：支持多种回调方式处理不同类型的响应
- **内置并发控制**：支持配置并发请求数、延迟等参数
- **暂停/恢复功能**：支持保存爬取状态并在之后恢复
- **流式输出**：支持流式处理数据，便于实时处理大规模数据
- **自动代理轮换**：内置代理池管理，支持自动切换代理
- **反爬虫绕过**：集成 Fetcher 的反机器人绕过功能

## 快速开始

### 安装

```bash
pip install scrapling
```

### 第一个 Spider 示例

```python
from scrapling.spiders import Spider, Response

class ProductSpider(Spider):
    name = "products"
    start_urls = ["https://example.com/products"]

    def parse(self, response: Response):
        # 提取商品列表
        for product in response.css('.product-item'):
            yield {
                'title': product.css('h3::text').get(),
                'price': product.css('.price::text').get(),
                'link': response.urljoin(product.css('a::attr(href)').get())
            }

        # 处理分页
        next_page = response.css('.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

# 运行爬虫
if __name__ == "__main__":
    ProductSpider().start()
```

---

## 第一部分：Spider 基础

### 1.1 定义 Spider

Spider 是 Scrapling 爬虫框架的核心类，继承它即可创建自定义爬虫。

```python
from scrapling.spiders import Spider, Response

class MySpider(Spider):
    name = "my_spider"           # 爬虫名称，唯一标识
    start_urls = []              # 起始 URL 列表
    custom_settings = {}         # 自定义配置

    def parse(self, response: Response):
        # 处理响应的逻辑
        pass
```

### 1.2 必填属性

| 属性 | 说明 | 必填 |
|------|------|------|
| `name` | 爬虫唯一标识名称 | 是 |
| `start_urls` | 起始 URL 列表 | 是（除非使用 start_requests） |

### 1.3 可选属性

```python
class AdvancedSpider(Spider):
    # 允许的域名列表，限制爬取范围
    allowed_domains = ["example.com"]

    # 用户自定义设置
    custom_settings = {
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0.5,
    }

    # 初始请求自定义
    def start_requests(self):
        for url in self.start_urls:
            yield self.request(url, callback=self.parse)
```

---

## 第二部分：回调方法

### 2.1 parse 回调

`parse` 是默认的回调方法，处理 start_urls 返回的响应。

```python
class BlogSpider(Spider):
    name = "blog"
    start_urls = ["https://example.com/blog"]

    def parse(self, response: Response):
        # 提取文章标题
        for article in response.css('.article'):
            yield {
                'title': article.css('h2::text').get(),
                'summary': article.css('.summary::text').get(),
                'date': article.css('.date::text').get()
            }
```

### 2.2 自定义回调

可以为不同的请求指定不同的回调方法。

```python
class MultiSpider(Spider):
    name = "multi"
    start_urls = ["https://example.com/"]

    def parse(self, response: Response):
        # 列表页处理
        for item in response.css('.item'):
            yield {
                'name': item.css('h3::text').get(),
                'link': response.urljoin(item.css('a::attr(href)').get())
            }

        # 跟进详情页
        for link in response.css('.item a::attr(href)').getall():
            yield response.follow(link, callback=self.parse_detail)

    def parse_detail(self, response: Response):
        # 详情页处理
        yield {
            'title': response.css('h1::text').get(),
            'content': response.css('.content::text').get(),
            'url': response.url
        }
```

### 2.3 使用 follow 方法

`response.follow()` 是 `scrapy` 风格的快捷方法，用于创建新的请求。

```python
def parse(self, response: Response):
    # 使用 CSS 选择器创建请求
    yield response.follow('.pagination a.next', callback=self.parse)

    # 使用元素创建请求（自动获取 href）
    for link in response.css('.article a'):
        yield response.follow(link, callback=self.parse_article)

    # 使用 URL 字符串创建请求
    yield response.follow('/page/2', callback=self.parse)
```

---

## 第三部分：请求方法

### 3.1 request 方法

创建自定义请求对象。

```python
from scrapling.spiders import Spider, Response, Request

class CustomRequestSpider(Spider):
    name = "custom_request"
    start_urls = ["https://example.com/"]

    def parse(self, response: Response):
        # 创建 GET 请求
        yield self.request(
            url='https://example.com/api/data',
            callback=self.parse_api,
            method='GET',
            headers={'Accept': 'application/json'}
        )

        # 创建 POST 请求
        yield self.request(
            url='https://example.com/search',
            callback=self.parse_search,
            method='POST',
            data={'keyword': 'python', 'page': 1}
        )

    def parse_api(self, response: Response):
        print(response.json())
```

### 3.2 FormRequest 表单请求

处理表单提交，包括登录等场景。

```python
class LoginSpider(Spider):
    name = "login"
    start_urls = ["https://example.com/login"]

    def parse(self, response: Response):
        # 从表单提取 CSRF token
        csrf_token = response.css('input[name="csrf_token"]::attr(value)').get()

        # 提交表单
        yield self.form_request(
            url='https://example.com/do_login',
            formdata={
                'username': 'your_username',
                'password': 'your_password',
                'csrf_token': csrf_token
            },
            callback=self.parse_logged_in
        )

    def parse_logged_in(self, response: Response):
        # 登录成功后提取数据
        yield {'status': 'logged_in'}
```

---

## 第四部分：并发控制

### 4.1 配置并发请求

通过自定义设置控制并发。

```python
class ConcurrentSpider(Spider):
    name = "concurrent"
    start_urls = [f"https://example.com/page/{i}" for i in range(100)]

    custom_settings = {
        'CONCURRENT_REQUESTS': 16,      # 最大并发请求数
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,  # 每个域名最大并发
        'DOWNLOAD_DELAY': 0.25,         # 请求之间的时间延迟
    }

    def parse(self, response: Response):
        yield {'url': response.url}
```

### 4.2 域名单限流

```python
class DomainLimitedSpider(Spider):
    name = "domain_limited"
    start_urls = ["https://site1.com/", "https://site2.com/"]

    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 1.0,
    }
```

---

## 第五部分：暂停和恢复

### 5.1 保存爬取状态

Scrapling 支持暂停和恢复爬取。

```python
class ResumableSpider(Spider):
    name = "resumable"
    start_urls = [f"https://example.com/item/{i}" for i in range(1000)]

    custom_settings = {
        'JOBDIR': 'crawls/resumable-001',  # 保存状态的目录
    }

    def parse(self, response: Response):
        yield {
            'id': response.url.split('/')[-1],
            'title': response.css('h1::text').get()
        }
```

### 5.2 运行和恢复

```bash
# 启动爬虫（会创建状态文件）
scrapling runspider my_spider.py

# 暂停爬虫（Ctrl+C）
# 状态会自动保存到 JOBDIR

# 恢复爬虫
scrapling runspider my_spider.py
```

---

## 第六部分：流式输出

### 6.1 流式处理数据

流式输出允许实时处理数据，无需等待所有请求完成。

```python
import json

class StreamingSpider(Spider):
    name = "streaming"
    start_urls = ["https://example.com/products"]

    def parse(self, response: Response):
        for product in response.css('.product'):
            item = {
                'name': product.css('h3::text').get(),
                'price': product.css('.price::text').get()
            }
            # 流式输出
            self.stream_write(json.dumps(item))

    def stream_close(self):
        # 完成时调用
        print("爬取完成")
```

### 6.2 配置流式输出

```python
class OutputSpider(Spider):
    name = "output"
    start_urls = ["https://example.com/"]

    custom_settings = {
        'STREAM_FILE': 'output.jsonl',  # 输出文件
        'STREAM_MODE': 'json',          # 输出模式：json, jsonl, csv
    }
```

---

## 第七部分：高级配置

### 7.1 请求头和代理

```python
class ProxiedSpider(Spider):
    name = "proxied"
    start_urls = ["https://example.com/"]

    custom_settings = {
        'PROXY_LIST': ['http://proxy1:8080', 'http://proxy2:8080'],
        'PROXY_ROTATION': True,
    }

    def parse(self, response: Response):
        yield {'url': response.url}
```

### 7.2 错误处理

```python
class ErrorHandlingSpider(Spider):
    name = "error_handling"
    start_urls = ["https://example.com/"]

    def parse(self, response: Response):
        if response.status != 200:
            yield self.request(response.url, callback=self.parse, dont_filter=True)
            return

        yield {'data': response.css('.data::text').get()}
```

### 7.3 中间件

```python
class MiddlewareSpider(Spider):
    name = "middleware"
    start_urls = ["https://example.com/"]

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapling.middlewares.UserAgentMiddleware': 400,
        },
        'USER_AGENT': 'MyBot/1.0',
    }
```

---

## 第八部分：最佳实践

### 8.1 项目结构

```
my_scrapling_project/
├── spiders/
│   ├── __init__.py
│   ├── product_spider.py
│   └── blog_spider.py
├── pipelines.py
├── settings.py
└── main.py
```

### 8.2 使用 pipelines

```python
from scrapling.spiders import Spider, Response
from scrapling.pipelines import Pipeline

class MyPipeline(Pipeline):
    def process_item(self, item):
        print(f"处理数据: {item}")
        return item

class PipedSpider(Spider):
    name = "piped"
    start_urls = ["https://example.com/"]

    custom_settings = {
        'ITEM_PIPELINES': {
            'my_module.MyPipeline': 300,
        }
    }

    def parse(self, response: Response):
        yield {'data': 'test'}
```

### 8.3 性能优化

```python
class OptimizedSpider(Spider):
    name = "optimized"
    start_urls = ["https://example.com/"]

    custom_settings = {
        'CONCURRENT_REQUESTS': 32,
        'DOWNLOAD_DELAY': 0,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
        'AUTOTHROTTLE_ENABLED': False,  # 禁用自动限速
    }

    def parse(self, response: Response):
        # 使用 CSS 选择器而非 XPath（通常更快）
        items = response.css('.item::text').getall()
        yield {'items': items}
```

---

## 参考资源

- 官方文档：https://scrapling.readthedocs.io
- Spider 文档：https://scrapling.readthedocs.io/en/latest/spiders.html
- GitHub：https://github.com/pyd4vinci/scrapling

---

## 相关技能

- [scrapling-core-skill](./scrapling-core-skill/SKILL.md) - Scrapling 核心解析引擎技能
