# Scrapling 域阻断

## 简介

域阻断（Domain Blocking）是 Scrapling 的一项重要功能，允许在抓取过程中阻止对特定域名的请求。这在处理包含大量第三方追踪资源的复杂网页时特别有用，可以减少不必要的网络请求、提高抓取效率并保护隐私。

## 使用场景

### 为什么要阻断域名

- **屏蔽广告和追踪器**：阻止广告网络、分析工具的请求
- **减少无效请求**：跳过社交媒体组件、评论系统等
- **保护隐私**：防止意外发送用户数据到第三方
- **提高速度**：减少页面加载时间和带宽消耗
- **规避反爬**：避免触发追踪器的反爬机制

### 典型需要阻断的域名类型

```
┌─────────────────────────────────────────────────────┐
│                   常见阻断类型                       │
├─────────────────────────────────────────────────────┤
│  • Google Analytics (google-analytics.com)         │
│  • Google Ads (doubleclick.net, googlesyndication) │
│  • Facebook (facebook.net, fbcdn.net)              │
│  • Twitter (twimg.com)                             │
│  • Hotjar (hotjar.com)                             │
│  • Intercom (intercom.io)                          │
│  • Cloudflare (cloudflare.com 特定路径)            │
│  • 其他第三方追踪器                                 │
└─────────────────────────────────────────────────────┘
```

## 基础用法

### 在 DynamicFetcher 中使用域阻断

```python
from scrapling.fetchers import DynamicFetcher

# 创建阻断列表
block_list = [
    'google-analytics.com',
    'doubleclick.net',
    'facebook.net',
    'hotjar.com'
]

# 创建带阻断的 Fetcher
fetcher = DynamicFetcher(block_domains=block_list)

# 获取页面时会自动阻断列表中的域名
page = fetcher.fetch('https://example.com')
```

### 在 StealthyFetcher 中使用

```python
from scrapling.fetchers import StealthyFetcher

# 阻断追踪器和分析域名
fetcher = StealthyFetcher(
    block_domains=[
        'google-analytics.com',
        'googletagmanager.com',
        'facebook.net',
        'hotjar.com',
        'intercom.io',
        'segment.io'
    ],
    headless=True
)

page = fetcher.fetch('https://example.com')
```

### 初始化后添加阻断

```python
fetcher = DynamicFetcher()

# 添加阻断域名
fetcher.block_domain('ads.example.com')
fetcher.block_domain('tracker.example.com')
fetcher.block_domain('analytics.example.com')

# 批量添加
fetcher.block_domains(['domain1.com', 'domain2.com'])
```

## 动态管理阻断列表

### 添加阻断

```python
fetcher = DynamicFetcher()

# 单个添加
fetcher.block_domain('new-tracker.com')

# 批量添加
fetcher.block_domains([
    'tracker1.com',
    'tracker2.com',
    'ad-server.com'
])
```

### 移除阻断

```python
fetcher = DynamicFetcher(block_domains=['a.com', 'b.com'])

# 移除单个
fetcher.unblock_domain('a.com')

# 移除多个
fetcher.unblock_domains(['b.com', 'c.com'])

# 清除所有
fetcher.clear_blocked_domains()
```

### 查询阻断状态

```python
fetcher = DynamicFetcher(block_domains=['a.com', 'b.com'])

# 获取所有阻断域名
blocked = fetcher.get_blocked_domains()
print(blocked)  # ['a.com', 'b.com']

# 检查域名是否被阻断
print(fetcher.is_blocked('a.com'))  # True
print(fetcher.is_blocked('c.com'))  # False
```

## 阻断规则

### 精确匹配

```python
# 只阻断 exact 域名
fetcher = DynamicFetcher(
    block_domains=['google-analytics.com']
)

# 会被阻断
# - https://www.google-analytics.com/analytics.js

# 不会被阻断
# - https://sub.google-analytics.com/analytics.js
```

### 子域名匹配

```python
# 使用通配符阻断主域名及所有子域名
fetcher = DynamicFetcher(
    block_domains=['*.google.com', '*.doubleclick.net']
)

# 会被阻断的域名示例:
# - www.google.com
# - mail.google.com
# - analytics.google.com
# - www.doubleclick.net
# - ad.doubleclick.net
```

### 子路径阻断

```python
# 阻断特定路径（需要自定义实现）
fetcher = DynamicFetcher()

# 自定义阻断逻辑
def should_block_request(url, resource_type):
    blocked_paths = [
        '/analytics',
        '/tracking',
        '/ads',
        '/pixel'
    ]
    
    for path in blocked_paths:
        if path in url:
            return True
    return False
```

### 基于资源类型阻断

```python
# 只阻断特定类型的请求
fetcher = DynamicFetcher(
    block_domains=['tracker.com'],
    block_resource_types=['image', 'script', 'xhr']
)

# 可选的资源类型:
# - image: 图片
# - script: JavaScript
# - xhr: XMLHttpRequest
# - fetch: Fetch 请求
# - websocket: WebSocket
# - stylesheet: CSS
# - document: 文档
# - media: 媒体文件
# - font: 字体
```

## 高级配置

### 阻断策略

```python
from scrapling.fetchers import DynamicFetcher

# 不同的阻断策略
fetcher = DynamicFetcher(
    block_domains=['tracker.com'],
    block_strategy='abort',  # 中断请求
    # 可选: 'abort', 'abort-promise', 'continue'
)
```

### 记录阻断日志

```python
fetcher = DynamicFetcher(
    block_domains=['tracker.com'],
    log_blocked=True,  # 记录被阻断的请求
    log_file='blocked.log'
)

page = fetcher.fetch('https://example.com')

# 查看阻断日志
# 可以在 blocked.log 中查看
```

### 自定义阻断逻辑

```python
class CustomBlocker:
    """自定义阻断器"""
    
    def __init__(self):
        self.blocked_domains = set()
        self.custom_rules = []
    
    def add_domain(self, domain):
        self.blocked_domains.add(domain)
    
    def should_block(self, url, domain):
        # 检查是否在阻断列表
        if domain in self.blocked_domains:
            return True
        
        # 检查自定义规则
        for rule in self.custom_rules:
            if rule(url, domain):
                return True
        
        return False
    
    def add_rule(self, func):
        """添加自定义阻断规则"""
        self.custom_rules.append(func)

# 使用自定义阻断器
blocker = CustomBlocker()
blocker.add_domain('tracker.com')
blocker.add_rule(lambda url, domain: 'ads' in url)

fetcher = DynamicFetcher(blocker=blocker)
```

### 动态阻断规则

```python
from scrapling.fetchers import DynamicFetcher

class DynamicBlocker:
    """基于请求内容的动态阻断"""
    
    def __init__(self):
        self.block_count = {}
    
    def should_block(self, url, domain):
        # 基于频率阻断
        count = self.block_count.get(domain, 0)
        if count > 10:  # 同一域名请求超过10次
            return True
        
        # 记录请求
        self.block_count[domain] = count + 1
        
        # 阻断已知的追踪器
        trackers = ['google-analytics', 'facebook', 'hotjar']
        return any(t in domain for t in trackers)

fetcher = DynamicFetcher(blocker=DynamicBlocker())
```

## 与代理轮换结合

### 组合使用

```python
from scrapling import ProxyRotator
from scrapling.fetchers import StealthyFetcher

# 配置代理轮换
proxies = ['http://proxy1:8080', 'http://proxy2:8080']
rotator = ProxyRotator(proxies)

# 配置域阻断
blocked = ['google-analytics.com', 'doubleclick.net']

# 创建 Fetcher
fetcher = StealthyFetcher(
    rotator=rotator,
    block_domains=blocked,
    headless=True
)

page = fetcher.fetch('https://example.com')
```

### 根据阻断状态切换代理

```python
class ProxyWithBlock:
    """根据阻断情况切换代理"""
    
    def __init__(self, proxies):
        self.rotator = ProxyRotator(proxies)
        self.blocked_count = 0
    
    def on_block(self, domain):
        """当请求被阻断时的回调"""
        self.blocked_count += 1
        
        # 如果阻断太多，切换代理
        if self.blocked_count > 5:
            self.rotator.next()
            self.blocked_count = 0

# 使用
manager = ProxyWithBlock(proxies)
fetcher = DynamicFetcher(...)
fetcher.on_block = manager.on_block
```

## 实际应用场景

### 场景1：快速抓取博客内容

```python
from scrapling.fetchers import DynamicFetcher

# 只允许获取主要内容，阻断无关资源
fetcher = DynamicFetcher(
    block_domains=[
        # 广告
        'doubleclick.net',
        'googlesyndication.com',
        'amazon-adsystem.com',
        # 分析
        'google-analytics.com',
        'segment.io',
        'mixpanel.com',
        # 社交
        'facebook.net',
        'platform.twitter.com',
        # 聊天
        'intercom.io',
        'drift.com'
    ],
    block_resource_types=['image', 'media', 'font'],
    headless=True
)

page = fetcher.fetch('https://blog.example.com/post/1')
content = page.css('.article-content::text').getall()
print(content)
```

### 场景2：电商价格监控

```python
from scrapling.fetchers import StealthyFetcher
import json

# 阻断分析追踪
fetcher = StealthyFetcher(
    block_domains=[
        'google-analytics.com',
        'facebook.net',
        'hotjar.com',
        'criteo.com',
        'outbrain.com'
    ],
    headless=True,
    solve_cloudflare=True
)

# 监控多个商品页面
products = ['/product/1', '/product/2', '/product/3']

prices = []
for path in products:
    page = fetcher.fetch(f'https://shop.example.com{path}')
    price = page.css('.price::text').re_first(r'\d+\.\d{2}')
    prices.append({'product': path, 'price': price})

with open('prices.json', 'w') as f:
    json.dump(prices, f)
```

### 场景3：登录后数据抓取

```python
from scrapling.fetchers import StealthySession

with StealthySession(headless=True) as session:
    # 阻断追踪器保护隐私
    session.block_domains([
        'google-analytics.com',
        'facebook.net',
        'intercom.io'
    ])
    
    # 登录
    session.fetch('https://app.example.com/login',
                 method='POST',
                 data={'email': 'user@example.com', 'password': 'pass'})
    
    # 获取数据
    page = session.fetch('https://app.example.com/dashboard')
    data = page.css('.data-item::text').getall()
    print(data)
```

## 性能优化

### 阻断的好处

1. **减少网络请求**：阻断追踪器和广告请求
2. **加快页面加载**：跳过不必要的资源
3. **降低带宽消耗**：特别是移动网络环境
4. **减少数据泄露**：避免发送用户信息到第三方

### 配置建议

```python
# 推荐的基础阻断配置
fetcher = DynamicFetcher(
    block_domains=[
        # 广告
        'doubleclick.net',
        'googlesyndication.com',
        'adnxs.com',
        'criteo.com',
        # 分析
        'google-analytics.com',
        'mixpanel.com',
        'amplitude.com',
        # 社交
        'facebook.net',
        'platform.twitter.com',
    ],
    block_resource_types=['image', 'media'],  # 根据需要调整
    headless=True
)
```

### 监控阻断效果

```python
class BlockStats:
    """阻断统计"""
    
    def __init__(self):
        self.blocked_domains = {}
        self.total_requests = 0
    
    def record_block(self, domain):
        self.blocked_domains[domain] = self.blocked_domains.get(domain, 0) + 1
    
    def record_request(self):
        self.total_requests += 1
    
    def get_stats(self):
        blocked = sum(self.blocked_domains.values())
        return {
            'total_requests': self.total_requests,
            'blocked_requests': blocked,
            'block_rate': blocked / self.total_requests if self.total_requests else 0,
            'top_blocked': sorted(self.blocked_domains.items(), 
                                key=lambda x: x[1], 
                                reverse=True)[:10]
        }

stats = BlockStats()
fetcher = DynamicFetcher(...)
fetcher.on_block = stats.record_block
fetcher.on_request = stats.record_request
```

## 常见问题

### Q1: 阻断后请求会怎样？

被阻断的请求会被取消，不会加载对应资源。在浏览器开发者工具的网络标签中会看到状态为 "(blocked)" 的请求。

### Q2: 如何查看哪些域名被阻断？

```python
fetcher = DynamicFetcher(block_domains=['a.com', 'b.com'])

# 获取阻断列表
blocked = fetcher.get_blocked_domains()

# 或者开启日志
fetcher = DynamicFetcher(block_domains=['a.com'], log_blocked=True)
```

### Q3: 子域名阻断不生效？

确保使用正确的通配符格式：

```python
# 正确：使用通配符
block_domains=['*.google.com']

# 或者手动添加所有子域名
block_domains=['www.google.com', 'mail.google.com', 'analytics.google.com']
```

### Q4: 阻断会影响登录功能吗？

通常不会，但如果你需要与第三方登录服务交互（如 Google 登录），需要将相关域名添加到白名单：

```python
fetcher = DynamicFetcher(
    block_domains=['tracker.com'],
    # 允许 OAuth 回调
    allow_domains=['accounts.google.com', 'oauth.example.com']
)
```

## 最佳实践

### 1. 按需阻断

```python
# 不要阻断太多，保持基本功能
fetcher = DynamicFetcher(
    block_domains=[
        # 只阻断明确的追踪器
        'google-analytics.com',
        'hotjar.com',
    ]
)
```

### 2. 测试后再生产

```python
# 测试阶段不阻断，确保功能正常
fetcher = DynamicFetcher()

# 确认功能正常后，再添加阻断
fetcher.block_domains(['tracker.com'])
```

### 3. 分类管理

```python
TRACKERS = ['google-analytics.com', 'hotjar.com']
ADS = ['doubleclick.net', 'criteo.com']
SOCIAL = ['facebook.net', 'twitter.com']

# 可以按需选择
fetcher = DynamicFetcher(block_domains=TRACKERS + ADS)
```

### 4. 定期更新

```python
# 维护阻断列表，定期更新
BLOCK_LIST = {
    'advertising': [...],
    'analytics': [...],
    'social': [...],
}

# 根据需要选择分类
fetcher = DynamicFetcher(
    block_domains=BLOCK_LIST['analytics'] + BLOCK_LIST['advertising']
)
```

## 相关链接

- [会话管理](./session-management.md)
- [代理轮换](./proxy-rotation.md)
