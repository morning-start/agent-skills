# Scrapling 基础使用

## 简介

Scrapling 核心解析引擎提供了强大的 HTML/XML 解析能力。本文档介绍基础使用，包括解析 HTML、CSS/XPath 选择器、元素操作和文本提取。

## 创建响应对象

### 从 HTML 字符串创建

```python
from scrapling import ParselResponse

html = """
<!DOCTYPE html>
<html>
<head>
    <title>示例页面</title>
</head>
<body>
    <div id="container">
        <h1 class="title">欢迎访问</h1>
        <ul class="products">
            <li class="product" data-id="1">
                <h2>产品 A</h2>
                <span class="price">99.99</span>
            </li>
            <li class="product" data-id="2">
                <h2>产品 B</h2>
                <span class="price">149.99</span>
            </li>
        </ul>
    </div>
</body>
</html>
"""

response = ParselResponse(html)
```

### 从文件加载

```python
with open('page.html', 'r', encoding='utf-8') as f:
    response = ParselResponse(f.read())
```

### 从 URL 获取（需要 fetchers）

```python
from scrapling.fetchers import Fetcher

fetcher = Fetcher()
page = fetcher.fetch('https://example.com')

# page 本身就可以直接使用 CSS/XPath 选择器
titles = page.css('h1::text').getall()
```

## CSS 选择器

### 基本选择

```python
response = ParselResponse(html)

# ID 选择器
element = response.css('#container')

# 类选择器
elements = response.css('.product')

# 标签选择器
links = response.css('a')

# 组合选择器
items = response.css('ul.products li')
```

### 属性选择器

```python
# 选择有特定属性的元素
element = response.css('[data-id]')

# 属性值精确匹配
element = response.css('[data-id="1"]')

# 属性值包含
elements = response.css('[class*="product"]')

# 属性值开头匹配
elements = response.css('[class^="prod"]')

# 属性值结尾匹配
elements = response.css('[class$="uct"]')
```

### 伪元素

```python
# 获取第一个元素
first = response.css('.product::first').get()

# 获取最后一个元素
last = response.css('.product::last').get()

# 获取第 n 个元素（从 1 开始）
second = response.css('.product::nth(2)').get()

# 获取所有文本
all_text = response.css('.title::text').getall()
```

### 获取元素属性

```python
# 获取 href 属性
links = response.css('a')
for link in links:
    href = link.attrib['href']
    # 或
    href = link.get('href')

# 使用 ::attr() 伪元素
href = response.css('a::attr(href)').get()
src = response.css('img::attr(src)').get()
```

## XPath 选择器

### 基本选择

```python
response = ParselResponse(html)

# 选择元素
element = response.xpath('//div[@id="container"]')
elements = response.xpath('//li[@class="product"]')

# 选择文本
title = response.xpath('//h1/text()').get()

# 选择属性
href = response.xpath('//a/@href').get()
```

### 条件过滤

```python
# 属性包含
elements = response.xpath('//div[contains(@class, "product")]')

# 属性匹配
elements = response.xpath('//li[@data-id="1"]')

# 位置选择
first_product = response.xpath('//li[@class="product"][1]').get()
last_product = response.xpath('//li[@class="product"][last()]').get()

# 文本包含
elements = response.xpath('//div[contains(text(), "欢迎")]')
```

### 轴（Axe）操作

```python
# 父元素
parent = response.xpath('//span/parent::*').get()

# 子元素
children = response.xpath('//ul/child::*').getall()

# 祖先元素
ancestors = response.xpath('//span/ancestor::*').getall()

# 后续兄弟元素
siblings = response.xpath('//h1/following-sibling::*').getall()

# 前置兄弟元素
prev_siblings = response.xpath('//h1/preceding-sibling::*').getall()
```

## 元素操作

### 获取元素数据

```python
response = ParselResponse(html)

# get() - 获取单个元素或值
element = response.css('.product').get()
text = response.css('h1::text').get()

# getall() - 获取所有元素或值
elements = response.css('.product').getall()
texts = response.css('li::text').getall()

# extract() 和 extract_first() - Scrapy 兼容方法
items = response.css('li::text').extract()
item = response.css('h1::text').extract_first()
```

### 元素属性操作

```python
element = response.css('.product').get()

# 获取所有属性
attrs = element.attrib

# 获取单个属性
id_value = element.attrib['data-id']
name = element.get('data-id')

# 检查属性存在
has_id = 'data-id' in element.attrib
```

### 元素文本操作

```python
element = response.css('.product h2').get()

# 获取文本（仅直接子节点）
text = element.text

# 获取所有文本（包括所有后代）
all_text = element.text_content()

# 获取 inner HTML
inner = element.inner_html()

# 使用 XPath 获取文本
texts = element.xpath('.//text()').getall()
clean_text = ' '.join(texts)
```

## 文本提取

### 基本文本提取

```python
response = ParselResponse(html)

# 从选择器提取文本
title = response.css('h1::text').get()

# 提取所有匹配的文本
all_titles = response.css('h2::text').getall()
```

### 文本清理

```python
# 提取带空白的文本
raw_text = response.css('.description::text').get()
# "  Hello   World  "

# 清理空白
clean_text = ' '.join(raw_text.split())
# "Hello World"

# 使用正则提取
price = response.css('.price::text').re_first(r'\d+\.?\d*')
prices = response.css('.price::text').re(r'\d+\.?\d*')
```

### 正则表达式

```python
response = ParselResponse(html)

# 在选择器结果上使用正则
prices = response.css('.price::text').re(r'\d+\.\d{2}')
price = response.css('.price::text').re_first(r'\d+')

# 在整个响应上使用正则
dates = response.re(r'\d{4}-\d{2}-\d{2}')
date = response.re_first(r'\d{4}-\d{2}-\d{2}')

# 使用默认值
price = response.css('.price::text').re_first(r'\d+', default='0')
```

## DOM 导航

### 父子关系

```python
element = response.css('.price').get()

# 获取父元素
parent = element.xpath('./..').get()
# 或使用 parent 属性（如果可用）
parent = element.parent

# 获取所有祖先
ancestors = element.xpath('./ancestor::*').getall()

# 获取根元素
root = element.root
```

### 兄弟关系

```python
element = response.css('.product').get()

# 下一个兄弟
next_elem = element.xpath('./following-sibling::*').get()

# 前一个兄弟
prev_elem = element.xpath('./preceding-sibling::*').get()

# 所有后续兄弟
all_next = element.xpath('./following-sibling::*').getall()
```

### 子元素

```python
container = response.css('#container').get()

# 所有直接子元素
children = container.xpath('./child::*').getall()

# 第一个子元素
first = container.xpath('./child::*[1]').get()

# 最后一个子元素
last = container.xpath('./child::*[last()]').get()
```

## 实用示例

### 示例 1：产品列表抓取

```python
from scrapling import ParselResponse

html = """
<ul class="products">
    <li class="product">
        <h3>iPhone 15</h3>
        <span class="price">6999</span>
        <a href="/product/iphone-15">详情</a>
    </li>
    <li class="product">
        <h3>MacBook Pro</h3>
        <span class="price">19999</span>
        <a href="/product/macbook-pro">详情</a>
    </li>
</ul>
"""

response = ParselResponse(html)

products = []
for product in response.css('.product'):
    products.append({
        'name': product.css('h3::text').get(),
        'price': product.css('.price::text').get(),
        'url': response.urljoin(product.css('a::attr(href)').get())
    })

for p in products:
    print(p)
```

输出：
```
{'name': 'iPhone 15', 'price': '6999', 'url': '/product/iphone-15'}
{'name': 'MacBook Pro', 'price': '19999', 'url': '/product/macbook-pro'}
```

### 示例 2：分页链接提取

```python
html = """
<div class="pagination">
    <a href="?page=1">1</a>
    <a href="?page=2">2</a>
    <a href="?page=3">3</a>
    <a href="?page=next">下一页</a>
</div>
"""

response = ParselResponse(html)

# 获取所有页码链接
pages = response.css('.pagination a::attr(href)').getall()
print(pages)
# ['?page=1', '?page=2', '?page=3', '?page=next']

# 转换为绝对 URL
base_url = 'https://example.com/products'
full_urls = [response.urljoin(p) for p in pages]
print(full_urls)
# ['https://example.com/products?page=1', ...]
```

### 示例 3：表格数据提取

```python
html = """
<table class="data">
    <thead>
        <tr><th>名称</th><th>价格</th><th>库存</th></tr>
    </thead>
    <tbody>
        <tr><td>产品 A</td><td>100</td><td>50</td></tr>
        <tr><td>产品 B</td><td>200</td><td>30</td></tr>
        <tr><td>产品 C</td><td>150</td><td>0</td></tr>
    </tbody>
</table>
"""

response = ParselResponse(html)

# 获取表头
headers = response.css('th::text').getall()
print(headers)
# ['名称', '价格', '库存']

# 获取所有行数据
rows = response.css('tbody tr')
data = []

for row in rows:
    cells = row.css('td::text').getall()
    data.append(dict(zip(headers, cells)))

print(data)
# [{'名称': '产品 A', '价格': '100', '库存': '50'}, ...]
```

### 示例 4：处理 JSON 数据

```python
html = """
<script type="application/ld+json">
{
    "name": "示例产品",
    "price": "99.99",
    "availability": "https://schema.org/InStock"
}
</script>
"""

import json
from scrapling import ParselResponse

response = ParselResponse(html)

# 从 script 标签提取 JSON
script_content = response.xpath(
    '//script[@type="application/ld+json"]/text()'
).get()

data = json.loads(script_content)
print(data)
# {'name': '示例产品', 'price': '99.99', 'availability': '...'}
```

### 示例 5：处理 XML/RSS

```python
xml = """
<rss version="2.0">
    <channel>
        <item>
            <title>文章标题</title>
            <link>https://example.com/1</link>
            <description>文章描述</description>
            <pubDate>2024-01-15</pubDate>
        </item>
        <item>
            <title>另一篇文章</title>
            <link>https://example.com/2</link>
            <description>另一篇描述</description>
            <pubDate>2024-01-16</pubDate>
        </item>
    </channel>
</rss>
"""

response = ParselResponse(xml)

items = []
for item in response.xpath('//item'):
    items.append({
        'title': item.xpath('./title/text()').get(),
        'link': item.xpath('./link/text()').get(),
        'description': item.xpath('./description/text()').get(),
        'date': item.xpath('./pubDate/text()').get()
    })

for item in items:
    print(item)
```

## 常见问题

### Q1: 如何处理不存在的元素？

```python
# 使用默认值
text = response.css('.missing::text').get()
# 返回 None

# 使用 default 参数
text = response.css('.missing::text').re_first(r'\d+', default='0')

# 检查是否存在
if response.css('.error'):
    print("发现错误")
```

### Q2: 如何处理多个同名属性？

```python
# 元素可能有多个 class
element = response.css('.product').get()
classes = element.attrib.get('class', '').split()
# ['product', 'active', 'featured']
```

### Q3: 如何处理特殊字符？

```python
# HTML 实体会自动解码
html = "<p>&lt;hello&gt; &amp; world</p>"
response = ParselResponse(html)
text = response.css('p::text').get()
# 输出: "<hello> & world"
```

### Q4: 编码问题？

```python
# 指定编码
response = ParselResponse(html, encoding='utf-8')

# 或自动检测
response = ParselResponse(html)
print(response.encoding)
```

## 下一步

- 学习[安装配置](./installation.md)以使用更多功能
- 了解自适应解析和智能元素追踪
- 探索 Spider 框架进行大规模爬取
