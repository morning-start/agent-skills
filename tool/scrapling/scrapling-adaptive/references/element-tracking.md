# 智能元素追踪

## 概述

智能元素追踪（SmartElement）是 Scrapling 自适应系统的核心组件，它能够"记住"特定元素的关键特征，并在页面结构发生变化后，通过智能相似度匹配重新定位该元素。这使得爬虫能够在目标网站更新后仍然正常工作，无需手动修改选择器。

## SmartElement 类

### 基本用法

```python
from scrapling.adaptive import SmartElement

# 原始 HTML
original_html = """
<html>
    <body>
        <div class="product">
            <h2>产品名称</h2>
            <span class="price">99.99</span>
        </div>
    </body>
</html>
"""

# 创建 SmartElement
element = SmartElement(original_html, selector='.product h2')

# 网站更新后的 HTML
updated_html = """
<html>
    <body>
        <div class="product-item">
            <h2>产品名称</h2>
            <span class="price">99.99</span>
        </div>
    </body>
</html>
"""

# 重新定位元素
new_element = element.relocate(updated_html)

if new_element:
    print("找到元素:", new_element.text)
```

### 初始化参数

```python
SmartElement(
    html,                    # 原始 HTML
    selector='.selector',     # CSS 选择器
    track_text=True,          # 跟踪文本内容
    track_attributes=['class', 'id'],  # 跟踪的属性
    track_position=True,       # 跟踪位置
    track_structure=True,     # 跟踪结构
)
```

## 追踪的特征

### 文本追踪

SmartElement 会记录元素的文本内容，用于后续相似度匹配。

```python
from scrapling.adaptive import SmartElement

# 跟踪文本
element = SmartElement(
    html,
    selector='h2.product-title',
    track_text=True
)

# 重新定位时基于文本匹配
new_element = element.relocate(updated_html)
# 如果新页面中有相同文本的元素，会被找到
```

### 属性追踪

可以指定要跟踪的 HTML 属性。

```python
from scrapling.adaptive import SmartElement

# 只跟踪特定属性
element = SmartElement(
    html,
    selector='a.link',
    track_attributes=['class', 'href', 'data-id']
)

# 重新定位
new_element = element.relocate(updated_html)
```

### 位置追踪

跟踪元素在 DOM 中的位置信息。

```python
from scrapling.adaptive import SmartElement

# 启用位置追踪
element = SmartElement(
    html,
    selector='.item',
    track_position=True
)

# 重新定位时考虑位置
new_element = element.relocate(updated_html)
```

### 结构追踪

跟踪元素的 DOM 结构特征。

```python
from scrapling.adaptive import SmartElement

# 启用结构追踪
element = SmartElement(
    html,
    selector='.card',
    track_structure=True
)

new_element = element.relocate(updated_html)
```

## 重新定位方法

### relocate()

基本的重新定位方法。

```python
element = SmartElement(html, selector='.product h2')

# 重新定位
new_element = element.relocate(new_html)

if new_element:
    print(new_element.text)
```

### relocate_with_score()

返回包含匹配分数的结果。

```python
element = SmartElement(html, selector='.title')

# 获取详细结果
result = element.relocate_with_score(new_html)

print(f"匹配分数: {result['score']}")
print(f"元素: {result['element']}")
print(f"匹配方法: {result['method']}")
```

### relocate_all()

找到所有匹配的元素。

```python
element = SmartElement(html, selector='.product')

# 找到所有相似元素
elements = element.relocate_all(new_html)

for elem in elements:
    print(f"分数: {elem.similarity_score}")
    print(f"内容: {elem.text}")
```

## 置信度控制

### confidence_threshold

设置最小匹配置信度。

```python
element = SmartElement(html, selector='.item')

# 高置信度（更严格）
strict_match = element.relocate(
    new_html,
    confidence_threshold=0.9
)

# 低置信度（更宽松）
loose_match = element.relocate(
    new_html,
    confidence_threshold=0.4
)
```

### 预定义阈值

```python
# 精确匹配
element.relocate(new_html, confidence_threshold=0.95)

# 宽松匹配
element.relocate(new_html, confidence_threshold=0.5)

# 默认值
element.relocate(new_html)  # 默认 0.7
```

## 匹配分数

### similarity_score 属性

每个重新定位的元素都有相似度分数。

```python
element = SmartElement(html, selector='.product')

results = element.relocate_all(new_html)

for result in results:
    score = result.similarity_score
    
    if score >= 0.9:
        print("高匹配:", result.text)
    elif score >= 0.7:
        print("中匹配:", result.text)
    else:
        print("低匹配:", result.text)
```

### 分数计算

相似度由多个因素综合决定：

- **文本相似度**：元素文本的匹配程度
- **属性相似度**：class、id 等属性的匹配程度
- **结构相似度**：DOM 层级结构的相似程度
- **位置相似度**：在页面中位置的接近程度

```python
from scrapling.adaptive import SmartElement

# 自定义各因素权重
element = SmartElement(
    html,
    selector='.item',
    text_weight=0.4,
    attribute_weight=0.3,
    structure_weight=0.2,
    position_weight=0.1
)
```

## 实战示例

### 电商商品追踪

```python
from scrapling.adaptive import SmartElement
from scrapling import ParselResponse

def track_product_price(original_html, product_name, updated_html):
    """追踪商品价格变化"""
    
    # 找到目标商品元素
    response = ParselResponse(original_html)
    product = response.css(f'.product:contains("{product_name}")').get()
    
    if not product:
        return None
    
    # 创建 SmartElement
    element = SmartElement(
        original_html,
        selector=f'.product:contains("{product_name}")',
        track_text=True,
        track_attributes=['data-product-id']
    )
    
    # 重新定位
    result = element.relocate_with_score(updated_html)
    
    if result['element'] and result['score'] > 0.7:
        return {
            'name': result['element'].css('.name::text').get(),
            'price': result['element'].css('.price::text').get(),
            'confidence': result['score']
        }
    
    return None
```

### 新闻文章追踪

```python
from scrapling.adaptive import SmartElement

def track_article_updates(original_html, article_title, updated_html):
    """追踪文章更新"""
    
    # 创建追踪器
    tracker = SmartElement(
        original_html,
        selector=f'.article:contains("{article_title}")',
        track_text=True,
        track_attributes=['data-article-id'],
        track_position=True
    )
    
    # 检查更新
    result = tracker.relocate_with_score(updated_html)
    
    if result['element']:
        return {
            'title': result['element'].css('h2::text').get(),
            'content': result['element'].css('.content::text').get(),
            'updated': result['element'].css('.update-time::text').get(),
            'match_score': result['score']
        }
    
    return None
```

### 列表项批量追踪

```python
from scrapling.adaptive import SmartElement

def track_list_items(original_html, updated_html):
    """追踪列表项变化"""
    
    from scrapling import ParselResponse
    
    response = ParselResponse(original_html)
    items = response.css('.list-item')
    
    tracked_items = []
    
    for item in items:
        # 为每个元素创建追踪器
        tracker = SmartElement(
            original_html,
            selector=item.css_first,
            track_text=True,
            track_attributes=['class', 'data-id']
        )
        
        # 重新定位
        result = tracker.relocate_with_score(updated_html)
        
        if result['element']:
            tracked_items.append({
                'original': item.text,
                'updated': result['element'].text,
                'score': result['score']
            })
    
    return tracked_items
```

## 高级用法

### 自定义匹配策略

```python
from scrapling.adaptive import SmartElement

class CustomSmartElement(SmartElement):
    def calculate_similarity(self, element1, element2):
        # 自定义相似度算法
        score = super().calculate_similarity(element1, element2)
        
        # 添加自定义逻辑
        if element1.attrib.get('data-category') == element2.attrib.get('data-category'):
            score += 0.1
        
        return score

# 使用自定义类
element = CustomSmartElement(html, selector='.item')
```

### 批量追踪

```python
from scrapling.adaptive import SmartElement

def batch_track(html_list, selector):
    """批量追踪多个页面的相同元素"""
    
    trackers = []
    
    for html in html_list:
        element = SmartElement(html, selector=selector)
        trackers.append(element)
    
    return trackers
```

### 持久化追踪器

```python
import json
from scrapling.adaptive import SmartElement

# 保存追踪器
def save_tracker(element, filename):
    data = {
        'selector': element.selector,
        'tracked_text': element.tracked_text,
        'tracked_attributes': element.tracked_attributes,
        'tracked_position': element.tracked_position
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f)

# 加载追踪器
def load_tracker(filename, html):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    element = SmartElement(
        html,
        selector=data['selector'],
        track_attributes=data['tracked_attributes']
    )
    
    return element
```

## 性能优化

### 减少追踪特征

```python
# 追踪所有特征（慢）
element = SmartElement(
    html,
    selector='.item',
    track_text=True,
    track_attributes=['class', 'id', 'href', 'data-*'],
    track_position=True,
    track_structure=True
)

# 只追踪关键特征（快）
element = SmartElement(
    html,
    selector='.item',
    track_text=True,
    track_attributes=['data-id']
)
```

### 使用索引

```python
# 预建索引以加速查找
element = SmartElement(
    html,
    selector='.product',
    build_index=True  # 创建文本/属性索引
)
```

### 并行处理

```python
from concurrent.futures import ThreadPoolExecutor

def parallel_relocate(trackers, html):
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(
            lambda t: t.relocate_with_score(html),
            trackers
        ))
    
    return results
```

## 故障排除

### 找不到元素

```python
# 问题：找不到匹配元素
# 解决方案1：降低阈值
result = element.relocate(new_html, confidence_threshold=0.3)

# 解决方案2：查看所有匹配
all_results = element.relocate_all(new_html)

# 解决方案3：手动检查
print("追踪的特征:", element.get_tracked_features())
```

### 匹配不准确

```python
# 问题：匹配到错误的元素
# 解决方案：增加追踪特征
element = SmartElement(
    html,
    selector='.item',
    track_text=True,
    track_attributes=['class', 'id', 'data-id', 'data-type'],
    track_position=True
)
```

## 最佳实践

1. **选择有辨识度的元素**：选择具有独特文本或属性的元素
2. **适当设置阈值**：根据需求在精确度和召回率之间平衡
3. **组合多个特征**：同时追踪文本、属性等多个特征
4. **处理失败情况**：始终检查返回值是否为 None
5. **记录关键信息**：保存原始元素用于调试
