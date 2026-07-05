# 自适应解析

## 概述

自适应解析是 Scrapling 框架最强大的特性之一，它使爬虫能够自动适应目标网站的结构变化。当网站开发者更新页面布局时，传统的爬虫通常会失败，而 Scrapling 的自适应解析可以自动调整，继续提取所需数据。

## 工作原理

### 选择器缓存机制

Scrapling 会自动保存有效的选择器到本地缓存文件（`.scrapling_cache.json`）。当下次抓取时，首先尝试缓存的选择器，如果失败则触发自适应策略。

```python
from scrapling import ParselResponse

html = """
<html>
    <body>
        <div class="product-list">
            <div class="product">
                <h2>产品 A</h2>
                <span class="price">100</span>
            </div>
        </div>
    </body>
</html>
"""

response = ParselResponse(html)

# 首次抓取时启用 auto_save
products = response.css('.product', auto_save=True)
# 选择器 '.product' 被保存到缓存
```

### 多策略查找

当主选择器失败时，Scrapling 会按顺序尝试以下策略：

1. **缓存选择器**：使用之前保存的选择器
2. **文本搜索**：基于元素文本内容查找
3. **属性搜索**：基于关键属性查找
4. **结构推断**：基于 DOM 结构推断
5. **相似度匹配**：基于元素特征相似度

```python
from scrapling import ParselResponse

# 网站更新后的 HTML
updated_html = """
<html>
    <body>
        <div class="product-grid">
            <div class="item">
                <h2>产品 A</h2>
                <span class="cost">100</span>
            </div>
        </div>
    </body>
</html>
"""

response = ParselResponse(updated_html)

# 使用自适应模式
products = response.css('.product', adaptive=True)
# 如果 '.product' 失败，会自动尝试其他策略
```

## 核心参数

### auto_save

自动保存选择器到缓存。

```python
response = ParselResponse(html)

# 简单保存
response.css('.product', auto_save=True)

# 带标签保存（用于区分不同页面）
response.css('.product', auto_save=True, tag='product_list')
```

### adaptive

启用自适应查找模式。

```python
response = ParselResponse(html)

# 启用自适应
items = response.css('.product', adaptive=True)

# 同时启用保存和自适应
items = response.css('.product', auto_save=True, adaptive=True)
```

### confidence_threshold

设置匹配置信度阈值（0-1）。

```python
response = ParselResponse(html)

# 高置信度要求
strict_items = response.css('.product', confidence_threshold=0.9)

# 低置信度要求（更宽松）
loose_items = response.css('.product', confidence_threshold=0.5)
```

## AdaptiveParser 类

### 创建实例

```python
from scrapling.adaptive import AdaptiveParser

# 从 HTML 创建
parser = AdaptiveParser(html)

# 从文件创建
parser = AdaptiveParser.from_file('page.html')

# 从 URL 获取
parser = AdaptiveParser.from_url('https://example.com')
```

### 查找方法

```python
# 基本查找
item = parser.find('.product')

# 自适应查找
item = parser.find('.product', adaptive=True)

# 带备用选择器
item = parser.find('.product', fallback=['.item', '.product-card'])
```

### 批量查找

```python
# 查找多个元素
items = parser.find_all('.product')

# 自适应批量查找
items = parser.find_all('.product', adaptive=True)
```

## 配置选项

### 全局配置

```python
from scrapling import ParselResponse
from scrapling.adaptive import AdaptiveConfig

# 创建配置
config = AdaptiveConfig(
    auto_save=True,
    adaptive_default=True,
    confidence_threshold=0.7,
    max_retries=3,
    cache_ttl=86400
)

# 使用配置
response = ParselResponse(html, adaptive_config=config)
```

### 缓存配置

```python
from scrapling.adaptive import CacheConfig

cache_config = CacheConfig(
    cache_file='.scrapling_cache.json',
    max_entries=200,
    ttl=604800,  # 7天
    auto_cleanup=True,
    compress=True
)

response = ParselResponse(html, cache_config=cache_config)
```

## 实战示例

### 电商商品列表

```python
from scrapling import ParselResponse

def parse_product_list(html):
    """解析商品列表页"""
    response = ParselResponse(html)
    
    products = []
    
    # 使用自适应解析
    for product in response.css('.product-item', adaptive=True, auto_save=True):
        products.append({
            'name': product.css('.product-name::text').get(),
            'price': product.css('.price::text').re_first(r'[\d.]+'),
            'image': product.css('img::attr(src)').get(),
            'link': product.css('a::attr(href)').get()
        })
    
    return products
```

### 新闻文章列表

```python
from scrapling import ParselResponse

def parse_news_list(html):
    """解析新闻列表页"""
    response = ParselResponse(html)
    
    # 启用自适应
    articles = response.css('.article-card', adaptive=True)
    
    results = []
    for article in articles:
        results.append({
            'title': article.css('h3::text').get(),
            'summary': article.css('.summary::text').get(),
            'time': article.css('.time::text').get(),
            'url': article.css('a::attr(href)').get()
        })
    
    return results
```

### 分页内容

```python
from scrapling import ParselResponse

def parse_paginated_content(html, base_url):
    """解析分页内容"""
    response = ParselResponse(html)
    
    items = []
    
    # 提取当前页内容
    for item in response.css('.content-item', adaptive=True):
        items.append(extract_item_data(item))
    
    # 获取下一页
    next_page = response.css('.next-page::attr(href)').get()
    
    return items, next_page
```

## 性能优化

### 选择性启用自适应

```python
# 只在关键元素上启用自适应
critical_items = response.css('.main-product', adaptive=True)

# 非关键元素使用普通选择器
secondary_items = response.css('.related-product')
```

### 批量处理

```python
# 优化前：逐个查找
for selector in selectors:
    items = response.css(selector)

# 优化后：批量处理
items = response.css(selectors[0], adaptive=True, fallback=selectors[1:])
```

### 缓存管理

```python
from scrapling.adaptive import CacheManager

# 定期清理过期缓存
CacheManager.cleanup(max_age_days=7)

# 预热缓存
CacheManager.warm_up(responses)
```

## 故障排除

### 常见问题

**问题：自适应模式找不到元素**

```python
# 解决方案1：降低置信度阈值
items = response.css('.product', confidence_threshold=0.4)

# 解决方案2：添加更多备用选择器
items = response.css('.product', fallback=['.item', '.product-card', '.goods'])

# 解决方案3：手动指定搜索策略
items = response.css('.product', search_strategy=['text', 'attribute', 'structure'])
```

**问题：缓存选择器失效**

```python
# 清除特定缓存
CacheManager.remove('.product')

# 重新保存
response.css('.product', auto_save=True)
```

## 最佳实践

1. **关键元素使用自适应**：重要的数据提取使用 `auto_save=True` 和 `adaptive=True`
2. **设置合理的置信度**：根据需求在精确度和召回率之间权衡
3. **定期清理缓存**：防止过期选择器影响新抓取
4. **记录失败情况**：帮助调试和优化选择器
5. **渐进式增强**：从简单选择器开始，逐步添加备选方案
