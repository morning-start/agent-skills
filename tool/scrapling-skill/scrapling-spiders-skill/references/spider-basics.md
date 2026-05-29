# Spider 基础

本文档详细介绍 Scrapling Spider 的基础概念，包括类定义、start_urls 配置和 parse 回调方法。

---

## 1. Spider 类定义

### 1.1 最小 Spider

创建一个最基本的 Spider 只需要继承 `Spider` 类并定义 `name` 属性：

```python
from scrapling.spiders import Spider

class MinimalSpider(Spider):
    name = "minimal"
```

但这样的 Spider 没有任何功能，需要配合 `start_urls` 和回调方法才能工作。

### 1.2 完整类定义

```python
from scrapling.spiders import Spider, Response

class MySpider(Spider):
    name = "my_spider"
    allowed_domains = ["example.com"]
    start_urls = [
        "https://example.com/page1",
        "https://example.com/page2"
    ]

    def parse(self, response: Response):
        # 处理响应
        pass
```

### 1.3 类属性说明

| 属性名 | 类型 | 说明 | 必填 |
|--------|------|------|------|
| `name` | str | 爬虫唯一标识名称 | 是 |
| `start_urls` | list | 起始 URL 列表 | 是（除非重写 start_requests） |
| `allowed_domains` | list | 允许爬取的域名列表 | 否 |
| `custom_settings` | dict | 自定义配置项 | 否 |
| `start_urls_for_empty_response` | bool | 当响应为空时是否继续 | 否 |

### 1.4 Spider 初始化

Spider 在实例化时可以传入配置：

```python
from scrapling.spiders import Spider

class ConfiguredSpider(Spider):
    name = "configured"

spider = ConfiguredSpider(
    CONCURRENT_REQUESTS=16,
    DOWNLOAD_DELAY=0.5
)
```

---

## 2. start_urls 配置

### 2.1 基本用法

`start_urls` 是 Spider 启动时自动请求的 URL 列表：

```python
class SimpleSpider(Spider):
    name = "simple"
    start_urls = ["https://example.com/"]
```

Spider 启动后会自动对这些 URL 发起 GET 请求，并使用 `parse` 方法处理响应。

### 2.2 多个 URL

可以添加多个起始 URL：

```python
class MultiUrlSpider(Spider):
    name = "multi_url"
    start_urls = [
        "https://example.com/category/electronics",
        "https://example.com/category/clothing",
        "https://example.com/category/books"
    ]
```

### 2.3 动态生成 URL

可以使用列表推导式动态生成 URL：

```python
class DynamicSpider(Spider):
    name = "dynamic"

    # 生成 100 页 URL
    start_urls = [f"https://example.com/products?page={i}" for i in range(1, 101)]

    # 生成日期范围 URL
    from datetime import datetime, timedelta
    start_urls = [
        f"https://example.com/{date.strftime('%Y-%m-%d')}"
        for date in [
            datetime.now() - timedelta(days=i)
            for i in range(30)
        ]
    ]
```

### 2.4 重写 start_requests

如果需要更灵活的控制，可以重写 `start_requests` 方法：

```python
class CustomStartSpider(Spider):
    name = "custom_start"

    def start_requests(self):
        # 自定义请求逻辑
        urls = [
            ("https://example.com/page1", {"category": "a"}),
            ("https://example.com/page2", {"category": "b"}),
        ]

        for url, meta in urls:
            yield self.request(
                url,
                callback=self.parse,
                meta=meta
            )
```

### 2.5 使用 formdata 生成 POST 请求

```python
class FormStartSpider(Spider):
    name = "form_start"

    def start_requests(self):
        keywords = ["python", "javascript", "java"]

        for keyword in keywords:
            yield self.form_request(
                url="https://example.com/search",
                formdata={"q": keyword},
                callback=self.parse_results
            )
```

---

## 3. parse 回调方法

### 3.1 默认 parse 方法

`parse` 是 Scrapling Spider 的默认回调方法，当没有指定回调时自动使用：

```python
class BlogSpider(Spider):
    name = "blog"
    start_urls = ["https://example.com/blog"]

    def parse(self, response: Response):
        # response 是一个 Response 对象
        # 可以使用 css()、xpath() 等方法

        for article in response.css('.article'):
            yield {
                'title': article.css('h2::text').get(),
                'url': response.urljoin(article.css('a::attr(href)').get())
            }
```

### 3.2 parse 方法的参数

```python
def parse(self, response: Response, **kwargs):
    """
    处理爬取到的响应

    参数:
        response: Response 对象，包含响应内容和解析方法
        **kwargs: 额外的关键字参数

    返回:
        可以返回:
        - dict: 单个数据项
        - Request: 跟进请求
        - Generator: 生成器 yields 多个数据项或请求
    """
```

### 3.3 多种返回类型

#### 返回字典（数据项）

```python
def parse(self, response: Response):
    item = {
        'url': response.url,
        'title': response.css('h1::text').get(),
        'content': response.css('.content::text').get()
    }
    return item
```

#### 使用生成器返回多项

```python
def parse(self, response: Response):
    for product in response.css('.product'):
        yield {
            'name': product.css('.name::text').get(),
            'price': product.css('.price::text').get()
        }
```

#### 跟进请求

```python
def parse(self, response: Response):
    # 提取详情页链接并跟进
    for link in response.css('.item a::attr(href)').getall():
        yield response.follow(link, callback=self.parse_detail)

def parse_detail(self, response: Response):
    yield {
        'title': response.css('h1::text').get(),
        'description': response.css('.description::text').get()
    }
```

### 3.4 处理分页

#### 方式一：CSS 选择器

```python
class PaginationSpider(Spider):
    name = "pagination"
    start_urls = ["https://example.com/products"]

    def parse(self, response: Response):
        for product in response.css('.product'):
            yield {
                'name': product.css('.name::text').get(),
                'price': product.css('.price::text').get()
            }

        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
```

#### 方式二：XPath 选择器

```python
class XPathPaginationSpider(Spider):
    name = "xpath_pagination"

    def parse(self, response: Response):
        items = response.xpath('//div[@class="item"]')
        for item in items:
            yield {
                'title': item.xpath('.//h3/text()').get(),
                'price': item.xpath('.//span[@class="price"]/text()').get()
            }

        next_page = response.xpath('//a[contains(@class, "next")]/@href').get()
        if next_page:
            yield response.follow(next_page)
```

### 3.5 处理 JSON 响应

```python
import json

class JsonSpider(Spider):
    name = "json"

    def parse(self, response: Response):
        # 解析 JSON
        data = response.json()

        for item in data.get('items', []):
            yield {
                'id': item.get('id'),
                'name': item.get('name')
            }

        # 处理分页
        next_page = data.get('pagination', {}).get('next')
        if next_page:
            yield self.request(next_page, callback=self.parse)
```

### 3.6 错误处理

```python
class SafeSpider(Spider):
    name = "safe"

    def parse(self, response: Response):
        try:
            title = response.css('h1::text').get()
            if not title:
                self.logger.warning(f"页面缺少标题: {response.url}")
                return

            yield {'title': title}

        except Exception as e:
            self.logger.error(f"解析错误: {e}, URL: {response.url}")
```

---

## 4. Response 对象

### 4.1 Response 简介

`Response` 对象是 Scrapling 传递给回调函数的数据载体，包含：

- 原始响应内容（HTML、JSON 等）
- URL 信息
- HTTP 状态码
- 响应头
- 解析方法（继承自 ParselResponse）

### 4.2 Response 属性

```python
def parse(self, response: Response):
    # URL 信息
    print(response.url)              # 当前 URL
    print(response.urljoin('/path')) # 相对路径转绝对路径

    # HTTP 信息
    print(response.status)           # 状态码 (200, 404 等)
    print(response.headers)          # 响应头字典

    # 内容
    print(response.text)             # 响应文本
    print(response.body)             # 原始字节

    # 编码
    print(response.encoding)         # 响应编码
```

### 4.3 Response 方法

```python
def parse(self, response: Response):
    # CSS 选择器
    elements = response.css('.item')

    # XPath 选择器
    elements = response.xpath('//div[@class="item"]')

    # 跟进请求（快捷方法）
    yield response.follow('.next')
    yield response.follow(link_element)

    # JSON 解析
    data = response.json()

    # 正则匹配
    matches = response.re(r'\d+')
```

---

## 5. 完整示例

### 5.1 商品爬虫

```python
from scrapling.spiders import Spider, Response

class ProductSpider(Spider):
    name = "products"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com/products"]

    def parse(self, response: Response):
        for product in response.css('.product-item'):
            item = {
                'name': product.css('.product-name::text').get(),
                'price': product.css('.price::text').get(),
                'rating': product.css('.rating::text').get(),
                'link': response.urljoin(
                    product.css('a::attr(href)').get()
                )
            }
            yield item

        next_page = response.css('.pagination a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
```

### 5.2 详情页跟进爬虫

```python
class ArticleSpider(Spider):
    name = "articles"
    start_urls = ["https://example.com/blog"]

    def parse(self, response: Response):
        article_links = response.css('.article-title a::attr(href)').getall()

        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        next_page = response.css('.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page)

    def parse_article(self, response: Response):
        yield {
            'title': response.css('h1.title::text').get(),
            'author': response.css('.author::text').get(),
            'date': response.css('.date::text').get(),
            'content': response.css('.article-content::text').getall(),
            'url': response.url
        }
```

---

## 6. 运行 Spider

### 6.1 使用命令行

```bash
scrapling runspider my_spider.py
```

### 6.2 在代码中运行

```python
if __name__ == "__main__":
    MySpider().start()
```

### 6.3 带参数运行

```bash
scrapling runspider my_spider.py -a category=electronics -a max_pages=50
```

```python
class ParamSpider(Spider):
    name = "param"

    def __init__(self, category=None, max_pages=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = category
        self.max_pages = max_pages
        self.start_urls = [f"https://example.com/{category}"]

    def parse(self, response: Response):
        # 使用参数
        pass
```
