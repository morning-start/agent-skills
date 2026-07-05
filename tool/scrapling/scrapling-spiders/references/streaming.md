# 流式输出和暂停恢复

本文档详细介绍 Scrapling Spider 的流式输出功能和暂停/恢复机制，帮助你处理大规模数据爬取和长时间运行任务。

---

## 1. 流式输出概述

流式输出允许 Scrapling Spider 在爬取过程中实时写入数据，无需等待所有请求完成。这对于大规模数据处理和长时间爬取任务特别有用。

---

## 2. 配置流式输出

### 2.1 基本配置

```python
from scrapling.spiders import Spider, Response

class StreamingSpider(Spider):
    name = "streaming"
    start_urls = ["https://example.com/products"]

    custom_settings = {
        'STREAM_FILE': 'output.jsonl',    # 输出文件路径
        'STREAM_MODE': 'jsonl',          # 输出模式
    }

    def parse(self, response: Response):
        for product in response.css('.product'):
            yield {
                'name': product.css('.name::text').get(),
                'price': product.css('.price::text').get()
            }
```

### 2.2 输出模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `json` | JSON 数组格式 | 小数据集，最终一次性处理 |
| `jsonl` | JSON Lines 格式 | 大数据集，流式处理 |
| `csv` | CSV 格式 | 表格数据，便于 Excel 处理 |

### 2.3 JSON 模式

```python
class JsonOutputSpider(Spider):
    name = "json_output"

    custom_settings = {
        'STREAM_FILE': 'data.json',
        'STREAM_MODE': 'json',
    }

    def parse(self, response: Response):
        for item in response.css('.item'):
            yield {
                'title': item.css('h3::text').get(),
                'link': item.css('a::attr(href)').get()
            }
```

输出文件内容：
```json
[
  {"title": "产品1", "link": "/item/1"},
  {"title": "产品2", "link": "/item/2"}
]
```

### 2.4 JSONL 模式（推荐）

```python
class JsonlOutputSpider(Spider):
    name = "jsonl_output"

    custom_settings = {
        'STREAM_FILE': 'data.jsonl',
        'STREAM_MODE': 'jsonl',
    }
```

输出文件内容：
```jsonl
{"title": "产品1", "link": "/item/1"}
{"title": "产品2", "link": "/item/2"}
```

### 2.5 CSV 模式

```python
class CsvOutputSpider(Spider):
    name = "csv_output"

    custom_settings = {
        'STREAM_FILE': 'data.csv',
        'STREAM_MODE': 'csv',
    }

    custom_settings_csv = {
        'CSV_EXPORT_FIELDS': ['title', 'price', 'link']
    }
```

---

## 3. 手动流式写入

### 3.1 stream_write 方法

```python
import json

class ManualStreamSpider(Spider):
    name = "manual_stream"
    start_urls = ["https://example.com/"]

    def parse(self, response: Response):
        for product in response.css('.product'):
            item = {
                'name': product.css('.name::text').get(),
                'price': product.css('.price::text').get()
            }
            self.stream_write(json.dumps(item))

        next_page = response.css('.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
```

### 3.2 stream_write 注意事项

```python
class CarefulStreamSpider(Spider):
    name = "careful_stream"

    def parse(self, response: Response):
        try:
            item = self.extract_item(response)
            self.stream_write(item)
        except Exception as e:
            self.logger.error(f"解析错误: {e}")
            yield {'error': str(e), 'url': response.url}

    def extract_item(self, response: Response):
        return {
            'title': response.css('h1::text').get(),
            'content': response.css('.content::text').get()
        }
```

---

## 4. 暂停和恢复机制

### 4.1 基本概念

Scrapling 的暂停/恢复功能允许你：

1. **保存状态**：爬取进度自动保存
2. **中断爬取**：随时暂停（Ctrl+C）
3. **恢复爬取**：从中断处继续

### 4.2 配置 JOBDIR

```python
class ResumableSpider(Spider):
    name = "resumable"
    start_urls = [f"https://example.com/item/{i}" for i in range(1000)]

    custom_settings = {
        'JOBDIR': 'crawls/resumable-001',
    }

    def parse(self, response: Response):
        yield {
            'id': response.url.split('/')[-1],
            'title': response.css('h1::text').get()
        }
```

### 4.3 运行命令

```bash
# 启动爬虫
scrapling runspider resumable_spider.py

# 爬虫运行中按 Ctrl+C 暂停
# 状态自动保存到 crawls/resumable-001 目录

# 恢复爬虫（使用相同命令）
scrapling runspider resumable_spider.py
```

### 4.4 JOBDIR 目录结构

```
crawls/resumable-001/
├── requests.queue      # 待处理请求队列
├── scheduler.pickle   # 调度器状态
└── spider.data        # Spider 自定义数据
```

---

## 5. 高级暂停恢复

### 5.1 自定义状态数据

```python
class StateSpider(Spider):
    name = "stateful"

    custom_settings = {
        'JOBDIR': 'crawls/state-001',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_count = 0

    def parse(self, response: Response):
        self.page_count += 1

        for item in response.css('.item'):
            yield item.css('::text').get()

        if self.page_count < 100:
            next_url = f"https://example.com/page/{self.page_count + 1}"
            yield self.request(next_url, callback=self.parse)
```

### 5.2 保存自定义状态

```python
class PersistentStateSpider(Spider):
    name = "persistent"

    custom_settings = {
        'JOBDIR': 'crawls/persistent-001',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scraped_ids = set()

    def parse(self, response: Response):
        for item in response.css('.item'):
            item_id = item.css('::attr(id)').get()

            if item_id not in self.scraped_ids:
                self.scraped_ids.add(item_id)
                yield {'id': item_id}

        self.save_state()  # 手动保存状态

    def save_state(self):
        state = {'scraped_ids': list(self.scraped_ids)}
        self.logger.info(f"已保存 {len(self.scraped_ids)} 个 ID")
```

---

## 6. 流式 + 暂停恢复组合

### 6.1 完整配置

```python
class FullFeatureSpider(Spider):
    name = "full_feature"
    start_urls = [f"https://example.com/page/{i}" for i in range(1, 101)]

    custom_settings = {
        'JOBDIR': 'crawls/full-001',
        'STREAM_FILE': 'output.jsonl',
        'STREAM_MODE': 'jsonl',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0.5,
    }

    def parse(self, response: Response):
        for item in response.css('.product'):
            yield {
                'name': item.css('.name::text').get(),
                'price': item.css('.price::text').get(),
                'url': response.url
            }
```

### 6.2 使用场景

```bash
# 场景1：启动大规模爬取
scrapling runspider full_feature_spider.py

# 场景2：Ctrl+C 暂停，状态已保存

# 场景3：恢复爬取
scrapling runspider full_feature_spider.py

# 场景4：爬取完成，查看输出
# output.jsonl 包含所有数据
```

---

## 7. 错误恢复

### 7.1 处理失败请求

```python
class ErrorRecoverySpider(Spider):
    name = "error_recovery"

    custom_settings = {
        'JOBDIR': 'crawls/error-recovery',
        'RETRY_TIMES': 3,
    }

    def parse(self, response: Response):
        if response.status != 200:
            yield self.request(
                response.url,
                callback=self.parse,
                dont_filter=True,
                meta={'priority': -1}
            )
            return

        yield {'url': response.url}
```

### 7.2 清理状态目录

```python
import shutil

class CleanSpider(Spider):
    name = "clean"

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crawler.signals.connect(
            self.spider_closed,
            signal=self.crawler.signals.spider_closed
        )

    def spider_closed(self):
        jobdir = self.settings.get('JOBDIR')
        if jobdir:
            self.logger.info(f"爬取完成，状态目录: {jobdir}")
```

---

## 8. 最佳实践

### 8.1 大规模数据爬取

```python
class LargeScaleSpider(Spider):
    name = "large_scale"

    custom_settings = {
        'JOBDIR': 'crawls/large-scale',
        'STREAM_FILE': 'large_data.jsonl',
        'STREAM_MODE': 'jsonl',
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0.25,
        'MEMUSAGE_ENABLED': True,
        'MEMUSAGE_LIMIT_MB': 1024,
    }
```

### 8.2 长时间运行任务

```python
class LongRunningSpider(Spider):
    name = "long_running"

    custom_settings = {
        'JOBDIR': 'crawls/long-running',
        'STREAM_FILE': 'data.jsonl',
        'STREAM_MODE': 'jsonl',
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 4.0,
    }

    custom_settings_logging = {
        'LOG_LEVEL': 'INFO',
    }
```

### 8.3 安全爬取

```python
class SafeSpider(Spider):
    name = "safe_crawl"

    custom_settings = {
        'JOBDIR': 'crawls/safe',
        'STREAM_FILE': 'safe_data.jsonl',
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'DOWNLOAD_DELAY': 2.0,
        'ROBOTSTXT_OBEY': True,
    }
```

---

## 9. 监控和调试

### 9.1 实时查看输出

```bash
# 实时查看 JSONL 输出
tail -f output.jsonl

# 实时查看行数
wc -l output.jsonl

# 实时查看文件大小
watch -n 1 'ls -lh output.jsonl'
```

### 9.2 查看爬取状态

```python
class DebugSpider(Spider):
    name = "debug"

    custom_settings = {
        'JOBDIR': 'crawls/debug',
        'STREAM_FILE': 'debug.jsonl',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item_count = 0

    def parse(self, response: Response):
        self.item_count += 1

        if self.item_count % 100 == 0:
            self.logger.info(f"已处理 {self.item_count} 条数据")

        yield {'index': self.item_count}
```

### 9.3 状态检查脚本

```python
import os
import json

def check_crawl_status(jobdir):
    if not os.path.exists(jobdir):
        print("状态目录不存在")
        return

    files = os.listdir(jobdir)
    print(f"状态文件: {files}")

    queue_file = os.path.join(jobdir, 'requests.queue')
    if os.path.exists(queue_file):
        size = os.path.getsize(queue_file)
        print(f"队列大小: {size} bytes")

check_crawl_status('crawls/large-scale')
```

---

## 10. 实战示例

### 10.1 商品数据采集

```python
import json
from datetime import datetime
from scrapling.spiders import Spider, Response

class ProductCollector(Spider):
    name = "product_collector"
    start_urls = [
        f"https://example.com/category/{cat}/page/{i}"
        for cat in ['electronics', 'clothing', 'books']
        for i in range(1, 51)
    ]

    custom_settings = {
        'JOBDIR': 'crawls/products',
        'STREAM_FILE': 'products.jsonl',
        'STREAM_MODE': 'jsonl',
        'CONCURRENT_REQUESTS': 8,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 1.0,
    }

    def parse(self, response: Response):
        for product in response.css('.product-item'):
            item = {
                'name': product.css('.name::text').get(),
                'price': product.css('.price::text').get(),
                'rating': product.css('.rating::text').get(),
                'category': response.url.split('/')[-3],
                'page': response.url.split('/')[-1],
                'url': response.urljoin(product.css('a::attr(href)').get()),
                'scraped_at': datetime.now().isoformat()
            }
            self.stream_write(json.dumps(item))
```

### 10.2 新闻文章采集

```python
class NewsCollector(Spider):
    name = "news_collector"
    start_urls = ["https://example.com/news"]

    custom_settings = {
        'JOBDIR': 'crawls/news',
        'STREAM_FILE': 'news.jsonl',
        'CONCURRENT_REQUESTS': 4,
        'DOWNLOAD_DELAY': 2.0,
    }

    def parse(self, response: Response):
        article_links = response.css('.article-title a::attr(href)').getall()

        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        next_page = response.css('.pagination a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page)

    def parse_article(self, response: Response):
        item = {
            'title': response.css('h1.title::text').get(),
            'author': response.css('.author::text').get(),
            'date': response.css('.date::text').get(),
            'content': ' '.join(response.css('.content p::text').getall()),
            'url': response.url,
            'scraped_at': datetime.now().isoformat()
        }
        self.stream_write(json.dumps(item))
```
