# Fetcher 基础 HTTP 请求

## 概述

Fetcher 是 Scrapling 框架中最基础的 HTTP 请求获取器，基于 httpx 库实现。它提供了简单易用的 API 来发送 HTTP 请求并获取响应，同时与 Scrapling 的解析引擎无缝集成。

## 安装

```bash
pip install scrapling
pip install "scrapling[fetchers]"
```

## 基本用法

### 创建 Fetcher 实例

```python
from scrapling.fetchers import Fetcher

# 创建默认获取器
fetcher = Fetcher()

# 创建带配置的获取器
fetcher = Fetcher(
    timeout=30,           # 超时时间（秒）
    retries=3,            # 重试次数
    retry_delay=2,        # 重试间隔（秒）
    verify=True,          # SSL 验证
    follow_redirects=True # 跟随重定向
)
```

### 发送请求

```python
from scrapling.fetchers import Fetcher

fetcher = Fetcher()

# GET 请求
page = fetcher.fetch('https://example.com')

# 获取响应内容
print(page.text)      # 响应文本
print(page.html)      # HTML 内容
print(page.body)      # 原始响应体
print(page.status)    # HTTP 状态码
print(page.url)       # 最终 URL
print(page.headers)   # 响应头
```

## 请求参数

### URL 参数

```python
fetcher = Fetcher()

# 查询参数
page = fetcher.fetch('https://api.example.com/search', params={
    'q': 'python',
    'page': 1,
    'limit': 10
})

# 完整 URL: https://api.example.com/search?q=python&page=1&limit=10
```

### POST 请求

```python
# 表单数据
page = fetcher.fetch('https://example.com/login', method='POST', data={
    'username': 'admin',
    'password': 'password123'
})

# JSON 数据
page = fetcher.fetch('https://api.example.com/users', method='POST', json={
    'name': '张三',
    'email': 'zhangsan@example.com'
})

# 多部分表单
page = fetcher.fetch('https://example.com/upload', method='POST', files={
    'file': open('document.pdf', 'rb')
})
```

### 请求头

```python
fetcher = Fetcher()

# 自定义请求头
page = fetcher.fetch('https://example.com', headers={
    'User-Agent': 'MyScraper/1.0',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://google.com'
})

# 设置默认请求头
fetcher = Fetcher(defaults={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9'
})
```

### 超时和重试

```python
fetcher = Fetcher()

# 设置总超时
page = fetcher.fetch('https://example.com', timeout=30)

# 设置连接超时和读取超时
page = fetcher.fetch('https://example.com', timeout=(5, 30))  # (连接超时, 读取超时)

# 设置重试
page = fetcher.fetch('https://example.com', retries=3, retry_delay=2)
```

### Cookie

```python
fetcher = Fetcher()

# 发送 Cookie
page = fetcher.fetch('https://example.com', cookies={
    'session_id': 'abc123',
    'user_preference': 'dark'
})

# 从响应获取 Cookie
page = fetcher.fetch('https://example.com')
print(page.cookies)

# 加载 Cookie
fetcher.load_cookies({'session': 'value123'})

# 导出 Cookie
cookies_dict = fetcher.dump_cookies()
```

### 代理

```python
fetcher = Fetcher()

# 使用代理
page = fetcher.fetch('https://example.com', proxy='http://proxy.com:8080')

# 代理认证
page = fetcher.fetch('https://example.com', proxy='http://user:pass@proxy.com:8080')

# SOCKS 代理
page = fetcher.fetch('https://example.com', proxy='socks5://proxy.com:1080')
```

## 会话管理

```python
fetcher = Fetcher()

# 创建新会话（重置 Cookie）
fetcher.new_session()

# 指定会话 ID
fetcher.new_session(session_id='my_session')

# 清除当前会话
fetcher.clear_session()

# 获取会话 ID
print(fetcher.session_id)
```

## 选择器集成

Fetcher 返回的对象直接支持 CSS 和 XPath 选择器。

```python
fetcher = Fetcher()

page = fetcher.fetch('https://example.com')

# CSS 选择器
titles = page.css('h1::text').getall()
items = page.css('.product .title').getall()

# XPath 选择器
links = page.xpath('//a/@href').getall()
paragraphs = page.xpath('//p/text()').getall()

# 正则表达式
emails = page.css('body::text').re(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
```

## 响应对象属性

```python
page = fetcher.fetch('https://example.com')

# 基本属性
print(page.text)          # 响应文本
print(page.html)          # HTML 内容
print(page.body)          # 原始字节
print(page.status)        # 状态码 (200, 404 等)
print(page.reason)        # 状态描述 (OK, Not Found 等)

# URL 信息
print(page.url)           # 最终 URL（处理重定向后）
print(page.urljoin('/path'))  # URL 拼接

# 头信息
print(page.headers)       # 响应头字典
print(page.encoding)      # 响应编码

# Cookie
print(page.cookies)       # Cookie 字典
```

## 错误处理

```python
from scrapling.fetchers import Fetcher, FetcherError, NetworkError, TimeoutError

fetcher = Fetcher()

# 方式1：异常捕获
try:
    page = fetcher.fetch('https://example.com')
except TimeoutError:
    print("请求超时")
except NetworkError as e:
    print(f"网络错误: {e}")
except FetcherError as e:
    print(f"获取器错误: {e}")

# 方式2：返回错误对象
result = fetcher.fetch('https://example.com', handle_errors=True)
if result.error:
    print(f"错误: {result.error_message}")
    print(f"状态码: {result.status}")
else:
    page = result.response
```

## 链式请求

```python
from scrapling.fetchers import Fetcher

fetcher = Fetcher()

# 登录
login_page = fetcher.fetch('https://example.com/login', method='POST', data={
    'username': 'user',
    'password': 'pass'
})

# 访问需要登录的页面（自动使用同一会话的 Cookie）
dashboard = fetcher.fetch('https://example.com/dashboard')

# 提取数据
user_info = dashboard.css('.user-info::text').get()
```

## 批量请求

```python
from scrapling.fetchers import Fetcher

fetcher = Fetcher()

urls = [
    'https://example.com/page1',
    'https://example.com/page2',
    'https://example.com/page3',
]

results = []
for url in urls:
    page = fetcher.fetch(url)
    results.append({
        'url': url,
        'status': page.status,
        'title': page.css('title::text').get(),
        'h1_count': len(page.css('h1').getall())
    })

print(results)
```

## SSL 配置

```python
fetcher = Fetcher()

# 禁用 SSL 验证（不推荐，仅用于测试）
page = fetcher.fetch('https://example.com', verify=False)

# 使用自定义 CA 证书
page = fetcher.fetch('https://example.com', verify='/path/to/ca.crt')

# 客户端证书
page = fetcher.fetch('https://example.com', cert='/path/to/client.crt')
```

## 完整示例

```python
from scrapling.fetchers import Fetcher

def crawl_website():
    fetcher = Fetcher(timeout=30, retries=3)

    results = {
        'title': None,
        'headings': [],
        'links': [],
        'metadata': {}
    }

    try:
        page = fetcher.fetch('https://example.com')

        results['title'] = page.css('title::text').get()
        results['headings'] = page.css('h1::text').getall()
        results['links'] = page.css('a::attr(href)').getall()
        results['metadata'] = {
            'description': page.css('meta[name="description"]::attr(content)').get(),
            'keywords': page.css('meta[name="keywords"]::attr(content)').get()
        }

        return results

    except Exception as e:
        print(f"抓取失败: {e}")
        return None

if __name__ == '__main__':
    data = crawl_website()
    if data:
        print(f"标题: {data['title']}")
        print(f"H1 数量: {len(data['headings'])}")
        print(f"链接数量: {len(data['links'])}")
```

## 相关链接

- [StealthyFetcher 反检测抓取](./stealthy-fetcher.md)
- [DynamicFetcher 动态网站抓取](./dynamic-fetcher.md)
- [官方文档](https://scrapling.readthedocs.io/en/latest/fetchers.html)
