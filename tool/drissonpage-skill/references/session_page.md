# SessionPage 参考

本文档详细介绍 SessionPage 的使用方法。

## 概述

SessionPage 是 DrissionPage 的无浏览器模式，使用 requests 库直接收发数据包。
适合静态页面数据采集，无需启动浏览器，性能更好。

## 创建对象

### 直接创建

```python
from DrissionPage import SessionPage

page = SessionPage()
```

### 使用配置创建

```python
from DrissionPage import SessionPage, SessionOptions

so = SessionOptions().set_proxies(http='127.0.0.1:1080')
page = SessionPage(session_or_options=so)
```

### 不使用 ini 文件

```python
so = SessionOptions(read_file=False)
so.set_retry(5)
page = SessionPage(so)
```

### 传递 Session 对象

多个页面对象共享一个 Session：

```python
page1 = SessionPage()
session = page1.session
page2 = SessionPage(session_or_options=session)
```

---

## 访问网页

### GET 请求

```python
page.get('https://example.com')
page.get('https://example.com', params={'key': 'value'})
```

### POST 请求

```python
page.post('https://example.com/api', data={'key': 'value'})
page.post('https://example.com/api', json={'key': 'value'})
```

### 其他请求

```python
page.put('url', data={})
page.delete('url')
page.patch('url', data={})
page.head('url')
page.options('url')
```

---

## 页面属性

| 属性 | 说明 |
|------|------|
| `url` | 当前 URL |
| `title` | 页面标题 |
| `html` | 页面 HTML |
| `json` | 页面 JSON 数据 |
| `status_code` | 响应状态码 |
| `headers` | 响应头 |
| `cookies` | cookies |
| `session` | 内置 Session 对象 |

---

## 元素查找

与 ChromiumPage 相同的语法：

```python
ele = page.ele('#id')
ele = page.ele('@name=value')
ele = page.ele('text=登录')
eles = page.eles('tag:a')
```

---

## 请求设置

### 设置请求头

```python
page.headers.update({'Authorization': 'Bearer token'})
page.headers.update({'User-Agent': 'Mozilla/5.0...'})
```

### 设置代理

```python
page.proxies.update({'http': 'http://proxy.com', 'https': 'https://proxy.com'})
```

### 设置 Cookie

```python
page.cookies.set('name', 'value')
```

### 设置超时

```python
page.timeout = 30
```

---

## SessionOptions 配置

### 常用配置

| 方法 | 说明 |
|------|------|
| `set_proxies()` | 设置代理 |
| `set_headers()` | 设置请求头 |
| `set_cookies()` | 设置 cookies |
| `set_auth()` | 设置认证 |
| `set_retry()` | 设置重试次数 |
| `set_timeout()` | 设置超时 |

```python
so = SessionOptions()
so.set_proxies(http='127.0.0.1:1080')
so.set_headers({'User-Agent': 'Mozilla/5.0...'})
so.set_retry(5)
so.set_timeout(30)
```
