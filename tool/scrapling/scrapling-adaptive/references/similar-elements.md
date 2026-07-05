# 相似元素查找

## 概述

相似元素查找是 Scrapling 自适应系统中的另一个强大功能，它允许你基于一个示例元素，快速找到页面上所有与该元素相似的其他元素。这在处理结构一致但数量不定的列表页面时特别有用，例如商品列表、新闻列表、搜索结果等。

## find_similar 方法

### 基本用法

```python
from scrapling import ParselResponse

html = """
<html>
    <body>
        <div class="products">
            <div class="product-card">
                <h3>产品 A</h3>
                <span class="price">100</span>
            </div>
            <div class="product-card">
                <h3>产品 B</h3>
                <span class="price">200</span>
            </div>
            <div class="product-card">
                <h3>产品 C</h3>
                <span class="price">300</span>
            </div>
            <div class="product-card">
                <h3>产品 D</h3>
                <span class="price">400</span>
            </div>
        </div>
    </body>
</html>
"""

response = ParselResponse(html)

# 获取第一个产品卡片作为模板
template = response.css('.product-card').get()

# 查找所有相似元素
similar_products = response.find_similar(template)

print(f"找到 {len(similar_products)} 个相似元素")

for product in similar_products:
    print(f"产品: {product.css('h3::text').get()}")
```

### 返回类型

`find_similar` 返回一个包含 `SimilarElement` 对象的列表，每个对象都支持常规的选择器操作。

```python
from scrapling import ParselResponse
from scrapling.adaptive import SimilarElement

response = ParselResponse(html)

template = response.css('.product-card').get()

# 返回 SimilarElement 列表
results = response.find_similar(template)

# 每个结果都可以使用选择器
for item in results:
    # SimilarElement 支持常规选择器方法
    name = item.css('h3::text').get()
    price = item.css('.price::text').get()
    print(f"{name}: {price}")
```

## 相似度算法

### 计算因素

相似度算法综合考虑以下因素：

1. **DOM 结构相似度**：元素层级结构的相似程度
2. **属性相似度**：class、id、data-* 等属性的匹配度
3. **文本相似度**：内部文本的相似程度
4. **位置相似度**：在页面中位置的接近程度

```python
from scrapling import ParselResponse

response = ParselResponse(html)

template = response.css('.product-card').get()

# 默认相似度计算
similar = response.find_similar(template)

# 查看每个元素的相似度分数
for item in similar:
    print(f"相似度: {item.similarity_score}")
```

### 自定义权重

可以调整各因素的权重来控制匹配行为。

```python
from scrapling import ParselResponse

response = ParselResponse(html)

template = response.css('.item').get()

# 自定义权重
similar = response.find_similar(
    template,
    structure_weight=0.4,    # 结构权重
    attribute_weight=0.3,   # 属性权重
    text_weight=0.2,        # 文本权重
    position_weight=0.1     # 位置权重
)
```

### 相似度阈值

设置最小相似度阈值，只返回超过阈值的元素。

```python
from scrapling import ParselResponse

response = ParselResponse(html)

template = response.css('.product-card').get()

# 只返回相似度 > 0.7 的元素
similar = response.find_similar(
    template,
    min_similarity=0.7
)

# 只返回相似度 > 0.9 的元素（更严格）
strict_similar = response.find_similar(
    template,
    min_similarity=0.9
)
```

## SimilarElement 类

### 属性

```python
from scrapling.adaptive import SimilarElement

results = response.find_similar(template)

for item in results:
    # 相似度分数 (0-1)
    score = item.similarity_score
    
    # 匹配的详细信息
    match_info = item.match_info
    
    # 原始模板元素
    original = item.original_element
    
    print(f"分数: {score}, 匹配: {match_info}")
```

### 方法

```python
# 使用选择器
item.css('h3::text').get()
item.xpath('.//span/text()').get()

# 获取元素属性
href = item.attrib['href']

# 获取文本
text = item.text
```

## 实战示例

### 商品列表抓取

```python
from scrapling import ParselResponse

html = """
<div class="shop">
    <div class="item">
        <img src="/img/1.jpg" />
        <h3>商品 A</h3>
        <span class="price">99</span>
        <a href="/item/1">购买</a>
    </div>
    <div class="item">
        <img src="/img/2.jpg" />
        <h3>商品 B</h3>
        <span class="price">199</span>
        <a href="/item/2">购买</a>
    </div>
    <div class="item">
        <img src="/img/3.jpg" />
        <h3>商品 C</h3>
        <span class="price">299</span>
        <a href="/item/3">购买</a>
    </div>
</div>
"""

response = ParselResponse(html)

# 获取第一个商品作为模板
template = response.css('.item').get()

# 查找所有相似商品
products = []

for item in response.find_similar(template):
    products.append({
        'image': item.css('img::attr(src)').get(),
        'name': item.css('h3::text').get(),
        'price': item.css('.price::text').get(),
        'link': item.css('a::attr(href)').get(),
        'similarity': item.similarity_score
    })

for p in products:
    print(p)
```

### 新闻列表抓取

```python
from scrapling import ParselResponse

html = """
<div class="news-list">
    <article class="news-item">
        <img src="/news/1.jpg" />
        <h2>新闻标题 A</h2>
        <p class="summary">摘要内容 A</p>
        <time>2024-01-01</time>
    </article>
    <article class="news-item">
        <img src="/news/2.jpg" />
        <h2>新闻标题 B</h2>
        <p class="summary">摘要内容 B</p>
        <time>2024-01-02</time>
    </article>
    <article class="news-item">
        <img src="/news/3.jpg" />
        <h2>新闻标题 C</h2>
        <p class="summary">摘要内容 C</p>
        <time>2024-01-03</time>
    </article>
</div>
"""

response = ParselResponse(html)

# 使用第一个新闻项作为模板
template = response.css('.news-item').get()

# 提取所有新闻
news = []
for item in response.find_similar(template):
    news.append({
        'image': item.css('img::attr(src)').get(),
        'title': item.css('h2::text').get(),
        'summary': item.css('.summary::text').get(),
        'date': item.css('time::text').get()
    })

print(f"共找到 {len(news)} 条新闻")
```

### 搜索结果抓取

```python
from scrapling import ParselResponse

html = """
<div class="results">
    <div class="result-item">
        <a href="/result/1">结果 A</a>
        <span class="url">example.com/a</span>
    </div>
    <div class="result-item">
        <a href="/result/2">结果 B</a>
        <span class="url">example.com/b</span>
    </div>
    <div class="result-item">
        <a href="/result/3">结果 C</a>
        <span class="url">example.com/c</span>
    </div>
</div>
"""

response = ParselResponse(html)

# 使用第一个结果作为模板
template = response.css('.result-item').get()

# 获取所有搜索结果
results = []
for item in response.find_similar(template):
    results.append({
        'title': item.css('a::text').get(),
        'url': item.css('.url::text').get(),
        'link': item.css('a::attr(href)').get()
    })

print(results)
```

### 表格数据抓取

```python
from scrapling import ParselResponse

html = """
<table>
    <tr class="row">
        <td class="name">张三</td>
        <td class="age">25</td>
        <td class="city">北京</td>
    </tr>
    <tr class="row">
        <td class="name">李四</td>
        <td class="age">30</td>
        <td class="city">上海</td>
    </tr>
    <tr class="row">
        <td class="name">王五</td>
        <td class="age">28</td>
        <td class="city">广州</td>
    </tr>
</table>
"""

response = ParselResponse(html)

# 使用第一行作为模板
template = response.css('.row').get()

# 提取所有行
data = []
for row in response.find_similar(template):
    data.append({
        'name': row.css('.name::text').get(),
        'age': row.css('.age::text').get(),
        'city': row.css('.city::text').get()
    })

print(data)
```

### 评论列表抓取

```python
from scrapling import ParselResponse

html = """
<div class="comments">
    <div class="comment">
        <div class="user">用户 A</div>
        <div class="content">评论内容 A</div>
        <div class="time">2小时前</div>
    </div>
    <div class="comment">
        <div class="user">用户 B</div>
        <div class="content">评论内容 B</div>
        <div class="time">3小时前</div>
    </div>
    <div class="comment">
        <div class="user">用户 C</div>
        <div class="content">评论内容 C</div>
        <div class="time">5小时前</div>
    </div>
</div>
"""

response = ParselResponse(html)

# 使用第一条评论作为模板
template = response.css('.comment').get()

# 获取所有评论
comments = []
for comment in response.find_similar(template):
    comments.append({
        'user': comment.css('.user::text').get(),
        'content': comment.css('.content::text').get(),
        'time': comment.css('.time::text').get()
    })

print(comments)
```

## 高级用法

### 结合自适应解析

```python
from scrapling import ParselResponse

response = ParselResponse(html)

# 模板元素
template = response.css('.product').get()

# 结合自适应模式
similar = response.find_similar(
    template,
    adaptive=True,        # 启用自适应
    auto_save=True        # 保存选择器
)
```

### 处理动态数量的元素

```python
from scrapling import ParselResponse

def extract_list_items(html, selector):
    """提取数量不固定的列表项"""
    response = ParselResponse(html)
    
    # 获取模板
    template = response.css(selector).get()
    
    if not template:
        return []
    
    # 查找所有相似元素
    items = []
    for item in response.find_similar(template):
        items.append(item)
    
    return items

# 使用
products = extract_list_items(html, '.product-card')
print(f"找到 {len(products)} 个商品")
```

### 过滤特定元素

```python
from scrapling import ParselResponse

response = ParselResponse(html)

template = response.css('.item').get()

# 获取所有相似元素
all_items = response.find_similar(template)

# 过滤：高相似度元素
high_similarity = [item for item in all_items if item.similarity_score > 0.8]

# 过滤：特定条件的元素
filtered = [
    item for item in all_items
    if '特定文本' in (item.css('.text::text').get() or '')
]
```

### 批量处理多个模板

```python
from scrapling import ParselResponse

response = ParselResponse(html)

# 多个模板
templates = [
    response.css('.product-a').get(),
    response.css('.product-b').get(),
    response.css('.product-c').get()
]

# 收集所有元素
all_items = []
for template in templates:
    if template:
        similar = response.find_similar(template)
        all_items.extend(similar)

# 去重
unique_items = list({id(item): item for item in all_items}.values())
```

## 性能优化

### 减少比较因素

```python
# 只比较结构（最快）
similar = response.find_similar(
    template,
    compare_structure=True,
    compare_attributes=False,
    compare_text=False,
    compare_position=False
)
```

### 使用索引

```python
# 启用索引以加速大量元素查找
response = ParselResponse(html, build_index=True)

template = response.css('.item').get()
similar = response.find_similar(template, use_index=True)
```

### 限制返回数量

```python
# 限制返回数量
similar = response.find_similar(
    template,
    limit=10  # 最多返回 10 个
)
```

## 故障排除

### 找不到相似元素

```python
# 问题：返回空列表
# 解决方案1：降低相似度阈值
similar = response.find_similar(template, min_similarity=0.3)

# 解决方案2：查看模板是否正确
print("模板:", template.get())

# 解决方案3：手动检查元素
all_items = response.css('.product-card')
print(f"页面共有 {len(all_items)} 个产品")
```

### 匹配到错误元素

```python
# 问题：匹配到不相关的元素
# 解决方案：提高相似度阈值
similar = response.find_similar(template, min_similarity=0.85)

# 或者添加更多过滤条件
similar = [
    item for item in response.find_similar(template)
    if '特定条件' in (item.css('.class::text').get() or '')
]
```

### 相似度分数异常

```python
# 检查模板元素
template = response.css('.item').get()
print("模板结构:", template.get())

# 调整权重
similar = response.find_similar(
    template,
    structure_weight=0.6,  # 提高结构权重
    attribute_weight=0.2,
    text_weight=0.1,
    position_weight=0.1
)
```

## 最佳实践

1. **选择有代表性的模板**：选择结构完整、信息丰富的元素作为模板
2. **设置合适的阈值**：根据页面结构复杂度调整
3. **处理空结果**：始终检查返回值
4. **结合其他选择器**：可以使用普通选择器进行初步筛选
5. **利用相似度分数**：根据分数排序或过滤结果
6. **批量去重**：处理多个模板时注意去重
