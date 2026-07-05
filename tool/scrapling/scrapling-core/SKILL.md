---
name: scrapling-core
description: Scrapling 核心解析引擎技能
version: 1.0.0
---

# Scrapling 核心解析引擎技能

## 技能概述

Scrapling 是一个自适应网页抓取框架，可处理从单个请求到完整爬取的所有任务。其解析器能够学习网站变化，在页面更新时自动重新定位元素。其获取器开箱即用可绕过反机器人系统（如 Cloudflare Turnstile）。其蜘蛛框架可扩展到并发、多会话爬取，支持暂停/恢复和自动代理轮换。

Scrapling 核心解析引擎（scrapling.parser）是整个框架的基础，提供了强大的 HTML/XML 解析能力，支持 CSS 选择器、XPath 选择器、智能元素追踪和自适应解析等功能。

## 核心特性

- **多选择器支持**：支持 CSS 选择器、XPath 选择器、基于过滤器的搜索、文本搜索和正则表达式搜索
- **智能元素追踪**：使用智能相似性算法在网站变化后重新定位元素
- **自适应解析**：网站结构变化时自动查找元素
- **丰富的导航 API**：高级 DOM 遍历，支持父级、兄弟级和子级导航方法
- **增强的文本处理**：内置正则表达式、清理方法和优化的字符串操作
- **自动选择器生成**：为任何元素生成健壮的 CSS/XPath 选择器
- **熟悉的 API**：类似于 Scrapy/BeautifulSoup 的语法

## 快速开始

### 安装

```bash
pip install scrapling
```

### 第一个示例

```python
from scrapling import ParselResponse

# 假设你已经有了一些 HTML 内容
html = """
<html>
    <body>
        <div class="product">
            <h2>产品名称</h2>
            <span class="price">99.99</span>
        </div>
        <div class="product">
            <h2>另一个产品</h2>
            <span class="price">149.99</span>
        </div>
    </body>
</html>
"""

# 创建响应对象
response = ParselResponse(html)

# 使用 CSS 选择器提取数据
products = response.css('.product')
for product in products:
    name = product.css('h2::text').get()
    price = product.css('.price::text').get()
    print(f"产品: {name}, 价格: {price}")
```

---

## 第一部分：响应对象

### 1.1 创建响应对象

Scrapling 的核心是 `ParselResponse` 类，它封装了 HTML 内容并提供了解析方法。

```python
from scrapling import ParselResponse

# 从 HTML 字符串创建
response = ParselResponse('<html><body><h1>标题</h1></body></html>')

# 从文件加载
with open('page.html', 'r', encoding='utf-8') as f:
    response = ParselResponse(f.read())

# 从 URL 获取（需要 fetchers）
from scrapling.fetchers import Fetcher
fetcher = Fetcher()
page = fetcher.fetch('https://example.com')
response = page
```

### 1.2 响应对象属性

```python
# 获取原始 HTML
print(response.text)
print(response.html)
print(response.body)

# 获取 URL 信息
print(response.url)
print(response.urljoin('/path'))  # 相对路径转绝对路径

# 获取元信息
print(response.encoding)      # 编码
print(response.headers)       # 响应头
print(response.status)        # 状态码
```

---

## 第二部分：选择器

### 2.1 CSS 选择器

CSS 选择器是最常用的选择器方式。

```python
response = ParselResponse(html)

# 选择单个元素
element = response.css('#main')
element = response.css('.product')
element = response.css('div.content')

# 选择多个元素
elements = response.css('.item')
for item in elements:
    print(item.get())

# 获取元素属性
link = response.css('a::attr(href)').get()
image_src = response.css('img::attr(src)').get()

# 获取元素文本
title = response.css('h1::text').get()

# 使用伪元素
first_item = response.css('.item::first').get()
last_item = response.css('.item::last').get()
nth_item = response.css('.item::nth(2)').get()
```

### 2.2 XPath 选择器

XPath 提供更强大的定位能力。

```python
response = ParselResponse(html)

# 基本 XPath
element = response.xpath('//div[@id="main"]')
elements = response.xpath('//div[@class="product"]')

# 获取文本
title = response.xpath('//h1/text()').get()

# 获取属性
link = response.xpath('//a/@href').get()

# 使用过滤器
elements = response.xpath('//div[contains(@class, "product")]')

# 父元素
parent = response.xpath('//span/parent::*')

# 兄弟元素
siblings = response.xpath('//h2/following-sibling::*')
```

### 2.3 选择器组合使用

```python
response = ParselResponse(html)

# 链式选择器
content = response.css('#content')
title = content.css('h1::text').get()

# 混合使用
elements = response.css('.section')
for section in elements:
    header = section.xpath('./h2/text()').get()
    items = section.css('.item::text').getall()
```

---

## 第三部分：元素操作

### 3.1 元素查找方法

```python
response = ParselResponse(html)

# css() - CSS 选择器
item = response.css('#item')
items = response.css('.items')

# xpath() - XPath 选择器
item = response.xpath('//div[@id="item"]')
items = response.xpath('//div[@class="items"]')

# re() - 正则表达式匹配
items = response.re(r'pattern\d+')

# re_first() - 返回第一个匹配
item = response.re_first(r'pattern\d+')
```

### 3.2 获取元素数据

```python
response = ParselResponse(html)

# get() - 获取单个元素或值
text = response.css('h1::text').get()
element = response.css('.item').get()

# getall() - 获取所有元素或值
texts = response.css('li::text').getall()

# extract() - 提取为列表（兼容 Scrapy）
items = response.css('li::text').extract()

# extract_first() - 提取第一个（兼容 Scrapy）
text = response.css('h1::text').extract_first()

# re() - 正则提取
prices = response.css('.price::text').re(r'\d+\.?\d*')
```

### 3.3 元素属性和文本

```python
element = response.css('.link').get()

# 获取属性
href = element.attrib['href']
href = element.get('href')
all_attrs = element.attrib

# 获取文本
text = element.get()
text = element.text
text = element.text_content()

# 获取内部 HTML
inner_html = element.inner_html()

# 获取 outer HTML
outer_html = element.get()
```

---

## 第四部分：DOM 导航

### 4.1 父子关系

```python
element = response.css('.child').get()

# 父元素
parent = element.xpath('./..').get()
parent = element.parent

# 所有祖先元素
ancestors = element.xpath('./ancestor::*').getall()

# 根元素
root = element.root
```

### 4.2 兄弟关系

```python
element = response.css('.item').get()

# 下一个兄弟元素
next_elem = element.xpath('./following-sibling::*').get()

# 前一个兄弟元素
prev_elem = element.xpath('./preceding-sibling::*').get()

# 所有兄弟元素
siblings = element.xpath('./following-sibling::*').getall()
```

### 4.3 子元素

```python
container = response.css('#container').get()

# 所有子元素
children = container.xpath('./child::*').getall()

# 第一个子元素
first_child = container.xpath('./child::*[1]').get()

# 最后一个子元素
last_child = container.xpath('./child::*[last()]').get()
```

---

## 第五部分：自适应解析

### 5.1 自动保存选择器

Scrapling 的核心优势是能够适应网站结构变化。

```python
response = ParselResponse(html)

# auto_save=True 自动保存智能选择器
products = response.css('.product', auto_save=True)

# 选择器会被保存，下次即使页面结构变化也能找到
# 保存位置: .scrapling_cache.json
```

### 5.2 自适应模式

```python
# 首次抓取
response = ParselResponse(html)
products = response.css('.product', auto_save=True)

# 网站更新后，使用 adaptive=True
# Scrapling 会尝试多种方式找到元素
response2 = ParselResponse(updated_html)
products = response2.css('.product', adaptive=True)
```

### 5.3 智能元素追踪

```python
from scrapling.adaptive import SmartElement

# 创建智能元素
element = SmartElement(original_html, selector='.product h2')

# 在新页面中查找
new_element = element.relocate(new_html)
```

---

## 第六部分：文本处理

### 6.1 文本提取

```python
element = response.css('.content').get()

# 纯文本（去除 HTML 标签）
text = element.text

# 去除多余空白
clean_text = element.text_content()

# 获取所有文本（包括子元素）
all_text = ' '.join(element.xpath('.//text()').getall())
```

### 6.2 文本清理

```python
from scrapling.tools import cleanup_text

# 清理文本
dirty_text = "  Hello\n\nWorld!  "
clean = cleanup_text(dirty_text)
# 结果: "Hello World!"

# 移除额外空白
normalized = ' '.join(dirty_text.split())
```

### 6.3 正则表达式匹配

```python
response = ParselResponse(html)

# 在选择器结果上使用正则
prices = response.css('.price::text').re(r'\d+\.?\d*')

# 在整个响应上使用正则
matches = response.re(r'\d{4}-\d{2}-\d{2}')

# 获取第一个匹配
match = response.re_first(r'\d+')
```

---

## 第七部分：选择器生成

### 7.1 自动生成 CSS 选择器

```python
from scrapling.tools import generate_selector

element = response.css('.product h2').get()

# 生成最优选择器
selector = generate_selector(element)
# 可能生成: '#product-123 > h2.title' 或 '.product h2'

print(selector)
```

### 7.2 生成 XPath

```python
from scrapling.tools import generate_xpath

element = response.css('div.item').get()
xpath = generate_xpath(element)
# 生成: '//div[@class="item" and position()=1]//h2'
```

---

## 第八部分：高级用法

### 8.1 处理动态内容

```python
from scrapling.fetchers import DynamicFetcher

# 使用动态获取器处理 JavaScript 渲染的页面
fetcher = DynamicFetcher()
page = fetcher.fetch('https://example.com')

# 然后使用解析功能
products = page.css('.product')
```

### 8.2 处理 JSON 数据

```python
response = ParselResponse(html)

# 从 script 标签提取 JSON
import json
script_content = response.xpath('//script[@type="application/ld+json"]/text()').get()
data = json.loads(script_content)

# 处理 JSON API 响应
from scrapling import ParselResponse
json_response = ParselResponse('{"items": []}')
# ParselResponse 也可以处理 JSON
```

### 8.3 处理 XML

```python
from scrapling import ParselResponse

xml = """
<rss version="2.0">
    <channel>
        <item>
            <title>标题</title>
            <link>https://example.com</link>
        </item>
    </channel>
</rss>
"""

response = ParselResponse(xml)

# 使用 XPath 处理 XML
titles = response.xpath('//item/title/text()').getall()
links = response.xpath('//item/link/text()').getall()
```

---

## 第九部分：最佳实践

### 9.1 常见场景

#### 场景1：商品信息抓取

```python
from scrapling import ParselResponse

html = """
<div class="products">
    <div class="product">
        <h3 class="name">iPhone 15</h3>
        <span class="price">6999</span>
        <a href="/item/1">查看详情</a>
    </div>
    <div class="product">
        <h3 class="name">MacBook Pro</h3>
        <span class="price">19999</span>
        <a href="/item/2">查看详情</a>
    </div>
</div>
"""

response = ParselResponse(html)

products = []
for product in response.css('.product'):
    products.append({
        'name': product.css('.name::text').get(),
        'price': product.css('.price::text').get(),
        'link': response.urljoin(product.css('a::attr(href)').get())
    })

for p in products:
    print(p)
```

#### 场景2：列表页抓取

```python
response = ParselResponse(list_html)

# 提取列表项
items = response.css('.list-item')
results = []

for item in items:
    results.append({
        'title': item.css('h2::text').get(),
        'summary': item.css('.summary::text').get(),
        'image': item.css('img::attr(src)').get(),
        'link': response.urljoin(item.css('a::attr(href)').get())
    })
```

#### 场景3：分页处理

```python
def parse_list_page(html):
    response = ParselResponse(html)
    items = []

    for item in response.css('.item'):
        items.append({
            'title': item.css('h3::text').get(),
            'price': item.css('.price::text').re_first(r'\d+')
        })

    # 获取下一页链接
    next_page = response.css('.next::attr(href)').get()

    return items, next_page
```

### 9.2 性能优化

1. **使用 CSS 选择器**：通常比 XPath 更快
2. **避免过度嵌套**：深层嵌套会影响性能
3. **使用 get() 代替 getall()**：当只需要一个元素时
4. **批量处理**：使用列表推导式

```python
# 优化前
results = []
for item in response.css('.item'):
    results.append(item.css('h3::text').get())

# 优化后（更简洁）
results = response.css('h3::text').getall()
```

### 9.3 错误处理

```python
from scrapling import ParselResponse

response = ParselResponse(html)

# 安全获取属性
link = response.css('a::attr(href)').get()
if link:
    print(link)

# 使用默认值
price = response.css('.price::text').re_first(r'\d+', default='0')

# 检查元素是否存在
if response.css('.error'):
    print("发现错误元素")
```

---

## 第十部分：与其他组件集成

### 10.1 与 Fetcher 集成

```python
from scrapling.fetchers import Fetcher

# 获取页面并解析
fetcher = Fetcher()
page = fetcher.fetch('https://example.com')

# page 本身就是 ParselResponse
titles = page.css('h1::text').getall()
```

### 10.2 与 Spider 框架集成

```python
from scrapling.spiders import Spider, Response

class MySpider(Spider):
    name = "demo"
    start_urls = ["https://example.com/"]

    def parse(self, response: Response):
        # response 是 Response 对象，支持 css/xpath 方法
        for item in response.css('.product'):
            yield {
                'title': item.css('h2::text').get(),
                'price': item.css('.price::text').get()
            }

MySpider().start()
```

---

## 参考资源

- 官方文档：https://scrapling.readthedocs.io
- GitHub：https://github.com/pyd4vinci/scrapling
- PyPI：https://pypi.org/project/scrapling/
