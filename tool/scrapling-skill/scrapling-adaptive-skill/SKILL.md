---
name: scrapling-adaptive-skill
description: Scrapling 自适应解析技能
version: 1.0.0
---

# Scrapling 自适应解析技能

## 技能概述

Scrapling 的自适应解析功能是其核心竞争优势之一，它能够智能地处理网站结构变化，确保爬虫在目标网站更新后仍然能够稳定运行。该技能包含三个主要功能模块：**自适应解析**、**智能元素追踪**和**相似元素查找**。

## 核心特性

- **自适应元素追踪**：使用智能相似性算法在网站变化后重新定位元素
- **自动选择器保存**：自动保存有效的选择器到本地缓存
- **多策略查找**：支持文本、属性、结构等多种备选查找策略
- **相似元素批量查找**：快速找到与目标元素相似的所有元素
- **增量更新检测**：智能识别网站变化并调整解析策略

## 快速开始

### 安装

```bash
pip install scrapling
```

### 基础示例

```python
from scrapling import ParselResponse

html = """
<html>
    <body>
        <div class="product">
            <h2>产品名称</h2>
            <span class="price">99.99</span>
        </div>
    </body>
</html>
"""

response = ParselResponse(html)

# 启用自适应模式
products = response.css('.product', auto_save=True)

# 下次抓取时使用 adaptive=True
# 即使页面结构变化也能找到元素
```

---

## 第一部分：自适应解析基础

### 1.1 什么是自适应解析

自适应解析是 Scrapling 框架的核心特性，它能够自动处理网站结构变化。当目标网站更新其 HTML 结构时，传统的爬虫可能会失败，而 Scrapling 可以通过以下方式自动适应：

1. **选择器缓存**：保存有效的 CSS/XPath 选择器
2. **多策略查找**：当主选择器失败时，使用备用策略
3. **智能相似度匹配**：基于元素特征寻找相似的元素
4. **自动重新训练**：从成功匹配中学习新的选择器

```python
from scrapling import ParselResponse

# 首次抓取 - 保存选择器
response = ParselResponse(html)
products = response.css('.product', auto_save=True)

# 网站更新后 - 使用自适应模式
updated_response = ParselResponse(updated_html)
products = updated_response.css('.product', adaptive=True)
```

### 1.2 启用自适应功能

```python
from scrapling import ParselResponse
from scrapling.adaptive import AdaptiveParser

# 方法1：使用 auto_save 参数
response = ParselResponse(html)
items = response.css('.item', auto_save=True)

# 方法2：使用 AdaptiveParser 类
parser = AdaptiveParser(html)
items = parser.find('.item', adaptive=True)

# 方法3：全局启用自适应
response = ParselResponse(html, adaptive_default=True)
items = response.css('.item')  # 自动使用自适应模式
```

---

## 第二部分：智能元素追踪

### 2.1 SmartElement 类

SmartElement 是 Scrapling 中用于追踪元素的核心类，它能够记住元素的关键特征并在页面变化后重新定位。

```python
from scrapling.adaptive import SmartElement

# 创建智能元素
element = SmartElement(original_html, selector='.product h2')

# 在新页面中查找
new_element = element.relocate(new_html)

if new_element:
    print("找到元素:", new_element.text)
else:
    print("未找到匹配元素")
```

### 2.2 元素特征追踪

SmartElement 会跟踪以下元素特征：

- **文本内容**：元素的内部文本
- **属性值**：HTML 属性如 class、id、href 等
- **结构位置**：元素在 DOM 树中的位置
- **邻居元素**：周围元素的信息
- **样式特征**：CSS 类名等

```python
from scrapling.adaptive import SmartElement

# 跟踪特定特征
element = SmartElement(
    html,
    selector='.product h2',
    track_attributes=['class', 'id'],
    track_text=True,
    track_position=True
)

# 重新定位
new_element = element.relocate(new_html, confidence_threshold=0.8)
```

### 2.3 置信度阈值

SmartElement 使用置信度来判断找到的元素是否足够相似。

```python
from scrapling.adaptive import SmartElement

element = SmartElement(html, selector='.title')

# 高置信度 - 更严格匹配
strict_match = element.relocate(new_html, confidence_threshold=0.9)

# 低置信度 - 更宽松匹配
loose_match = element.relocate(new_html, confidence_threshold=0.5)

# 获取匹配分数
result = element.relocate_with_score(new_html)
print(f"匹配分数: {result['score']}")
print(f"找到元素: {result['element']}")
```

---

## 第三部分：相似元素查找

### 3.1 find_similar 方法

Scrapling 提供了强大的相似元素查找功能，可以快速找到与目标元素相似的所有元素。

```python
from scrapling import ParselResponse

html = """
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
</div>
"""

response = ParselResponse(html)

# 找到第一个产品卡片
template = response.css('.product-card').get()

# 查找相似元素
similar = response.find_similar(template)
print(f"找到 {len(similar)} 个相似元素")
```

### 3.2 相似度算法

相似度算法基于多个维度计算：

- **DOM 结构相似度**：元素层级结构的相似程度
- **属性相似度**：class、id 等属性的匹配度
- **文本相似度**：内部文本的相似程度
- **位置相似度**：在页面中位置的接近程度

```python
from scrapling import ParselResponse

response = ParselResponse(html)

# 获取模板元素
template = response.css('.product-card').get()

# 自定义相似度权重
similar = response.find_similar(
    template,
    structure_weight=0.4,   # 结构权重
    attribute_weight=0.3,   # 属性权重
    text_weight=0.2,       # 文本权重
    position_weight=0.1     # 位置权重
)

# 获取每个元素的相似度分数
for elem in similar:
    score = elem.similarity_score
    print(f"相似度: {score}")
```

### 3.3 批量处理相似元素

```python
from scrapling import ParselResponse

response = ParselResponse(html)

# 找到所有相似元素并提取数据
products = []
for card in response.find_similar(response.css('.product-card').get()):
    products.append({
        'title': card.css('h3::text').get(),
        'price': card.css('.price::text').get()
    })

print(products)
```

---

## 第四部分：缓存管理

### 4.1 选择器缓存

Scrapling 自动将有效的选择器保存到缓存文件。

```python
from scrapling import ParselResponse
import json

# 首次使用 - 保存选择器
response = ParselResponse(html)
response.css('.product', auto_save=True)

# 查看缓存内容
with open('.scrapling_cache.json', 'r') as f:
    cache = json.load(f)
    print(cache)
```

### 4.2 手动管理缓存

```python
from scrapling.adaptive import CacheManager

# 查看缓存
cache = CacheManager.load()
print(cache.get_selectors('.product'))

# 更新选择器
CacheManager.update('.product', ['.product', '.item', 'div.product'])

# 清除缓存
CacheManager.clear()

# 清除特定选择器
CacheManager.remove('.product')
```

### 4.3 缓存策略配置

```python
from scrapling import ParselResponse
from scrapling.adaptive import CacheConfig

# 配置缓存
config = CacheConfig(
    cache_file='.custom_cache.json',
    max_entries=100,
    ttl=86400,  # 24小时
    auto_cleanup=True
)

response = ParselResponse(html, cache_config=config)
```

---

## 第五部分：高级用法

### 5.1 自定义适应策略

```python
from scrapling.adaptive import AdaptiveStrategy, SmartElement

class CustomStrategy(AdaptiveStrategy):
    def __init__(self):
        super().__init__()
        self.fallback_selectors = []

    def find_element(self, selector, html):
        # 首先尝试主选择器
        result = self._try_selector(selector, html)
        if result:
            return result

        # 然后尝试备用选择器
        for fallback in self.fallback_selectors:
            result = self._try_selector(fallback, html)
            if result:
                return result

        # 最后使用智能查找
        return self._smart_find(selector, html)

# 使用自定义策略
response = ParselResponse(html, strategy=CustomStrategy())
```

### 5.2 结合多种选择器

```python
from scrapling import ParselResponse

response = ParselResponse(html)

# CSS 选择器 + 自适应
items = response.css('.product', adaptive=True)

# XPath 选择器 + 自适应
items = response.xpath('//div[@class="product"]', adaptive=True)

# 混合策略
items = response.css('.item', auto_save=True, adaptive=True)
```

### 5.3 错误处理和调试

```python
from scrapling import ParselResponse
from scrapling.adaptive import AdaptiveError

try:
    response = ParselResponse(html)
    items = response.css('.product', adaptive=True)
    
    if not items:
        print("警告: 未找到元素，尝试备用策略")
        items = response.xpath('//div[contains(@class, "product")]')
        
except AdaptiveError as e:
    print(f"自适应解析失败: {e}")
    # 降级到基本选择器
    items = response.css('.product')

# 调试模式
response = ParselResponse(html, debug=True)
items = response.css('.product', adaptive=True)
# 会输出详细的匹配过程
```

---

## 第六部分：最佳实践

### 6.1 常见场景

#### 场景1：电商商品列表

```python
from scrapling import ParselResponse
from scrapling.adaptive import SmartElement

def parse_products(html):
    response = ParselResponse(html)
    
    # 找到第一个产品作为模板
    first_product = response.css('.product-card').get()
    
    # 查找所有相似产品
    products = []
    for card in response.find_similar(first_product):
        products.append({
            'name': card.css('.product-name::text').get(),
            'price': card.css('.price::text').re_first(r'\d+'),
            'link': card.css('a::attr(href)').get()
        })
    
    return products
```

#### 场景2：新闻文章列表

```python
from scrapling import ParselResponse

def parse_news(html):
    response = ParselResponse(html)
    
    # 启用自适应保存
    articles = response.css('.news-item', auto_save=True)
    
    results = []
    for article in articles:
        results.append({
            'title': article.css('h2::text').get(),
            'summary': article.css('.summary::text').get(),
            'date': article.css('.date::text').get(),
            'author': article.css('.author::text').get()
        })
    
    return results
```

### 6.2 性能优化

1. **合理使用 auto_save**：只在关键元素上启用
2. **设置合适的置信度阈值**：避免过度匹配
3. **批量处理**：使用 find_similar 代替循环单个查找
4. **缓存策略**：定期清理过期缓存

```python
# 优化示例
response = ParselResponse(html)

# 只在关键元素上启用自适应
main_items = response.css('.main-item', auto_save=True)

# 非关键元素使用普通选择器
secondary_items = response.css('.secondary-item')
```

### 6.3 错误处理

```python
from scrapling import ParselResponse
from scrapling.adaptive import SmartElement

def safe_adaptive_find(html, selector):
    response = ParselResponse(html)
    
    try:
        # 尝试自适应查找
        items = response.css(selector, adaptive=True)
        if items:
            return items
        
        # 尝试备用选择器
        items = response.xpath(f'//div[contains(@class, "{selector.lstrip(".")}")]')
        if items:
            return items
            
    except Exception as e:
        print(f"查找失败: {e}")
    
    # 最后手段：使用相似元素查找
    return response.find_similar(response.css(selector).get()) if response.css(selector).get() else []
```

---

## 参考资源

- 官方文档：https://scrapling.readthedocs.io
- 自适应解析：https://scrapling.readthedocs.io/en/latest/adaptive.html
- GitHub：https://github.com/pyd4vinci/scrapling
- PyPI：https://pypi.org/project/scrapling/

---

## 相关技能

- [scrapling-core-skill](../scrapling-core-skill/SKILL.md) - Scrapling 核心解析引擎
